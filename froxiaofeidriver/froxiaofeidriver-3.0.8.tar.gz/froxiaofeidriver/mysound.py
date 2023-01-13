import vlc



music = {
    '蓝色':'file:///home/pi/AiCar/music/blue.mp3',
    '青色':'file:///home/pi/AiCar/music/cyan.mp3',
    '橙色': 'file:///home/pi/AiCar/music/orange.mp3',
    '红色': 'file:///home/pi/AiCar/music/red.mp3',
    '紫色': 'file:///home/pi/AiCar/music/violet.mp3',
    '黄色': 'file:///home/pi/AiCar/music/yellow.mp3',
    '绿色':'file:///home/pi/AiCar/music/green.mp3',
    '火灾':'file:///home/pi/AiCar/music/Fire.mp3',
    '前进': 'file:///home/pi/AiCar/music/forward.mp3',
    '倒车': 'file:///home/pi/AiCar/music/Reversing.mp3',
    '左转': 'file:///home/pi/AiCar/music/Turn_left.mp3',
    '右转': 'file:///home/pi/AiCar/music/Turn_right.mp3',
    '允许通行': 'file:///home/pi/AiCar/music/Allow passage.mp3',
    '禁止通行':'file:///home/pi/AiCar/music/No allow passage.mp3',
    '开始采集人脸':'file:///home/pi/AiCar/music/StartCollect.mp3',
    '前二十张人脸':'file:///home/pi/AiCar/music/FirstTwenty.mp3',
    '中间二十张人脸':'file:///home/pi/AiCar/music/MiddleTwenty.mp3',
    '人脸采集完成':'file:///home/pi/AiCar/music/CollectEnd.mp3',
    '人脸训练完成':'file:///home/pi/AiCar/music/TrainEnd.mp3',
    '开始人脸识别':'file:///home/pi/AiCar/music/startrecognize.mp3',
    '下一个ID图像采集':'file:///home/pi/AiCar/music/nextID.mp3'
}

"""
@设置声音播报
"""
class Sound:
    
    def __init__(self):
        self.vlc_obj = vlc.Instance()
        self.vlc_player = self.vlc_obj.media_player_new()
        self.vlc_media = self.vlc_obj.media_new('')

    """
    @播放某一段声音
    """
    def play(self,src):
        self.vlc_media = self.vlc_obj.media_new(src)
        self.vlc_player.set_media(self.vlc_media)
        self.vlc_player.play()

    """
    @停止播放某一段声音
    """
    def stop(self,src):
        self.vlc_media = self.vlc_obj.media_new(src)
        self.vlc_player.set_media(self.vlc_media)
        self.vlc_player.stop()

    """
    @播放允许通行音频
    """
    def allow(self):
        self.stop(music['允许通行'])
        self.play(music['允许通行'])

    """
    @播放蓝色音频
    """
    def blue(self):
        self.stop(music['蓝色'])
        self.play(music['蓝色'])

    """
    @播放青色音频
    """
    def cyan(self):
        self.stop(music['青色'])
        self.play(music['青色'])

    """
    @播放有火灾音频
    """
    def fire(self):
        self.stop(music['火灾'])
        self.play(music['火灾'])

    """
    @播放前进音频
    """
    def forward(self):
        self.stop(music['前进'])
        self.play(music['前进'])

    """
    @播放绿色音频
    """
    def green(self):
        self.stop(music['绿色'])
        self.play(music['绿色'])

    """
    @播放禁止通行音频
    """
    def notAllow(self):
        self.stop(music['禁止通行'])
        self.play(music['禁止通行'])

    """
    @播放橙色音频
    """
    def orange(self):
        self.stop(music['橙色'])
        self.play(music['橙色'])

    """
    @播放红色音频
    """
    def red(self):
        self.stop(music['红色'])
        self.play(music['红色'])

    """
    @播放倒车音频
    """
    def reversing(self):
        self.stop(music['倒车'])
        self.play(music['倒车'])

    """
    @播放左转音频
    """
    def turn_left(self):
        self.stop(music['左转'])
        self.play(music['左转'])

    """
    @播放右转音频
    """
    def turn_right(self):
        self.stop(music['右转'])
        self.play(music['右转'])

    """
    @播放紫色音频
    """
    def violet(self):
        self.stop(music['紫色'])
        self.play(music['紫色'])

    """
    @播放黄色音频
    """
    def yellow(self):
        self.stop(music['黄色'])
        self.play(music['黄色'])

    """
    @
    """
    def stopMedia(self):
        self.vlc_player.stop()

    """
    @播放开始采集人脸音频
    """

    def faceStartCollect(self):
        self.stop(music['开始采集人脸'])
        self.play(music['开始采集人脸'])

    """
    @播放前二十张人脸采集成功音频
    """

    def faceFirstTwenty(self):
        self.stop(music['前二十张人脸'])
        self.play(music['前二十张人脸'])

    """
    @播放中间二十张人脸采集成功音频
    """

    def faceMiddleTwenty(self):
        self.stop(music['中间二十张人脸'])
        self.play(music['中间二十张人脸'])

    """
    @播放人脸采集完成音频
    """

    def faceCollectEnd(self):
        self.stop(music['人脸采集完成'])
        self.play(music['人脸采集完成'])

    """
    @播放人脸识别训练完成音频
    """

    def faceTrainEnd(self):
        self.stop(music['人脸训练完成'])
        self.play(music['人脸训练完成'])

    """
    @播放开始人脸识别音频
    """

    def faceStartRecognize(self):
        self.stop(music['开始人脸识别'])
        self.play(music['开始人脸识别'])

    """
    @播放下一个ID图像采集音频
    """
    def faceNextID(self):
        self.stop(music['下一个ID图像采集'])
        self.play(music['下一个ID图像采集'])
