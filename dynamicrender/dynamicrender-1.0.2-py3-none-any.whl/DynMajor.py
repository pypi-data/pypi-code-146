import emoji
import asyncio
from loguru import logger
from math import ceil
from os import path
from fontTools.ttLib import TTFont
from dynamicadaptor.Majors import Major
from PIL import Image, ImageDraw, ImageFont

from typing import Optional
from .DynConfig import DynColor, DynFontPath, DynSize
from .Tools import get_pictures


class DynMajorRender:
    def __init__(self, static_path: str, dyn_color: DynColor, dyn_font_path: DynFontPath, dyn_size: DynSize) -> None:
        """Initial configuration

        Parameters
        ----------
        static_path : str
            path to the static file
        dyn_color : DynColor
            color information in the configuration
        dyn_font_path : DynFontPath
            font_path information in the configuration
        dyn_size : DynSize
            size information in the configuration
        """
        self.static_path: str = static_path
        self.dyn_color: DynColor = dyn_color
        self.dyn_font_path: DynFontPath = dyn_font_path
        self.dyn_size: DynSize = dyn_size

    async def run(self, dyn_maojor: Major, dyn_type: Optional[str] = None) -> Optional[Image.Image]:
        """Render the major of the dynamic into image

        Parameters
        ----------
        dyn_text : Head
            The major of the dynamic
        dyn_type : Optional[str]
            F or None

        Returns
        -------
        Optional[Image.Image]
            Rendered image
        """
        try:
            major_type = dyn_maojor.type
            if major_type == "MAJOR_TYPE_DRAW":
                return await DynMajorDraw(dyn_maojor, dyn_type, self.dyn_color).run()
            elif major_type == "MAJOR_TYPE_ARCHIVE":
                return await DynMajorArchive(self.static_path, self.dyn_color, self.dyn_font_path, self.dyn_size).run(
                    dyn_maojor, dyn_type)
            elif major_type == "MAJOR_TYPE_LIVE_RCMD":
                return await DynMajorLiveRcmd(self.static_path, self.dyn_color, self.dyn_font_path, self.dyn_size).run(
                    dyn_maojor, dyn_type)
            elif major_type == "MAJOR_TYPE_ARTICLE":
                return await DynMajorArticle(self.static_path, self.dyn_color, self.dyn_font_path, self.dyn_size).run(
                    dyn_maojor, dyn_type)
            elif major_type == "MAJOR_TYPE_COMMON":
                return await DynMajorCommon(self.static_path, self.dyn_color, self.dyn_font_path, self.dyn_size).run(
                    dyn_maojor, dyn_type)
            elif major_type == "MAJOR_TYPE_MUSIC":
                return await DynMajorMusic(self.static_path, self.dyn_color, self.dyn_font_path, self.dyn_size).run(
                    dyn_maojor, dyn_type)
            elif major_type == "MAJOR_TYPE_PGC":
                return await DynMajorPgc(self.static_path, self.dyn_color, self.dyn_font_path, self.dyn_size).run(
                    dyn_maojor, dyn_type)
            elif major_type == "MAJOR_TYPE_MEDIALIST":
                return await DynMajorMediaList(self.static_path, self.dyn_color, self.dyn_font_path, self.dyn_size).run(
                    dyn_maojor, dyn_type)

            elif major_type == "MAJOR_TYPE_COURSES":
                return await DynMajorCourses(self.static_path, self.dyn_color, self.dyn_font_path, self.dyn_size).run(
                    dyn_maojor, dyn_type)
            elif major_type == "MAJOR_TYPE_LIVE":
                return await DynMajorLive(self.static_path, self.dyn_color, self.dyn_font_path, self.dyn_size).run(
                    dyn_maojor, dyn_type)
            else:
                logger.error("Unknown major type")
                return None
        except Exception as e:
            logger.exception(e)
            return None


class DynMajorDraw:
    def __init__(self, major_draw: Major, dyn_type: str, dyn_color: DynColor) -> None:
        self.major_draw: Major = major_draw
        self.dyn_type = dyn_type
        self.dyn_color = dyn_color
        self.backgroud_img = None
        self.items = None

    async def run(self) -> Optional[Image.Image]:
        """make the image of the draw

        Returns
        -------
        Optional[Image.Image]
            img
        """
        self.items = self.major_draw.draw.items
        item_count = len(self.items)
        backgroud_color = self.dyn_color.dyn_gray if self.dyn_type == "F" else self.dyn_color.dyn_white
        if item_count == 1:
            await self.single_img(backgroud_color)
        elif item_count in {2, 4}:
            await self.dual_img(backgroud_color)
        else:
            await self.triplex_img(backgroud_color)
        return self.backgroud_img

    async def single_img(self, backgroud_color: str):
        src = self.items[0].src
        img_height = self.items[0].height
        img_width = self.items[0].width
        if img_height / img_width > 4:
            img_url = f"{src}@{600}w_{800}h_!header.webp"
        else:
            img_url = src
        img = await get_pictures(img_url)
        if img is not None:
            img_ori_size = img.size
            img = img.resize(
                (1008, int(img_ori_size[1] * 1008 / img_ori_size[0])))
            img_size = img.size
            self.backgroud_img = Image.new(
                "RGBA", (1080, img_size[1] + 20), backgroud_color)
            self.backgroud_img.paste(img, (36, 10), img)

    async def dual_img(self, backgroud_color: str):
        url_list = []
        for item in self.items:
            src = item.src
            img_height = item.height
            img_width = item.width
            if img_height / img_width > 3:
                url_list.append(f"{src}@520w_520h_!header.webp")
            else:
                url_list.append(f"{src}@520w_520h_1e_1c.webp")
        imgs = await get_pictures(url_list, 520)
        num = len(url_list) / 2
        back_size = int(num * 520 + 20 * num)
        self.backgroud_img = Image.new(
            "RGBA", (1080, back_size), backgroud_color)
        x, y = 15, 10
        for i in imgs:
            if i is not None:
                self.backgroud_img.paste(i, (x, y), i)
            x += 530
            if x > 1000:
                x = 15
                y += 530

    async def triplex_img(self, backgroud_color: str):
        url_list = []
        for item in self.items:
            src = item.src
            img_height = item.height
            img_width = item.width
            if img_height / img_width > 3:
                url_list.append(f"{src}@260w_260h_!header.webp")
            else:
                url_list.append(f"{src}@260w_260h_1e_1c.webp")
        num = ceil(len(self.items) / 3)
        imgs = await get_pictures(url_list, 346)
        back_size = int(num * 346 + 20 * num)
        self.backgroud_img = Image.new(
            "RGBA", (1080, back_size), backgroud_color)
        x, y = 11, 10
        for img in imgs:
            if img is not None:
                self.backgroud_img.paste(img, (x, y), img)
            x += 356
            if x > 1000:
                x = 11
                y += 356


