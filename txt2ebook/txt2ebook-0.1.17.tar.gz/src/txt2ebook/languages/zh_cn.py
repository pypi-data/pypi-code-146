# Copyright (C) 2021,2022,2023 Kian-Meng Ang
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Config for Simplified Chinese (zh-cn) language."""

IDEOGRAPHIC_SPACE = "\u3000"
SPACE = "\u0020"
NUMS_WORDS = "零一二三四五六七八九十百千两"
FULLWIDTH_NUMS = "０１２３４５６７８９"
HALFWIDTH_NUMS = "0123456789"

RE_NUMS = f"[.{HALFWIDTH_NUMS}{FULLWIDTH_NUMS}{NUMS_WORDS}]"
RE_VOLUMES = [
    f"第{RE_NUMS}*[集卷册部][^。~\n]*",
    f"卷{RE_NUMS}.*",
]
RE_CHAPTERS = [
    f"第{RE_NUMS}*[章篇回折辑节话].*",
    f"{RE_NUMS}*、.*",
    "声明.*",
    "引子.*",
    "楔子.*",
    "序[章幕曲]?",
    "序.*",
    "前言.*",
    "(?:内容)?简介",
    "外篇.*",
    "[号番]外[篇]?.*",
    "尾声",
    "终章.*",
    "后记.*",
    "文案.*",
    "尾声.*",
    "人物[介绍简介].*",
]

DEFAULT_RE_TITLE = r"书名：(.*)"
DEFAULT_RE_AUTHOR = r"作者：(.*)"
DEFAULT_RE_TAG = r"标签：(.*)"
DEFAULT_RE_VOLUME = "(" + "|".join(RE_VOLUMES) + ")"
DEFAULT_RE_CHAPTER = "(" + "|".join(RE_CHAPTERS) + ")"

STRUCTURE_NAMES = {
    "cover": "封面",
}
