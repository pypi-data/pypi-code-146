# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2022 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Data model for "new product" batches
"""

from __future__ import unicode_literals, absolute_import

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declared_attr

from rattail.db.model import (Base, BatchMixin, ProductBatchRowMixin,
                              Vendor, Department, Subdepartment,
                              Category, Family, ReportCode, Brand)
from rattail.db.core import filename_column


class NewProductBatch(BatchMixin, Base):
    """
    Primary data model for new product batches.
    """
    __tablename__ = 'batch_newproduct'
    __batchrow_class__ = 'NewProductBatchRow'
    batch_key = 'newproduct'
    model_title = "New Product Batch"
    model_title_plural = "New Product Batches"

    input_filename = filename_column(nullable=True, doc="""
    Base name of the input data file, if applicable.
    """)


class NewProductBatchRow(ProductBatchRowMixin, Base):
    """
    Row of data within a new product batch.
    """
    __tablename__ = 'batch_newproduct_row'
    __batch_class__ = NewProductBatch

    @declared_attr
    def __table_args__(cls):
        return cls.__default_table_args__() + (
            sa.ForeignKeyConstraint(['vendor_uuid'], ['vendor.uuid'],
                                    name='batch_newproduct_row_fk_vendor'),
            sa.ForeignKeyConstraint(['department_uuid'], ['department.uuid'],
                                    name='batch_newproduct_row_fk_department'),
            sa.ForeignKeyConstraint(['subdepartment_uuid'], ['subdepartment.uuid'],
                                    name='batch_newproduct_row_fk_subdepartment'),
            sa.ForeignKeyConstraint(['category_uuid'], ['category.uuid'],
                                    name='batch_newproduct_row_fk_category'),
            sa.ForeignKeyConstraint(['family_uuid'], ['family.uuid'],
                                    name='batch_newproduct_row_fk_family'),
            sa.ForeignKeyConstraint(['report_uuid'], ['report_code.uuid'],
                                    name='batch_newproduct_row_fk_report'),
            sa.ForeignKeyConstraint(['brand_uuid'], ['brand.uuid'],
                                    name='batch_newproduct_row_fk_brand'),
        )

    STATUS_OK                           = 1
    STATUS_MISSING_KEY                  = 2
    STATUS_PRODUCT_EXISTS               = 3
    STATUS_VENDOR_NOT_FOUND             = 4
    STATUS_DEPT_NOT_FOUND               = 5
    STATUS_SUBDEPT_NOT_FOUND            = 6
    STATUS_CATEGORY_NOT_FOUND           = 7
    STATUS_FAMILY_NOT_FOUND             = 8
    STATUS_REPORTCODE_NOT_FOUND         = 9
    STATUS_CANNOT_CALCULATE_PRICE       = 10

    STATUS = {
        STATUS_OK                       : "ok",
        STATUS_MISSING_KEY              : "missing product key",
        STATUS_PRODUCT_EXISTS           : "product already exists",
        STATUS_VENDOR_NOT_FOUND         : "vendor not found",
        STATUS_DEPT_NOT_FOUND           : "department not found",
        STATUS_SUBDEPT_NOT_FOUND        : "subdepartment not found",
        STATUS_CATEGORY_NOT_FOUND       : "category not found",
        STATUS_FAMILY_NOT_FOUND         : "family not found",
        STATUS_REPORTCODE_NOT_FOUND     : "report code not found",
        STATUS_CANNOT_CALCULATE_PRICE   : "cannot calculate price",
    }

    vendor_id = sa.Column(sa.String(length=15), nullable=True, doc="""
    ID string for the vendor from whom product may be purchased.
    """)

    vendor_uuid = sa.Column(sa.String(length=32), nullable=True)
    vendor = orm.relationship(Vendor, doc="""
    Reference to the vendor which corresponds to :attr:`vendor_id`.  Note that
    this may be ``None`` if the ``vendor_id`` value is missing or unknown.
    """)

    vendor_item_code = sa.Column(sa.String(length=20), nullable=True, doc="""
    Vendor-specific item code (SKU) for the product.
    """)

    department_uuid = sa.Column(sa.String(length=32), nullable=True)
    department = orm.relationship(Department, doc="""
    Reference to the department which corresponds to :attr:`department_number`.
    Note that this may be ``None`` if the ``department_number`` value is
    missing or unknown.
    """)

    subdepartment_uuid = sa.Column(sa.String(length=32), nullable=True)
    subdepartment = orm.relationship(Subdepartment, doc="""
    Reference to the subdepartment which corresponds to
    :attr:`subdepartment_number`.  Note that this may be ``None`` if the
    ``subdepartment_number`` value is missing or unknown.
    """)

    category_code = sa.Column(sa.String(length=20), nullable=True, doc="""
    Category code (string value) for the item.
    """)

    category_uuid = sa.Column(sa.String(length=32), nullable=True)
    category = orm.relationship(Category, doc="""
    Reference to the category record which corresponds to
    :attr:`category_code`.  Note that this may be ``None`` if the
    ``category_code`` value is missing or unknown.
    """)

    family_code = sa.Column(sa.Integer(), nullable=True, doc="""
    Family code (integer value) for the item.
    """)

    family_uuid = sa.Column(sa.String(length=32), nullable=True)
    family = orm.relationship(Family, doc="""
    Reference to the "family code" record which corresponds to
    :attr:`family_code`.  Note that this may be ``None`` if the ``family_code``
    value is missing or unknown.
    """)

    report_code = sa.Column(sa.Integer(), nullable=True, doc="""
    Report code (integer value) for the item.
    """)

    report_uuid = sa.Column(sa.String(length=32), nullable=True)
    report = orm.relationship(ReportCode, doc="""
    Reference to the "report code" record which corresponds to
    :attr:`report_code`.  Note that this may be ``None`` if the ``report_code``
    value is missing or unknown.
    """)

    brand_uuid = sa.Column(sa.String(length=32), nullable=True)
    brand = orm.relationship(Brand, doc="""
    Reference to the brand which corresponds to :attr:`brand_name`.  Note that
    this may be ``None`` if the ``brand_name`` value is missing or unknown.
    """)

    unit_size = sa.Column(sa.Numeric(precision=8, scale=3), nullable=True, doc="""
    Unit size for product; see also
    :attr:`~rattail.db.model.products.Product.unit_size`.
    """)

    unit_of_measure = sa.Column(sa.String(length=4), nullable=True, doc="""
    Unit of measure for product; see also
    :attr:`~rattail.db.model.products.Product.unit_of_measure`.
    """)

    unit_of_measure_entry = sa.Column(sa.String(length=20), nullable=True, doc="""
    Raw entry string for the unit of measure.  This would be e.g. ``'ml'``
    for milliliters, as opposed to ``enum.UNIT_OF_MEASURE_MILLILITER``.
    """)

    weighed = sa.Column(sa.Boolean(), nullable=True, doc="""
    Whether or not the product must be weighed to determine its final price.
    """)

    case_size = sa.Column(sa.Numeric(precision=9, scale=4), nullable=True, doc="""
    Number of units which constitute a "case" of product.  May be a fractional
    quantity, e.g. 17.5 (LB).
    """)

    case_cost = sa.Column(sa.Numeric(precision=10, scale=5), nullable=True, doc="""
    Cost per case of the product.
    """)

    unit_cost = sa.Column(sa.Numeric(precision=10, scale=5), nullable=True, doc="""
    Cost per unit of the product.
    """)

    regular_price = sa.Column(sa.Numeric(precision=8, scale=3), nullable=True, doc="""
    Regular price for the item.
    """)

    regular_price_multiple = sa.Column(sa.Integer(), nullable=True, doc="""
    Regular pricing "multiple" for the item; usually is just 1.
    """)

    pack_price = sa.Column(sa.Numeric(precision=8, scale=3), nullable=True, doc="""
    Pack price for the item.
    """)

    pack_price_multiple = sa.Column(sa.Integer(), nullable=True, doc="""
    Pack pricing "multiple" for the item.
    """)

    suggested_price = sa.Column(sa.Numeric(precision=8, scale=3), nullable=True, doc="""
    The "suggested" retail price for the item.
    """)

    tax1 = sa.Column(sa.Boolean(), nullable=True, doc="""
    (hack?) Flag indicating whether 'tax 1' applies to the item.
    """)

    tax2 = sa.Column(sa.Boolean(), nullable=True, doc="""
    (hack?) Flag indicating whether 'tax 2' applies to the item.
    """)

    tax3 = sa.Column(sa.Boolean(), nullable=True, doc="""
    (hack?) Flag indicating whether 'tax 3' applies to the item.
    """)

    ecommerce_available = sa.Column(sa.Boolean(), nullable=True, doc="""
    Flag indicating the item should be made available on the eCommerce
    site, if applicable.
    """)
