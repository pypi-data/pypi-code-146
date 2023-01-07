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
Handler for new product batches
"""

from __future__ import unicode_literals, absolute_import

from rattail.db import model
from rattail.batch import BatchHandler


class NewProductBatchHandler(BatchHandler):
    """
    Handler for new product batches.
    """
    batch_model_class = model.NewProductBatch

    def should_populate(self, batch):
        if batch.input_filename:
            return True
        return False

    def populate(self, batch, progress=None):
        if batch.input_filename:
            return self.populate_from_file(batch, progress=progress)

    def populate_from_file(self, batch, progress=None):
        raise NotImplementedError

    def refresh_row(self, row):
        model = self.model
        session = self.app.get_session(row)

        if not row.upc and row.item_entry:
            row.upc = self.app.make_gpc(row.item_entry)

        # vendor
        if not row.vendor:
            if row.vendor_id:
                row.vendor = session.query(model.Vendor)\
                                    .filter(model.Vendor.id == row.vendor_id)\
                                    .first()
        if row.vendor:
            row.vendor_id = row.vendor.id

        # department
        if not row.department:
            if row.department_number:
                row.department = session.query(model.Department)\
                                        .filter(model.Department.number == row.department_number)\
                                        .first()
            elif row.department_name:
                row.department = session.query(model.Department)\
                                        .filter(model.Department.name == row.department_name)\
                                        .first()
                if not row.department:
                    row.department = session.query(model.Department)\
                                            .filter(model.Department.name.ilike('%{}%'.format(row.department_name)))\
                                            .first()
        if row.department:
            row.department_number = row.department.number
            row.department_name = row.department.name

        # subdepartment
        if not row.subdepartment:
            if row.subdepartment_number:
                row.subdepartment = session.query(model.Subdepartment)\
                                           .filter(model.Subdepartment.number == row.subdepartment_number)\
                                           .first()
            elif row.subdepartment_name:
                row.subdepartment = session.query(model.Subdepartment)\
                                           .filter(model.Subdepartment.name == row.subdepartment_name)\
                                           .first()
                if not row.subdepartment:
                    row.subdepartment = session.query(model.Subdepartment)\
                                               .filter(model.Subdepartment.name.ilike('%{}%'.format(row.subdepartment_name)))\
                                               .first()
        if row.subdepartment:
            row.subdepartment_number = row.subdepartment.number
            row.subdepartment_name = row.subdepartment.name

        # category
        if not row.category:
            if row.category_code:
                row.category = session.query(model.Category)\
                                      .filter(model.Category.code == row.category_code)\
                                      .first()
        if row.category:
            row.category_code = row.category.code

        # family
        if not row.family:
            if row.family_code:
                row.family = session.query(model.Family)\
                                    .filter(model.Family.code == row.family_code)\
                                    .first()
        if row.family:
            row.family_code = row.family.code

        # report
        if not row.report:
            if row.report_code:
                row.report = session.query(model.ReportCode)\
                                    .filter(model.ReportCode.code == row.report_code)\
                                    .first()
        if row.report:
            row.report_code = row.report.code

        # brand
        if not row.brand:
            if row.brand_name:
                row.brand = session.query(model.Brand)\
                                   .filter(model.Brand.name == row.brand_name)\
                                   .first()
        if row.brand:
            row.brand_name = row.brand.name

        if not row.product:
            if not row.item_entry:
                row.status_code = row.STATUS_MISSING_KEY
                return

            row.product = self.locate_product_for_entry(session, row.item_entry)

        if row.product:
            row.status_code = row.STATUS_PRODUCT_EXISTS
            return

        if row.vendor_id and not row.vendor:
            row.status_code = row.STATUS_VENDOR_NOT_FOUND
            return

        if (row.department_number or row.department_name) and not row.department:
            row.status_code = row.STATUS_DEPT_NOT_FOUND
            return

        if ((row.subdepartment_number or row.subdepartment_name)
            and not row.subdepartment):
            row.status_code = row.STATUS_SUBDEPT_NOT_FOUND
            return

        if row.category_code and not row.category:
            row.status_code = row.STATUS_CATEGORY_NOT_FOUND
            return

        if row.family_code and not row.family:
            row.status_code = row.STATUS_FAMILY_NOT_FOUND
            return

        if row.report_code and not row.report:
            row.status_code = row.STATUS_REPORTCODE_NOT_FOUND
            return

        row.status_code = row.STATUS_OK
