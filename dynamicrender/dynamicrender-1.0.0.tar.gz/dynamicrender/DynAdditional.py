import re
from os import path
import asyncio
import emoji
from loguru import logger
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont
from dynamicadaptor.AddonCard import Additional


from .Core import  Optional
from .Tools import get_pictures
from .DynConfig import DynColor, DynFontPath, DynSize

class DynAdditionalRender:
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

    async def run(self, dyn_additional: Additional, dyn_type: Optional[str] = None) -> Optional[Image.Image]:
        """Render  additional of the dynamic into image

        Parameters
        ----------
        dyn_additional : Additional
            additional of the dynamic
        dyn_type : Optional[str]
            F or None
        Returns
        -------
        Optional[Image.Image]
            Rendered image
        """
        additional_type = dyn_additional.type
        try:
            if additional_type == "ADDITIONAL_TYPE_COMMON":
                return await DynAdditionalCommon(self.static_path, self.dyn_color, self.dyn_font_path, self.dyn_size).run(dyn_additional,dyn_type)
            elif additional_type == "ADDITIONAL_TYPE_GOODS":
                return await DynAdditionalGoods(self.static_path, self.dyn_color, self.dyn_font_path, self.dyn_size).run(dyn_additional,dyn_type)
            elif additional_type == "ADDITIONAL_TYPE_RESERVE":
                return await DynAdditionalReserve(self.static_path, self.dyn_color, self.dyn_font_path, self.dyn_size).run(dyn_additional,dyn_type)
            elif additional_type == "ADDITIONAL_TYPE_VOTE":
                return await DynAdditionalVote(self.static_path, self.dyn_color, self.dyn_font_path, self.dyn_size).run(dyn_additional,dyn_type)
            elif additional_type == "ADDITIONAL_TYPE_UGC":
                return await DynAdditionalUgc(self.static_path, self.dyn_color, self.dyn_font_path, self.dyn_size).run(dyn_additional,dyn_type)
            elif additional_type == "ADDITIONAL_TYPE_UPOWER_LOTTERY":
                return await DynAdditionalUpworkLottery(self.static_path, self.dyn_color, self.dyn_font_path, self.dyn_size).run(dyn_additional,dyn_type)
            else:
                logger.error("Unknown additional type")
                return None
        except Exception as e:
            logger.exception("error")
            return None
        

