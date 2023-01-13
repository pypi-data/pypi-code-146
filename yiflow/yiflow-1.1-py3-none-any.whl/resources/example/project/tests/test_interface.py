import cv2
import argparse

from project.interface import AlgorithmInterface


def test(image_path, config):
    # 读取图片
    req = dict(
        imageName=image_path,
        imageData=cv2.imread(image_path)
    )

    # 实例化接口
    interface = AlgorithmInterface(config_file=config)
    resp = interface(req)

    alarm = resp['alarm']
    print("Alarm signal:", alarm)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--image', type=str, default="path/to/default/image", help="测试用的样例图片")
    parser.add_argument('-c', '--config', type=str, default=None, help="测试用配置文件，如为None则使用setting.ini中的配置")
    args = parser.parse_args()

    test(args.image, args.config)