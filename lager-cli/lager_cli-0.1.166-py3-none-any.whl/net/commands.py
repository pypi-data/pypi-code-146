"""
    lager.lister.commands

    List commands
"""
import json
import click
from texttable import Texttable
from ..context import get_default_gateway
from ..context import get_impl_path
from ..python.commands import run_python_internal

def channel_num(mux, mapping):
    point = mux['scope_points'][0][1]
    if mux['role'] == 'analog':
        return ord(point) - ord('A') + 1
    if mux['role'] == 'logic':
        return int(point)
    try:
        numeric = int(point, 10)
        return numeric
    except ValueError:
        return ord(point) - ord('A') + 1

def get_nets(ctx, gateway):
    session = ctx.obj.session
    resp = session.all_muxes(gateway)
    resp.raise_for_status()
    return resp.json()['muxes']


def display_nets(muxes, netname, net_role=None):
    table = Texttable()
    table.set_deco(Texttable.HEADER)
    table.set_cols_dtype(['t', 't', 't'])
    table.set_cols_align(['l', 'r', 'r'])
    table.add_row(['name', 'type', 'channel'])
    for mux in muxes:
        for mapping in mux['mappings']:
            if netname is None or netname == mapping['net']:
                channel = channel_num(mux, mapping)
                if net_role!=None:
                    if net_role == mux['role']:
                        table.add_row([mapping['net'], mux['role'], channel])
                else:
                    table.add_row([mapping['net'], mux['role'], channel])

    click.echo(table.draw())

@click.group(invoke_without_command=True)
@click.argument('NETNAME', required=False)
@click.pass_context
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
def analog(ctx, gateway, dut, netname):
    """
        Interface for Analog nets
    """
    gateway = gateway or dut
    if netname!=None:
        ctx.obj.netname = netname
    if ctx.invoked_subcommand is not None:
        return

    if gateway is None:
        gateway = get_default_gateway(ctx)

    muxes = get_nets(ctx, gateway)

    display_nets(muxes, None, 'analog')    

@click.group(invoke_without_command=True)
@click.argument('NETNAME', required=False)
@click.pass_context
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
def logic(ctx, gateway, dut, netname):
    """
        Interface for Logic nets
    """
    gateway = gateway or dut
    if netname!=None:
        ctx.obj.netname = netname
    if ctx.invoked_subcommand is not None:
        return

    if gateway is None:
        gateway = get_default_gateway(ctx)

    muxes = get_nets(ctx, gateway)

    display_nets(muxes, None, 'logic') 

@click.group(invoke_without_command=True)
@click.pass_context
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
def net(ctx, gateway, dut):
    """
        Active nets for a given DUT
    """
    gateway = gateway or dut
    if ctx.invoked_subcommand is not None:
        return

    if gateway is None:
        gateway = get_default_gateway(ctx)

    muxes = get_nets(ctx, gateway)

    display_nets(muxes, None)

def validate_net(ctx, muxes, netname, role):
    for mux in muxes:
        if mux['role'] != role:
            continue
        for mapping in mux['mappings']:
            if mapping['net'] == netname:
                return mapping
    raise click.UsageError(f'{role.title()} net with name `{netname}` not found!', ctx=ctx)

@net.command()
@click.pass_context
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--mcu', required=False)
@click.option('--clear', is_flag=True, default=False, required=False, help='Clear the associated mux')
@click.argument('NETNAME')
def mux(ctx, gateway, dut, mcu, clear, netname):
    """
        Activate a Net
    """
    gateway = gateway or dut
    if gateway is None:
        gateway = get_default_gateway(ctx)
    session = ctx.obj.session

    data = {
        'action': 'mux',
        'mcu': mcu,
        'params': {
            'clear': clear,
            'netname': netname,
        }
    }
    session.net_action(gateway, data).json()


@net.command()
@click.pass_context
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
@click.argument('NETNAME')
def show(ctx, gateway, dut, netname):
    """
        Show the available nets which match a given name
    """
    gateway = gateway or dut
    if gateway is None:
        gateway = get_default_gateway(ctx)

    muxes = get_nets(ctx, gateway)
    display_nets(muxes, netname)

@analog.command()
@click.pass_context
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--mcu', required=False)
def disable(ctx, gateway, dut, mcu):
    """
        Disable Net
    """
    gateway = gateway or dut
    if gateway is None:
        gateway = get_default_gateway(ctx)

    netname = ctx.obj.netname
    data = {
        'action': 'disable_net',
        'mcu': mcu,
        'params': {
            'netname': netname,
        }
    }
    run_python_internal(
        ctx,
        get_impl_path('enable_disable.py'),
        dut,
        image='',
        env=(f'LAGER_COMMAND_DATA={json.dumps(data)}',),
        passenv=(),
        kill=False,
        download=(),
        allow_overwrite=False,
        signum='SIGTERM',
        timeout=0,
        detach=False,
        port=(),
        org=None,
        args=(),
    )    

@analog.command()
@click.pass_context
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--mcu', required=False)
def enable(ctx, gateway, dut, mcu):
    """
        Enable Net
    """
    gateway = gateway or dut
    if gateway is None:
        gateway = get_default_gateway(ctx)

    netname = ctx.obj.netname
    data = {
        'action': 'enable_net',
        'mcu': mcu,
        'params': {
            'netname': netname,
        }
    }
    run_python_internal(
        ctx,
        get_impl_path('enable_disable.py'),
        dut,
        image='',
        env=(f'LAGER_COMMAND_DATA={json.dumps(data)}',),
        passenv=(),
        kill=False,
        download=(),
        allow_overwrite=False,
        signum='SIGTERM',
        timeout=0,
        detach=False,
        port=(),
        org=None,
        args=(),
    ) 

@logic.command()
@click.pass_context
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--mcu', required=False)
def enable(ctx, gateway, dut, mcu):
    """
        Enable Net
    """
    gateway = gateway or dut
    if gateway is None:
        gateway = get_default_gateway(ctx)

    netname = ctx.obj.netname
    data = {
        'action': 'enable_net',
        'mcu': mcu,
        'params': {
            'netname': netname,
        }
    }
    run_python_internal(
        ctx,
        get_impl_path('enable_disable.py'),
        dut,
        image='',
        env=(f'LAGER_COMMAND_DATA={json.dumps(data)}',),
        passenv=(),
        kill=False,
        download=(),
        allow_overwrite=False,
        signum='SIGTERM',
        timeout=0,
        detach=False,
        port=(),
        org=None,
        args=(),
    )

@analog.command()
@click.pass_context
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--mcu', required=False)
def start(ctx, gateway, dut, mcu):
    """
        Start waveform capture
    """
    gateway = gateway or dut
    if gateway is None:
        gateway = get_default_gateway(ctx)

    netname = ctx.obj.netname
    data = {
        'action': 'start_capture',
        'mcu': mcu,
        'params': {
            'netname': netname,
        }
    }
    run_python_internal(
        ctx,
        get_impl_path('enable_disable.py'),
        dut,
        image='',
        env=(f'LAGER_COMMAND_DATA={json.dumps(data)}',),
        passenv=(),
        kill=False,
        download=(),
        allow_overwrite=False,
        signum='SIGTERM',
        timeout=0,
        detach=False,
        port=(),
        org=None,
        args=(),
    ) 

@analog.command()
@click.pass_context
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--mcu', required=False)
def start_single(ctx, gateway, dut, mcu):
    """
        Start a single waveform capture
    """
    gateway = gateway or dut
    if gateway is None:
        gateway = get_default_gateway(ctx)

    netname = ctx.obj.netname
    data = {
        'action': 'start_single',
        'mcu': mcu,
        'params': {
            'netname': netname,
        }
    }
    run_python_internal(
        ctx,
        get_impl_path('enable_disable.py'),
        dut,
        image='',
        env=(f'LAGER_COMMAND_DATA={json.dumps(data)}',),
        passenv=(),
        kill=False,
        download=(),
        allow_overwrite=False,
        signum='SIGTERM',
        timeout=0,
        detach=False,
        port=(),
        org=None,
        args=(),
    )

