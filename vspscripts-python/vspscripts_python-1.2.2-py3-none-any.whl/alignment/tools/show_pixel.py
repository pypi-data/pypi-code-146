import cv2
import argparse

def parse_args():
    parser = argparse.ArgumentParser('parser for alignment')
    parser.add_argument("--data_path", type=str, default='../samples/GP2S___977_11.jpg')

    return parser.parse_args()

args = parse_args()
img = cv2.imread(args.data_path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

def mouse_click(event, x, y, flags, para):
    if event == cv2.EVENT_LBUTTONDOWN:
        print('PIX:', x, y)
        print("BGR:", img[y, x])
        print("GRAY:", gray[y, x])
        print("HSV:", hsv[y, x])


if __name__ == '__main__':
    cv2.namedWindow("img")
    cv2.setMouseCallback("img", mouse_click)
    while True:
        cv2.imshow('img', img)
        if cv2.waitKey() == ord('q'):
            break
    cv2.destroyAllWindows()
