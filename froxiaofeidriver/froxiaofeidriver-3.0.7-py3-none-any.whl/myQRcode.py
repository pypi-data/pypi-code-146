import qrcode
import cv2
import numpy as np
import time
from froxiaofeidriver.myvideo import Video

class QRcode(Video):
    code_path = "/home/pi/AiCar/file/"
    # cap = cv2.VideoCapture(0)
    QR_detector = cv2.QRCodeDetector()
#     flag_now = 'No'
    flag_pass = 'No'
    img1 = 0
    count = 0
    width = 320
    height = 240
    dim = (width,height) #压缩以后的视频尺寸，避免视频帧过大造成显示卡顿
    
    def __init__(self):
        pass
    def create_QRcode(self,s):
        file_img = self.code_path + s +'.png'
        img = qrcode.make(s)
        img.save(file_img)
        
        img = cv2.imread(file_img)
        cv2.putText(img,s,(0,20),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,0),1)
        cv2.imwrite(file_img,img)
        
    def detect_QRcode(self):
        
        while True:
            success,img0 = self.cap.read()
            self.img1 = cv2.resize(img0, self.dim, interpolation = cv2.INTER_AREA)#视频帧压缩
            if success:
                flag_now,AA,BB = self.QR_detector.detectAndDecode(self.img1)
                if flag_now:
                    if flag_now == self.flag_pass:
                        self.count += 1
                        if self.count == 5:
                            self.count = 0
                            return flag_now
                        
                    self.flag_pass = flag_now
                else:
                    self.count = 0
                    return flag_now
    def QRcode_num(self,num):
        return int(num)
    
                
    def cv2_show(self,name):
        
        cv2.imshow(name,self.img1)
        cv2.waitKey(1)

    def cv2_destroy(self):
        cv2.destroyAllWindows()
                    
                    
            
            
            
            
    