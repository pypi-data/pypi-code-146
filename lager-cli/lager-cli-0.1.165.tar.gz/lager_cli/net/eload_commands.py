# @net.group()
# @click.argument('NETNAME')
# @click.pass_context
# def eload(ctx, netname):
#     """
#         Control e-load nets
#     """    
#     ctx.obj.netname = netname

# @eload.command()
# @click.argument('VALUE', required=False, type=click.FLOAT)
# @click.pass_context
# @click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
# @click.option('--dut', required=False, help='ID of DUT')
# @click.option('--mcu', required=False)
# @click.option('--max-volt', required=False, type=click.FLOAT, help='Set max voltage')
# @click.option('--max-curr', required=False, type=click.FLOAT, help='Set max current')
# def resistance(ctx, gateway, dut, mcu, value, max_volt, max_curr):
#     """
#         Set constant resistance load
#     """      
#     pass

# @eload.command()
# @click.argument('VALUE', required=False, type=click.FLOAT)
# @click.pass_context
# @click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
# @click.option('--dut', required=False, help='ID of DUT')
# @click.option('--mcu', required=False)
# @click.option('--max-volt', required=False, type=click.FLOAT, help='Set max voltage')
# @click.option('--max-curr', required=False, type=click.FLOAT, help='Set max current')
# def voltage(ctx, gateway, dut, mcu, value, max_volt, max_curr):
#     """
#         Set constant voltage load
#     """      
#     pass

# @eload.command()
# @click.argument('VALUE', required=False, type=click.FLOAT)
# @click.pass_context
# @click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
# @click.option('--dut', required=False, help='ID of DUT')
# @click.option('--mcu', required=False)
# @click.option('--max-volt', required=False, type=click.FLOAT, help='Set max voltage')
# @click.option('--max-curr', required=False, type=click.FLOAT, help='Set max current')
# def current(ctx, gateway, dut, mcu, value, max_volt, max_curr):
#     """
#         Set constant current load
#     """      
#     pass

# @eload.command()
# @click.argument('VALUE', required=False, type=click.FLOAT)
# @click.pass_context
# @click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
# @click.option('--dut', required=False, help='ID of DUT')
# @click.option('--mcu', required=False)
# @click.option('--max-volt', required=False, type=click.FLOAT, help='Set max voltage')
# @click.option('--max-curr', required=False, type=click.FLOAT, help='Set max current')
# def current(ctx, gateway, dut, mcu, value, max_volt, max_curr):
#     """
#         Set constant power load
#     """      
#     pass


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
