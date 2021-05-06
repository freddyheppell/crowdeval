"""Automatically determines thresholds of ranking algorithm."""

import click

from crowdeval.posts.support.scoring import BayesianRatingCalculator, ScoreEnum

MIN = 1
MAX = 6

SCORE_VALUES = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}


def test_singles():
    """Test how many ratings are required for a single score."""
    print("== Testing single ratings ==")
    for s in range(MIN, MAX):
        print("Testing score", ScoreEnum(s))

        c = 0
        width = 999

        while width > 1:
            c += 1
            score_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
            score_counts[s] = c
            calculator = BayesianRatingCalculator(score_counts, SCORE_VALUES)
            width = calculator.get_credible_width()

        print("Requires", c)
    print("\n\n")


def test_uniform():
    """Test how many ratings are required for each score."""
    print("== Testing uniform ratings ==")
    width = 999
    c = 0

    while width > 1:
        score_counts = {1: c, 2: c, 3: c, 4: c, 5: c}
        calculator = BayesianRatingCalculator(score_counts, SCORE_VALUES)
        width = calculator.get_credible_width()

        c += 1

    print("Requires", c)
    print("\n\n")


def test_polarised():
    """Test how many ratings are required for the lowest and highest scores."""
    print("== Testing Polarised ==")
    width = 999
    c = 0

    while width > 1:
        score_counts = {1: c, 2: 0, 3: 0, 4: 0, 5: c}
        calculator = BayesianRatingCalculator(score_counts, SCORE_VALUES)
        width = calculator.get_credible_width()

        c += 1

    print("Requires", c)
    print("\n\n")


def test_score_progression(review):
    """Report the upper/lower boundaries at each review count.

    Outputs in LaTeX pgfplots point format.
    """
    print("TESTING", ScoreEnum(review))
    print("n,width,lower,upper")

    lowers = []
    uppers = []

    for i in range(1, 31):
        score_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        score_counts[review] = i

        calculator = BayesianRatingCalculator(score_counts, SCORE_VALUES)

        low = calculator.get_lower_bound()
        upp = calculator.get_upper_bound()

        lowers.append((i, round(low, 3)))
        uppers.append((i, round(upp, 3)))

    print("LOWERS")
    for lower in lowers:
        print(lower, end="")
    print()
    print("UPPERS")
    for upper in uppers:
        print(upper, end="")

    print("\n\n\n\n\n\n")


@click.command()
def test_review_thresholds():
    """Execute tests of the ranking algorithm's thresholds."""
    test_singles()
    test_uniform()
    test_polarised()

    print("Testing polarised reviews")
    test_score_progression(5)
    test_score_progression(4)
    test_score_progression(3)
    test_score_progression(2)
    test_score_progression(1)
