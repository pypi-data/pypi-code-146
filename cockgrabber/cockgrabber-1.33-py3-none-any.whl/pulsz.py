# import argparse
import datetime
import os
import psycopg2
# import pytesseract
import requests
import time
import random
import undetected_chromedriver.v2 as uc
import zipfile

from twocaptcha import TwoCaptcha
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
DATABASE_URL="postgresql://victor:6OkPKgBQrktuaqnH2RgCzg@free-tier4.aws-us-west-2.cockroachlabs.cloud:26257/postal?sslmode=prefer&options=--cluster%3Dtundra-badger-3949"
NOPECHA_KEY = 'I-7T7KTE4NNMDU'

written = 0
goal = random.randint(50, 65)

def wait(secs=0):
    time.sleep(secs + random.random())

def solveRecaptcha(sitekey, url):
    solver = TwoCaptcha("8a587be4fe022de5e80be77f35da99ae")
    try:
        result = solver.recaptcha(
            sitekey=sitekey,
            url=url)
    except Exception as e:
        print(e)
    else:
        return result

def login(driver, username, password):
    print("Logging in...")
    driver.get("https://www.pulsz.com")

    try:
        WebDriverWait(driver, 8).until(EC.visibility_of_element_located((By.CLASS_NAME, "mt-progress-circle")))
        print("Logged in already")
    except TimeoutException:
        try:
            login_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Login')]")))
            login_button.click()

            username_box = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.NAME, "email")))
            username_box.send_keys(username)

            password_box = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.NAME, "password")))
            password_box.send_keys(password)
            password_box.send_keys(Keys.ENTER)

            print("Logged in")
        except TimeoutException:
            print("Login boxes not found")

def login_google(driver, username, password):
    print("Logging in with Google...")
    driver.get("https://www.pulsz.com/login")

    try:
        WebDriverWait(driver, 8).until(EC.visibility_of_element_located((By.CLASS_NAME, "mt-progress-circle")))
        print("Logged in already")
    except TimeoutException:
        try:
            google_box = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-test='Login with google']")))
            google_box.click()
            
            username_box = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "identifierId")))
            username_box.send_keys(username)
            username_box.send_keys(Keys.ENTER)

            password_box = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.NAME, "password")))
            password_box.send_keys(password)
            password_box.send_keys(Keys.ENTER)
            print("Logged in")
        except TimeoutException:
            print("Login boxes not found")


def close_modals(driver):
    try:
        print("Finding continue button")
        continue_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Continue')]")))
        wait(1)
        continue_button.click()
        print("Continue clicked")
    except TimeoutException:
        print("Continue button not found")

    try:
        print("Finding my stash button")
        my_stash_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Claim')]")))
        wait(1)
        my_stash_button.click()
        print("My stash claimed")
    except TimeoutException:
        print("My stash not found")

    try:
        print("Finding daily bonus button")
        daily_bonus_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class*='styles_claimBtn___pOxw']")))
        wait(1)
        daily_bonus_button.click()
        print("Daily bonus claimed")
    except TimeoutException:
        print("Daily bonus modal not found")

    try:
        print("Finding offer close button")
        offer_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-test='close-modal-button']")))
        wait(1)
        offer_button.click()
        print("Offer closed")
    except TimeoutException:
        print("Offer modal not found")

