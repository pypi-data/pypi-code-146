from setuptools import setup, find_packages
import codecs
import os

VERSION = '1.4'
DESCRIPTION = 'A Temp Mail library for python'
LONG_DESCRIPTION = '''
A package that allows to create temp mail and receive emails from it.
<br>
<h3>Example:</h3>

    from pytempmail import TempMail
    from time import sleep
    
    tm=TempMail()
    # Print Current Mail
    print(f'Email: {tm.email}')
    
    printed_mails=[]
    
    print('All Emails are:')
    while True:
    	all_mails=tm.get_mails()
    	for mail in all_mails:
    		if mail.id not in printed_mails:
    			# Adding to the list, so it will not print it again
    			printed_mails.append(mail.id)
    			print(f'From: {mail.from_name} - {mail.from_addr}')
    			print(f'Subject: {mail.subject}')
    			print(f'Body: {mail.text}')
    			# you can use mail.description to print short text
    			# mail.html returns only html. use it if you're on web
    			print('\n-  -  -  -  -  END  -  -  -  -  -\n')
    	sleep(5)


'''

# Setting up
setup(
    name="temporary-mail",
    version=VERSION,
    author="S M Shahriar Zarir",
    author_email="<shahriarzariradvance@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python', 'mail', 'tempmail'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)