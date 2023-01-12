import argparse
import datetime
import sys
from cm.configs import settings
import os


def create_parser():
    """ Создать и вернуть парсер для аргументов, передаваемых при запуске
    приложения"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-ar_ip', nargs='?')
    parser.add_argument('-ar_port', nargs='?', default=52250)
    parser.add_argument('-mirrored', nargs='?', default=0)
    parser.add_argument('-scale_server_ip', nargs='?')
    parser.add_argument('-check_doubles', nargs='?', default=0)
    parser.add_argument('-scale_server_port', nargs='?', default=2297)
    parser.add_argument('-fgsm', nargs='?', default=False)
    return parser


def draw_version_on_screen(canvas, xpos, ypos, version_text, font):
    """ Рисует на холсте версию приложения """
    canvas.create_text(xpos, ypos, text=version_text, font=font,
                       fill='grey')


def log_events():
    td = datetime.datetime.today().date()
    path = os.path.join(settings.LOGS_DIR, f'{td}.log')
    log_file = open(path, "w")
    sys.stdout = log_file


def del_logs():
    files = os.listdir(settings.LOGS_DIR)
    for filename in files:
        if filename == '__init__.py' or filename == '__pycache__':
            continue
        date = filename.split('.')[0]
        date = datetime.datetime.strptime(date, '%Y-%m-%d')
        today = datetime.datetime.today().date()
        if date.date() < today - datetime.timedelta(
                days=3):
            os.remove(os.path.join(settings.LOGS_DIR, filename))
