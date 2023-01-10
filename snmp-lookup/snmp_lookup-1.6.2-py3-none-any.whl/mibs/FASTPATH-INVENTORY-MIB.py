#
# PySNMP MIB module FASTPATH-INVENTORY-MIB (http://snmplabs.com/pysmi)
# ASN.1 source file://data/mibs/FASTPATH-INVENTORY-MIB
# Produced by pysmi-0.3.4 at Wed Jan 29 17:31:16 2020
# On host nerk platform Linux version 5.3.15-300.fc31.x86_64 by user spider
# Using Python version 3.7.5 (default, Oct 17 2019, 12:16:48) 
#
OctetString, Integer, ObjectIdentifier = mibBuilder.importSymbols("ASN1", "OctetString", "Integer", "ObjectIdentifier")
NamedValues, = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
ConstraintsUnion, ConstraintsIntersection, ValueSizeConstraint, ValueRangeConstraint, SingleValueConstraint = mibBuilder.importSymbols("ASN1-REFINEMENT", "ConstraintsUnion", "ConstraintsIntersection", "ValueSizeConstraint", "ValueRangeConstraint", "SingleValueConstraint")
fastPath, = mibBuilder.importSymbols("BROADCOM-REF-MIB", "fastPath")
ObjectGroup, ModuleCompliance, NotificationGroup = mibBuilder.importSymbols("SNMPv2-CONF", "ObjectGroup", "ModuleCompliance", "NotificationGroup")
ObjectIdentity, Counter32, NotificationType, Gauge32, TimeTicks, Unsigned32, Counter64, Integer32, Bits, MibIdentifier, MibScalar, MibTable, MibTableRow, MibTableColumn, IpAddress, ModuleIdentity, iso = mibBuilder.importSymbols("SNMPv2-SMI", "ObjectIdentity", "Counter32", "NotificationType", "Gauge32", "TimeTicks", "Unsigned32", "Counter64", "Integer32", "Bits", "MibIdentifier", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "IpAddress", "ModuleIdentity", "iso")
TextualConvention, DisplayString, RowStatus = mibBuilder.importSymbols("SNMPv2-TC", "TextualConvention", "DisplayString", "RowStatus")
fastPathInventory = ModuleIdentity((1, 3, 6, 1, 4, 1, 4413, 1, 1, 13))
fastPathInventory.setRevisions(('2013-10-15 00:00', '2011-01-26 00:00', '2007-05-23 00:00', '2004-10-28 20:37', '2003-05-26 19:30',))

if getattr(mibBuilder, 'version', (0, 0, 0)) > (4, 4, 0):
    if mibBuilder.loadTexts: fastPathInventory.setRevisionsDescriptions(('Object support modifications for LinuxHost systems.', 'Postal address updated.', 'Broadcom branding related changes.', 'Version 2 - Add support for Front Panel Stacking configuration.', 'Initial version.',))
if mibBuilder.loadTexts: fastPathInventory.setLastUpdated('201310150000Z')
if mibBuilder.loadTexts: fastPathInventory.setOrganization('Broadcom Corporation')
if mibBuilder.loadTexts: fastPathInventory.setContactInfo(' Customer Support Postal: Broadcom Corporation 1030 Swabia Court Suite 400 Durham, NC 27703 Tel: +1 919 865 2700')
if mibBuilder.loadTexts: fastPathInventory.setDescription('This MIB defines the objects used for FastPath to configure and report information and status of units, slots and supported cards.')
class AgentInventoryUnitPreference(TextualConvention, Integer32):
    description = 'Indicates the preference the unit has for being the management unit in the stack. If the value is 0, it indicates the unit is disabled for management.'
    status = 'current'
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(0, 1, 2))
    namedValues = NamedValues(("disabled", 0), ("unsassigned", 1), ("assigned", 2))

class AgentInventoryUnitType(TextualConvention, Unsigned32):
    description = 'The Unit Type value for a given unit, displayed in hexadecimal.'
    status = 'current'
    displayHint = 'x'

