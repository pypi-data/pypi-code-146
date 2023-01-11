# coding: utf-8
#

import base64
import io
import json
import os
import sys
import traceback
import time
import threading

import tornado
from logzero import logger
from PIL import Image
from tornado.escape import json_decode, url_escape
import tornado.websocket
from tornado.ioloop import IOLoop
import asyncio

from ..device import connect_device, get_device
from ..version import __version__
from .page import BaseHandler
from .. import idbUtil,adbUtil
from .. import monitor
from .. import winUtil


class DeviceListHandler(BaseHandler):
    def get(self):
        try:
            deviceinfo_list = []
            util_list = [adbUtil,idbUtil]
            for util in util_list:
                device_list = util.GetConnectedDevice()
                for device in device_list:
                    deviceinfo = util.GetDeviceInfo(device)
                    deviceinfo_list.append(deviceinfo)
            if sys.platform=="win32":
                deviceinfo_list.append(winUtil.get_pc_info())
            self.write({"data":deviceinfo_list})
        except Exception as e:
            logger.error("get device list error: %s",traceback.format_exc())
            self.set_status(500)
            self.write({
                "success": False,
                "description": traceback.format_exc(),
            })

class PackageListHandler(BaseHandler):
    def get(self,deviceinfo):
        try:
            logger.info("select device is %s"%deviceinfo)
            deviceid = deviceinfo.split('|')[0]
            util = adbUtil
            if "iPhone" in deviceinfo or 'iOS' in deviceinfo:
                util = idbUtil
            elif "windows" in deviceinfo.lower():
                util = winUtil
            app_list = util.get_app_list(deviceid)
            self.write({"data":app_list})
        except Exception as e:
            logger.error("get package list error: %s",traceback.format_exc())
            self.set_status(500)
            self.write({
                "success": False,
                "description": traceback.format_exc(),
            })

class DeviceAPPHandler(BaseHandler):
    def post(self):
        try:
            deviceinfo = self.get_argument("deviceinfo")
            package = self.get_argument("package").split('--')[-1]
            deviceid = deviceinfo.split('|')[0]
            util = adbUtil
            if "iPhone" in deviceinfo or 'iOS' in deviceinfo:
                util = idbUtil
            util.start_app(deviceid,package)
        except Exception as e:
            logger.error("start app error: %s",traceback.format_exc())
            self.set_status(500)
            self.write({
                "success": False,
                "description": traceback.format_exc(),
            })


class PerfCaptrueHandler(tornado.websocket.WebSocketHandler):
    def initialize(self):
        self.device_read_thread = {}
        self.interval_time = 5

    def on_close(self):
        logger.warning("websocket closed, cleanup")

    async def prepare(self):
        pass

    def send_keyboard_interrupt(self):
       monitor.stop_all()

    async def open(self):
        logger.debug("websocket opened")

    def write2(self, data):
        self.write_message(json.dumps(data))

    async def on_message(self, message):
        logger.info("Receive:%s", message)
        data = json.loads(message)
        device,platform,package,action = data['device'],data['platform'],data['package'],data['action']
        file_name = data['filename']
        self.interval_time = data['intervaltime']
        save_detail = data.get('save_detail',False)
        divided_core_nums = data.get('divided_core_nums', False)
        logger.info(f"自定义文件名：{file_name},是否保存详细数据：{save_detail}")
        device = device.split('|')[0]
        package = package.split('--')[-1]
        if action=='start':
            monitor.start_captrue(platform, device, package, file_name, save_detail, divided_core_nums)
            self.device_read_thread[device] = True
            th = threading.Thread(target=self.read_perf_data,args=(device,))
            th.setDaemon(True)
            th.start()
        elif action=='stop':
            self.device_read_thread[device] = False
            filepath = monitor.get_perf_file_name(device)
            del self.device_read_thread[device]
            time.sleep(2)
            monitor.stop_captrue(device)
            self.write2({"action":"stop","filepath":filepath})
        elif action=='change':
            logger.info(f'设置数据刷新时间间隔：{self.interval_time}s')
        else:
            logger.warning("Unknown received message: %s", data)

    def read_perf_data(self,device):
        asyncio.set_event_loop(asyncio.new_event_loop())
        while True:
            if device not in self.device_read_thread or self.device_read_thread[device] is False:
                break
            data = monitor.read_perf_data(device)
            if data:
                self.write2(data)
            time.sleep(int(self.interval_time))

class ExportDataHandler(BaseHandler):
    async def get(self,filepath,save_filename):
        logger.info(f'导出文件：{filepath},自定义文件名：{save_filename}')
        if os.path.exists(filepath) is False:
            logger.info('文件不存在：'+filepath)
            self.set_status(500)
            self.write({
                "success": False,
                "description": '文件不存在：'+filepath
            })
            return
        content = open(filepath,mode='r',encoding='utf-8').read()
        sio = io.BytesIO()
        sio.write(content.encode('utf-8'))
        if not save_filename:
            save_filename = os.path.basename(filepath)
        if not save_filename.endswith(".csv"):
            save_filename += ".csv"
        logger.info(f"导出后的文件名为：{save_filename}")
        self.set_header('Content-Type', 'text/csv')
        self.set_header('Content-Disposition',
                        'attachment; filename={}'.format(url_escape(save_filename)))
        self.write(sio.getvalue())