def postal(driver, username, password):
    global written

    conn = psycopg2.connect(DATABASE_URL)

    login(driver, username, password)
    wait(5)
    driver.get("https://www.pulsz.com/sweepstakes-code")
    # close_modals(driver)

    while written < goal:
        close_modals(driver)
        
        gotten = False
        while not gotten:
            try:
                print("Finding postal request button")
                postal_request_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class*='styles_btnRequest__lil_Q']")))
                wait(2)
                postal_request_button.click()
                print("Postal request button clicked")
                gotten = True
            except ElementClickInterceptedException:
                print("Something is blocking the postal request button, trying to close...")
                close_modals(driver)
            except TimeoutException:
                print("Failed to find postal request button")
                driver.save_screenshot('screenie5.png')
                raise

        # solved = False
        # prc

        try:
            print("Waiting for captcha to be solved...")
            # global prc
            prc = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[3]/main/div/div/div/h5/b'))).text
            # solved = True
        except TimeoutException:
            # print("Captcha solve timed out, falling back to 2Captcha")
            print("Captcha solve timed out")
            raise

        # if not solved:
        #     res = solveRecaptcha(
        #         "6Ldwj1EiAAAAADS3fd1KkbPRPYr--QE6-eGdpgjk",
        #         "https://www.pulsz.com/sweepstakes-code"
        #     )
        #     print("Captcha solved")

        #     code = res["code"]

        #     driver.execute_script(
        #         "document.getElementById('g-recaptcha-response').innerHTML='{}';".format(code)
        #     )
        #     driver.execute_script(
        #         "recaptchaCallback();"
        #     )

        #     global prc
        #     prc = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[3]/main/div/div/div/h5/b'))).text

        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO postal_codes (postal_code, casino_name, user_email, generate_time) VALUES (%s, %s, %s, now());", (prc, "pulsz", username)
            )
        conn.commit()
        print("Wrote new code: ", written, prc)
        written += 1

        wait(2)
        driver.refresh()

        rand_time = random.randint(300, 420)
        cur_time = datetime.datetime.now()
        next_time = cur_time + datetime.timedelta(seconds=rand_time)
        print("Current time is ", cur_time.time(), ". Waiting until ", next_time.time())
        wait(rand_time)

def postal_google(driver, username, password):
    global written

    conn = psycopg2.connect(DATABASE_URL)

    login_google(driver, username, password)
    close_modals(driver)

    while written < goal:
        driver.get("https://www.pulsz.com/sweepstakes-code")
        close_modals(driver)
        # try:
        #     print("Finding offer close button")
        #     offer_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-test='close-modal-button']")))
        #     offer_button.click()
        #     print("Offer closed")
        # except TimeoutException:
        #     print("Offer modal not found")
        
        gotten = False
        while not gotten:
            try:
                print("Finding postal request button")
                postal_request_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class*='styles_btnRequest__lil_Q']")))
                postal_request_button.click()
                print("Postal request button clicked")
                gotten = True
            except ElementClickInterceptedException:
                print("Something is blocking the postal request button, trying to close...")
                close_modals(driver)
            except TimeoutException:
                print("Failed to find postal request button")
                driver.save_screenshot('screenie5.png')
                raise

        print("Solving captcha")
        # driver.save_screenshot('captcha1.png')
        res = solveRecaptcha(
            "6Ldwj1EiAAAAADS3fd1KkbPRPYr--QE6-eGdpgjk",
            "https://www.pulsz.com/sweepstakes-code"
        )
        print("Captcha solved")
        # driver.save_screenshot('captcha2.png')

        code = res["code"]

        # driver.save_screenshot('captcha3.png')
        driver.execute_script(
            "document.getElementById('g-recaptcha-response').innerHTML='{}';".format(code)
        )
        driver.execute_script(
            "recaptchaCallback();"
        )

        prc = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[3]/main/div/div/div/h5/b'))).text

        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO postal_codes (postal_code, casino_name, user_email, generate_time) VALUES (%s, %s, %s, now());", (prc, "pulsz", username)
            )
        conn.commit()
        print("Wrote new code: ", written, prc)
        written += 1

        rand_time = random.randint(300, 420)
        cur_time = datetime.datetime.now()
        next_time = cur_time + datetime.timedelta(seconds=rand_time)
        print("Current time is ", cur_time.time(), ". Waiting until ", next_time.time())
        wait(rand_time)

def get_pulsz(username, password):
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

    driver.quit()

def get_pulsz_google(username, password):
    global written

    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options)

    while written < goal:
        # login_google(driver, username, password)
        try:
            postal_google(driver, username, password)
        except Exception as e:
            print("Postal failed with error: ", e)

    driver.quit()
