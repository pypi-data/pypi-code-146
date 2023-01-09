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

from pytest import fixture

from budosystems.models.style import (
    Business,
    Studio,
    Style
)

@fixture
def budo_business():
    return Business(name="Budo Systems", slug="budo")

@fixture
def cyber_studio():
    return Studio(name="Cyberspace", slug="cyber")

@fixture
def bnm_studio():
    return Studio(name="Brick & Mortar", slug="bnm")

@fixture
def multi_business(cyber_studio, bnm_studio):
    biz = Business(name="Multi-Location Karate", slug="multi")
    biz.add_studio(cyber_studio)
    biz.add_studio(bnm_studio)
    return biz

@fixture
def shared_studio(budo_business, multi_business):
    studio = Studio(name="Shared Studio", slug="shared")
    studio.add_business(budo_business)
    studio.add_business(multi_business)
    return studio

@fixture
def uniq_style():
    return Style(name="Uniq Style", slug="uniq")

@fixture
def ameridote_style():
    return Style(name="Ameridote Style", slug="ameridote")

@fixture
def karate_style(cyber_studio, bnm_studio):
    style = Style(name="Karate Style", slug="karate")
    style.add_studio(cyber_studio)
    style.add_studio(bnm_studio)
    return style

@fixture
def versa_studio(uniq_style, ameridote_style):
    studio = Studio(name="Versa Studio", slug="versa")
    studio.add_style(uniq_style)
    studio.add_style(ameridote_style)
    return studio
