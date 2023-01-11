from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod


class MessageType:
    Text = "text"
    Image = "image"
    Audio = "audio"
    Video = "video"
    File = "file"
    Template = "template"
    Custom = "custom"
