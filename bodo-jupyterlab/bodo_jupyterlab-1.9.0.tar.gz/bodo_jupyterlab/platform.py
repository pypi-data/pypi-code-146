import json

from cachetools import TTLCache, cached
from cachetools.keys import hashkey
from requests.models import Response

from .config import (
    AUTH_API,
    BACKEND_API,
    NOTEBOOK_UUID,
    BACKEND_API_CLIENT_ID_LOC,
    BACKEND_API_SECRET_LOC,
    BACKEND_API_TOKEN_LOC,
    GET_CATALOG_REFRESH_PERIOD_SECONDS,
    GET_CATALOG_MAX_RETRIES,
    GET_CLUSTER_LIST_REFRESH_PERIOD_SECONDS,
    GET_CLUSTER_INFO_REFRESH_PERIOD_SECONDS,
    GET_CLUSTER_INFO_MAX_CACHE_SIZE,
    GET_CLUSTER_INFO_MAX_RETRIES,
    RESUME_CLUSTER_MAX_RETRIES,
    PAUSE_CLUSTER_MAX_RETRIES,
)
from .helpers import get_session


class PlatformTokensManager:
    access_token: str = None
    client_id: str = None
    secret: str = None

    @classmethod
    def get_access_token(cls) -> str:
        if cls.access_token is not None:
            return cls.access_token

        cls.access_token = cls._read_access_token_from_disk()
        if cls.access_token is not None:
            return cls.access_token

        return cls.refresh_access_token()

    @classmethod
    def refresh_access_token(cls) -> str:
        if cls.client_id is None or cls.secret is None:
            cls.client_id, cls.secret = cls._load_api_keys_from_disk()

        cls.access_token = cls._fetch_access_token_over_http(cls.client_id, cls.secret)
        cls._write_access_token_to_disk(cls.access_token)
        return cls.access_token

    @staticmethod
    def is_access_token_expired(res: Response) -> bool:
        return not res.ok and res.status_code in (401, 403)

    @staticmethod
    def _fetch_access_token_over_http(client_id: str, secret: str) -> str:
        payload = {"clientId": client_id, "secret": secret}
        session = get_session()
        res: Response = session.post(AUTH_API, json=payload)
        if not res.ok:
            raise Exception(f"Unable to fetch token. Response: {res}")
        resp_json = json.loads(res.content.decode("utf-8"))
        token = resp_json["accessToken"]
        return token

    @staticmethod
    def _load_api_keys_from_disk():
        try:
            with open(BACKEND_API_CLIENT_ID_LOC, "r") as f:
                client_id = f.read().strip()
            with open(BACKEND_API_SECRET_LOC, "r") as f:
                secret = f.read().strip()
            return client_id, secret
        except Exception as e:
            print("Error getting api keys from disk: ", e)
            raise

    @staticmethod
    def _read_access_token_from_disk():
        try:
            with open(BACKEND_API_TOKEN_LOC, "r") as f:
                access_token = f.read().strip()
                if access_token:
                    return access_token
                return None
        except FileNotFoundError:
            return None
        except Exception as e:
            print("Error getting api token from disk: ", e)
            raise

    @staticmethod
    def _write_access_token_to_disk(token: str):
        try:
            with open(BACKEND_API_TOKEN_LOC, "w") as f:
                f.write(token)
        except Exception as e:
            print("Error writing tokens to disk: ", e)
            raise