class DynMajorArchive:

    def __init__(self, static_path: str, dyn_color: DynColor, dyn_font_path: DynFontPath, dyn_size: DynSize) -> None:
        """Initial configuration

        Parameters
        ----------
        static_path : str
            path to the static file
        dyn_color : DynColor
            color information in the configuration
        dyn_font_path : DynFontPath
            font_path information in the configuration
        dyn_size : DynSize
            size information in the configuration
        """
        self.static_path: str = static_path
        self.dyn_color: DynColor = dyn_color
        self.dyn_font_path: DynFontPath = dyn_font_path
        self.dyn_size: DynSize = dyn_size
        self.background_img = None
        self.background_color = None
        self.text_font = None
        self.extra_font = None
        self.emoji_font = None
        self.key_map = None
        self.src_path = None

    async def run(self, dyn_maojor: Major, dyn_type) -> Optional[Image.Image]:
        self.background_color = self.dyn_color.dyn_gray if dyn_type == "F" else self.dyn_color.dyn_white
        self.background_img = Image.new("RGB", (1080, 695), self.background_color)
        self.draw = ImageDraw.Draw(self.background_img)
        self.text_font = ImageFont.truetype(self.dyn_font_path.text, self.dyn_size.text)
        self.extra_font = ImageFont.truetype(self.dyn_font_path.extra_text, self.dyn_size.text)
        self.emoji_font = ImageFont.truetype(self.dyn_font_path.emoji, self.dyn_size.emoji)
        self.key_map = TTFont(self.dyn_font_path.text, fontNumber=0)['cmap'].tables[0].ttFont.getBestCmap().keys()
        self.src_path = path.join(self.static_path, "Src")
        cover = f"{dyn_maojor.archive.cover}@505w_285h_1c.webp"
        title = dyn_maojor.archive.title
        duration = dyn_maojor.archive.duration_text
        badge = dyn_maojor.archive.badge
        try:
            await asyncio.gather(
                self.make_cover(cover, duration, badge),
                self.make_title(title)
            )
            self.background_img = self.background_img.convert("RGBA")
            return self.background_img
        except Exception as e:
            logger.exception("error")
            return None

    async def make_cover(self, cover: str, duration: str, badge):
        cover = await get_pictures(cover, (1010, 570))
        self.background_img.paste(cover, (35, 25), cover)
        play_icon = Image.open(path.join(self.src_path, "tv.png")).convert("RGBA").resize((130, 130))
        font = ImageFont.truetype(self.dyn_font_path.text, self.dyn_size.sub_title)

        duration_size = font.getsize(duration)
        duration_pic_size = (duration_size[0] + 20, duration_size[1] + 20)
        duration_pic = Image.new("RGBA", duration_pic_size, (0, 0, 0, 90))
        draw = ImageDraw.Draw(duration_pic)
        draw.text((10, 5), duration, fill=self.dyn_color.dyn_white, font=font)
        self.background_img.paste(duration_pic, (80, 525), duration_pic)
        self.background_img.paste(play_icon, (905, 455), play_icon)
        if badge != None:
            badge_text = badge.text
            bg_color = badge.bg_color
        else:
            badge_text = "投稿视频"
            bg_color = self.dyn_color.dyn_pink
        badge_size = font.getsize(duration)
        badge_pic_size = (badge_size[0] + 50, badge_size[1] + 20)
        badge_pic = Image.new("RGBA", badge_pic_size, bg_color)
        draw = ImageDraw.Draw(badge_pic)
        draw.text((10, 5), badge_text, self.dyn_color.dyn_white, font=font)
        self.background_img.paste(badge_pic, (905, 50), badge_pic)

    async def make_title(self, title):
        emoji = await self.get_emoji(title)
        offset = 0
        position = 35
        total = len(title) - 1
        while offset <= total:
            if offset in emoji:
                emoji_img = emoji[offset]["emoji"]
                self.background_img.paste(emoji_img, (int(position), 606), emoji_img)
                position += (emoji_img.size[0])
                offset = emoji[offset]["match_end"]
                if position >= 1020:
                    self.draw.text((int(position), 600), "...", fill=self.dyn_color.dyn_black, font=self.text_font)
                    break
            else:
                text = title[offset]
                if ord(text) not in self.key_map:
                    self.draw.text((int(position), 600), text, fill=self.dyn_color.dyn_black, font=self.extra_font)
                    next_offset = self.extra_font.getbbox(text)[2]
                else:
                    self.draw.text((int(position), 600), text, fill=self.dyn_color.dyn_black, font=self.text_font)
                    next_offset = self.text_font.getbbox(text)[2]
                position += next_offset
                offset += 1
                if position >= 1020:
                    self.draw.text((int(position), 600), "...", fill=self.dyn_color.dyn_black, font=self.text_font)
                    break

    async def get_emoji(self, title):
        result = emoji.emoji_list(title)
        duplicate_removal_result = {i["emoji"] for i in result}
        emoji_dic = {}
        for i in duplicate_removal_result:
            emoji_origin_text = self.emoji_font.getbbox(i)
            emoji_img = Image.new(
                "RGBA", (emoji_origin_text[2], emoji_origin_text[3]), self.background_color)
            draw = ImageDraw.Draw(emoji_img)
            draw.text((0, 0), i, embedded_color=True, font=self.emoji_font)
            emoji_img = emoji_img.resize((self.dyn_size.text, self.dyn_size.text))
            emoji_dic[i] = emoji_img
        temp = {}
        for i in result:
            temp[i["match_start"]] = i
            temp[i["match_start"]]["emoji"] = emoji_dic[temp[i["match_start"]]["emoji"]]
        return temp


