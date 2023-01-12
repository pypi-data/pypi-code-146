from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib, requests, base64

def mp3_to_wav(mp3_file_name, wav_file_name):
    data=urllib.parse.quote(base64.b64encode(open(mp3_file_name, 'rb').read()).decode())
    resp=requests.post('https://mp3towav.onrender.com/', headers={'Content-Type': 'application/x-www-form-urlencoded'}, data='data='+data)
    urllib.request.urlretrieve(resp.json()['link'], wav_file_name)
    return True

def wait(driver,time=5):
	driver.implicitly_wait(time)

def find_until_located(driver,find_by,name,timeout=60):
	return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((find_by, name)))

def find_until_clicklable(driver,find_by,name,timeout=60):
	return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((find_by, name)))

def scroll_to_element(driver,element):
	driver.execute_script("arguments[0].scrollIntoView();", element)
