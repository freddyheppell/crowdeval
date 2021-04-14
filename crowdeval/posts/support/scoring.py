"""Support for scoring posts."""

from collections import Counter
from enum import IntEnum
from itertools import starmap
from math import inf, sqrt


class ScoreEnum(IntEnum):
    """Represents score options."""

    TRUE = 5
    MOSTLY_TRUE = 4
    MIXED = 3
    MOSTLY_FALSE = 2
    FALSE = 1


class WeightedAverageSimilarPostScorer:
    """Returns the score of similar posts."""

    def __init__(self, similar_posts, scores) -> None:
        """Create a new weighted average scorer for similar posts."""
        self.similar_posts = zip(similar_posts, scores)

    def _process_post(self, post, score) -> int:
        """Convert elasticsearch cosine similarity scores into 0-01 range."""
        scorer = PostScorer(post)
        # Spread out values: 1.75 -> 0, 2 -> 1
        weight = (score - 1.75) * 4
        weighted_score = scorer.get_bound() * weight

        return weighted_score, weight

    def get_score(self) -> float:
        """Get the weighted average."""
        similar_post_scores = list(starmap(self._process_post, self.similar_posts))

        if len(similar_post_scores) > 1:
            sum_weighted_scores, sum_weights = tuple(
                sum(x) for x in zip(*similar_post_scores)
            )
        else:
            sum_weighted_scores, sum_weights = similar_post_scores[0]

        return sum_weighted_scores / sum_weights


class PostScorer:
    """Responsible for scoring a post's ratings."""

    def __init__(self, post) -> None:
        """Create a new scorer.

        post:   The post to score
        """
        self.post = post

        ratings = [(rating.rating) for rating in self.post.ratings]
        score_counts = dict(Counter(ratings))
        score_values = dict(zip(list(map(int, ScoreEnum)), list(map(int, ScoreEnum))))

        self.calculator = BayesianRatingCalculator(score_counts, score_values)

        center = self.calculator.get_center()

        self.width = self.calculator.get_credible_width()

        # Use the center-biased bound
        if center >= 3:
            self.bound = self.calculator.get_lower_bound()
        else:
            self.bound = self.calculator.get_upper_bound()

    def get_width(self):
        """Return the width of the interval."""
        return self.width

    def get_bound(self):
        """Return the center-biased bound."""
        return self.bound

    def get_calculator(self):
        """Return the current calculator instance."""
        return self.calculator


class BayesianRatingCalculator:
    """Calculates the Bayesian approximation of a star rating.

    Based on this article by Evan Miller: https://www.evanmiller.org/ranking-items-with-star-ratings.html
    This algorithm performs an optimised version of the equation, check the page for the human-readable form.
    """

    def __init__(self, score_counts, score_values) -> None:
        """Create a new rating calculator.

        score_counts:   a dict of the score (k) -> the count of that score (n_k).
        score_values:   a dict of the score (k) -> the value of the score (s_k)
                        If this argument is omitted, it will be assumed each score's value is itself.
        """
        self.score_counts = score_counts

        if score_values is None:
            # Assume score's value is itself
            score_values = dict(zip(score_counts.keys(), score_counts.keys()))
        self.score_values = score_values

        # Precalculate the total number of reviews
        self.N = sum(score_counts.values())
        # ... and the number of different scores
        self.K = len(score_values.keys())
        # Precomputed value for the value on a normalised normal distribution where the certainty is 95%
        self.z = 1.65

        self._credible_width = None
        self._lower_bound = None
        self._upper_bound = None

        count_keys = set(score_counts.keys())
        score_keys = set(score_values.keys())

        if not score_keys.issuperset(count_keys):
            raise Exception(
                f"The score value keys ({score_keys}) must be a superset of the score count keys ({count_keys})"
            )

    def calculate(self):
        """Perform the calculation."""
        score_sum = 0
        score_sum_sq = 0

        # Check if no ratings have been supplied
        if len(self.score_counts) == 0:
            # Say the credible width is infinitely wide
            self._credible_width = inf
            self._lower_bound = 0
            self._upper_bound = 0
            self._center = 0
            return

        for score in self.score_values.keys():
            # For each score we need to compute three summations

            # First, compute (n_k + 1) / (N+K)
            # where n_k is the number of ratings given k
            # N is the total number of ratings
            # K is the number of different assignable scores

            frac = (self.score_counts.get(score, 0) + 1) / (self.N + self.K)

            # compute both s_k * frac and s_k^2 * frac
            score_sum += self.score_values[score] * frac
            score_sum_sq += (self.score_values[score] ** 2) * frac

        print(score_sum)
        print(score_sum_sq)

        # Compute the variance and standard deviations
        variance = (score_sum_sq - (score_sum ** 2)) / (self.N + self.K + 1)
        print(variance)
        stdev = sqrt(variance)

        # This is the credible amount the score could be above or below the expectation
        credible_diff = self.z * stdev
        # The width that the answer lies in. If this is > 1 then no single score is certain
        self._credible_width = credible_diff * 2
        # The lower bound of the score
        self._lower_bound = score_sum - credible_diff
        # The higher bound of the score
        self._upper_bound = score_sum + credible_diff
        # In theory the 'true' score lies between these two
        # Also store the middle
        self._center = score_sum

    def get_credible_width(self):
        """Return the width of the credible interval of this score."""
        if self._credible_width is None:
            self.calculate()

        return self._credible_width

    def get_lower_bound(self):
        """Return the lower bound for this score."""
        if self._lower_bound is None:
            self.calculate()

        return self._lower_bound

    def get_upper_bound(self):
        """Return the upper bound for this score."""
        if self._upper_bound is None:
            self.calculate()

        return self._upper_bound

    def get_center(self):
        """Return the center of this score's uncertainty window."""
        if self._upper_bound is None:
            self.calculate()

        return self._center
