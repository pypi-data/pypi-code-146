from time import time

def scroll_to_bottom(driver):
    """将窗口一点一点滑动到底部，方便加载图片
    """
    js = "return action=document.body.scrollHeight"
    # 初始化现在滚动条所在高度为0
    height = 0
    # 当前窗口总高度
    new_height = driver.execute_script(js)
    while height < new_height:
        # 将滚动条调整至页面底部
        for i in range(height, new_height, 300):
            driver.execute_script('window.scrollTo(0, {})'.format(i))
            time.sleep(0.3)
        height = new_height
        new_height = driver.execute_script(js)