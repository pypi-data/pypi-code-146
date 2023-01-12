# encoding: utf-8
import jdk
import glob
import os
import urllib.request
import psutil

current_path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
main_path = os.path.dirname(current_path)

class SeleniumGridServer():
    def __init__(self):
        self.killdriver()
        java_path = self.java_loader()
        selenium_path = self.selenium()
        command = '%s/java -jar %s standalone --port 4444' %(java_path, selenium_path)
        os.popen(command)
        
    def killdriver(self):
        for proc in psutil.process_iter():
            if 'chromedriver' in proc.name():
                proc.kill()
            if 'geckodriver' in proc.name():
                proc.kill()
            if 'edgedriver' in proc.name():
                proc.kill()
                
    def java_loader(self):
        if 'windows' in jdk.OS:
            java_name = '%s/jdk*/bin' %(main_path)
        else:
            java_name = '%s/jdk*/Contents/Home/bin' %(main_path)
        os_name = glob.glob(java_name)
        if len(os_name) == 0:
            jdk.install(version='11', path=main_path)
            os_name = glob.glob(java_name)
        return os_name[0].replace('\\', '/')
        
    def selenium(self):
        if not 'selenium-server.jar' in os.listdir(main_path):
            url = 'https://objects.githubusercontent.com/github-production-release-asset-2e65be/7613257/4c92f970-137f-43a4-82d2-6048bdd593b0?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20230112%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20230112T053219Z&X-Amz-Expires=300&X-Amz-Signature=ee407ee6f9132e95c41c356e05fc1ce2f389bc2dadd87b2436c81caba14441f7&X-Amz-SignedHeaders=host&actor_id=0&key_id=0&repo_id=7613257&response-content-disposition=attachment%3B%20filename%3Dselenium-server-4.7.2.jar&response-content-type=application%2Foctet-stream'
            urllib.request.urlretrieve(url, '%s/selenium-server.jar' %(main_path))
        return '%s/selenium-server.jar' %(main_path)

SeleniumGridServer()