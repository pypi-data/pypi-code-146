from code import interact
import time
from utils import generateRdmNumber, getSysArgs
from notifications import createNotification

def timer(): 
	choice = getSysArgs()[1]
	interval = int(getSysArgs()[2])

	#'1' hourly interval reminders
	#'2' custom interval
	#'3' random interval reminders

	while True:
		createNotification()

		randomTime = generateRdmNumber(0, 3600)
		if choice == "1":
			time.sleep(3600)
		elif choice == "2":
			time.sleep(interval)
		else:
			time.sleep(randomTime)


if __name__ == "__main__":
	timer()
