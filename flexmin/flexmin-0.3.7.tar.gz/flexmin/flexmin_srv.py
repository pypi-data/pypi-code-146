#!/usr/local/bin/python
import subprocess
import re
import time
import os
import sys
import stat
import zipfile
import shutil
import shlex
import platform
import getpass
import datetime
import traceback
import random
import yaml
from threading import Thread
from xmlrpc.server import SimpleXMLRPCServer
from .utils.simplepam import authenticate
from .utils.utilities import Substitute
from .utils import yamlconfigs

from runpy import run_path
from argparse import Namespace
from .flexmin_task import Task

def get_config(silent=False):
    """
    Look for flexmin config file on local system and load settings
    Returns a Namespace which allows dot notation to access settings
    """
    # Find FM_CONFIGS folder on this system
    if os.path.exists('/usr/local/etc/flexmin/'):
        # use path in etc as configs folder if it exists
        fm_configs = '/usr/local/etc/flexmin'
    elif os.path.exists('/etc/flexmin/'):
        # use path in etc as configs folder if it exists
        fm_configs = '/etc/flexmin'
    else:
        # otherwise resort to configs folder within flexmin app folder
        fm_configs = ''

    try:
        # Get parameters from flexmin.conf then filter out junk using FM_ check.
        fm = Namespace(**run_path(os.path.join(fm_configs,'flexmin.conf')))
        local_conf = os.path.join(fm_configs,'flexmin.local.conf')
        if os.path.isfile(local_conf):
            fm.__init__(**run_path(local_conf))  # merge/override params with 'local' version
        fm.__dict__ = dict(filter(lambda item: 'FM_' in item[0], fm.__dict__.items()))
    except:
        if not silent: print("Error opening flexmin.conf or flexmin.local.conf from " + str(fm_configs))
        fm = Namespace()

    fm.FM_CONFIGS = fm_configs

    return fm


