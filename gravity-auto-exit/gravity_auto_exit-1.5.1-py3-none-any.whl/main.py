import datetime
import logging
import threading
import time
import uuid
from cad.main import CAD
from whikoperator.main import Wpicoperator
import requests
from gravity_auto_exit.logger import logger
from neurocore_worker.main import NeuroCoreWorker


class AutoExit:
    def __init__(self, cam_host, cam_login, cam_password,
                 neurocore_login, neurocore_password,
                 auth_method='Digest', engine_callback=None,
                 reload_time=15, debug=False,
                 detection_amount=4, failed_callback=None,
                 fail_callback_react_amount=2, fail_reload_time=1.5,
                 active=True, resize_photo: tuple = False, cam_port=80,
                 catch_event='Line Crossing',
                 simple_callback_func=None):
        self.simple_callback_func = simple_callback_func
        self.neurocore_worker = NeuroCoreWorker(
            api_login=neurocore_login,
            api_password=neurocore_password,
            plate_frame_size=resize_photo)
        self.cad = CAD(host=cam_host, port=cam_port, login=cam_login,
                       password=cam_password,
                       callback_func=self.cad_callback_func,
                       delay_time=0,
                       logger=logger,
                       catch_event=catch_event)
        cam_ip = cam_host.replace('http://', '')
        cam_ip = f"{cam_ip}:{cam_port}"
        self.reload_time = reload_time
        self.active = active
        self.resize_photo = resize_photo
        self.fail_callback_react_amount = fail_callback_react_amount
        self.fail_reload_time = fail_reload_time
        self.cam = Wpicoperator(cam_ip=cam_ip,
                                cam_login=cam_login,
                                cam_pass=cam_password,
                                auth_method=auth_method)
        self.callback_request_url = None
        self.debug = debug
        self.count = 0
        self.fail_count = 0
        self.detection_amount = detection_amount
        self.last_take = datetime.datetime.now()
        self.failed_callback = failed_callback
        # threading.Thread(target=self.counter_checker).start()
        self.engine_callback = engine_callback
        logger.info('AUTO_EXIT has started successfully')

    def set_active(self, activity_bool: bool):
        self.active = activity_bool

    def start(self):
        self.cad.mainloop()

    def save_pic(self, pic_name, pic_body, frmt='.jpg'):
        logger.debug(f'Saving picture {pic_name}')
        with open(pic_name + frmt, 'wb') as fobj:
            fobj.write(pic_body)
        logger.debug("Success!")

    def cad_callback_func(self, data=None):
        if self.simple_callback_func:
            threading.Thread(target=self.simple_callback_func).start()
        if not self.active:
            logging.debug("It is not active")
            return
        logger.debug(f'self.count: {self.count}')
        if datetime.datetime.now() - self.last_take > datetime.timedelta(
                seconds=self.reload_time):
            logger.debug(f'Working')
            response = self.camera_and_recognise()
            if 'error' in response:
                return response
            result, photo = response
            if result:
                self.last_take = datetime.datetime.now()
                return result
            else:
                time.sleep(2)
                for i in range(4):
                    logger.debug(f'Неудачное считывание! {self.fail_count}')
                    response = self.camera_and_recognise()
                    if 'error' in response:
                        return response
                    result, photo = response
                    if result:
                        self.last_take = datetime.datetime.now()
                        return result
                    elif self.failed_callback and i == 1:
                        logger.warning('Неудачное считывание!')
                        self.failed_callback()
                    time.sleep(1)

    def camera_and_recognise(self):
        result = self.try_recognise_plate()
        if 'error' in result:
            return result
        photo, result = result['photo'], result['number']
        if result:
            if self.debug:
                self.save_pic(f"{str(uuid.uuid4())}.jpg", photo)
            if self.engine_callback:
                threading.Thread(target=self.engine_callback,
                                 args=(result, photo)).start()
            if self.callback_request_url:
                threading.Thread(target=self.http_callback,
                                 kwargs={'number': result}).start()
        return result, photo

    def http_callback(self, number):
        requests.post(self.callback_request_url,
                      params={'number': number})

    def try_recognise_plate(self):
        logger.debug(f'Taking photo...')
        photo = self.cam.take_shot()
        result = self.neurocore_worker.get_car_number(photo)
        return result

    def set_post_request_url(self, url):
        self.callback_request_url = url
        return url

    def counter_checker(self):
        count_time = datetime.datetime.now()
        count_now = self.count
        while True:
            if self.count != count_now:
                logger.debug('Abort checker internal counter')
                count_now = self.count
                count_time = datetime.datetime.now()
            if count_now != 0 and self.count == count_now and (
                    datetime.datetime.now() - count_time > datetime.timedelta(
                seconds=5)):
                logger.debug('Abort self.count')
                self.count = 0
                self.fail_count = 0
            time.sleep(1)


class CADEntrance(AutoExit):
    """ Детекция автомобиля на брутто """
    pass


if __name__ == '__main__':
    def engine_callback(*args, **kwargs):
        print('k')

    inst = AutoExit(  # 'http://172.16.6.176',
        'http://127.0.0.1',
        'admin',
        'Assa+123',
        debug=True,
        cam_port=82,
        neurocore_login='admin',
        neurocore_password='admin',
        engine_callback=engine_callback
    )
    # inst.set_post_request_url('http://127.0.0.1:8080/start_auto_exit')
    #res = inst.try_recognise_plate()
    inst.start()
