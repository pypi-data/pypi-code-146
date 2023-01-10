from queue import Queue
from .db import model
from .db import sqlite as kcwsqlite
import threading,time,os,hashlib,random,traceback,multiprocessing
queuesdbpath=os.path.split(os.path.realpath(__file__))[0]+"/Queues"
class model_kcweb_task(model.model):
    "任务"
    config={'type':'sqlite','db':queuesdbpath}
    model.dbtype.conf=config
    table="model_kcweb_queues" 
    fields={
        "id":model.dbtype.int(LEN=11,PRI=True,A_L=True),        #设置id为自增主键
        "taskid":model.dbtype.varchar(LEN=32,DEFAULT=''),        #设置id为自增主键
        "title":model.dbtype.varchar(LEN=1024,DEFAULT=''),      #名称
        "describes":model.dbtype.varchar(LEN=2048,DEFAULT=''),  #描述
        "code":model.dbtype.int(LEN=11,DEFAULT=2),              #状态码 0成功 1失败 2等待中 3正在执行  4完成
        "msg":model.dbtype.text(),                              #状态描述
        "error":model.dbtype.text(),                            #异常信息
        "start":model.dbtype.varchar(LEN=11,DEFAULT=0),             #进度条起始值
        "end":model.dbtype.int(LEN=11,DEFAULT=100),               #进度条结束值
        "starts":model.dbtype.varchar(LEN=11,DEFAULT=0),             #每秒钟进度条起始值增加多少
        "addtime":model.dbtype.int(LEN=11,DEFAULT=0),            #添加时间
        "endtime":model.dbtype.int(LEN=11,DEFAULT=0),            #结束时间
        "updtime":model.dbtype.int(LEN=11,DEFAULT=0)            #更新时间
    }