@analog.command()
@click.pass_context
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--mcu', required=False)
def stop(ctx, gateway, dut, mcu):
    """
        Stop waveform capture
    """
    gateway = gateway or dut
    if gateway is None:
        gateway = get_default_gateway(ctx)

    netname = ctx.obj.netname
    data = {
        'action': 'stop_capture',
        'mcu': mcu,
        'params': {
            'netname': netname,
        }
    }
    run_python_internal(
        ctx,
        get_impl_path('enable_disable.py'),
        dut,
        image='',
        env=(f'LAGER_COMMAND_DATA={json.dumps(data)}',),
        passenv=(),
        kill=False,
        download=(),
        allow_overwrite=False,
        signum='SIGTERM',
        timeout=0,
        detach=False,
        port=(),
        org=None,
        args=(),
    )


@net.command()
@click.pass_context
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--mcu', required=False)
@click.option('--voltdiv', help='Volts per division')
@click.option('--timediv', help='Time per division')
@click.option('--voltoffset', help='Voltage offset')
@click.option('--timeoffset', help='Time offset')
@click.argument('NETNAME')
def trace(ctx, gateway, dut, mcu, voltdiv, timediv, voltoffset, timeoffset, netname):
    """
        Trace options
    """
    gateway = gateway or dut
    if gateway is None:
        gateway = get_default_gateway(ctx)

    data = {
        'action': 'trace',
        'mcu': mcu,
        'params': {
            'voltdiv': voltdiv,
            'timediv': timediv,
            'voltoffset': voltoffset,
            'timeoffset': timeoffset,
            'netname': netname,
        }
    }
    run_python_internal(
        ctx,
        get_impl_path('trace.py'),
        dut,
        image='',
        env=(f'LAGER_COMMAND_DATA={json.dumps(data)}',),
        passenv=(),
        kill=False,
        download=(),
        allow_overwrite=False,
        signum='SIGTERM',
        timeout=0,
        detach=False,
        port=(),
        org=None,
        args=(),
    )


@net.group()
def measure():
    """
        Measure characteristics of analog andl logic nets
    """    
    pass

@measure.command()
@click.pass_context
@click.argument('NETNAME')
@click.option('--mcu', required=False)
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--display', default=False, type=click.BOOL, help='Display measurement on screen')
@click.option('--cursor', default=False, type=click.BOOL, help='Enable measurement cursor')
def vavg(ctx, netname, mcu, gateway, dut, display, cursor):
    """
    Measure average voltage of captured net waveform
    """    
    gateway = gateway or dut
    if gateway is None:
        gateway = get_default_gateway(ctx)

    data = {
        'action': 'measure_vavg',
        'mcu': mcu,
        'params': {
            'netname': netname,
            'display': display,
            'cursor': cursor
        }
    }

    run_python_internal(
        ctx,
        get_impl_path('measurement.py'),
        dut,
        image='',
        env=(f'LAGER_COMMAND_DATA={json.dumps(data)}',),
        passenv=(),
        kill=False,
        download=(),
        allow_overwrite=False,
        signum='SIGTERM',
        timeout=0,
        detach=False,
        port=(),
        org=None,
        args=(),
    )

@measure.command()
@click.pass_context
@click.argument('NETNAME')
@click.option('--mcu', required=False)
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--display', default=False, type=click.BOOL, help='Display measurement on screen')
@click.option('--cursor', default=False, type=click.BOOL, help='Enable measurement cursor')
def vmax(ctx, netname, mcu, gateway, dut, display, cursor):
    """
    Measure maximum voltage of captured net waveform
    """    
    gateway = gateway or dut
    if gateway is None:
        gateway = get_default_gateway(ctx)

    data = {
        'action': 'measure_vmax',
        'mcu': mcu,
        'params': {
            'netname': netname,
            'display': display,
            'cursor': cursor            
        }
    }

    run_python_internal(
        ctx,
        get_impl_path('measurement.py'),
        dut,
        image='',
        env=(f'LAGER_COMMAND_DATA={json.dumps(data)}',),
        passenv=(),
        kill=False,
        download=(),
        allow_overwrite=False,
        signum='SIGTERM',
        timeout=0,
        detach=False,
        port=(),
        org=None,
        args=(),
    )

@measure.command()
@click.pass_context
@click.argument('NETNAME')
@click.option('--mcu', required=False)
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--display', default=False, type=click.BOOL, help='Display measurement on screen')
@click.option('--cursor', default=False, type=click.BOOL, help='Enable measurement cursor')
def vmin(ctx, netname, mcu, gateway, dut, display, cursor):
    """
    Measure minimum voltage of captured net waveform
    """    
    gateway = gateway or dut
    if gateway is None:
        gateway = get_default_gateway(ctx)

    data = {
        'action': 'measure_vmin',
        'mcu': mcu,
        'params': {
            'netname': netname,
            'display': display,
            'cursor': cursor            
        }
    }

    run_python_internal(
        ctx,
        get_impl_path('measurement.py'),
        dut,
        image='',
        env=(f'LAGER_COMMAND_DATA={json.dumps(data)}',),
        passenv=(),
        kill=False,
        download=(),
        allow_overwrite=False,
        signum='SIGTERM',
        timeout=0,
        detach=False,
        port=(),
        org=None,
        args=(),
    )

@measure.command()
@click.pass_context
@click.argument('NETNAME')
@click.option('--mcu', required=False)
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--display', default=False, type=click.BOOL, help='Display measurement on screen')
@click.option('--cursor', default=False, type=click.BOOL, help='Enable measurement cursor')
def vpp(ctx, netname, mcu, gateway, dut, display, cursor):
    """
    Measure peak to peak voltage of captured net waveform
    """    
    gateway = gateway or dut
    if gateway is None:
        gateway = get_default_gateway(ctx)

    data = {
        'action': 'measure_vpp',
        'mcu': mcu,
        'params': {
            'netname': netname,
            'display': display,
            'cursor': cursor            
        }
    }

    run_python_internal(
        ctx,
        get_impl_path('measurement.py'),
        dut,
        image='',
        env=(f'LAGER_COMMAND_DATA={json.dumps(data)}',),
        passenv=(),
        kill=False,
        download=(),
        allow_overwrite=False,
        signum='SIGTERM',
        timeout=0,
        detach=False,
        port=(),
        org=None,
        args=(),
    )

@measure.command()
@click.pass_context
@click.argument('NETNAME')
@click.option('--mcu', required=False)
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--display', default=False, type=click.BOOL, help='Display measurement on screen')
@click.option('--cursor', default=False, type=click.BOOL, help='Enable measurement cursor')
def vrms(ctx, netname, mcu, gateway, dut, display, cursor):
    """
    Measure Root Mean Square voltage of captured net waveform
    """    
    gateway = gateway or dut
    if gateway is None:
        gateway = get_default_gateway(ctx)

    data = {
        'action': 'measure_vrms',
        'mcu': mcu,
        'params': {
            'netname': netname,
            'display': display,
            'cursor': cursor            
        }
    }

    run_python_internal(
        ctx,
        get_impl_path('measurement.py'),
        dut,
        image='',
        env=(f'LAGER_COMMAND_DATA={json.dumps(data)}',),
        passenv=(),
        kill=False,
        download=(),
        allow_overwrite=False,
        signum='SIGTERM',
        timeout=0,
        detach=False,
        port=(),
        org=None,
        args=(),
    )

