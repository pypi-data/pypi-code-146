# coding:utf-8
from tools_hjh.HTTPRequest import HTTPRequest
from math import ceil
from tools_hjh.Tools import mkdir
from tools_hjh.ThreadPool import ThreadPool
import os

    
def main():
    pass


class HTTPTools():
    
    @staticmethod
    def get_page(url, headers=None, data=None, proxies=None, encoding='UTF-8', timeout=None, stream=True, allow_redirects=True, verify=False):
        req = HTTPRequest(url=url, headers=headers, data=data, proxies=proxies, encoding=encoding, timeout=timeout, stream=stream, allow_redirects=allow_redirects, verify=verify)
        text = req.get_text()
        req.close()
        return text
    
    @staticmethod
    def get_size(url, headers=None, data=None, proxies=None, encoding='UTF-8', timeout=None, stream=True, allow_redirects=True, verify=False):
        req = HTTPRequest(url=url, headers=headers, data=data, proxies=proxies, encoding=encoding, timeout=timeout, stream=stream, allow_redirects=allow_redirects, verify=verify)
        text = req.get_size()
        req.close()
        return text
    
    @staticmethod
    def get_status_code(url, headers=None, data=None, proxies=None, encoding='UTF-8', timeout=None, stream=True, allow_redirects=True, verify=False):
        req = HTTPRequest(url=url, headers=headers, data=data, proxies=proxies, encoding=encoding, timeout=timeout, stream=stream, allow_redirects=allow_redirects, verify=verify)
        text = req.get_status_code()
        req.close()
        return text

    @staticmethod
    def download(url, filepath, replace=False, partsize=1024 * 1024, threadnum=1, headers=None, data=None, proxies=None, encoding='UTF-8', timeout=None, stream=True, allow_redirects=True, verify=False):
        req = HTTPRequest(url=url, headers=headers, data=data, proxies=proxies, encoding=encoding, timeout=timeout, stream=stream, allow_redirects=allow_redirects, verify=verify)
        if threadnum == 1:
            return req.download(filepath=filepath, replace=replace)
        else:
            tp = ThreadPool(threadnum)
            filesize = req.get_size()
            partnum = ceil(filesize / partsize)
            filepath = filepath.replace('\\', '/')
            path = filepath.rsplit('/', 1)[0] + '/'
            name = filepath.split('/')[-1]
            tmp_path = path + name + '_tmp/'
            mkdir(tmp_path)
            downloaded_files = []
            for idx in range(partnum):
                begin = idx * partsize + 1
                if idx == partnum - 1:
                    end = filesize
                else:
                    end = begin + partsize - 1
                new_filepath = tmp_path + str(idx)
                downloaded_files.append(new_filepath)
                new_headers = headers.copy()
                new_headers['Range'] = f'bytes={begin}-{end}'
                tp.run(HTTPTools.download, (url, new_filepath, True, 1024 * 1024, 1, new_headers, data, proxies, encoding, timeout, stream, allow_redirects, verify))
            tp.wait()
            
            size = 0
            filepath = open(filepath, 'wb')
            for downloaded_file in downloaded_files:
                if os.path.exists(downloaded_file):
                    f = open(downloaded_file, "rb")
                    tsfileRead = f.read()
                size = size + filepath.write(tsfileRead)
                f.close()
            # rm(m3u8TmpFileDir)
            filepath.close()
            return size
        
    @staticmethod
    def N_m3u8DL_CLI(url, filepath, filename, theadnum=32, exe_path='N_m3u8DL-CLI_v3.0.2.exe'):
        cmd = exe_path + ' --workDir ' + filepath + ' --saveName ' + filename + ' --maxThreads ' + str(theadnum) + ' --enableDelAfterDone ' + url
        os.popen('chcp 65001')
        os.system(cmd)

    
if __name__ == '__main__':
    main()
