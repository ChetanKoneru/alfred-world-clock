import unittest
from datetime import datetime

import pytz

import helpers
import main


class ParseArgsTest(unittest.TestCase):
    def setUp(self):
        self.home_now = pytz.timezone("America/New_York").localize(datetime(2024, 1, 1, 12, 0))

    def test_empty_args_show_current_time(self):
        _, query = main.parse_args([], self.home_now)

        self.assertEqual(query, "")

    def test_timezone_search_is_returned_as_query(self):
        _, query = main.parse_args(["Sydney"], self.home_now)

        self.assertEqual(query, "Sydney")

    def test_multiple_search_terms_are_joined(self):
        _, query = main.parse_args(["Australia", "Sydney"], self.home_now)

        self.assertEqual(query, "Australia Sydney")

    def test_search_query_passed_as_a_single_argument(self):
        _, query = main.parse_args(["Australia Sydney"], self.home_now)

        self.assertEqual(query, "Australia Sydney")

    def test_time_mode_passed_as_a_single_argument(self):
        _, query = main.parse_args(["04:20 2024-01-01"], self.home_now)

        self.assertEqual(query, "")

    def test_offset_mode_accepts_a_query(self):
        _, query = main.parse_args(["+2h", "Sydney"], self.home_now)

        self.assertEqual(query, "Sydney")

    def test_time_mode_does_not_use_a_query(self):
        _, query = main.parse_args(["04:20", "2024-01-01"], self.home_now)

        self.assertEqual(query, "")

    def test_invalid_time_still_raises_an_error(self):
        with self.assertRaises(ValueError):
            main.parse_args(["25:99"], self.home_now)


class FilterTimezonesTest(unittest.TestCase):
    def setUp(self):
        now = datetime(2024, 1, 1, 12, 0, tzinfo=pytz.utc)
        self.timezones = {
            "Australia/Sydney": now,
            "Australia/Perth": now,
            "Europe/Paris": now,
            "America/New_York": now,
            "Africa/Abidjan": now,
        }

    def test_empty_query_returns_every_timezone(self):
        self.assertEqual(
            helpers.filter_timezones(self.timezones, "", {}),
            self.timezones,
        )

    def test_filter_by_city(self):
        self.assertEqual(
            set(helpers.filter_timezones(self.timezones, "sydney", {})),
            {"Australia/Sydney"},
        )

    def test_filter_by_country(self):
        self.assertEqual(
            set(helpers.filter_timezones(self.timezones, "australia", {})),
            {"Australia/Sydney", "Australia/Perth"},
        )

    def test_filter_by_timezone_name(self):
        self.assertEqual(
            set(helpers.filter_timezones(self.timezones, "europe/paris", {})),
            {"Europe/Paris"},
        )

    def test_filter_with_multiple_terms(self):
        self.assertEqual(
            set(helpers.filter_timezones(self.timezones, "aus syd", {})),
            {"Australia/Sydney"},
        )

    def test_filter_ignores_punctuation(self):
        self.assertEqual(
            set(helpers.filter_timezones(self.timezones, "Sydney, Australia", {})),
            {"Australia/Sydney"},
        )

    def test_filter_by_friendly_name_and_original_city(self):
        replacements = {"Sydney": "Home"}

        self.assertEqual(
            set(helpers.filter_timezones(self.timezones, "home", replacements)),
            {"Australia/Sydney"},
        )
        self.assertEqual(
            set(helpers.filter_timezones(self.timezones, "sydney", replacements)),
            {"Australia/Sydney"},
        )

    def test_filter_ignores_accents(self):
        self.assertEqual(
            set(helpers.filter_timezones(self.timezones, "cote d'ivoire", {})),
            {"Africa/Abidjan"},
        )

    def test_filter_without_matches_returns_no_timezones(self):
        self.assertEqual(
            helpers.filter_timezones(self.timezones, "not-a-place", {}),
            {},
        )


if __name__ == "__main__":
    unittest.main()