class DynMajorLiveRcmd:
    def __init__(self, static_path: str, dyn_color: DynColor, dyn_font_path: DynFontPath, dyn_size: DynSize) -> None:
        """Initial configuration

        Parameters
        ----------
        static_path : str
            path to the static file
        dyn_color : DynColor
            color information in the configuration
        dyn_font_path : DynFontPath
            font_path information in the configuration
        dyn_size : DynSize
            size information in the configuration
        """
        self.static_path: str = static_path
        self.dyn_color: DynColor = dyn_color
        self.dyn_font_path: DynFontPath = dyn_font_path
        self.dyn_size: DynSize = dyn_size
        self.background_img = None
        self.background_color = None
        self.text_font = None
        self.extra_font = None
        self.emoji_font = None
        self.key_map = None
        self.src_path = None

    async def run(self, dyn_maojor: Major, dyn_type) -> Optional[Image.Image]:
        self.background_color = self.dyn_color.dyn_gray if dyn_type == "F" else self.dyn_color.dyn_white
        self.background_img = Image.new("RGB", (1080, 695), self.background_color)
        self.draw = ImageDraw.Draw(self.background_img)
        self.text_font = ImageFont.truetype(self.dyn_font_path.text, self.dyn_size.text)
        self.extra_font = ImageFont.truetype(self.dyn_font_path.extra_text, self.dyn_size.text)
        self.emoji_font = ImageFont.truetype(self.dyn_font_path.emoji, self.dyn_size.emoji)
        self.key_map = TTFont(self.dyn_font_path.text, fontNumber=0)['cmap'].tables[0].ttFont.getBestCmap().keys()
        self.src_path = path.join(self.static_path, "Src")

        cover = f"{dyn_maojor.live_rcmd.content.live_play_info.cover}@505w_285h_1c.webp"
        title = dyn_maojor.live_rcmd.content.live_play_info.title
        watch_show = dyn_maojor.live_rcmd.content.live_play_info.watched_show.text_large
        badge = "直播中"
        try:
            await asyncio.gather(
                self.make_cover(cover, watch_show, badge),
                self.make_title(title)
            )
            self.background_img = self.background_img.convert("RGBA")
            return self.background_img
        except Exception as e:
            logger.exception("error")
            return None

    async def make_cover(self, cover: str, watch_show: str, badge: str):
        cover = await get_pictures(cover, (1010, 570))
        self.background_img.paste(cover, (35, 25), cover)
        font = ImageFont.truetype(self.dyn_font_path.text, self.dyn_size.sub_title)

        watch_show_size = font.getsize(watch_show)
        watch_show_pic_size = (watch_show_size[0] + 20, watch_show_size[1] + 10)
        watch_show_pic = Image.new("RGBA", watch_show_pic_size, (0, 0, 0, 90))
        draw = ImageDraw.Draw(watch_show_pic)
        draw.text((10, 3), watch_show, fill=self.dyn_color.dyn_white, font=font)
        badge_text = badge
        bg_color = self.dyn_color.dyn_pink
        badge_size = font.getsize(badge)
        badge_pic_size = (badge_size[0] + 20, badge_size[1] + 10)
        badge_pic = Image.new("RGBA", badge_pic_size, bg_color)
        draw = ImageDraw.Draw(badge_pic)
        draw.text((10, 3), badge_text, self.dyn_color.dyn_white, font=font)
        self.background_img.paste(badge_pic, (905, 50), badge_pic)
        self.background_img.paste(watch_show_pic, (885 - watch_show_size[0], 50), watch_show_pic)

    async def make_title(self, title):
        emoji = await self.get_emoji(title)
        offset = 0
        position = 35
        total = len(title) - 1
        while offset <= total:
            if offset in emoji:
                emoji_img = emoji[offset]["emoji"]
                self.background_img.paste(emoji_img, (int(position), 606), emoji_img)
                position += (emoji_img.size[0] - 15)
                offset = emoji[offset]["match_end"]
                if position >= 1020:
                    self.draw.text((int(position), 600), "...", fill=self.dyn_color.dyn_black, font=self.text_font)
                    break
            else:
                text = title[offset]
                if ord(text) not in self.key_map:
                    self.draw.text((int(position), 600), text, fill=self.dyn_color.dyn_black, font=self.extra_font)
                    next_offset = self.extra_font.getbbox(text)[2]
                else:
                    self.draw.text((int(position), 600), text, fill=self.dyn_color.dyn_black, font=self.text_font)
                    next_offset = self.text_font.getbbox(text)[2]
                position += next_offset
                offset += 1
                if position >= 1020:
                    self.draw.text((int(position), 600), "...", fill=self.dyn_color.dyn_black, font=self.text_font)
                    break

    async def get_emoji(self, title):
        result = emoji.emoji_list(title)
        duplicate_removal_result = {i["emoji"] for i in result}
        emoji_dic = {}
        for i in duplicate_removal_result:
            emoji_origin_text = self.emoji_font.getbbox(i)
            emoji_img = Image.new(
                "RGBA", (emoji_origin_text[2], emoji_origin_text[3]), self.background_color)
            draw = ImageDraw.Draw(emoji_img)
            draw.text((0, 0), i, embedded_color=True, font=self.emoji_font)
            emoji_img = emoji_img.resize((self.dyn_size.text, self.dyn_size.text))
            emoji_dic[i] = emoji_img
        temp = {}
        for i in result:
            temp[i["match_start"]] = i
            temp[i["match_start"]]["emoji"] = emoji_dic[temp[i["match_start"]]["emoji"]]
        return temp


