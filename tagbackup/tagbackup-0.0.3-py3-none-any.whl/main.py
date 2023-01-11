import typer

from tagbackup.commands import link, pull, push, status, unlink
# from commands import link, pull, push, status, unlink

app = typer.Typer(add_completion=False)
app.registered_commands += link.app.registered_commands
app.registered_commands += pull.app.registered_commands
app.registered_commands += push.app.registered_commands
app.registered_commands += status.app.registered_commands
app.registered_commands += unlink.app.registered_commands

# comment out this next line when publishing
# if __name__ == "__main__":
#     app()