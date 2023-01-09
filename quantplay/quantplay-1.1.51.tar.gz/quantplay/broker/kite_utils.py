import time
import traceback

from retrying import retry
import getpass
from quantplay.utils.selenium_utils import Selenium
from quantplay.config.qplay_config import QplayConfig
import pyotp

class KiteUtils():
    zerodha_username = "zerodha_username"
    zerodha_password = "zerodha_password"
    zeordha_totp_unique_id = "zerodha_totp_unique_id"

    @staticmethod
    @retry(wait_exponential_multiplier=1000, wait_exponential_max=10000, stop_max_attempt_number=3)
    def get_request_token(kite_api_key=None):
        quantplay_config = QplayConfig.get_config()

        try:
            browser = Selenium.get_browser()

            # TODO api should be fetched from configuration

            kite_url = "https://kite.trade/connect/login?api_key={}&v=3".format(kite_api_key)
            print("Kite Url {}".format(kite_url))
            browser.get(kite_url)
            time.sleep(5)

            username = browser.find_element("xpath", '//*[@id="container"]/div/div/div[2]/form/div[1]/input')
            password = browser.find_element("xpath", '//*[@id="container"]/div/div/div[2]/form/div[2]/input')

            if KiteUtils.zerodha_username not in quantplay_config["DEFAULT"]:
                print("Enter zerodha username:")
                username_value = input()
            else:
                username_value = quantplay_config['DEFAULT'][KiteUtils.zerodha_username]

            if KiteUtils.zerodha_password not in quantplay_config["DEFAULT"]:
                print("Enter zerodha password:")
                password_value = getpass.getpass()
            else:
                password_value = quantplay_config['DEFAULT'][KiteUtils.zerodha_password]

            username.send_keys(username_value)
            password.send_keys(password_value)

            login_attempt = browser.find_element("xpath", '//*[@id="container"]/div/div/div[2]/form/div[4]/button')
            login_attempt.submit()
            time.sleep(5)

            kite_pin = browser.find_element("xpath", '//*[@id="container"]/div/div/div[2]/form/div[2]/input')

            if KiteUtils.zeordha_totp_unique_id not in quantplay_config["DEFAULT"]:
                print("Enter TOTP:")
                totp = input()
            else:
                unique_id = quantplay_config['DEFAULT'][KiteUtils.zeordha_totp_unique_id]
                totp = pyotp.TOTP(unique_id)
                totp = totp.now()

            kite_pin.send_keys(totp)
            time.sleep(3)

            login_attempt = browser.find_element("xpath", '//*[@id="container"]/div/div/div[2]/form/div[3]/button')
            login_attempt.submit()
            time.sleep(5)

            url = browser.current_url
            print("got kite url {}".format(url))
            request_token = url.split('token=')[1].split('&')[0]

            browser.close()

            return request_token
        except:
            print(traceback.print_exc())
            raise


if __name__ == '__main__':
    k = KiteUtils()
    k.get_request_token()