@measure.command()
@click.pass_context
@click.argument('NETNAME')
@click.option('--mcu', required=False)
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--display', default=False, type=click.BOOL, help='Display measurement on screen')
@click.option('--cursor', default=False, type=click.BOOL, help='Enable measurement cursor')
def period(ctx, netname, mcu, gateway, dut, display, cursor):
    """
    Measure period of captured net waveform
    """    
    gateway = gateway or dut
    if gateway is None:
        gateway = get_default_gateway(ctx)

    data = {
        'action': 'measure_period',
        'mcu': mcu,
        'params': {
            'netname': netname,
            'display': display,
            'cursor': cursor            
        }
    }

    run_python_internal(
        ctx,
        get_impl_path('measurement.py'),
        dut,
        image='',
        env=(f'LAGER_COMMAND_DATA={json.dumps(data)}',),
        passenv=(),
        kill=False,
        download=(),
        allow_overwrite=False,
        signum='SIGTERM',
        timeout=0,
        detach=False,
        port=(),
        org=None,
        args=(),
    )

@measure.command()
@click.pass_context
@click.argument('NETNAME')
@click.option('--mcu', required=False)
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--display', default=False, type=click.BOOL, help='Display measurement on screen')
@click.option('--cursor', default=False, type=click.BOOL, help='Enable measurement cursor')
def freq(ctx, netname, mcu, gateway, dut, display, cursor):
    """
    Measure frequency of captured net waveform
    """    
    gateway = gateway or dut
    if gateway is None:
        gateway = get_default_gateway(ctx)

    data = {
        'action': 'measure_freq',
        'mcu': mcu,
        'params': {
            'netname': netname,
            'display': display,
            'cursor': cursor            
        }
    }

    run_python_internal(
        ctx,
        get_impl_path('measurement.py'),
        dut,
        image='',
        env=(f'LAGER_COMMAND_DATA={json.dumps(data)}',),
        passenv=(),
        kill=False,
        download=(),
        allow_overwrite=False,
        signum='SIGTERM',
        timeout=0,
        detach=False,
        port=(),
        org=None,
        args=(),
    )

@measure.command()
@click.pass_context
@click.argument('NETNAME')
@click.option('--mcu', required=False)
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--display', default=False, type=click.BOOL, help='Display measurement on screen')
@click.option('--cursor', default=False, type=click.BOOL, help='Enable measurement cursor')
def dc_pos(ctx, netname, mcu, gateway, dut, display, cursor):
    """
    Measure positive duty cycle
    """    
    gateway = gateway or dut
    if gateway is None:
        gateway = get_default_gateway(ctx)

    data = {
        'action': 'measure_dc_pos',
        'mcu': mcu,
        'params': {
            'netname': netname,
            'display': display,
            'cursor': cursor            
        }
    }

    run_python_internal(
        ctx,
        get_impl_path('measurement.py'),
        dut,
        image='',
        env=(f'LAGER_COMMAND_DATA={json.dumps(data)}',),
        passenv=(),
        kill=False,
        download=(),
        allow_overwrite=False,
        signum='SIGTERM',
        timeout=0,
        detach=False,
        port=(),
        org=None,
        args=(),
    )

@measure.command()
@click.pass_context
@click.argument('NETNAME')
@click.option('--mcu', required=False)
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--display', default=False, type=click.BOOL, help='Display measurement on screen')
@click.option('--cursor', default=False, type=click.BOOL, help='Enable measurement cursor')
def dc_neg(ctx, netname, mcu, gateway, dut, display, cursor):
    """
    Measure negative duty cycle
    """    
    gateway = gateway or dut
    if gateway is None:
        gateway = get_default_gateway(ctx)

    data = {
        'action': 'measure_dc_neg',
        'mcu': mcu,
        'params': {
            'netname': netname,
            'display': display,
            'cursor': cursor            
        }
    }

    run_python_internal(
        ctx,
        get_impl_path('measurement.py'),
        dut,
        image='',
        env=(f'LAGER_COMMAND_DATA={json.dumps(data)}',),
        passenv=(),
        kill=False,
        download=(),
        allow_overwrite=False,
        signum='SIGTERM',
        timeout=0,
        detach=False,
        port=(),
        org=None,
        args=(),
    )

@measure.command()
@click.pass_context
@click.argument('NETNAME')
@click.option('--mcu', required=False)
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--display', default=False, type=click.BOOL, help='Display measurement on screen')
@click.option('--cursor', default=False, type=click.BOOL, help='Enable measurement cursor')
def pw_pos(ctx, netname, mcu, gateway, dut, display, cursor):
    """
    Measure positive pulse width
    """    
    gateway = gateway or dut
    if gateway is None:
        gateway = get_default_gateway(ctx)

    data = {
        'action': 'measure_pw_pos',
        'mcu': mcu,
        'params': {
            'netname': netname,
            'display': display,
            'cursor': cursor            
        }
    }

    run_python_internal(
        ctx,
        get_impl_path('measurement.py'),
        dut,
        image='',
        env=(f'LAGER_COMMAND_DATA={json.dumps(data)}',),
        passenv=(),
        kill=False,
        download=(),
        allow_overwrite=False,
        signum='SIGTERM',
        timeout=0,
        detach=False,
        port=(),
        org=None,
        args=(),
    )

@measure.command()
@click.pass_context
@click.argument('NETNAME')
@click.option('--mcu', required=False)
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--display', default=False, type=click.BOOL, help='Display measurement on screen')
@click.option('--cursor', default=False, type=click.BOOL, help='Enable measurement cursor')
def pw_neg(ctx, netname, mcu, gateway, dut, display, cursor):
    """
    Measure negative pulse width
    """    
    gateway = gateway or dut
    if gateway is None:
        gateway = get_default_gateway(ctx)

    data = {
        'action': 'measure_dc_pos',
        'mcu': mcu,
        'params': {
            'netname': netname,
            'display': display,
            'cursor': cursor            
        }
    }

    run_python_internal(
        ctx,
        get_impl_path('measurement.py'),
        dut,
        image='',
        env=(f'LAGER_COMMAND_DATA={json.dumps(data)}',),
        passenv=(),
        kill=False,
        download=(),
        allow_overwrite=False,
        signum='SIGTERM',
        timeout=0,
        detach=False,
        port=(),
        org=None,
        args=(),
    )


@net.group()
def trigger():
    """
        Set up trigger properties for analog and logic nets
    """    
    pass


MODE_CHOICES = click.Choice(('normal', 'auto', 'single'))
COUPLING_CHOICES = click.Choice(('dc', 'ac', 'low_freq_rej', 'high_freq_rej'))

@trigger.command()
@click.pass_context
@click.argument('NETNAME')
@click.option('--mcu', required=False)
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--mode', default='normal', type=MODE_CHOICES, help='Trigger mode', show_default=True)
@click.option('--coupling', default='dc', type=COUPLING_CHOICES, help='Coupling mode', show_default=True)
@click.option('--source', required=False, help='Trigger source', metavar='NET')
@click.option('--slope', type=click.Choice(('rising', 'falling', 'both')), help='Trigger slope')
@click.option('--level', type=click.FLOAT, help='Trigger level')
def edge(ctx, netname, mcu, gateway, dut, mode, coupling, source, slope, level):
    """
    Set edge trigger
    """
    gateway = gateway or dut
    if gateway is None:
        gateway = get_default_gateway(ctx)

    data = {
        'action': 'trigger_edge',
        'mcu': mcu,
        'params': {
            'netname': netname,
            'mode': mode,
            'coupling': coupling,
            'source': source,
            'slope': slope,
            'level': level,
        }
    }

    run_python_internal(
        ctx,
        get_impl_path('trigger.py'),
        dut,
        image='',
        env=(f'LAGER_COMMAND_DATA={json.dumps(data)}',),
        passenv=(),
        kill=False,
        download=(),
        allow_overwrite=False,
        signum='SIGTERM',
        timeout=0,
        detach=False,
        port=(),
        org=None,
        args=(),
    )


