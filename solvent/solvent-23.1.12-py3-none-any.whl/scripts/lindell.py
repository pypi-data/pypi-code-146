import time

import log
import pomace

from . import Script


class MyPillow(Script):

    URL = "https://www.mypillow.com/"

    def run(self, page: pomace.Page) -> pomace.Page:
        person = pomace.fake.person

        pomace.shared.client.clear_cookies()
        page = pomace.visit(self.URL)

        log.debug("Waiting for modal...")
        for _ in range(10):
            time.sleep(0.5)
            modal = pomace.shared.browser.find_by_id("ltkpopup-content")
            if modal and modal.visible:
                break
        else:
            log.warn("No modal found")

        log.info(f"Submitting email address: {person.email_address}")
        page.fill_email_address(person.email_address)
        page = page.click_activate_offer(wait=1)
        log.info(f"Submitting phone number: {person.phone}")
        page.fill_phone(person.phone)
        return page.click_get_mobile_alerts(wait=1)

    def check(self, page: pomace.Page) -> bool:
        success = "Thanks!" in page
        if success:
            page.click_continue_shopping(wait=0)
        return success


class FrankSpeech(Script):

    URL = "https://frankspeech.com/"
    SKIP = True

    def run(self, page: pomace.Page) -> pomace.Page:
        person = pomace.fake.person

        if "Access denied" in page:
            raise RuntimeError

        page = page.click_profile(wait=0)
        page = page.click_sign_up()

        page.fill_phone(person.phone)
        page.click_confirm(wait=0)
        page.fill_email(person.email)
        page.fill_username(person.username)
        # TODO: Get this working
        # page.fill_password(person.password)
        # page.fill_confirm_password(person.password)

        return page.click_create_new_account()

    def check(self, page: pomace.Page) -> bool:
        return "prod-static" not in page.url
