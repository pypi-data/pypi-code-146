import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

if not 'GIT_PROTOCOL' in os.environ:
    os.environ['GIT_PROTOCOL'] = 'https'

if not 'GIT_SERVER' in os.environ:
    os.environ['GIT_SERVER']='github.com'

if not 'SOURCE_FOLDER' in os.environ:
    os.environ['SOURCE_FOLDER'] = os.environ['USERPROFILE']+'\\src\\'

if not 'SLEEP_TIME' in os.environ:
    os.environ['SLEEP_TIME'] = '5'

if not 'WORKERPOOL_STREAM' in os.environ:
    os.environ['WORKERPOOL_STREAM'] = 'deepportfolio-workerpool'

os.environ['USER_COMPUTER'] = os.environ['USERNAME']+'@'+os.environ['COMPUTERNAME']
