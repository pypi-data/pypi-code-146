from pysnmp.smi import builder, view, compiler, error

# Create MIB loader/builder
mibBuilder = builder.MibBuilder()
compiler.addMibCompiler(mibBuilder, sources=["/usr/share/snmp/mibs"])
mibBuilder.addMibSources(builder.DirMibSource("/opt/pysnmp_mibs"))
print(mibBuilder.getMibSources())

mibBuilder.loadModules(
    "SNMPv2-MIB",
    "SNMP-FRAMEWORK-MIB",
    "SNMP-COMMUNITY-MIB",
    "IF-MIB",
    "IP-FORWARD-MIB",
)

mibView = view.MibViewController(mibBuilder)


def is_table(modName, symName, mibBuilder):
    rowNode = mibBuilder.importSymbols(modName, symName)
    # Its a tuple with a single value in it.
    rowNode = rowNode[0]
    return rowNode.__class__.__name__ == "MibTable"


def traverse_mib(mibView):
    oid, label, suffix = mibView.getFirstNodeName()
    while True:
        try:
            modName, nodeName, suffix = mibView.getNodeLocation(oid)
            yield modName, nodeName
            oid, label, suffix = mibView.getNextNodeName(oid)
        except error.NoSuchObjectError:
            # Exahusted
            return


for modName, nodeName in traverse_mib(mibView):
    if is_table(modName, nodeName, mibBuilder):
        print(f"{modName}::{nodeName}")
