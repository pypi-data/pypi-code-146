import json
import os
import re
import aiohttp
import jwt
import pendulum
import time
import uuid
import asyncio
from datetime import datetime, timedelta
from nerualpha.IBridge import IBridge


class Bridge(IBridge):
    def testRegEx(self, str, regExp):
        if re.match(regExp, str):
            return True
        else:
            return False

    def isInteger(self, value):
        try:
            int(value)
            return True
        except ValueError:
            return False

    def substring(self, str, start, end):
        return str[start:end]

    def jsonStringify(self, data):
        return json.dumps(data, default=lambda o: o.reprJSON(),
                          sort_keys=True, indent=4)

    def jsonParse(self, str):
        return json.loads(str)

    def getEnv(self, name):
        return os.getenv(name)

    async def request(self, params):
        try:
            if not hasattr(params, 'url'):
                raise Exception('url is required')

            url = params.url.host + '/' + params.url.pathname if params.url.pathname else params.url.host
            data = params.data
            headers = params.headers if params.headers is not None else {}
            query = params.url.query if hasattr(params.url, 'query') and params.url.query is not None else {}
            method = params.method

            if 'Content-Type' in headers:
                if headers['Content-Type'] == 'multipart/form-data':
                    # Delete multipart/form-date header to let aiohttp calculate its length
                    del headers['Content-Type']
                elif headers['Content-Type'] == 'application/json':
                    if hasattr(data, 'reprJSON'):
                        data = data.reprJSON()
                    data = json.dumps(data)

            async with aiohttp.ClientSession() as session:
                async with session.request(method, url, data=data, headers=headers, params=query) as resp:
                    if resp.content_type == 'application/json':
                        return await resp.json()
                    else:
                        return await resp.text()
        except Exception as e:
            print("Exception in request")
            raise e

    def runBackgroundTask(self, task):
        loop = asyncio.get_event_loop()
        loop.create_task(task)

    def createReadStream(self, path):
        return open(path, 'rb')

    async def requestWithoutResponse(self, params):
        await self.request(params)

    def uuid(self):
        return str(uuid.uuid4())

    def isoDate(self):
        dt = pendulum.now("UTC")
        return dt.to_iso8601_string()

    def toISOString(self, seconds):
        dt = pendulum.now("UTC")
        nt = dt.add(seconds=seconds)
        return nt.to_iso8601_string()

    def jwtSign(self, payload, privateKey, algorithm):
        return jwt.encode({
            'api_application_id': payload.api_application_id,
            'api_account_id': payload.api_account_id,
            'exp': payload.exp,
            'aud': payload.aud,
            'sub': payload.sub,
            'iss': payload.iss,
        }, privateKey, algorithm)

    def jwtVerify(self, token, privateKey, algorithm):
        return jwt.decode(token, privateKey, algorithm)

    def jwtDecode(self, token):
        return jwt.decode(token, options={"verify_signature": False})

    def getSystemTime(self):
        return int(time.time())

    def log(self, logAction):
        print(logAction)

    def getObjectKeys(self, obj):
        return list(obj.keys())
