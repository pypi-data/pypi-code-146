class checkdiralldata:
    def __init__(self,imagedirlocation):
        import os
        originaljson=[]
        image=[]
        for filename in os.listdir(imagedirlocation):
            if filename.split(".")[1]=="json":
                originaljson.append(filename)
            if filename.split(".")[1]=="jpg":
                image.append(filename)
        self.originaljson=originaljson
        self.image=image
    
    def check_file_in_alldata(self):
        print("all資料夾內")
        if len(self.originaljson)==len(self.image):
            different=0
            for i in range(len(self.image)):
                n=0
                for j in range(len(self.originaljson)): 
                    if "carpl_"+self.image[i].split("_")[1].split(".")[0]+".json"==self.originaljson[j]:
                        break
                    n=n+1
                if n==len(self.originaljson):
                    print(self.image[i]+"無對應的原json")
                    different=different+1
            for i in range(len(self.originaljson)):
                n=0
                for j in range(len(self.image)): 
                    if "carpl_"+self.originaljson[i].split("_")[1].split(".")[0]+".jpg"==self.image[j]:
                        break
                    n=n+1
                if n==len(self.image):
                    print(self.originaljson[i]+"無對應的image")
                    different=different+1
            if different==0:
                print("image與json無相異處")
        elif len(self.originaljson)<len(self.image):
            print("image多了")
            for i in range(len(self.image)):
                n=0
                for j in range(len(self.originaljson)): 
                    if "carpl_"+self.image[i].split("_")[1].split(".")[0]+".json"==self.originaljson[j]:
                        break
                    n=n+1
                if n==len(self.originaljson):
                    print(self.image[i])
        elif len(self.originaljson)>len(self.image):
            print("原json多了")
            for i in range(len(self.originaljson)):
                n=0
                for j in range(len(self.image)): 
                    if "carpl_"+self.originaljson[i].split("_")[1].split(".")[0]+".jpg"==self.image[j]:
                        break
                    n=n+1
                if n==len(self.image):
                    print(self.originaljson[i])

class cocotidy:
    def __init__(self,labelfilelocation,jsonfilelocation,imagedirlocation):
        import json
        with open(jsonfilelocation) as f:
            cocojson = json.load(f)
        self.labelfilelocation=labelfilelocation
        self.jsonfilelocation=jsonfilelocation
        self.imagedirlocation=imagedirlocation
        self.cocojson=cocojson

    def check_categories(self):
        t = open(self.labelfilelocation).read()
        open(self.labelfilelocation).close()

        catlabel=[]
        a=""
        for i in range(len(t)):
            if (t[i]!="\n"):
                a=a+t[i]
                if i==(len(t)-1):
                    catlabel.append(a)
                    a=""   
            elif (t[i]=="\n"):
                catlabel.append(a)
                a=""            
        # print(catlabel)

        catjson=[]
        for i in range(len(self.cocojson["categories"])):
            if i==len(self.cocojson["categories"])-1:
                print("\""+self.cocojson["categories"][i].get("supercategory")+"\"")
            else:
                print("\""+self.cocojson["categories"][i].get("supercategory")+"\""+",", end = "")
            catjson.append(self.cocojson["categories"][i].get("supercategory"))
        # print(catjson)

        if len(catlabel)==len(catjson):
            print("種類無誤")
        elif len(catlabel)>len(catjson):
            print("此jpg資料集無以下所列種類")
            different=0
            for i in range(len(catlabel)):
                n=0
                for j in range(len(catjson)): 
                    if catlabel[i]==catjson[j]:
                        break
                    n=n+1
                if n==len(catjson):
                    print(catlabel[i])
                    different=different+1
            print(f"共{different}種")
        else:
            strange=[]
            print("此jpg資料集多標了一些奇怪的種類如下")
            different=0
            for i in range(len(catjson)):
                n=0
                for j in range(len(catlabel)): 
                    if catjson[i]==catlabel[j]:
                        break
                    n=n+1
                if n==len(catlabel):
                    strange.append(catjson[i])
                    print(catjson[i])
                    different=different+1
            print(f"共{different}種")
            for i in range(len(strange)):
                print(f"第{i+1}種:"+strange[i])
                n=0
                s=[]
                for j in range(len(self.cocojson["categories"])):
                    if strange[i]==self.cocojson["categories"][j]["supercategory"]:
                        for k in range(len(self.cocojson["annotations"])):
                            if self.cocojson["categories"][j]["id"]==self.cocojson["annotations"][k]["category_id"]:
                                for l in range(len(self.cocojson["images"])):
                                    if self.cocojson["annotations"][k]["image_id"]==self.cocojson["images"][l]["id"]:
                                        s.append(self.cocojson["images"][l]["file_name"].split("_")[1].split(".")[0])
                                        n=n+1
                print(f"共{n}處分別為")
                s=sorted(s)
                for j in range(len(s)):
                    print("carpl_"+s[j]+".jpg")

    def split_all(self):
        import os
        import shutil
        if not os.path.exists("coco"):
            os.mkdir("coco")
        if not os.path.exists("coco\\annotations"):
            os.mkdir("coco\\annotations")
        if not os.path.exists("coco\\train2017"):
            os.mkdir("coco\\train2017")
        if not os.path.exists("coco\\val2017"):
            os.mkdir("coco\\val2017")
        print(self.jsonfilelocation.split("\\")[1].split(".")[0]+"2017"+"共有"+str(len(self.cocojson["images"]))+"筆")
        for i in range(len(self.cocojson["images"])):
            shutil.copy(self.imagedirlocation+"\\"+self.cocojson["images"][i]["file_name"],"coco\\"+self.jsonfilelocation.split("\\")[1].split(".")[0]+"2017"+"\\"+self.cocojson["images"][i]["file_name"])
        shutil.copy(self.jsonfilelocation,"coco\\annotations")
def add_one(number):
    return number + 1