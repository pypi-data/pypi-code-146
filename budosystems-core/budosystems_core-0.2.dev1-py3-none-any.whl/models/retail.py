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

"""Retail product related Entity classes and tools."""

from __future__ import annotations

from . import core
# from . import typehints as th


class Product(core.BasicInfo):
    """
    Represents a product for sale.
    """
    sale_price: float
    purchase_cost: float


class ProductVariant(core.BasicInfo):
    """Represents a variation on a product in the catalog."""


class Bundle(core.BasicInfo):
    """Represents a collection of products to be sold together, possible with a discount."""
