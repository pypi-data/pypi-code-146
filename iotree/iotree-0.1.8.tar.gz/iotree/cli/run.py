import os
import sys
import json
import rich
import typer
import subprocess
from signal import SIGINT, signal
from rich.prompt import Prompt, Confirm


from iotree.core.io.reader import read
from iotree.core.io.writer import write

from iotree.core.render.trees import (
    build
)

from iotree.core.render.demo import (
    print_demo, demo_symbols, demo_themes,
    colorTable, themeTable, symbolTable, extrasTable,
    render_file_demo
)

from iotree.core.render.tables import (
    tableFromRecords, treeThemeToTable, recordFormatting,

)
from iotree.utils.paths import (
    config_dir, package_dir,
    base_dir, tests_dir, safe_config_load
)

console = rich.console.Console()

symbols, themes, user_info, local_config = safe_config_load()

app = typer.Typer(
    name='iotree',
    help='A CLI & python package for rendering markup language docs as trees.',
    no_args_is_help=True,
    rich_help_panel="rich",
    rich_markup_mode='rich',
    )

config = typer.Typer(
    name='config',
    help='Configure the style of your tree.',
    no_args_is_help=True,
    rich_help_panel="rich",
    rich_markup_mode='rich',
    )

dev = typer.Typer(
    name='develop',
    help="Work ☕💻 on the package's 📦 content.",
    no_args_is_help=True,
    rich_help_panel="rich",
    rich_markup_mode='rich',
    )

view = typer.Typer(
    name='view',
    help="View 🔎 the package's 📦 themes 🖌️ & symbols ➡️ for customization 💅",
    no_args_is_help=True,
    rich_help_panel="rich",
    rich_markup_mode='rich',
    )

app.add_typer(config, name='config',
    help='Configure the ✨ style ✨ of your tree. [yellow]Alias: `cfg`.[/yellow]',
    rich_help_panel="rich",
    )

app.add_typer(config, name='cfg', hidden=True,
    help='Alias for `config`. Configure the ✨ style ✨ of your tree.',
    rich_help_panel="rich",
    )

app.add_typer(view, name='view', hidden=False,
    help="View 🔎 the package's 📦 themes 🖌️ & symbols 🗼 for customization 💅",
    rich_help_panel="rich",
    )

app.add_typer(dev, name='develop', hidden=False,
    help="Work 💻 on the package's 📦 content.",
    rich_help_panel="rich",
    )

@app.command(name='render', help='Render a Markup Language file 📂 as a tree.')
def render(
    file = typer.Argument(..., help='The file to render as a tree.'),
    ):
    """Render a Markup Language file 📂 as a tree 🌳."""
    obj = read(file)
    console.print(build(obj))

@dev.command(name='check', help='Run checks ❓ on the package 📦')
def checks():
    """Run checks on the package."""
    os.system('pytest')
    
@app.command(name='demo', help='Run a demo of the CLI part of the package.')
def demo():
    """Run a demo of the CLI part of the package."""
    render_file_demo(appname='iotree')

@config.command(name='init', help='Initialize a config file.')
def initialize(
    user: str = typer.Option(None, "-u", "--user", help='The user to set the value for.'),
    use_saved: bool = typer.Option(True, "-us", "--use-saved", help='Use the saved config.'),
    ):
    """Set a config value. These values are saved in the config directory.
    
    The file is named `local-config.json` can be updated either manually or through this command.
    """
    user = (
        user_info['last_user'] if user is None
        else user or os.getlogin()
        )
    
    ok = None
    console.print(f'[bold orange]Warning: no user declared.[/][dim magenta] using default/declared value = [underline]{user}[/][/]')
    if use_saved and len(local_config) > 0:
        lconf = local_config["user_info"] if "user_info" in local_config else local_config
        if user not in lconf:
            lconf["user_info"] = {user: "default"}
            console.print(f'[bold magenta]No config found for user [underline]{user}, [/][/][bold magenta]using default value.[/]')
        else:
            uconf = lconf["user_info"][user]
            uconf_theme = user_info[user]['theme'] if user in user_info else user_info['default']['theme']
            console.print(f'[bold magenta]Config found for user {user}[/]')
            console.print(f'[dim magenta]Config: {uconf} ===> {uconf_theme}: {themes[uconf_theme]}[/]')
            ok = Confirm.ask('[bold green underline]No need to initialize.[/] [bold magenta] Would you still like to overwrite these ?[/]')
    if ok is None:
        ok = Confirm.ask('[bold red]No saved config found.[/] [bold magenta] Would you like to create one?[/]')
    if ok:
        lconf = {}
        choices = demo_symbols()
        user_symbol = Prompt.ask(
            '[bold magenta]Which [bold yellow]symbol[/bold yellow] did you [bold pink]like most[/bold pink] ?[/bold magenta]',
            choices=choices, show_choices=True
            )
        user_data = {"name":user, "symbol": user_symbol}
        choices = demo_themes()
        user_theme = Prompt.ask(
            '[bold magenta]Which [bold yellow]theme[/bold yellow] did you [bold pink]like most[/bold pink] ?[/bold magenta]',
            choices=choices, show_choices=True
            )
        user_data['theme'] = user_theme
        user_info[user] = user_data
        lconf = { "user_info": {user: user_theme}, "last_user": user }
        write(user_info, config_dir /'user-info.json')
        write(lconf, config_dir /'user-info.json')
    else:
        console.print('[dim yellow]Proceeding with default values.[/]')
        lconf = { "user_info": {user: "default"}, "last_user": user }
        write(lconf, config_dir /'user-info.json')
            
