
import aircv as ac
import cv2


def match_image(imsrc, imobj, confidencevalue=0.5):  # imgsrc=原始图像，imgobj=待查找的图片
    """
    大图找小图 (不会自动调整分辨率)
    :param imsrc:
    :param imobj:
    :param confidencevalue:
    :return:
    """
    # {'confidence': 0.5435812473297119, 'rectangle': ((394, 384), (394, 416), (450, 384), (450, 416)), 'result': (422.0, 400.0)}
    match_result = ac.find_template(imsrc, imobj, confidencevalue)
    if match_result is not None:
        match_result['shape'] = (imsrc.shape[1], imsrc.shape[0])  # 0为高，1为宽

    score = match_result["confidence"] if match_result else 0
    # print("match_score: {}".format(score))

    return round(score, 5)

if __name__ == '__main__':
    # image1 = cv2.imread('../downloads/screenshot/12.png')
    # image2 = cv2.imread('../downloads/0_11403/763.png')
    image1 = cv2.imread('../tests/images/video/origin_video_frame/1.png')
    image2 = cv2.imread('../tests/images/video/target_video_frame/526.png')

    image1 = cv2.imread('../tests/images/1.png')
    image2 = cv2.imread('../tests/images/3.png')
    print(match_image(image1, image2))