class AgentInventoryCardType(TextualConvention, Unsigned32):
    description = 'The Card Type value for a given card, displayed in hexadecimal.'
    status = 'current'
    displayHint = 'x'

agentInventoryStackGroup = MibIdentifier((1, 3, 6, 1, 4, 1, 4413, 1, 1, 13, 1))
agentInventoryStackSTKname = MibScalar((1, 3, 6, 1, 4, 1, 4413, 1, 1, 13, 1, 5), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(("unconfigured", 1), ("image1", 2), ("image2", 3)))).setMaxAccess("readwrite")
if mibBuilder.loadTexts: agentInventoryStackSTKname.setStatus('current')
if mibBuilder.loadTexts: agentInventoryStackSTKname.setDescription('STK file on management unit for copy/activate/delete operations to all units in the stack unconfigured(1) - indicates a default state and can not be set.')
agentInventoryStackActivateSTK = MibScalar((1, 3, 6, 1, 4, 1, 4413, 1, 1, 13, 1, 6), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(("enable", 1), ("disable", 2)))).setMaxAccess("readwrite")
if mibBuilder.loadTexts: agentInventoryStackActivateSTK.setStatus('current')
if mibBuilder.loadTexts: agentInventoryStackActivateSTK.setDescription('Activates the specified STK file on all units on the stack.')
agentInventoryStackDeleteSTK = MibScalar((1, 3, 6, 1, 4, 1, 4413, 1, 1, 13, 1, 7), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(("enable", 1), ("disable", 2)))).setMaxAccess("readwrite")
if mibBuilder.loadTexts: agentInventoryStackDeleteSTK.setStatus('current')
if mibBuilder.loadTexts: agentInventoryStackDeleteSTK.setDescription('Deletes the specified STK file from all units on the stack.')
agentInventoryCardGroup = MibIdentifier((1, 3, 6, 1, 4, 1, 4413, 1, 1, 13, 4))
agentInventoryCardTypeTable = MibTable((1, 3, 6, 1, 4, 1, 4413, 1, 1, 13, 4, 1), )
if mibBuilder.loadTexts: agentInventoryCardTypeTable.setStatus('current')
if mibBuilder.loadTexts: agentInventoryCardTypeTable.setDescription('Contains information for all supported Card Types in the system.')
agentInventoryCardTypeEntry = MibTableRow((1, 3, 6, 1, 4, 1, 4413, 1, 1, 13, 4, 1, 1), ).setIndexNames((0, "FASTPATH-INVENTORY-MIB", "agentInventoryCardIndex"))
if mibBuilder.loadTexts: agentInventoryCardTypeEntry.setStatus('current')
if mibBuilder.loadTexts: agentInventoryCardTypeEntry.setDescription('Contains information related to a specific Card Type.')
agentInventoryCardIndex = MibTableColumn((1, 3, 6, 1, 4, 1, 4413, 1, 1, 13, 4, 1, 1, 1), Unsigned32())
if mibBuilder.loadTexts: agentInventoryCardIndex.setStatus('current')
if mibBuilder.loadTexts: agentInventoryCardIndex.setDescription('An arbitrary index used to identify cards in the table.')
agentInventoryCardType = MibTableColumn((1, 3, 6, 1, 4, 1, 4413, 1, 1, 13, 4, 1, 1, 2), AgentInventoryCardType()).setMaxAccess("readonly")
if mibBuilder.loadTexts: agentInventoryCardType.setStatus('current')
if mibBuilder.loadTexts: agentInventoryCardType.setDescription('The Card Type associated with this instance.')
agentInventoryCardModelIdentifier = MibTableColumn((1, 3, 6, 1, 4, 1, 4413, 1, 1, 13, 4, 1, 1, 3), DisplayString()).setMaxAccess("readonly")
if mibBuilder.loadTexts: agentInventoryCardModelIdentifier.setStatus('current')
if mibBuilder.loadTexts: agentInventoryCardModelIdentifier.setDescription('The model identifier for the supported Card Type.')
agentInventoryCardDescription = MibTableColumn((1, 3, 6, 1, 4, 1, 4413, 1, 1, 13, 4, 1, 1, 4), DisplayString()).setMaxAccess("readonly")
if mibBuilder.loadTexts: agentInventoryCardDescription.setStatus('current')
if mibBuilder.loadTexts: agentInventoryCardDescription.setDescription('The card description for the supported Card Type.')
agentInventoryComponentGroup = MibIdentifier((1, 3, 6, 1, 4, 1, 4413, 1, 1, 13, 5))
agentInventoryComponentTable = MibTable((1, 3, 6, 1, 4, 1, 4413, 1, 1, 13, 5, 1), )
if mibBuilder.loadTexts: agentInventoryComponentTable.setStatus('current')
if mibBuilder.loadTexts: agentInventoryComponentTable.setDescription('Contains information for all supported Components in the system.')
agentInventoryComponentEntry = MibTableRow((1, 3, 6, 1, 4, 1, 4413, 1, 1, 13, 5, 1, 1), ).setIndexNames((0, "FASTPATH-INVENTORY-MIB", "agentInventoryComponentIndex"))
if mibBuilder.loadTexts: agentInventoryComponentEntry.setStatus('current')
if mibBuilder.loadTexts: agentInventoryComponentEntry.setDescription('Contains information related to a specific Components.')
agentInventoryComponentIndex = MibTableColumn((1, 3, 6, 1, 4, 1, 4413, 1, 1, 13, 5, 1, 1, 1), Unsigned32())
if mibBuilder.loadTexts: agentInventoryComponentIndex.setStatus('current')
if mibBuilder.loadTexts: agentInventoryComponentIndex.setDescription('An arbitrary index used to reference components in the table.')
agentInventoryComponentMnemonic = MibTableColumn((1, 3, 6, 1, 4, 1, 4413, 1, 1, 13, 5, 1, 1, 2), DisplayString()).setMaxAccess("readonly")
if mibBuilder.loadTexts: agentInventoryComponentMnemonic.setStatus('current')
if mibBuilder.loadTexts: agentInventoryComponentMnemonic.setDescription('The abreviated name of this component.')
agentInventoryComponentName = MibTableColumn((1, 3, 6, 1, 4, 1, 4413, 1, 1, 13, 5, 1, 1, 3), DisplayString()).setMaxAccess("readonly")
if mibBuilder.loadTexts: agentInventoryComponentName.setStatus('current')
if mibBuilder.loadTexts: agentInventoryComponentName.setDescription('The name of the component for this instance.')
mibBuilder.exportSymbols("FASTPATH-INVENTORY-MIB", agentInventoryCardIndex=agentInventoryCardIndex, agentInventoryComponentEntry=agentInventoryComponentEntry, agentInventoryStackGroup=agentInventoryStackGroup, fastPathInventory=fastPathInventory, agentInventoryComponentMnemonic=agentInventoryComponentMnemonic, agentInventoryCardTypeTable=agentInventoryCardTypeTable, PYSNMP_MODULE_ID=fastPathInventory, agentInventoryCardModelIdentifier=agentInventoryCardModelIdentifier, agentInventoryComponentGroup=agentInventoryComponentGroup, AgentInventoryUnitPreference=AgentInventoryUnitPreference, agentInventoryComponentTable=agentInventoryComponentTable, agentInventoryCardType=agentInventoryCardType, agentInventoryCardGroup=agentInventoryCardGroup, agentInventoryStackDeleteSTK=agentInventoryStackDeleteSTK, agentInventoryStackActivateSTK=agentInventoryStackActivateSTK, agentInventoryCardTypeEntry=agentInventoryCardTypeEntry, agentInventoryComponentIndex=agentInventoryComponentIndex, AgentInventoryCardType=AgentInventoryCardType, AgentInventoryUnitType=AgentInventoryUnitType, agentInventoryCardDescription=agentInventoryCardDescription, agentInventoryStackSTKname=agentInventoryStackSTKname, agentInventoryComponentName=agentInventoryComponentName)