class DynMajorArticle:
    def __init__(self, static_path: str, dyn_color: DynColor, dyn_font_path: DynFontPath, dyn_size: DynSize) -> None:
        """Initial configuration

        Parameters
        ----------
        static_path : str
            path to the static file
        dyn_color : DynColor
            color information in the configuration
        dyn_font_path : DynFontPath
            font_path information in the configuration
        dyn_size : DynSize
            size information in the configuration
        """
        self.static_path: str = static_path
        self.dyn_color: DynColor = dyn_color
        self.dyn_font_path: DynFontPath = dyn_font_path
        self.dyn_size: DynSize = dyn_size
        self.background_img = None
        self.background_color = None
        self.inner_color = None
        self.offset = None

    async def run(self, dyn_maojor: Major, dyn_type) -> Optional[Image.Image]:
        try:
            self.background_color = self.dyn_color.dyn_gray if dyn_type == "F" else self.dyn_color.dyn_white
            self.inner_color = self.dyn_color.dyn_gray if dyn_type != "F" else self.dyn_color.dyn_white
            self.background_img = Image.new("RGBA", (1080, 640), self.background_color)

            self.draw = ImageDraw.ImageDraw(self.background_img)
            self.draw.rectangle(((35, 20), (1045, 620)), fill=self.inner_color, outline='#e5e9ef', width=2)
            cover = dyn_maojor.article.cover
            self.offset = True if len(cover) == 1 else False
            tasks = [self.make_cover(cover),
                     self.make_title(dyn_maojor.article.title),
                     self.make_desc(dyn_maojor.article.desc, dyn_maojor.article.label)]
            await asyncio.gather(*tasks)

            return self.background_img
        except Exception as e:
            logger.exception("error")
            return None

    async def make_cover(self, covers):
        if len(covers) == 1:
            cover_url = f"{covers[0]}@647w_150h_1c.webp"
            cover_img = await get_pictures(cover_url, (1010, 300))
            if cover_img:
                self.background_img.paste(cover_img, (35, 20), cover_img)
        else:
            cover_url = [f"{i}@360w_360h_1c" for i in covers]
            cover_imgs = await get_pictures(cover_url, (330, 330))
            if cover_imgs:
                for i, j in enumerate(cover_imgs):
                    self.background_img.paste(j, (35 + i * 340, 20), j)

    async def make_title(self, title):
        x_position = 45
        y = 330 if self.offset else 360
        font = ImageFont.truetype(self.dyn_font_path.text, self.dyn_size.uname)
        for i in title:
            self.draw.text((x_position, y), i, fill=self.dyn_color.dyn_black, font=font)
            next_offset = font.getbbox(i)[2]
            x_position += next_offset
            if x_position >= 980:
                self.draw.text((x_position, y), "...", fill=self.dyn_color.dyn_black, font=font)
                break

    async def make_desc(self, desc, lable):
        x_position = 65
        y = 360 + self.dyn_size.uname if self.offset else 390 + self.dyn_size.uname
        font = ImageFont.truetype(self.dyn_font_path.text, self.dyn_size.title)
        y_constrain = 560 - self.dyn_size.sub_text
        for i in desc:
            self.draw.text((x_position, y), i, fill=self.dyn_color.dyn_silver_gray, font=font)
            next_offset = font.getbbox(i)
            x_position += next_offset[2]
            x_temp = x_position
            if x_position >= 990:
                x_position = 45
                y += int(next_offset[3] * 1.5)
                if y >= y_constrain:
                    self.draw.text((x_temp, y - int(next_offset[3] * 1.3)), "...", fill=self.dyn_color.dyn_silver_gray,
                                   font=font)
                    break
        lable_size = font.getbbox(lable)
        x_position = 920 - lable_size[3]
        self.draw.text((x_position, y_constrain + lable_size[3]), f">{lable}", fill=self.dyn_color.dyn_blue, font=font)


