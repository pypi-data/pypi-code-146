import asyncio
import os

try:
    import aiohttp
except ModuleNotFoundError:
    raise ModuleNotFoundError("你没有安装aiohttp模块，请在终端输入'pip install aiohttp'安装此模块")


class ImageSave:
    """图片异步存储"""

    def __init__(self):
        self.astrict = None
        self.semaphore = None

    @staticmethod
    def create_path(iamge_path):  # 路径创建
        path = os.path.split(iamge_path)[0]
        if path:
            if os.path.exists(path):
                pass
            else:
                os.makedirs(path)

    async def job(self, session, url_data):
        async with self.semaphore:
            img = await session.get(url_data[0])  # 触发到await就切换，等待get到数据
            img_code = await img.read()  # 读取内容
            image_path = url_data[1]
            self.create_path(image_path)
            with open(str(image_path), 'wb') as f:
                f.write(img_code)

    async def create_session(self, loop, urls):
        timeout = aiohttp.ClientTimeout(total=5)  # 超时检测
        async with aiohttp.ClientSession(timeout=timeout) as session:  # 建立会话session
            tasks = [loop.create_task(self.job(session, url_data)) for url_data in urls]  # 建立所有任务
            await asyncio.wait(tasks)

    def create_loop(self, url_list):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.create_session(loop, url_list))

    def image_save(self, image_url, image_path, astrict=100):
        """单张图片保存"""
        self.astrict = astrict
        image_iteration = [[image_url, image_path]]
        self.semaphore = asyncio.Semaphore(self.astrict)  # 限制并发量为500
        self.data_detection(image_iteration)
        self.create_loop(image_iteration)

    def images_save(self, image_iteration, astrict=100):
        """多张图片保存[[链接：文件保存地址]]"""
        self.astrict = astrict
        self.semaphore = asyncio.Semaphore(self.astrict)  # 限制并发量为500
        self.data_detection(image_iteration)
        self.create_loop(image_iteration)

    @staticmethod
    def data_detection(iteration_data):
        for url_data in iteration_data:
            if 'http' != str(url_data[0][:4]).lower():
                raise ValueError('数据中的第一个参数不是一个链接，因为它没有携带http协议')
            if '.' not in str(url_data[1]):
                raise ValueError('数据中的第二个参数没有后缀名称')


image_save = ImageSave().image_save
images_save = ImageSave().images_save
