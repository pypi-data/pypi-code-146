from datetime import date
from datetime import datetime
from datetime import timedelta
from decimal import Decimal
import json
import logging
import pandas as pd

log = logging.getLogger(__name__)


def make_json_serializable(value, fn=lambda x: x):
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.isoformat('T')
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, Decimal):
        return f'{value}'
    return fn(value)


class JsonEncoder(json.JSONEncoder):
    def default(self, o):  # pylint: disable=method-hidden
        return make_json_serializable(o, super().default)


class CommerceApiException(Exception):
    def __init__(self, status_code=None, content=None, text=None, data=None):
        super().__init__(status_code, content, text, data)
        self.status_code = status_code
        self.content = content
        self.text = text
        self.data = data

    def __str__(self):
        return f'[{self.status_code}] {self.text}'

    @classmethod
    def from_response(cls, response):
        return cls(
            response.status_code,
            response.content,
            response.text,
            response.json(),
        )


class CommerceApi:
    """
    This class provides a wrapper around the sales force
    commerce api.  We setup credentials for peaky peep
    in account manager, following the commerce api guide, here:
    https://developer.commercecloud.com/s/article/CommerceAPI-Client-Permissions-for-API-Endpoints

    Once we had created the api client accounts in account manager,
    we loaded the configuration into waddle.  There are about 6 configuration
    values we needed to configure this client to work, and each
    of these can be specified in the constructor to override the values
    from waddle.

    Args

        :conf (ParamBunch): the param bunch with the configuration, included
        encrypted secrets
        :base_url (str): which is the api url found in the guide, prefixed
                      by the short code which we generated from the
                      administration portal.  n.b., there is a single
                      short code for all of our instances
        :site_id (str): the site id can be found in the administration portal
                     by going to Administration > Manage Sites.
        :scopes (List(str]): a list of scopes from this page
        https://developer.commercecloud.com/s/article/CommerceAPI-AuthZ-Scope-Catalog
        :client_id (str): the client_id that we generated in account manager when
                       we created the api client record
        :password (str):  the password that we set when we created the api client
                       record.  It can be reset using account manager.
        :organization_id (str):  this value can be seen from Administration >
                              Salesforce Commerce API Settings (in the
                              admin console)
    """
    def __init__(self, conf,
                 base_url=None, site_id=None, scopes=None,
                 client_id=None, password=None, organization_id=None,
                 webdav_prefix=None, default_time_zone=None, **kwargs):
        """
        :param str which: specifies which config to load from waddle
        """
        import pytz
        from urllib3 import Retry
        from requests.adapters import HTTPAdapter as HttpAdapter
        from requests_oauthlib import OAuth2Session
        from oauthlib.oauth2 import BackendApplicationClient
        self.base_url = base_url or conf.base_url
        self.site_id = site_id or conf.site_id
        self.scopes = scopes or conf.scopes
        self.conf = conf
        self.client_id = client_id or conf.client_id
        self.password = password or conf.password
        self.organization_id = organization_id or conf.organization_id
        self.default_time_zone = default_time_zone or pytz.timezone('PST8PDT')
        self.webdav_prefix = webdav_prefix or conf.webdav_prefix
        retry = Retry(total=5, status=3, backoff_factor=10, status_forcelist=[
            413, 429, 503, 500,
        ])
        adapter = HttpAdapter(max_retries=retry)
        self.session = OAuth2Session(client=BackendApplicationClient(
            client_id=self.client_id,
            scope=self.scope))
        self.session.mount('https://', adapter)
        self.fetch_token()
        self.base_orders_url = (
            f'{self.base_url}/checkout/orders/v1'
            f'/organizations/{self.organization_id}'
        )
        self.base_products_url = (
            f'{self.base_url}/product/products/v1'
            f'/organizations/{self.organization_id}'
        )
        self.base_cdn_url = (
            f'{self.base_url}/cdn/zones/v1'
            f'/organizations/{self.organization_id}'
        )

        self.base_catalog_url = (
            f'{self.base_url}/product/catalogs/v1'
            f'/organizations/{self.organization_id}/catalogs'
        )

    @property
    def json_headers(self):
        return {
            'content-type': 'application/json',
        }

    @property
    def tenant_id(self):
        return self.organization_id.split('_', 2)[-1]

    @property
    def scope(self):
        scopes = ' '.join(self.scopes)
        scope = f'SALESFORCE_COMMERCE_API:{self.tenant_id} {scopes}'
        return scope

    def fetch_token(self):
        token_url = 'https://account.demandware.com/dwsso/oauth2/access_token'
        self.session.fetch_token(
            token_url,
            client_id=self.client_id,
            client_secret=self.password,
            scope=self.scope)

    def send(self, method, url, params=None, data=None, json_data=None, **kwargs):
        from oauthlib.oauth2 import TokenExpiredError
        data = data or json.dumps(json_data, cls=JsonEncoder)
        headers = None
        if json_data:
            headers = self.json_headers
        try:
            response = self.session.request(
                method, url, data=data, params=params,
                headers=headers, timeout=15,
            )
        except TokenExpiredError:
            self.fetch_token()
            response = self.session.request(
                method, url, data=data, params=params,
                headers=headers
            )
        if response.status_code // 100 != 2:
            raise CommerceApiException.from_response(response)
        response_data = response.json()
        headers = response.headers
        return headers, response_data

    def get(self, url, params=None, **kwargs):
        return self.send('get', url, params=params, **kwargs)

    def post(self, url, json_body=None, **kwargs):
        return self.send('post', url, json=json_body, **kwargs)

    def normalize_date(self, value):
        from dateutil.parser import parse as parse_date
        from pytz import utc
        if isinstance(value, str):
            value = parse_date(value)
        elif isinstance(value, date) and not isinstance(value, datetime):
            value = datetime(
                value.year, value.month, value.day,
                tzinfo=self.default_time_zone)
        if isinstance(value, datetime):
            value = value.astimezone(utc).isoformat('T', 'seconds')
        return value

    def now(self):
        return datetime.now(self.default_time_zone)

    def today(self):
        return self.now().replace(
            hour=0, minute=0, second=0, microsecond=0
        )

    def get_orders_by_creation_date_page(
            self,
            start_date=None,
            end_date=None, page=1, limit=1000):
        if not start_date:
            start_date = self.today() - timedelta(days=1)
        if not end_date:
            end_date = start_date + timedelta(days=1)
        params = {
            'creationDateFrom': self.normalize_date(start_date),
            'creationDateTo': self.normalize_date(end_date),
            'sortBy': 'creation_date',
        }
        yield from self.orders_page(params, page, limit)

    def orders_by_creation_date(
            self,
            start_date=None,
            end_date=None, limit=1000):
        for page in range(1, 100):
            results = list(self.get_orders_by_creation_date_page(
                start_date, end_date, page, limit
            ))
            if results:
                yield from results
            if len(results) < limit:
                break

    def orders_page(self, params, page, limit):
        params.setdefault('confirmationStatus', 'confirmed')
        params.setdefault('siteId', self.site_id)
        params.setdefault('limit', limit)
        if page > 1:
            params.setdefault('offset', (page - 1) * limit)
        url = f'{self.base_orders_url}/orders'
        headers, response = self.get(url, params)
        # sfcc pagination end points can be hard-capped to only returning
        # a certain number of results.  This is true, in particular
        # of the orders endpoint which hard-caps to 1000 orders
        n_pagination_total = headers.get('sfdc-pagination-total-count')
        if n_pagination_total:
            if int(n_pagination_total) > 1000:
                log.warning(
                    '[sfcc / commerce_api] n_pagination_total: %s',
                    n_pagination_total, extra={
                        'url': url,
                        'params': params,
                    })
        if 'data' in response:
            yield from response['data']

    def get_orders_by_modified_date_page(
            self,
            start_date=None,
            end_date=None, page=1, limit=1000):
        if not start_date:
            start_date = self.today() - timedelta(days=1)
        if not end_date:
            end_date = start_date + timedelta(days=1)
        params = {
            'lastModifiedDateFrom': self.normalize_date(start_date),
            'lastModifiedDateTo': self.normalize_date(end_date),
        }
        yield from self.orders_page(params, page, limit)

    def orders_by_modified_date(
            self,
            start_date=None,
            end_date=None, limit=200):
        for page in range(1, 100):
            results = list(self.get_orders_by_modified_date_page(
                start_date, end_date, page, limit
            ))
            if results:
                yield from results
            if len(results) < limit:
                break

    def order(self, order_number):
        url = f'{self.base_orders_url}/orders/{order_number}'
        log.info('order endpoint - %s', url)
        params = {
            'siteId': self.site_id,
        }
        _, order_data = self.get(url, params)
        return order_data

    def product(self, product_id):
        url = f'{self.base_products_url}/products/{product_id}'
        params = {
            'siteId': self.site_id,
        }
        _, product_data = self.get(url, params)
        return product_data

    def product_variations(self, product_id):
        url = f'{self.base_products_url}/products/{product_id}/variations'
        params = {
            'siteId': self.site_id,
        }
        _, product_data = self.get(url, params)
        return product_data

    def products_by_category(self, catalog_id, category_id):
        url = f'{self.base_catalog_url}/{catalog_id}/categories/{category_id}/category-product-assignment-search'
        log.info('url %s', url)
        params = {
             'query': { 'match_all_query': {},
                         },
             'select': '(**)',
             'expand': ['product_base']
        }
        _, product_data = self.post(url, json_data=params)
        return product_data

    # we need to pull all products updated in last couple of days
    def products_last_modified(self, from_date, to_date):
        url = f'{self.base_products_url}/product-search'
        params = {
            'query': {
                'filtered_query': {
                    'query': {'match_all_query': {}},
                    'filter': {
                        'range_filter': {
                            'field': 'lastModified',
                            'from': f'{from_date}',  # '2023-01-04T00:00:00.000Z'
                            'to': f'{to_date}',  # '2023-01-05T00:00:00.000Z'
                            'from_inclusive': True,
                            'to_inclusive': True,
                        }
                    }
                }
            },
            'expand': ['all']
        }
        _, product_data = self.post(url, json_data=params)
        list_products = []
        total_records = product_data['total']
        log.info('total records %s', total_records)
        while True:
            list_products.extend([d['id'] for d in product_data['hits']])
            log.info('fetched records count %s', len(list_products))

            # exit when we read all records
            if total_records == len(list_products):
                return list_products
            params = {
                'limit': 120,
                'offset': len(list_products),
                'query': {
                    'filtered_query': {
                        'query': {'match_all_query': {}},
                        'filter': {
                            'range_filter': {
                                'field': 'lastModified',
                                'from': f'{from_date}',  # '2023-01-04T00:00:00.000Z'
                                'to': f'{to_date}',  # '2023-01-05T00:00:00.000Z'
                                'from_inclusive': True,
                                'to_inclusive': True,
                            }
                        }
                    }
                },
                'expand': ['all']
            }
            _, product_data = self.post(url, json_data=params)
        return list_products


    def get_zone_info(self, limit=1, offset=None):
        url = f'{self.base_cdn_url}/zones/info'
        # params = dict(limit=limit)
        # if offset:
        #     params[offset] = offset
        # _, response = self.get(url, params=params)
        _, response = self.get(url)
        return response

    def get_zone_id(self):
        zones = self.get_zone_info()
        webdav_prefix = self.webdav_prefix
        for x in zones['data']:
            if x['name'].startswith(webdav_prefix):
                return x['zoneId']
        log.info('[sfcc] no zone id found!')
        return None

    def get_certificates(self, zone_id=None, params=None, **kwargs):
        zone_id = zone_id or self.get_zone_id()
        url = f'{self.base_cdn_url}/zones/{zone_id}/certificates'
        _, response = self.get(url, params=params, **kwargs)
        return response

    def update_certificate(self, certificate_id, hostname, certificate, key,
                           zone_id=None, params=None, **kwargs):
        """
        certificate and key should be specified in pem format
        """
        zone_id = zone_id or self.get_zone_id()
        url = f'{self.base_cdn_url}/zones/{zone_id}/certificates/{certificate_id}'
        json_data = dict(
            hostname=hostname,
            certificate=certificate,
            privateKey=key,
        )
        return self.send('patch', url, params=params, json_data=json_data, **kwargs)

    def add_certificate(self, hostname, certificate, key,
                        zone_id=None, params=None, **kwargs):
        """
        certificate and key should be specified in pem format
        """
        zone_id = zone_id or self.get_zone_id()
        url = f'{self.base_cdn_url}/zones/{zone_id}/certificates'
        json_data = dict(
            hostname=hostname,
            certificate=certificate,
            privateKey=key,
        )
        return self.post(url, params=params, json_data=json_data, **kwargs)

    def get_firewall_rules(self):
        zone_id = self.get_zone_id()
        if zone_id:
            url = f'{self.base_cdn_url}/zones/{zone_id}/firewall/rules'
            _, response = self.get(url)
            return response
        log.info('[sfcc] no zone id found!')
        return None

    def add_firewall_rules(self, type_, action, values):
        zone_id = self.get_zone_id()
        if zone_id:
            url = f'{self.base_cdn_url}/zones/{zone_id}/firewall/rules'
            json_data = {
                'type': type_,
                'action': action,
                'values': values,
            }
            _, response = self.post(url, json_data)
            return response
        return None