class DynAdditionalCommon:
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
        self.title_font = None
        self.sub_title_font = None
        self.background_img = None
        self.background_color = None
        self.inner_color = None
        self.draw = None
    
    async def run(self, dyn_additional: Additional, dyn_type) -> Optional[Image.Image]:
        try:
            self.background_color = self.dyn_color.dyn_gray if dyn_type == "F" else self.dyn_color.dyn_white
            self.inner_color = self.dyn_color.dyn_gray if dyn_type != "F" else self.dyn_color.dyn_white
            self.background_img = Image.new("RGBA", (1080, 285), self.background_color)
            self.draw = ImageDraw.ImageDraw(self.background_img)
            self.draw.rectangle(((35, 20), (1045, 265)), fill=self.inner_color, outline='#e5e9ef',width=2)
            self.title_font = ImageFont.truetype(self.dyn_font_path.text,self.dyn_size.sub_text)
            self.sub_title_font = ImageFont.truetype(self.dyn_font_path.text,self.dyn_size.title)
            
            await asyncio.gather(
                self.make_cover(dyn_additional.common.cover,dyn_additional.common.sub_type),
                self.make_title(dyn_additional.common),
                self.make_desc(dyn_additional.common),
                self.make_badge(dyn_additional.common)
            )


            return self.background_img
        except Exception as e:
            logger.exception("error")
            return None
    
    async def make_cover(self,cover,sub_type):
        if sub_type in {'decoration','game'}:
            cover_url = f"{cover}@190w_190h_1c.webp"
            cover = await get_pictures(cover_url,190)
        else:
            cover_url = f"{cover}@145w_195h_1c.webp"
            cover = await get_pictures(cover_url,(145,195))
        self.background_img.paste(cover,(60, 50),cover)
        
    async def make_title(self,common):
        title = common.title
        x = 280
        y= 70 if common.desc2 is None else 60
        for i in title:
            self.draw.text((x,y),i,self.dyn_color.dyn_black,self.title_font)
            x += self.title_font.getbbox(i)[2]
            if x > 815:
                self.draw.text((x,y),"...",self.dyn_color.dyn_black,self.title_font)
                break
    
    async def make_desc(self,common):
        x = 280
        desc2 = common.desc2
        y= 150 if desc2 is None else 135
        if common.desc2:
            y2 = 195
            for i in desc2:
                self.draw.text((x,y2),i,self.dyn_color.dyn_silver_gray,self.sub_title_font)
                x += self.sub_title_font.getbbox(i)[2]
                if x > 815:
                    self.draw.text((x,y2),"...",self.dyn_color.dyn_silver_gray,self.sub_title_font)
                    break
        x = 280
        desc1 = common.desc1
        for i in desc1:
            self.draw.text((x,y),i,self.dyn_color.dyn_silver_gray,self.sub_title_font)
            x += self.sub_title_font.getbbox(i)[2]
            if x > 815:
                self.draw.text((x,y),"...",self.dyn_color.dyn_silver_gray,self.sub_title_font)
                break
    
    async def make_badge(self,common):
        badge_text_map = {
            "pugv":"去试看",
            "ogv":"去追番",
            "manga":"去追漫",
            "decoration":"去看看",
            "game":"  进入  "
        }
        badge_text = badge_text_map.get(common.sub_type,"去看看")
        badge_color = self.dyn_color.dyn_pink
        badge_img_size = self.title_font.getbbox(badge_text)
        
        badge_img = Image.new("RGBA",(badge_img_size[2]+40,badge_img_size[3]+20),badge_color)
        draw = ImageDraw.Draw(badge_img)
        draw.text((20,5),badge_text,self.dyn_color.dyn_white,self.title_font)
        self.background_img.paste(badge_img,(860,95),badge_img)


