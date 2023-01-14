import numpy as np
import os, sys
import json, requests, ast
import pkg_resources
import GPUtil, platform, psutil


IP = '54.226.28.103:8000'
#IP = '127.0.0.1:8000'

def reset_os_variables():
    os.environ['prev_node'] = "-999"
    
    os.environ["prev_filename"] = ''
    os.environ["prev_filename2"] = ''
    os.environ["prev_filename3"] = ''
    os.environ["prev_filename4"] = ''
    os.environ["prev_filename5"] = ''
    os.environ["prev_filename6"] = ''

    os.environ["prev_filename7"] = ''
    os.environ["prev_filename8"] = ''
    os.environ["prev_filename9"] = ''
    os.environ["prev_filename10"] = ''
    os.environ["prev_filename11"] = ''
    os.environ["prev_filename12"] = ''

    os.environ["prev_func"] = ''
    os.environ["prev_func1"] = ''
    os.environ["prev_func2"] = ''
    os.environ["prev_func3"] = ''
    os.environ["prev_func4"] = ''
    os.environ["prev_func5"] = ''

    os.environ["call"] = ''
    os.environ["return"] = '' 

    os.environ["include_variables"] = 'False'
    os.environ["variables_to_track"] = ''
    os.environ["variables_to_not_track"] = ''
  

def login(username, key):
  print("Logging in...")
  credentials = {'username':username, 'key':key, 'task':'login'}
  response = requests.post('http://'+IP+'/api/python_login', data=credentials)
  
  if response.text == '1':
    reset_os_variables()
    os.environ["username"] = username
    os.environ["key"] = key
    print("Successfully connected to mynacode!")
  else:
    print("Credentials could not be verified.")


def project(project_name):

  os.environ['project_name'] = project_name
    
  installed_packages = pkg_resources.working_set #Save all installed packages for that project
  installed_packages_list = sorted(["%s = %s" % (i.key, i.version) for i in installed_packages])

  project_info_list = ['Codebase Python ' + platform.python_version()]
  
  project_info_list.append("    GPU    ")
  try:
      gpus = GPUtil.getGPUs()
      if len(gpus) == 0:
          project_info_list.append("No NVIDIA GPU found")
      else:
          for gpu in gpus:
            gpu_id = gpu.id
            gpu_name = gpu.name
            gpu_memory = gpu.memoryTotal
            project_info_list.append("GPU ID " + str(gpu_id))
            project_info_list.append(gpu_name)
            project_info_list.append(str(gpu_memory) + " MB")
  except:
      project_info_list.append("No NVIDIA Driver found")

  project_info_list.append("    CPU    ")
  project_info_list.append(platform.processor())
  project_info_list.append(platform.platform())
  project_info_list.append(platform.machine())
  project_info_list.append("    MEMORY    ")
  project_info_list.append("RAM " + str(round(psutil.virtual_memory().total / (1024.0 **3))) + " GB")

  data = {'project_name': project_name, 'installed_packages': str(installed_packages_list),
          'username': os.environ['username'], 'key': os.environ['key'], 'project_information': str(project_info_list)}
  
  response = requests.post('http://'+IP+'/api/create_project', data=data)
  
  if response.text == '0':
    print("Authentication failed")
  else:
    response_dict = ast.literal_eval(response.text)
    
    if response_dict['exists'] == 0:
      print("Created a new project.")
    else:
      print("Project exists. Created a new run")
      
  os.environ['project_id'] = str(response_dict['project_id'])
  reset_os_variables()
  #os.environ["prev_file"] = ''
  #os.environ["prev_func"] = ''
  #os.environ['prev_node'] = "-999"      
  
