import lxml.etree as ET
import os


xsltfile = ET.XSLT(ET.parse('mstest-to-junit.xsl'))
trxfile = open("svc_buildagent_automaster_2021-10-23_06_36_52.trx", "r").read()
print("here")
trxfile = trxfile.encode('utf-8').decode('utf-8', errors='replace')
trxfile  = ET.parse(trxfile)
print("here2")
#output = xsltfile(trxfile).decode('utf-8', errors='replace').write_output('output.xml')

