"""Cofactr graph API client."""
# pylint: disable=too-many-arguments
# Python Modules
import json
from typing import Any, Dict, List, Literal, NamedTuple, Optional

# 3rd Party Modules
import httpx
from more_itertools import batched, flatten
from tenacity import (
    retry,
    retry_any,
    retry_if_exception_message,
    retry_if_exception_type,
    stop_after_attempt,
    wait_chain,
    wait_fixed,
)

# Local Modules
from cofactr.helpers import parse_entities
from cofactr.schema import (
    OfferSchemaName,
    OrgSchemaName,
    ProductSchemaName,
    SupplierSchemaName,
    schema_to_offer,
    schema_to_org,
    schema_to_product,
    schema_to_supplier,
)
from cofactr.schema.types import Completion

Protocol = Literal["http", "https"]


drop_none_values = lambda d: {k: v for k, v in d.items() if v is not None}

BATCH_LIMIT = 500


class RetrySettings(NamedTuple):
    """Retry settings for GraphAPI methods.
    TODO: Consider extending to other 5xx errors if and when encountered.
    """

    reraise: bool = True
    retry: retry_any = (
        retry_if_exception_type(httpx.ConnectTimeout)
        | retry_if_exception_type(httpx.ReadTimeout)
        | retry_if_exception_message(match=r"Server error '502 Bad Gateway'")
    )
    stop: stop_after_attempt = stop_after_attempt(3)
    wait: wait_chain = wait_chain(*[wait_fixed(wait=wait) for wait in [1, 3, 5]])


def get_products(
    url,
    client_id,
    api_key,
    query,
    fields,
    before,
    after,
    limit,
    external,
    force_refresh,
    schema,
    filtering,
    timeout: Optional[int] = None,
) -> httpx.Response:
    """Get products."""

    res = httpx.get(
        f"{url}/products/",
        headers=drop_none_values(
            {
                "X-CLIENT-ID": client_id,
                "X-API-KEY": api_key,
            }
        ),
        params=drop_none_values(
            {
                "q": query,
                "fields": fields,
                "before": before,
                "after": after,
                "limit": limit,
                "external": external,
                "force_refresh": force_refresh,
                "schema": schema,
                "filtering": json.dumps(filtering) if filtering else None,
            }
        ),
        timeout=timeout,
        follow_redirects=True,
    )

    res.raise_for_status()

    return res


def get_orgs(
    url,
    client_id,
    api_key,
    query,
    before,
    after,
    limit,
    schema,
    timeout,
    filtering,
) -> httpx.Response:
    """Get orgs."""

    res = httpx.get(
        f"{url}/orgs",
        headers=drop_none_values(
            {
                "X-CLIENT-ID": client_id,
                "X-API-KEY": api_key,
            }
        ),
        params=drop_none_values(
            {
                "q": query,
                "before": before,
                "after": after,
                "limit": limit,
                "schema": schema,
                "filtering": json.dumps(filtering) if filtering else None,
            }
        ),
        timeout=timeout,
        follow_redirects=True,
    )

    res.raise_for_status()

    return res


def get_suppliers(
    url,
    client_id,
    api_key,
    query,
    before,
    after,
    limit,
    schema,
    timeout,
    filtering,
) -> httpx.Response:
    """Get orgs."""

    res = httpx.get(
        f"{url}/orgs/suppliers",
        headers=drop_none_values(
            {
                "X-CLIENT-ID": client_id,
                "X-API-KEY": api_key,
            }
        ),
        params=drop_none_values(
            {
                "q": query,
                "before": before,
                "after": after,
                "limit": limit,
                "schema": schema,
                "filtering": json.dumps(filtering) if filtering else None,
            }
        ),
        timeout=timeout,
        follow_redirects=True,
    )

    res.raise_for_status()

    return res