@config.command(name='set', help='Set a config value.', no_args_is_help=True)
def setter(
    param: str = typer.Argument(..., help='The parameter to set.'),
    value: str = typer.Argument(..., help='The value to set the parameter to.'),
    user: str = typer.Argument(None, help='The user to set the value for.'),
    ):
    """Set a config value. These values are saved in the config directory.
    
    Possible values for `param` are:
    - `symbol`: The symbol to use for the tree.
    - `theme`: The theme to use for the tree.
    - `last_user`: The default user whose profile will be loaded by default.
    
    [bold red]Note: [/]The `last_user` parameter is set automatically when the `init` command is run.
    [bold red]Note: [/][orange]The value is [underline]only set for the given user[/underline][/].
    """
    confpaths = [config_dir / 'local-config.json', config_dir / 'user-settings.json']

    __local_config = read(confpaths[0])
    __user_info = read(confpaths[1])

    param, value = param.lower(), value.lower()

    if param == 'last_user':
        __local_config['last_user'] = value
        write(__local_config, confpaths[0])
        console.print(f'[bold magenta] ✅ Config found for user {user}[/]')
        console.print(f'[dim magenta] 👷 Config: {param} ===> {value}[/]')
        sys.exit(0)

    user = user.lower() if user is not None else None
    
    if user is not None and user not in __user_info:
        ok = Confirm.ask(f'[bold red] ❌ No config found for user {user}[/] [bold magenta] Would you like to create one?[/]')
        if ok:
            __user_info[user] = {}
            if param == 'theme':
                if value in themes:
                    __user_info[user]['theme'] = value
                    __local_config['user_info'] = {user: value}
                else:
                    __user_info[user]['theme'] = 'default'
                    console.print(f'[bold red] ❌ No theme found for user {user}[/] [bold magenta] Using default theme.[/]')
            elif param == 'symbol':
                if value in symbols:
                   __user_info[user]['symbol'] = value
                else:
                    __user_info[user]['symbol'] = '{'
                    console.print(f'[bold red] ❌ No symbol found for user {user}[/] [bold magenta] Using default symbol.[/]')
            write(__user_info, confpaths[1])
            console.print(f'[bold magenta] ✅ Config created for user {user}[/]')
            console.print(f'[dim magenta] 👷 Config: {param} ===> {value}[/]')
            write(__user_info, confpaths[1])
            write(__local_config, confpaths[0])
            sys.exit(0)
        else:
            console.print(f'[bold red] ❌ No config found for user {user}[/]')
            sys.exit(0)

    user = (
        user if user is not None
        else local_config['last_user'] if 'last_user' in local_config
        else os.getlogin()
        )
    
    for i, conf in enumerate([__local_config, __user_info]):
        uconf = (
            conf[user] if user in conf
            else conf["user_info"][user] if "user_info" in conf and user in conf["user_info"]
            else conf["user_info"] if "user_info" in conf
            else conf
            )
        if param in uconf:
            uconf[param] = value
            json.dump(
                conf, open(confpaths[i], 'w+'), indent=4
                )
            console.print(f'[dim magenta]Config: {uconf} ===> {param}: {value}[/]')
            sys.exit(0)
    console.print(f'[bold red] ❌ No config found for user {user}[/]')

@config.command(
    name='from-file',
    help='Add a new user from a JSON 📁 user entry. [bold yellow] Alias: `ff`[/]',
    no_args_is_help=True
    )
def from_file(
    markup_file: str = typer.Argument(..., help='The JSON/TOML/XML/YAML file containing the user entry.'),
    ):
    """Add a new user from a JSON 📁 user entry.
    
    The JSON file should have the following structure:
    ```json
    {
        "user": "<the user name>",
        "name": "<your first name>",
        "symbol": "<the symbol you like most>",
        "theme": "<the color theme you prefer>"
    }
    ```
    The equivalent TOML file would be:
    
    ```toml
    user = "<the user name>"
    name = "<your first name>"
    symbol = "<the symbol you like most>"
    theme = "<the color theme you prefer>"
    ```
    
    [bold red]Note: [/]The `last_user` parameter is set automatically when the `init` command is run.
    This command will add the user to the `user_info` dictionary in the `user-settings.json` file,
    but not set the last user in the `local-config.json` file.
    """
    mandatory_keys = ['user', 'name', 'symbol', 'theme']
    content = read(markup_file)
    if len(set(mandatory_keys).difference(content.keys())) > 0:
        str_mandatory_keys = '\n- '.join(mandatory_keys)
        console.print(
            f"""[bold red]The Markup file is missing one of the following keys:\n- {str_mandatory_keys}[/]"""
        )
        sys.exit(1)
    else:
        user_info[content['user']] = content
        local_config['user_info'][content['user']] = content['theme']
        json.dump(user_info, open(config_dir / 'user-settings.json', 'w+'), indent=4)
        json.dump(local_config, open( config_dir /'local-config.json', 'w+'), indent=4)
        console.print(f'[bold green]Added user {content["user"]} to config.[/]')