@trigger.command()
@click.pass_context
@click.argument('NETNAME')
@click.option('--mcu', required=False)
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--mode', default='normal', type=MODE_CHOICES, help='Trigger mode', show_default=True)
@click.option('--coupling', default='dc', type=COUPLING_CHOICES, help='Coupling mode', show_default=True)
@click.option('--source', required=False, help='Trigger source', metavar='NET')
@click.option('--level', type=click.FLOAT, help='Trigger level')
@click.option('--trigger-on', type=click.Choice(('gt', 'lt', 'gtlt')), help='Trigger on')
@click.option('--upper', type=click.FLOAT, help='upper width')
@click.option('--lower', type=click.FLOAT, help='lower width')
def pulse(ctx, netname, mcu, gateway, dut, mode, coupling, source, level, trigger_on, upper, lower):
    """
    Set pulse trigger
    """

    gateway = gateway or dut
    if gateway is None:
        gateway = get_default_gateway(ctx)

    data = {
        'action': 'trigger_pulse',
        'mcu': mcu,
        'params': {
            'netname': netname,
            'mode': mode,
            'coupling': coupling,
            'source': source,
            'level': level,
            'trigger_on': trigger_on,
            'upper': upper,
            'lower': lower,
        }
    }

    run_python_internal(
        ctx,
        get_impl_path('trigger.py'),
        dut,
        image='',
        env=(f'LAGER_COMMAND_DATA={json.dumps(data)}',),
        passenv=(),
        kill=False,
        download=(),
        allow_overwrite=False,
        signum='SIGTERM',
        timeout=0,
        detach=False,
        port=(),
        org=None,
        args=(),
    )    

@trigger.command()
@click.pass_context
@click.argument('NETNAME')
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--mcu', required=False)
@click.option('--mode', default='normal', type=MODE_CHOICES, help='Trigger mode, e.g. Normal, Automatic, or Single Shot', show_default=True)
@click.option('--coupling', default='dc', type=COUPLING_CHOICES, help='Coupling mode', show_default=True)
@click.option('--source-scl', required=False, help='Trigger source', metavar='NET')
@click.option('--source-sda', required=False, help='Trigger source', metavar='NET')
@click.option('--level-scl', type=click.FLOAT, help='Trigger scl level')
@click.option('--level-sda', type=click.FLOAT, help='Trigger sda level')
@click.option('--trigger-on', type=click.Choice(('start', 'restart', 'stop', 'nack', 'address', 'data', 'addr_data')), help='Trigger on')
@click.option('--address', type=click.INT, help='Address value to trigger on in ADDRESS mode')
@click.option('--addr-width', type=click.Choice(('7', '8', '9', '10')), help='Address width in bits')
@click.option('--data', type=click.INT, help='Data value to trigger on in DATA mode')
@click.option('--data-width', type=click.Choice(('1', '2', '3', '4', '5')), help='Data width in bytes')
@click.option('--direction', type=click.Choice(('write', 'read', 'rw')), help='Direction to trigger on')
def i2c(ctx, netname, gateway, dut, mcu, mode, coupling, source_scl, level_scl, source_sda, level_sda, trigger_on, address, addr_width, data, data_width, direction):
    """
    Set I2C trigger
    """
    if addr_width !=None:
        addr_width = int(addr_width)
    if data_width !=None:
        data_width = int(data_width)
    gateway = gateway or dut
    if gateway is None:
        gateway = get_default_gateway(ctx)

    data = {
        'action': 'trigger_i2c',
        'mcu': mcu,
        'params': {
            'netname': netname,
            'mode': mode,
            'coupling': coupling,
            'source_scl': source_scl,
            'source_sda': source_sda,
            'level_scl': level_scl,
            'level_sda': level_sda,
            'trigger_on': trigger_on,
            'address': address,
            'addr_width': addr_width,
            'data': data,
            'data_width': data_width,
            'direction': direction
        }
    }

    run_python_internal(
        ctx,
        get_impl_path('trigger.py'),
        dut,
        image='',
        env=(f'LAGER_COMMAND_DATA={json.dumps(data)}',),
        passenv=(),
        kill=False,
        download=(),
        allow_overwrite=False,
        signum='SIGTERM',
        timeout=0,
        detach=False,
        port=(),
        org=None,
        args=(),
    )    

@trigger.command()
@click.pass_context
@click.argument('NETNAME')
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--mcu', required=False)
@click.option('--mode', default='normal', type=MODE_CHOICES, help='Trigger mode, e.g. Normal, Automatic, or Single Shot', show_default=True)
@click.option('--coupling', default='dc', type=COUPLING_CHOICES, help='Coupling mode', show_default=True)
@click.option('--source', required=False, help='Trigger source', metavar='NET')
@click.option('--level', type=click.FLOAT, help='Trigger level')
@click.option('--trigger-on', type=click.Choice(('start', 'error', 'cerror', 'data')), help='Trigger on')
@click.option('--parity', type=click.Choice(('even', 'odd', 'none')), help='Data trigger parity')
@click.option('--stop-bits', type=click.Choice(('1', '1.5', '2')), help='Data trigger stop bits')
@click.option('--baud', type=click.INT, help='Data trigger baud')
@click.option('--data-width', type=click.INT, help='Data trigger data width in bits')
@click.option('--data', type=click.INT, help='Data trigger data')
def uart(ctx, netname, gateway, dut, mcu, mode, coupling, source, level, trigger_on, parity, stop_bits, baud, data_width, data):
    """
    Set UART trigger
    """
    if stop_bits !=None:
        stop_bits = float(stop_bits)
    gateway = gateway or dut
    if gateway is None:
        gateway = get_default_gateway(ctx)

    data = {
        'action': 'trigger_uart',
        'mcu': mcu,
        'params': {
            'netname': netname,
            'mode': mode,
            'coupling': coupling,
            'source': source,
            'level': level,
            'trigger_on': trigger_on,
            'parity': parity,
            'stop_bits': stop_bits,
            'baud': baud,
            'data_width': data_width,
            'data': data,
        }
    }

    run_python_internal(
        ctx,
        get_impl_path('trigger.py'),
        dut,
        image='',
        env=(f'LAGER_COMMAND_DATA={json.dumps(data)}',),
        passenv=(),
        kill=False,
        download=(),
        allow_overwrite=False,
        signum='SIGTERM',
        timeout=0,
        detach=False,
        port=(),
        org=None,
        args=(),
    )

@trigger.command()
@click.pass_context
@click.argument('NETNAME')
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--mcu', required=False)
@click.option('--mode', default='normal', type=MODE_CHOICES, help='Trigger mode, e.g. Normal, Automatic, or Single Shot', show_default=True)
@click.option('--coupling', default='dc', type=COUPLING_CHOICES, help='Coupling mode', show_default=True)
@click.option('--source-mosi-miso', required=False, help='Trigger master/slave data source', metavar='NET')
@click.option('--source-sck', required=False, help='Trigger clock source', metavar='NET')
@click.option('--source-cs', required=False, help='Trigger chip select source', metavar='NET')
@click.option('--level-mosi-miso', type=click.FLOAT, help='Trigger mosi/miso level')
@click.option('--level-sck', type=click.FLOAT, help='Trigger sck level')
@click.option('--level-cs', type=click.FLOAT, help='Trigger cs level')
@click.option('--data', type=click.INT, help='Trigger data value')
@click.option('--data-width', type=click.INT, help='Data width in bits')
@click.option('--clk-slope', type=click.Choice(('positive', 'negative')), help='Slope of clock edge to sample data')
@click.option('--trigger-on', type=click.Choice(('timeout', 'cs')), help='Trigger on')
@click.option('--cs-idle', type=click.Choice(('high', 'low')), help='CS Idle type')
@click.option('--timeout', type=click.FLOAT, help='Timeout length')
def spi(ctx, netname, gateway, dut, mcu, mode, coupling, source_mosi_miso, source_sck, source_cs, level_mosi_miso, level_sck, level_cs, data, data_width, clk_slope, trigger_on, cs_idle, timeout):
    """
    Set SPI trigger
    """
    gateway = gateway or dut
    if gateway is None:
        gateway = get_default_gateway(ctx)

    data = {
        'action': 'trigger_spi',
        'mcu': mcu,
        'params': {
            'netname': netname,
            'mode': mode,
            'coupling': coupling,
            'source_mosi_miso': source_mosi_miso,
            'source_sck': source_sck,
            'source_cs': source_cs,
            'level_mosi_miso': level_mosi_miso,
            'level_sck': level_sck,
            'level_cs': level_cs,
            'data': data,
            'data_width': data_width,
            'clk_slope': clk_slope,
            'trigger_on': trigger_on,            
            'cs_idle': cs_idle,
            'timeout': timeout
        }
    }

    run_python_internal(
        ctx,
        get_impl_path('trigger.py'),
        dut,
        image='',
        env=(f'LAGER_COMMAND_DATA={json.dumps(data)}',),
        passenv=(),
        kill=False,
        download=(),
        allow_overwrite=False,
        signum='SIGTERM',
        timeout=0,
        detach=False,
        port=(),
        org=None,
        args=(),
    ) 

