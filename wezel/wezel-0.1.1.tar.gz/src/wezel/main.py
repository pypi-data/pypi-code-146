import os
import sys
import venv
#import logging

# from PyQt5.QtWidgets import QApplication
# from PyQt5.QtCore import Qt
# from PyQt5.QtGui import QIcon

# import wezel

# QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
# QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)


# class Wezel:

#     def __init__(self):
#         self.app = None
#         self.log = logger()
#         self.QApp = QApplication(sys.argv)
#         self.QApp.setWindowIcon(QIcon(wezel.icons.favicon))
#         self.status = wezel.widgets.StatusBar()
#         self.main = wezel.core.Main(self)
#         self.main.setStatusBar(self.status)
#         self.dialog = wezel.widgets.Dialog(self.main)
#         self.app = wezel.core.Windows(self)

from wezel.core import Wezel


def app():

    return Wezel()



def post_installation_build_cleanup():
    print("Cleaning up building and compilation files...")
    windows = (sys.platform == "win32") or (sys.platform == "win64") or (os.name == 'nt')
    if windows:
        os.system('move dist\* .')
        os.system('rmdir build /S /Q')
        os.system('rmdir dist /S /Q')
        os.system('del myproject.spec')
        print("Deleting the created Python Virtual Environment for the process...")
        os.system('rmdir .venv /S /Q')
    else:
        os.system('mv dist/* .')
        os.system('rm -rf build/ dist/')
        os.system('rm myproject.spec')
        print("Deleting the created Python Virtual Environment for the process...")
        os.system('rm -r .venv/')

def activate():
    """Active virtual environment"""

    venv_dir = os.path.join(os.getcwd(), ".venv")
    os.makedirs(venv_dir, exist_ok=True)
    venv.create(venv_dir, with_pip=True)
    windows = (sys.platform == "win32") or (sys.platform == "win64") or (os.name == 'nt')
    if windows:
        return os.path.join(venv_dir, "Scripts", "activate")
    else: # MacOS and Linux
        return '. "' + os.path.join(venv_dir, "bin", "activate")

def install():
    """Install requirements to a virtual environment"""

    print('Creating virtual environment..')
    os.system('py -3 -m venv .venv')

    print('Installing requirements..')
    os.system(activate() + ' && ' + 'py -m pip install -r requirements.txt')  

def build(project, onefile=True, terminal=False, name='my_app', data_folders=[], hidden_modules=[]):
    """Generate project executable"""


    install()
    os.system(activate() + ' && ' + 'pip install pyinstaller')

#    hidden_modules = ['matplotlib']
#    hidden_imports = ' '.join(['--hidden-import '+ mod + ' ' for mod in hidden_modules])

#    windows = (sys.platform == "win32") or (sys.platform == "win64") or (os.name == 'nt')

    # if 'itk' in hidden_modules:
    #     # Pyinstaller doesn't have hooks for the itk package
    #     itk_path_win = '.venv\\lib\\site-packages\\itk'
    #     intermediate_python_folder = [fldr.name for fldr in os.scandir('venv/lib') if fldr.is_dir()][0] # It's known there's a Python subfolder between 'lib' and 'site-packages' for Unix systems
    #     itk_path_unix = '.venv/lib/' + intermediate_python_folder + '/site-packages/itk'
    
#     if windows:
#         all_data = [
#             'wezel\\widgets\\icons\\my_icons;.\\wezel\\widgets\\icons\\my_icons',
#             'wezel\\widgets\\icons\\fugue-icons-3.5.6;.\\wezel\\widgets\\icons\\fugue-icons-3.5.6',
#             'wezel;.\\wezel'
#             ]
# #        if 'itk' in hidden_modules: all_data.append(itk_path_win+';.\\itk')
#         for name in data_folders:
#             all_data.append(name+";./"+name) 
#     else:
#         all_data = [
#             'wezel/widgets/icons/my_icons:./wezel/widgets/icons/my_icons',
#             'wezel/widgets/icons/fugue-icons-3.5.6:./wezel/widgets/icons/fugue-icons-3.5.6',
#             'wezel:./wezel'
#             ]
#         # if 'itk' in hidden_modules: all_data.append(itk_path_unix+':./itk')
#         for name in data_folders:
#             all_data.append(name+":./"+name) 

#    add_data = ' '.join(['--add-data='+ mod + ' ' for mod in all_data])
    # hidden_imports = ' '.join(['--hidden-import '+ mod + ' ' for mod in hidden_modules])
    # # The following is a special situation for dbdicom and dipy
    # collect_data = ''
    # if 'dbdicom' in hidden_modules:
    #     collect_data += ' --collect-datas dbdicom'
    # if 'dipy' in hidden_modules:
    #     collect_data += ' --collect-datas dipy'
    # # wezel and widgets might be needed at --collect-datas in the future. 

    print('Creating executable..')
    cmd = activate() + ' && ' + 'pyinstaller --name "myproject" --clean'
    #cmd = activate() + ' && ' + 'pyinstaller --name '+ name + ' --clean'
    if onefile: 
        cmd += ' --onefile'
    if not terminal: 
        cmd += ' --noconsole'
    # cmd += ' ' + hidden_imports
    # cmd += ' ' + add_data
    # cmd += ' ' + collect_data
    cmd += ' ' + project + '.py'
    # if os.path.exists(os.path.join(os.getcwd(), project + '.py')):
    #     cmd += ' ' + project + '.py'
    # else:
    #     # Default option
    #     cmd += ' ' + "wezel\\main.py" 
    # # This command (and path!) may be different when wezel becomes a pip install package
    os.system(cmd)

#    post_installation_build_cleanup()


# def logger():
    
#     LOG_FILE_NAME = "wezel_log.log"
#     # creates some sort of conflict with mdreg - commenting out for now
# #    if os.path.exists(LOG_FILE_NAME):
# #        os.remove(LOG_FILE_NAME)
#     LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
#     logging.basicConfig(
#         filename = LOG_FILE_NAME, 
#         level = logging.INFO, 
#         format = LOG_FORMAT)
#     return logging.getLogger(__name__)


if __name__ == '__main__':
    wsl = app()
    wsl.show()