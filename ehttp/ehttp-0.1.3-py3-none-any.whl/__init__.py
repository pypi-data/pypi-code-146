"""Легковесный и предельно простой модуль для приема http запросов и отправления ответов."""
import logging

from .proxy import proxy
from .server import Server
from .file_manager import manage_files
from .classes import File, Request, Response

logging.basicConfig(level=0)
