"""Provides methods for interacting with the Bitfount Web services."""
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
import json
import logging
from pathlib import Path
import threading
import time
from typing import Generator, Tuple

import chromedriver_autoinstaller
from requests import HTTPError
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from bitfount.config import (
    _DEVELOPMENT_ENVIRONMENT,
    _STAGING_ENVIRONMENT,
    _get_environment,
)
from bitfount.hub.api import BitfountAM, BitfountSession
from bitfount.hub.authentication_flow import _get_auth_environment
from bitfount.hub.authentication_handlers import (
    _HUB_API_IDENTIFIER,
    _SCOPES,
    ExternallyManagedJWTHandler,
)
from bitfount.hub.types import _DEV_AM_URL, _STAGING_AM_URL, PRODUCTION_AM_URL
from bitfount.utils import web_utils

SCREENSHOT_DIRECTORY: Path = Path("selenium-screenshots")
IMPLICIT_WAIT_TIME = 8  # seconds; high value due to slow GitHub runner

logger = logging.getLogger(__name__)


@contextmanager
def webdriver_factory(
    wait_time: int = IMPLICIT_WAIT_TIME,
) -> Generator[WebDriver, None, None]:
    """Create a Selenium webdriver instance."""
    chromedriver_autoinstaller.install()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    with webdriver.Chrome(options=chrome_options) as driver:
        driver.implicitly_wait(wait_time)
        yield driver


def save_screenshot(file_name: str, driver: WebDriver) -> None:
    """Saves a screenshot of the Selenium driver view."""
    SCREENSHOT_DIRECTORY.mkdir(parents=True, exist_ok=True)
    file_path = SCREENSHOT_DIRECTORY / f"{file_name}_{str(int(time.time()))}.png"
    file_path = file_path.resolve()
    driver.get_screenshot_as_file(str(file_path))
    logger.error(f"Screenshot saved to {file_path}")


def _oauth_sign_in(username: str, password: str, driver: WebDriver) -> None:
    """Sign in to the oauth form using the supplied username and password."""
    logger.info(f"OAuth sign in for {username} at {driver.current_url}")
    try:
        # Supply login details to Auth0 login panel
        driver.find_element(
            by=By.CSS_SELECTOR, value="input[name='username']"
        ).send_keys(username)
        driver.find_element(
            by=By.CSS_SELECTOR, value="input[name='password']"
        ).send_keys(password)
        driver.find_element(by=By.CSS_SELECTOR, value="button[name='action']").click()
    except Exception as e:
        logger.error("Exception encountered whilst signing in.")
        save_screenshot("perform_login", driver)
        raise e


class ExtendedBitfountAM(BitfountAM):
    """Extends BitfountAM with methods relevant to testing."""

    def __init__(self, session: BitfountSession, access_manager_url: str):
        logger.info(f"Using {access_manager_url} for access manager")
        super().__init__(session, access_manager_url)

    def grant_proactive_access(
        self, pod_id: str, user_to_grant: str, role: str
    ) -> None:
        """Sets a pod to grant proactive access to the username specified."""
        response = self.session.post(
            f"{self.access_manager_url}/api/casbin",
            timeout=10,
            json={
                "podIdentifier": pod_id,
                "grantee": user_to_grant,
                "role": role,
            },
        )

        if response.status_code not in (200, 201):
            raise HTTPError(
                f"Unexpected response ({response.status_code}): {response.text}"
            )


def get_bitfount_session(
    username: str,
    password: str,
    token_dir: Path,
) -> BitfountSession:
    """Creates and returns a BitfountSession that uses Resource Owner Password Flow."""
    bf_env = _get_auth_environment()
    logger.info(f"Webdriver is using {bf_env.auth_domain} for user {username}")

    def get_token() -> Tuple[str, datetime]:
        body = {
            "grant_type": "password",
            "username": username,
            "password": password,
            "audience": _HUB_API_IDENTIFIER,
            "scope": _SCOPES,
            "client_id": bf_env.client_id,
        }

        response = web_utils.post(
            f"https://{bf_env.auth_domain}/oauth/token", data=body
        ).json()
        logger.error(json.dumps(response))
        return response["access_token"], datetime.now(timezone.utc) + timedelta(
            seconds=response["expires_in"]
        )

    token, expiry = get_token()

    handler = ExternallyManagedJWTHandler(token, expiry, get_token, username)

    handler.user_storage_path = token_dir / username
    session = BitfountSession(
        authentication_handler=handler,
    )

    return session


def oidc_flow(
    url: str,
    username: str,
    password: str,
) -> None:
    """Opens provided oidc url and logs in before closing browser.

    This is run in a separate thread so that the Modeller can respond to the challenges
    from the pods. Otherwise this ends up blocking the Modeller.

    Args:
        url (str): the oidc authentication url to open. This is provided at run-time.
        username (str): the username of the user to log in as
        password (str): the password of the user
    """

    def execute_oidc_flow() -> None:
        with webdriver_factory() as driver:
            try:
                logger.warning("opening url in browser")
                driver.get(url)

                # Wait for a maximum of 30 seconds for the OIDC Confirmation to appear
                # The webdriver won't wait for the full 30 seconds if the element is
                # located before this time.
                WebDriverWait(driver, 30).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, '//button[@value="confirm"]')
                    )
                )
                driver.find_element_by_css_selector("button[value='confirm']").click()

                _oauth_sign_in(username, password, driver)

                # Wait for a maximum of 30 seconds for the device to connect
                WebDriverWait(driver, 30).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, "//p[text()='Your device is now connected.']")
                    )
                )

            except Exception as e:
                logger.error(
                    f"Exception encountered whilst attempting to perform oidc auth "
                    f"verification at {url}."
                )
                save_screenshot("do_oidc_verification", driver)
                raise e

    oidc_thread = threading.Thread(target=execute_oidc_flow, name="oidc")
    oidc_thread.start()


def grant_proactive_access(
    modeller_username: str,
    pod_id: str,
    role: str,
    pod_session: BitfountSession,
) -> None:
    """Grants proactive access to a pod for a given modeller."""
    bf_env = _get_environment()
    if bf_env == _STAGING_ENVIRONMENT:
        am_url = _STAGING_AM_URL
    elif bf_env == _DEVELOPMENT_ENVIRONMENT:
        am_url = _DEV_AM_URL
    else:
        am_url = PRODUCTION_AM_URL

    am = ExtendedBitfountAM(pod_session, am_url)
    am.grant_proactive_access(
        pod_id=pod_id,
        user_to_grant=modeller_username,
        role=role,
    )
