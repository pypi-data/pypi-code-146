
import time

import MakeOrBreak.utils as utils
import MakeOrBreak.notifications as notifications

def timer(): 
	print(utils.getSysArgs())
	choice = utils.getSysArgs()[1]
	interval = int(utils.getSysArgs()[2])

	#'1' hourly interval reminders
	#'2' custom interval
	#'3' random interval reminders

	while True:
		notifications.createNotification()

		randomTime = utils.generateRdmNumber(0, 3600)
		if choice == "1":
			time.sleep(3600)
		elif choice == "2":
			time.sleep(interval)
		else:
			time.sleep(randomTime)


if __name__ == "__main__":
	timer()