class DynAdditionalReserve:
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
        self.title_font = None
        self.sub_title_font = None
        self.background_img = None
        self.background_color = None
        self.inner_color = None
        self.draw = None
        self.key_map=None
    
    async def run(self, dyn_additional: Additional, dyn_type) -> Optional[Image.Image]:
        try:
            self.background_color = self.dyn_color.dyn_gray if dyn_type == "F" else self.dyn_color.dyn_white
            self.inner_color = self.dyn_color.dyn_gray if dyn_type != "F" else self.dyn_color.dyn_white
            self.background_img = Image.new("RGBA", (1080, 225), self.background_color)
            self.draw = ImageDraw.ImageDraw(self.background_img)
            self.draw.rectangle(((35, 20), (1045, 205)), fill=self.inner_color, outline='#e5e9ef',width=2)
            self.title_font = ImageFont.truetype(self.dyn_font_path.text,self.dyn_size.sub_text)
            self.sub_title_font = ImageFont.truetype(self.dyn_font_path.text,self.dyn_size.title)
            self.extra_font = ImageFont.truetype(self.dyn_font_path.extra_text,self.dyn_size.sub_text)
            self.emoji_font = ImageFont.truetype(self.dyn_font_path.emoji,self.dyn_size.emoji)
            self.key_map = TTFont(self.dyn_font_path.text,fontNumber=0)['cmap'].tables[0].ttFont.getBestCmap().keys()
            await asyncio.gather(
                self.make_title(dyn_additional.reserve.title),
                self.make_desc(dyn_additional.reserve.desc1,dyn_additional.reserve.desc2),
                self.make_badge()
            )


            return self.background_img
        except Exception as e:
            logger.exception("error")
            return None

    async def make_title(self,title):
        emoji = await self.get_emoji(title)
        offset = 0
        position = 75
        total = len(title) - 1
        while offset <= total:
            if offset in emoji:
                emoji_img = emoji[offset]["emoji"]
                self.background_img.paste(emoji_img, (int(position), 70), emoji_img)
                position += (emoji_img.size[0])
                offset = emoji[offset]["match_end"]
                if position >= 810:
                    self.draw.text((int(position),70),"...",fill=self.dyn_color.dyn_black,font=self.title_font)
                    break
            else:
                text = title[offset]
                if ord(text) not in self.key_map:
                    self.draw.text((int(position),70),text,fill=self.dyn_color.dyn_black,font=self.extra_font)
                    next_offset = self.extra_font.getbbox(text)[2]
                else:
                    self.draw.text((int(position),70),text,fill=self.dyn_color.dyn_black,font=self.title_font)
                    next_offset = self.title_font.getbbox(text)[2]
                position += next_offset
                offset += 1
                if position >= 810:
                    self.draw.text((int(position),70),"...",fill=self.dyn_color.dyn_black,font=self.title_font)
                    break

    async def get_emoji(self,title):
        result = emoji.emoji_list(title)
        duplicate_removal_result = {i["emoji"] for i in result}
        emoji_dic = {}
        for i in duplicate_removal_result:
            emoji_origin_text = self.emoji_font.getbbox(i)
            emoji_img = Image.new(
                "RGBA", (emoji_origin_text[2], emoji_origin_text[3]), self.inner_color)
            draw = ImageDraw.Draw(emoji_img)
            draw.text((0, 0), i, embedded_color=True, font=self.emoji_font)
            emoji_img = emoji_img.resize((self.dyn_size.text, self.dyn_size.text))
            emoji_dic[i] = emoji_img
        temp = {}
        for i in result:
            temp[i["match_start"]] = i
            temp[i["match_start"]]["emoji"] = emoji_dic[temp[i["match_start"]]["emoji"]]
        return temp

    async def make_desc(self,desc1,desc2):
        desc = f"{desc1.text} · {desc2.text}"
        self.draw.text((75,140),desc,self.dyn_color.dyn_silver_gray,self.sub_title_font)

    async def make_badge(self):
        badge_text = "预约"
        badge_color = self.dyn_color.dyn_blue
        btn_img = Image.new("RGBA", (170, 75), badge_color)
        text_size = self.title_font.getbbox(badge_text)
        draw = ImageDraw.Draw(btn_img)
        x = int((170 - text_size[2]) / 2)
        y = int((75 - text_size[3]) / 2)-5
        draw.text((x,y),badge_text,fill=self.dyn_color.dyn_white,font=self.title_font)
        self.background_img.paste(btn_img,(850, 75),btn_img)


