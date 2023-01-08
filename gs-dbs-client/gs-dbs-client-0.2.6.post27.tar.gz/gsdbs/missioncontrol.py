import ast
import asyncio
import ctypes
import http.client as httplib
import os
import random
import sys
import threading
import time
from datetime import datetime

import websocket
import string
from threading import Thread
import json
import requests
from websocket import WebSocketConnectionClosedException

from gsdbs.dbclient import GSDBS
from twisted.internet import task, reactor
from multiprocessing.dummy import Pool
import logging
import os.path
from multiprocessing import Process, Queue


class MissionControl(Thread):

    def __init__(self, cnode, prefix, gsdbs: GSDBS, execute, ondestruct, restartCNode, heartbeatintervall=10):
        self._mandantname = ""
        self.counter = 0
        self.cnode = cnode
        self._gsdbs = gsdbs
        self._prefix = prefix
        self.execute = execute
        self.ondestruct = ondestruct
        self.restartCNode = restartCNode
        self.heartbeatintervall = heartbeatintervall * 1000
        self._pool = Pool(self._gsdbs.credentials["poolsize"])
        self._logger = logging.getLogger(__name__)
        self.joblist = {}
        Thread.__init__(self)
        self.threadid = threading.current_thread().ident
        self.connect()

    def connect(self):
        self.start()

    def disconnect(self):
        pass

    def run(self):
        self._r1 = str(random.randint(0, 1000))
        self._conn_id = self.random_str(8)
        websocket.enableTrace(False)

        if len(self._gsdbs.cookiejar) == 0:
            self._logger.error("no session available restarting")
            exit(-1)

        self._ws = websocket.WebSocketApp(
            ("ws://" if "localhost" in self._gsdbs.credentials["wshost"] else "wss://")
            + self._gsdbs.credentials["wshost"] + ":" + str(self._gsdbs.credentials["wsport"]) +
            self._prefix +
            "/" +
            self._r1 +
            "/" +
            self._conn_id +
            "/websocket?gssession=" +
            self._gsdbs.cookiejar.get("session") + "." + self._gsdbs.cookiejar.get("signature"),
            on_message=self.on_message,
            on_open=self.on_open,
            on_error=self.on_error,
            on_close=self.on_close)

        self._ws.run_forever()

    def on_message(self, ws, message):
        self._pool.apply_async(self.processMessage, args=[message], callback=self.on_success,
                               error_callback=self.on_errorPost)

    def on_errorPost(self, error):
        self._logger.exception('message failed :' + error)

    def processMessage(self, message):
        # sleep(0.05)

        if message == 'a["\\n"]':
            self._logger.debug("beat:" + datetime.now().strftime("%H:%M:%S"))
            self._ws.send('["\\n"]')
            self.counter = self.counter + 1
            # if self.counter % self.heartbeatintervall == 0:
            self.ETHome()
            # self.counter = 0

        if message == "o":
            pass
        if message.startswith("a"):
            if "{" in message:
                ackid = list(filter(lambda c: c.startswith('message-id'), message.split("\\n")))[0].split(":")[1]
                subscription = list(filter(lambda c: c.startswith('subscription'), message.split("\\n")))[0].split(":")[
                    1]
                ack = f'ACK\\nid:{ackid}\\nsubscription:{subscription}\\n\\n\\u0000'
                self._ws.send("[\"" + ack + "\"]")
                try:
                    mssgbdy = json.loads(
                        message[message.find("{"):message.find("\\u0000")].replace("\\\"", "\"").replace("\\n", " ")
                        .replace("\\r", " ").replace("\\t", " "))

                    if "gscnoderestart" in mssgbdy:
                        self.restartCNode(self.threadid)

                    if "gscnodestatus" in mssgbdy:
                        self.reportJobStatus(mssgbdy)
                    else:
                        self._logger.info("Starting job")
                        if len(self.joblist) < self._gsdbs.credentials["concurrentjobcount"]:
                            self.joblist[mssgbdy["jobid"]] = mssgbdy
                            self.execute(self._gsdbs, mssgbdy, self.onNext)
                        else:
                            self._logger.warn("max concurrent job count reached")
                            return

                    if "isCommand" not in mssgbdy and "gscnodestatus" not in mssgbdy and "gscnoderestart" not in mssgbdy:
                        if self.str2bool(mssgbdy["isComputingStep"]) and mssgbdy["computingstep"] != '':
                            self.markJobAsDone(mssgbdy["jobid"], mssgbdy["groupid"], mssgbdy["computingstep"])

                except Exception as e:

                    if "mssgbdy" in locals():
                        if "gscnoderestart" not in mssgbdy:
                            self.markJobAsFailed(mssgbdy["jobid"])
                    else:
                        self._logger.exception("JobFailed " + str(e))
                    if self.ondestruct is not None:
                        self.ondestruct()

        if message == "start_streaming":
            self.execute(self._gsdbs, {"start_streaming": True}, self.onNext)

        else:
            pass

    def str2bool(self, v):
        return v.lower() in ("yes", "true", "t", "1")

    def call_api(self, send):
        x = 16388
        res = [send[y - x:y] for y in range(x, len(send) + x, x)]
        for x in res:
            self._ws.send("[\"" + x + "\"]")

    def on_success(self, r):
        self._logger.debug('Job succeed')

    def on_errorPost(self, error):
        self._logger.error('job failed ' + str(error))

    def onNext(self, target, json1, data):
        try:
            data["mandantname"] = self._mandantname

            url = "http://" + self._gsdbs.credentials["wshost"] + ":" + str(
                self._gsdbs.credentials["wsport"]) + "/missioncontrol/onnext"
            json2 = {"jobid": json1["jobid"],
                     "groupid": json1["groupid"],
                     "accesstoken": self._gsdbs.cookiejar.get("session") + "." + self._gsdbs.cookiejar.get("signature"),
                     "computingstep": json1["computingstep"],
                     "target": target,
                     "cnode": self.cnode,
                     "jobkonfigname": json1["jobconfigname"],
                     "data": data}

            datastring = json.dumps(json2).replace("\"", "\'")
            self._logger.debug(datastring)
            transactionid = 'tx-' + self.random_str(8)
            send = 'SEND\\n' \
                   'destination:/queue/onnext\\n' \
                   'durable:false\\n' \
                   'exclusive:false\\n' \
                   'auto-delete:false\\n\\n' \
                   + datastring + '\\u0000'
            self.call_api(send)

        except Exception as e:
            self._logger.exception(e)
            return e

    def utf8len(self, s):

        encoded_string = s.encode('utf-8')
        byte_array = bytearray(s)

        return len(s.encode('utf-8'))

    def reportJobStatus(self, mssgbdy):

        targetJobName = mssgbdy["jobconfigname"]
        jobconfigFound = False

        for jobinfo in self.joblist:
            testSameJobkonfigname = self.joblist[jobinfo]["jobconfigname"] == targetJobName
            if testSameJobkonfigname:
                jobconfigFound = True
                break

        if not jobconfigFound:
            reportAnswer = {'channel': mssgbdy["streamkey"],
                            'pipelinetemplateName': mssgbdy["pipelinetemplateName"],
                            'jobconfigname': targetJobName}

            resp = requests.post(self._gsdbs.credentials["baseurl"] + "/missioncontrol/channelpipelines/rva/report",
                                 json=reportAnswer,
                                 cookies=self._gsdbs.cookiejar)
            resp.raise_for_status()

    def on_error(self, ws, error):
        self._logger.exception(error)
        if not (type(error) is (
                ConnectionRefusedError or ConnectionAbortedError or ConnectionResetError or WebSocketConnectionClosedException)):
            statuscode = getattr(error, 'status_code', 'default value')
            if statuscode == "status_code":
                self._gsdbs.getTokenFromApi()

    def on_close(self, ws, close_status_code, close_msg):
        if close_status_code == 401:
            self._gsdbs.getTokenFromApi()

        self._logger.exception(
            "### closed: Code->" + str(close_status_code) + "Message:" + str(close_msg) + ":" + datetime.now().strftime(
                "%H:%M:%S") + "###")

    def on_open(self, ws):
        connect = '\"CONNECT\\naccept-version:1.2\\nheart-beat:' + str(self.heartbeatintervall) + ',' + str(
            self.heartbeatintervall) + '\\nprefetch-count:1\\nauto-delete:true\\nexclusive:true\\nx-single-active-consumer:true\\n\\n\\u0000\"'
        self._ws.send("[" + connect + "]")
        time.sleep(1)
        sub = f'\"SUBSCRIBE\\nid:{self.random_str(4)}\\ndestination:/queue/{self.getQueue()}\\nack:client-individual\\n\\n\\u0000\"'
        self._ws.send("[" + sub + "]")
        self.ETHome()
        self._logger.info("open:" + datetime.now().strftime("%H:%M:%S"))
        if "camera" in self._gsdbs.credentials and self._gsdbs.credentials["camera"]:
            self.on_message(None, "start_streaming")

    def ETHome(self):
        resp = requests.get(self._gsdbs.credentials["baseurl"] + "missioncontrol/register",
                            cookies=self._gsdbs.cookiejar)
        resp.raise_for_status()

        if len(self.joblist) == 0:
            resp = requests.get(self._gsdbs.credentials["baseurl"] + "missioncontrol/channelpipelines/rva/heartbeat",
                                cookies=self._gsdbs.cookiejar)

        # self._gsdbs.executeStatementSync(f"""
        #                                     mutation{{
        #                                       addDTable(
        #                                         dtablename:"cnode",
        #                                         superDTable:DTABLE,
        #                                         sriBuildInfo:"${{cnode}}",
        #                                         dataLinks:[
        #                                           {{alias:"cnode",locale:DE,superPropertyURI:DYNAMIC_DATALINK,DataType:STRING}}
        #                                           {{alias:"desciption",locale:DE,superPropertyURI:DYNAMIC_DATALINK,DataType:STRING}}
        #                                         ]
        #                                         data:[
        #                                           ["cnode","desciption"],
        #                                           ["{self.cnode}","desciption"]
        #                                         ]
        #                                       )
        #                                     }}
        #                                     """)

        # if "camera" in self._gsdbs.credentials and self._gsdbs.credentials["camera"]:
        #
        #     self._gsdbs.executeStatementSync(f"""
        #                         mutation{{
        #                               addDTable(
        #                                 dtablename:"gscamera",
        #                                 superDTable:DTABLE,
        #                                 sriBuildInfo:"${{streamkey}}",
        #                                 dataLinks:[
        #                                   {{alias:"streamkey",locale:DE,superPropertyURI:DYNAMIC_DATALINK,DataType:STRING}}
        #                                   {{alias:"name",locale:DE,superPropertyURI:DYNAMIC_DATALINK,DataType:STRING}}
        #                                   {{alias:"humidity",locale:DE,superPropertyURI:DYNAMIC_DATALINK,DataType:STRING}}
        #                                   {{alias:"temperatur",locale:DE,superPropertyURI:DYNAMIC_DATALINK,DataType:STRING}}
        #                                   {{alias:"hres",locale:DE,superPropertyURI:DYNAMIC_DATALINK,DataType:STRING}}
        #                                   {{alias:"vres",locale:DE,superPropertyURI:DYNAMIC_DATALINK,DataType:STRING}}
        #                                   {{alias:"fps",locale:DE,superPropertyURI:DYNAMIC_DATALINK,DataType:STRING}}
        #                                   {{alias:"ptz",locale:DE,superPropertyURI:DYNAMIC_DATALINK,DataType:STRING}}
        #                                 ],
        #                                 data:[
        #                                     ["streamkey","name","humidity","temperatur","hres","vres","fps","ptz"]
        #                                      ["{self._gsdbs.credentials["cnode"]}","{self._gsdbs.credentials["cnode"]}","0","0","{self._gsdbs.credentials["hres"]}","{self._gsdbs.credentials["vres"]}","{self._gsdbs.credentials["framerate"]}","{self._gsdbs.credentials["ptz"]}"]
        #
        #                                 ]
        #                               )
        #                     }}
        #                     """)

    def getQueue(self):
        try:
            resp = requests.get(self._gsdbs.credentials["baseurl"] + self._gsdbs.credentials['userInfo'],
                                cookies=self._gsdbs.cookiejar)
            resp.raise_for_status()
            userinfo = resp.json()
            self._mandantname = userinfo["mandant"]["mandantName"]
            return userinfo["mandant"]["mandantName"] + "-" + self.cnode  # + "-" + self._conn_id
        except Exception as e:
            self._logger.exception("cant get quere"+ str(e))
            return ""

    def random_str(self, length):
        letters = string.ascii_lowercase + string.digits
        return ''.join(random.choice(letters) for c in range(length))

    def markJobAsDone(self, jobid, groupid, computingstep):
        self.joblist.pop(jobid)
        json2 = {"jobid": jobid, "groupid": groupid,
                 "accesstoken": self._gsdbs.cookiejar.get("session") + "." + self._gsdbs.cookiejar.get("signature"),
                 "computingstep": computingstep, "cnode": self.cnode}
        datastring = json.dumps(json2).replace("\"", "\\\"")

        send = 'SEND\\ndestination:/queue/onnotify\\ndurable:false\\nexclusive:false\\nauto-delete:false\\n\\n' + datastring + '\\u0000'
        self.call_api(send)
        if self.ondestruct is not None:
            self.ondestruct(self._gsdbs)
        self._logger.info("job done")

    def markJobAsFailed(self, jobid):
        self.joblist.pop(jobid)
        self._gsdbs.executeStatement(f"""
                    mutation{{
                            updateDTable(
                      dtablename:gsasyncjob,
                       where: [
                          {{connective: BLANK, column: gsasyncjob_jobid, operator: EQUAL, value: "{jobid}"}}
                            {{connective: AND, column: gsasyncjob_cnode, operator: EQUAL, value: "{self.cnode}"}}
                      ],
                      updatelist:[
                        {{datalink:gsasyncjob_jobstatus,value:"failed"}}
                      ]
                    )
                    }}
                """)


