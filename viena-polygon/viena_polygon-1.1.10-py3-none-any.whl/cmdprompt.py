import cmd, sys
from turtle import *
from polygon import parse
from polygon import rest_connect
import json
import typer
import simplejson
import traceback
import re
class PolygonShell(cmd.Cmd):
    intro = 'Welcome to the Polygon Query shell.   Type help or ? to list commands.\n'
    prompt = '>'
    file = None

    # ----- basic Polygon commands -----
    def do_select(self, arg):
        'Move the Polygon forward by the specified distance:  FORWARD 10'
        sqlResult=""
        try:
            data = ("**** polygon query **** \n"
                    " ##  Below are the tables that can be queried\n"
                    "        image, dataset, annotation, training_set, version, training_data\n"
                    " ##  Sql query :\n"
                    " ##      Example: \n"
                    "               1. select * from image\n"
                    "               2. select * from dataset limit 5\n"
                    "               3. select objectName from annotation\n"
                    "               4  select name,datasetId from dataset where active=1\n"
                    "               5. select datasetId,name from image where datasetId='<value>' | more\n"
                    " ##  NoSql query : \n"
                    "        Example: \n"
                    "                 db.image.find({'datasetId':'<value>'})\n"
                    "                 db.dataset.find({'name':'<value>'})\n"
                    "                 db.image.count({'datasetId':'<value>'})\n"
                    "                 db.annotation.find({'objectName':'<value>'})")
            cvargs=[]
            operation=[]
            status=True
            if '|' in arg:
                queryTmp=arg.split("|")
                for i in range(len(queryTmp)):
                    if(i==0):
                        args = queryTmp[i]
                    else:
                        text=queryTmp[i]
                        if (text == "more" or text == "More"):
                            outptDisplay = True
                        else:
                            cvtype = text.lstrip()
                            word = cvtype.split()[0]
                            if (word.lower() == "blur"):
                                y = cvtype.split("--percentage=")
                                per=re.sub('\W+','', y[1])
                                if (int(per) > 0 and int(per) < 100):
                                    x = ["blur1", int(per)]
                                    cvargs.append(x)
                                else:
                                    print("You have an error in your query syntax")
                                    print("Blur percentage value should be in range 1-100")
                                    status=False
                                    break
                            elif(word.lower() == "verticalflip"):
                                x = ["verticalflip"]
                                cvargs.append(x)
                            elif (word.lower() == "horizontalflip"):
                                x = ["horizontalflip"]
                                cvargs.append(x)
                            elif (word.lower() == "grayscale"):
                                x = ["grayscale"]
                                cvargs.append(x)
                            elif (word.lower() == "upscale"):
                                y = cvtype.split("--percentage=")
                                per = re.sub('\W+', '', y[1])
                                if (int(per) > 0):
                                    x = ["upscale", int(per)]
                                    cvargs.append(x)
                                else:
                                    print("You have an error in your query syntax")
                                    print("Upscale percentage value should be greater than 0")
                                    status = False
                                    break
                            elif (word.lower() == "downscale"):
                                y = cvtype.split("--percentage=")
                                per = re.sub('\W+', '', y[1])
                                if (int(per) > 0 and int(per) < 50):
                                    x = ["downscale", int(per)]
                                    cvargs.append(x)
                                else:
                                    print("You have an error in your query syntax")
                                    print("Downscale percentage value should be in range 1-50")
                                    status = False
                                    break
                            elif (word.lower() == "addwatermark"):
                                y = cvtype.split("--text=")
                                per = re.sub('\W+', '', y[1])
                                if (per !=""):
                                    x = ["addwatermark", per]
                                    cvargs.append(x)
                                else:
                                    print("You have an error in your query syntax")
                                    print("Downscale percentage value should be in range 1-50")
                                    status = False
                                    break
                            elif (word.lower() == "bilateralfilter"):
                                x = ["bilateralfilter"]
                                cvargs.append(x)
                            elif (word.lower() == "boxfilter"):
                                x = ["boxfilter"]
                                cvargs.append(x)
                            elif (word.lower() == "sharpeningfilter"):
                                x = ["sharpeningfilter"]
                                cvargs.append(x)
                            elif (word.lower() == "embossfilter"):
                                x = ["embossfilter"]
                                cvargs.append(x)
                            elif (word.lower() == "erode"):
                                x = ["erode"]
                                cvargs.append(x)
                            elif (word.lower() == "dilate"):
                                x = ["dilate"]
                                cvargs.append(x)
                            elif (word.lower() == "morphology"):
                                x = ["morphology"]
                                cvargs.append(x)
                            elif (word.lower() == "addborder"):
                                x = ["addborder"]
                                cvargs.append(x)
                            elif(word.lower()=="copy" or  word.lower()=="download"):
                                copyType=-1
                                if(word.lower()=="copy"):
                                    if("--datasetid=" in cvtype.lower()):
                                        copyType=0
                                    elif("--datasetname=" in cvtype.lower()):
                                        copyType = 1
                                    if(copyType==0):
                                        y = cvtype.split("--datasetid=")
                                        per = re.sub('\W+', '', y[1])
                                        operation.append("copy")
                                        operation.append(0)
                                        operation.append(per)
                                    elif(copyType==1):
                                        y = cvtype.split("--datasetname=")
                                        per = re.sub('\W+', '', y[1])
                                        operation.append("copy")
                                        operation.append(per)
                                        operation.append(0)
                                elif(word.lower()=="download"):
                                    operation.append("download")
            else:
                args=arg
                outptDisplay =False

            if(status==True):
                query="select "+ str(args)
                parsedData=parse.parse_sql(query)
                sqlResult=""
                if(len(cvargs)>0):
                    datasetDetails=json.loads(parsedData[2])
                    datasetname=""
                    datasetid=""
                    for key in datasetDetails:
                        if(key.lower()=="datasetid"):
                            datasetid = eval(datasetDetails[key])
                        if (key.lower() == "datasetname"):
                            datasetname = eval(datasetDetails[key])
                    if(datasetid=="" and datasetname==""):
                        print("You have an error in your query syntax")
                        print("Dastaset name or dataset Id is missing in where clause to perform cv function")
                    else:
                        sqlResult = rest_connect.processCvfunctions(operation,cvargs,datasetname,datasetid)
                else:
                    sqlResult = rest_connect.sqlreslt(parsedData)
                    error1 = sqlResult["error"]
                    cnt = sqlResult["count"]
                    res = sqlResult["results"]
                    if (error1 != None):
                        print(sqlResult)
                        print('\033[92m' +data)
                    elif (outptDisplay == True):
                        x={
                            "count":cnt,
                            "results":res,
                        }
                        data = simplejson.dumps(x, indent=4)
                        cnt = 0
                        for line in data.split('\n'):
                            cnt += 1
                            print(line)
                            input("Press Enter to continue") if cnt % 30 == 0 else None
                    else:
                        x = {
                            "count": cnt,
                            "results": res,
                        }
                        print(json.dumps(x, indent=3))
        except Exception:
            traceback.print_exc()
            print("You have an error in your query syntax")
            print(sqlResult)
            #print('\033[92m' +data)

    def createop(self,name,classes,targetcloudstoragename):
        print("createop")
        print(name)
        print(classes)
        print(targetcloudstoragename)
        print("createop")

    def do_db(self, arg):
        'Move the Polygon forward by the specified distance:  FORWARD 10'
        nosqlResult=""
        try:
            data = ("**** polygon query **** \n"
                    " ##  Below are the tables that can be queried\n"
                    "        image, dataset, annotation, training_set, version, training_data\n"
                    " ##  Sql query :\n"
                    " ##      Example: \n"
                    "               1. select * from image\n"
                    "               2. select * from dataset limit 5\n"
                    "               3. select objectName from annotation\n"
                    "               4  select name,datasetId from dataset where active=1\n"
                    "               5. select datasetId from image where datasetId='<value>' | more\n"
                    " ##  NoSql query : \n"
                    "        Example: \n"
                    "                 db.image.find({'datasetId':'<value>'})\n"
                    "                 db.dataset.find({'name':'<value>'})\n"
                    "                 db.image.count({'name':'<value>'})\n"
                    "                 db.annotation.find({'objectName':'<value>'})")
            if '|' in arg:
                x = arg.split("|")
                args = x[0]
                outptDisplay = True
            else:
                args = arg
                outptDisplay = False
            pharse="db"+args
            nosqlResult = rest_connect.nosqlreslt(pharse)

            error1=nosqlResult["error"]
            cnt=nosqlResult["count"]
            res=nosqlResult["results"]
            if(error1 !=None):
                print(nosqlResult)
                print('\033[92m' +data)
            elif(outptDisplay == True):
                x = {
                    "count": cnt,
                    "results": res,
                }
                data = simplejson.dumps(x, indent=4)
                cnt = 0
                for line in data.split('\n'):
                    cnt += 1
                    print(line)
                    input("Press Enter to continue") if cnt % 30 == 0 else None
            else:
                x = {
                    "count": cnt,
                    "results": res,
                }
                print(json.dumps(x, indent=3))
        except:
            print("You have an error in your query syntax")
            print(nosqlResult)
            print('\033[92m' +data)


    def do_bye(self, arg):
        'Stop recording, close the  window, and exit:  BYE'
        print(arg)
        print('Thank you for using Polygon')
        self.close()
        bye()
        return True

    def do_clear(self, arg):
        print("\033c")

    def do_help(self, arg):
        data = ("**** polygon query **** \n"                
                    " ##  Below are the tables that can be queried\n"
                    "        image, dataset, annotation, training_set, version, training_data\n"
                    " ##  Sql query :\n"
                    " ##      Example: \n"
                    "               1. select * from image\n"
                    "               2. select * from dataset limit 5\n"
                    "               3. select objectName from annotation\n"
                    "               4  select name,datasetId from dataset where active=1\n"
                    "               5. select datasetId from image where datasetId='<value>' | more\n"
                    " ##  NoSql query : \n"
                    "        Example: \n"
                    "                 db.image.find({'datasetId':'<value>'})\n"
                    "                 db.dataset.find({'name':'<value>'})\n"
                    "                 db.image.count({'name':'<value>'})\n" 
                    "                 db.annotation.find({'objectName':'<value>'})")
        print('\033[92m'+data)

    def pagetext(self,text_lined, num_lines=25):
        for index, line in enumerate(text_lined):
            if index % num_lines == 0 and index:
                input = raw_input("Hit any key to continue press q to quit")
                if input.lower() == 'q':
                    break
            else:
                print(line)

    # ----- record and playback -----
    def do_record(self, arg):
        'Save future commands to filename:  RECORD rose.cmd'
        self.file = open(arg, 'w')
    def do_playback(self, arg):
        'Playback commands from a file:  PLAYBACK rose.cmd'
        self.close()
        with open(arg) as f:
            self.cmdqueue.extend(f.read().splitlines())
    def precmd(self, line):
        # line = line.lower()
        if self.file and 'playback' not in line:
            print(line, file=self.file)
        return line
    def close(self):
        if self.file:
            self.file.close()
            self.file = None

if __name__ == '__main__':
    PolygonShell().cmdloop()