#!/usr/bin/env python3

"""Range Announcer
Author:  Michael J. Swenson

Announce impending range closure near sunset.
"""
import datetime
import json
import logging.handlers
import os
from pathlib import Path
from time import sleep
from range_announcer.switch import Switch
from range_announcer.announcer import Announcer
from range_announcer.sunrise import Sun

#  Delay time constants
TWELVE_HOURS = 43200  # seconds
ONE_HOUR = 3600  # seconds
THIRTY_MINUTES = 1800  # seconds
FIFTEEN_MINUTES = 900  # seconds
TEN_MINUTES = 600  # seconds
FIVE_MINUTES = 300  # seconds
AMP_DELAY = 3  # seconds it takes from power switch on until amp is ready to broadcast

logger = logging.getLogger('range_announcer')
logger.setLevel(logging.DEBUG)
logformat = logging.Formatter('{asctime} {levelname} {message}', style='{')
# file handler for normal logging
fh = logging.FileHandler(filename='Range_Announcer_Log.txt')
fh.setLevel(logging.DEBUG)
fh.setFormatter(logformat)
# email hanlder for severe errors
eh = logging.handlers.SMTPHandler(mailhost='smtp.ipower.com',
                                  fromaddr='RangeAnnouncer@smsclub.org',
                                  toaddrs=['smscadmin@smsclub.org'],
                                  subject='Range Announcer Message',
                                  credentials=('RangeAnnouncer@smsclub.org', 'pdtd5nsySAmhzHRV0lMM'),
                                  secure=None)
eh.setLevel(logging.ERROR)
eh.setFormatter(logformat)
logger.addHandler(fh)
logger.addHandler(eh)


def main():
    # Open the settings file and load the setup_values dictonary from it.
    # Start by setting the current directory to the one in which the script runs.
    os.chdir(Path(__file__).absolute().parent)
    setup_values = None
    try:
        #with open(f'{file_location}/rangeannouncer.json') as setup_file:
        with open('rangeannouncer.json') as setup_file:
            setup_values = json.load(setup_file)
    except FileNotFoundError as fnfe:
        logger.fatal(f'Unable to find setup file. {fnfe}')
        print(f'Unable to find setup file. {fnfe}')
    # initialize the shelly power switch
    shelly = Switch(setup_values)
    # initialize the announcer
    announcer = Announcer()
    # initialize the sunset calculator
    sun = Sun(setup_values)
    logger.info(f'Starting the range announcer program.')

    while True:
        logger.info(f'_________________________________________________________________________________________________')
        # figure out how long until sunset
        dtnow = datetime.datetime.now()
        sunset = sun.sunset()
        dtsunset = datetime.datetime.combine(dtnow.date(), sunset)
        print(f'Sunset today is at {dtsunset}')
        logger.info(f'Sunset today is at {dtsunset}')
        # for testing purposes override the time.
        # now = datetime.datetime.strptime('18:37:41', '%H:%M:%S').time()
        # dtnow = datetime.datetime.combine(dtnow.date(), now)
        if dtnow > dtsunset:
            logger.info(f'Too late to run announcements today.')
        delta = dtsunset - dtnow
        seconds_to_sunset = round(delta.total_seconds())
        print(f'Seconds to sunset: {seconds_to_sunset}')
        if FIVE_MINUTES > seconds_to_sunset > 0:
            logger.info(f'Going to sleep for {seconds_to_sunset} seconds.')
            sleep(seconds_to_sunset)
            logger.info(f'Turning on the power to the amp.')
            shelly.on()
            sleep(AMP_DELAY)
            announcer.announce_message(0)
            shelly.off()
        if seconds_to_sunset > ONE_HOUR:
            sleep(seconds_to_sunset - ONE_HOUR)
            shelly.on()
            sleep(AMP_DELAY)
            announcer.announce_message(60)
            sleep(THIRTY_MINUTES)
            announcer.announce_message(30)
            sleep(FIFTEEN_MINUTES)
            announcer.announce_message(15)
            sleep(TEN_MINUTES)
            announcer.announce_message(5)
            sleep(FIVE_MINUTES)
            announcer.announce_message(0)
            shelly.off()
        if seconds_to_sunset > THIRTY_MINUTES:
            sleep(seconds_to_sunset - THIRTY_MINUTES)
            shelly.on()
            sleep(AMP_DELAY)
            announcer.announce_message(30)
            sleep(FIFTEEN_MINUTES)
            announcer.announce_message(15)
            sleep(TEN_MINUTES)
            announcer.announce_message(5)
            sleep(FIVE_MINUTES)
            announcer.announce_message(0)
            shelly.off()
        if seconds_to_sunset > FIFTEEN_MINUTES:
            sleep(seconds_to_sunset - FIFTEEN_MINUTES)
            shelly.on()
            sleep(AMP_DELAY)
            announcer.announce_message(15)
            sleep(TEN_MINUTES)
            announcer.announce_message(5)
            sleep(FIVE_MINUTES)
            announcer.announce_message(0)
            shelly.off()
        if seconds_to_sunset >= FIVE_MINUTES:
            sleep(seconds_to_sunset - FIVE_MINUTES)
            shelly.on()
            sleep(AMP_DELAY)
            announcer.announce_message(5)
            sleep(FIVE_MINUTES)
            announcer.announce_message(0)
            shelly.off()

        print(f'Going to sleep for 12 hours starting at {datetime.datetime.now()}')
        sleep(TWELVE_HOURS)
    # end while


if __name__ == "__main__":
    main()
