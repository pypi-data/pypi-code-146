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

"""Membership program related Entity classes and tools."""

from __future__ import annotations
from datetime import timedelta

from . import core
from .. import typehints as th


class MembershipOption(core.BasicInfo):
    """
    Represents a membership offering, used as a template for a membership agreement.
    """

    # General information
    duration: timedelta
    membership_category: str
    limit_on_classes: th.Any  # Todo: Figure out proper type of field
    auto_renewal: bool

    # Billing information
    installment_plan: str  # Todo: shortlist of payment frequencies
    number_of_installments: int
    signup_fee: float
    installment_amount: float
    add_service_tax: bool
    add_retail_tax: bool
    income_category: th.Any  # TODO: What is this for again?

    # Programs & Classes
    # TODO: Reference the list of programs and training classes in which students can
    #       participate under this option.

    active: bool
