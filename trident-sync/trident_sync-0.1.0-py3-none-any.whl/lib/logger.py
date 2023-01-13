import datetime


class Logger:
    def info(self, text):
        now = datetime.datetime.now()
        print(f"【{now}】 {text}")


logger = Logger()