class PlatformClusterManager:
    # Keep in sync with ICluster interface in src/types.ts
    CLUSTER_FIELDS = [
        "uuid",
        "name",
        "workersQuantity",
        "instanceType",
        "status",
        "bodoVersion",
        "nodesIp"
    ]
    cluster_list_cache = TTLCache(
        maxsize=2, ttl=GET_CLUSTER_LIST_REFRESH_PERIOD_SECONDS
    )

    # Backup of clusters that, will be used if backend API will not respond
    # this will help us to maintain clusters used in notebooks even when API will not respond for some time
    clusters_backup = []

    @staticmethod
    def _fetch_clusters_list_api(access_token: str) -> Response:
        session = get_session()
        return session.get(
            f"{BACKEND_API}/cluster?withTasks=false&clusterSource=user",
            headers={"Authorization": f"Bearer {access_token}"},
        )

    @classmethod
    @cached(
        cache=cluster_list_cache,
        key=lambda cls, logger: hashkey("A"),
    )
    def _fetch_clusters_list(cls, logger):
        logging_prefix = f"[GetClustersList]"
        try:
            response = None
            access_token = PlatformTokensManager.get_access_token()

            for attempt in range(GET_CLUSTER_INFO_MAX_RETRIES):
                logger.info(
                    f"{logging_prefix} Getting clusters list {attempt + 1} attempt"
                )

                response = cls._fetch_clusters_list_api(access_token)
                if response.ok:
                    break

                if PlatformTokensManager.is_access_token_expired(response):
                    logger.info(
                        f"{logging_prefix} Token expired, refreshing access token..."
                    )
                    access_token = PlatformTokensManager.refresh_access_token()

            if response is None or not response.ok:
                raise Exception(
                    f"Could not get cluster list from platform! Response: {response}"
                )

            logger.info(f"{logging_prefix} Response: {response}")
            clusters = json.loads(response.content.decode("utf-8"))

            clusters = list(filter(lambda x: x["status"] != "FAILED", clusters))
            logger.info(
                f"{logging_prefix} Cluster list received from backend: {clusters}"
            )

            # Only keep the required fields
            clusters = [
                {FIELD: c.get(FIELD) for FIELD in cls.CLUSTER_FIELDS} for c in clusters
            ]
            logger.info(f"{logging_prefix} Clusters (after filtering): {clusters}")
            return clusters

        except Exception as e:
            logger.error(
                f"{logging_prefix} Error in PlatformClusterManager.get_clusters_list: {e}"
            )
            raise

    @classmethod
    def get_clusters_list(cls, logger, force_refresh=False):
        # Wraps around fetch_cluster_list if force_refresh true then the cache is cleared.
        # This force refresh is currently used after pause and resume are called on a cluster within the list
        if force_refresh:
            cls.cluster_list_cache.clear()
        return cls._fetch_clusters_list(logger)

    @staticmethod
    def _resume_cluster_api(access_token: str, cluster_uuid: str) -> Response:
        session = get_session()
        return session.put(
            f"{BACKEND_API}/cluster/{cluster_uuid}/resume",
            headers={"Authorization": f"Bearer {access_token}"},
        )

    @classmethod
    def resume_cluster(cls, cluster_uuid: str, logger):
        logging_prefix = f"[ResumeCluster][UUID: {cluster_uuid}]"
        try:
            response = None
            access_token = PlatformTokensManager.get_access_token()
            for attempt in range(RESUME_CLUSTER_MAX_RETRIES):
                logger.info(
                    f"{logging_prefix} Resuming cluster: {cluster_uuid} {attempt + 1} attempt"
                )
                response = cls._resume_cluster_api(access_token, cluster_uuid)

                if response.ok:
                    break

                if PlatformTokensManager.is_access_token_expired(response):
                    logger.info(
                        f"{logging_prefix} Token expired, refreshing access token..."
                    )
                    access_token = PlatformTokensManager.refresh_access_token()

            if response is None or not response.ok:
                raise Exception(
                    f"Could not get resume cluster: {cluster_uuid}! Response: {response}"
                )

        except Exception as e:
            logger.error(
                f"{logging_prefix} Error in PlatformClusterManager.resume_cluster: {e}"
            )
            raise

    @staticmethod
    def _pause_cluster_api(access_token: str, cluster_uuid: str) -> Response:
        session = get_session()
        return session.put(
            f"{BACKEND_API}/cluster/{cluster_uuid}/pause",
            headers={"Authorization": f"Bearer {access_token}"},
        )

    @classmethod
    def pause_cluster(cls, cluster_uuid: str, logger):
        logging_prefix = f"[PauseCluster][UUID: {cluster_uuid}]"
        try:
            response = None
            access_token = PlatformTokensManager.get_access_token()
            for attempt in range(PAUSE_CLUSTER_MAX_RETRIES):
                logger.info(
                    f"{logging_prefix} Pausing cluster: {cluster_uuid} {attempt + 1} attempt"
                )
                response = cls._pause_cluster_api(access_token, cluster_uuid)

                if response.ok:
                    break

                if PlatformTokensManager.is_access_token_expired(response):
                    logger.info(
                        f"{logging_prefix} Token expired, refreshing access token..."
                    )
                    access_token = PlatformTokensManager.refresh_access_token()

            if response is None or not response.ok:
                raise Exception(
                    f"Could not get pause cluster: {cluster_uuid}! Response: {response}"
                )

        except Exception as e:
            logger.error(
                f"{logging_prefix} Error in PlatformClusterManager.pause_cluster: {e}"
            )
            raise

    @staticmethod
    def _get_cluster_info_api(access_token: str, cluster_uuid: str) -> Response:
        query = f"?notebookUUID={NOTEBOOK_UUID}" if NOTEBOOK_UUID else ""
        session = get_session()
        return session.get(
            f"{BACKEND_API}/cluster/{cluster_uuid}/connection-info{query}",
            headers={"Authorization": f"Bearer {access_token}"},
        )

    @classmethod
    @cached(
        cache=TTLCache(
            maxsize=GET_CLUSTER_INFO_MAX_CACHE_SIZE,
            ttl=GET_CLUSTER_INFO_REFRESH_PERIOD_SECONDS,
        ),
        key=lambda cls, cluster_uuid, logger: hashkey(cluster_uuid),
    )
    def get_cluster_info(cls, cluster_uuid: str, logger):
        logging_prefix = f"[GetClusterInfo][UUID: {cluster_uuid}]"
        try:
            response = None
            access_token = PlatformTokensManager.get_access_token()

            for attempt in range(GET_CLUSTER_INFO_MAX_RETRIES):
                logger.info(
                    f"{logging_prefix} Getting cluster: {cluster_uuid} info {attempt + 1} attempt"
                )
                response = cls._get_cluster_info_api(access_token, cluster_uuid)

                if response.ok:
                    break

                if PlatformTokensManager.is_access_token_expired(response):
                    logger.info(
                        f"{logging_prefix} Token expired, refreshing access token..."
                    )
                    access_token = PlatformTokensManager.refresh_access_token()

            if response is None or not response.ok:
                raise Exception(
                    f"Could not get cluster: {cluster_uuid} info! Response: {response}"
                )

            cluster_info = json.loads(response.content.decode("utf-8"))
            logger.info(
                f"{logging_prefix} Cluster Info received from backend: {cluster_info}"
            )
            return cluster_info

        except Exception as e:
            logger.error(
                f"{logging_prefix} Error in PlatformClusterManager.get_cluster_info: {e}"
            )
            raise

    @classmethod
    def get_cluster_hostlist(cls, cluster_uuid: str, logger):
        return cls.get_cluster_info(cluster_uuid, logger)["hostList"]