class TaskServer():
    """
    XML RPC Server that controls the addition of tasks and retrieving current
    state of any given task.
    """
    
    def __init__(self, parameter, timeout=3600, failure_timeout=1800):
        """
        timeout is the timeout of the session
        failure_timeout is the time after which a login failure is removed from
          the list, thereby reducing the failure count used to determine if
          the threshold is reached where no further login attmepts are permitted
        """
        self.root = os.path.dirname(os.path.abspath(sys.argv[0]))   # path this service is running from
        self.service_param = parameter                              # optional parameter if not running as a service  
        if self.service_param == "debug":
            self.debug = True
        else:
            self.debug = False
        if self.service_param == "display":
            self.display = True
        else:
            self.display = False
        if self.display:
            print("Starting Flexmin Task Server in 'display' mode")
        elif self.debug:
            print("Starting Flexmin Task Server in 'debug' mode")
        else:
            print("Starting Flexmin Task Server")
        self.scripts = os.path.join( self.root, 'scripts' )         # local scripts path
        self.login_fail = []                                        # list of timestamps of recent login failures
        self.login_success = []                                     # list of client IP of recent successful logins

        # register unique key to restrict access to some functions internally
        chars = "abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789"
        random.seed = (os.urandom(1024))
        self.key = ''.join(random.choice(chars) for i in range(20))
        
        # Find FM_CONFIGS folder on this system
        fm = get_config()
    
        # Generate local FM (flexmin) variables where not already available
        # TODO: Doesn't look like these are ever available, remove checks and just set them?
        # TODO: Consider moving this to get_config function as yamlconfig uses get_config and may need some of these 
        fm.FM_SERVICE_ROOT = self.root
        fm.FM_TASK_DATA = os.path.join( fm.FM_LOGROOT, 'task_data')  # also in common.sh
        if 'FM_SCRIPTS' not in fm:
            fm.FM_SCRIPTS = self.scripts  # see init method, and common.sh
        if 'FM_DEFAULT_CONFIGS' not in fm:
            fm.FM_DEFAULT_CONFIGS = os.path.join(fm.FM_CONFIGS, 'config-defaults')  # see init method, and common.sh
        if 'FMS_PARAMETER' not in fm:
            # set parameter povided on service start up
            fm.FMS_PARAMETER = self.service_param
        if not os.path.exists(fm.FM_TASK_DATA):
            os.makedirs(fm.FM_TASK_DATA)
            
        self.fm = fm
        self.load_menu()
        self.tasks = dict()                         # for tracking ongoing tasks
        self.sessions = dict()                      # key = session id, value = expiry time
        self.session_timeout = timeout
        self.failure_timeout = failure_timeout
        
        params = shlex.split(parameter)             # parameters passed as string like shell parameters

                
    def load_menu(self):
        """
        Load menu details from menu.conf file save as list of entries,
        each entry being a list of the entry attributes
        
        Also calculate allowed_scripts dictionary which has script name
        as key and script file as value.
        """
        # First process menu.yaml and generate menu.conf
        yaml_file = os.path.join(self.fm.FM_CONFIGS, 'menu.yaml')
        c = yamlconfigs.Config(yaml_file, self.fm.__dict__)
        c.native()
        
        # Load and process menu.conf
        menu_file = os.path.join(self.fm.FM_CONFIGS, 'menu.conf')
        self.menu = []
        self.allowed_scripts = {}
        if os.path.isfile(menu_file):
            with open(menu_file,'r') as f:
                for line in f:
                    if line[0] != '#':
                        entry = line.strip().split(';')
                        if entry[0] == '1':
                            if len(entry) > 3 and entry[3]:
                                script = entry[3]
                                # Make sure script exists, make symlink if only exists in 'local'
                                script_path = os.path.join(self.fm.FM_HOME,'scripts',script)
                                if not os.path.isfile(script_path):
                                    alt_path = os.path.join(self.fm.FM_HOME,'local','scripts',script)
                                    if os.path.isfile(alt_path):
                                        # create symlink
                                        os.symlink(alt_path, script_path)
                                        # adjust permissions so is executable by user and group
                                        perms = os.stat(alt_path)
                                        os.chmod(alt_path, perms.st_mode | stat.S_IXUSR | stat.S_IXGRP)
                                        self.allowed_scripts[script[0:-3]] = script
                                        self.menu.append(entry)
                                else:
                                    self.allowed_scripts[script[0:-3]] = script
                                    self.menu.append(entry)
                        else:
                            self.menu.append(entry)  # add group entry

            return True
        else:
            return False
        
                
    def get_menu(self):
        """
        Return the menu object
        """
        return self.menu
    
    
    def get_allowed_scripts(self):
        return self.allowed_scripts


    def writeTaskDataFile(self,taskid, script, varnum, mode, data):
        """
        Write the specified data into a parameter file
        script is the name of the script for which the data is intended
        varnum is the parameter number (1,2,...)
        mode is the type of file to create ('w' text  or 'wb' binary)
        data is the object holding the data to save (binary or text)
        """
        mod = os.path.splitext(script)[0]
        paramfile = mod + "_param"
        taskfolder = 'task' + str(taskid)
        path = taskfolder + os.sep + paramfile + '_' + str(varnum)
        path = os.path.join(self.fm.FM_TASK_DATA, path)
        if self.debug: print("Writing data file to; " + path)
        folder = os.path.dirname(os.path.abspath(path))
        if not os.path.exists(folder):
            os.makedirs(folder)
        with open(path,mode) as f:
            f.write(data)
        return True

        
    def tidyTaskData(self,taskid,force):
        """ 
        Remove task data for specified task id 
        
        set *force* to True if you wish to force deletion of existing data,
        otherwise folder is only deleted if no data stored there.
        """
        path = os.path.join(self.fm.FM_TASK_DATA,'task' + str(taskid))
        if os.path.exists(path):
            if not force:
                if not os.listdir(path):
                    os.rmdir(path)
            else:
                shutil.rmtree(path)
        return True

        
    def getScripts(self):
        """ Return list of available scripts on this system """
        import glob
        #root = os.path.join(request.folder,'private','scripts')
        #modroot = os.path.join(request.folder,'modules')
        scripts = glob.glob(self.scripts + os.sep + '*.sh')
        scripts += glob.glob(self.scripts + os.sep + '*.py')
        if self.service_param == 'display':
            print("scripts:" + str(scripts))
        return scripts

        
    def get_vars(self):
        """ Return flexmin service variables to web interface """
        if self.service_param == 'display' or self.service_param == 'debug':
            print("method get_vars called")
        return self.fm

    
    def check_session(self, auth):
        """
        auth = { session_id: '',
                 username: '',
                 password: ''}
                 
        Check session identified by the auth dictionary.
        
        If the session has expired, or does not yet exist,  then this will not 
        be considered a valid session unless a valid username and password are 
        supplied in auth. If the credentials are valid a new session is created
        using the session_d provided by the calling process, or the existing 
        session is re-activated (no longer expired).
        
        The calling process is responsible for using secure random session_id's
        
        If the session has expired, or does not exist, and no valid username and
        password are supplied, then the session will be rejected.
        
        This should only be used prior to running a task as this process
        automatically extends the session timeout.
        
        Return None indicates success otherwise string "error: ..." indicates
        nature of failure.
        """
        if self.debug: print("Function: check_session")
            
        if 'session_id' in auth:
            #print auth
            sess_id = auth['session_id']
            if self.debug: print("session id: {}".format(str(sess_id)))
            now = datetime.datetime.now()
            newexpiry = now + datetime.timedelta(seconds = self.session_timeout)
            failexpiry = now - datetime.timedelta(seconds = self.failure_timeout)

            # remove expired failures
            while len(self.login_fail) > 0 and self.login_fail[0] < failexpiry:
                self.login_fail.pop()
                
            # allow greater threshold if successful login logged recently 
            # from this IP, allows genuine administrators extra chances in 
            # case attacker has triggered possible lockout
            if auth['client_ip'] in self.login_success:
                threshold = 5
            else:
                # if no recent success from this IP then limit failure threshold
                threshold = 3

            # Handle login failure threshold Exceeded
            if len(self.login_fail) >= threshold:
                remaining = self.login_fail[0] - failexpiry
                strRemain = re.sub(r'\.\d*$','',str(remaining))
                retstr = "error: ERROR - Account Locked for {} (hh:mm:ss);".format(strRemain)
                retstr = retstr + " recent successful logins {}".format(str(self.login_success))
                return retstr

            # session id provided
            if 'username' in auth and 'password' in auth:
                # with username and password. If valid (re)create session 
                if self.debug: print("Verifying credentials")
                if auth['username'] == 'flexmin':
                    if self.debug: print("auth: " + str(auth))
                    if authenticate(auth['username'],auth['password']):
                        # (re)create session, or renew session
                        sess = dict()
                        sess['session_id'] = sess_id
                        sess['expires'] = newexpiry
                        self.sessions[sess_id] = sess
                        if not auth['client_ip'] in self.login_success:
                            self.login_success.append(auth['client_ip'])
                            # keep login_success (IP address) list to last 5
                            self.login_success = self.login_success[-5:]
                        return None
                    else:
                        # failed login attempt
                        if self.debug: print("Login failed")
                        self.login_fail.append(now)
                        if len(self.login_fail) >= threshold:
                            # too many failed logins report account locked
                            return "error: ERROR - Account Locked; Failed Logins {}".format(str(len(self.login_fail)))
                        else:
                            return "error: ERROR - Login Required (Failed Login {})".format(str(len(self.login_fail)))
                else:
                    if self.debug: print("Username must be flexmin")
                    return "error: ERROR - Username must be flexmin"

            else:
                # no username and password, so check if session expired
                if sess_id in self.sessions:
                    sess = self.sessions[sess_id]
                else:
                    return "error: ERROR - Login Required (No Session)"
                s_expires = sess['expires']
                if now < s_expires:
                    sess['expires'] = newexpiry
                    return None  # session still valid
                else:
                    return "error: ERROR - Login Required (Session Expired)"  # session expired
        else:
            if self.debug: print("No session id provided, not a valid session")
            # no session id provided, failure
            return "error: ERROR - Session ID required" 


    def completed(self, taskid):
        """
        Return True if specified task completed, False
        if not completed, or no such task.
        """
        try:
            return self.tasks[taskid].completed()
        except:
            return False
        
            
    def tasklist(self):
        """
        Return list of tasks and their status as a multiline text output
        """
        output = []
        for key in self.tasks:
            if self.tasks[key].completed():
                status = "completed"
            else:
                status = "running"
            output.append(str(key) + ": " + status)
        if len(output) == 0:
            output.append("No tasks registered")
            
        return "\n".join(output)
    
    
    def taskClear(self):
        """
        Clear out internal list of tasks (if all completed)
        """
        alldone = True
        for key in self.tasks:
            if self.tasks[key].completed():
                self.tidyTaskData(key,True)   # clear up data from filesystem
            else:
                alldone = False
        if alldone:
            self.tasks = dict()   # clear task record
            return True    # confirm tasks cleared
        else:
            return False   # indicate tasks not cleared
            
            
    def runyaml(self, cmd, task_vars=None, auth=None):
        """
        Run shell command, python module, or script and data from zip.
        
        auth = { session_id: '',
                 username: '',
                 password: ''}
                 
        Need session_id if calling process has already authenticated previously,
        otherwise username and password required to authenticate.
        
        task_vars is a dictionary with any parameters required for this request.
        
        task_vars = { 'FM_TASKID': integer }

        Same as run method, except yaml output is obtained before returning this
        output to calling program.

        Once yaml output is received, this method returns, but process continues
        to run in background. 

        state and stateUpdate methods should be used to get text output of the task.
        --- is used to indicate end of yaml content and beginning of regular 
        text stream, ... is used to indicate an ongoing task with text output.
        """
        
        # Security relies on web application sending through auth token
        # for tasks not initiated by interface authentication not required.
        # reference to internal key used in place of authentication for internal requests.
        if auth:
            if auth == self.key:
                pass # okay call verified to be internal
            else:
                login_mess = self.check_session(auth)
                if login_mess:  # a message return = failure
                    return login_mess
                    #return "error: ERROR - Login Required"
        else: # do nothing if no authentication provided
            return "error: Not authenticated"
        
        # Check allowed scripts list before permitting execution
        script = cmd.split(' ')[0][0:-3]
        if not ( script in self.allowed_scripts or script == 'flexmin_login'):
            return "error: This action (" + script + ") is not permitted"

        if 'FM_LOGIN_SUCCESS' not in task_vars:
            # only needed by flexmin_login.py (no need in common.sh)
            task_vars['FM_LOGIN_SUCCESS'] = self.login_success

        # experimental, use fm_vars and override with task_vars where defined
        # TODO remove reference to fm dictionary
        task_vars = {**self.fm.__dict__, **task_vars}
        
        taskid = task_vars['FM_TASKID']
        

        if taskid > 0 and taskid in self.tasks:
            # Can't run same task id again, except for 0
            return "error: ERROR - Task id already exists"
        else:
            try:
                self.tasks[taskid] = Task(cmd,taskid=taskid,task_vars=task_vars)
                self.tasks[taskid].start()
                yaml_done = False
                wait = False
                yaml_out = []
                timeout = 200 # approx 10 seconds
                while not yaml_done:
                    output = self.tasks[taskid].state()  # get output lines
                    if self.display: print(output)
                    if '...' in output or self.tasks[taskid].completed():
                        # found end of yaml, extract yaml
                        for line in output:
                            if line != '...':
                                yaml_out.append(line)
                            elif line == '...':
                                wait = True
                                break
                        yaml_done = True
                    timeout = timeout - 1
                    if timeout <= 0:
                        yaml_out.append("text: Timeout, no recognised task or yaml completion.")
                        yaml_done = True
                    time.sleep(0.05) # avoid hogging CPU
                if yaml_out and wait:
                    # append task data for follow up checks
                    # and clear yaml section from task state
                    y_len = len(yaml_out) + 1
                    yaml_out.append("task:")
                    yaml_out.append("  id: "+ str(taskid))
                    yaml_out.append("  line: " + str(y_len))  # report back start of main output
                    yaml_out.append("  task: OK")
                    return "\n".join(yaml_out)  # return yaml output
                elif yaml_out:
                    return "\n".join(yaml_out)  # return yaml output
                    if self.display: print("\n".join(yaml_out))
                    
            except Exception as err:
                print(err)
                return "error: ERROR executing task in runyaml"
        
    def remove(self, taskid):
        """
        Remove the task and associated output
        """
        if taskid in self.tasks:
            del self.tasks[taskid]
            return ["OK: Deleted"]
        else:
            return ["ERROR: No matching task id"]
        

    def state(self, taskid):
        """
        Return a pair of values
        - Boolean indicating whether task has completed or not
        - List of text lines output by the task
        
        TODO Should check authorisation/session
        """
        if taskid in self.tasks:
            task = self.tasks[taskid]
            return task.state()
        else:
            return ["ERROR: No matching task id"]

    def stateUpdate(self, taskid, line=0, titleTag=''):
        """
        Return a pair of values
        - List of text lines output by the task (from line onwards)
        - Length of output returned so far using this method

        TODO Should check authorisation/session
        """
        if taskid in self.tasks:
            task = self.tasks[taskid]
            return task.stateUpdate(line, titleTag)
        else:
            return ["ERROR: No matching task id"], 1
            

        


if __name__ == "__main__":
    """
    Main entry point, 'run' parameter followed by a package path will run the
    package as a one off and terminate (some output to stdout), most output to a 
    log file.
    Otherwise this will initialize service and keep running. This can accept a 
    single parameter of 'display' or 'debug' for help to see what is going on
    during troubleshooting.
    """
    if len(sys.argv) > 2 and sys.argv[1] == "run":
        # one off packagae execution
        once = TaskServer("run " + sys.argv[2])
    else:
        # service
        server = SimpleXMLRPCServer(("localhost",8001),allow_none=True)
        if len(sys.argv) > 1:
            server.register_instance(TaskServer(sys.argv[1]))
        else:
            server.register_instance(TaskServer(''))
        server.serve_forever()