def node(node_name = "", filename = "", lineno = 0, node_description="", library_function = 0):

  if os.environ['prev_node'] == "-999":
    data = {'current_node_name': node_name, 'node_description': node_description,
            'username': os.environ['username'], 'key': os.environ['key'], 'project_id': os.environ['project_id'],
            'filepath': filename, 'line_number': lineno, 'library_function': library_function}
  else:
    data = {'current_node_name': node_name, 'connect_with':  os.environ['prev_node'], 'node_description': node_description,
            'username': os.environ['username'], 'key': os.environ['key'], 'project_id': os.environ['project_id'],
            'filepath': filename, 'line_number': lineno, 'library_function': library_function}

  response = requests.post('http://'+IP+'/api/create_node', data=data)

  if response.text == '-1':
    print("Authentication failed")
  elif response.text == '-3':
    print("Node repeated")
  else:
    print(response.text)

      
    os.environ['prev_node'] = response.text #Store previous node
    #os.environ["prev_func"] = node_name
    #os.environ["prev_file"] = filename  


def node_log(variables, main_function = False):
  if len(variables) == 0:
    return 0

  if main_function == True:
      data = {'project_id':os.environ['project_id'], '_id': os.environ['prev_node'], 'type':'node', 'variables': str(variables), 'username': os.environ['username'], 'key': os.environ['key'], 'main_function':1}
  else:
      data = {'_id': os.environ['prev_node'], 'type':'node', 'variables': str(variables), 'username': os.environ['username'], 'key': os.environ['key'], 'main_function':0}

  response = requests.post('http://'+IP+'/api/set_variables', data=data)


def include_variables(status = False, include_only = [], exclude_only = []):
  if status == False:
    return
  elif status == True:
    os.environ["include_variables"] = 'True'
    
    if len(include_only) != 0:
      variables_to_track = []
      for var in include_only:
        variables_to_track.append(var)
      os.environ["variables_to_track"] = str(variables_to_track)
      print(os.environ["variables_to_track"])
      
    elif len(exclude_only) != 0:
      variables_to_not_track = []
      for var in exclude_only:
        variables_to_not_track.append(var)
      os.environ["variables_to_not_track"] = str(variables_to_not_track)
      print(os.environ["variables_to_not_track"])
      
    else:
      pass


