import os
import json
import time
from lager.pcb.net import Net, NetType


def net_setup(*args, **kwargs):
    pass

def net_teardown(*args, **kwargs):
    pass

def set_voltage(netname, value, ocp, ovp, clear_ocp, clear_ovp):
    target_net = Net(netname, type=None, setup_function=net_setup, teardown_function=net_teardown)
    if clear_ocp==True:
        target_net.clear_ocp()
    if clear_ovp==True:
        target_net.clear_ovp()        
    if ocp!=None:
        target_net.set_ocp(ocp)
    if ovp!=None:
        target_net.set_ovp(ovp)

    if value!=None:  
        target_net.set_voltage(value)
        return

    print(f"Voltage: {target_net.voltage()}")



def set_current(netname, value, ocp, ovp, clear_ocp, clear_ovp):
    target_net = Net(netname, type=None, setup_function=net_setup, teardown_function=net_teardown)
    if clear_ocp==True:
        target_net.clear_ocp()
    if clear_ovp==True:
        target_net.clear_ovp()        
    if ocp!=None:
        target_net.set_ocp(ocp)
    if ovp!=None:
        target_net.set_ovp(ovp)  

    if value!=None:  
        target_net.set_current(value)
        return

    print(f"Current: {target_net.current()}")


def get_state(netname):
    target_net = Net(netname, type=None, setup_function=net_setup, teardown_function=net_teardown)    
    print(f"Voltage: {target_net.voltage()}")
    print(f"Current: {target_net.current()}")
    print(f"Power: {target_net.power()}")
    print(f"Over Current Limit {target_net.get_ocp_limit()}")
    print(f"    Net in Over Current: {target_net.is_ocp()}")
    print(f"Over Voltage Limit {target_net.get_ovp_limit()}")
    print(f"    Net in Over Voltage: {target_net.is_ovp()}")     


def disable_net(netname):
    target_net = Net(netname, type=None, setup_function=net_setup, teardown_function=net_teardown)
    target_net.disable() 

def enable_net(netname):
    target_net = Net(netname, type=None, setup_function=net_setup, teardown_function=net_teardown)
    target_net.enable() 

def main():
    command = json.loads(os.environ['LAGER_COMMAND_DATA'])
    if command['action'] == 'voltage':
        set_voltage(**command['params'])
    elif command['action'] == 'current':
        set_current(**command['params']) 
    elif command['action'] == 'get_state':
        get_state(**command['params'])
    elif command['action'] == 'disable_net':
        disable_net(**command['params'])
    elif command['action'] == 'enable_net': 
        enable_net(**command['params'])                                            
    else:
        pass

if __name__ == '__main__':
    main()