class DynAdditionalGoods:
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
        self.title_font = None
        self.sub_title_font = None
        self.background_img = None
        self.background_color = None
        self.inner_color = None
        self.draw = None
        self.key_map=None
    
    async def run(self, dyn_additional: Additional, dyn_type) -> Optional[Image.Image]:
        try:
            self.background_color = self.dyn_color.dyn_gray if dyn_type == "F" else self.dyn_color.dyn_white
            self.inner_color = self.dyn_color.dyn_gray if dyn_type != "F" else self.dyn_color.dyn_white
            self.background_img = Image.new("RGBA", (1080, 280), self.background_color)
            self.draw = ImageDraw.ImageDraw(self.background_img)

            self.draw.rectangle(((35, 20), (1045, 260)), fill=self.inner_color, outline='#e5e9ef',width=2)
            self.title_font = ImageFont.truetype(self.dyn_font_path.text,self.dyn_size.sub_text)
            self.sub_title_font = ImageFont.truetype(self.dyn_font_path.text,self.dyn_size.title)
            self.extra_font = ImageFont.truetype(self.dyn_font_path.extra_text,self.dyn_size.sub_text)
            self.emoji_font = ImageFont.truetype(self.dyn_font_path.emoji,self.dyn_size.emoji)
            self.key_map = TTFont(self.dyn_font_path.text,fontNumber=0)['cmap'].tables[0].ttFont.getBestCmap().keys()
            tasks = [self.make_cover(dyn_additional.goods.items)]
            if len(dyn_additional.goods.items)==1:
                tasks.append(self.make_title(dyn_additional.goods.items))
                tasks.append(self.make_price(dyn_additional.goods.items))
                tasks.append(self.make_btn())
            await asyncio.gather(*tasks)

            return self.background_img
        except Exception as e:
            logger.exception("error")
            return None
    
    async def make_title(self,items):
        name = items[0].name
        position = 295
        for text in name:
            if ord(text) not in self.key_map:
                self.draw.text((position,90),text,fill=self.dyn_color.dyn_black,font=self.extra_font)
                next_offset = self.extra_font.getbbox(text)[2]
            else:
                self.draw.text((position,90),text,fill=self.dyn_color.dyn_black,font=self.title_font)
                next_offset = self.title_font.getbbox(text)[2]
            position += next_offset
            if position >= 800:
                self.draw.text((position,90),"...",fill=self.dyn_color.dyn_black,font=self.title_font)
                break

    async def make_cover(self,items):
        url_list = []
        for i in items:
            url = re.sub("@(\d+)h_(\d+)w\S+","",i.cover)
            url_list.append(f"{url}@80w_80h_1c.webp")
        covers = await get_pictures(url_list,190)
        if len(covers)>1:
            for i,j in  enumerate(covers):
                x = 45 + i * 200
                if x > 1000:
                    break
                self.background_img.paste(j,(x,45),j)
        else:
            cover = covers[0]
            self.background_img.paste(cover,(60, 45),cover)

    async def make_price(self,items):
        price = items[0].price + "起"
        self.draw.text((295,160),price,fill=self.dyn_color.dyn_blue,font = self.sub_title_font)

    async def make_btn(self):
        btn_text = "去看看"
        badge_color = self.dyn_color.dyn_blue
        btn_img = Image.new("RGBA", (150, 75), badge_color)
        text_size = self.title_font.getbbox(btn_text)
        draw = ImageDraw.Draw(btn_img)
        x = int((150 - text_size[2]) / 2)
        y = int((75 - text_size[3]) / 2)-5
        draw.text((x,y),btn_text,fill=self.dyn_color.dyn_white,font=self.title_font)
        self.background_img.paste(btn_img,(870, 90),btn_img)

