import cv2
import yiflow as yf
import mediapipe as mp

from copy import copy


class DetectionStage(yf.Stage):

    def setup(self):
        # 初始化关键点检测器
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose()

    def run(self, feed_dict):
        # 获取输入
        img = feed_dict['image']

        # 获取关键点数据
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = self.pose.process(img_rgb)

        # 画结果
        if self.draw:
            if result.pose_landmarks:
                drawed_img = copy(img)
                self.mpDraw.draw_landmarks(drawed_img, result.pose_landmarks, self.mpPose.POSE_CONNECTIONS)

                # 输出画图结果
                feed_dict['drawed'] = drawed_img

        # 收集关键点
        landmarks = []
        if result.pose_landmarks:
            for id, lm in enumerate(result.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                landmarks.append((id, cx, cy))
        
        # 输出关键点
        feed_dict['landmarks'] = landmarks
