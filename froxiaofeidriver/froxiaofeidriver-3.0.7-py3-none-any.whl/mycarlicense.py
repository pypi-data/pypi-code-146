import cv2
from hyperlpr import HyperLPR_plate_recognition
from froxiaofeidriver.myvideo import Video
from froxiaofeidriver import mytts
import numpy as np
import onnxruntime as ort
import time
import os
import shutil

voice = mytts.Pyttsx()


class License(Video):
    result = 0
    lic_list = [1,2,3,4] #车牌清单，只用了第一个
    lic_count = [0,0,0,0] #车牌识别顺序，第0个是第一张，第1个是第2张，第2个是第三张，只有这三张都有才会保存三张图片文件
    imgA1 = 0  #第一张图片
    imgA2 = 0  #第二张图片
    imgA3 = 0  #第三张图片

    imgA1_flag = 0  #同一处的违章只保留一张，判定第一张是否有
    imgA2_flag = 0  #同一处的违章只保留一张，判定第二张是否有
    imgA3_flag = 0  #同一处的违章只保留一张，判定第三张是否有
    
    car_path = "/home/pi/AiCar/file/license"  #抓拍图片存储路径
    model_pb_path = "/home/pi/AiCar/mylib/car.onnx"  #识别小汽车的模型
    img1 = 0
    
    # 标签字典
    dic_labels= {0:'car'} #模型分类，可以进行识别汽车
    
    # 模型参数
    model_h = 320
    model_w = 320
    nl = 3
    na = 3
    stride=[8.,16.,32.]
    anchors = [[10, 13, 16, 30, 33, 23], [30, 61, 62, 45, 59, 119], [116, 90, 156, 198, 373, 326]]
    anchor_grid = np.asarray(anchors, dtype=np.float32).reshape(nl, -1, 2)

    posion_A1 = (50,300)  #起始线白线左起点
    posion_A2 = (600,300) #起始线白线右终点
    posion_B1 = (50,70)   #对面起始线左起点
    posion_B2 = (600,70)  #对面起始线右终点
    
    if(os.path.exists(car_path)):
        shutil.rmtree(car_path)
        os.mkdir(car_path)
    else:
        os.mkdir(car_path)
    os.chdir(car_path)
        
    so = ort.SessionOptions()
    net = ort.InferenceSession(model_pb_path, so)
    
    
    
    def __init__(self):
        pass
    
    def get_car_license(self):
        while True:
            success,self.img1 = self.cap.read()
            if not success:
                continue
            
            result = HyperLPR_plate_recognition(self.img1)
            
            if len(result) != 0:
                return result[0][0]
            else:
                return 0
    def cv2_show(self,name):
        cv2.imshow(name,self.img1)
        cv2.waitKey(1)

    def cv2_destroy(self):
        cv2.destroyAllWindows()
    
    def plot_one_box(self,x, img, color=None, label=None, line_thickness=None):
        """
        description: Plots one bounding box on image img,
                     this function comes from YoLov5 project.
        param: 
            x:      a box likes [x1,y1,x2,y2]
            img:    a opencv image object
            color:  color to draw rectangle, such as (0,255,0)
            label:  str
            line_thickness: int
        return:
            no return
        """
        tl = (
            line_thickness or round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1
        )  # line/font thickness
        color = color or [random.randint(0, 255) for _ in range(3)]
        c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
        cv2.rectangle(img, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
        if label:
            tf = max(tl - 1, 1)  # font thickness
            t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
            c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
            cv2.rectangle(img, c1, c2, color, -1, cv2.LINE_AA)  # filled
            cv2.putText(
                img,
                label,
                (c1[0], c1[1] - 2),
                0,
                tl / 3,
                [225, 255, 255],
                thickness=tf,
                lineType=cv2.LINE_AA,
            )
        
    def _make_grid(self,nx, ny):
        xv, yv = np.meshgrid(np.arange(ny), np.arange(nx))
        return np.stack((xv, yv), 2).reshape((-1, 2)).astype(np.float32)
    
    def cal_outputs(self,outs,nl,na,model_w,model_h,anchor_grid,stride):
    
        row_ind = 0
        grid = [np.zeros(1)] * nl
        for i in range(nl):
            h, w = int(model_w/ stride[i]), int(model_h / stride[i])
            length = int(na * h * w)
            if grid[i].shape[2:4] != (h, w):
                grid[i] = self._make_grid(w, h)

            outs[row_ind:row_ind + length, 0:2] = (outs[row_ind:row_ind + length, 0:2] * 2. - 0.5 + np.tile(
                grid[i], (na, 1))) * int(stride[i])
            outs[row_ind:row_ind + length, 2:4] = (outs[row_ind:row_ind + length, 2:4] * 2) ** 2 * np.repeat(
                anchor_grid[i], h * w, axis=0)
            row_ind += length
        return outs
    
    def post_process_opencv(self,outputs,model_h,model_w,img_h,img_w,thred_nms,thred_cond):
        conf = outputs[:,4].tolist()
        c_x = outputs[:,0]/model_w*img_w
        c_y = outputs[:,1]/model_h*img_h
        w  = outputs[:,2]/model_w*img_w
        h  = outputs[:,2]/model_h*img_h
        p_cls = outputs[:,5:]
        if len(p_cls.shape)==1:
            p_cls = np.expand_dims(p_cls,1)
        cls_id = np.argmax(p_cls,axis=1)

        p_x1 = np.expand_dims(c_x-w/2,-1)
        p_y1 = np.expand_dims(c_y-h/2,-1)
        p_x2 = np.expand_dims(c_x+w/2,-1)
        p_y2 = np.expand_dims(c_y+h/2,-1)
        areas = np.concatenate((p_x1,p_y1,p_x2,p_y2),axis=-1)
        
        areas = areas.tolist()
        ids = cv2.dnn.NMSBoxes(areas,conf,thred_cond,thred_nms)
        if len(ids)>0:
            return  np.array(areas)[ids],np.array(conf)[ids],cls_id[ids]
        else:
            return [],[],[]
    def infer_img(self,img0,net,model_h,model_w,nl,na,stride,anchor_grid,thred_nms=0.4,thred_cond=0.5):
        # 图像预处理
        img = cv2.resize(img0, [model_w,model_h], interpolation=cv2.INTER_AREA)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img.astype(np.float32) / 255.0
        blob = np.expand_dims(np.transpose(img, (2, 0, 1)), axis=0)

        # 模型推理
        outs = net.run(None, {net.get_inputs()[0].name: blob})[0].squeeze(axis=0)

        # 输出坐标矫正
        outs = self.cal_outputs(outs,nl,na,model_w,model_h,anchor_grid,stride)

        # 检测框计算
        img_h,img_w,_ = np.shape(img0)
        boxes,confs,ids = self.post_process_opencv(outs,model_h,model_w,img_h,img_w,thred_nms,thred_cond)

        return  boxes,confs,ids
    
    def red_light(self):
        
        
        while True:
            success, self.img1 = self.cap.read()
            
            if success:
                t1 = time.time()
                det_boxes,scores,ids = self.infer_img(self.img1,self.net,self.model_h,self.model_w,self.nl,self.na,self.stride,self.anchor_grid,thred_nms=0.4,thred_cond=0.5)
                t2 = time.time()
                
                cv2.line(self.img1,self.posion_A1,self.posion_A2,(255,255,255),3)
                cv2.line(self.img1,self.posion_B1,self.posion_B2,(255,255,255),3)
                cv2.rectangle(self.img1,(450,5),(610,60),(5,5,5),-1)
                cv2.circle(self.img1,(483,31),22,(0,10,250),-1)
                cv2.circle(self.img1,(528,31),22,(128,128,128),-1)
                cv2.circle(self.img1,(573,31),22,(128,128,128),-1)
                

                if (len(det_boxes)!=0) and (scores[0] > 0.8):
                    
                    if det_boxes[0][1]> 310 and det_boxes[0][3] < 460:
                        print("before the start line")
                        self.result = HyperLPR_plate_recognition(self.img1)
                        if len(self.result) != 0:
                            
                            self.lic_list[0] = self.result[0][0]
                            
                            self.lic_count[0] = 1
                            self.lic_count[1] = 0
                            self.lic_count[2] = 0
                            self.imgA2_flag = 0
                            self.imgA3_flag = 0
                            if self.imgA1_flag == 0:
                                self.imgA1_flag = 1
                                
                                self.imgA1 = self.img1
                            print(self.lic_list[0])
                            
                    if det_boxes[0][1]< 270 and det_boxes[0][3] < 270:
                        if det_boxes[0][1]> 100 and det_boxes[0][3] > 100: 
                            print("in the box")
                            self.result = HyperLPR_plate_recognition(self.img1)
                            if len(self.result) != 0:
                                print(self.result[0][0])
                                if self.result[0][0] == self.lic_list[0]:
                                    self.lic_count[1] = 1
                                    if self.imgA2_flag == 0:
                                        self.imgA2_flag = 1
                                
                                        self.imgA2 = self.img1
                                    
                    if det_boxes[0][1]< 60 and det_boxes[0][3] > 60:
                        print("on the end line")
                        self.result = HyperLPR_plate_recognition(self.img1)
                        if len(self.result) != 0:
                            print(self.result[0][0])
                            if self.result[0][0] == self.lic_list[0]:
                                    self.lic_count[2] = 1
                                    if self.imgA3_flag == 0:
                                        self.imgA3_flag = 1
                                        self.imgA3 = self.img1
                                        print("Hello imgA3")
                if (self.lic_count[0] == 1) and (self.lic_count[1] == 1) and (self.lic_count[2] == 1):
                    print("weizhang")
                    os.chdir(self.car_path)
                    if(os.path.exists(self.lic_list[0])):
                        shutil.rmtree(self.lic_list[0])
                        os.makedirs(self.lic_list[0])
                    else:
                        os.makedirs(self.lic_list[0])
                    os.chdir(self.lic_list[0])
                    cv2.imwrite((self.result[0][0]+'_1'+'.jpg'),self.imgA1)
                    cv2.imwrite((self.result[0][0]+'_2'+'.jpg'),self.imgA2)
                    cv2.imwrite((self.result[0][0]+'_3'+'.jpg'),self.imgA3)
                    voice.my_say("dudu")
                    self.lic_count[0] = 0
                    self.lic_count[1] = 0
                    self.lic_count[2] = 0
                    self.imgA1_flag = 0
                    self.imgA2_flag = 0
                    self.imgA3_flag = 0
                for box,score,id in zip(det_boxes,scores,ids):
                    
#                     label = 0
                    if score > 0.8:
                        
                        label = '%s:%.2f'%(self.dic_labels[id],score)
            
                        self.plot_one_box(box.astype(np.int16), self.img1, color=(255,0,0), label=label, line_thickness=None)
                    
                str_FPS = "FPS: %.2f"%(1./(t2-t1))
                
                cv2.putText(self.img1,str_FPS,(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),3)
                
                return self.img1
        
                
            
        
    