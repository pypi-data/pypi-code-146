import traceback
import yagmail
from qrunner.utils.allure_data import get_allure_data
from qrunner.utils.log import logger
from qrunner.testdata import get_now_datetime


class Mail:
    def __init__(self, host, port, user, password):
        self.host = host
        self.port = port
        self.username = user
        self.password = password

    def send_email(self, receivers, subject, contents, attachments=None):
        """
        发送邮件
        @param receivers: 收件人列表
        @param subject: 邮件主题
        @param contents: 邮件内容
        @param attachments: 附件文件的绝对路径
        @return:
        """
        try:
            logger.info(f'开始发送邮件~')
            # 初始化服务对象直接根据参数给定，更多参考SMTP(）内部
            server = yagmail.SMTP(host=self.host, port=self.port,
                                  user=self.username, password=self.password)
            # 发送内容，设置接受人等信息，更多参考SMTP.send()内部
            server.send(to=receivers,
                        subject=subject,
                        contents=contents,
                        attachments=attachments)
            server.close()
        except Exception:
            logger.info(f'发送失败~')
            print('traceback.format_exc(): {}'.format(traceback.format_exc()))
            return False

        # 无任何异常表示发送成功
        logger.info(f'发送成功~')
        return True

    # def send_mail(self, mail_data, receivers):
    #     """
    #     参考：https://blog.csdn.net/fenglepeng/article/details/107005000
    #     @param mail_data:
    #     @param receivers:
    #     @return:
    #     """
    #     print(f'向{receivers}发送邮件...')
    #     # 创建一个带附件的实例
    #     message = MIMEMultipart()
    #     message['From'] = Header(self.username)
    #     message['To'] = Header(",".join(receivers))
    #     message['Subject'] = Header(mail_data.get('title'), 'utf-8')
    #
    #     # 邮件正文内容
    #     message.attach(MIMEText(mail_data.get('body'), 'plain', 'utf-8'))
    #     # 附件
    #     file_path = mail_data.get('file_path')
    #     if file_path:
    #         # 构造附件，传送当前目录下的文件
    #         att1 = MIMEText(open(file_path, 'r').read(), 'base64', 'utf-8')
    #         att1["Content-Type"] = 'application/octet-stream'
    #         # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
    #         file_name = mail_data.get('file_name')
    #         att1["Content-Disposition"] = f'attachment; filename="{file_name}"'
    #         message.attach(att1)
    #
    #     # 连接
    #     conn = smtplib.SMTP_SSL(self.host, 465)
    #     # 登录
    #     conn.login(self.username, self.password)
    #     # 发送邮件
    #     try:
    #         conn.sendmail(self.username, receivers, message.as_string())
    #     except Exception as e:
    #         print(f'发送失败: {str(e)}')
    #     else:
    #         print('发送成功')
    #     # 断开连接
    #     conn.quit()

    def send_report(self, to_list, title, report_url):
        allure_data = get_allure_data('allure-results')
        total = allure_data.get('total')
        fail = allure_data.get('failed')
        passed = allure_data.get('passed')
        rate = allure_data.get('rate')

        # 邮件内容
        title = f'{title}({get_now_datetime(strftime=True)})'
        body_str = '\n\n共 {0} 个用例，通过 {1} 个，失败 {2} 个，通过率 {3}%，详见: {4}'\
            .format(total, passed, fail, rate, report_url)

        # 发送邮件
        self.send_email(to_list, title, body_str)


if __name__ == '__main__':
    pass





