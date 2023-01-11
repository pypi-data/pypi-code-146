import pyrebase
import os
from dotenv import load_dotenv
load_dotenv()

config = {
  "apiKey": os.environ.get("API_KEY"),
  "authDomain": os.environ.get("AUTH_DOMAIN"),
  "databaseURL": os.environ.get("DATABASE_URL"),
  "projectId": os.environ.get("PROJECT_ID"),
  "storageBucket": os.environ.get("STORAGE_BUCKET"),
  "messagingSenderId": os.environ.get("MESSAGING_SENDER_ID"),
  "appId": os.environ.get("APP_ID"),
  "measurementId": os.environ.get("MEASUREMENT_ID")
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()


def run_steps():
    start_time = time.time()
    step = 1
    total_time = 0
    while step <= 10:
        start_step_time = time.time()
        message = f"Current step: {step}"
        logger.info(message)
        db.child("logs").push({"message": message, "level": "info", "timestamp": time.time()})
        entered_step = input("Please enter the number of the step: ")
        end_step_time = time.time()
        step_time = end_step_time - start_step_time
        total_time += step_time
        if entered_step != str(step):
            if entered_step == 'exit':
                message = f"User decided to exit the script"
                logger.info(message)
                db.child("logs").push({"message": message, "level": "info", "timestamp": time.time()})
            else:
                message = f"Incorrect step entered. Exiting... Step time taken: {step_time} seconds"
                logger.info(message)
                db.child("logs").push({"message": message, "level": "info", "timestamp": time.time()})
                message = f"User stopped at step {step} because of 'incorrect step entered'"
                logger.info(message)
                db.child("logs").push({"message": message, "level": "info", "timestamp": time.time()})
            break
        message = f"Proceeding to step {step+1}... Step time taken: {step_time} seconds"
        logger.info(message)
        db.child("logs").push({"message": message, "level": "info", "timestamp": time.time()})
        step += 1
    else:
        end_time = time.time()
        total_time = end_time - start_time
        message = "All steps completed!"
        logger.info(message)
        db.child("logs").push({"message": message, "level": "info", "timestamp": time.time()})
        message = f"Total time taken: {total_time} seconds"
        logger.info(message)
        db.child("logs").push({"message": message, "level": "info", "timestamp": time.time()})