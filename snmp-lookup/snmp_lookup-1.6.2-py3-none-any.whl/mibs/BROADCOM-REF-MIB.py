#
# PySNMP MIB module BROADCOM-REF-MIB (http://snmplabs.com/pysmi)
# ASN.1 source file://data/mibs/BROADCOM-REF-MIB
# Produced by pysmi-0.3.4 at Wed Jan 29 17:31:16 2020
# On host nerk platform Linux version 5.3.15-300.fc31.x86_64 by user spider
# Using Python version 3.7.5 (default, Oct 17 2019, 12:16:48) 
#
OctetString, Integer, ObjectIdentifier = mibBuilder.importSymbols("ASN1", "OctetString", "Integer", "ObjectIdentifier")
NamedValues, = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
ConstraintsUnion, ConstraintsIntersection, ValueSizeConstraint, ValueRangeConstraint, SingleValueConstraint = mibBuilder.importSymbols("ASN1-REFINEMENT", "ConstraintsUnion", "ConstraintsIntersection", "ValueSizeConstraint", "ValueRangeConstraint", "SingleValueConstraint")
ModuleCompliance, NotificationGroup = mibBuilder.importSymbols("SNMPv2-CONF", "ModuleCompliance", "NotificationGroup")
ObjectIdentity, Counter32, NotificationType, Gauge32, TimeTicks, Unsigned32, Counter64, Integer32, Bits, MibIdentifier, MibScalar, MibTable, MibTableRow, MibTableColumn, IpAddress, ModuleIdentity, enterprises, iso = mibBuilder.importSymbols("SNMPv2-SMI", "ObjectIdentity", "Counter32", "NotificationType", "Gauge32", "TimeTicks", "Unsigned32", "Counter64", "Integer32", "Bits", "MibIdentifier", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "IpAddress", "ModuleIdentity", "enterprises", "iso")
TextualConvention, DisplayString = mibBuilder.importSymbols("SNMPv2-TC", "TextualConvention", "DisplayString")
broadcom = ModuleIdentity((1, 3, 6, 1, 4, 1, 4413))
broadcom.setRevisions(('2011-01-26 00:00', '2007-05-23 00:00', '2003-11-21 00:00', '2003-02-06 12:00',))

if getattr(mibBuilder, 'version', (0, 0, 0)) > (4, 4, 0):
    if mibBuilder.loadTexts: broadcom.setRevisionsDescriptions(('Postal address updated.', 'Broadcom branding related changes.', 'Revisions made for new release.', 'Updated for release',))
if mibBuilder.loadTexts: broadcom.setLastUpdated('201101260000Z')
if mibBuilder.loadTexts: broadcom.setOrganization('Broadcom Corporation')
if mibBuilder.loadTexts: broadcom.setContactInfo(' Customer Support Postal: Broadcom Corporation 1030 Swabia Court Suite 400 Durham, NC 27703 Tel: +1 919 865 2700')
if mibBuilder.loadTexts: broadcom.setDescription('')
broadcomProducts = MibIdentifier((1, 3, 6, 1, 4, 1, 4413, 1))
fastPath = MibIdentifier((1, 3, 6, 1, 4, 1, 4413, 1, 1))
class AgentPortMask(TextualConvention, OctetString):
    description = "Each octet within this value specifies a set of eight ports, with the first octet specifying ports 1 through 8, the second octet specifying ports 9 through 16, etc. Within each octet, the most significant bit represents the lowest numbered port, and the least significant bit represents the highest numbered port. Thus, each port of the bridge is represented by a single bit within the value of this object. If that bit has a value of '1' then that port is included in the set of ports; the port is not included if its bit has a value of '0' When setting this value, the system will ignore configuration for ports not between the first and last valid ports. Configuration of any port numbers between this range that are not valid ports return a failure message, but will still apply configuration for valid ports."
    status = 'current'

mibBuilder.exportSymbols("BROADCOM-REF-MIB", broadcom=broadcom, broadcomProducts=broadcomProducts, AgentPortMask=AgentPortMask, PYSNMP_MODULE_ID=broadcom, fastPath=fastPath)
