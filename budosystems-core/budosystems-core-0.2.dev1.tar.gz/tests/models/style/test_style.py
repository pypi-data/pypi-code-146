#
#  Copyright (c) 2021.  Budo Systems
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#

from collections.abc import Set

class TestBusiness:
    def test_business_has_set(self, budo_business):
        assert isinstance(budo_business.studios, Set)
        assert len(budo_business.studios) == 0

    def test_add_studio(self, budo_business, cyber_studio):
        budo_business.add_studio(cyber_studio)
        assert cyber_studio in budo_business.studios
        assert budo_business in cyber_studio.businesses

    def test_remove_studio(self, multi_business, cyber_studio, bnm_studio):
        multi_business.remove_studio(cyber_studio)
        assert cyber_studio not in multi_business.studios
        assert bnm_studio in multi_business.studios
        assert multi_business not in cyber_studio.businesses
        assert multi_business in bnm_studio.businesses

class TestStudio:
    def test_studio_has_sets(self, cyber_studio):
        # Businesses
        assert isinstance(cyber_studio.businesses, Set)
        assert len(cyber_studio.businesses) == 0

        # Styles
        assert isinstance(cyber_studio.styles, Set)
        assert len(cyber_studio.styles) == 0

    def test_add_business(self, cyber_studio, budo_business):
        cyber_studio.add_business(budo_business)
        assert budo_business in cyber_studio.businesses
        assert cyber_studio in budo_business.studios

    def test_remove_business(self, shared_studio, budo_business, multi_business):
        shared_studio.remove_business(budo_business)
        assert budo_business not in shared_studio.businesses
        assert multi_business in shared_studio.businesses
        assert shared_studio not in budo_business.studios
        assert shared_studio in multi_business.studios

    def test_add_style(self, cyber_studio, ameridote_style):
        cyber_studio.add_style(ameridote_style)
        assert ameridote_style in cyber_studio.styles
        assert cyber_studio in ameridote_style.studios

    def test_remove_style(self, versa_studio, ameridote_style, uniq_style):
        versa_studio.remove_style(ameridote_style)
        assert ameridote_style not in versa_studio.styles
        assert uniq_style in versa_studio.styles
        assert versa_studio not in ameridote_style.studios
        assert versa_studio in uniq_style.studios

class TestStyle:
    def test_style_has_set(self, uniq_style):
        assert isinstance(uniq_style.studios, Set)
        assert len(uniq_style.studios) == 0

    def test_add_studio(self, uniq_style, cyber_studio):
        uniq_style.add_studio(cyber_studio)
        assert cyber_studio in uniq_style.studios
        assert uniq_style in cyber_studio.styles

    def test_remove_studio(self, karate_style, cyber_studio, bnm_studio):
        karate_style.remove_studio(cyber_studio)
        assert cyber_studio not in karate_style.studios
        assert bnm_studio in karate_style.studios
        assert karate_style not in cyber_studio.styles
        assert karate_style in bnm_studio.styles

