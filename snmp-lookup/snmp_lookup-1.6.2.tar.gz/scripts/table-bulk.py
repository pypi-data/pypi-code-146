from tabulate import tabulate
from pysnmp.hlapi import (
    SnmpEngine,
    EndOfMibView,
    CommunityData,
    UdpTransportTarget,
    ContextData,
    ObjectIdentity,
    nextCmd,
    bulkCmd,
    ObjectType,
)
from pysnmp.smi import view, compiler


assert EndOfMibView
assert SnmpEngine
assert CommunityData
assert UdpTransportTarget
assert ContextData
assert ObjectIdentity
assert nextCmd

HOST = "demo.snmplabs.com"
HOST = "193.12.137.37"
PORT = 161


engine = SnmpEngine()
community = CommunityData("public")
transport = UdpTransportTarget((HOST, PORT))
context = ContextData()

mibBuilder = engine.getMibBuilder()

compiler.addMibCompiler(
    mibBuilder, sources=["/home/spider/Projects/modio_snmp/data/mibs"]
)

mibBuilder.loadModules("IP-FORWARD-MIB", "IF-MIB")
mibView = view.MibViewController(mibBuilder)

TABLES = [
    ("IP-FORWARD-MIB", "inetCidrRouteTable"),
    ("IF-MIB", "ifTable"),
    ("SYNOLOGY-SMART-MIB", "diskSMARTTable"),
    ("SYNOLOGY-DISK-MIB", "diskTable"),
    ("SYNOLOGY-RAID-MIB", "raidTable"),
    ("SYNOLOGY-STORAGEIO-MIB", "storageIOTable"),
]

for mib, _ in TABLES:
    mibBuilder.loadModule(mib)

oids = [ObjectIdentity(mib, label) for mib, label in TABLES]
objects = [ObjectType(t) for t in oids]

# Look up our data in the mibView
for t in oids:
    t.resolveWithMib(mibView)

for t in objects:
    t.resolveWithMib(mibView)

# This fails is any isn't resolved
for t in oids:
    hash(t)

cmd = bulkCmd(
    engine,
    community,
    transport,
    context,
    0,
    50,
    *objects,
    lexicographicMode=False,
    lookupMib=True,
)


my_items = []
t_items = {}


for (errorIndication, errorStatus, errorIndex, varBinds) in cmd:
    if errorIndication:
        print("Error Indication", errorIndication)
        break
    elif errorStatus:
        print(
            "%s at %s"
            % (
                errorStatus.prettyPrint(),
                errorIndex and varBinds[int(errorIndex) - 1][0] or "?",
            )
        )
        break
    else:
        for varBind in varBinds:
            if isinstance(varBind[1], EndOfMibView):
                # This is something that we don't care for
                continue

            print(" = ".join([x.prettyPrint() for x in varBind]))
            row = {}
            object_identity, object_value = varBind
            object_identity.resolveWithMib(mibView)

            parent = None
            for t in oids:
                if t.isPrefixOf(object_identity):
                    parent = t.prettyPrint()
                    # print(parent)

            (
                mod_name,
                var_name,
                indices,
            ) = object_identity.getMibSymbol()
            index_labels = []
            indexes = []
            if indices:
                # Take the label, drop off one from the right to get the MIB
                # tree parent
                label_parent = object_identity.getLabel()[:-1]
                parent_mib, parent_name, _ = mibView.getNodeLocation(
                    label_parent
                )
                row_node = mibView.mibBuilder.importSymbols(
                    parent_mib, parent_name
                )
                # Is a 1-value tuple.
                row_node = row_node[0]
                # row_node.getIndexNames() returns a tuple of tuples:
                # ((0, MIB, FIRST_NAME,(0, MIB, SECOND_NAME))
                index_labels = [
                    label_name for _, _, label_name in row_node.getIndexNames()
                ]
                # If we want to create a VarBind, or an proper ObjectIdentity,
                # See below.
                # We only need the labels
                # index_labels = [
                #   ObjectIdentity(label_mib, label_name)
                #   for _,label_mib, label_name in row_node.getIndexNames()]

            for idx, label in zip(indices, index_labels):
                idx_datatype = idx.__class__.__name__
                idx_name = label
                # This always string-ifies the data. Suitable for our output.
                idx_val = idx.prettyPrint()
                indexes.append((idx_name, idx_val))

            print(indexes)
            row["table"] = parent
            row["name"] = var_name
            row["index"] = tuple(indexes)

            # Is it an enumeration?
            try:
                value = object_value.namedValues[object_value]
                print("Enumerateable: ", object_value.namedValues)
            except (AttributeError, KeyError):
                value = object_value.prettyPrint()
            row["value"] = value
            #            my_table[parent][index].append(var_bind_dict["value"])
            my_items.append(row)

            t_table = t_items.setdefault(parent, {})
            t_row = t_table.setdefault(tuple(indexes), {})
            t_row[var_name] = value

#            bangBind(varBind)


# tablename, row_name, index, value

# table:
#        row_title1, row_title2, row_title3
# index, value,         value2,     value3
for tabname, table in t_items.items():
    print("\n\nSNMP Table:\t", tabname, "")

    headers = []
    for indexes, tabdata in table.items():
        for header, value in indexes:
            tabdata[header] = value
    #        index_col = " | ".join(x[0] for x in indexes)
    #        index_val = " | ".join(x[1] for x in indexes)
    #        tabdata[index_col]=index_val
    #        index_table = tabulate(indexes,
    # The index is a a tuple of tuples
    # (("name", "value"), ("name", "value"))
    #        for key, val in indexes:
    #            headers.append(key)
    #            tabdata[key] = val
    print(tabulate(table.values(), headers="keys"))
