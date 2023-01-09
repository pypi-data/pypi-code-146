import cv2
import time
import numpy as np
import mediapipe as mp
from PIL import Image,ImageFont,ImageDraw
from flask import Flask,render_template,Response,request,jsonify,redirect,url_for
from froxiaofeidriver.myvideo import Video

class Guester(Video):
    
    dic_guester={1:"识别结果:1",2:"识别结果:2",3:"识别结果:3",4:"识别结果:4",5:"识别结果:5",6:"识别结果:6",8:"识别结果:8",0:"识别结果:0"}
        
    # cap = cv2.VideoCapture(0)
    mpHands = mp.solutions.hands
    hands = mpHands.Hands()
    mpDraw = mp.solutions.drawing_utils
    c_guester = None
    p_guester = None
    str_show = ""
    img1 = 0
    
    def __init__(self):
#         super(Guester,self).__init__()
        pass
    
    def get_guester(self,img,list_lms):
        hull_index = [0,1,2,3,6,10,14,19,18,17]
        up_hull = [4,8,12,16,20]
        up_fingers = []
        guester = None
        
        hull = cv2.convexHull(list_lms[hull_index,:])
        cv2.polylines(img,[hull],True,(0,255,0),2)
        
        for i in up_hull:
            pt = (int(list_lms[i][0]),int(list_lms[i][1]))
            dist = cv2.pointPolygonTest(hull,pt,True)
            if dist < 0:
                up_fingers.append(i)
        
        if len(up_fingers) == 1 and up_fingers[0] == 8:
            guester = 1
        elif len(up_fingers) == 2 and up_fingers[0] == 8 and up_fingers[1] == 12:
            guester = 2
        elif len(up_fingers) == 3 and up_fingers[0] == 8 and up_fingers[1] == 12 and up_fingers[2] == 16:
            guester = 3
        elif len(up_fingers) == 4 and up_fingers[0] == 8 and up_fingers[1] == 12 and up_fingers[2] == 16 and up_fingers[3] == 20:
            guester = 4
        elif len(up_fingers) == 5:
            guester = 5
        elif len(up_fingers) == 2 and up_fingers[0] == 4 and up_fingers[1] == 20:
            guester = 6
        elif len(up_fingers) == 2 and up_fingers[0] == 4 and up_fingers[1] == 8:
            guester = 8
        elif len(up_fingers) == 0:
            guester = 0
         
        return guester
         
    def paint_chinese_opencv(self,im,chinese,pos,color,font_size=20):
        img_PIL = Image.fromarray(cv2.cvtColor(im,cv2.COLOR_BGR2RGB))
        font = ImageFont.truetype('/home/pi/AiCar/mylib/NotoSansCJK-Bold.otf',font_size,encoding="utf-8")
        fillColor = color
        position =pos
        
        draw = ImageDraw.Draw(img_PIL)
        draw.text(position,chinese,fillColor,font)
        img = cv2.cvtColor(np.asarray(img_PIL),cv2.COLOR_RGB2BGR)
        
        return img
    
    def get_gesture_img(self):
        
        while True:
            success,self.img1 = self.cap.read()
            if not success:
                continue
            image_height,image_width,_ = np.shape(self.img1)
            imgRGB = cv2.cvtColor(self.img1,cv2.COLOR_BGR2RGB)
            results = self.hands.process(imgRGB)
            
            if results.multi_hand_landmarks:
                hand = results.multi_hand_landmarks[0]
                self.mpDraw.draw_landmarks(self.img1,hand,self.mpHands.HAND_CONNECTIONS)
                list_lms = []
                for i in range(21):
                    pos_x = hand.landmark[i].x*image_width
                    pos_y = hand.landmark[i].y*image_height
                    list_lms.append([int(pos_x),int(pos_y)])
                
                list_lms = np.array(list_lms,dtype = np.int32)
                self.c_guester = self.get_guester(self.img1,list_lms)
                
                if not self.c_guester is None and self.c_guester != self.p_guester:
                    self.p_guester = self.c_guester
            if not self.p_guester is None:
                self.str_show = ' %s'%(self.dic_guester[self.p_guester])
            self.img1 = self.paint_chinese_opencv(self.img1,self.str_show,(10,10),(0,255,255),font_size=30)

        
            return self.p_guester
        cap.release()
         
    def gesture_web_video(self):
        
        while True:
            success,img = self.cap.read()
            if not success:
                continue
            image_height,image_width,_ = np.shape(img)
            imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            results = self.hands.process(imgRGB)
            
            if results.multi_hand_landmarks:
                hand = results.multi_hand_landmarks[0]
                self.mpDraw.draw_landmarks(img,hand,self.mpHands.HAND_CONNECTIONS)
                list_lms = []
                for i in range(21):
                    pos_x = hand.landmark[i].x*image_width
                    pos_y = hand.landmark[i].y*image_height
                    list_lms.append([int(pos_x),int(pos_y)])
                
                list_lms = np.array(list_lms,dtype = np.int32)
                self.c_guester = self.get_guester(img,list_lms)
                
                if not self.c_guester is None and self.c_guester != self.p_guester:
                    self.p_guester = self.c_guester
            if not self.p_guester is None:
                self.str_show = ' %s'%(self.dic_guester[self.p_guester])
            img = self.paint_chinese_opencv(img,self.str_show,(10,10),(0,255,255),font_size=30)

            ret,jpeg = cv2.imencode('.jpg',img)
            yield(b'--frame\r\n'+b'Content-Type:image/jpeg\r\n\r\n'+jpeg.tobytes()+b'\r\n\r\n')
        cap.release()
        
    def return_gesture(self):
        
        return self.p_guester
    
    def run(self):
         
        while True:
            gesture_flag, img = self.get_gesture_img() 
            ret,jpeg = cv2.imencode('.jpg',img)
            yield(b'--frame\r\n'+b'Content-Type:image/jpeg\r\n\r\n'+jpeg.tobytes()+b'\r\n\r\n')
    
    def cv2_show(self,name):
        cv2.imshow(name,self.img1)
        cv2.waitKey(1)

    def cv2_destroy(self):
        cv2.destroyAllWindows()
        
    def img_encode(self,img):
        ret,jpeg = cv2.imencode('.jpg',img)
        return jpeg
                
            