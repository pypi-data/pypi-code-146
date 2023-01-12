import re
import urllib
import urllib.parse
from dataclasses import dataclass, fields
import datetime as dt


@dataclass
class LogLine:
    ipAddress: str
    identd: str
    userId: str
    receivedAt: dt.datetime
    method: str
    path: str
    params: dict[str, str]
    potocol: str
    status_code: int
    return_size: int
    referer: str
    agent: str
    raw: str

    def dict(self):
        return {field.name: str(getattr(self, field.name)) for field in fields(self)}

    @staticmethod
    def read_log_lines(line):
        try:
            result = []

            I_IP = 0
            I_IID = 1
            I_UID = 2
            I_DATE = 3
            I_URL_S = 4
            I_URL_E = 5
            I_STATUS_S = 6
            I_STATUS_E = 7
            I_LENGTH = 8
            I_REFERER_S = 9
            I_REFERER_E = 10
            I_AGENT_S = 11
            I_AGENT_E = 12

            varIndex = 0
            buf = ""
            for c in line:
                if varIndex in [I_IP, I_IID, I_UID, I_STATUS_E, I_LENGTH] and c == " ":
                    if varIndex in [I_STATUS_E, I_LENGTH]:
                        result.append(int(buf))
                    else:
                        result.append(buf)
                    buf = ""
                    varIndex += 1
                elif varIndex in [I_DATE] and c == "[":
                    buf = ""
                elif varIndex in [I_DATE] and c == "]":
                    result.append(dt.datetime.strptime(buf, "%d/%b/%Y:%H:%M:%S %z"))
                    buf = ""
                    varIndex += 1
                elif varIndex in [I_URL_S, I_REFERER_S, I_AGENT_S] and c == "\"":
                    buf = ""
                    varIndex += 1
                elif varIndex in [I_URL_E] and c == "\"":
                    l = buf
                    if l in ["-", "\\n"]:
                        result.append("")
                        result.append("")
                        result.append({})
                        result.append("")
                    else:
                        # v1 => method
                        # v2 => path
                        # v3 => potocol
                        v1, v2, v3 = buf.split(" ")
                        vPath = v2.split("?")

                        v5d = {
                            (urllib.parse.unquote(pair[0]), urllib.parse.unquote(pair[1])) if len(pair) == 2 else (
                                urllib.parse.unquote(pair[0]), "")
                            for paramStr in vPath[1].split("&") if len(paramStr) > 0
                            for pair in [paramStr.split("=")]

                        } if len(vPath) == 2 else {}

                        result.append(urllib.parse.unquote(v1))
                        url = None
                        if re.match(urllib.parse.unquote_plus(vPath[0]), "[a-zA-Z0-9]{4}"):
                            url = urllib.parse.unquote_plus(url)
                        else:
                            url = urllib.parse.unquote_plus(vPath[0])
                        result.append(urllib.parse.unquote(url))

                        result.append(v5d)
                        result.append(urllib.parse.unquote(v3))
                    buf = ""
                    varIndex += 1
                elif varIndex in [I_REFERER_E, I_AGENT_E] and c == "\"":
                    result.append(buf)
                    buf = ""
                    varIndex += 1
                elif varIndex in [I_STATUS_S] and c == " ":
                    varIndex += 1
                else:
                    buf += c
            result.append(line)
            return result
        except Exception:
            print(line)
            raise