class MissionControlClient:

    def __init__(self, execute,
                 gsdbspath=os.path.dirname(os.path.realpath(__file__)),
                 configstr="",
                 logginglevel=logging.WARNING,
                 initmethod=None,
                 ondestruct=None):
        self.threadident = None
        self.execute = execute
        self.gsdbs = GSDBS(gsdbspath, configstr=configstr)
        self.cnode = self.gsdbs.credentials["cnode"]
        self.client = None
        self.logginglevel = self.gsdbs.credentials["logginglevel"]
        self.initMethod = initmethod
        self.reactor = reactor
        self.ondestruct = ondestruct
        self.restartPlanned = False
        self.logger = logging.getLogger(__name__)
        self.init()

    def createClient(self):
        try:
            self.client = MissionControl(self.cnode,
                                         '/gs-guide-websocket',
                                         self.gsdbs,
                                         self.execute,
                                         self.ondestruct,
                                         self.restartCNode,
                                         60)
        except Exception as e:
            self.logger.exception("critical cant get connection"+ str(e))
            os._exit(0)

    def restartCNode(self, threadid):
        self.reactor.callFromThread(self.reactor.stop)
        # self.terminate()

    def checkThreadRunning(self):
        if not self.restartPlanned:
            if self.client is None or not self.client.is_alive():
                reactor.callFromThread(self.createClient)

    def terminate(self):
        # os.system("python main.py")
        # os.execl(sys.executable, self.gsdbs.creadPath, *sys.argv)
        # raise SystemExit(0)
        os._exit(0)
        # if self.restartPlanned:
        # else:

    def init(self):
        logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=self.logginglevel)
        if self.initMethod is not None:
            t1 = threading.Thread(target=self.initMethod, args=[self.gsdbs])
            t1.start()

        l = task.LoopingCall(self.checkThreadRunning)
        l.start(1.0)

        self.reactor.addSystemEventTrigger('before', 'shutdown', self.terminate)

        self.startreactor()

    def startreactor(self):
        if threading.current_thread() is threading.main_thread():
            self.reactor.run()
        else:
            self.reactor.run(installSignalHandlers=0)