class DynMajorCommon:
    def __init__(self, static_path: str, dyn_color: DynColor, dyn_font_path: DynFontPath, dyn_size: DynSize) -> None:
        """Initial configuration

        Parameters
        ----------
        static_path : str
            path to the static file
        dyn_color : DynColor
            color information in the configuration
        dyn_font_path : DynFontPath
            font_path information in the configuration
        dyn_size : DynSize
            size information in the configuration
        """
        self.static_path: str = static_path
        self.dyn_color: DynColor = dyn_color
        self.dyn_font_path: DynFontPath = dyn_font_path
        self.dyn_size: DynSize = dyn_size
        self.background_img = None
        self.background_color = None
        self.inner_color = None
        self.draw = None

    async def run(self, dyn_maojor: Major, dyn_type) -> Optional[Image.Image]:
        try:
            self.background_color = self.dyn_color.dyn_gray if dyn_type == "F" else self.dyn_color.dyn_white
            self.inner_color = self.dyn_color.dyn_gray if dyn_type != "F" else self.dyn_color.dyn_white
            self.background_img = Image.new("RGB", (1080, 285), self.background_color)
            self.draw = ImageDraw.ImageDraw(self.background_img)
            self.draw.rectangle(((35, 20), (1045, 265)), fill=self.inner_color, outline='#e5e9ef', width=2)
            await asyncio.gather(
                self.make_cover(dyn_maojor.common.cover),
                self.make_title(dyn_maojor.common.title, dyn_maojor.common.desc),
                self.make_badge(dyn_maojor)
            )
            self.background_img = self.background_img.convert("RGBA")
            return self.background_img
        except Exception as e:
            logger.exception("error")
            return None

    async def make_cover(self, cover):
        cover_url = f"{cover}@245w_245h_1c.webp"
        cover_img = await get_pictures(cover_url, 245)
        self.background_img.paste(cover_img, (35, 20), cover_img)

    async def make_title(self, title, sub_title):
        title_size = self.dyn_size.text
        sub_title_size = self.dyn_size.sub_text
        title_font = ImageFont.truetype(self.dyn_font_path.text, title_size)
        sub_title_font = ImageFont.truetype(self.dyn_font_path.text, sub_title_size)
        x = 310
        for i in title:
            self.draw.text((x, 85), i, fill=self.dyn_color.dyn_black, font=title_font)
            x += title_font.getbbox(i)[2]
            if x >= 950:
                self.draw.text((x, 85), "...", fill=self.dyn_color.dyn_black, font=title_font)
                break
        x = 310
        for i in sub_title:
            self.draw.text((x, 170), i, fill=self.dyn_color.dyn_silver_gray, font=sub_title_font)
            x += sub_title_font.getbbox(i)[2]
            if x >= 970:
                self.draw.text((x, 170), "...", fill=self.dyn_color.dyn_silver_gray, font=title_font)
                break

    async def make_badge(self, dyn_maojor: Major):
        if dyn_maojor.common.badge and dyn_maojor.common.badge.text:
            text = dyn_maojor.common.badge.text
            text_color = dyn_maojor.common.badge.color
            bg_color = dyn_maojor.common.badge.bg_color
            font = ImageFont.truetype(self.dyn_font_path.text, self.dyn_size.sub_title)
            badge_size = font.getsize(text)
            badge_pic_size = (badge_size[0] + 20, badge_size[1] + 10)
            badge_pic = Image.new("RGBA", badge_pic_size, bg_color)
            draw = ImageDraw.Draw(badge_pic)
            draw.text((10, 3), text, text_color, font=font)
            self.background_img.paste(badge_pic, (945, 40), badge_pic)


class DynMajorMusic:
    def __init__(self, static_path: str, dyn_color: DynColor, dyn_font_path: DynFontPath, dyn_size: DynSize) -> None:
        """Initial configuration

        Parameters
        ----------
        static_path : str
            path to the static file
        dyn_color : DynColor
            color information in the configuration
        dyn_font_path : DynFontPath
            font_path information in the configuration
        dyn_size : DynSize
            size information in the configuration
        """
        self.static_path: str = static_path
        self.dyn_color: DynColor = dyn_color
        self.dyn_font_path: DynFontPath = dyn_font_path
        self.dyn_size: DynSize = dyn_size
        self.background_img = None
        self.background_color = None
        self.inner_color = None
        self.draw = None

    async def run(self, dyn_maojor: Major, dyn_type) -> Optional[Image.Image]:
        try:
            self.background_color = self.dyn_color.dyn_gray if dyn_type == "F" else self.dyn_color.dyn_white
            self.inner_color = self.dyn_color.dyn_gray if dyn_type != "F" else self.dyn_color.dyn_white
            self.background_img = Image.new("RGBA", (1080, 210), self.background_color)
            self.draw = ImageDraw.ImageDraw(self.background_img)
            self.draw.rectangle(((35, 10), (1045, 200)), fill=self.inner_color, outline='#e5e9ef', width=2)
            await asyncio.gather(
                self.make_cover(dyn_maojor.music.cover),
                self.make_title(dyn_maojor.music.title),
                self.make_lable(dyn_maojor.music.label)
            )

            return self.background_img
        except Exception as e:
            logger.exception("error")
            return None

    async def make_cover(self, cover):
        cover_url = f"{cover}@190w_190h_1c.webp"
        cover_img = await get_pictures(cover_url, 190)
        self.background_img.paste(cover_img, (35, 10), cover_img)

    async def make_title(self, title):
        font = ImageFont.truetype(self.dyn_font_path.text, self.dyn_size.sub_text)
        x = 280
        for i in title:
            self.draw.text((x, 45), i, fill=self.dyn_color.dyn_black, font=font)
            text_size = font.getbbox(i)
            x += text_size[2]
            if x >= 1020:
                self.draw.text((x, 55), "...", fill=self.dyn_color.dyn_black, font=font)
                break

    async def make_lable(self, lable):
        font = ImageFont.truetype(self.dyn_font_path.text, self.dyn_size.title)
        self.draw.text((280, 115), lable, fill=self.dyn_color.dyn_silver_gray, font=font)


