from unittest import TestCase

from browser import Converters

class TestConverters(TestCase):
    def test_can_convert_percentages(self):
        test_cases = [
            (1.0,   "100%"),
            (1.0,   "100.00%"),
            (0.99,  "99.00%"),
            (0.01,  "1%"),
            (-0.01, "-1%"),
            (-0.1,  "- 10%"),
            (-0.01, "-\u2013 1%"),
            (-0.1,  "- \u2013 10%")
        ]

        for result, case in test_cases:
            self.assertEqual(result, Converters.percent(case), "Failed for {}".format(case))

    def test_can_convert_dollar_amounts(self):
        test_cases = [
            (1.0,   "1"),
            (10,   "10"),
            (10.1,  "10.1"),
            (1000,  "1,000"),
            (-1000000, "-1,000,000"),
            (1.0,   "$1"),
            (10,   "$10"),
            (10.1,  "$10.1"),
            (1000,  "$1,000"),
            (-1000000, "-$1,000,000"),
            (-1000000, "- $1,000,000"),
            (10,   "$ \u2013 10"),
            (10.1,  "\u2013 $10.1"),
        ]

        for result, case in test_cases:
            self.assertEqual(result, Converters.dollar_amount(case), "Failed for {}".format(case))
