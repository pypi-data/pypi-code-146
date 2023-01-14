from template_generators.flipper import Flipper
from .base import Base

class FlipperCommand(Base):
    
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def run_command(**kwargs) -> None:
        Flipper.generate_code(**kwargs)
        print("flipper scaffolded")
