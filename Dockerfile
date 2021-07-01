# We have a hard dependency on python 3.9.4
FROM python:3.9.4

# download and install nodejs so we can run npm later on
RUN curl -fsSL https://deb.nodesource.com/setup_14.x | bash -
RUN apt-get install -y nodejs

# download tini to use as the init process when we start the container
ADD https://github.com/krallin/tini/releases/download/v0.19.0/tini /sbin/tini

# create a normal user so we don't run the service as root
RUN addgroup --gid 1001 "crowdeval" && \
      adduser --disabled-password --gecos "CrowdEval User,,," \
      --home /crowdeval --ingroup crowdeval --uid 1001 crowdeval && \
      chmod +x /sbin/tini

# copy the app into the users home folder
COPY . /crowdeval/

# Everything from here down runs as the unprivileged user account
USER crowdeval:crowdeval

# switch to working in the user home folder
WORKDIR /crowdeval

# create a virtual python environment so that we know the path to all the
# binaries and don't have to rely on installing as root
RUN python -mvenv venv

# install poetry so that we can then...
RUN venv/bin/pip install poetry
RUN venv/bin/poetry config virtualenvs.create false

# ... install all the python dependencies for the app
RUN venv/bin/poetry install --no-dev

# make sure we get all the javascript dependencies by doing
RUN npm install

# we want to run under gunicorn but it's not a dependency in the poetry config
RUN venv/bin/pip install gunicorn

# for some reason I was getting failures unless I installed factory_boy. I've
# no idea why this is and if it should be part of the poetry config but this
# fixes the problem so...
RUN venv/bin/pip install factory_boy

# Long term we may want to vary the number of threads and workers we devote to
# the app but 2 of each seems like a reasonable starting point for a demo service
ENV WORKERS=2 THREADS=2

# use the shell script to start up the container
ENTRYPOINT ["./docker-entrypoint.sh"]
