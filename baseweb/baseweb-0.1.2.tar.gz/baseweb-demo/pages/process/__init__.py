import os
from datetime import datetime, timedelta
import random

# def random_date_between(start, end):
#   delta = end - start
#   int_delta = (delta.days * 24 * 3600) + delta.seconds
#   return start + timedelta(seconds=random.randrange(int_delta))
#
# def random_date():
#   return random_date_between(datetime.now(), datetime.now()+timedelta(days=1))

from baseweb.interface import register_component

register_component("collection.js", os.path.dirname(__file__))

from flask import request
from flask_restful import Resource

from baseweb.rest     import api
from baseweb.security import authenticated

# set up an in-memory collection of random names and provide a resource to
# access them with query arguments, emulating a MongoDB collection

# first_names = [ "John", "Andy", "Joe" ]
# last_names  = [ "Johnson", "Smith", "Williams" ]
# data = [
#   {
#     "id"      : index + 1,
#     "name"    : random.choice(first_names) + " " + random.choice(last_names),
#     "created" : random_date().isoformat(),
#     "updated" : random_date().isoformat()
#   } for index in range(100)
# ]

class Process(Resource):
  @authenticated("app.process.get")
  def get(self):


    #
    # start = int(request.args.get("start", 0))
    # limit = int(request.args.get("limit", 5))
    # sort  = request.args.get("sort", None)
    # order = request.args.get("order", "asc")
    # name  = request.args.get("name", None)
    #
    # selection = data
    # if name:
    #   selection = filter(lambda item: name in item["name"], selection)
    # if sort:
    #   selection = sorted(selection, key=lambda item: item[sort])
    # if order == "desc":
    #   selection.reverse()

    return {
      id: "full",
      sequence: [
        { label: "Generator",        stats: "adcs.intake.generator" },
        { fanout: [ 
          { sequence: [
            { label: "Intake UP",    stats: "adcs.intake.legacy.up"  },
            { label: "Process UP",   stats: "adcs.intake.process.up" }
          ]},
          { sequence: [
            { label: "Intake ADB",   stats: "adcs.intake.legacy.adb"  },
            { label: "Process ADB",  stats: "adcs.intake.process.adb" }
          ]},
          { sequence: [
            { label: "Intake BM",    stats: "adcs.intake.legacy.bm"  },
            { label: "Process BM",   stats: "adcs.intake.process.bm" }
          ]},
          { label: "Intake DAR",     stats: "adcs.intake" }
        ]},
        { label: "Process DAR",      stats: "adcs.intake.process.dar" },
        { label: "Forward UP",       stats: "adcs.intake.forward.up" },
        { label: "UP",               stats: "up" },
        { label: "Receive Feedback", stats: "adcs.intake.feedback" },
        { label: "Process Feedback", stats: "adcs.process.feedback" }
      ]
    }
);


api.add_resource(Process, "/api/process")
