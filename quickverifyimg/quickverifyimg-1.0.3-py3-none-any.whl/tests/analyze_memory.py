import os
import psutil
import time
import multiprocessing
from quickverifyimg.log.logger import get_logger
from quickverifyimg.quick_verify import QuickVerify
from quickverifyimg.quick_verify_simple import QuickVerifySimple
from quickverifyimg.quick_verify_video import QuickVerifyVideo
logger = get_logger(__name__)

def get_pid_memory(pid):
    """
    根据进程号来获取进程的内存大小
    :param pid: 进程id
    :return: pid内存大小/MB
    """
    process = psutil.Process(pid)
    mem_info = process.memory_info()
    print('当前进程占用内存：{:.2f} MB'.format(mem_info.rss / 1024 / 1024))
    return mem_info.rss / 1024 / 1024


def get_process_memory(process_name):
    """
    获取同一个进程名所占的所有内存
    :param process_name:进程名字
    :return:同一个进程名所占的所有内存/MB
    """
    total_mem = 0
    for i in psutil.process_iter():
        if i.name() == process_name:
            total_mem += get_pid_memory(i.pid)
    print('{:.2f} MB'.format(total_mem))
    return total_mem


def print_memory(pip):
    while True:
        get_pid_memory(pip)
        time.sleep(2)


def test(n):
    pid = os.getpid()
    print("Test PID:{}".format(pid))
    m = 2
    list = []
    for i in range(n):
        print("Test i{}...".format(i))
        m = m*5
        for item in range(m):
            list.append(item)
        time.sleep(1)
    return pid

def verify_video():
    origin_video = "./images/video/origin_video.mp4"
    target_video = "./images/video/target_video.mp4"
    crop_place = {"size": (0.48, 0.95), "offset": (0.13, 0)}
    verify_engine_list = [
        ('ac_tpl', 0.99),
        ('hist', 0.995)
    ]
    quick_v = QuickVerifyVideo(verify_engine_list, 0.8, crop_place=crop_place, background_similar=0.999)
    print(quick_v.verify_video_effect(origin_video, target_video))

def verify_img_simple():
    start_time = time.time()
    quick_v = QuickVerifySimple(verify_img_dir='../downloads/0_11377', backgroup_img_path='../downloads/background.png',
                          crop_place={"size": (0.815, 1.0), "offset": (0.175, 0)}, quick_verify=True, background_similar=0.998)
    verify_engine_list = [
        ('ac_tpl', 0.99),
        ('hist', 0.99)
    ]
    # 选择多个匹配算法，如果第一个匹配算法完成通过，即其他会被忽略
    ret = quick_v.mutliple_engine_verify(
        img_dir="../downloads/screenshot", verify_engine_list=verify_engine_list, match_rate_threshold=0.8)

    logger.info("结果：{}, 通过率：{}".format(ret['result'], ret["final_match_rate"]))
    logger.info('总耗时：{}'.format(time.time() - start_time))
    logger.info('失败截图：{}'.format(ret["verify_fail_screenshots"]))
    logger.info('非背景图总数：{}'.format(ret["available_screenshot_num"]))
    logger.info('非背景图：{}'.format(ret["available_screenshots"]))

def verify_img():
    start_time = time.time()
    quick_v = QuickVerify(verify_img_dir='../downloads/0_11377', backgroup_img_path='../downloads/background.png',
                          crop_place={"size": (0.815, 1.0), "offset": (0.175, 0)}, quick_verify=True)
    verify_engine_list = [
        ('ac_tpl', 0.99),
        ('hist', 0.99)
    ]
    # 选择多个匹配算法，如果第一个匹配算法完成通过，即其他会被忽略
    ret = quick_v.mutliple_engine_verify(
        img_dir="../downloads/screenshot", verify_engine_list=verify_engine_list, match_rate_threshold=0.8)

    logger.info("结果：{}, 通过率：{}".format(ret['result'], ret["final_match_rate"]))
    logger.info('总耗时：{}'.format(time.time() - start_time))
    logger.info('失败截图：{}'.format(ret["verify_fail_screenshots"]))
    logger.info('非背景图总数：{}'.format(ret["available_screenshot_num"]))
    logger.info('非背景图：{}'.format(ret["available_screenshots"]))

if __name__ == '__main__':

    # 待测试进程
    test_p = multiprocessing.Process(target=verify_img_simple)
    test_p.start()
    print("test_p PID:{}".format(test_p.pid))
    print("Main PID:{}".format(os.getpid()))

    # 分析内存进程
    test_m = multiprocessing.Process(target=print_memory, args=(test_p.pid,))
    test_m.start()

    test_p.join()
    test_m.terminate()
    test_m.join()
    test_m.close()
    test_p.terminate()
    test_p.close()