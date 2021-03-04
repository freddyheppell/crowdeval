"""Routes for login."""
from flask import flash, redirect, url_for
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from flask_dance.contrib.twitter import make_twitter_blueprint
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy.orm.exc import NoResultFound

from crowdeval.extensions import db, login_manager
from crowdeval.users.models import OAuth, User


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


blueprint = make_twitter_blueprint(
    login_url="/login/twitter",
    authorized_url="/login/twitter/authorized",
    storage=SQLAlchemyStorage(OAuth, db.session, user=current_user),
)


@oauth_authorized.connect_via(blueprint)
def twitter_logged_in(blueprint, token):
    """Upon succesful OAuth, create or find an existing user."""
    if not token:
        flash("Failed to log in.", category="error")
        return False

    resp = blueprint.session.get("account/verify_credentials.json?include_email=true")
    if not resp.ok:
        msg = "Failed to fetch user info."
        flash(msg, category="danger")
        return False

    info = resp.json()
    user_id = info["id_str"]

    # Find this OAuth token in the database, or create it
    query = OAuth.query.filter_by(
        provider=blueprint.name,
        provider_user_id=user_id,
    )
    try:
        oauth = query.one()
    except NoResultFound:
        oauth = OAuth(
            provider=blueprint.name,
            provider_user_id=user_id,
            token=token,
        )

    if not oauth.user:
        # Create a new local user account for this user
        print(info)
        user = User(username=info["screen_name"], email=info["email"])
        # Associate the new local user account with the OAuth token
        oauth.user = user
        # Save and commit our database models
        db.session.add_all([user, oauth])
        db.session.commit()
        # Log in the new local user account
        login_user(user)
    else:
        login_user(oauth.user)

    flash("Successfully signed in.", category="success")

    # Disable Flask-Dance's default behavior for saving the OAuth token
    return False


@blueprint.route("/logout")
@login_required
def logout():
    """Logout."""
    logout_user()
    flash("You are logged out.", "info")
    return redirect(url_for("public.index"))


@oauth_error.connect_via(blueprint)
def twitter_error(blueprint, message, response):
    """Notify upon OAuth error."""
    msg = ("OAuth error from {name}! " "message={message} response={response}").format(
        name=blueprint.name,
        message=message,
        response=response,
    )
    flash(msg, category="danger")
