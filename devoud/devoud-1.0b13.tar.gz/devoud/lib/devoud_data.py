from PySide6.QtCore import *
from PySide6 import QtCore
from PySide6.QtCore import Qt, QUrl, QSize
from PySide6.QtGui import *
from PySide6.QtWebEngineCore import *
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import *
from .filesystem import FileSystem
from .styles import Theme
import json
import time

FS = FileSystem()

search_engines = {'Yandex': ('https://yandex.ru/search/?text=', 'https://ya.ru/', './ui/svg/yandex.svg'),
                  'Google': (
                      'https://www.google.com/search?q=', 'https://www.google.com/', './ui/svg/google.svg'),
                  'StartPage': (
                      'https://www.startpage.com/sp/search?query=', 'https://www.startpage.com/?t=dark',
                      './ui/svg/startpage.svg'
                  ),
                  'DDGo': (
                      'https://duckduckgo.com/?q=', 'https://duckduckgo.com/', './ui/svg/duckduckgo.svg')}

new_page_dict = {'Заставка с часами': lambda: 'https://web.tabliss.io/',
                 'Поисковик': lambda: search_engines[FS.get_option('searchEngine')][1],
                 'Домашняя страница': lambda: QUrl.fromUserInput(FS.get_option('homePage')).toString()}

new_page = new_page_dict.get(FS.get_option('newPage'))()
systemFrame = FS.get_option('systemWindowFrame')
