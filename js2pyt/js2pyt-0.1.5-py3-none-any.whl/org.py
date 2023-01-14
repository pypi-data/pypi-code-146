# VideoEncoder - a telegram bot for compressing/encoding videos in h264/h265 format.
# Copyright (c) 2021 WeebTime/VideoEncoder
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import time
from logging.handlers import RotatingFileHandler
from pyrogram import Client
from pyrogram.types import CallbackQuery
from pyrogram import filters, Client, enums
from DK import download_dir, log, owner, sudo_users
from database.access_db import db_two as db
from DK.utils.settings import (AudioSettings, ExtraSettings, OpenSettings,
                              VideoSettings)
from database.add_user import AddUserToDatabase
from DK.utils.helper import check_chat
from DK.utils.tasks import handle_tasks
from DK.utils.helper import check_chat, output
from DK.utils.settings import OpenSettings


from DK.utils.display_progress import TimeFormatter, humanbytes
from DK.utils.helper import check_chat, start_but


from DK.utils.ffmpeg import get_duration, get_thumbnail, get_width_height
from DK.utils.helper import check_chat
from DK.utils.uploads.drive.upload import Uploader
from DK.utils.uploads.telegram import upload_doc, upload_video