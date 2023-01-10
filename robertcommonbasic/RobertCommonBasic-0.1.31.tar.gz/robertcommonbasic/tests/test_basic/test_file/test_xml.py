import json

from robertcommonbasic.basic.file.xml import *


def write(path):
    xml_dom = create_xml_document()
    root_noode = create_xml_node(xml_dom, None, 'license', None, {"vendor": 'Ari', "expire": '2024-01-01', "mac": '00:0E:C6:DC:D4:BB', "version": 'V1.0.2', "author": '', "generated": '2022-11-22'})
    project_node = create_xml_node(xml_dom, root_noode, 'project', None, {"name": '测试项目', "id": 1, "user": 'admin', "psw": '123456'})
    drivers_node = create_xml_node(xml_dom, project_node, 'drivers', None, {"support": '*'})

    driver_noode = create_xml_node(xml_dom, drivers_node, 'driver', None, {'type': 'opc', 'device.limit': '10', 'point.limit': '500000'})
    driver_noode = create_xml_node(xml_dom, drivers_node, 'driver', None, {'type': 'tcp_core', 'device.limit': '1', 'point.limit': 'none'})
    devices_node = create_xml_node(xml_dom, driver_noode, 'devices', None)
    device_node = create_xml_node(xml_dom, devices_node, 'device', None, {'name': 'TCP'})
    create_xml_node(xml_dom, device_node, 'property', None, {"name": "port", "value": "9500", "type": "int"})
    create_xml_node(xml_dom, device_node, 'property', None, {"name": "reg", "value": "test_dtu", "type": "str"})

    device_node = create_xml_node(xml_dom, devices_node, 'device', None, {'name': 'TCP1'})
    create_xml_node(xml_dom, device_node, 'property', None, {"name": "port", "value": "9500", "type": "int"})
    create_xml_node(xml_dom, device_node, 'property', None, {"name": "reg", "value": "test_dtu", "type": "str"})

    save_xml_node(path, xml_dom, encoding='UTF-8')


def read(path):
    xml_dom = value_to_xml(open(path, 'r', encoding='UTF-8').read())
    root = get_xml_root_node(xml_dom)
    nodes = get_xml_nodes(root, 'sign')
    if len(nodes) >0 :
        del_xml_node(root, 'sign')
    else:
        create_xml_node(xml_dom, root, 'sign', None, {'date': '2022-11-18', 'user': 'robert'})
    save_xml_node(path, xml_dom, encoding='UTF-8')

    for child in get_xml_child_nodes(root):
        print(child)
    content = read_xml_dict(path, encoding='utf-8')
    s = value_to_xml(content)
    print(s)
    print(xml_node_to_str(s))


def write_license(path: str, vendor: str, expire: str, mac: str, version: str, author: str, generated: str, name: str, id: str, user:str, psw: str, support: str, drivers: list):
    xml_dom = create_xml_document()
    root_noode = create_xml_node(xml_dom, None, 'license', None, {"vendor": vendor, "expire": expire, "mac": mac, "version": version, "author": author, "generated": generated})
    project_node = create_xml_node(xml_dom, root_noode, 'project', None, {"name": name, "id": id, "user": user, "psw": psw})
    drivers_node = create_xml_node(xml_dom, project_node, 'drivers', None, {"support": support})
    for d in drivers:
        driver_noode = create_xml_node(xml_dom, drivers_node, 'driver', None, d.get('attributes', {}))
        devices = d.get('devices', {})
        if len(devices) > 0:
            devices_noode = create_xml_node(xml_dom, driver_noode, 'devices', None)
            for k, propertys in devices.items():
                device_noode = create_xml_node(xml_dom, devices_noode, 'device', None, {"name": k})
                for property in propertys:
                    create_xml_node(xml_dom, device_noode, 'property', None, property)
    save_xml_node(path, xml_dom, encoding='UTF-8')


def read_license(path: str):
    content = open(path, 'r', encoding='UTF-8').read()
    xml_dict = read_xml_dict(path, encoding='UTF-8')
    print()


path = r'E:\test2.xml'
#write(path)
read_license(path)
write_license(path, 'Ari', '2024-01-01', '1DA8-E3F0-9E6A-493D', 'V1.0.2', '', '2022-11-22', '测试项目', '1', 'admin', '123456', '*', [{'attributes': {'type': 'opc', 'device.limit': '10', 'point.limit': '10000'}}, {'attribute': {'type': 'tcp_core', 'device.limit': '1', 'point.limit': 'none'}, 'devices': {'TCP': [{"name": "enabled", "value": "true", "type": "str"}, {"name": "host", "value": "localhost", "type": "str"}, {"name": "port", "value": "9500", "type": "int"}, {"name": "reg", "value": "test_dtu", "type": "str"}, {"name": "interval", "value": "1m", "type": "str"}, {"name": "timeout", "value": "5", "type": "int"}]}}])