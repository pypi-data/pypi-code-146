import typer
from typing import Optional

from commands.template_select import TemplateSelectCommand
from commands.flipper import FlipperCommand
from commands.psp22 import PSP22Command
from commands.psp34 import PSP34Command
from commands.psp37 import PSP37Command

def main(new: Optional[str] = typer.Argument(None), name: Optional[str] = typer.Argument(None)) -> None:
    
    if new and name:
        if new == "new":
            if name == "flipper":
                FlipperCommand.run_command()
            if name == "psp22":
                PSP22Command.run_command()
            if name == "psp34":
                PSP34Command.run_command()
            if name == "psp37":
                PSP37Command.run_command()
        else:
            print("Invalid option. Type ink-wizard to continue.")
    elif new and not name:
        print("Invalid option. Type ink-wizard to continue.")
    else:
    
        TemplateSelectCommand.show_options()

        contract_type = TemplateSelectCommand.ask_user()

        if contract_type == "1":
            FlipperCommand.run_command()
        if contract_type == "2":
            PSP22Command.run_command()
        if contract_type == "3":
            PSP34Command.run_command()
        if contract_type == "4":
            PSP37Command.run_command()


if __name__ == "__main__":
    typer.run(main)