class DynMajorPgc:
    def __init__(self, static_path: str, dyn_color: DynColor, dyn_font_path: DynFontPath, dyn_size: DynSize) -> None:
        """Initial configuration

        Parameters
        ----------
        static_path : str
            path to the static file
        dyn_color : DynColor
            color information in the configuration
        dyn_font_path : DynFontPath
            font_path information in the configuration
        dyn_size : DynSize
            size information in the configuration
        """
        self.static_path: str = static_path
        self.dyn_color: DynColor = dyn_color
        self.dyn_font_path: DynFontPath = dyn_font_path
        self.dyn_size: DynSize = dyn_size
        self.background_img = None
        self.background_color = None
        self.text_font = None
        self.extra_font = None
        self.key_map = None
        self.src_path = None

    async def run(self, dyn_maojor: Major, dyn_type) -> Optional[Image.Image]:
        self.background_color = self.dyn_color.dyn_gray if dyn_type == "F" else self.dyn_color.dyn_white
        self.background_img = Image.new("RGB", (1080, 695), self.background_color)
        self.draw = ImageDraw.Draw(self.background_img)
        self.text_font = ImageFont.truetype(self.dyn_font_path.text, self.dyn_size.text)
        self.extra_font = ImageFont.truetype(self.dyn_font_path.extra_text, self.dyn_size.text)
        self.key_map = TTFont(self.dyn_font_path.text, fontNumber=0)['cmap'].tables[0].ttFont.getBestCmap().keys()
        self.src_path = path.join(self.static_path, "Src")
        cover = f"{dyn_maojor.pgc.cover}@505w_285h_1c.webp"
        title = dyn_maojor.pgc.title
        play = dyn_maojor.pgc.stat.play
        badge = dyn_maojor.pgc.badge
        try:
            await asyncio.gather(
                self.make_cover(cover),
                self.make_title(title),
            )
            await self.make_badge(play, badge)
            self.background_img = self.background_img.convert("RGBA")
            return self.background_img
        except Exception as e:
            logger.exception("error")
            return None

    async def make_cover(self, cover: str):
        cover = await get_pictures(cover, (1010, 570))
        self.background_img.paste(cover, (35, 25), cover)
        play_icon = Image.open(path.join(self.src_path, "tv.png")).convert("RGBA").resize((130, 130))
        self.background_img.paste(play_icon, (905, 455), play_icon)

    async def make_title(self, title):
        offset = 0
        position = 35
        total = len(title) - 1
        while offset <= total:
            text = title[offset]
            if ord(text) not in self.key_map:
                self.draw.text((int(position), 600), text, fill=self.dyn_color.dyn_black, font=self.extra_font)
                next_offset = self.extra_font.getbbox(text)[2]
            else:
                self.draw.text((int(position), 600), text, fill=self.dyn_color.dyn_black, font=self.text_font)
                next_offset = self.text_font.getbbox(text)[2]
            position += next_offset
            offset += 1
            if position >= 1020:
                self.draw.text((int(position), 600), "...", fill=self.dyn_color.dyn_black, font=self.text_font)
                break

    async def make_badge(self, play, badge):
        font = ImageFont.truetype(self.dyn_font_path.text, self.dyn_size.sub_title)
        if badge != None:
            badge_text = badge.text
            bg_color = badge.bg_color
        else:
            badge_text = "投稿视频"
            bg_color = self.dyn_color.dyn_pink
        badge_size = font.getsize(badge_text)
        badge_pic_size = (badge_size[0] + 20, badge_size[1] + 10)
        badge_pic = Image.new("RGBA", badge_pic_size, bg_color)
        draw = ImageDraw.Draw(badge_pic)
        draw.text((10, 3), badge_text, self.dyn_color.dyn_white, font=font)
        self.background_img.paste(badge_pic, (955, 50), badge_pic)
        play_size = font.getsize(play)
        play_pic_size = (play_size[0] + 20, badge_size[1] + 10)
        play_pic = Image.new("RGBA", play_pic_size, (0, 0, 0, 90))
        draw = ImageDraw.Draw(play_pic)
        draw.text((10, 3), play, fill=self.dyn_color.dyn_white, font=font)
        self.background_img.paste(play_pic, (955 - play_pic.getbbox()[2], 50), play_pic)


class DynMajorMediaList:
    def __init__(self, static_path: str, dyn_color: DynColor, dyn_font_path: DynFontPath, dyn_size: DynSize) -> None:
        """Initial configuration

        Parameters
        ----------
        static_path : str
            path to the static file
        dyn_color : DynColor
            color information in the configuration
        dyn_font_path : DynFontPath
            font_path information in the configuration
        dyn_size : DynSize
            size information in the configuration
        """
        self.static_path: str = static_path
        self.dyn_color: DynColor = dyn_color
        self.dyn_font_path: DynFontPath = dyn_font_path
        self.dyn_size: DynSize = dyn_size
        self.background_img = None
        self.background_color = None
        self.text_font = None
        self.extra_font = None
        self.key_map = None
        self.src_path = None

    async def run(self, dyn_maojor: Major, dyn_type) -> Optional[Image.Image]:
        background_color = self.dyn_color.dyn_gray if dyn_type == "F" else self.dyn_color.dyn_white
        inner_color = self.dyn_color.dyn_gray if dyn_type != "F" else self.dyn_color.dyn_white
        self.background_img = Image.new("RGB", (1080, 300), background_color)
        self.draw = ImageDraw.Draw(self.background_img)
        self.text_font = ImageFont.truetype(self.dyn_font_path.text, self.dyn_size.sub_text)
        self.extra_font = ImageFont.truetype(self.dyn_font_path.extra_text, self.dyn_size.sub_text)
        self.key_map = TTFont(self.dyn_font_path.text, fontNumber=0)['cmap'].tables[0].ttFont.getBestCmap().keys()
        self.src_path = path.join(self.static_path, "Src")
        self.draw.rectangle(((35, 15), (1045, 285)), fill=inner_color, outline='#e5e9ef', width=2)

        cover = f"{dyn_maojor.medialist.cover}@435w_270h_1c.webp"
        title = dyn_maojor.medialist.title
        sub_title = dyn_maojor.medialist.sub_title
        badge = dyn_maojor.medialist.badge

        try:
            await asyncio.gather(
                self.make_cover(cover),
                self.make_title(title),
            )
            await self.make_badge(sub_title, badge)
            self.background_img = self.background_img.convert("RGBA")
            return self.background_img
        except Exception as e:
            logger.exception("error")
            return None

    async def make_cover(self, cover: str):
        cover = await get_pictures(cover, (435, 270))
        self.background_img.paste(cover, (35, 15), cover)

    async def make_title(self, title):
        x = 500
        y = 55
        for i in title:
            if ord(i) not in self.key_map:
                self.draw.text((x, y), i, fill=self.dyn_color.dyn_black, font=self.extra_font)
                x += self.extra_font.getbbox(i)[2]
            else:
                self.draw.text((x, y), i, fill=self.dyn_color.dyn_black, font=self.text_font)
                x += self.text_font.getbbox(i)[2]
            if x >= 1000:
                y += int(self.dyn_size.sub_text * 1.5)
                x = 500
                if y >= 120:
                    break

    async def make_badge(self, sub_title, badge):
        font = ImageFont.truetype(self.dyn_font_path.text, self.dyn_size.sub_title)
        badge_text = badge.text
        bg_color = badge.bg_color
        badge_size = font.getsize(badge_text)
        badge_pic_size = (badge_size[0] + 20, badge_size[1] + 10)
        badge_pic = Image.new("RGBA", badge_pic_size, bg_color)
        draw = ImageDraw.Draw(badge_pic)
        draw.text((10, 3), badge_text, self.dyn_color.dyn_white, font=font)
        self.background_img.paste(badge_pic, (940, 35), badge_pic)
        font = ImageFont.truetype(self.dyn_font_path.text, self.dyn_size.title)
        self.draw.text((500, 210), sub_title, fill=self.dyn_color.dyn_silver_gray, font=font)


