import ctypes
import os

import win32api
import win32con
import win32gui
import win32process
import time
from PyQt5.QtCore import QThread, QWaitCondition, QMutex
from constants import const


class ScriptInter(QThread):
    # 构造函数
    def __init__(self):
        super().__init__()
        self.isBlock = False
        self.isCancel = False
        self.cond = QWaitCondition()
        self.mutex = QMutex()

    # 阻塞
    def block(self):
        self.isBlock = True
        const.status['paused'] = True
        const.UI.ui_signal.emit('status_pause', '暂停执行')

    # 恢复
    def resume(self):
        self.isBlock = False
        self.cond.wakeAll()
        const.status['paused'] = False
        const.UI.ui_signal.emit('status_pause', '继续执行')

    # 取消
    def cancel(self):
        self.isCancel = True
        const.status['paused'] = False
        const.status['running'] = False
        const.UI.ui_signal.emit('status_run', '完成执行')

    # 恢复
    def begin(self):
        const.status['running'] = True
        const.UI.ui_signal.emit('status_run', '开始执行')

    # 恢复
    def end(self):
        const.status['running'] = False
        const.UI.ui_signal.emit('status_run', '完成执行')

    #
    def mouse(self, action, x=-1, y=-1):
        # 线程锁on
        self.mutex.lock()
        if self.isBlock:
            self.cond.wait(self.mutex)
        # TODO=>待优化，应该一次结束后面的动作不再判断，而不是每个动作里都判断
        if self.isCancel:
            # TODO=>
            # self.valueChange.emit(0)
            return

        time.sleep(0.1)

        if action == 'move_to' and x != -1 and y != -1:
            # 挪动鼠标 普通做法
            ctypes.windll.user32.SetCursorPos(x, y)

        # 约定 [-1, -1] 表示鼠标保持原位置不动, 非move_to的动作就不需要传入坐标值，默认-1 -1
        elif action == 'left_single_click':
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            time.sleep(0.1)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        elif action == 'left_double_click':
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            time.sleep(0.1)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            time.sleep(0.1)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            time.sleep(0.1)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        elif action == 'left_long_press':
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        elif action == 'left_long_up':
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

        elif action == 'right_single_click':
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
            time.sleep(0.1)
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
        elif action == 'right_double_click':
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
            time.sleep(0.1)
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
            time.sleep(0.1)
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
            time.sleep(0.1)
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
        elif action == 'right_long_press':
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
        elif action == 'right_long_up':
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)

        elif action == 'middle_single_click':
            win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEDOWN, 0, 0, 0, 0)
            time.sleep(0.1)
            win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUP, 0, 0, 0, 0)
        elif action == 'middle_double_click':
            win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEDOWN, 0, 0, 0, 0)
            time.sleep(0.1)
            win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUP, 0, 0, 0, 0)
            time.sleep(0.1)
            win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEDOWN, 0, 0, 0, 0)
            time.sleep(0.1)
            win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUP, 0, 0, 0, 0)
        elif action == 'middle_long_press':
            win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEDOWN, 0, 0, 0, 0)
        elif action == 'middle_long_up':
            win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUP, 0, 0, 0, 0)

        elif action == 'wheel_up':
            win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, win32con.WHEEL_DELTA, 0)
        elif action == 'wheel_down':
            win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -win32con.WHEEL_DELTA, 0)

        # 线程锁off
        self.mutex.unlock()

    def keyboard(self, action, key_name):
        # 线程锁on
        self.mutex.lock()
        if self.isBlock:
            self.cond.wait(self.mutex)
        # TODO=>待优化，应该一次结束后面的动作不再判断，而不是每个动作里都判断
        if self.isCancel:
            # TODO=>
            # self.valueChange.emit(0)
            return

        time.sleep(0.2)

        if action == 'key_combine':
            for child_name in key_name:
                key_code = const.key_dict[child_name]
                win32api.keybd_event(key_code, 0, 0, 0)
            for child_name in key_name:
                key_code = const.key_dict[child_name]
                win32api.keybd_event(key_code, 0, win32con.KEYEVENTF_KEYUP, 0)
        else:
            key_code = const.key_dict[key_name]
            # keybd_event函数的第3个参数为0表示按下，为win32con.KEYEVENTF_KEYUP表示弹起；第2个参数和第4个参数都默认0就行
            if action == 'key':
                win32api.keybd_event(key_code, 0, 0, 0)
                time.sleep(0.2)
                win32api.keybd_event(key_code, 0, win32con.KEYEVENTF_KEYUP, 0)
            elif action == 'key_down':
                win32api.keybd_event(key_code, 0, 0, 0)
            elif action == 'key_up':
                win32api.keybd_event(key_code, 0, win32con.KEYEVENTF_KEYUP, 0)

        # 线程锁off
        self.mutex.unlock()

    def util(self, action, *args):
        func = getattr(self, action)
        return func(*args)

    def get_color(self, x, y):
        # 获取颜色值并得到对应的RGB值和16进制值
        hdc = ctypes.windll.user32.GetDC(None)  # 获取颜色值
        pixel = ctypes.windll.gdi32.GetPixel(hdc, x, y)  # 提取RGB值
        r = pixel & 0x0000ff
        g = (pixel & 0x00ff00) >> 8
        b = pixel >> 16

        hex_value = list(map(lambda x: str(hex(x)).replace('0x', '').upper(), [r, g, b]))
        color = '#{:0>2s}{:0>2s}{:0>2s}'.format(*hex_value)
        return color

    def wait(self, ms):
        # 休眠多少毫秒
        time.sleep(ms)

    def do_until(self, x, y, color, interval=0.1, timeout=1):
        start_time = time.time()
        while True:
            end_time = time.time()
            # 如果未超出时间限制，判断指定位置颜色是否符合预期
            if end_time - start_time < timeout:
                # 如果颜色符合预期直接结束，否则休眠一定时间再进行下一次判断
                if self.get_color(x, y) == color:
                    break
                else:
                    time.sleep(interval)
            # 如果超出时间限制，休眠一定时间再进行下一次判断
            else:
                break

    def open_file(self, filepath=None):
        if filepath is not None:
            os.startfile(filepath)

    def get_file_name(self, filepath=None):
        if filepath is not None:
            file_name = os.path.basename(filepath)
            file_name_no_ex = os.path.splitext(file_name)[0]
            return file_name, file_name_no_ex
        else:
            return None, None

    def send_text(self, text):
        handle = win32gui.GetForegroundWindow()
        process_id = win32process.GetWindowThreadProcessId(handle)[0]

        thread_id = win32api.GetCurrentThreadId()

        win32process.AttachThreadInput(process_id, thread_id, True)

        win32api.SendMessage(win32api.GetFocus(), win32con.WM_SETTEXT, 0, text)

    def get_files(self, dir_path, ex):
        files = []
        for file_name in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file_name)
            if os.path.isfile(file_path) and file_name.endswith(ex):
                files.append(file_path)
        return files

    # 特别注意，线程的开始不是直接调用run方法，而是调用start；否则仍然是阻塞状态，就像没使用线程一样的普通调用
    # 要发挥线程的效果就必须使用start()来开始运行线程任务
    # 运行(入口)
    def run(self):
        self.begin()
        run_times = const.UI.get_run_times()
        for time in range(run_times):
            self.execute()
        self.end()

    def execute(self, x, y):
        pass
