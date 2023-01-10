#!/usr/bin/env python

mystr = """
/araali_fog2agent.araalifog2agentservices/attesttargetworkload:
  Count: 25755
  Errors: 0
  Avg: 11269
  Min: 0
  Max: 1646546
  InBytes: 75147845
  OutBytes: 312561961
/araali_fog2agent.araalifog2agentservices/reportprocessvulnerabilities:
  Count: 1075
  Errors: 0
  Avg: 57169
  Min: 0
  Max: 1259702
  InBytes: 6742865
  OutBytes: 7525
/araali_fog2agent.araalifog2agentservices/imagedownload:
  Count: 11
  Errors: 0
  Avg: 17
  Min: 0
  Max: 25
  InBytes: 9761
  OutBytes: 773090532
/araali_fog2agent.araalifog2agentservices/reportassets:
  Count: 121
  Errors: 0
  Avg: 4
  Min: 0
  Max: 45
  InBytes: 152873
  OutBytes: 847
/araali_fortify.araalifogfortifyservices/listk8sservicesbyoperator:
  Count: 2
  Errors: 0
  Avg: 173743
  Min: 0
  Max: 264459
  InBytes: 136
  OutBytes: 18
/araali_fortify.araalifogfortifyservices/registerworkload:
  Count: 1
  Errors: 0
  Avg: 17820
  Min: 0
  Max: 17820
  InBytes: 259
  OutBytes: 54
/araali_fog2agent.araalifog2agentservices/getsyscallrules:
  Count: 3
  Errors: 0
  Avg: 5
  Min: 0
  Max: 6
  InBytes: 210
  OutBytes: 339
/araali_fog2agent.araalifog2agentinitialservices/attestworkload:
  Count: 9
  Errors: 0
  Avg: 2716
  Min: 0
  Max: 2793
  InBytes: 22198
  OutBytes: 104932
/araali_fog2agent.araalifog2agentservices/sendheartbeat:
  Count: 267788
  Errors: 0
  Avg: 4
  Min: 0
  Max: 14138
  InBytes: 34322584
  OutBytes: 4016820
/araali_fog2agent.araalifog2agentservices/getaraalihostsv2:
  Count: 263290
  Errors: 0
  Avg: 375
  Min: 0
  Max: 14246
  InBytes: 127033099
  OutBytes: 44881246877
/araali_fog2agent.araalifog2agentservices/sendgtorinfo:
  Count: 65824
  Errors: 0
  Avg: 23
  Min: 0
  Max: 12349
  InBytes: 175292402
  OutBytes: 1261991
/araali_fog2agent.araalifog2agentservices/getaraalipolicy:
  Count: 40796
  Errors: 0
  Avg: 143
  Min: 0
  Max: 48416
  InBytes: 113958861
  OutBytes: 169804848
/araali_fog2agent.araalifog2agentservices/reportflows:
  Count: 214983
  Errors: 0
  Avg: 5
  Min: 0
  Max: 5354
  InBytes: 5568400893
  OutBytes: 2149820
/araali_fog2agent.araalifog2agentservices/servicesession:
  Count: 38
  Errors: 0
  Avg: 9
  Min: 0
  Max: 46
  InBytes: 64309
  OutBytes: 1464
/araali_fortify.araalifogfortifyservices/registerservice:
  Count: 74
  Errors: 0
  Avg: 7527
  Min: 0
  Max: 142585
  InBytes: 112864
  OutBytes: 518
Total:
  InBytes: 6101261159
  OutBytes: 46144248546
Flow Count: 1892168 (2022-08-25 02:44:33.495749646 +0000 UTC m=+47206.162003645)
CPU Usage: 2.88%/2.83%
Memory Usage: 4.85%/4.85%
A2B Queue Stats:
   QElemTypeAgentInfo: 0
   QElemTypeAgentHeartbeat: 0
   QElemTypeFlowInfo: 19
   QElemTypeFortificationInfo: 0
   QElemTypeTimer: 0
   QElemTypeMalwareAlert: 19
   QElemTypeFetchPolicy: 0
   QElemTypeAgentHeartbeatV2: 0
   QElemTypeListK8Services: 0
   QElemTypeAssetInfo: 0
   QElemTypeProcessInfo: 0
   QElemTypeAraaliK8SPolicy: 0
   invalid q type: 0
   """
hdr = ["Count", "Errors", "Avg", "Min", "Max", "InBytes", "OutBytes"]
topic = None
items = {}
for line in mystr.strip().split("\n"):
    line = line.strip().split(":")
    if not line[1]:
        topic = line[0]
        items[topic] = {}
        continue
    if line[0] in hdr:
        items[topic][line[0]] = line[1]
        continue
    print(line)

print(",".join(hdr))
for k,v in items.items():
    print(k, end=",", sep='')
    for h in hdr:
        print(v.get(h, 0), end=",", sep='')
    print()
