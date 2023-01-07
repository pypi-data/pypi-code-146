import typer

from tagbackup.commands import link, pull, push, status, unlink

app = typer.Typer()
app.registered_commands += link.app.registered_commands
app.registered_commands += pull.app.registered_commands
app.registered_commands += push.app.registered_commands
app.registered_commands += status.app.registered_commands
app.registered_commands += unlink.app.registered_commands
