from .components import *
from selenium.webdriver.common.by import By
import speech_recognition as sr
import subprocess
import os
import urllib
from time import sleep

class Recaptcha_Solver:
	"""
	Usage:
		solver = Recaptcha_Solver(driver)
		solver.solve_recaptcha()
	How to use:
		1. Pass your webdriver variable in driver param
	"""
	def __init__(self,driver,debug=False):
		self.driver=driver
		self.mp3='captcha.mp3'
		self.wav='captcha.wav'
		self.time_to_sleep_after_submit=3
		self.debug=debug

	def solve_recaptcha(self):
		self.driver.switch_to.default_content()
		iframe1=find_until_located(self.driver,By.XPATH,'//*[@title="reCAPTCHA"]')
		self.driver.switch_to.frame(iframe1)
		sleep(1)
		find_until_clicklable(self.driver,By.CLASS_NAME,'recaptcha-checkbox-border').click()
		sleep(1)
		self.driver.switch_to.default_content()
		try:
			self.driver.find_element(By.CLASS_NAME, 'recaptcha-checkbox-checked')
			return True
		except:
			pass
		iframe2=find_until_located(self.driver,By.XPATH,'//*[@title="recaptcha challenge expires in two minutes"]')
		self.driver.switch_to.frame(iframe2)
		sleep(1)
		find_until_clicklable(self.driver,By.ID,'recaptcha-audio-button').click()
		sleep(1)
		err=True
		try:
			header_text=self.driver.find_element(By.CLASS_NAME,'rc-doscaptcha-header-text')
		except:
			err=False

		if err:
			self.driver.switch_to.default_content()
			raise Exception('Sorry, looks like google blocking the captcha.' + header_text.text)

		if self.debug==True:
			print('Solving Captcha...')
		audio_url=find_until_located(self.driver,By.CLASS_NAME,'rc-audiochallenge-tdownload-link').get_attribute('href')
		if self.debug==True:
			print('Downloading Audio...')
		urllib.request.urlretrieve(audio_url, self.mp3)
		if self.debug==True:
			print('Processing audio...')
		
		mp3_to_wav(self.mp3, self.wav)

		r=sr.Recognizer()

		def recognize_audio(wav_file):
			with sr.AudioFile(wav_file) as source:
				r.adjust_for_ambient_noise(source)
				audio=r.listen(source)
				text=r.recognize_google(audio, language='en-US')
				return text


		if self.debug==True:
			print('Recognizing audio...')
		try:
			text=recognize_audio(self.wav)
		except:
			self.driver.refresh()
			return self.solve_recaptcha()

		os.remove(self.mp3)
		os.remove(self.wav)

		find_until_located(self.driver,By.ID,'audio-response').send_keys(text)
		sleep(1)
		find_until_clicklable(self.driver,By.ID,'recaptcha-verify-button').click()
		sleep(self.time_to_sleep_after_submit)
		msg=find_until_located(self.driver,By.CLASS_NAME,'rc-audiochallenge-error-message').text
		if msg!='':
			self.driver.switch_to.default_content()
			raise Exception(f'Captcha Could not be solved. Error: {str(msg)}')
		else:
			if self.debug==True:
				print('Successfully Solved')
			self.driver.switch_to.default_content()