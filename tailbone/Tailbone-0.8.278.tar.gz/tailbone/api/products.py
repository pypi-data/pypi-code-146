# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2023 Lance Edgar
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
Tailbone Web API - Product Views
"""

from __future__ import unicode_literals, absolute_import

import six
import sqlalchemy as sa
from sqlalchemy import orm

from cornice import Service

from rattail.db import model

from tailbone.api import APIMasterView


class ProductView(APIMasterView):
    """
    API views for Product data
    """
    model_class = model.Product
    collection_url_prefix = '/products'
    object_url_prefix = '/product'
    supports_autocomplete = True

    def __init__(self, request, context=None):
        super(ProductView, self).__init__(request, context=context)
        app = self.get_rattail_app()
        self.products_handler = app.get_products_handler()

    def normalize(self, product):

        # get what we can from handler
        data = self.products_handler.normalize_product(product, fields=[
            'brand_name',
            'full_description',
            'department_name',
            'unit_price_display',
            'sale_price',
            'sale_price_display',
            'sale_ends',
            'sale_ends_display',
            'vendor_name',
            'costs',
            'image_url',
        ])

        # but must supplement
        cost = product.cost
        data.update({
            'upc': six.text_type(product.upc),
            'scancode': product.scancode,
            'item_id': product.item_id,
            'item_type': product.item_type,
            'status_code': product.status_code,
            'default_unit_cost': cost.unit_cost if cost else None,
            'default_unit_cost_display': "${:0.2f}".format(cost.unit_cost) if cost and cost.unit_cost is not None else None,
        })

        return data

    def make_autocomplete_query(self, term):
        query = self.Session.query(model.Product)\
                            .outerjoin(model.Brand)\
                            .filter(sa.or_(
                                model.Brand.name.ilike('%{}%'.format(term)),
                                model.Product.description.ilike('%{}%'.format(term))))

        if not self.request.has_perm('products.view_deleted'):
            query = query.filter(model.Product.deleted == False)

        query = query.order_by(model.Brand.name,
                               model.Product.description)\
                     .options(orm.joinedload(model.Product.brand))
        return query

    def autocomplete_display(self, product):
        return product.full_description

    def quick_lookup(self):
        """
        View for handling "quick lookup" user input, for index page.
        """
        data = self.request.GET
        entry = data['entry']

        product = self.products_handler.locate_product_for_entry(self.Session(),
                                                                 entry)
        if not product:
            return {'error': "Product not found"}

        return {'ok': True,
                'product': self.normalize(product)}

    @classmethod
    def defaults(cls, config):
        cls._defaults(config)
        cls._product_defaults(config)

    @classmethod
    def _product_defaults(cls, config):
        route_prefix = cls.get_route_prefix()
        permission_prefix = cls.get_permission_prefix()
        collection_url_prefix = cls.get_collection_url_prefix()

        # quick lookup
        quick_lookup = Service(name='{}.quick_lookup'.format(route_prefix),
                               path='{}/quick-lookup'.format(collection_url_prefix))
        quick_lookup.add_view('GET', 'quick_lookup', klass=cls,
                              permission='{}.list'.format(permission_prefix))
        config.add_cornice_service(quick_lookup)


def defaults(config, **kwargs):
    base = globals()

    ProductView = kwargs.get('ProductView', base['ProductView'])
    ProductView.defaults(config)


def includeme(config):
    defaults(config)
