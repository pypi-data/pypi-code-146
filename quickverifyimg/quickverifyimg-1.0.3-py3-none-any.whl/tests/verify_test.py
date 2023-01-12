import time

from quickverifyimg.log.logger import get_logger
from quickverifyimg.quick_verify import QuickVerify
from quickverifyimg.quick_verify_simple import QuickVerifySimple

logger = get_logger(__name__)

if __name__ == '__main__':
    """
    crop_place：{ size: 需要识别的区域的大小， 百分比, offset: 需要识别的区域的左上角坐标点位置， 百分比}
    quick_verify: 是否快速校验，即不对已校验过的对照集图片继续校验
    """
    quick_v = QuickVerifySimple(verify_img_dir='../downloads/0_11377', backgroup_img_path='./images/background.png', crop_place={"size": (0.815, 1.0), "offset": (0.175, 0)},  quick_verify=True)
    start_time = time.time()
    # 选择使用的图片匹配算法和阈值
    # ac_tpl：模版匹配：大图找小图，速度快推荐
    # hist: 直方图匹配：速度一般，效果
    # ssim: ssim匹配算法：精准，速度不快，适合作为第二个算法补充
    # psnr: 峰值信噪比算法：目前只判断40以上为匹配，即认为相似度0.999
    # hash_p: 感知哈希算法：速度快，效果一般
    # hash_a: 均值哈希算法：速度快，效果一般
    # hash_d: 查值哈希算法：速度快，效果一般
    verify_engine_list = [
        ('ac_tpl', 0.99),
        ('hist', 0.995)
    ]
    # 选择多个匹配算法，如果第一个匹配算法完成通过，即其他会被忽略
    ret = quick_v.mutliple_engine_verify(
        img_dir="../downloads/screenshot", verify_engine_list=verify_engine_list, match_rate_threshold=0.8)

    logger.info("结果：{}, 通过率：{}".format(ret['result'], ret["final_match_rate"]))
    logger.info('总耗时：{}'.format(time.time() - start_time))
    logger.info('失败截图：{}'.format(ret["verify_fail_screenshots"]))
    logger.info('非背景图总数：{}'.format(ret["available_screenshot_num"]))
    logger.info('非背景图：{}'.format(ret["available_screenshots"]))