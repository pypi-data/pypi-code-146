#!/usr/bin/env python

# Import essential packages 
import time
import os
import random 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
import sys
import chromedriver_autoinstaller
import datetime
import argparse

def main():

	# Clear the screen
	os.system('cls' if os.name == 'nt' else 'clear')

	from pyfiglet import Figlet
	f = Figlet(font='slant')
	print(f.renderText("UNIST Special Agent Work Time Calculator"))
	print("INFO 해당 프로그램은 유저의 아이디와 비번을 입력받아, ")
	print("INFO 전문연구요원 복무관리 시스템에서 남은 근무 시간을 유저에게 알려줍니다.")
	print("INFO 오늘이 근무 마지막 날일 때, 퇴근이 가능한 시간을 알아보세요. \n")

	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--id', type=str, help='ID')
	parser.add_argument('-p', '--pw', type=str, help='PW')
	args = parser.parse_args()

	# ------------------------------
	# ID / PW input from USER
	getID = args.id
	getPW = args.pw
	# ------------------------------

	# If the user doesn't input the ID and PW, the program will ask for it.
	if getID == None:
		getID = input("Portal ID를 입력하세요: ")
	if getPW == None:
		getPW = input("Portal PW를 입력하세요: ")

	options = webdriver.ChromeOptions()
	options.add_argument('--ignore-ssl-errors=yes')
	options.add_argument('--ignore-certificate-errors')
	options.add_argument('--headless')
	options.add_argument('--no-sandbox')
	options.add_argument('--disable-dev-shm-usage')
	options.add_argument('window-size=1200x750')

	# Install the chromedriver
	chromedriver_autoinstaller.install()

	driver = webdriver.Chrome('chromedriver', options=options)
	time.sleep(1)

	driver.get('https://114.70.1.101/unistSM/user/login/login.do')
	time.sleep(1)

	# 1. LOGIN
	try:
		idInput = driver.find_element("xpath", "/html/body/div/div/div[1]/div/div/form/p[1]/input")
		idInput.send_keys(getID) # MyID

		pwInput = driver.find_element("xpath", "/html/body/div/div/div[1]/div/div/form/p[2]/input")
		pwInput.send_keys(getPW) # MyPW
		pwInput.send_keys(Keys.ENTER)

		time.sleep(random.uniform(1,2))

	except NoSuchElementException:
		driver.switch_to.alert.accept() 
		print(error)
		driver.close()

	try:
		# Get the value of the span tag
		spanTag = driver.find_element("xpath", "/html/body/div/div/div[3]/div/div[2]/div[1]/div/div/p[2]/span")
		spanValue = spanTag.text
		spanValue = int(spanValue)

		# Get the value of the em tag
		emTag = driver.find_element("xpath", "/html/body/div/div/div[3]/div/div[2]/div[1]/div/div/p[2]/em")
		emValue = emTag.text
		emValue = int(emValue)

		# Calculate the total work time for the week
		totalWorkTime = spanValue * 60 + emValue

	except NoSuchElementException:
		driver.switch_to.alert.accept()
		print(error)
		driver.close()

	print("INFO 이번 주 총 근무 시간은 " + str(totalWorkTime // 60) + "시간 " + str(totalWorkTime % 60) + "분 입니다.")

	try:
		# Get the value of the span tag
		enterTag = driver.find_element("xpath", "/html/body/div/div/div[3]/div/div[2]/div[2]/div[1]/ul/li[1]/span")
		enterValue = enterTag.text
		enterValue = enterValue[3:]

		outTag = driver.find_element("xpath", "/html/body/div/div/div[3]/div/div[2]/div[2]/div[1]/ul/li[2]/span")
		outValue = outTag.text
		outValue = outValue[3:]

	except NoSuchElementException:
		driver.switch_to.alert.accept()
		print(error)
		driver.close()

	print("INFO 오늘의 출근 시간은 " + enterValue + " 입니다.")
	print("INFO 오늘의 퇴근 시간은 " + outValue + " 입니다.")
	print("INFO 총 남은 근무 시간은 " + str((2400 - totalWorkTime) // 60) + "시간 " + str((2400 - totalWorkTime) % 60) + "분" + " 입니다.")

	currentTime = datetime.datetime.now()
	currentHour = currentTime.hour
	currentMinute = currentTime.minute
	print("INFO 현재 시간은 " + str(currentHour) + "시 " + str(currentMinute) + "분 입니다.")

	if totalWorkTime >= 2400:
		print("INFO 이번 주 40시간을 모두 채웠습니다. 축하합니다!")

	else:
		enterHour = int(enterValue[:2])
		enterMinute = int(enterValue[3:])

		outHour = int(outValue[:2])
		outMinute = int(outValue[3:])

		timeRemaining = 2400 - totalWorkTime

		timeRemainingHour = timeRemaining // 60
		timeRemainingMinute = timeRemaining % 60

		# Ask the user if today is the last day.
		lastDay = input("INFO 오늘이 마지막 날입니까? (y/n) ")

		if lastDay == "y" or lastDay == "Y":
			# Exclude the time if the working time contains 12:00 to 13:00 or 18:00 to 19:00
			if enterHour < 12 and currentHour >= 12:
				timeRemainingHour = timeRemainingHour + 1

			if enterHour < 18 and currentHour >= 18:
				timeRemainingHour = timeRemainingHour + 1

			# Calculate the okay time
			okayTime = enterHour + timeRemainingHour
			okayTimeMinute = enterMinute + timeRemainingMinute

			if okayTimeMinute >= 60:
				okayTime = okayTime + 1
				okayTimeMinute = okayTimeMinute - 60
			
			print("INFO 오늘은 마지막 날입니다. 40시간을 채우기 위해 오늘 퇴근 가능한 시간은 " + str(okayTime) + "시 " + str(okayTimeMinute + 1) + "분 부터입니다.")

		else:
			print("INFO 오늘은 마지막 날이 아닙니다. 마지막 날일 때 사용해주세요.")

		# quit the browser
		driver.close()

if __name__ == "__main__": 
	main()