def tracefunc(frame, event, arg, indent=[0]):
    save_function = False
    library_function = False

    if ('_init_' in frame.f_code.co_name and (('torch' in frame.f_code.co_filename and 'cuda' not in frame.f_code.co_filename and 'cudnn' not in frame.f_code.co_filename and 'opt_einsum' not in frame.f_code.co_filename and 'utils' not in frame.f_code.co_filename and '_internal' not in frame.f_code.co_filename and '_prims_common' not in frame.f_code.co_filename and 'onnx' not in frame.f_code.co_filename and 'jit' not in frame.f_code.co_filename and 'distribut' not in frame.f_code.co_filename and 'multiprocessing' not in frame.f_code.co_filename and 'quantiz' not in frame.f_code.co_filename and 'mkldnn' not in frame.f_code.co_filename and 'fx' not in frame.f_code.co_filename) or ('sklearn' in frame.f_code.co_filename and 'externals' not in frame.f_code.co_filename and 'utils' not in frame.f_code.co_filename)  or ('keras' in frame.f_code.co_filename and 'utils' not in frame.f_code.co_filename and 'engine' not in frame.f_code.co_filename and 'mixed_precision' not in frame.f_code.co_filename and 'initializers' not in frame.f_code.co_filename and 'saved_model' not in frame.f_code.co_filename and 'backend' not in frame.f_code.co_filename))):
      
      if not os.environ["prev_filename"] == frame.f_code.co_filename:
        if not os.environ["prev_filename2"] == frame.f_code.co_filename:
          if not os.environ["prev_filename3"] == frame.f_code.co_filename:
            if not os.environ["prev_filename4"] == frame.f_code.co_filename:
              if not os.environ["prev_filename5"] == frame.f_code.co_filename:
                if not os.environ["prev_filename6"] == frame.f_code.co_filename:
                  if not os.environ["prev_filename7"] == frame.f_code.co_filename:
                    if not os.environ["prev_filename8"] == frame.f_code.co_filename:
                      if not os.environ["prev_filename9"] == frame.f_code.co_filename:
                        if not os.environ["prev_filename10"] == frame.f_code.co_filename:
                          if not os.environ["prev_filename11"] == frame.f_code.co_filename:
                            if not os.environ["prev_filename12"] == frame.f_code.co_filename:

                              #print("Library:", frame.f_code.co_name, frame.f_code.co_filename)
                              #print("\n\n")

                              os.environ["prev_filename12"] = os.environ["prev_filename11"]
                              os.environ["prev_filename11"] = os.environ["prev_filename10"]
                              os.environ["prev_filename10"] = os.environ["prev_filename9"]
                              os.environ["prev_filename9"] = os.environ["prev_filename8"]
                              os.environ["prev_filename8"] = os.environ["prev_filename7"]
                              os.environ["prev_filename7"] = os.environ["prev_filename6"]
                              os.environ["prev_filename6"] = os.environ["prev_filename5"]
                              os.environ["prev_filename5"] = os.environ["prev_filename4"]

                              os.environ["prev_filename4"] = os.environ["prev_filename3"]
                              os.environ["prev_filename3"] = os.environ["prev_filename2"]
                              os.environ["prev_filename2"] = os.environ["prev_filename"]
                              os.environ["prev_filename"] = frame.f_code.co_filename

                              save_function = True
                              library_function = True
                              
    elif 'Attributes' in frame.f_code.co_filename or 'Attributes' in frame.f_code.co_name:
        pass
    elif "Python" in frame.f_code.co_filename:
        pass
    elif "<module" in frame.f_code.co_name:
        pass
    elif ("<" in frame.f_code.co_name or "<" in frame.f_code.co_filename) and ("<ipython-input" not in frame.f_code.co_filename):
        pass
    elif "site-packages" in frame.f_code.co_filename:
        pass
    elif "dist-packages" in frame.f_code.co_filename:
        pass
    elif "lib/python" in frame.f_code.co_filename:
        pass
    else:
        save_function = True
        
    if save_function:
        
        if event == "call":
            if not library_function:
              if os.environ["prev_func"] == frame.f_code.co_name or os.environ["prev_func1"] == frame.f_code.co_name or os.environ["prev_func2"] == frame.f_code.co_name or os.environ["prev_func3"] == frame.f_code.co_name or os.environ["prev_func4"] == frame.f_code.co_name or os.environ["prev_func5"] == frame.f_code.co_name:
                print("Node Repeated")
                return
              else:
                os.environ["prev_func5"] = os.environ["prev_func4"]
                os.environ["prev_func4"] = os.environ["prev_func3"]
                os.environ["prev_func3"] = os.environ["prev_func2"]
                os.environ["prev_func2"] = os.environ["prev_func1"]
                os.environ["prev_func1"] = os.environ["prev_func"]
                os.environ["prev_func"] = frame.f_code.co_name

            print(frame.f_code.co_name, frame.f_code.co_filename)

            if library_function == True:
                print("library function")
                print(frame.f_code.co_filename.rsplit('/', 1)[1])
                node(frame.f_code.co_filename.rsplit('/', 1)[1], frame.f_code.co_filename, frame.f_code.co_firstlineno,"", 1)
            else:
              if 'ipykernel' not in frame.f_code.co_filename:
                  node(frame.f_code.co_name, frame.f_code.co_filename, frame.f_code.co_firstlineno,"", 0)
              else:
                  node(frame.f_code.co_name, 'Jupyter notebook', 0,"", 0)

        if event == "return":
            variables_to_log = {}
            if os.environ["include_variables"] == 'True':
              if len(os.environ["variables_to_track"]) != 0:
                variables_to_track = ast.literal_eval(os.environ["variables_to_track"])
                for key in frame.f_locals:
                  if key in variables_to_track:
                    variables_to_log[key] = frame.f_locals[key]
                    
              elif len(os.environ["variables_to_not_track"]) != 0:
                variables_to_not_track = ast.literal_eval(os.environ["variables_to_not_track"])
                for key in frame.f_locals:
                  if key not in variables_to_not_track:
                    variables_to_log[key] = frame.f_locals[key]
                    
              else:
                for key in frame.f_locals:
                  variables_to_log[key] = frame.f_locals[key]                
                          

              if frame.f_code.co_name == 'main':
                  node_log(variables_to_log, True)
              else:
                  node_log(variables_to_log, False)

        return tracefunc


# FUNCTION TO STORE VARIABLES
   
def settrace():
  sys.setprofile(tracefunc)


