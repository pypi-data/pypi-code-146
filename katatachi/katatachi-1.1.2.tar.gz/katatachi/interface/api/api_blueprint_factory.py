from typing import Callable
from flask import Blueprint
from katatachi.content import ContentStore


ApiBlueprintFactory = Callable[[ContentStore], Blueprint]
