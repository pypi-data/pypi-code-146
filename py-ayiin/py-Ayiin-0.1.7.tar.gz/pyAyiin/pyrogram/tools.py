# AyiinXd
# Copyright (C) 2022-2023 @AyiinXd
#
# This file is a part of < https://github.com/AyiinXd/AyiinXd >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/AyiinXd/AyiinXd/blob/main/LICENSE/>.
#
# FROM AyiinXd <https://github.com/AyiinXd/AyiinXd>
# t.me/AyiinChat & t.me/AyiinSupport

# ========================×========================
#            Jangan Hapus Credit Ngentod
# ========================×========================

import aiohttp
import asyncio
import importlib
import math
import os
import shlex
import textwrap
from typing import Tuple, Union
from io import BytesIO

from pymediainfo import MediaInfo
from fipper import Client, enums
from fipper.types import Message, User
from PIL import Image, ImageDraw, ImageFont


class Tools(object):
    async def CheckAdmin(
        self,
        client: Client,
        message: Message
    ):
        """Check if we are an admin."""
        admin = enums.ChatMemberStatus.ADMINISTRATOR
        creator = enums.ChatMemberStatus.OWNER
        ranks = [admin, creator]
    
        SELF = await client.get_chat_member(
            chat_id=message.chat.id, user_id=client.me.id
        )
    
        if SELF.status not in ranks:
            await message.reply_text("<i>Maaf Anda Bukan Admin!</i>")
    
        else:
            if SELF.status is admin or SELF.privileges:
                return True
            else:
                await message.reply_text("<i>Anda Tidak Mempunyai Izin Untuk Melakukan Itu</i>")
    
    
    def get_cmd(
        self,
        message: Message
    ):
        msg = message.text
        msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
        split = msg[1:].replace("\n", " \n").split(" ")
        if " ".join(split[1:]).strip() == "":
            return ""
        return " ".join(split[1:])
    
    
    def get_args(
        self,
        message: Message
    ):
        try:
            message = message.text
        except AttributeError:
            pass
        if not message:
            return False
        message = message.split(maxsplit=1)
        if len(message) <= 1:
            return []
        message = message[1]
        try:
            split = shlex.split(message)
        except ValueError:
            return message
        return list(filter(lambda x: len(x) > 0, split))
    
    
    def get_user(
        self,
        message: Message,
        text: str
    ) -> Tuple[int, str, None]:
        """Get User From Message"""
        if text is None:
            asplit = None
        else:
            asplit = text.split(" ", 1)
        user_s = None
        reason_ = None
        if message.reply_to_message:
            user_s = message.reply_to_message.from_user.id
            reason_ = text if text else None
        elif asplit is None:
            return None, None
        elif len(asplit[0]) > 0:
            if message.entities:
                if len(message.entities) == 1:
                    required_entity = message.entities[0]
                    if required_entity.type == "text_mention":
                        user_s = int(required_entity.user.id)
                    else:
                        user_s = int(
                            asplit[0]) if asplit[0].isdigit() else asplit[0]
            else:
                user_s = int(asplit[0]) if asplit[0].isdigit() else asplit[0]
            if len(asplit) == 2:
                reason_ = asplit[1]
        return user_s, reason_
    
    
    def get_text(
        self,
        message: Message
    ) -> Tuple[None, str]:
        """Extract Text From Commands"""
        text_to_return = message.text
        if message.text is None:
            return None
        if " " in text_to_return:
            try:
                return message.text.split(None, 1)[1]
            except IndexError:
                return None
        else:
            return None
    
    
    def media_data(
        self,
        media: str
    ) -> dict:
        "Get downloaded media's information"
        found = False
        media_info = MediaInfo.parse(media)
        for track in media_info.tracks:
            if track.track_type == "Video":
                found = True
                type_ = track.track_type
                format_ = track.format
                duration_1 = track.duration
                other_duration_ = track.other_duration
                duration_2 = (
                    f"{other_duration_[0]} - ({other_duration_[3]})"
                    if other_duration_
                    else None
                )
                pixel_ratio_ = [track.width, track.height]
                aspect_ratio_1 = track.display_aspect_ratio
                other_aspect_ratio_ = track.other_display_aspect_ratio
                aspect_ratio_2 = other_aspect_ratio_[
                    0] if other_aspect_ratio_ else None
                fps_ = track.frame_rate
                fc_ = track.frame_count
                media_size_1 = track.stream_size
                other_media_size_ = track.other_stream_size
                media_size_2 = (
                    [
                        other_media_size_[1],
                        other_media_size_[2],
                        other_media_size_[3],
                        other_media_size_[4],
                    ]
                    if other_media_size_
                    else None
                )

        dict_ = (
            {
                "media_type": type_,
                "format": format_,
                "duration_in_ms": duration_1,
                "duration": duration_2,
                "pixel_sizes": pixel_ratio_,
                "aspect_ratio_in_fraction": aspect_ratio_1,
                "aspect_ratio": aspect_ratio_2,
                "frame_rate": fps_,
                "frame_count": fc_,
                "file_size_in_bytes": media_size_1,
                "file_size": media_size_2,
            }
            if found
            else None
        )
        return dict_
    
    
    def resize_image(self, image):
        im = Image.open(image)
        maxsize = (512, 512)
        if (im.width and im.height) < 512:
            size1 = im.width
            size2 = im.height
            if im.width > im.height:
                scale = 512 / size1
                size1new = 512
                size2new = size2 * scale
            else:
                scale = 512 / size2
                size1new = size1 * scale
                size2new = 512
            size1new = math.floor(size1new)
            size2new = math.floor(size2new)
            sizenew = (size1new, size2new)
            im = im.resize(sizenew)
        else:
            im.thumbnail(maxsize)
        file_name = "Sticker.png"
        im.save(file_name, "PNG")
        if os.path.exists(image):
            os.remove(image)
        return file_name
    
    
    async def resize_media(
        self,
        media: str,
        video: bool,
        fast_forward: bool
    ) -> str:
        if video:
            info_ = self.media_data(media)
            width = info_["pixel_sizes"][0]
            height = info_["pixel_sizes"][1]
            sec = info_["duration_in_ms"]
            s = round(float(sec)) / 1000
    
            if height == width:
                height, width = 512, 512
            elif height > width:
                height, width = 512, -1
            elif width > height:
                height, width = -1, 512
    
            resized_video = f"{media}.webm"
            if fast_forward:
                if s > 3:
                    fract_ = 3 / s
                    ff_f = round(fract_, 2)
                    set_pts_ = ff_f - 0.01 if ff_f > fract_ else ff_f
                    cmd_f = f"-filter:v 'setpts={set_pts_}*PTS',scale={width}:{height}"
                else:
                    cmd_f = f"-filter:v scale={width}:{height}"
            else:
                cmd_f = f"-filter:v scale={width}:{height}"
            fps_ = float(info_["frame_rate"])
            fps_cmd = "-r 30 " if fps_ > 30 else ""
            cmd = f"ffmpeg -i {media} {cmd_f} -ss 00:00:00 -to 00:00:03 -an -c:v libvpx-vp9 {fps_cmd}-fs 256K {resized_video}"
            _, error, __, ___ = await self.run_cmd(cmd)
            os.remove(media)
            return resized_video
    
        image = Image.open(media)
        maxsize = 512
        scale = maxsize / max(image.width, image.height)
        new_size = (int(image.width * scale), int(image.height * scale))
    
        image = image.resize(new_size, Image.LANCZOS)
        resized_photo = "sticker.png"
        image.save(resized_photo)
        os.remove(media)
        return resized_photo
