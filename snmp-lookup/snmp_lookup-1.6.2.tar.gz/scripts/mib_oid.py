from pysnmp.smi import builder, view, compiler

# Load MIB objects, index them by MIB::name
mibBuilder = builder.MibBuilder()

# If Pythonized MIB is not present, call pysmi parser to fetch
# and compile requested MIB into Python
compiler.addMibCompiler(mibBuilder)  # , sources=['/usr/share/snmp/mibs'])

# Load or compile&load this MIB
mibBuilder.loadModules("IF-MIB", "UBNT-UniFi-MIB")

# Index MIB objects (as maintained by `mibBulder`) by OID
mibView = view.MibViewController(mibBuilder)

# Look up MIB name and MIB object name by OID
modName, symName, suffix = mibView.getNodeLocation(
    (1, 3, 6, 1, 2, 1, 31, 1, 1, 1, 6)
)
modName, symName, suffix = mibView.getNodeLocation(
    (".1.3.6.1.4.1.41112.1.6.1.1.1.6.2")
)

# Fetch MIB object
(mibNode,) = mibBuilder.importSymbols(modName, symName)

# This might be an ASN.1 schema object representing one of SNMP types
print(mibNode.syntax.__class__)