class GraphAPI:  # pylint: disable=too-many-instance-attributes
    """A client-side representation of the Cofactr graph API."""

    PROTOCOL: Protocol = "https"
    HOST = "graph.cofactr.com"
    retry_settings = RetrySettings()

    def __init__(
        self,
        protocol: Optional[Protocol] = PROTOCOL,
        host: Optional[str] = HOST,
        default_product_schema: ProductSchemaName = ProductSchemaName.FLAGSHIP,
        default_org_schema: OrgSchemaName = OrgSchemaName.FLAGSHIP,
        default_offer_schema: OfferSchemaName = OfferSchemaName.FLAGSHIP,
        default_supplier_schema: SupplierSchemaName = SupplierSchemaName.FLAGSHIP,
        client_id: Optional[str] = None,
        api_key: Optional[str] = None,
    ):

        self.url = f"{protocol}://{host}"
        self.default_product_schema = default_product_schema
        self.default_org_schema = default_org_schema
        self.default_offer_schema = default_offer_schema
        self.default_supplier_schema = default_supplier_schema
        self.client_id = client_id
        self.api_key = api_key

    def check_health(self):
        """Check the operational status of the service."""

        res = httpx.get(self.url)

        res.raise_for_status()

        return res.json()

    @retry(
        reraise=retry_settings.reraise,
        retry=retry_settings.retry,
        stop=retry_settings.stop,
        wait=retry_settings.wait,
    )
    def get_products(
        self,
        query: Optional[str] = None,
        fields: Optional[str] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        limit: Optional[int] = None,
        external: Optional[bool] = True,
        force_refresh: bool = False,
        schema: Optional[ProductSchemaName] = None,
        filtering: Optional[List[Dict]] = None,
        timeout: Optional[int] = None,
    ):
        """Get products.

        Args:
            query: Search query.
            fields: Used to filter properties that the response should contain. A field can be a
                concrete property like "mpn" or an abstract group of properties like "assembly".
                Example: `"id,aliases,labels,statements{spec,assembly},offers"`.
            before: Upper page boundry, expressed as a product ID.
            after: Lower page boundry, expressed as a product ID.
            limit: Restrict the results of the query to a particular number of documents.
            external: Whether to query external sources.
            force_refresh: Whether to force re-ingestion from external sources. Overrides
                `external`.
            schema: Response schema.
            filtering: Filter products.
                Example: `[{"field":"id","operator":"IN","value":["CCCQSA3G9SMR","CCV1F7A8UIYH"]}]`.
            timeout: Time to wait (in seconds) for the server to issue a response.
        """

        if not schema:
            schema = self.default_product_schema

        res = get_products(
            url=self.url,
            client_id=self.client_id,
            api_key=self.api_key,
            query=query,
            fields=fields,
            external=external,
            force_refresh=force_refresh,
            before=before,
            after=after,
            limit=limit,
            schema=schema.value,
            filtering=filtering,
            timeout=timeout,
        )

        extracted_products = res.json()

        # Handle schemas that have parsers.
        Product = schema_to_product.get(schema)  # pylint: disable=invalid-name

        if Product:
            extracted_products["data"] = [
                Product(**data) for data in extracted_products["data"]
            ]

        return extracted_products

    @retry(
        reraise=retry_settings.reraise,
        retry=retry_settings.retry,
        stop=retry_settings.stop,
        wait=retry_settings.wait,
    )
    def get_products_by_searches(
        self,
        queries: List[str],
        external: bool = True,
        force_refresh: bool = False,
        schema: Optional[ProductSchemaName] = None,
        timeout: Optional[int] = None,
    ):
        """Search for products associated with each query.

        Args:
            queries: Queries to find products for.
            external: Whether to query external sources in order to refresh data if applicable.
            force_refresh: Whether to force re-ingestion from external sources. Overrides
                `external`.
            schema: Response schema.
            timeout: Time to wait (in seconds) for the server to issue a response.

        Returns:
            A dictionary mapping each MPN to a list of matching products.
        """

        if not queries:
            return {}

        if not schema:
            schema = self.default_product_schema

        res = httpx.post(
            f"{self.url}/batch/products/",
            headers=drop_none_values(
                {
                    "X-CLIENT-ID": self.client_id,
                    "X-API-KEY": self.api_key,
                }
            ),
            json={
                "batch": [
                    {
                        "method": "GET",
                        "relative_url": (
                            f"?q={query}&schema={schema.value}&external={bool(external)}"
                            f"&force_refresh={force_refresh}"
                        ),
                    }
                    for query in queries
                ]
            },
            timeout=timeout,
            follow_redirects=True,
        )

        res.raise_for_status()

        responses = res.json()

        Product = schema_to_product[schema]  # pylint: disable=invalid-name

        query_to_products: Dict[str, Any] = {}

        for query, response in zip(queries, responses):
            matches = []

            if response["code"] == 200:
                data = response["body"]["data"]

                matches = [Product(**product_data) for product_data in data]

            query_to_products[query] = matches

        return query_to_products

    @retry(
        reraise=retry_settings.reraise,
        retry=retry_settings.retry,
        stop=retry_settings.stop,
        wait=retry_settings.wait,
    )
    def get_products_by_ids(
        self,
        ids: List[str],
        external: Optional[bool] = True,
        force_refresh: bool = False,
        schema: Optional[ProductSchemaName] = None,
        timeout: Optional[int] = None,
    ):
        """Get a batch of products by IDs.

        Note: Multiple requests are made if more than 250 IDs are provided.

        Args:
            ids: Cofactr product IDs to match on.
            external: Whether to query external sources in order to refresh data if applicable.
            force_refresh: Whether to force re-ingestion from external sources. Overrides
                `external`.
            schema: Response schema.
            timeout: Time to wait (in seconds) for the server to issue a response.
        """

        batch_size = 250

        if not schema:
            schema = self.default_product_schema

        batched_products = [
            self.get_products(
                external=external,
                force_refresh=force_refresh,
                schema=schema,
                filtering=[{"field": "id", "operator": "IN", "value": batched_ids}],
                limit=batch_size,
                timeout=timeout,
            )
            for batched_ids in batched(ids, n=batch_size)
        ]

        products_data = list(
            flatten([products["data"] for products in batched_products])
        )

        extracted_products = (
            {
                "data": products_data,
                "paging": {
                    "previous": f"/products?limit={len(ids)}&before={products_data[0].id}",
                    "next": None,
                },
            }
            if products_data
            else {"data": [], "paging": {}}
        )

        id_to_product = parse_entities(
            ids=ids,
            entities=extracted_products["data"],
            entity_dataclass=schema_to_product[schema],
        )

        return id_to_product

    @retry(
        reraise=retry_settings.reraise,
        retry=retry_settings.retry,
        stop=retry_settings.stop,
        wait=retry_settings.wait,
    )
    def get_canonical_product_ids(
        self,
        ids: List[str],
        timeout: Optional[int] = None,
    ):
        """Get the canonical product ID for each of the given IDs, which may or may not be
        deprecated.
        """

        batch_size = 500

        batched_products = [
            self.get_products(
                fields="id,deprecated_ids",
                external=False,
                force_refresh=False,
                schema=ProductSchemaName.INTERNAL,
                filtering=[{"field": "id", "operator": "IN", "value": batched_ids}],
                limit=batch_size,
                timeout=timeout,
            )
            for batched_ids in batched(ids, n=batch_size)
        ]

        id_to_canonical_id = {}

        for res in batched_products:
            products = res.get("data", [])

            for product in products:
                canonical_id = product["id"]

                for key in [canonical_id, *(product.get("deprecated_ids") or [])]:
                    id_to_canonical_id[key] = canonical_id

        return {id_: id_to_canonical_id.get(id_) for id_ in ids}

    @retry(
        reraise=retry_settings.reraise,
        retry=retry_settings.retry,
        stop=retry_settings.stop,
        wait=retry_settings.wait,
    )
    def get_orgs(
        self,
        query: Optional[str] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        limit: Optional[int] = None,
        schema: Optional[OrgSchemaName] = None,
        timeout: Optional[int] = None,
        filtering: Optional[List[Dict]] = None,
    ):
        """Get organizations.

        Args:
            query: Search query.
            before: Upper page boundry, expressed as a product ID.
            after: Lower page boundry, expressed as a product ID.
            limit: Restrict the results of the query to a particular number of documents.
            schema: Response schema.
            timeout: Time to wait (in seconds) for the server to issue a response.
            filtering: Filter orgs.
                Example: `[{"field":"id","operator":"IN","value":["622fb450e4c292d8287b0af5"]}]`.
        """

        if not schema:
            schema = self.default_org_schema

        res = get_orgs(
            url=self.url,
            client_id=self.client_id,
            api_key=self.api_key,
            query=query,
            before=before,
            after=after,
            limit=limit,
            schema=schema.value,
            timeout=timeout,
            filtering=filtering,
        )

        res_json = res.json()

        Org = schema_to_org[schema]  # pylint: disable=invalid-name

        res_json["data"] = [Org(**data) for data in res_json["data"]]

        return res_json

    @retry(
        reraise=retry_settings.reraise,
        retry=retry_settings.retry,
        stop=retry_settings.stop,
        wait=retry_settings.wait,
    )
    def get_suppliers(
        self,
        query: Optional[str] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        limit: Optional[int] = None,
        schema: Optional[SupplierSchemaName] = None,
        timeout: Optional[int] = None,
        filtering: Optional[List[Dict]] = None,
    ):
        """Get suppliers.

        Args:
            query: Search query.
            before: Upper page boundry, expressed as a product ID.
            after: Lower page boundry, expressed as a product ID.
            limit: Restrict the results of the query to a particular number of documents.
            schema: Response schema.
            timeout: Time to wait (in seconds) for the server to issue a response.
            filtering: Filter suppliers.
                Example: `[{"field":"id","operator":"IN","value":["622fb450e4c292d8287b0af5"]}]`.
        """

        if not schema:
            schema = self.default_supplier_schema

        res = get_suppliers(
            url=self.url,
            client_id=self.client_id,
            api_key=self.api_key,
            query=query,
            before=before,
            after=after,
            limit=limit,
            schema=schema.value,
            timeout=timeout,
            filtering=filtering,
        )

        res_json = res.json()

        Supplier = schema_to_supplier[schema]  # pylint: disable=invalid-name

        res_json["data"] = [Supplier(**data) for data in res_json["data"]]

        return res_json

    @retry(
        reraise=retry_settings.reraise,
        retry=retry_settings.retry,
        stop=retry_settings.stop,
        wait=retry_settings.wait,
    )
    def get_suppliers_by_ids(
        self,
        ids: List[str],
        schema: Optional[SupplierSchemaName] = None,
        timeout: Optional[int] = None,
    ):
        """Get a batch of suppliers by IDs.

        Note: Multiple requests are made if more than 250 IDs are provided.

        Args:
            ids: Cofactr org IDs to match on.
            schema: Response schema.
            timeout: Time to wait (in seconds) for the server to issue a response.
        """

        batch_size = 250

        if not schema:
            schema = self.default_supplier_schema

        batched_suppliers = [
            self.get_suppliers(
                schema=schema,
                filtering=[{"field": "id", "operator": "IN", "value": batched_ids}],
                limit=batch_size,
                timeout=timeout,
            )
            for batched_ids in batched(ids, n=batch_size)
        ]

        suppliers_data = list(
            flatten([suppliers["data"] for suppliers in batched_suppliers])
        )

        extracted_suppliers = (
            {
                "data": suppliers_data,
                "paging": {
                    "previous": f"/products?limit={len(ids)}&before={suppliers_data[0].id}",
                    "next": None,
                },
            }
            if suppliers_data
            else {"data": [], "paging": {}}
        )

        id_to_supplier = parse_entities(
            ids=ids,
            entities=extracted_suppliers["data"],
            entity_dataclass=schema_to_supplier[schema],
        )

        return id_to_supplier

    @retry(
        reraise=retry_settings.reraise,
        retry=retry_settings.retry,
        stop=retry_settings.stop,
        wait=retry_settings.wait,
    )
    def autocomplete_orgs(
        self,
        query: Optional[str] = None,
        limit: Optional[int] = None,
        types: Optional[str] = None,
        timeout: Optional[int] = None,
    ) -> Dict[Literal["data"], Completion]:
        """Autocomplete organizations.

        Args:
            query: Search query.
            before: Upper page boundry, expressed as a product ID.
            after: Lower page boundry, expressed as a product ID.
            limit: Restrict the results of the query to a particular number of
                documents.
            types: Filter for types of organizations.
                Example: "supplier" filters to suppliers.
                Example: "supplier|manufacturer" filters to orgs that are a
                    supplier or a manufacturer.
            timeout: Time to wait (in seconds) for the server to issue a response.
        """

        res = httpx.get(
            f"{self.url}/orgs/autocomplete",
            headers=drop_none_values(
                {
                    "X-CLIENT-ID": self.client_id,
                    "X-API-KEY": self.api_key,
                }
            ),
            params=drop_none_values(
                {
                    "q": query,
                    "limit": limit,
                    "types": types,
                }
            ),
            timeout=timeout,
            follow_redirects=True,
        )

        res.raise_for_status()

        return res.json()

    @retry(
        reraise=retry_settings.reraise,
        retry=retry_settings.retry,
        stop=retry_settings.stop,
        wait=retry_settings.wait,
    )
    def get_product(
        self,
        id: str,
        fields: Optional[str] = None,
        external: Optional[bool] = True,
        force_refresh: bool = False,
        schema: Optional[ProductSchemaName] = None,
        timeout: Optional[int] = None,
    ):
        """Get product.

        Args:
            fields: Used to filter properties that the response should contain. A field can be a
                concrete property like "mpn" or an abstract group of properties like "assembly".
                Example: "id,aliases,labels,statements{spec,assembly},offers"
            external: Whether to query external sources in order to update information for the
                given product.
            force_refresh: Whether to force re-ingestion from external sources. Overrides
                `external`.
            schema: Response schema.
            timeout: Time to wait (in seconds) for the server to issue a response.
        """

        if not schema:
            schema = self.default_product_schema

        res = httpx.get(
            f"{self.url}/products/{id}",
            headers=drop_none_values(
                {
                    "X-CLIENT-ID": self.client_id,
                    "X-API-KEY": self.api_key,
                }
            ),
            params=drop_none_values(
                {
                    "fields": fields,
                    "external": external,
                    "force_refresh": force_refresh,
                    "schema": schema.value,
                }
            ),
            timeout=timeout,
            follow_redirects=True,
        )

        res.raise_for_status()

        res_json = res.json()

        Product = schema_to_product[schema]  # pylint: disable=invalid-name

        res_json["data"] = (
            Product(**res_json["data"]) if (res_json and res_json.get("data")) else None
        )

        return res_json

    @retry(
        reraise=retry_settings.reraise,
        retry=retry_settings.retry,
        stop=retry_settings.stop,
        wait=retry_settings.wait,
    )
    def get_offers(
        self,
        product_id: str,
        fields: Optional[str] = None,
        external: Optional[bool] = True,
        force_refresh: bool = False,
        schema: Optional[OfferSchemaName] = None,
        timeout: Optional[int] = None,
    ):
        """Get product.

        Args:
            product_id: ID of the product to get offers for.
            fields: Used to filter properties that the response should contain.
            external: Whether to query external sources in order to update information.
            force_refresh: Whether to force re-ingestion from external sources. Overrides
                `external`.
            schema: Response schema.
            timeout: Time to wait (in seconds) for the server to issue a response.
        """

        if not schema:
            schema = self.default_offer_schema

        res = httpx.get(
            f"{self.url}/products/{product_id}/offers",
            headers=drop_none_values(
                {
                    "X-CLIENT-ID": self.client_id,
                    "X-API-KEY": self.api_key,
                }
            ),
            params=drop_none_values(
                {
                    "fields": fields,
                    "external": external,
                    "force_refresh": force_refresh,
                    "schema": schema.value,
                }
            ),
            timeout=timeout,
            follow_redirects=True,
        )

        res.raise_for_status()

        res_json = res.json()

        Offer = schema_to_offer[schema]  # pylint: disable=invalid-name

        res_json["data"] = [Offer(**data) for data in res_json["data"]]

        return res_json

    @retry(
        reraise=retry_settings.reraise,
        retry=retry_settings.retry,
        stop=retry_settings.stop,
        wait=retry_settings.wait,
    )
    def get_org(
        self,
        id: str,
        schema: Optional[OrgSchemaName] = None,
        timeout: Optional[int] = None,
    ):
        """Get organization."""

        if not schema:
            schema = self.default_org_schema

        res = httpx.get(
            f"{self.url}/orgs/{id}",
            headers=drop_none_values(
                {
                    "X-CLIENT-ID": self.client_id,
                    "X-API-KEY": self.api_key,
                }
            ),
            params=drop_none_values({"schema": schema.value}),
            timeout=timeout,
            follow_redirects=True,
        )

        res.raise_for_status()

        res_json = res.json()

        Org = schema_to_org[schema]  # pylint: disable=invalid-name

        res_json["data"] = (
            Org(**res_json["data"]) if (res_json and res_json.get("data")) else None
        )

        return res_json

    @retry(
        reraise=retry_settings.reraise,
        retry=retry_settings.retry,
        stop=retry_settings.stop,
        wait=retry_settings.wait,
    )
    def get_supplier(
        self,
        id: str,
        schema: Optional[SupplierSchemaName] = None,
        timeout: Optional[int] = None,
    ):
        """Get supplier."""

        if not schema:
            schema = self.default_supplier_schema

        res = httpx.get(
            f"{self.url}/orgs/{id}",
            headers=drop_none_values(
                {
                    "X-CLIENT-ID": self.client_id,
                    "X-API-KEY": self.api_key,
                }
            ),
            params=drop_none_values({"schema": schema.value}),
            timeout=timeout,
            follow_redirects=True,
        )

        res.raise_for_status()

        res_json = res.json()

        Supplier = schema_to_supplier[schema]  # pylint: disable=invalid-name

        res_json["data"] = (
            Supplier(**res_json["data"])
            if (res_json and res_json.get("data"))
            else None
        )

        return res_json
