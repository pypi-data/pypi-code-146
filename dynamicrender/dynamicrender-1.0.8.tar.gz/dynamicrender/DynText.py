import emoji
from PIL import Image, ImageFont, ImageDraw
from asyncio import gather
from dynamicadaptor.Content import Text
from loguru import logger
from os import path
from fontTools.ttLib import TTFont

from typing import Optional
from .DynConfig import DynColor, DynFontPath, DynSize
from .Tools import get_pictures, merge_pictures


class DynTextRender:
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
        self.static_path = static_path
        self.dyn_color = dyn_color
        self.dyn_font_path = dyn_font_path
        self.dyn_size = dyn_size

        self.cache_fold = None
        self.src_fold = None
        self.background = None
        self.text_font = None
        self.extra_text_font = None
        self.emoji_font = None
        self.background_color = None
        self.draw = None
        self.pic_list = None
        self.icon_size = None
        self.emoji_dict = None
        self.key_map=None
        self.offset = 45

    async def run(self, dyn_text: Text, dyn_type: Optional[str] = None) -> Optional[Image.Image]:
        """Render the text of the dynamic into image

        Parameters
        ----------
        dyn_text : Text
            The text of the dynamic
        dyn_type : Optional[str]
            F or None
        Returns
        -------
        Optional[Image.Image]
            Rendered image
        """
        self.background_color = self.dyn_color.dyn_gray if dyn_type == "F" else self.dyn_color.dyn_white
        self.text_font = ImageFont.truetype(
            self.dyn_font_path.text, size=self.dyn_size.text)
        self.extra_text_font = ImageFont.truetype(
            self.dyn_font_path.extra_text, size=self.dyn_size.text)
        self.emoji_font = ImageFont.truetype(
            self.dyn_font_path.emoji, size=self.dyn_size.emoji)
        self.cache_fold = path.join(self.static_path, "Cache")
        self.src_fold = path.join(self.static_path, "Src")
        self.icon_size = int(self.dyn_size.text * 1.5)
        self.key_map = TTFont(self.dyn_font_path.text,fontNumber=0)['cmap'].tables[0].ttFont.getBestCmap().keys()

        self.pic_list = []
        tasks = []
        try:
            if dyn_text.topic is not None:
                tasks.append(self.make_topic(dyn_text.topic))
            tasks.append(self.make_text_img(dyn_text))
            await gather(*tasks)
            return await merge_pictures([i for i in self.pic_list if i is not None])
        except Exception as e:
            logger.exception("error")
            return None

    async def make_topic(self, topic):
        topic = topic.name
        topic_size = self.dyn_size.text
        topic_img = Image.open(path.join(self.src_fold, "new_topic.png")).resize(
            (topic_size, topic_size))
        topic_bg = Image.new(
            "RGBA", (1080, self.icon_size + 10), self.background_color)
        topic_bg.paste(topic_img, (45, 15), topic_img)
        draw = ImageDraw.Draw(topic_bg)
        draw.text((45 + topic_size + 10, 10), topic,
                  self.dyn_color.dyn_blue, self.text_font)
        self.pic_list.append(topic_bg)

    async def make_text_img(self, dyn_text: Text):
        emoji_list = []
        emoji_name_list = []
        rich_list = []
        for i in dyn_text.rich_text_nodes:
            if i.type in {"RICH_TEXT_NODE_TYPE_VOTE", "RICH_TEXT_NODE_TYPE_LOTTERY", "RICH_TEXT_NODE_TYPE_GOODS",
                          "RICH_TEXT_NODE_TYPE_WEB", "RICH_TEXT_NODE_TYPE_BV", "RICH_TEXT_NODE_TYPE_CV"}:
                rich_list.append(i)
            if i.type == "RICH_TEXT_NODE_TYPE_EMOJI":
                if i.text not in emoji_name_list:
                    emoji_name_list.append(i.text)
                    emoji_list.append(i.emoji.icon_url)
        result = await gather(self.get_emoji(emoji_list, emoji_name_list), self.get_rich_pic(rich_list))
        await self.draw_text(result[1], dyn_text)

    async def get_emoji(self, emoji_url: list, emoji_name: list):
        emoji_pic = []
        emoji_index = []
        emoji_url_list = []
        temp = {}
        for i, emoji_text in enumerate(emoji_name):
            emoji_path = path.join(
                self.cache_fold, "Emoji", f"{emoji_text}.png")
            if path.exists(emoji_path):
                emoji_pic.append(Image.open(emoji_path))
            else:
                emoji_url_list.append(emoji_url[i])
                emoji_index.append(i)
        if emoji_url_list:
            result = await get_pictures(emoji_url_list, self.icon_size)
            for i, j in enumerate(emoji_index):
                emoji_path = path.join(
                    self.cache_fold, "Emoji", f"{emoji_name[j]}.png")
                emoji_pic.insert(j, result[i])
                result[i].save(emoji_path)
        for i, j in enumerate(emoji_name):
            temp[j] = emoji_pic[i]
        self.emoji_dict = temp

    async def get_emoji_text(self, text: str):
        result = emoji.emoji_list(text)
        duplicate_removal_result = {i["emoji"] for i in result}
        emoji_dic = {}
        for i in duplicate_removal_result:
            emoji_origin_text = self.emoji_font.getbbox(i)
            emoji_img = Image.new(
                "RGBA", (emoji_origin_text[2], emoji_origin_text[3]), self.background_color)
            draw = ImageDraw.Draw(emoji_img)
            draw.text((0, 0), i, embedded_color=True, font=self.emoji_font)
            emoji_img = emoji_img.resize(
                (self.dyn_size.text, self.dyn_size.text))
            emoji_dic[i] = emoji_img
        temp = {}
        for i in result:
            temp[i["match_start"]] = i
            temp[i["match_start"]]["emoji"] = emoji_dic[temp[i["match_start"]]["emoji"]]
        return temp

    async def get_rich_pic(self, rich_list):
        rich_dic = {}
        rich_size = self.dyn_size.text
        for i in rich_list:
            if i.type == "RICH_TEXT_NODE_TYPE_VOTE":
                if "vote" not in rich_dic:
                    img_path = path.join(self.src_fold, "vote.png")
                    img = Image.open(img_path).resize((rich_size, rich_size))
                    rich_dic["vote"] = img
            if i.type == "RICH_TEXT_NODE_TYPE_LOTTERY":
                if "lottery" not in rich_dic:
                    img_path = path.join(self.src_fold, "lottery.png")
                    img = Image.open(img_path).resize((rich_size, rich_size))
                    rich_dic["lottery"] = img
            if i.type == "RICH_TEXT_NODE_TYPE_GOODS":
                if "goods" not in rich_dic:
                    img_path = path.join(self.src_fold, "taobao.png")
                    img = Image.open(img_path).resize((rich_size, rich_size))
                    rich_dic["goods"] = img
            if i.type in {"RICH_TEXT_NODE_TYPE_WEB", "RICH_TEXT_NODE_TYPE_BV"}:
                if "link" not in rich_dic:
                    img_path = path.join(self.src_fold, "link.png")
                    img = Image.open(img_path).resize((rich_size, rich_size))
                    rich_dic["link"] = img
            if i.type == "RICH_TEXT_NODE_TYPE_CV":
                if "cv" not in rich_dic:
                    img_path = path.join(self.src_fold, "article.png")
                    img = Image.open(img_path).resize((rich_size, rich_size))
                    rich_dic["cv"] = img
        return rich_dic

    async def draw_text(self, rich_list: list, dyn_text: Text):

        self.background = Image.new(
            "RGBA", (1080, self.icon_size), self.background_color)
        self.draw = ImageDraw.Draw(self.background)
        for i in dyn_text.rich_text_nodes:

            if i.type in {"RICH_TEXT_NODE_TYPE_AT", "RICH_TEXT_NODE_TYPE_TEXT", "RICH_TEXT_NODE_TYPE_TOPIC"}:
                await self.draw_pain_text(i.type, i.text)
            elif i.type == "RICH_TEXT_NODE_TYPE_EMOJI":
                await self.draw_emoji(i.text)
            else:
                await self.draw_rich_text(i, rich_list)

        if self.offset != 45:
            self.pic_list.append(self.background)

    async def draw_pain_text(self, dyn_type: str, dyn_detail):
        dyn_detail = dyn_detail.translate(str.maketrans(
            {'\r': '', chr(65039): '', chr(65038): '', chr(8205): ''}))
        if dyn_type in {"RICH_TEXT_NODE_TYPE_AT", "RICH_TEXT_NODE_TYPE_TOPIC"}:
            for i in dyn_detail:
                self.draw.text((self.offset, 0), i,
                               fill=self.dyn_color.dyn_blue, font=self.text_font)
                self.offset += self.text_font.getlength(i)
                if self.offset >= 1020:
                    self.pic_list.append(self.background)
                    self.background = Image.new(
                        "RGBA", (1080, self.icon_size), self.background_color)
                    self.draw = ImageDraw.Draw(self.background)
                    self.offset = 45
        if dyn_type == "RICH_TEXT_NODE_TYPE_TEXT":
            emoji_text_list = await self.get_emoji_text(dyn_detail)
            offset = 0
            total = len(dyn_detail) - 1
            while offset <= total:
                if offset in emoji_text_list:
                    emoji_img = emoji_text_list[offset]["emoji"]
                    self.background.paste(
                        emoji_img, (int(self.offset), 5), emoji_img)
                    self.offset += self.icon_size - 15
                    offset = emoji_text_list[offset]["match_end"]
                    if self.offset >= 1000:
                        self.pic_list.append(self.background)
                        self.background = Image.new(
                            "RGBA", (1080, self.icon_size), self.background_color)
                        self.draw = ImageDraw.Draw(self.background)
                        self.offset = 45
                else:
                    text = dyn_detail[offset]
                    if text == "\n":
                        self.pic_list.append(self.background)
                        self.background = Image.new(
                            "RGBA", (1080, self.icon_size), self.background_color)
                        self.draw = ImageDraw.Draw(self.background)
                        self.offset = 45

                    else:
                        if ord(text) in self.key_map:
                            self.draw.text(
                                (self.offset, 0), text, fill=self.dyn_color.dyn_black, font=self.text_font)
                            self.offset += self.text_font.getlength(text)
                        else:
                            self.draw.text(
                                (self.offset, 0), text, fill=self.dyn_color.dyn_black, font=self.extra_text_font)
                            self.offset += self.extra_text_font.getlength(text)
                        if self.offset >= 1020:
                            self.pic_list.append(self.background)
                            self.background = Image.new(
                                "RGBA", (1080, self.icon_size), self.background_color)
                            self.draw = ImageDraw.Draw(self.background)
                            self.offset = 45
                    offset += 1

    async def draw_emoji(self, emoji_detail):
        img = self.emoji_dict[emoji_detail]
        img_size = img.size
        self.background.paste(img, (int(self.offset), 0), img)
        self.offset += img_size[0]
        if self.offset >= 1020:
            self.pic_list.append(self.background)
            self.background = Image.new(
                "RGBA", (1080, self.icon_size), self.background_color)
            self.draw = ImageDraw.Draw(self.background)
            self.offset = 45

    async def draw_rich_text(self, text_detail, rich_list):
        text = text_detail.text.translate(
            str.maketrans({chr(8203): '', chr(8205): ''}))
        if text_detail.type == "RICH_TEXT_NODE_TYPE_VOTE":
            icon = rich_list["vote"].convert("RGBA")
        elif text_detail.type == "RICH_TEXT_NODE_TYPE_LOTTERY":
            icon = rich_list["lottery"].convert("RGBA")
        elif text_detail.type == "RICH_TEXT_NODE_TYPE_GOODS":
            icon = rich_list["goods"].convert("RGBA")
        elif text_detail.type == "RICH_TEXT_NODE_TYPE_CV":
            icon = rich_list["cv"].convert("RGBA")
        else:
            icon = rich_list["link"].convert("RGBA")
        self.background.paste(icon, (int(self.offset), 5), icon)
        self.offset += icon.size[0]
        if self.offset >= 1020:
            self.pic_list.append(self.background)
            self.background = Image.new(
                "RGBA", (1080, self.icon_size), self.background_color)
            self.draw = ImageDraw.Draw(self.background)
            self.offset = 45
        for i in text:
            self.draw.text((self.offset, 0), i,
                           self.dyn_color.dyn_blue, self.text_font)
            self.offset += self.text_font.getbbox(i)[2]
            if self.offset >= 1020:
                self.pic_list.append(self.background)
                self.background = Image.new(
                    "RGBA", (1080, self.icon_size), self.background_color)
                self.draw = ImageDraw.Draw(self.background)
                self.offset = 45
