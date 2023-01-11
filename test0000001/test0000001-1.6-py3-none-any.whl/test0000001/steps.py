import pyrebase
import os
from dotenv import load_dotenv
import time
import logging
import logger
import uuid
from datetime import datetime

load_dotenv()

config = {
  "apiKey": os.environ.get("API_KEY"),
  "authDomain": os.environ.get("AUTH_DOMAIN"),
  "databaseURL": "https://test0000001-e47d5-default-rtdb.firebaseio.com",
  "projectId": os.environ.get("PROJECT_ID"),
  "storageBucket": os.environ.get("STORAGE_BUCKET"),
  "messagingSenderId": os.environ.get("MESSAGING_SENDER_ID"),
  "appId": os.environ.get("APP_ID"),
  "measurementId": os.environ.get("MEASUREMENT_ID")
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()


def run_steps():
    function_id = str(uuid.uuid4())
    start_time = time.time()
    step = 1
    total_time = 0
    while step <= 5:
        start_step_time = time.time()
        message = f"Current step: {step}"
        logging.info(message)
        db.child("logs").push({"function_id": function_id, "message": message, "level": "info", "timestamp": datetime.utcnow().isoformat()})
        entered_step = input("Please enter the number of the step: ")
        end_step_time = time.time()
        step_time = end_step_time - start_step_time
        total_time += step_time
        if entered_step != str(step):
            if entered_step == 'exit':
                message = f"User decided to exit the script"
                logging.info(message)
                db.child("logs").push({"function_id": function_id, "message": message, "level": "info", "timestamp": datetime.utcnow().isoformat()})
            else:
                message = f"Incorrect step entered. Exiting... Step {step} time taken: {step_time} seconds"
                logging.info(message)
                db.child("logs").push({"function_id": function_id, "message": message, "level": "info", "timestamp": datetime.utcnow().isoformat()})
                message = f"User stopped at step {step} because of 'incorrect step entered'"
                logging.info(message)
                db.child("logs").push({"function_id": function_id, "message": message, "level": "info", "timestamp": datetime.utcnow().isoformat()})
            break
        message = f"Proceeding to step {step+1}... Step {step} time taken: {step_time} seconds"
        logging.info(message)
        db.child("logs").push({"function_id": function_id, "message": message, "level": "info", "timestamp": datetime.utcnow().isoformat()})
        step += 1
    else:
        end_time = time.time()
        total_time = end_time - start_time
        message = "All steps completed!"
        logging.info(message)
        db.child("logs").push({"function_id": function_id, "message": message, "level": "info", "timestamp": datetime.utcnow().isoformat()})
        message = f"Total time taken: {total_time} seconds"
        logging.info(message)
        db.child("logs").push({"function_id": function_id, "message": message, "level": "info", "timestamp": datetime.utcnow().isoformat()})