@config.command(
    name='ff',
    help='Alias for `from-file`, adds user from Markup language file',
    no_args_is_help=True, hidden=True
    )
def ff(
    markup_file: str = typer.Argument(..., help='The JSON/TOML/XML/YAML file containing the user entry.'),
    ):
    from_file(markup_file)

@config.command(name='get', help='Get a config value.', no_args_is_help=True)
def getter(
    param: str = typer.Argument(..., help='The parameter to get.'),
    user: str = typer.Option(None, help='The user to get the value for.'),
    ):
    confpaths = [config_dir / 'local-config.json', config_dir / 'user-settings.json']
    
    __local_config = read(confpaths[0])
    __user_info = read(confpaths[1])


    console.print(__user_info)
    console.print(__local_config)

    user = (
        user if user is not None
        else os.getlogin()
        )

    param, user = param.lower(), user.lower()

    if param == 'last_user':
        value = __local_config['last_user']
        console.print(f'[bold magenta] ✅ Config found for user {user}[/]')
        console.print(value)
        sys.exit(0)
    
    if param == "user":
        if user in __local_config["user_info"] or user in __user_info:
            value = f"user: {__user_info[user]}" if user in __user_info else f"user: {__local_config['user_info'][user]}"
            console.print(f'[bold magenta] ✅ Config for themes found for user {user}[/]')
            console.print(value)
            sys.exit(0)
        else:
            console.print(f'[bold red] ❌ No config found for user {os.getlogin()}[/]')
            console.print(f'[dim yellow] ❗️ You can add a config for {os.getlogin()} by running `config from-file <file>` or `config init`, or `config set <param> <value> <user>`[/]')
            sys.exit(1)

    user = os.getlogin() if "last_user" not in __local_config else __local_config["last_user"]
    
    for i, conf in enumerate([__local_config, __user_info]):
        uconf = (
            conf[user] if user in conf
            else conf["user_info"][user] if "user_info" in conf and user in conf["user_info"]
            else conf["user_info"] if "user_info" in conf
            else conf
            )
        if param in uconf:
            value = uconf[param]
            console.print(f'[bold magenta] ✅ Config found for user {user}[/]')
            console.print(value)
            sys.exit(0)
    console.print(f'[bold red] ❌ No config found for user {user}[/]')

@config.command(name='list', help='List all config values. [bold yellow] Alias: `ls`[/]')
def lister():
    rows = []
    for user, values in user_info.items():
        values['user'] = user
        rows.append(values)
    
    table = tableFromRecords(rows, title='User Settings', theme=user_info['default']['theme'])
    console.print(table)
    
@config.command(name='ls', help='Alias for `list`.', hidden=True)
def ls():
    lister()

@config.command(name='reset', help='Reset the config file.')
def reset():
    """Reset the config file."""
    os.remove(local_config)
    
    
@view.command(
    name='colors',
    help='View currently available 🏳️‍🌈 color 🏳️‍🌈 options',
    )
def view_colors():
    """View currently available 🏳️‍🌈 color 🏳️‍🌈 options"""
    console.print(
            colorTable()
        )

@view.command(
    name='themes',
    help='View currently available 🖌️ theme 🖌️ options',
    )
def view_themes():
    """View currently available 🖌️ theme 🖌️ options"""
    console.print(
            themeTable()
        )

@view.command(
    name='symbols',
    help='View currently available 🗼 symbols 🗼 options',
    )
def view_themes():
    """View currently available 🗼 symbols 🗼 options"""
    console.print(
            symbolTable()
        )

@view.command(
    name='extras',
    help='View extra 🎁 symbols 🎁 options 🧐 [dim](not included in the default set)[/]',
    )
def extras(num: int = typer.Option(100, "-n", "--num", help='The number of extra symbols to view.')):
    """View extra 🎁 symbols 🎁 options 🧐 [dim](not included in the default set)[/]"""

    rich.print("""
[bold magenta]I had to keep the basic symbols quite light, however,[/]
    
[bold green]There are [underline]a lot of other symbols[/] available.[/]
If you want to add one to the list, feel free to either [bold cyan]contact me[/]
or add the corresponding unicode to the symbols file [yellow]using the `extra` config command.
[/]
    """)
    ok = typer.confirm(f'You are about to view {num} extra symbols. Do you want to continue?', default=True)
    if ok:
        console.print(
            extrasTable(num)
        )
    else:
        console.print('[bold red]Aborting.[/]')
        console.print('[dim]You can always view the extra symbols later.[/]')
        console.print('[green]Tip: Use the -n or --num parameter[/]')
        console.print('[bold yellow]Exiting...[/]')
        sys.exit(0)
   