class DynMajorCourses:
    def __init__(self, static_path: str, dyn_color: DynColor, dyn_font_path: DynFontPath, dyn_size: DynSize) -> None:
        """Initial configuration

        Parameters
        ----------
        static_path : str
            path to the static file
        dyn_color : DynColor
            color information in the configuration
        dyn_font_path : DynFontPath
            font_path information in the configuration
        dyn_size : DynSize
            size information in the configuration
        """
        self.static_path: str = static_path
        self.dyn_color: DynColor = dyn_color
        self.dyn_font_path: DynFontPath = dyn_font_path
        self.dyn_size: DynSize = dyn_size
        self.background_img = None
        self.background_color = None
        self.text_font = None
        self.extra_font = None
        self.key_map = None
        self.src_path = None

    async def run(self, dyn_maojor: Major, dyn_type) -> Optional[Image.Image]:
        self.background_color = self.dyn_color.dyn_gray if dyn_type == "F" else self.dyn_color.dyn_white
        self.background_img = Image.new("RGB", (1080, 695), self.background_color)
        self.draw = ImageDraw.Draw(self.background_img)
        self.text_font = ImageFont.truetype(self.dyn_font_path.text, self.dyn_size.text)
        self.extra_font = ImageFont.truetype(self.dyn_font_path.extra_text, self.dyn_size.text)
        self.emoji_font = ImageFont.truetype(self.dyn_font_path.emoji, self.dyn_size.emoji)
        self.key_map = TTFont(self.dyn_font_path.text, fontNumber=0)['cmap'].tables[0].ttFont.getBestCmap().keys()
        self.src_path = path.join(self.static_path, "Src")
        cover = f"{dyn_maojor.courses.cover}@505w_285h_1c.webp"
        title = dyn_maojor.courses.title
        sub_title = dyn_maojor.courses.sub_title
        badge = dyn_maojor.courses.badge
        try:
            await asyncio.gather(
                self.make_cover(cover, badge, sub_title),
                self.make_title(title)
            )
            print(dyn_maojor.courses)
            self.background_img = self.background_img.convert("RGBA")
            return self.background_img
        except Exception as e:
            logger.exception("error")
            return None

    async def make_cover(self, cover: str, badge, sub_title):
        cover = await get_pictures(cover, (1010, 570))
        self.background_img.paste(cover, (35, 25), cover)
        play_icon = Image.open(path.join(self.src_path, "tv.png")).convert("RGBA").resize((130, 130))
        font = ImageFont.truetype(self.dyn_font_path.text, self.dyn_size.sub_title)
        self.background_img.paste(play_icon, (905, 455), play_icon)
        if badge != None:
            badge_text = badge.text
            bg_color = badge.bg_color
        else:
            badge_text = "投稿视频"
            bg_color = self.dyn_color.dyn_pink
        badge_size = font.getsize(badge_text)
        badge_pic_size = (badge_size[0] + 20, badge_size[1] + 10)
        badge_pic = Image.new("RGBA", badge_pic_size, bg_color)
        draw = ImageDraw.Draw(badge_pic)
        draw.text((10, 3), badge_text, self.dyn_color.dyn_white, font=font)
        self.background_img.paste(badge_pic, (925, 50), badge_pic)
        sub_title_size = font.getsize(sub_title)
        sub_title_pic_size = (sub_title_size[0] + 20, sub_title_size[1] + 10)
        sub_title_pic = Image.new("RGBA", sub_title_pic_size, (0, 0, 0, 90))
        draw = ImageDraw.Draw(sub_title_pic)
        draw.text((10, 3), sub_title, fill=self.dyn_color.dyn_white, font=font)
        self.background_img.paste(sub_title_pic, (80, 525), sub_title_pic)

    async def make_title(self, title):
        emoji = await self.get_emoji(title)
        offset = 0
        position = 35
        total = len(title) - 1
        while offset <= total:
            if offset in emoji:
                emoji_img = emoji[offset]["emoji"]
                self.background_img.paste(emoji_img, (int(position), 606), emoji_img)
                position += (emoji_img.size[0])
                offset = emoji[offset]["match_end"]
                if position >= 1020:
                    self.draw.text((int(position), 600), "...", fill=self.dyn_color.dyn_black, font=self.text_font)
                    break
            else:
                text = title[offset]
                if ord(text) not in self.key_map:
                    self.draw.text((int(position), 600), text, fill=self.dyn_color.dyn_black, font=self.extra_font)
                    next_offset = self.extra_font.getbbox(text)[2]
                else:
                    self.draw.text((int(position), 600), text, fill=self.dyn_color.dyn_black, font=self.text_font)
                    next_offset = self.text_font.getbbox(text)[2]
                position += next_offset
                offset += 1
                if position >= 1020:
                    self.draw.text((int(position), 600), "...", fill=self.dyn_color.dyn_black, font=self.text_font)
                    break

    async def get_emoji(self, title):
        result = emoji.emoji_list(title)
        duplicate_removal_result = {i["emoji"] for i in result}
        emoji_dic = {}
        for i in duplicate_removal_result:
            emoji_origin_text = self.emoji_font.getbbox(i)
            emoji_img = Image.new(
                "RGBA", (emoji_origin_text[2], emoji_origin_text[3]), self.background_color)
            draw = ImageDraw.Draw(emoji_img)
            draw.text((0, 0), i, embedded_color=True, font=self.emoji_font)
            emoji_img = emoji_img.resize((self.dyn_size.text, self.dyn_size.text))
            emoji_dic[i] = emoji_img
        temp = {}
        for i in result:
            temp[i["match_start"]] = i
            temp[i["match_start"]]["emoji"] = emoji_dic[temp[i["match_start"]]["emoji"]]
        return temp


