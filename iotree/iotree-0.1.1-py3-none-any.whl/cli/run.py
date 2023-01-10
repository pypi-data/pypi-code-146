import os
import sys
import json
import rich
import typer
import subprocess
from rich.prompt import Prompt, Confirm

from iotree.core.reader import read
from iotree.core.render import (
    build, initConfig,
    demo_symbols, demo_themes,
    tableFromRecords
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
    )

@app.command(name='render', help='Render a Markup Language file as a tree.')
def render(
    file = typer.Argument(..., help='The file to render as a tree.'),
    ):
    """Render a Markup Language file as a tree."""
    obj = read(file)
    console.print(build(obj))

@app.command(name='check', help='Run checks on the package.')
def checks():
    """Run checks on the package."""
    os.system('pytest')
    
@app.command(name='demo', help='Run a demo of the CLI part of the package.')
def demo():
    """Run a demo of the CLI part of the package."""
    path = str(tests_dir / 'render_ex.py')
    subprocess.run([ sys.executable, path])
    
config = typer.Typer(
    name='config',
    help='Configure the style of your tree.',
    no_args_is_help=True)

@config.command(name='init', help='Initialize a config file.')
def initialize(
    user: str = typer.Option("machine", "-u", "--user", help='The user to set the value for.'),
    use_saved: bool = typer.Option(True, "-us", "--use-saved", help='Use the saved config.'),
    ):
    """Set a config value. These values are saved in the config directory.
    
    The file is named `local-config.json` can be updated either manually or through this command.
    """
    user = os.getlogin() if user == 'machine' else user
    ok = None
    console.print(f'[bold orange]Warning: no user declared.[/][dim magenta] using default/declared value = [underline]{user}[/][/]')
    if use_saved and len(local_config) > 0:
        lconf = local_config["user_info"] if "user_info" in lconf else local_config
        if user not in lconf:
            lconf["user_info"] = {user: "default"}
            console.print(f'[bold magenta]No config found for user [underline]{user}, [/][/][bold magenta]using default value.[/]')
        else:
            uconf = lconf["user_info"][user]
            uconf_theme = user_info[user]['theme'] if user in user_info else user_info['default']['theme']
            console.print(f'[bold magenta]Config found for user {user}[/]')
            console.print(f'[dim magenta]Config: {uconf} ===> {uconf_theme}: {__themes[uconf_theme]}[/]')
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
        json.dump(user_info, open(config_dir / 'user-settings.json', 'w+'), indent=4)
        json.dump(lconf, open( config_dir /'local-config.json', 'w+'), indent=4)
    else:
        console.print('[dim yellow]Proceeding with default values.[/]')
        lconf = { "user_info": {user: "default"}, "last_user": user }
        json.dump(lconf, open( config_dir /'local-config.json', 'w+'), indent=4)
            
@config.command(name='set', help='Set a config value.', no_args_is_help=True)
def setter(
    param: str = typer.Argument(..., help='The parameter to set.'),
    value: str = typer.Argument(..., help='The value to set the parameter to.'),
    user: str = typer.Argument(..., help='The user to set the value for.'),
    ):
    """Set a config value. These values are saved in the config directory.
    
    Possible values for `param` are:
    - `symbol`: The symbol to use for the tree.
    - `theme`: The theme to use for the tree.
    - `last_user`: The default user whose profile will be loaded by default.
    
    [bold red]Note: [/]The `last_user` parameter is set automatically when the `init` command is run.
    [bold red]Note: [/][orange]The value is [underline]only set for the given user[/underline][/].
    """
    param, value, user = param.lower(), value.lower(), user.lower()
    
    if param not in ['symbol', 'theme', 'last_user']:
        console.print(f'[bold red]Invalid parameter: {param}[/]')
        return sys.exit(1)
    elif param == 'last_user':
        console.print(f'[bold red]Cannot set the last user manually yet.[/]')
        return sys.exit(1)

@config.command(name='from-json', help='Add a new user from a JSON user entry.', no_args_is_help=True)
def from_file(
    markup_file: str = typer.Argument(..., help='The JSON/TOML/XML/YAML file containing the user entry.'),
    ):
    """Add a new user from a JSON user entry.
    
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

@config.command(name='ff', help='Alias for `from-file`, adds user from Markup language file', no_args_is_help=True)
def ff(
    markup_file: str = typer.Argument(..., help='The JSON/TOML/XML/YAML file containing the user entry.'),
    ):
    from_file(markup_file)

@config.command(name='get', help='Get a config value.', no_args_is_help=True)
def getter(
    param: str = typer.Argument(..., help='The parameter to get.'),
    user: str = typer.Option("machine", help='The user to get the value for.'),
    ):
    console.print(f'Getting {param} for {user}.')
    console.print(user_info[user][param])

@config.command(name='list', help='List all config values.')
def lister():
    rows = []
    for user, values in user_info.items():
        values['user'] = user
        rows.append(values)
    
    table = tableFromRecords(rows, title='User Settings', theme=user_info['default']['theme'])
    console.print(table)
    
@config.command(name='ls', help='Alias for `list`.')
def ls():
    lister()

@config.command(name='reset', help='Reset the config file.')
def reset():
    """Reset the config file."""
    os.remove(local_config)

app.add_typer(config, name='config',
    help='Configure the style of your tree.'
    )

app.add_typer(config, name='cfg',
    help='Alias for `config`. Configure the style of your tree.'
    )
