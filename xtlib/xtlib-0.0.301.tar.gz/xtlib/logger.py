# logger.py: lightweight XT presence in user training script
import os
import sys
import signal

def init():

    def signal_handler(sig, frame):
        
        print('You pressed Ctrl+C!')

        cmd_line = " ".join(sys.argv)
        cmd = "xt run --target=singularity {}".format(cmd_line)

        print("submit command: {}".format(cmd))
        response = input("enter OK to submit: ")
        if response.lower() == "ok":
            os.system(cmd)

    signal.signal(signal.SIGINT, signal_handler)
    print('Press Ctrl+C to submit job to SINGULARITY...')