class DynMajorLive:
    def __init__(self, static_path: str, dyn_color: DynColor, dyn_font_path: DynFontPath, dyn_size: DynSize) -> None:
        """Initial configuration

        Parameters
        ----------
        static_path : str
            path to the static file
        dyn_color : DynColor
            color information in the configuration
        dyn_font_path : DynFontPath
            font_path information in the configuration
        dyn_size : DynSize
            size information in the configuration
        """
        self.static_path: str = static_path
        self.dyn_color: DynColor = dyn_color
        self.dyn_font_path: DynFontPath = dyn_font_path
        self.dyn_size: DynSize = dyn_size
        self.background_img = None
        self.background_color = None
        self.text_font = None
        self.extra_font = None
        self.emoji_font = None
        self.key_map = None
        self.src_path = None

    async def run(self, dyn_maojor: Major, dyn_type) -> Optional[Image.Image]:
        self.background_color = self.dyn_color.dyn_gray if dyn_type == "F" else self.dyn_color.dyn_white
        self.background_img = Image.new("RGB", (1080, 695), self.background_color)
        self.draw = ImageDraw.Draw(self.background_img)
        self.text_font = ImageFont.truetype(self.dyn_font_path.text, self.dyn_size.text)
        self.extra_font = ImageFont.truetype(self.dyn_font_path.extra_text, self.dyn_size.text)
        self.emoji_font = ImageFont.truetype(self.dyn_font_path.emoji, self.dyn_size.emoji)
        self.key_map = TTFont(self.dyn_font_path.text, fontNumber=0)['cmap'].tables[0].ttFont.getBestCmap().keys()
        self.src_path = path.join(self.static_path, "Src")
        cover = f"{dyn_maojor.live.cover}@505w_285h_1c.webp"
        title = dyn_maojor.live.title
        watch_show = dyn_maojor.live.desc_second
        badge = dyn_maojor.live.badge
        try:
            await asyncio.gather(
                self.make_cover(cover, watch_show, badge),
                self.make_title(title)
            )
            self.background_img = self.background_img.convert("RGBA")
            return self.background_img
        except Exception as e:
            logger.exception("error")
            return None

    async def make_cover(self, cover: str, watch_show: str, badge):
        cover = await get_pictures(cover, (1010, 570))
        self.background_img.paste(cover, (35, 25), cover)
        font = ImageFont.truetype(self.dyn_font_path.text, self.dyn_size.sub_title)
        if badge.text:
            badge_text = badge.text
        else:
            badge_text = "直播"
        bg_color = self.dyn_color.dyn_pink
        badge_size = font.getsize(badge_text)
        badge_pic_size = (badge_size[0] + 20, badge_size[1] + 10)
        badge_pic = Image.new("RGBA", badge_pic_size, bg_color)
        draw = ImageDraw.Draw(badge_pic)
        draw.text((10, 3), badge_text, self.dyn_color.dyn_white, font=font)
        self.background_img.paste(badge_pic, (905, 50), badge_pic)

        watch_show_size = font.getsize(watch_show)
        watch_show_pic_size = (watch_show_size[0] + 20, badge_size[1] + 10)
        watch_show_pic = Image.new("RGBA", watch_show_pic_size, (0, 0, 0, 90))
        draw = ImageDraw.Draw(watch_show_pic)
        draw.text((10, 3), watch_show, fill=self.dyn_color.dyn_white, font=font)
        self.background_img.paste(watch_show_pic, (885 - watch_show_size[0], 50), watch_show_pic)

    async def make_title(self, title):
        emoji = await self.get_emoji(title)
        offset = 0
        position = 35
        total = len(title) - 1
        while offset <= total:
            if offset in emoji:
                emoji_img = emoji[offset]["emoji"]
                self.background_img.paste(emoji_img, (int(position), 606), emoji_img)
                position += (emoji_img.size[0] - 15)
                offset = emoji[offset]["match_end"]
                if position >= 1020:
                    self.draw.text((int(position), 600), "...", fill=self.dyn_color.dyn_black, font=self.text_font)
                    break
            else:
                text = title[offset]
                if ord(text) not in self.key_map:
                    self.draw.text((int(position), 600), text, fill=self.dyn_color.dyn_black, font=self.extra_font)
                    next_offset = self.extra_font.getbbox(text)[2]
                else:
                    self.draw.text((int(position), 600), text, fill=self.dyn_color.dyn_black, font=self.text_font)
                    next_offset = self.text_font.getbbox(text)[2]
                position += next_offset
                offset += 1
                if position >= 1020:
                    self.draw.text((int(position), 600), "...", fill=self.dyn_color.dyn_black, font=self.text_font)
                    break

    async def get_emoji(self, title):
        result = emoji.emoji_list(title)
        duplicate_removal_result = {i["emoji"] for i in result}
        emoji_dic = {}
        for i in duplicate_removal_result:
            emoji_origin_text = self.emoji_font.getbbox(i)
            emoji_img = Image.new(
                "RGBA", (emoji_origin_text[2], emoji_origin_text[3]), self.background_color)
            draw = ImageDraw.Draw(emoji_img)
            draw.text((0, 0), i, embedded_color=True, font=self.emoji_font)
            emoji_img = emoji_img.resize((self.dyn_size.text, self.dyn_size.text))
            emoji_dic[i] = emoji_img
        temp = {}
        for i in result:
            temp[i["match_start"]] = i
            temp[i["match_start"]]["emoji"] = emoji_dic[temp[i["match_start"]]["emoji"]]
        return temp