class Queues():
    __globalqueue=None
    __processglobalqueue=None
    def __start():
        if not Queues.__globalqueue:
            if not os.path.isfile(queuesdbpath):
                model_kcweb_tasks=model_kcweb_task()
                model_kcweb_tasks.create_table()
            try:
                kcwsqlite.sqlite().connect(queuesdbpath).table("model_kcweb_queues").find()
            except:
                model_kcweb_tasks=model_kcweb_task()
                model_kcweb_tasks.create_table()
            Queues.__globalqueue=Queue()
            t=threading.Thread(target=Queues.__messagequeue)
            t.daemon=True
            t.start()
    def __startprocess():
        if not Queues.__processglobalqueue:
            if not os.path.isfile(queuesdbpath):
                model_kcweb_tasks=model_kcweb_task()
                model_kcweb_tasks.create_table()
            try:
                kcwsqlite.sqlite().connect(queuesdbpath).table("model_kcweb_queues").find()
            except:
                model_kcweb_tasks=model_kcweb_task()
                model_kcweb_tasks.create_table()
            Queues.__processglobalqueue=multiprocessing.Queue()
            t=multiprocessing.Process(target=Queues.messagequeueprocess,args=(Queues.__processglobalqueue,))
            t.daemon=True
            t.start()
    def messagequeueprocess(processglobalqueue):
        """不支持外部调用"""
        kcwsqlite.sqlite().connect(queuesdbpath).table("model_kcweb_queues").where("code=2 and updtime<"+str(int(time.time())-86400*7)).delete()
        kcwsqlite.sqlite().connect(queuesdbpath).table("model_kcweb_queues").where("code=3 and updtime<"+str(int(time.time())-1200)).delete()
        while True:
            if not processglobalqueue.empty():
                value=processglobalqueue.get()
                kcwsqlite.sqlite().connect(queuesdbpath).table("model_kcweb_queues").where("taskid = '"+value['task']['taskid']+"' and code!=4").update({"code":3,"error":""})
                if value['args']:
                    try:
                        value['target'](*value['args'])
                    except:
                        kcwsqlite.sqlite().connect(queuesdbpath).table("model_kcweb_queues").where("taskid = '"+value['task']['taskid']+"' and code!=4").update({"code":1,'endtime':int(time.time()),'updtime':int(time.time()),"error":str(traceback.format_exc())})
                    else:
                        kcwsqlite.sqlite().connect(queuesdbpath).table("model_kcweb_queues").where("taskid = '"+value['task']['taskid']+"' and code!=4").update({"code":4,"start":100,'endtime':int(time.time()),'updtime':int(time.time())})
                else:
                    try:
                        value['target']()
                    except:
                        kcwsqlite.sqlite().connect(queuesdbpath).table("model_kcweb_queues").where("taskid = '"+value['task']['taskid']+"' and code!=4").update({"code":1,'endtime':int(time.time()),'updtime':int(time.time()),"error":str(traceback.format_exc())})
                    else:
                        kcwsqlite.sqlite().connect(queuesdbpath).table("model_kcweb_queues").where("taskid = '"+value['task']['taskid']+"' and code!=4").update({"code":4,"start":100,'endtime':int(time.time()),'updtime':int(time.time())})
            else:
                time.sleep(1)
    def __messagequeue():
        # time.sleep(0.01)
        kcwsqlite.sqlite().connect(queuesdbpath).table("model_kcweb_queues").where("code=2 and updtime<"+str(int(time.time())-86400*7)).delete()
        kcwsqlite.sqlite().connect(queuesdbpath).table("model_kcweb_queues").where("code=3 and updtime<"+str(int(time.time())-1200)).delete()
        while True:
            if not Queues.__globalqueue.empty():
                value=Queues.__globalqueue.get()
                kcwsqlite.sqlite().connect(queuesdbpath).table("model_kcweb_queues").where("taskid = '"+value['task']['taskid']+"' and code!=4").update({"code":3,"error":""})
                if value['args']:
                    try:
                        value['target'](*value['args'])
                    except:
                        kcwsqlite.sqlite().connect(queuesdbpath).table("model_kcweb_queues").where("taskid = '"+value['task']['taskid']+"' and code!=4").update({"code":1,'endtime':int(time.time()),'updtime':int(time.time()),"error":str(traceback.format_exc())})
                    else:
                        kcwsqlite.sqlite().connect(queuesdbpath).table("model_kcweb_queues").where("taskid = '"+value['task']['taskid']+"' and code!=4").update({"code":4,"start":100,'endtime':int(time.time()),'updtime':int(time.time())})
                else:
                    try:
                        value['target']()
                    except:
                        kcwsqlite.sqlite().connect(queuesdbpath).table("model_kcweb_queues").where("taskid = '"+value['task']['taskid']+"' and code!=4").update({"code":1,'endtime':int(time.time()),'updtime':int(time.time()),"error":str(traceback.format_exc())})
                    else:
                        kcwsqlite.sqlite().connect(queuesdbpath).table("model_kcweb_queues").where("taskid = '"+value['task']['taskid']+"' and code!=4").update({"code":4,"start":100,'endtime':int(time.time()),'updtime':int(time.time())})
            else:
                time.sleep(1)
    def delhist():
        """清除任务历史记录(包括 成功的 失败的 已完成的)"""
        return kcwsqlite.sqlite().connect(queuesdbpath).table("model_kcweb_queues").where("code","in",0,1,4).delete()
    def delwhere(where):
        "通过where条件删除 (不推荐使用)"
        return kcwsqlite.sqlite().connect(queuesdbpath).table("model_kcweb_queues").where(where).delete()
    def setfield(taskid,key,value):
        """设置指定字段(不建议使用)"""
        try:
            return kcwsqlite.sqlite().connect(queuesdbpath).table("model_kcweb_queues").where("taskid",taskid).update({key:value})
        except:
            return False
    def setstart(taskid,start=0.001,describes=None):
        """增加进度条起始位置
        
        start 支持0.001到10
        """
        if start>=0.001 and start<=10:
            arr=kcwsqlite.sqlite().connect(queuesdbpath).table("model_kcweb_queues").where("taskid",taskid).find()
            if arr:
                start+=round(float(arr['start']),3)
                if start>=0.01 and start <=99.99:
                    dqsjc=int(time.time())-arr['updtime'] #当前时间差
                    if dqsjc>=1:
                        starts=round(float((float(start)-float(arr['start']))/dqsjc),3)
                        upddate={"start":start,'starts':starts,'updtime':int(time.time())}
                        if describes:
                            upddate['describes']=describes
                        kcwsqlite.sqlite().connect(queuesdbpath).table("model_kcweb_queues").where("taskid",taskid).update(upddate)
                    return True
                else:
                    return False
            else:
                return False
        else:
            False
    def insert(target,args=None,title="默认任务",describes='',msg='',taskid=None,start=0,updtime=0,types=''): #add_queue
        """添加队列
        
        target 方法名  必须

        args 方法参数 非必须  如 (参数1,参数2)

        title 任务名称

        describes 任务描述

        msg 状态描述

        taskid 任务id

        start 进度条开始位置 （建议1到50）

        updtime 进度条更新时间

        types process表示使用进程执行 否则使用线程执行

        return taskid
        """
        if types=='process':
            Queues.__startprocess()
        else:
            Queues.__start()
        ttt=int(time.time())
        if not taskid:
            m = hashlib.md5()
            m.update((str(ttt)+str(random.randint(100000,999999))).encode(encoding='utf-8'))
            taskid=m.hexdigest()
        end=100
        if not updtime:
            updtime=ttt
        task={"taskid":taskid,"title":title,"describes":describes,"code":2,"msg":msg,"error":"","start":start,"end":end,"addtime":ttt,'starts':0,'endtime':0,'updtime':updtime}
        key={"target":target,"args":args,"task":task}
        kcwsqlite.sqlite().connect(queuesdbpath).table("model_kcweb_queues").insert(task)
        if types=='process':
            Queues.__processglobalqueue.put(key)
        else:
            Queues.__globalqueue.put(key)
        return taskid
    def getall(pagenow=1,pagesize=20,where=None):
        """获取全部队列

        code 1获取失败的任务   2获取等待中的任务   3获取正在执行中的任务  4获取执行完成的任务

        return list
        """
        if not os.path.isfile(queuesdbpath):
            model_kcweb_tasks=model_kcweb_task()
            model_kcweb_tasks.create_table()
        try:
            lists=kcwsqlite.sqlite().connect(queuesdbpath).where(where).table("model_kcweb_queues").order("id desc").page(pagenow,pagesize).select()
            count=kcwsqlite.sqlite().connect(queuesdbpath).where(where).table("model_kcweb_queues").count()
            return lists,count
        except:
            model_kcweb_tasks=model_kcweb_task()
            model_kcweb_tasks.create_table()
            return [],0
    def status(taskid):
        """获取任务状态
        
        taskid  任务id

        return dict
        """
        arr=kcwsqlite.sqlite().connect(queuesdbpath).table("model_kcweb_queues").where("taskid",taskid).find()
        if arr:
            arr['start']=float(arr['start'])
            dqsjc=arr['updtime']-arr['addtime']
            if dqsjc and arr['start']>=1:
                arr['starts']=round(float(arr['start'])/dqsjc,3)
            else:
                try:
                    arr['starts']=round(float(arr['starts']),3)
                except:
                    arr['starts']=0
        return arr
    def iscomplete():
        """判断对列中的任务是否全部执行完成
        
        return Boolean
        """
        if kcwsqlite.sqlite().connect(queuesdbpath).table("model_kcweb_queues").where("code","in",2,3).count():
            return True
        else:
            return False