@net.group()
def cursor():
    """
        Move scope cursor on a given net
    """    
    pass

@cursor.command()
@click.pass_context
@click.argument('NETNAME')
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--mcu', required=False)
@click.option('--x', required=False, type=click.FLOAT, help='cursor a x coordinate')
@click.option('--y', required=False, type=click.FLOAT, help='cursor a y coordinate')
def set_a(ctx, netname, gateway, dut, mcu, x, y):
    """
        Set cursor a's x position
    """    
    gateway = gateway or dut
    if gateway is None:
        gateway = get_default_gateway(ctx)

    data = {
        'action': 'set_a',
        'mcu': mcu,
        'params': {
            'netname': netname,
            'x': x,
            'y': y,
        }
    }

    run_python_internal(
        ctx,
        get_impl_path('cursor.py'),
        dut,
        image='',
        env=(f'LAGER_COMMAND_DATA={json.dumps(data)}',),
        passenv=(),
        kill=False,
        download=(),
        allow_overwrite=False,
        signum='SIGTERM',
        timeout=0,
        detach=False,
        port=(),
        org=None,
        args=(),
    )

@cursor.command()
@click.pass_context
@click.argument('NETNAME')
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--mcu', required=False)
@click.option('--x', required=False, type=click.FLOAT, help='cursor b x coordinate')
@click.option('--y', required=False, type=click.FLOAT, help='cursor b y coordinate')
def set_b(ctx, netname, gateway, dut, mcu, x, y):
    """
        Set cursor b's x position
    """    
    gateway = gateway or dut
    if gateway is None:
        gateway = get_default_gateway(ctx)

    data = {
        'action': 'set_b',
        'mcu': mcu,
        'params': {
            'netname': netname,
            'x': x,
            'y': y,
        }
    }

    run_python_internal(
        ctx,
        get_impl_path('cursor.py'),
        dut,
        image='',
        env=(f'LAGER_COMMAND_DATA={json.dumps(data)}',),
        passenv=(),
        kill=False,
        download=(),
        allow_overwrite=False,
        signum='SIGTERM',
        timeout=0,
        detach=False,
        port=(),
        org=None,
        args=(),
    )

@cursor.command()
@click.pass_context
@click.argument('NETNAME')
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--mcu', required=False)
@click.option('--del-x', required=False, type=click.FLOAT, help='shift a\'s x coordinate')
@click.option('--del-y', required=False, type=click.FLOAT, help='shift a\'s y coordinate')
def move_a(ctx, netname, gateway, dut, mcu, del_x, del_y):
    """
        Shift cursor a's  position
    """    
    gateway = gateway or dut
    if gateway is None:
        gateway = get_default_gateway(ctx)

    data = {
        'action': 'move_a',
        'mcu': mcu,
        'params': {
            'netname': netname,
            'del_x': del_x,
            'del_y': del_y,
        }
    }

    run_python_internal(
        ctx,
        get_impl_path('cursor.py'),
        dut,
        image='',
        env=(f'LAGER_COMMAND_DATA={json.dumps(data)}',),
        passenv=(),
        kill=False,
        download=(),
        allow_overwrite=False,
        signum='SIGTERM',
        timeout=0,
        detach=False,
        port=(),
        org=None,
        args=(),
    )

@cursor.command()
@click.pass_context
@click.argument('NETNAME')
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--mcu', required=False)
@click.option('--del-x', required=False, type=click.FLOAT, help='shift b\'s x coordinate')
@click.option('--del-y', required=False, type=click.FLOAT, help='shift b\'s y coordinate')
def move_b(ctx, netname, gateway, dut, mcu, del_x, del_y):
    """
        Shift cursor b's position
    """    
    gateway = gateway or dut
    if gateway is None:
        gateway = get_default_gateway(ctx)

    data = {
        'action': 'move_b',
        'mcu': mcu,
        'params': {
            'netname': netname,
            'del_x': del_x,
            'del_y': del_y,
        }
    }

    run_python_internal(
        ctx,
        get_impl_path('cursor.py'),
        dut,
        image='',
        env=(f'LAGER_COMMAND_DATA={json.dumps(data)}',),
        passenv=(),
        kill=False,
        download=(),
        allow_overwrite=False,
        signum='SIGTERM',
        timeout=0,
        detach=False,
        port=(),
        org=None,
        args=(),
    )


@net.group()
def bus():
    """
        Decode communication busses
    """    
    pass


@bus.command()
@click.pass_context
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--mcu', required=False)
@click.option('--source-tx', required=True, help='UART Bus TX signal', metavar='NET')
@click.option('--source-rx', required=True, help='UART Bus RX signal', metavar='NET')
@click.option('--level-tx', required=False, type=click.FLOAT, help='tx signal threshold level')
@click.option('--level-rx', required=False, type=click.FLOAT, help='rx signal threshold level')
@click.option('--parity', required=False, type=click.Choice(('even', 'odd', 'none')), help='Bus parity')
@click.option('--stop-bits', required=False, type=click.Choice(('1', '1.5', '2')), help='Bus stop bits')
@click.option('--data-bits', required=False, type=click.Choice(('5', '6', '7','8','9')), help='Bus stop bits')
@click.option('--baud', required=False, type=click.INT, help='Bus baud')
@click.option('--polarity', required=False, type=click.Choice(('pos', 'neg')), help='Bus polarity. Typical is negative')
@click.option('--endianness', required=False, type=click.Choice(('msb', 'lsb')), help='Bus endianness')
@click.option('--packet-ending', required=False, type=click.Choice(('null', 'cr', 'lf', 'sp', 'none')), help='Packet Ending of data')
@click.option('--disable', is_flag=True)
def uart(ctx, gateway, dut, mcu, source_tx, source_rx, level_tx, level_rx, parity, stop_bits, data_bits, baud, polarity, endianness, packet_ending, disable):
    """
        Enable UART Bus Decoding
    """    
    gateway = gateway or dut
    if gateway is None:
        gateway = get_default_gateway(ctx)
    if stop_bits != None:
        stop_bits = float(stop_bits)

    if data_bits != None:
        data_bits = int(data_bits)
    data = {
        'action': 'bus_uart',
        'mcu': mcu,
        'params': {
            'source_tx': source_tx,
            'source_rx': source_rx,
            'level_tx': level_tx,
            'level_rx': level_rx,
            'parity': parity,
            'stop_bits': stop_bits,
            'data_bits': data_bits,
            'baud': baud,
            'polarity': polarity,
            'endianness': endianness,
            'packet_ending': packet_ending,
            'disable': disable
        }
    }

    run_python_internal(
        ctx,
        get_impl_path('bus.py'),
        dut,
        image='',
        env=(f'LAGER_COMMAND_DATA={json.dumps(data)}',),
        passenv=(),
        kill=False,
        download=(),
        allow_overwrite=False,
        signum='SIGTERM',
        timeout=0,
        detach=False,
        port=(),
        org=None,
        args=(),
    )

