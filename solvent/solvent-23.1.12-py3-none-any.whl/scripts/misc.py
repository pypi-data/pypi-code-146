import random

import pomace

from . import Script


class TommyBryant(Script):

    URL = "https://www.cityoftarrant.com/contact"

    def run(self, page: pomace.Page) -> pomace.Page:
        person = pomace.fake.person

        pomace.log.info(f"Beginning iteration as {person}")
        page.fill_first_name(person.first_name)
        page.fill_last_name(person.last_name)
        page.fill_email(person.email)
        page.fill_comment(
            random.choice(
                [
                    "Tommy Bryant must resign over his racist comments.",
                    "Tommy Bryant's racism doesn't belong in Alabama.",
                    "Get Tommy Bryant out of our city council.",
                    "Tarrant is better than Tommy Bryant. He must go!",
                    "I'm going to keep email the City of Tarrant until Tommy Bryant resigns.",
                ]
            )
        )
        page.fill_captcha("Blue")
        return page.click_submit()

    def check(self, page: pomace.Page) -> bool:
        return "submission has been received" in page


class PatriotPage(Script):

    URL = "https://patriotpage.org"

    def run(self, page: pomace.Page) -> pomace.Page:
        person = pomace.fake.person

        pomace.log.info(f"Beginning iteration as {person}")
        page = page.click_create_an_account()
        page.fill_email(person.email)
        page.fill_confirm_email(person.email)
        page.fill_password(person.password)
        page.fill_confirm_password(person.password)
        page.fill_first_name(person.first_name)
        page.fill_last_name(person.last_name)
        page.fill_nickname(person.nickname)
        page.fill_country("United States")
        page.fill_selection(
            random.choice(
                [
                    "Precinct delegate",
                    "Poll Watcher",
                    "Poll Challenger",
                    "Election Inspector",
                    "Patriot Approved Candidate",
                    "Grassroots Patriot Leader",
                    "Patriot Volunteer",
                ]
            )
        )
        page.browser.execute_script('document.getElementsByTagName("a")[3].remove()')
        page.browser.execute_script('document.getElementsByTagName("a")[3].remove()')
        page.click_agree(wait=0)

        pomace.log.info("Creating account")
        return page.click_create_account(wait=1)

    def check(self, page: pomace.Page) -> bool:
        return "We’re almost there!" in page


class HeyHandy(Script):

    URL = "https://heyhandy.xyz"
    SKIP = True  # CAPTCHA added

    def run(self, page: pomace.Page) -> pomace.Page:
        person = pomace.fake.person

        pomace.log.info(f"Beginning iteration as {person}")
        page = page.click_handy_makes(wait=1)
        page.fill_first_name(person.first_name)
        page.fill_last_name(person.last_name)
        page.fill_email(person.email)

        subject, message = random.choice(
            [
                (
                    "Hello",
                    "I want to learn more about NFTs.",
                ),
                (
                    "Help Me",
                    "Your water bottle is tracking me and I need it to stop.",
                ),
                (
                    "Stop This",
                    "You need to stop scamming people with NFTs.",
                ),
                (
                    "Stop Tracking Me",
                    "I demand you stop tracking me.",
                ),
            ]
        )

        page.fill_subject(subject)
        page.fill_message(message)
        return page.click_submit(wait=1)

    def check(self, page: pomace.Page) -> bool:
        return "Successfully submitted!" in page


class HelmsOptical(Script):

    URL = "https://helmsoptical.com"

    def run(self, page) -> pomace.Page:
        page.click_contact_us()

        person = pomace.fake.person
        page.fill_name(person.name)
        page.fill_email(person.email)
        page.fill_message(
            random.choice(
                [
                    "Since Barbara is an anti-gay bigot I will find a different doctor.",
                    "Barbara is harassing my children. How do I change doctors?",
                    "🏳️‍🌈",
                    "Barbara is hurting the kids at my school. Please transfer me to a different location.",
                ]
            )
        )
        return page.click_send(wait=1)

    def check(self, page) -> bool:
        return "Thank you" in page or "Contact Us" in page


class FamilyFare(Script):

    URL = "https://www.shopfamilyfare.com/p/help/message"
    SKIP = True  # CAPTCHA added

    def run(self, page) -> pomace.Page:
        person = pomace.fake.person
        pomace.log.info(f"Beginning iteration as {person}")
        page.fill_first_name(person.first_name)
        page.fill_last_name(person.last_name)
        page.fill_email_address(person.email_address)
        page.fill_phone(person.phone)
        page.select_store(
            random.choice(
                [
                    "Leonard (254)",
                    "Lake Michigan Dr (339)",
                    "Northland Dr (636)",
                    "Fulton Heights (1587)",
                ]
            )
        )
        page.select_subject("Feedback")
        page.fill_message("Abortion is a human right! Tony Sarsam should resign.")
        return page.click_send(wait=1)

    def check(self, page) -> bool:
        success = "Thank you for your message" in page
        page.browser.reload()
        return success
