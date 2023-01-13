import yiflow as yf


class RuleStage(yf.Stage):

    def setup(self):
        pass

    def run(self, feed_dict):
        # 获取输入
        landmarks = feed_dict['landmarks']

        # 判断是否有人
        alarm = False
        if len(landmarks) != 0:
            # 有人则预警
            alarm = True

        # 输出预警信号
        feed_dict['alarm'] = alarm
