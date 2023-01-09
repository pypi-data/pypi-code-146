import cv2
import time
import os
import shutil
import numpy as np
from froxiaofeidriver import mysound
from froxiaofeidriver.myvideo import Video


class Face(Video):
    xf=mysound.Sound()
    index_photo=0
    img1 = 0
    str_face = 0
    count = 1
    
    width = 320
    height = 240
    dim = (width,height) #压缩以后的视频尺寸
    
    
    
    def __init__(self):
        pass
    # 获取所有文件（人脸id）
    def get_face_list(self,path):
        for root,dirs,files in os.walk(path):
            if root == path:
                return dirs
    def collect(self,str_face_id1="face1",str_face_id2="face2",str_face_id3="face3"):
        
        os.chdir("/home/pi/AiCar/face")
        # 加载训练好的人脸检测器
        faceCascade = cv2.CascadeClassifier('/home/pi/AiCar/face/haarface.xml')
        if(os.path.exists("/home/pi/AiCar/face/face-collect")):
            shutil.rmtree("/home/pi/AiCar/face/face-collect")
            os.mkdir("/home/pi/AiCar/face/face-collect")
        else:
            os.mkdir("/home/pi/AiCar/face/face-collect")
        os.chdir("/home/pi/AiCar/face/face-collect")

        os.makedirs(str_face_id1) 
        os.makedirs(str_face_id2) 
        os.makedirs(str_face_id3)

        self.xf.faceStartCollect()
        time.sleep(4)
        # 打开摄像头
        # cap = cv2.VideoCapture(0)
        
        if str_face_id1 != "face1":
            
            while True:
          
                # 读取一帧图像
                success, img = self.cap.read()
            
                if not success:
                    continue
                
                # 转换为灰度
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                
                # 进行人脸检测
                faces = faceCascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(50, 50),flags=cv2.CASCADE_SCALE_IMAGE)
                
                # 画框
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 3)
                
                
                # 保存人脸
                for (x, y, w, h) in faces:
                    roi = img[y:y+h,x:x+w]
                    cv2.imwrite("/home/pi/AiCar/face/face-collect/%s/%d.jpg"%(str_face_id1,self.index_photo),roi)
                    self.index_photo = self.index_photo+1
                if self.index_photo == 20:
                    self.xf.faceFirstTwenty()
                    time.sleep(4)
                if self.index_photo == 40:
                    self.xf.faceMiddleTwenty()
                    time.sleep(4)
                if self.index_photo == 60:
                    self.xf.faceNextID()
                    time.sleep(4)
                    break
                
        self.index_photo = 0
        if str_face_id2 != "face2":
            
            while True:
          
                # 读取一帧图像
                success, img = self.cap.read()
            
                if not success:
                    continue
                
                # 转换为灰度
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                
                # 进行人脸检测
                faces = faceCascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(50, 50),flags=cv2.CASCADE_SCALE_IMAGE)
                
                # 画框
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 3)
                
                
                # 保存人脸
                for (x, y, w, h) in faces:
                    roi = img[y:y+h,x:x+w]
                    cv2.imwrite("/home/pi/AiCar/face/face-collect/%s/%d.jpg"%(str_face_id2,self.index_photo),roi)
                    self.index_photo = self.index_photo+1
                if self.index_photo == 20:
                    self.xf.faceFirstTwenty()
                    time.sleep(4)
                if self.index_photo == 40:
                    self.xf.faceMiddleTwenty()
                    time.sleep(4)
                if self.index_photo == 60:
                    self.xf.faceNextID()
                    time.sleep(4)
                    break
                
        self.index_photo = 0
        if str_face_id3 != "face3":
            
            while True:
          
                # 读取一帧图像
                success, img = self.cap.read()
            
                if not success:
                    continue
                
                # 转换为灰度
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                
                # 进行人脸检测
                faces = faceCascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(50, 50),flags=cv2.CASCADE_SCALE_IMAGE)
                
                # 画框
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 3)
                
                
                # 保存人脸
                for (x, y, w, h) in faces:
                    roi = img[y:y+h,x:x+w]
                    cv2.imwrite("/home/pi/AiCar/face/face-collect/%s/%d.jpg"%(str_face_id3,self.index_photo),roi)
                    self.index_photo = self.index_photo+1
                if self.index_photo == 20:
                    self.xf.faceFirstTwenty()
                    time.sleep(4)
                if self.index_photo == 40:
                    self.xf.faceMiddleTwenty()
                    time.sleep(4)
                if self.index_photo == 60:
                    self.xf.faceNextID()
                    time.sleep(4)
                    break
         
        self.xf.faceCollectEnd()
        time.sleep(4)
        cv2.destroyAllWindows()
        self.cap.release()
        os.chdir("../..")
        print(os.getcwd())

        # 创建人脸识别器
        recognizer = cv2.face.LBPHFaceRecognizer_create()

        # 用来存放人脸id的字典
        # 构建人脸编号 和 人脸id 的关系
        dic_face = {}

        # 人脸存储路径
        base_path = "/home/pi/AiCar/face/face-collect"
    
        # 获取人脸id
        face_ids = self.get_face_list(base_path)
        print(face_ids)
        # 用来存放人脸数据与id号的列表
        faceSamples=[]
        ids = []
    
        # 遍历人脸id命名的文件夹
        for i, face_id in enumerate(face_ids):
        
            # 人脸字典更新
            dic_face[i] = face_id
            
            # 获取人脸图片存放路径
            path_img_face = os.path.join(base_path,face_id)
        
            for face_img in os.listdir(path_img_face):
                # 读取以.jpg为后缀的文件
                if face_img.endswith(".jpg"):
                    file_face_img = os.path.join(path_img_face,face_img)
                
                    # 读取图像并转换为灰度图
                    img = cv2.imread(file_face_img)
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                
                    # 保存图像和人脸ID
                    faceSamples.append(img)
                    ids.append(i)
    
        print(dic_face)
    
        # 进行模型训练    
        recognizer.train(faceSamples, np.array(ids))

        # 模型保存 
        recognizer.save('/home/pi/AiCar/face/trainer.yml')                
    
        # 进行字典保存
        with open("/home/pi/AiCar/face/face_list.txt",'w') as f:
            for face_id in dic_face:
                f.write("%d %s\n"%(face_id,dic_face[face_id]))
        self.xf.faceTrainEnd()
        time.sleep(3)
    
    def read_dic_face(self,file_list):
        data = np.loadtxt(file_list,dtype='str')
        dic_face = {}
        for i in range(len(data)):
            dic_face[int(data[i][0])] = data[i][1]
        return dic_face
    
    def recognize(self):
        # 加载人脸字典
        dic_face = self.read_dic_face("/home/pi/AiCar/face/face_list.txt")
    
        # 加载Opencv人脸检测器
        faceCascade = cv2.CascadeClassifier('/home/pi/AiCar/face/haarface.xml')

        # 加载训练好的人脸识别器
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read('/home/pi/AiCar/face/trainer.yml')

        
        self.xf.faceStartRecognize()
        time.sleep(3)
        while True:
        
            # 读取一帧图像
            success, img = self.cap.read()
            #img = cv2.resize(img0, self.dim, interpolation = cv2.INTER_AREA) #压缩视频尺寸

            if not success:
                continue
        
            # 转换为灰度
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
            # 进行人脸检测
            faces = faceCascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(50, 50),flags=cv2.CASCADE_SCALE_IMAGE)
        
            # 遍历检测到的人脸
            for (x, y, w, h) in faces:
                # 画框
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 3)
            
                # 进行人脸识别 
                id_face, confidence = recognizer.predict(gray[y:y+h,x:x+w])
            
                # 检测可信度，这里是通过计算距离来计算可信度，confidence越小说明越近似 
                if (confidence < 35):
                    self.str_face = dic_face[id_face]
                    cv2.destroyAllWindows()
                    self.cap.release()
                    return self.str_face
                    
            cv2.waitKey(2)
            
        cv2.destroyAllWindows()
        self.cap.release()
    def face_detect(self):
            
        # 加载Opencv人脸检测器
        faceCascade = cv2.CascadeClassifier('/home/pi/AiCar/face/haarface.xml')
        
        while True:
        
            # 读取一帧图像
            success, img0 = self.cap.read()
            img = cv2.resize(img0, self.dim, interpolation = cv2.INTER_AREA) #压缩视频尺寸
            if not success:
                continue
        
            # 转换为灰度
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
            # 进行人脸检测
            faces = faceCascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(50, 50),flags=cv2.CASCADE_SCALE_IMAGE)
            # 遍历检测到的人脸
            for (x, y, w, h) in faces:
                # 画框
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 3)
                return 1,img
  
            return 0,img
    def face_5detect(self):
        while True:
            flag, self.img1 = self.face_detect()
            if flag == 1:
                self.count +=1
                if self.count == 6:
                    self.count = 6 
                return 1
            
            else:
                self.count -= 1
                if self.count == 0:
                    self.count = 1
                    return 0
                else:
                    return 1
    
    
    def cv2_show(self,name):
        cv2.imshow(name,self.img1)
        cv2.waitKey(1)
    def cv2_destroy(self):
        cv2.destroyAllWindows()