class DynAdditionalUgc:
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
        self.title_font = None
        self.sub_title_font = None
        self.background_img = None
        self.background_color = None
        self.inner_color = None
        self.draw = None
    
    async def run(self, dyn_additional: Additional, dyn_type) -> Optional[Image.Image]:
        try:
            self.background_color = self.dyn_color.dyn_gray if dyn_type == "F" else self.dyn_color.dyn_white
            self.inner_color = self.dyn_color.dyn_gray if dyn_type != "F" else self.dyn_color.dyn_white
            self.background_img = Image.new("RGB", (1080, 280), self.background_color)
            self.draw = ImageDraw.ImageDraw(self.background_img)

            self.draw.rectangle(((35, 20), (1045, 260)), fill=self.inner_color, outline='#e5e9ef',width=2)
            self.title_font = ImageFont.truetype(self.dyn_font_path.text,self.dyn_size.sub_text)
            self.sub_title_font = ImageFont.truetype(self.dyn_font_path.text,self.dyn_size.title)
            self.extra_font = ImageFont.truetype(self.dyn_font_path.extra_text,self.dyn_size.sub_text)
            self.emoji_font = ImageFont.truetype(self.dyn_font_path.emoji,self.dyn_size.emoji)
            await asyncio.gather(
                self.make_cover(dyn_additional.ugc.cover),
                self.make_title(dyn_additional.ugc.title),
                self.make_desc(dyn_additional.ugc.desc_second)
            )
            await self.make_duration(dyn_additional.ugc.duration)
            self.background_img = self.background_img.convert("RGBA")
            return self.background_img
        except Exception as e:
            logger.exception("error")
            return None
    
    async def make_title(self,title):
        position = 430
        y = 65
        for text in title:
            self.draw.text((position,y),text,fill=self.dyn_color.dyn_black,font=self.title_font)
            bbox = self.title_font.getbbox(text)
            next_offset = bbox[2]
            position += next_offset
            temp = position
            if position >= 1000:
                position = 430
                y += int(1.3 * bbox[3])
                if y>130:
                    self.draw.text((temp,y-int(1.5 * bbox[3])),"...",fill=self.dyn_color.dyn_black,font=self.title_font)
                    break

    async def make_cover(self,cover):
        cover_url = f"{cover}@340w_195h_1c.webp"
        cover = await get_pictures(cover_url)
        self.background_img.paste(cover,(60, 45),cover)


    async def make_desc(self,desc):
        self.draw.text((430,190),desc,fill=self.dyn_color.dyn_silver_gray,font=self.sub_title_font)

    async def make_duration(self,duration):
        duration_size = self.sub_title_font.getbbox(duration)
        bk_pic_size = (duration_size[2] + 20, duration_size[3] + 10)
        bk_pic = Image.new("RGBA", bk_pic_size, (0, 0, 0, 90))
        draw = ImageDraw.Draw(bk_pic)
        draw.text((10, 3),duration,self.dyn_color.dyn_white,font=self.sub_title_font)
        self.background_img.paste(bk_pic,(260, 170),bk_pic)

