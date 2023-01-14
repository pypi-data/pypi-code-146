from template_generators.psp22 import PSP22
from .base import Base

class PSP22Command(Base):
    
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def run_command(cls, **kwargs) -> None:
        cls = cls()
        contract_name = cls.typer.prompt("Please enter name of contract")
        metadata = cls.typer.confirm("Do you want to store Metadata?")
        mintable = cls.typer.confirm("Do you want it to be mintable?")
        burnable = cls.typer.confirm("Do you want it to be burnable?")
        wrapper = cls.typer.confirm("Do you want it to be wrapper?")
        flashmint = cls.typer.confirm("Do you want it to be flashmint?")
        pausable = cls.typer.confirm("Do you want it to be pausable?")
        capped = cls.typer.confirm("Do you want it to be capped?")
        if metadata == False and mintable == False and burnable == False and wrapper == False and flashmint == False and pausable == False and capped == False:
            PSP22.generate_code(contract_name=contract_name, basic=True)
        else:
            PSP22.generate_code(contract_name=contract_name, mintable=mintable, metadata=metadata, burnable=burnable, wrapper=wrapper, flashmint=flashmint, pausable=pausable, capped=capped)
        print("psp22 contract scaffolded")