@bus.command()
@click.pass_context
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--mcu', required=False)
@click.option('--source-scl', required=True, help='I2C Bus SCL signal', metavar='NET')
@click.option('--source-sda', required=True, help='I2C Bus SDA signal', metavar='NET')
@click.option('--level-scl', required=False, type=click.FLOAT, help='scl signal threshold level')
@click.option('--level-sda', required=False, type=click.FLOAT, help='sda signal threshold level')
@click.option('--rw', required=False, type=click.Choice(('on', 'off')), help='Decode RW bit')
@click.option('--disable', is_flag=True)
def i2c(ctx, gateway, dut, mcu, source_scl, source_sda, level_scl, level_sda, rw, disable):
    """
        Enable I2C Bus Decoding
    """    
    gateway = gateway or dut
    if gateway is None:
        gateway = get_default_gateway(ctx)

    data = {
        'action': 'bus_i2c',
        'mcu': mcu,
        'params': {
            'source_scl': source_scl,
            'source_sda': source_sda,
            'level_scl': level_scl,
            'level_sda': level_sda,
            'rw': rw,
            'disable': disable
        }
    }

    run_python_internal(
        ctx,
        get_impl_path('bus.py'),
        dut,
        image='',
        env=(f'LAGER_COMMAND_DATA={json.dumps(data)}',),
        passenv=(),
        kill=False,
        download=(),
        allow_overwrite=False,
        signum='SIGTERM',
        timeout=0,
        detach=False,
        port=(),
        org=None,
        args=(),
    )

@bus.command()
@click.pass_context
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--mcu', required=False)
@click.option('--source-mosi', required=True, help='SPI Bus MOSI signal', metavar='NET')
@click.option('--source-miso', required=True, help='SPI Bus MISO signal', metavar='NET')
@click.option('--source-sck', required=True, help='SPI Bus SCK signal', metavar='NET')
@click.option('--source-cs', required=False, help='SPI Bus CS signal', metavar='NET')
@click.option('--level-mosi', required=False, type=click.FLOAT, help='MOSI signal threshold level')
@click.option('--level-miso', required=False, type=click.FLOAT, help='MISO signal threshold level')
@click.option('--level-sck', required=False, type=click.FLOAT, help='SCK signal threshold level')
@click.option('--level-cs', required=False, type=click.FLOAT, help='CS signal threshold level')
@click.option('--pol-mosi', required=False, type=click.Choice(('pos', 'neg')), help='MOSI signal polarity')
@click.option('--pol-miso', required=False, type=click.Choice(('pos', 'neg')), help='MISO signal polarity')
@click.option('--pol-cs', required=False, type=click.Choice(('pos', 'neg')), help='CS signal polarity')
@click.option('--pha-sck', required=False, type=click.Choice(('rising', 'falling')), help='SCK edge to sample data on')
@click.option('--capture', required=False, type=click.Choice(('timeout', 'cs')), help='Mode to capture bus data')
@click.option('--timeout', required=False, type=click.FLOAT, help='Timeout value')
@click.option('--endianness', required=False, type=click.Choice(('msb', 'lsb')), help='Endianness of data')
@click.option('--data-width', required=False, type=click.INT, help='Width in bits of data')
@click.option('--disable', is_flag=True)
def spi(ctx, gateway, dut, mcu, source_mosi, source_miso, source_sck, source_cs, level_mosi, level_miso, level_sck, level_cs, pol_mosi, pol_miso, pol_cs, pha_sck, capture, timeout, endianness, data_width, disable):
    """
        Enable SPI Bus Decoding
    """    
    gateway = gateway or dut
    if gateway is None:
        gateway = get_default_gateway(ctx)

    data = {
        'action': 'bus_spi',
        'mcu': mcu,
        'params': {
            'source_mosi': source_mosi,
            'source_miso': source_miso,
            'source_sck': source_sck,
            'source_cs': source_cs,            
            'level_mosi': level_mosi,
            'level_miso': level_miso,
            'level_mosi': level_mosi,
            'level_miso': level_miso,
            'level_sck': level_sck,
            'level_cs': level_cs,                        
            'pol_mosi': pol_mosi,
            'pol_miso': pol_miso,
            'pol_cs': pol_cs,
            'pha_sck': pha_sck,
            'capture': capture,
            'timeout': timeout,
            'endianness': endianness,
            'data_width': data_width,
            'disable': disable
        }
    }

    run_python_internal(
        ctx,
        get_impl_path('bus.py'),
        dut,
        image='',
        env=(f'LAGER_COMMAND_DATA={json.dumps(data)}',),
        passenv=(),
        kill=False,
        download=(),
        allow_overwrite=False,
        signum='SIGTERM',
        timeout=0,
        detach=False,
        port=(),
        org=None,
        args=(),
    )

@bus.command()
@click.pass_context
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--mcu', required=False)
@click.option('--source', required=True, help='CAN Bus signal', metavar='NET')
@click.option('--level', required=False, type=click.FLOAT, help='signal threshold level')
@click.option('--baud', required=False, type=click.INT, help='Bus BAUD ratae')
@click.option('--signal-type', required=False, type=click.Choice(('tx', 'rx', 'can_h', 'can_l', 'diff')), help='Signal type of source data. e.g tx transceiver, raw CAN high signal, raw CAN low signal, raw differential signal')
@click.option('--disable', is_flag=True)
def can(ctx, gateway, dut, mcu, source, level, baud, signal_type, disable):
    """
        Enable CAN Bus Decoding
    """    
    gateway = gateway or dut
    if gateway is None:
        gateway = get_default_gateway(ctx)

    data = {
        'action': 'bus_can',
        'mcu': mcu,
        'params': {
            'source': source,
            'level': level,
            'baud': baud,
            'signal_type': signal_type,
            'disable': disable
        }
    }

    run_python_internal(
        ctx,
        get_impl_path('bus.py'),
        dut,
        image='',
        env=(f'LAGER_COMMAND_DATA={json.dumps(data)}',),
        passenv=(),
        kill=False,
        download=(),
        allow_overwrite=False,
        signum='SIGTERM',
        timeout=0,
        detach=False,
        port=(),
        org=None,
        args=(),
    )



@net.group()
@click.argument('NETNAME')
@click.pass_context
def battery(ctx, netname):
    """
        Control battery nets
    """    
    ctx.obj.netname = netname

@battery.command()
@click.argument('MODE_TYPE', required=False, type=click.Choice(('static', 'dynamic')))
@click.pass_context
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--mcu', required=False)
def mode(ctx, gateway, dut, mcu, mode_type):
    """
        Set battery simulation mode type
    """    
    gateway = gateway or dut
    if gateway is None:
        gateway = get_default_gateway(ctx)
    netname = ctx.obj.netname
    data = {
        'action': 'set_mode',
        'mcu': mcu,
        'params': {
            'netname': netname,
            'mode_type': mode_type,
        }
    }

    run_python_internal(
        ctx,
        get_impl_path('battery.py'),
        dut,
        image='',
        env=(f'LAGER_COMMAND_DATA={json.dumps(data)}',),
        passenv=(),
        kill=False,
        download=(),
        allow_overwrite=False,
        signum='SIGTERM',
        timeout=0,
        detach=False,
        port=(),
        org=None,
        args=(),
    )

@battery.command()
@click.argument('VALUE', required=False, type=click.FLOAT)
@click.pass_context
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--mcu', required=False)
def soc(ctx, gateway, dut, mcu, value):
    """
        Set battery state of charge in %
    """   
    gateway = gateway or dut
    if gateway is None:
        gateway = get_default_gateway(ctx)
    netname = ctx.obj.netname
    data = {
        'action': 'set_soc',
        'mcu': mcu,
        'params': {
            'netname': netname,
            'value': value,
        }
    }

    run_python_internal(
        ctx,
        get_impl_path('battery.py'),
        dut,
        image='',
        env=(f'LAGER_COMMAND_DATA={json.dumps(data)}',),
        passenv=(),
        kill=False,
        download=(),
        allow_overwrite=False,
        signum='SIGTERM',
        timeout=0,
        detach=False,
        port=(),
        org=None,
        args=(),
    )