class PlatformCatalogsManager:
    # Keep in sync with ICatalog interface in src/types.ts
    CATALOG_FIELDS = [
        "uuid",
        "name",
        "description",
        "createdAt",
        "updatedAt",
        "catalogType",
    ]
    catalog_list_cache = TTLCache(maxsize=128, ttl=GET_CATALOG_REFRESH_PERIOD_SECONDS)

    # Backup of catalogs that, will be used if backend API does not respond
    # this will help us to maintain catalogs used in notebooks even when API does not respond for some time
    catalogs_backup = []

    @staticmethod
    def _fetch_catalogs_list_api(access_token: str) -> Response:
        session = get_session()
        return session.get(
            f"{BACKEND_API}/catalog",
            headers={"Authorization": f"Bearer {access_token}"},
        )

    @classmethod
    @cached(
        cache=catalog_list_cache,
        key=lambda cls, logger: hashkey("A"),
    )
    def _fetch_catalogs_list(cls, logger):
        logging_prefix = f"[GetCatalogsList]"
        try:
            response = None
            access_token = PlatformTokensManager.get_access_token()

            for attempt in range(GET_CATALOG_MAX_RETRIES):
                logger.info(
                    f"{logging_prefix} Getting catalogs list {attempt + 1} attempt"
                )

                response = cls._fetch_catalogs_list_api(access_token)
                if response.ok:
                    break

                if PlatformTokensManager.is_access_token_expired(response):
                    logger.info(
                        f"{logging_prefix} Token expired, refreshing access token..."
                    )
                    access_token = PlatformTokensManager.refresh_access_token()

            if response is None or not response.ok:
                raise Exception(
                    f"Could not get catalogs list from platform! Response: {response}"
                )

            logger.info(f"{logging_prefix} Response: {response}")
            catalogs = json.loads(response.content.decode("utf-8"))

            logger.info(
                f"{logging_prefix} Catalogs list received from backend: {catalogs}"
            )

            # Only keep the required fields
            catalogs = [
                {FIELD: c.get(FIELD) for FIELD in cls.CATALOG_FIELDS} for c in catalogs
            ]
            logger.info(f"{logging_prefix} Catalogs (after filtering): {catalogs}")
            return catalogs

        except Exception as e:
            logger.error(
                f"{logging_prefix} Error in PlatformCatalogsManager.get_catalogs_list: {e}"
            )
            raise

    @classmethod
    def get_catalogs_list(cls, logger, force_refresh=False):
        # Wraps around _fetch_catalogs_list. If `force_refresh=true` then the cache is cleared.
        if force_refresh:
            cls.catalog_list_cache.clear()
        return cls._fetch_catalogs_list(logger)
