#!/usr/bin/env python3
import os
import subprocess
import sys
import argparse

def parseArgs(args):
    parser = argparse.ArgumentParser(description="用BaiduPCS-GO上传数据到百度网盘, 使用之前需要登录")
    parser.add_argument('--indir',
                        '-i',
                        help='需要上传的目录, 请指定到上传的目录如:pro_dir/Upload, 切勿指定到项目目录, 否则会上传整个项目',
                        required=True)
    parser.add_argument('--remote',
                        '-o',
                        help='网盘路径,如:/2022/0001-0100/project/Data/',
                        required=True)
    return parser.parse_args(args)

def main(args):
    args = parseArgs(args)
    os.chdir(args.indir)
    files = subprocess.getoutput("find . " ).split()
    for file in files:
        if os.path.isdir(file):
            continue
        dir = file.split("/")[1:-1]	        # remote_dest不能是指向文件, 否则将会创建一个同名目录
        remote_dest = args.remote
        for d in dir:
            remote_dest = os.path.join(remote_dest,d)
        file = subprocess.getoutput("readlink -f %s" %(file))
        os.system("BaiduPCS-Go upload %s %s" %(file,remote_dest))

if __name__ == "__main__":
    main(sys.argv[1:])
