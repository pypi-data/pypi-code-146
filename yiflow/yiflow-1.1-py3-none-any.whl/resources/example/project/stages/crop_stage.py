import yiflow as yf


class CropStage(yf.Stage):

    def setup(self):
        pass

    def run(self, feed_dict):
        # 获取输入
        img = feed_dict['image']

        # 裁剪图片，crop_rect通过配置文件指定
        x1, y1, x2, y2 = self.crop_rect
        croped_img = img[y1:y2, x1:x2, :]

        # 返回输出
        feed_dict['image'] = croped_img
