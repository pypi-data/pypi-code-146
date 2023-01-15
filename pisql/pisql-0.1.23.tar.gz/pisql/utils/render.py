from rich.console import Console

console = Console(markup=True, color_system="auto", emoji=True, record=True)

errors = Console(
    markup=True, color_system="auto",
    emoji=True, record=True, stderr=True)