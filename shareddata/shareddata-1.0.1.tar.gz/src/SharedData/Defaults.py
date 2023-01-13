import os
from dotenv import load_dotenv

#print('loading environment variables...')

load_dotenv()  # take environment variables from .env.

if not 'AWS_PROFILE' in os.environ:
    raise Exception('Missing AWS_PROFILE environment variable!')

if not 'DATABASE_FOLDER' in os.environ:    
    os.environ['DATABASE_FOLDER'] = os.path.expanduser("~")+'\DB' 

if not 'S3_BUCKET' in os.environ:    
    os.environ['S3_BUCKET'] = 's3://deepportfolio'

if not 'S3_AWS_PROFILE' in os.environ:
    os.environ['S3_AWS_PROFILE'] = os.environ['AWS_PROFILE']

if not 'LOG_STREAMNAME' in os.environ:    
    os.environ['LOG_STREAMNAME'] = 'deepportfolio-logs'

if not 'LOG_AWS_PROFILE' in os.environ:    
    os.environ['LOG_AWS_PROFILE'] = os.environ['AWS_PROFILE']
    
if not 'BASE_STREAM_NAME' in os.environ:    
    os.environ['BASE_STREAM_NAME'] = 'deepportfolio-real-time'    

if not 'STREAM_AWS_PROFILE' in os.environ:    
    os.environ['STREAM_AWS_PROFILE'] = os.environ['AWS_PROFILE']

if not 'USER_COMPUTER' in os.environ:
    os.environ['USER_COMPUTER'] = os.environ['USERNAME']+'@'+os.environ['COMPUTERNAME']

if not 'LOG_LEVEL' in os.environ:    
    os.environ['LOG_LEVEL']='INFO'

if not 'SAVE_LOCAL' in os.environ:    
    os.environ['SAVE_LOCAL']='True'


loaded=True