@battery.command()
@click.argument('VALUE', required=False, type=click.FLOAT)
@click.pass_context
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--mcu', required=False)
def voc(ctx, gateway, dut, mcu, value):
    """
        Set battery open circuit voltage in Volts
    """    
    gateway = gateway or dut
    if gateway is None:
        gateway = get_default_gateway(ctx)
    netname = ctx.obj.netname
    data = {
        'action': 'set_voc',
        'mcu': mcu,
        'params': {
            'netname': netname,
            'value': value,
        }
    }

    run_python_internal(
        ctx,
        get_impl_path('battery.py'),
        dut,
        image='',
        env=(f'LAGER_COMMAND_DATA={json.dumps(data)}',),
        passenv=(),
        kill=False,
        download=(),
        allow_overwrite=False,
        signum='SIGTERM',
        timeout=0,
        detach=False,
        port=(),
        org=None,
        args=(),
    )

@battery.command()
@click.argument('VALUE', required=False, type=click.FLOAT)
@click.pass_context
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--mcu', required=False)
def batt_full(ctx, gateway, dut, mcu, value):
    """
        Set battery fully charged voltage in Volts
    """    
    gateway = gateway or dut
    if gateway is None:
        gateway = get_default_gateway(ctx)
    netname = ctx.obj.netname
    data = {
        'action': 'set_volt_full',
        'mcu': mcu,
        'params': {
            'netname': netname,
            'value': value,
        }
    }

    run_python_internal(
        ctx,
        get_impl_path('battery.py'),
        dut,
        image='',
        env=(f'LAGER_COMMAND_DATA={json.dumps(data)}',),
        passenv=(),
        kill=False,
        download=(),
        allow_overwrite=False,
        signum='SIGTERM',
        timeout=0,
        detach=False,
        port=(),
        org=None,
        args=(),
    )

@battery.command()
@click.argument('VALUE', required=False, type=click.FLOAT)
@click.pass_context
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--mcu', required=False)
def batt_empty(ctx, gateway, dut, mcu, value):
    """
        Set battery fully discharged voltage in Volts
    """      
    gateway = gateway or dut
    if gateway is None:
        gateway = get_default_gateway(ctx)
    netname = ctx.obj.netname
    data = {
        'action': 'set_volt_empty',
        'mcu': mcu,
        'params': {
            'netname': netname,
            'value': value,
        }
    }

    run_python_internal(
        ctx,
        get_impl_path('battery.py'),
        dut,
        image='',
        env=(f'LAGER_COMMAND_DATA={json.dumps(data)}',),
        passenv=(),
        kill=False,
        download=(),
        allow_overwrite=False,
        signum='SIGTERM',
        timeout=0,
        detach=False,
        port=(),
        org=None,
        args=(),
    )

@battery.command()
@click.argument('VALUE', required=False, type=click.FLOAT)
@click.pass_context
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--mcu', required=False)
def capacity(ctx, gateway, dut, mcu, value):
    """
        Set battery capacity limit in Amps-hours
    """      
    gateway = gateway or dut
    if gateway is None:
        gateway = get_default_gateway(ctx)
    netname = ctx.obj.netname
    data = {
        'action': 'set_capacity',
        'mcu': mcu,
        'params': {
            'netname': netname,
            'value': value,
        }
    }

    run_python_internal(
        ctx,
        get_impl_path('battery.py'),
        dut,
        image='',
        env=(f'LAGER_COMMAND_DATA={json.dumps(data)}',),
        passenv=(),
        kill=False,
        download=(),
        allow_overwrite=False,
        signum='SIGTERM',
        timeout=0,
        detach=False,
        port=(),
        org=None,
        args=(),
    )

@battery.command()
@click.argument('VALUE', required=False, type=click.FLOAT)
@click.pass_context
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--mcu', required=False)
def current_limit(ctx, gateway, dut, mcu, value):
    """
        Set maximum charge/discharge current in Amps
    """       
    gateway = gateway or dut
    if gateway is None:
        gateway = get_default_gateway(ctx)
    netname = ctx.obj.netname
    data = {
        'action': 'set_current_limit',
        'mcu': mcu,
        'params': {
            'netname': netname,
            'value': value,
        }
    }

    run_python_internal(
        ctx,
        get_impl_path('battery.py'),
        dut,
        image='',
        env=(f'LAGER_COMMAND_DATA={json.dumps(data)}',),
        passenv=(),
        kill=False,
        download=(),
        allow_overwrite=False,
        signum='SIGTERM',
        timeout=0,
        detach=False,
        port=(),
        org=None,
        args=(),
    )

@battery.command()
@click.argument('VALUE', required=False, type=click.FLOAT)
@click.pass_context
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--mcu', required=False)
def ovp(ctx, gateway, dut, mcu, value):
    """
        Set over voltage protection limit in Volts
    """   
    gateway = gateway or dut
    if gateway is None:
        gateway = get_default_gateway(ctx)
    netname = ctx.obj.netname
    data = {
        'action': 'set_ovp',
        'mcu': mcu,
        'params': {
            'netname': netname,
            'value': value,
        }
    }

    run_python_internal(
        ctx,
        get_impl_path('battery.py'),
        dut,
        image='',
        env=(f'LAGER_COMMAND_DATA={json.dumps(data)}',),
        passenv=(),
        kill=False,
        download=(),
        allow_overwrite=False,
        signum='SIGTERM',
        timeout=0,
        detach=False,
        port=(),
        org=None,
        args=(),
    )

@battery.command()
@click.argument('VALUE', required=False, type=click.FLOAT)
@click.pass_context
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--mcu', required=False)
def ocp(ctx, gateway, dut, mcu, value):
    """
        Set over current protection limit in Amps
    """     
    gateway = gateway or dut
    if gateway is None:
        gateway = get_default_gateway(ctx)
    netname = ctx.obj.netname
    data = {
        'action': 'set_ocp',
        'mcu': mcu,
        'params': {
            'netname': netname,
            'value': value,
        }
    }

    run_python_internal(
        ctx,
        get_impl_path('battery.py'),
        dut,
        image='',
        env=(f'LAGER_COMMAND_DATA={json.dumps(data)}',),
        passenv=(),
        kill=False,
        download=(),
        allow_overwrite=False,
        signum='SIGTERM',
        timeout=0,
        detach=False,
        port=(),
        org=None,
        args=(),
    )    

@battery.command()
@click.pass_context
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--mcu', required=False)
def state(ctx, gateway, dut, mcu):
    """
        Get Battery State
    """    
    gateway = gateway or dut
    if gateway is None:
        gateway = get_default_gateway(ctx)
    netname = ctx.obj.netname
    data = {
        'action': 'state',
        'mcu': mcu,
        'params': {
            'netname': netname,
        }
    }

    run_python_internal(
        ctx,
        get_impl_path('battery.py'),
        dut,
        image='',
        env=(f'LAGER_COMMAND_DATA={json.dumps(data)}',),
        passenv=(),
        kill=False,
        download=(),
        allow_overwrite=False,
        signum='SIGTERM',
        timeout=0,
        detach=False,
        port=(),
        org=None,
        args=(),
    ) 

@battery.command()
@click.pass_context
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--mcu', required=False)
def enable(ctx, gateway, dut, mcu):
    """
        Enable Battery
    """    
    gateway = gateway or dut
    if gateway is None:
        gateway = get_default_gateway(ctx)
    netname = ctx.obj.netname
    data = {
        'action': 'enable_battery',
        'mcu': mcu,
        'params': {
            'netname': netname,
        }
    }

    run_python_internal(
        ctx,
        get_impl_path('battery.py'),
        dut,
        image='',
        env=(f'LAGER_COMMAND_DATA={json.dumps(data)}',),
        passenv=(),
        kill=False,
        download=(),
        allow_overwrite=False,
        signum='SIGTERM',
        timeout=0,
        detach=False,
        port=(),
        org=None,
        args=(),
    ) 

