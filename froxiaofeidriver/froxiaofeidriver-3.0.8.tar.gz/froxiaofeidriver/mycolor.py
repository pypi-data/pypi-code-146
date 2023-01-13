import cv2
import numpy as np
from froxiaofeidriver.myvideo import Video

#可以检测红色、绿色、蓝色、黄色、紫色、橙色
class Color(Video):
    count = 0
    last_color = 0
    img1 = 0
    width = 320
    height = 240
    dim = (width,height) #压缩以后的视频尺寸
    
    font= cv2.FONT_HERSHEY_SIMPLEX
    lower_red=np.array([0,166,217])#红色阈值下界
    higher_red=np.array([10,255,255])#红色阈值上界

    lower_green=np.array([44,164,99])#绿色阈值下界
    higher_green=np.array([84,255,255])#绿色阈值上界

    lower_blue=np.array([63,127,255])#蓝色阈值下界
    higher_blue=np.array([179,255,255])#蓝色阈值上界

    lower_yellow=np.array([26,95,206])#黄色阈值下界
    higher_yellow=np.array([41,255,255])#黄色阈值上界

    lower_violet=np.array([131,110,153])#紫色阈值下界
    higher_violet=np.array([160,255,255])#紫色阈值上界

    lower_orange=np.array([0,91,255])#橙色阈值下界
    higher_orange=np.array([23,255,255])#橙色阈值上界

    # cap=cv2.VideoCapture(0)#打开摄像头
    
    def __init__(self):
        pass
    #单次检测颜色
    def color_detect(self):
        while True:
            ret,img=self.cap.read()#按帧读取，这是读取一帧
            frame = cv2.resize(img, self.dim, interpolation = cv2.INTER_AREA) #压缩视频尺寸
            img_hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV) #把BGR转换为HSV色域
            mask_red = cv2.inRange(img_hsv,self.lower_red,self.higher_red)#可以认为是过滤出红色部分，获得红色的掩膜
            mask_red = cv2.medianBlur(mask_red, 7)  # 中值滤波
            mask_green = cv2.inRange(img_hsv,self.lower_green,self.higher_green)#获得绿色部分掩膜
            mask_green = cv2.medianBlur(mask_green, 7)  # 中值滤波
            mask_blue = cv2.inRange(img_hsv,self.lower_blue,self.higher_blue)#获得蓝色部分掩膜
            mask_blue = cv2.medianBlur(mask_blue, 7)  # 中值滤波
            mask_yellow =cv2.inRange(img_hsv,self.lower_yellow,self.higher_yellow)#获得黄色部分掩膜
            mask_yellow = cv2.medianBlur(mask_yellow, 7)  # 中值滤波
            mask_violet =cv2.inRange(img_hsv,self.lower_violet,self.higher_violet)#获得紫色部分掩膜
            mask_violet = cv2.medianBlur(mask_violet, 7)  # 中值滤波
            mask_orange =cv2.inRange(img_hsv,self.lower_orange,self.higher_orange)#获得橙色部分掩膜
            mask_orange = cv2.medianBlur(mask_orange, 7)  # 中值滤波
        
            cnts1,hierarchy1=cv2.findContours(mask_red,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)    #红色轮廓检测
            cnts2,hierarchy2=cv2.findContours(mask_green,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)  #绿色轮廓检测
            cnts3,hierarchy3=cv2.findContours(mask_blue,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)   #蓝色轮廓检测
            cnts4,hierarchy4=cv2.findContours(mask_yellow,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) #黄色轮廓检测
            cnts5,hierarchy5=cv2.findContours(mask_violet,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) #紫色轮廓检测
            cnts6,hierarchy6=cv2.findContours(mask_orange,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) #橙色轮廓检测
        
            for cnt in cnts1:
                (x,y,w,h)=cv2.boundingRect(cnt)#该函数返回矩阵四个点
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)#将检测到的红色框起来
                cv2.putText(frame,'red',(x,y-5),self.font,0.7,(0,0,255),2)
                return 'red',frame

            for cnt in cnts2:
                (x, y, w, h) = cv2.boundingRect(cnt)  # 该函数返回矩阵四个点
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # 将检测到的绿色框起来
                cv2.putText(frame, 'green', (x, y - 5), self.font, 0.7, (0,255,0), 2)
                return 'green',frame
                
            for cnt in cnts3:
                (x, y, w, h) = cv2.boundingRect(cnt)  # 该函数返回矩阵四个点
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)  # 将检测到的蓝色框起来
                cv2.putText(frame, 'blue', (x, y - 5), self.font, 0.7, (255,0,0), 2)
                return 'blue',frame
            
            for cnt in cnts4:
                (x, y, w, h) = cv2.boundingRect(cnt)  # 该函数返回矩阵四个点
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)  # 将检测到的黄色框起来
                cv2.putText(frame, 'yellow', (x, y - 5), self.font, 0.7, (0,255,255), 2)
                return 'yellow',frame
            
            for cnt in cnts5:
                (x, y, w, h) = cv2.boundingRect(cnt)  # 该函数返回矩阵四个点
                cv2.rectangle(frame, (x, y), (x + w, y + h), (240, 32, 160), 2)  # 将检测到的紫色框起来
                cv2.putText(frame, 'violet', (x, y - 5), self.font, 0.7, (240,32,160), 2)
                return 'violet',frame
                
            for cnt in cnts6:
                (x, y, w, h) = cv2.boundingRect(cnt)  # 该函数返回矩阵四个点
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 97, 255), 2)  # 将检测到的橙色框起来
                cv2.putText(frame, 'orange', (x, y - 5), self.font, 0.7, (0,97,255), 2)
                return 'orange',frame
            
            return 'No',frame
    #多次检测颜色算一次，避免视频托帧返回多次数据 
    def color_5detect(self):
        while True:
            color,self.img1 = self.color_detect()
            if color != 'No':
                if color == self.last_color:
                    self.count +=1
                    if self.count == 35:
                        self.count = 0
                        return color
            else:
                 return color
            self.last_color = color
                
    #显示视频，只能在python版实验中运行，不能在按键启动中运行，否则按键会启动不了app.py文件
    def cv2_show(self,name):
        cv2.imshow(name,self.img1)
        cv2.waitKey(1)

    def cv2_destroy(self):
        cv2.destroyAllWindows()
            

            
            
            
            
            
            
            
            
            
            
            
            
            
            
        