from typing import List

from .consts import TYPES_TO_STR


class Balloon:
    def __init__(
        self, 
        tl_content: List[str] = [""], 
        pr_content: List[str] = [""], 
        comments: List[str] = [""], 
        btype: int = 0, 
        has_img: int = 0, 
        balloon_img: bytes = b"",
        img_type: str = ""
    ):
        self.tl_content: List[str] = tl_content
        self.pr_content: List[str] = pr_content
        self.comments: List[str] = comments
        self.btype: int = btype
        self.has_img: bool = has_img
        self.img: List[str, bytes] = [img_type, balloon_img]

    def add_img(self, img_t: str, img_b: bytes):
        """
        Adds image to the balloon or replaces original image.
        Image can be any type.
        """
        self.has_img = 1
        self.img = [img_t, img_b]

    def remove_img(self):
        """
        Removes image from the balloon.
        """
        self.has_img = 0
        self.img = ["", b""]

    @property
    def tl_len(self):
        """
        All translation lines' character length.
        """
        return sum(len(tl) for tl in self.tl_content)

    @property
    def pr_len(self):
        """
        All proofread lines' character length.
        """
        return sum(len(pr) for pr in self.pr_content)

    @property
    def comment_len(self):
        """
        All comment lines' character length.
        """
        return sum(len(comment) for comment in self.comments)

    @property
    def line_count(self):
        """
        Total trasnaltion line count, independent from pr or comment.
        """
        if not self.tl_content[0]:
            return 0
        return len(self.tl_content)

    def __str__(self) -> str:
        """
        '[BalloonTypeIdentifier]: [BalloonContent]'
        """
        if self.pr_content[0]:
            return "\n//\n".join([TYPES_TO_STR[self.btype] + line for line in self.pr_content])
        else:
            return "\n//\n".join([TYPES_TO_STR[self.btype] + line for line in self.tl_content])