@battery.command()
@click.pass_context
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--mcu', required=False)
def disable(ctx, gateway, dut, mcu):
    """
        Disable Battery
    """    
    gateway = gateway or dut
    if gateway is None:
        gateway = get_default_gateway(ctx)
    netname = ctx.obj.netname
    data = {
        'action': 'disable_battery',
        'mcu': mcu,
        'params': {
            'netname': netname,
        }
    }

    run_python_internal(
        ctx,
        get_impl_path('battery.py'),
        dut,
        image='',
        env=(f'LAGER_COMMAND_DATA={json.dumps(data)}',),
        passenv=(),
        kill=False,
        download=(),
        allow_overwrite=False,
        signum='SIGTERM',
        timeout=0,
        detach=False,
        port=(),
        org=None,
        args=(),
    )

@net.group()
@click.argument('NETNAME')
@click.pass_context
def supply(ctx, netname):
    """
        Control power supply nets
    """    
    ctx.obj.netname = netname



@supply.command()
@click.argument('VALUE', required=False)
@click.pass_context
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--mcu', required=False)
@click.option('--ocp', required=False, type=click.FLOAT, help='Set over current protection')
@click.option('--ovp', required=False, type=click.FLOAT, help='Set over voltage protection')
@click.option('--clear-ocp', is_flag=True, help='Clear over current condition')
@click.option('--clear-ovp', is_flag=True, help='Clear over voltage condition')
def voltage(ctx, gateway, dut, mcu, value, ocp, ovp, clear_ocp, clear_ovp):
    """
        Set voltage on net
    """    
    gateway = gateway or dut
    if gateway is None:
        gateway = get_default_gateway(ctx)

    netname = ctx.obj.netname

    if value != None:
        if value.lower() == "off":
            if click.confirm(f"Disable voltage?", default=True):
                pass
            else:
                print("Aborting")
                return
        elif value.lower() == "on":
            if click.confirm(f"Enable voltage?", default=False):
                pass
            else:
                print("Aborting")
                return                      
        else:
            try:
                float(value)
            except ValueError:
                raise ValueError(f"{value} is not a number") 

            if click.confirm(f"Set voltage to {value}V?", default=False):
                pass
            else:
                print("Aborting")
                return

    data = {
        'action': 'voltage',
        'mcu': mcu,
        'params': {
            'netname': netname,
            'value': value,
            'ocp': ocp,
            'ovp': ovp,
            'clear_ocp': clear_ocp,
            'clear_ovp': clear_ovp,
        }
    }

    run_python_internal(
        ctx,
        get_impl_path('supply.py'),
        dut,
        image='',
        env=(f'LAGER_COMMAND_DATA={json.dumps(data)}',),
        passenv=(),
        kill=False,
        download=(),
        allow_overwrite=False,
        signum='SIGTERM',
        timeout=0,
        detach=False,
        port=(),
        org=None,
        args=(),
    )

@supply.command()
@click.argument('VALUE', required=False)
@click.pass_context
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--mcu', required=False)
@click.option('--ocp', required=False, type=click.FLOAT, help='Set over current protection')
@click.option('--ovp', required=False, type=click.FLOAT, help='Set over voltage protection')
@click.option('--clear-ocp', is_flag=True, help='Clear over current condition')
@click.option('--clear-ovp', is_flag=True, help='Clear over voltage condition')
def current(ctx, gateway, dut, mcu, value, ocp, ovp, clear_ocp, clear_ovp):
    """
        Set current on net
    """    
    gateway = gateway or dut
    if gateway is None:
        gateway = get_default_gateway(ctx)

    netname = ctx.obj.netname

    if value != None:
        if value.lower() == "off":
            if click.confirm(f"Disable current?", default=True):
                pass
            else:
                print("Aborting")
                return
        elif value.lower() == "on":
            if click.confirm(f"Enable voltage?", default=False):
                pass
            else:
                print("Aborting")
                return                              
        else:
            try:
                float(value)
            except ValueError:
                raise ValueError(f"{value} is not a number") 

            if click.confirm(f"Set voltage to {value}A?", default=False):
                pass
            else:
                print("Aborting")
                return

    data = {
        'action': 'current',
        'mcu': mcu,
        'params': {
            'netname': netname,
            'value': value,
            'ocp': ocp,
            'ovp': ovp,
            'clear_ocp': clear_ocp,
            'clear_ovp': clear_ovp,        
        }
    }

    run_python_internal(
        ctx,
        get_impl_path('supply.py'),
        dut,
        image='',
        env=(f'LAGER_COMMAND_DATA={json.dumps(data)}',),
        passenv=(),
        kill=False,
        download=(),
        allow_overwrite=False,
        signum='SIGTERM',
        timeout=0,
        detach=False,
        port=(),
        org=None,
        args=(),
    )


@net.group()
@click.argument('NETNAME')
@click.pass_context
def eload(ctx, netname):
    """
        Control e-load nets
    """    
    ctx.obj.netname = netname

@eload.command()
@click.argument('VALUE', required=False, type=click.FLOAT)
@click.pass_context
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--mcu', required=False)
@click.option('--max-volt', required=False, type=click.FLOAT, help='Set max voltage')
@click.option('--max-curr', required=False, type=click.FLOAT, help='Set max current')
def resistance(ctx, gateway, dut, mcu, value, max_volt, max_curr):
    """
        Set constant resistance load
    """      
    pass

@eload.command()
@click.argument('VALUE', required=False, type=click.FLOAT)
@click.pass_context
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--mcu', required=False)
@click.option('--max-volt', required=False, type=click.FLOAT, help='Set max voltage')
@click.option('--max-curr', required=False, type=click.FLOAT, help='Set max current')
def voltage(ctx, gateway, dut, mcu, value, max_volt, max_curr):
    """
        Set constant voltage load
    """      
    pass

@eload.command()
@click.argument('VALUE', required=False, type=click.FLOAT)
@click.pass_context
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--mcu', required=False)
@click.option('--max-volt', required=False, type=click.FLOAT, help='Set max voltage')
@click.option('--max-curr', required=False, type=click.FLOAT, help='Set max current')
def current(ctx, gateway, dut, mcu, value, max_volt, max_curr):
    """
        Set constant current load
    """      
    pass

@eload.command()
@click.argument('VALUE', required=False, type=click.FLOAT)
@click.pass_context
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--mcu', required=False)
@click.option('--max-volt', required=False, type=click.FLOAT, help='Set max voltage')
@click.option('--max-curr', required=False, type=click.FLOAT, help='Set max current')
def current(ctx, gateway, dut, mcu, value, max_volt, max_curr):
    """
        Set constant power load
    """      
    pass


# @net.command()
# @click.pass_context
# @click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
# @click.option('--dut', required=False, help='ID of DUT')
# @click.option('--mcu', required=False)
# @click.option('--max-settings', is_flag=True, default=False)
# @click.option('--voltage')
# @click.option('--resistance')
# @click.option('--current')
# @click.option('--power')
# @click.argument('NETNAME')
# def eload(ctx, gateway, dut, mcu, max_settings, voltage, resistance, current, power, netname):
#     """
#         Control the electronic load
#     """
#     gateway = gateway or dut
#     if gateway is None:
#         gateway = get_default_gateway(ctx)

#     session = ctx.obj.session

#     data = {
#         'action': 'eload',
#         'mcu': mcu,
#         'params': {
#             'max_settings': max_settings,
#             'voltage': voltage,
#             'resistance': resistance,
#             'current': current,
#             'power': power,
#             'netname': netname,
#         }
#     }
#     session.net_action(gateway, data).json()
