import time
from randomNumberGenerator import generateRdmNumber

def timer(type, delay): 

	#'1' hourly interval reminders
	#'2' custom interval
	#'3' random interval reminders

	while True:
		randomTime = generateRdmNumber(0, 3600)
		if type == 1:
			time.sleep(3600)
		elif type == 2:
			time.sleep(delay)
		else:
			time.sleep(randomTime)

if __name__ == "__main__":
	timer(3, 3600)

