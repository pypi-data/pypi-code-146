'''
https://stackoverflow.com/questions/882712/sending-html-email-using-python
'''
import smtplib
from email.header import Header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr, parseaddr

from loguru import logger

from toolkits import utils


def format_parse(s):
    _name, _addr = parseaddr(s)
    return formataddr((Header(_name, 'utf-8').encode(), _addr))

def related_html(smtp={}, sender={}, recipients=[], subject='', html_file='', images=[]):
    '''
    smtp SMTP信息

        server SMTP地址
        port   SMTP端口
        ssl    是否使用SSL

    sender 发件人信息

        name     发件人名称
        address  发件人邮箱地址
        password 发件人邮箱密码(SMTP)

    recipients 收件人列表
    subject 邮件主题
    html_file HTML文件

    images 图片列表(可选)

        cid  图片CID
        path 图片路径
    '''

    # 参数判断
    match True:
        case True if smtp == None or type(smtp) != dict or smtp == {}:
            logger.error('ERROR!! {} is not dictionary or none'.format('smtp'))
            return False
        case True if sender == None or type(sender) != dict or sender == {}:
            logger.error('ERROR!! {} is not dictionary or none'.format('sender'))
            return False
        case True if recipients == None or type(recipients) != list or recipients == []:
            logger.error('ERROR!! {} is not list or none'.format('recipients'))
            return False
        case True if subject == None or type(subject) != str or subject == '':
            logger.error('ERROR!! {} is not string or none'.format('subject'))
            return False
        case True if html_file == None or type(html_file) != str or html_file == '':
            logger.error('ERROR!! {} is not string or none'.format('html_file'))
            return False

    logger.success('sendmail start')

    try:

        _message = MIMEMultipart('related')

        with open(html_file, 'r') as _html_file:

            _message.attach(MIMEText(_html_file.read(), 'html', 'utf-8'))

            if utils.vTrue(images, list):

                for _image in images:

                    try:

                        if utils.stat(_image.get('path', ''), 'file'):

                            '''
                            添加图片
                            with open(image_path, 'rb') as image_file:
                                mime_image = MIMEImage(image_file.read())
                                # Define the image's ID as referenced above
                                mime_image.add_header('Content-ID', '<CID>')
                                message.attach(mime_image)
                            '''

                            with open(_image['path'], 'rb') as _image_file:
                                _mime_image = MIMEImage(_image_file.read())
                                _mime_image.add_header('Content-ID', '<{}>'.format(_image['cid']))
                                _message.attach(_mime_image)

                        else:

                            next

                    except Exception as e:
                        logger.error(e)
                        next

        # 发件人
        _message['From'] = formataddr([sender.get('name'), sender.get('address')])

        # 收件人
        _message['To'] = ", ".join(list(map(format_parse, recipients)))

        # 主题
        _message['Subject'] = subject

        '''
        发送邮件

        SMTP.sendmail(from_addr, to_addrs, msg, mail_options=(), rcpt_options=())

            to_addrs = sender_to + sender_cc
            https://docs.python.org/3/library/smtplib.html#smtplib.SMTP.sendmail
            https://gist.github.com/AO8/c5a6f747eeeca02351152ae8dc79b537
        '''

        if smtp.get('ssl', False) == True:

            with smtplib.SMTP_SSL(smtp.get('server'), smtp.get('port')) as _smtp:
                _smtp.login(sender.get('address'), sender.get('password'))
                _smtp.sendmail(sender.get('address'), recipients, _message.as_string())

        else:

            with smtplib.SMTP(smtp.get('server'), smtp.get('port')) as _smtp:
                _smtp.login(sender.get('address'), sender.get('password'))
                _smtp.sendmail(sender.get('address'), recipients, _message.as_string())

        logger.success('sendmail end')

        return True

    except Exception as e:
        logger.exception(e)
        logger.error('sendmail end')
        return False
