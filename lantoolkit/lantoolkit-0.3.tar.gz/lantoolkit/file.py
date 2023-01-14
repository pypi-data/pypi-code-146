import shutil,os,platform
def cpfiledata(a, b):
    try:
        file1 = open(a)
        file2 = open(b, "w")
        shutil.copyfileobj(file1, file2)
    except IOError as e:
        print("could not open file or no such file:", e)
        print("无法打开文件或无此文件：", e)


def cpflieper(src, dst):
    try:
        if os.path.isdir(dst):
            dst = os.path.join(dst, os.path.basename(src))
            shutil.copyfile(src, dst)
            shutil.copymode(src, dst)
    except IOError as e:
        print("could not open file or no such files:", e)
        print("无法打开文件或无该文件：", e)


def cpfiletree(a, b):
    try:
        shutil.copytree(a, b)
    except IOError as e:
        print("could not open file or no such files:", e)
        print("无法打开文件树或无该文件树：", e)


# noinspection PyUnboundLocalVariable
def rmtree(fdir):
    try:
        shutil.rmtree(fdir)
    except IOError as e:
        print("could not open file or no such files:", e)
        print("无法打开文件或无该文件：", e)


def mvfile(src, dst):
    try:
        shutil.move(src, dst)
    except IOError as e:
        print("could not open file or no such files:", e)
        print("无法打开文件或无该文件：", e)


def rmfile(src):
    try:
        os.remove(src)
    except IOError as e:
        print("could not open file or no such files:", e)
        print("无法打开文件或无该文件：", e)


def renames(old, new):
    try:
        os.renames(old, new)
    except IOError as e:
        print("could not open file or no such files:", e)
        print("无法打开文件或无该文件：", e)


def path(file):
    # B  ct=25920000
    print("文件名：" + os.path.basename(file))
    # B  print( '最近访问时间：'+str(int(float(os.path.getatime(file))/ct))+'天前' )
    # B  print( '创建时间：'+str(float(os.path.getctime(file))/ct)+'天前' )
    # B  print( '最近修改时间：'+str(int(float(os.path.getmtime(file))/ct))+'天前' )

    if int(os.path.getsize(file)) >= 1024 * 1024 * 1024 * 1024 * 1024:
        print(
            "文件大小："
            + str(int(os.path.getsize(file)) / 1125899906842624)
            + "Pib"
        )
    elif int(os.path.getsize(file)) >= 1024 * 1024 * 1024 * 1024:
        print(
            "文件大小：" + str(int(os.path.getsize(file)) / 1099511627776) + "Tib"
        )
    elif int(os.path.getsize(file)) >= 1024 * 1024 * 1024:
        print("文件大小：" + str(int(os.path.getsize(file)) / 1073741824) + "Gib")
    elif int(os.path.getsize(file)) >= 1024 * 1024:
        print("文件大小：" + str(int(os.path.getsize(file)) / 1048576) + "Mib")
    elif int(os.path.getsize(file)) >= 1024:
        print("文件大小：" + str(int(os.path.getsize(file)) / 1024) + "Kib")
    else:
        print("文件大小：" + str(int(os.path.getsize(file))) + "B")
    print("文件路径：", os.path.abspath(file))  # 输出绝对路径
    print(os.path.normpath(file))  # 规范path字符串形式


def cpfile(a, b):
    try:
        shutil.copyfile(a, b)
    except IOError as e:
        print("could not open file or no such files:", e)
        print("无法打开文件或无该文件：", e)


def listfile(tdir):
    plat = platform.system().lower()
    if plat == "windows":
        if tdir == "":
            os.system("dir")
        else:
            os.system("cd %s" % tdir)
            os.system("dir")
    else:
        if tdir == "":
            os.system("ls")
        else:
            os.system("cd %s" % tdir)
            os.system("ls")