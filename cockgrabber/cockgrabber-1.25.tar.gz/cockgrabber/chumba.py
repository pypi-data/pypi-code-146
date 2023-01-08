import datetime
import psycopg2
import pytesseract

import os
import requests
import zipfile
import time
import random
import undetected_chromedriver.v2 as uc

from twocaptcha import TwoCaptcha
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
DATABASE_URL="postgresql://victor:6OkPKgBQrktuaqnH2RgCzg@free-tier4.aws-us-west-2.cockroachlabs.cloud:26257/postal?sslmode=prefer&options=--cluster%3Dtundra-badger-3949"
NOPECHA_KEY = 'I-7T7KTE4NNMDU'

written = 0
goal = random.randint(50, 60)

def wait(secs=0):
    time.sleep(secs + random.random())

# def solveRecaptcha(sitekey, url):
#     solver = TwoCaptcha("8a587be4fe022de5e80be77f35da99ae")
#     try:
#         result = solver.recaptcha(
#             sitekey=sitekey,
#             url=url)
#     except Exception as e:
#         print(e)
#     else:
#         return result

def login(driver, username, password):
    print("Logging in...")
    driver.get("https://www.chumbacasino.com/")

    try:
        login_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Login')]")))
        login_button.click()

        username_box = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.NAME, "email")))
        username_box.send_keys(username)

        password_box = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.NAME, "password")))
        password_box.send_keys(password)

        wait(1)
        password_box.send_keys(Keys.ENTER)
        print("Logged in")
    except TimeoutException:
        print("Could not login")

def relog(driver, username, password):
    print("Trying to log in again...")
    try:
        username_box = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.NAME, "email")))
        username_box.send_keys(username)

        password_box = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.NAME, "password")))
        password_box.send_keys(password)

        wait(1)
        password_box.send_keys(Keys.ENTER)
        print("Logged in")
        return True
    except TimeoutException:
        print("Could not login")
        return False

def close_modals(driver):
    try:
        print("Finding daily bonus claim button")
        daily_bonus_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "daily-bonus__claim-btn")))
        daily_bonus_button.click()
        print("Daily bonus claimed")
    except TimeoutException:
        print("Daily bonus modal not found")

    try:
        print("Finding offer close button")
        offer_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "offer__close")))
        offer_button.click()
        print("Offer closed")
    except TimeoutException:
        print("Offer modal not found")

def postal(driver, username, password):
    global written

    conn = psycopg2.connect(DATABASE_URL)

    login(driver, username, password)
    close_modals(driver)

    while written < goal:
        close_modals(driver)
        try:
            print("Finding table games button")
            table_games_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "TOP_HUD__table-games_link")))
            wait(2)
            table_games_button.click()
            print("Table games button")
        except TimeoutException:
            print("Failed to find table games button")
            close_modals(driver)
            if not relog(driver, username, password):
                raise

        try:
            print("Finding footer button")
            footer_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "footer__postal-request-code")))
            wait(3)
            footer_button.click()
            print("Footer button clicked")
        except TimeoutException:
            print("Failed to find footer button")
            close_modals(driver)
            if not relog(driver, username, password):
                raise

        try:
            print("Finding postal request button")
            postal_request_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "get-postal-request-code")))
            wait(2)
            postal_request_button.click()
            print("Postal request button clicked")
        except TimeoutException:
            print("Failed to find postal request button")
            close_modals(driver)
            if not relog(driver, username, password):
                raise

        # try:
        #     WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[title='reCAPTCHA']")))
        # except TimeoutException:
        #     print("Failed to find captcha")
        #     raise

        # print("Solving captcha")
        # # driver.save_screenshot('captcha1.png')
        # res = solveRecaptcha(
        #     "6LfvyQ0iAAAAAGBPXO2PBIW1JLftMPb47T8IxORq",
        #     "https://payments.vgwgroup.net/"
        # )
        # print("Captcha solved")
        # # driver.save_screenshot('captcha2.png')

        # code = res["code"]

        # # driver.save_screenshot('captcha3.png')
        # driver.execute_script(
        #     "___grecaptcha_cfg.clients['0']['V']['V']['callback'](" "'" + code + "')"
        # )

        try:
            print("Waiting for captcha to be solved...")
            prc_image = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[style*='border: 3px solid']")))
        except TimeoutException:
            print("Captcha solve timed out")
            raise

        prc_image.screenshot("code.png")
        prc = pytesseract.image_to_string("code.png").strip()

        # with open("chumba-codes.txt", "a") as myfile:
        #     myfile.write(prc + "\n")
        #     print("Wrote new code: ", prc)

        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO postal_codes (postal_code, casino_name, user_email, generate_time) VALUES (%s, %s, %s, now());", (prc, "chumba", username)
            )
        conn.commit()
        print("Wrote new code: ", written, prc)
        written += 1

        try:
            print("Finding return button")
            return_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "return")))
            wait(2)
            return_button.click()
            print("Return button clicked")
        except TimeoutException:
            print("Failed to find return button")
            close_modals(driver)
            if not relog(driver, username, password):
                raise

        rand_time = random.randint(300, 436)
        cur_time = datetime.datetime.now()
        next_time = cur_time + datetime.timedelta(seconds=rand_time)
        print("Current time is ", cur_time.time(), ". Waiting until ", next_time.time())
        wait(rand_time)

def get_chumba(username, password):
    global written

    options = uc.ChromeOptions()
    # options.add_argument('--no-sandbox')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-dev-shm-usage')
    # options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--no-first-run --no-service-autorun --password-store=basic')

    with open('chrome.zip', 'wb') as f:
        f.write(requests.get('https://nopecha.com/f/chrome.zip').content)
    with zipfile.ZipFile('chrome.zip', 'r') as zip_ref:
        zip_ref.extractall('nopecha')
    options.add_argument(f"--load-extension={os.getcwd()}/nopecha")

    driver = uc.Chrome(options=options, user_data_dir=f"{os.getcwd()}/profile")

    print("Getting NopeCHA key...")
    driver.get(f"https://nopecha.com/setup#{NOPECHA_KEY}|awscaptcha_solve_delay_time=6969")

    while written < goal:
        # login(driver, username, password)
        try:
            postal(driver, username, password)
        except Exception as e:
            print("Postal failed with error: ", e)
