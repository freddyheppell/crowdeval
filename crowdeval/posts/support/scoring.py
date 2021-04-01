"""Support for scoring posts."""

from collections import Counter
from enum import IntEnum
from math import sqrt


class ScoreEnum(IntEnum):
    """Represents score options."""

    TRUE = 5
    MOSTLY_TRUE = 5
    MIXED = 3
    MOSTLY_FALSE = 2
    FALSE = 1


class PostScorer:
    """Responsible for scoring a post's ratings."""

    def __init__(self, post) -> None:
        """Create a new scorer.

        post:   The post to score
        """
        self.post = post

        ratings = [(rating.rating) for rating in self.post.ratings]
        score_counts = dict(Counter(ratings))

        calculator = BayesianRatingCalculator(score_counts)

        center = calculator.get_center()

        self.width = calculator.get_credible_width()

        # Use the center-biased bound
        if center >= 3:
            self.bound = calculator.get_lower_bound()
        else:
            self.bound = calculator.get_upper_bound()

    def get_width(self):
        """Return the width of the interval."""
        return self.width

    def get_bound(self):
        """Return the center-biased bound."""
        return self.bound


class BayesianRatingCalculator:
    """Calculates the Bayesian approximation of a star rating.

    Based on this article by Evan Miller: https://www.evanmiller.org/ranking-items-with-star-ratings.html
    This algorithm performs an optimised version of the equation, check the page for the human-readable form.
    """

    def __init__(self, score_counts, score_values=None) -> None:
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
        # ... and the number of dufferent scores
        self.K = len(score_counts.keys())
        # Precomputed value for the value on a normalised normal distribution where the certainty is 95%
        self.z = 1.65

        self._credible_width = None
        self._lower_bound = None
        self._upper_bound = None

        # Throw an exception if the possible scores are inconsistent between the counts and values dicts
        if (count_keys := set(score_counts.keys())) != (
            score_keys := set(score_values.keys())
        ):
            raise Exception(
                f"The score count keys ({count_keys}) and score value keys ({score_keys}) are not consistent"
            )

    def calculate(self):
        """Perform the calculation."""
        score_sum = 0
        score_sum_sq = 0

        for score in self.score_counts.keys():
            # For each score we need to compute three summations

            # First, compute (n_k + 1) / (N+K)
            # where n_k is the number of ratings given k
            # N is the total number of ratings
            # K is the number of different assignable scores

            frac = (self.score_counts[score] + 1) / (self.N + self.K)

            # compute both s_k * frac and s_k^2 * frac
            score_sum += self.score_values[score] * frac
            score_sum_sq += (self.score_values[score] ** 2) * frac

        # Compute the variance and standard deviations
        variance = (score_sum ** 2) / (self.N + self.K + 1)
        stdev = sqrt(variance)

        # This is the credible amount the score could be above or below the expectation
        credible_diff = self.z * stdev
        # The width that the width lies in. If this is > 1 then no single score is certain
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
