import time

import utils
import notifications
# import MakeOrBreak.utils as utils
# import MakeOrBreak.notifications as notifications

def timer(): 
	mode = utils.getSysArgs()[1]
	choice = utils.getSysArgs()[2]
	interval = int(utils.getSysArgs()[3])

	#'1' hourly interval reminders
	#'2' custom interval
	#'3' random interval reminders

	while True:
		notifications.createNotification(int(mode) - 1)

		randomTime = utils.generateRdmNumber(0, 3600)
		if choice == "1":
			time.sleep(3600)
		elif choice == "2":
			time.sleep(interval)
		else:
			time.sleep(randomTime)


if __name__ == "__main__":
	timer()
