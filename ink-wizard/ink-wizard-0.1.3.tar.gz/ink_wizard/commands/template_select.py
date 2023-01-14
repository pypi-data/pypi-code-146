from .base import Base

class TemplateSelectCommand(Base):
    
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def show_options(**kwargs) -> None:
        print("Welcome to Ink Wizard!")
        print("Type 1 to scaffold flipper contract")
        print("Type 2 to scaffold psp22 contract")
        print("Type 3 to scaffold psp34 contract")
        print("Type 4 to scaffold psp37 contract")        

    @classmethod
    def ask_user(cls, **kwargs) -> str:
        return cls().typer.prompt("Enter your choice to continue")
