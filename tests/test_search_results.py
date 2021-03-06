#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from unittestzero import Assert

from pages.home import HomePage
from pages.search_results import SearchResultsPage


class TestSearchPage:

    @pytest.mark.nondestructive
    @pytest.mark.xfail(reason='Bug 1058726 - Search button ID differs between dev and staging/prod')
    def test_no_results_returned_from_blank_search(self, mozwebqa):
        home_pg = HomePage(mozwebqa)
        home_pg.go_to_home_page()

        search_results_pg = home_pg.header_region.click_search_button()
        Assert.true(search_results_pg.is_the_current_page)
        Assert.false(search_results_pg.is_search_results_area_present, "Search Results area is present.")

        Assert.equal(search_results_pg.search_page_title, "Search", "Search Results page header mismatch.")
        Assert.equal(search_results_pg.main_search_box_text, "", "Main Search field should be empty.")

    @pytest.mark.nondestructive
    @pytest.mark.xfail(reason='Bug 1058726 - Search button ID differs between dev and staging/prod')
    def test_search_term_returned_and_matched(self, mozwebqa):
        home_pg = HomePage(mozwebqa)
        home_pg.go_to_home_page()

        home_pg.header_region.enter_text_into_search_field()
        search_results_pg = home_pg.header_region.click_search_button()
        search_results_pg.wait_for_results()
        Assert.true(search_results_pg.is_search_results_area_present, "Search Results area is not present.")

        Assert.true(search_results_pg.is_search_types_present, "Search Types are missing.")
        Assert.equal(search_results_pg.main_search_box_text, SearchResultsPage._search_term, "Main Search field should contain the term searched - " + SearchResultsPage._search_term)

        for matchedTerm in search_results_pg.get_matched_search_term_in_results:
            Assert.equal(matchedTerm.text.lower(), SearchResultsPage._search_term.lower(), "Search term was not found in matched result. Expected: " + SearchResultsPage._search_term + " but got: " + matchedTerm.text)
