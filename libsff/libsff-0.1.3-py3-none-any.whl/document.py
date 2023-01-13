from base64 import b64decode, b64encode
from gzip import open as gzopen
from lzma import compress, decompress
from typing import List

from lxml import etree

from .balloon import Balloon
from .consts import IMG, R_IMG, R_TYPES, TYPES, Out
from .errors import FileExtentionNotCompatible


class Document:
    def __init__(self):
        self.METADATA_SCRIPT_VERSION = "Scanlation Script File v0.1.0"
        self.METADATA_APP_VERSION    = ""
        self.METADATA_INFO           = "Made by NandeMD."
        self.balloons: List[Balloon] = []

    def __str__(self):
        """
        Pretty printed xml as string.
        """
        return etree.tostring(
            self.create_xml(),
            pretty_print=True,
            encoding="utf-8"
        ).decode("utf-8")

    def __repr__(self):
        """
        Pretty printed xml as bytes.
        """
        return etree.tostring(
            self.create_xml(),
            pretty_print=True,
            encoding="utf-8"
        )

    @property
    def tl_len(self):
        """
        Sum of all balloons' tl_len.
        """
        return sum(balloon.tl_len for balloon in self.balloons)

    @property
    def pr_len(self):
        """
        Sum of all balloons' pr_len.
        """
        return sum(balloon.pr_len for balloon in self.balloons)

    @property
    def comment_len(self):
        """
        Sum of all balloons' comment_len.
        """
        return sum(balloon.comment_len for balloon in self.balloons)

    @property
    def balloon_count(self):
        """
        Total balloon count of the Document object.
        """
        return len(self.balloons)
    
    @property
    def line_count(self):
        """
        Sum of all balloons' line_count.
        """
        return sum(ln.line_count for ln in self.balloons)

    def __len__(self):
        """
        Total balloon count of the Document object.
        Same as balloon_count property.
        """
        return len(self.balloons)

    def add_balloon(self, balloon: Balloon):
        """
        Adds a balloon to the document.
        Balloon can onle be Balloon type.
        """
        self.balloons.append(balloon)

    def create_sub_elements(self, balloon: Balloon, sub_balloon: etree.Element, e_type: str):
        """
        Create sub xml elements for a Balloon object.
        Probably will change this.
        """
        content_map = {"text": balloon.tl_content, "proofread": balloon.pr_content, "comment": balloon.comments}
        wanted_content = content_map[e_type]
        if wanted_content[0]:
            for content in wanted_content:
                sub_text = etree.SubElement(sub_balloon, e_type)
                sub_text.text = content

    def __create_metadata(self, page):
        """
        Creates metadata xml element and it's all subelements.
        """
        metadata = etree.SubElement(
            page,
            "Metadata"
        )

        script = etree.SubElement(
            metadata,
            "Script"
        )
        script.text = self.METADATA_SCRIPT_VERSION

        app = etree.SubElement(
            metadata,
            "App"
        )
        app.text = self.METADATA_APP_VERSION

        metadata_info = etree.SubElement(
            metadata,
            "Info"
        )
        metadata_info.text = self.METADATA_INFO

        metadata_tl_len = etree.SubElement(
            metadata,
            "TLLength"
        )
        metadata_tl_len.text = str(self.tl_len)

        metadata_pr_len = etree.SubElement(
            metadata,
            "PRLength"
        )
        metadata_pr_len.text = str(self.pr_len)

        metadata_comments_length = etree.SubElement(
            metadata,
            "CMLength"
        )
        metadata_comments_length.text = str(self.comment_len)

        metadata_balloon_count = etree.SubElement(
            metadata,
            "BalloonCount"
        )
        metadata_balloon_count.text = str(self.balloon_count)

        metadata_line_count = etree.SubElement(
            metadata,
            "LineCount"
        )
        metadata_line_count.text = str(self.line_count)

        return metadata
    
    def create_xml(self) -> etree.ElementTree:
        """
        Builds document xml from python classes.
        """
        page = etree.Element('Document')
        doc = etree.ElementTree(page)

        metadata = self.__create_metadata(page)

        for balloon in self.balloons:
            sub_balloon = etree.SubElement(
                page,
                "Baloon",
                type=TYPES[balloon.btype],
                has_image=IMG[balloon.has_img]
            )

            self.create_sub_elements(balloon, sub_balloon, "text")
            self.create_sub_elements(balloon, sub_balloon, "proofread")
            self.create_sub_elements(balloon, sub_balloon, "comment")

            if balloon.has_img:
                sub_img = etree.SubElement(sub_balloon, "img", type=balloon.img[0])
                sub_img.text = b64encode(balloon.img[1])

        return doc

    def __save_raw(self, filename: str):
        """
        Save as raw xml with no compression.
        File sizes may be large if you add images.
        """
        with open(f"{filename}.sffx", "wb") as file:
            file.write(self.__repr__())

    def __save_gzip(self, filename: str):
        """
        Save as a gzip compressed xml.
        File size is considerably lower with this.
        Compression is done with Python gzip library.
        Faster than lzma.
        Compression level: 9
        """
        xml = self.create_xml()
        xml.write(f"{filename}.sffg", encoding='utf-8', pretty_print=True, compression=9)

    def __save_lzma(self, filename: str):
        """
        Save as a lzma compressed xml.
        File size is considerably lower with this.
        Compression is done with Python lzma library.
        Slower than gzip.
        Compression level: 9
        """
        binady_data = self.__repr__()
        with open(f"{filename}.sffl", "wb") as file:
            file.write(compress(binady_data, preset=9))

    def __save_txt(self, filename: str):
        """
        Save as a formatted txt.
        This mode can be used for distributing the translation.
        If your main goal is readabiliry, use this.
        No compression.
        File sizes are related to balloon count and total character count.
        """
        balloon_strings = [str(bl) for bl in self.balloons]

        with open(f"{filename}.txt", "w") as sfffile:
            sfffile.write(
                "\n\n".join(balloon_strings)
            )

    def save_sff(self, filename: str, method: int) -> bool:
        """
        Saves the file as specified filename with specified method.
        Use Out Enum for methods.\n
        Out.RAW: Raw XML (Possible large file size)\n
        Out.GZIP: Gzip compressed XML (Small file size)\n
        Out.LZMA: LZMA Compressed XML (Possible smaller file size but slower compression)\n
        Out.TXT: Formatted text, for distributing translation. Readability is high.\n
        Please look into save methods (__save_raw etc.) if you need more info.
        """
        if method == Out.RAW:
            self.__save_raw(filename)
        elif method == Out.GZIP:
            self.__save_gzip(filename)
        elif method == Out.LZMA:
            self.__save_lzma(filename)
        elif method == Out.TXT:
            self.__save_txt(filename)

        return True


    @staticmethod
    def open_sff(path: str) -> etree.Element:
        """
        Open a .sff* file and turn into xml tree.
        Currently has support for .sffx (raw xml), .sffg (gzip compessed xml)
        and .sffl (lzma compressed xml.
        """

        uncompressed = None
        if path.endswith(".sffg"):
            with gzopen(path, "rb") as sfffile:
                uncompressed = sfffile.read()
        elif path.endswith(".sffx"):
            with open(path, "r") as sfffile:
                uncompressed = sfffile.read()
        elif path.endswith(".sffl"):
            with open(path, "rb") as sfffile:
                uncompressed = decompress(sfffile.read())
        else:
            raise FileExtentionNotCompatible("CanScanlate only supports sffx, sffg and sffl types.")
        

        return etree.fromstring(uncompressed)

    @classmethod
    def create_from_sff(cls, path: str):
        """
        Read a xml tree and create a Document object from it.
        """
        doc = cls()
        tree = doc.open_sff(path)
        data = tree.find("Metadata")

        doc.METADATA_INFO           = data.find("Info").text if data is not None and data.find("Info") is not None else doc.METADATA_INFO
        doc.METADATA_APP_VERSION    = data.find("App").text if data is not None and data.find("App") is not None else doc.METADATA_APP_VERSION
        doc.METADATA_SCRIPT_VERSION = data.find("Script").text if data is not None and data.find("Script") is not None else doc.METADATA_SCRIPT_VERSION

        lines = tree.findall("Line")
        for line in lines:
            img_element = line.find("img")

            doc.add_balloon(
                Balloon(
                    tl_content=[text_elem.text for text_elem in line.findall("text")],
                    btype=R_TYPES[line.get("type")],
                    has_img=R_IMG[line.get("has_image")],
                    balloon_img=b64decode(img_element.text) if img_element is not None else b""
                )
            )
        return doc

    @classmethod
    def create_blank(cls):
        """
        Creates and returns a blanck Document object.
        Same as 'Document()'
        """
        return cls()
