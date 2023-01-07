from pathlib import Path

import typer
from rich import print as rprint
from rich.markup import escape
from rich.progress import Progress, SpinnerColumn, TextColumn

from .proxmox import ProxmoxVMNotFoundError, ProxmoxMissingPermissionError
from .util.exceptions import PVECLIError

guest_cli = typer.Typer()


@guest_cli.callback()
def guest(
        ctx: typer.Context,
        vm: str = typer.Argument(..., help='VM Name or ID')
):
    proxmox_api = ctx.obj['proxmox_api']

    try:
        proxmox_api.check_permission('/vms', 'VM.Audit')
    except ProxmoxMissingPermissionError as exc:
        raise PVECLIError(f'Missing permission for VM-Management ({exc.path}): {exc.permission}')

    try:
        if vm.isdigit():
            vm_obj = proxmox_api.get_vm_by_id(int(vm))
        else:
            vm_obj = proxmox_api.get_vm_by_name(vm)
    except ProxmoxVMNotFoundError:
        raise PVECLIError(f'VM {vm} was not found.')

    try:
        proxmox_api.check_permission(f'/vms/{vm_obj["vmid"]}', 'VM.Monitor')
    except ProxmoxMissingPermissionError as exc:
        raise PVECLIError(f'Missing permission for VM {vm_obj["name"]} ({exc.path}): {exc.permission}')

    ctx.ensure_object(dict)
    ctx.obj['vm'] = vm_obj


@guest_cli.command()
def start(
        ctx: typer.Context,
        command: list[str] = typer.Argument(...)
):
    """Start command on guest"""
    proxmox_api = ctx.obj['proxmox_api']
    vm = ctx.obj['vm']
    command_string = ' '.join(command)

    pid = proxmox_api.exec(node=vm['node'], vm_id=vm['vmid'], command=command_string)
    rprint(pid)


@guest_cli.command()
def run(
        ctx: typer.Context,
        command: list[str] = typer.Argument(...)
):
    """Execute command on guest and return output.

    Exits with the exitcode of the command inside the VM."""
    proxmox_api = ctx.obj['proxmox_api']
    vm = ctx.obj['vm']
    command_string = ' '.join(command)

    pid = proxmox_api.exec(node=vm['node'], vm_id=vm['vmid'], command=command_string)
    result = proxmox_api.check_exec_status(node=vm['node'], vm_id=vm['vmid'], pid=pid)
    rprint(escape(result['out_data']))
    raise typer.Exit(code=result['exitcode'])


@guest_cli.command()
def upload(
        ctx: typer.Context,
        source: Path = typer.Argument(..., help='Path of the source file. Use "-" to read from stdin.',
                                      exists=True, dir_okay=False, resolve_path=True, allow_dash=True),
        destination: Path = typer.Argument(..., help='Path of the destination file inside the guest.',
                                           exists=False, readable=False)
):
    """Upload file to guest"""
    proxmox_api = ctx.obj['proxmox_api']
    vm = ctx.obj['vm']

    with typer.open_file(str(source), mode='rb') as source_stream:
        source_file = source_stream.read()

    with Progress(SpinnerColumn(style='bold white', finished_text='[blue bold]⠿'),
                  TextColumn('[progress.description]{task.description}')) as progress:
        task_id = progress.add_task(description=f'[white]Uploading {source} to {destination} on {vm["name"]}...',
                                    total=1)
        proxmox_api.file_write(node=vm['node'], vm_id=vm['vmid'], file_path=destination, content=source_file)
        progress.update(task_id, completed=1, refresh=True,
                        description=f'[blue]Done: Uploaded {source} to {destination} on {vm["name"]}')
