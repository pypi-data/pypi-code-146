import logging

import requests

# proxies = {
#         "http": "http://localhost:9000",
#         "https": "89.23.194.174:8080"
#     }

logger = logging.getLogger(__name__)


def pretty_print_POST(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in
    this function because it is programmed to be pretty
    printed and may differ from the actual request.
    """
    logger.debug(
        "{}\n{}\n{}\n\n{}".format(
            "-----------START-----------",
            req.method + " " + req.url,
            "\n".join("{}: {}".format(k, v) for k, v in req.headers.items()),
            req.body,
        )
    )


def get(accToken=None, url="", proxy={}, data={}, timeout=10):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + str(accToken),
    }

    try:
        logger.debug(url)
        r = requests.get(url, timeout=timeout, headers=headers, proxies=proxy)
        r.raise_for_status()
        resp = r.json()
        logger.debug("resp = %s", resp)
        return resp

    except Exception:
        logger.exception("Fatal error in main loop")
        raise


def post(accToken, url="", proxy={}, data={}, timeout=30):
    # accToken = access_token()

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + str(accToken),
    }

    try:
        logger.debug("{}, {}".format(url, data))
        req = requests.Request("POST", url, data=data, headers=headers)
        # r = requests.post(url,  headers=headers, data=data, timeout=timeout)
        prepared = req.prepare()
        pretty_print_POST(prepared)
        s = requests.Session()
        res = s.send(prepared, proxies=proxy)

        res.raise_for_status()
        resp = res.json()
        logger.debug("resp = {}".format(resp))
        return resp

    except Exception:
        logger.exception("Fatal error in main loop")
        raise


def file_upload(accToken, url="", proxy={}, files={}, timeout=30):
    headers = {"Authorization": "Bearer " + str(accToken)}

    try:
        # print(url, files)
        r = requests.post(
            url, files=files, timeout=timeout, headers=headers, proxies=proxy
        )
        r.raise_for_status()
        resp = r.json()
        return resp
    except Exception:
        logger.exception("Failed file upload")
        raise


def put(accToken, url="", proxy={}, data={}, timeout=30):
    # accToken = access_token()

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + str(accToken),
    }

    try:
        logger.debug(url, data)
        req = requests.Request("PUT", url, data=data, headers=headers)
        # r = requests.post(url,  headers=headers, data=data, timeout=timeout)
        prepared = req.prepare()
        pretty_print_POST(prepared)
        s = requests.Session()
        res = s.send(prepared)

        res.raise_for_status()
        resp = res.json()
        logger.debug("resp = {}", resp)
        return resp

    except Exception:
        logger.exception("Fatal error in main loop")
        raise