class DynAdditionalVote:
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
        self.title_font = None
        self.sub_title_font = None
        self.background_img = None
        self.background_color = None
        self.src_path = None
        self.inner_color = None
        self.draw = None
        self.key_map = None
    
    async def run(self, dyn_additional: Additional, dyn_type) -> Optional[Image.Image]:
        try:
            self.background_color = self.dyn_color.dyn_gray if dyn_type == "F" else self.dyn_color.dyn_white
            self.inner_color = self.dyn_color.dyn_gray if dyn_type != "F" else self.dyn_color.dyn_white
            self.background_img = Image.new("RGB", (1080, 280), self.background_color)
            self.draw = ImageDraw.ImageDraw(self.background_img)

            self.draw.rectangle(((35, 20), (1045, 260)), fill=self.inner_color, outline='#e5e9ef',width=2)
            self.title_font = ImageFont.truetype(self.dyn_font_path.text,self.dyn_size.sub_text)
            self.sub_title_font = ImageFont.truetype(self.dyn_font_path.text,self.dyn_size.title)
            self.extra_font = ImageFont.truetype(self.dyn_font_path.extra_text,self.dyn_size.sub_text)
            self.emoji_font = ImageFont.truetype(self.dyn_font_path.emoji,self.dyn_size.emoji)
            self.src_path = path.join(self.static_path,"Src")
            self.key_map = TTFont(self.dyn_font_path.text,fontNumber=0)['cmap'].tables[0].ttFont.getBestCmap().keys()

            await asyncio.gather(
                self.make_cover(),
                self.make_title(dyn_additional.vote.desc),
                self.make_join_num(dyn_additional.vote.join_num),
                self.make_btn()
            )
            self.background_img = self.background_img.convert("RGBA")
            return self.background_img
        except Exception as e:
            logger.exception("error")
            return None
    
    async def make_cover(self):
        cover = Image.open(path.join(self.src_path,"vote_icon.png")).convert("RGBA").resize((195, 195))
        self.background_img.paste(cover,(60, 45),cover)

    async def make_title(self,title):
        emoji = await self.get_emoji(title)
        offset = 0
        position = 280
        total = len(title) - 1
        while offset <= total:
            if offset in emoji:
                emoji_img = emoji[offset]["emoji"]
                self.background_img.paste(emoji_img, (int(position), 65), emoji_img)
                position += (emoji_img.size[0])
                offset = emoji[offset]["match_end"]
                if position >= 810:
                    self.draw.text((int(position),65),"...",fill=self.dyn_color.dyn_black,font=self.title_font)
                    break
            else:
                text = title[offset]
                if ord(text) not in self.key_map:
                    self.draw.text((int(position),65),text,fill=self.dyn_color.dyn_black,font=self.extra_font)
                    next_offset = self.extra_font.getbbox(text)[2]
                else:
                    self.draw.text((int(position),65),text,fill=self.dyn_color.dyn_black,font=self.title_font)
                    next_offset = self.title_font.getbbox(text)[2]
                position += next_offset
                offset += 1
                if position >= 810:
                    self.draw.text((int(position),65),"...",fill=self.dyn_color.dyn_black,font=self.title_font)
                    break

    async def get_emoji(self,title):
        result = emoji.emoji_list(title)
        duplicate_removal_result = {i["emoji"] for i in result}
        emoji_dic = {}
        for i in duplicate_removal_result:
            emoji_origin_text = self.emoji_font.getbbox(i)
            emoji_img = Image.new(
                "RGBA", (emoji_origin_text[2], emoji_origin_text[3]), self.inner_color)
            draw = ImageDraw.Draw(emoji_img)
            draw.text((0, 0), i, embedded_color=True, font=self.emoji_font)
            emoji_img = emoji_img.resize((self.dyn_size.text, self.dyn_size.text))
            emoji_dic[i] = emoji_img
        temp = {}
        for i in result:
            temp[i["match_start"]] = i
            temp[i["match_start"]]["emoji"] = emoji_dic[temp[i["match_start"]]["emoji"]]
        return temp
    
    async def make_join_num(self,join_num):
        text = f"{join_num}参与"
        self.draw.text((280,160),text,fill=self.dyn_color.dyn_silver_gray,font=self.sub_title_font)
    
    async def make_btn(self):
        btn_text = " 投票 "
        badge_color = self.dyn_color.dyn_blue
        btn_img = Image.new("RGBA", (150, 75), badge_color)
        text_size = self.title_font.getbbox(btn_text)
        draw = ImageDraw.Draw(btn_img)
        x = int((150 - text_size[2]) / 2)
        y = int((75 - text_size[3]) / 2)-5
        draw.text((x,y),btn_text,fill=self.dyn_color.dyn_white,font=self.title_font)
        self.background_img.paste(btn_img,(870, 90),btn_img)

