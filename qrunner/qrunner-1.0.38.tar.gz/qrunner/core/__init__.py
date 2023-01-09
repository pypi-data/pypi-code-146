import os
from qrunner.utils.log import logger
from qrunner.core.image.image_discern import ImageDiscern
from qrunner.core.ocr.ocr_discern import OCRDiscern


class ImageElem(object):
    """图像识别定位"""

    def __init__(self, driver, target_image: str):
        self.driver = driver
        self.target_image = target_image

    def exists(self, grade=0.8, gauss_num=111):
        logger.info(f'判断图片: {self.target_image} 是否存在')
        self.driver.screenshot(os.path.join(os.path.join(
            os.path.abspath('./Images/'), 'SourceImage.png')))
        res = ImageDiscern(self.target_image, grade, gauss_num).get_coordinate()
        return True if isinstance(res, tuple) else False

    def click(self, grade=0.8, gauss_num=111):
        logger.info(f'点击图片: {self.target_image}')
        self.driver.screenshot(os.path.join(os.path.join(
            os.path.abspath('./Images/'), 'SourceImage.png')))
        res = ImageDiscern(self.target_image, grade, gauss_num).get_coordinate()
        if isinstance(res, tuple):
            self.driver.click(res[0], res[1])
        else:
            raise Exception('为识别到图片，无法进行点击')


class OCRElem(object):
    """ocr识别定位"""

    def __init__(self, driver, text: str):
        self.driver = driver
        self.text = text

    def exists(self):
        logger.info(f'判断文本: {self.text} 是否存在')
        self.driver.screenshot('SourceImage.png')
        res = OCRDiscern().get_coordinate(self.text)
        return True if isinstance(res, tuple) else False

    def click(self):
        logger.info(f'点击文本: {self.text}')
        self.driver.screenshot('SourceImage.png')
        res = OCRDiscern().get_coordinate(self.text)
        if isinstance(res, tuple):
            self.driver.click(res[0], res[1])
            return
        else:
            raise Exception('通过OCR未识别指定文字或置信度过低，无法进行点击操作！')


if __name__ == '__main__':
    from qrunner.core.android.driver import AndroidDriver

    driver = AndroidDriver()
    # elem = OCRElem(driver, '查老板')
    # elem.click()

    elem = ImageElem(driver, 'tpl1670752017616.png')
    elem.click()
