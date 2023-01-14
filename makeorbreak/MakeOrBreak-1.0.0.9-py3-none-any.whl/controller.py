import time
from utils import generateRdmNumber
from notifications import createNotification

def timer(type, delay): 
	#'1' hourly interval reminders
	#'2' custom interval
	#'3' random interval reminders

	while True:
		createNotification()

		randomTime = generateRdmNumber(0, 3600)
		if type == 1:
			time.sleep(3600)
		elif type == 2:
			time.sleep(delay)
		else:
			time.sleep(randomTime)


if __name__ == "__main__":
	timer(2, 1)