class DynAdditionalUpworkLottery:
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
        self.title_font = None
        self.sub_title_font = None
        self.background_img = None
        self.background_color = None
        self.inner_color = None
        self.draw = None
        self.key_map=None
        self.src_path = None
    
    async def run(self, dyn_additional: Additional, dyn_type) -> Optional[Image.Image]:
        try:
            self.background_color = self.dyn_color.dyn_gray if dyn_type == "F" else self.dyn_color.dyn_white
            self.inner_color = self.dyn_color.dyn_gray if dyn_type != "F" else self.dyn_color.dyn_white
            self.background_img = Image.new("RGBA", (1080, 225), self.background_color)
            self.draw = ImageDraw.ImageDraw(self.background_img)
            self.draw.rectangle(((35, 20), (1045, 205)), fill=self.inner_color, outline='#e5e9ef',width=2)
            self.title_font = ImageFont.truetype(self.dyn_font_path.text,self.dyn_size.sub_text)
            self.sub_title_font = ImageFont.truetype(self.dyn_font_path.text,self.dyn_size.title)
            self.extra_font = ImageFont.truetype(self.dyn_font_path.extra_text,self.dyn_size.sub_text)
            self.emoji_font = ImageFont.truetype(self.dyn_font_path.emoji,self.dyn_size.emoji)
            self.key_map = TTFont(self.dyn_font_path.text,fontNumber=0)['cmap'].tables[0].ttFont.getBestCmap().keys()
            self.src_path = path.join(self.static_path,"Src")
            await asyncio.gather(
                self.make_title(dyn_additional.upower_lottery.title),
                self.make_desc(dyn_additional.upower_lottery.desc),
                self.make_badge(dyn_additional.upower_lottery.button)
            )


            return self.background_img
        except Exception as e:
            logger.exception("error")
            return None

    async def make_title(self,title):
        emoji = await self.get_emoji(title)
        offset = 0
        position = 75
        total = len(title) - 1
        while offset <= total:
            if offset in emoji:
                emoji_img = emoji[offset]["emoji"]
                self.background_img.paste(emoji_img, (int(position), 70), emoji_img)
                position += (emoji_img.size[0])
                offset = emoji[offset]["match_end"]
                if position >= 810:
                    self.draw.text((int(position),70),"...",fill=self.dyn_color.dyn_black,font=self.title_font)
                    break
            else:
                text = title[offset]
                if ord(text) not in self.key_map:
                    self.draw.text((int(position),70),text,fill=self.dyn_color.dyn_black,font=self.extra_font)
                    next_offset = self.extra_font.getbbox(text)[2]
                else:
                    self.draw.text((int(position),70),text,fill=self.dyn_color.dyn_black,font=self.title_font)
                    next_offset = self.title_font.getbbox(text)[2]
                position += next_offset
                offset += 1
                if position >= 810:
                    self.draw.text((int(position),70),"...",fill=self.dyn_color.dyn_black,font=self.title_font)
                    break

    async def get_emoji(self,title):
        result = emoji.emoji_list(title)
        duplicate_removal_result = {i["emoji"] for i in result}
        emoji_dic = {}
        for i in duplicate_removal_result:
            emoji_origin_text = self.emoji_font.getbbox(i)
            emoji_img = Image.new(
                "RGBA", (emoji_origin_text[2], emoji_origin_text[3]), self.inner_color)
            draw = ImageDraw.Draw(emoji_img)
            draw.text((0, 0), i, embedded_color=True, font=self.emoji_font)
            emoji_img = emoji_img.resize((self.dyn_size.text, self.dyn_size.text))
            emoji_dic[i] = emoji_img
        temp = {}
        for i in result:
            temp[i["match_start"]] = i
            temp[i["match_start"]]["emoji"] = emoji_dic[temp[i["match_start"]]["emoji"]]
        return temp

    async def make_desc(self,desc):
        img_size = int(1.3*self.dyn_size.title)
        lottery_img = Image.open(path.join(self.src_path,"lottery.png")).convert("RGBA").resize((img_size,img_size))
        self.background_img.paste(lottery_img,(75,140),lottery_img)
        x = 75+img_size
        for i in desc.text:
            self.draw.text((x,140),i,self.dyn_color.dyn_blue,self.sub_title_font)
            x += self.sub_title_font.getbbox(i)[2]
            if x> 810:
                self.draw.text((x,140),"...",self.dyn_color.dyn_blue,self.sub_title_font)
                break

    async def make_badge(self,button):
        badge_text = button.jump_style.text
        badge_color = self.dyn_color.dyn_blue
        btn_img = Image.new("RGBA", (170, 75), badge_color)
        text_size = self.title_font.getbbox(badge_text)
        draw = ImageDraw.Draw(btn_img)
        x = int((170 - text_size[2]) / 2)
        y = int((75 - text_size[3]) / 2)-5
        draw.text((x,y),badge_text,fill=self.dyn_color.dyn_white,font=self.title_font)
        self.background_img.paste(btn_img,(850, 75),btn_img)
