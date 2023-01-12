import requests
from .base import base


class cjdgEmba(base):
    '''
    Cjdg商学院接口使用：
    1.1.	书本添加	addBook
    1.2.	单元添加	addSection
    1.3.	单元章节	addChapter
    1.4.	章节课程添加	addLesson
    1.5.	获取商学院相关信息	get
    '''

    def __init__(self, token, app_secret=None):
        super().__init__(token, app_secret)

    def addBook(self, name, moduleId=16193, order=1, img="https://xxy-1258031202.picsh.myqcloud.com/eda1c4c2-56a0-4ded-8603-f7a52cf51863.png"):
        '''
        1.1.	书本添加
        1.1.1.	说明
        Http请求方式： post
        URL: /api/emba/addBook
        Description :  添加书本，名称不能重复
        1.1.2.	  参数说明

        参数名	必选	类型	功能描述	备注
        accessToken	True	String	访问token，从token接口取得。	
        name	True	String	书本名称	
        comment	False	String	书本描述	
        img	False	String	书本封面，尽量不要为空	
        owner	False	Integer	指定书本拥有者	
        moduleId	False	Integer	指定书本关联的模块	


        1.1.3.	返回值
        {
            "code": 102,
            "dataArray": [],
            "dataObject":{"id":111, "name":"测试书本"}，
            "dataType": 101,
            "status": 0,
            "userStatus": 0

        }
        返回值字段 	字段类型 	字段说明 
        code	String 	返回状态编码,详情见状态描述
        dataArray	String	暂无作用
        dataType	string 	对象类型码101 对象  102 数组
        dataObject	String	返回新增书本的信息，id为新增书本的id如果错误会返回错误信息
        '''
        url = "emba/addBook"
        data = {
            "name": name,
            "comment": "从接口写的",
            "img": img,
            # "owner": "",
            "moduleId": moduleId,
            "order": order,
        }
        result = self.request(url, data, method="GET")
        code = result.get("code")
        if code:
            code = int(code)
            if code == 102:
                return result.get("dataObject").get("id")

    def deleteBook(self, ebid):
        headers = {
            "Host": "bms.chaojidaogou.com",
            "Connection": "keep-alive",
            "Content-Length": "90",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "Origin": "http://bms.chaojidaogou.com",
            "Upgrade-Insecure-Requests": "1",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Referer": "http://bms.chaojidaogou.com/shopguide/book_view.jhtml?topId=140&requestSource=h5",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
            "Cookie": f"JSESSIONID=9AC8A3799D296A8712AE18B059D5B694; Hm_lvt_5e3170920dadcb2f29dfb66f63b9b6aa=1574042672; accessToken={self.token}",
        }
        url = "http://bms.chaojidaogou.com/shopguide/bookdelBook.jhtml?level=0"
        data = {
            "EB.id": ebid
        }
        response = requests.post(url, data=data, headers=headers)
        if response.status_code == 200:
            result = response.json()
            return (result)

    def addSection(self, name, bookId):
        '''
        1.2.	单元添加
        1.2.1.	说明
        Http请求方式： post
        URL: /api/emba/addSection
        Description :  添加书本单元,只能操作本企业的书本，且名称不能重复
        1.2.2.	  参数说明

        参数名	必选	类型	功能描述	备注
        accessToken	True	String	访问token，从token接口取得。	
        name	True	String	单元名称	
        bookId	True	Integer	书本ID	

        1.2.3.	返回值
        {
            "code": 102,
            "dataArray": [],
            "dataObject":{"id":1, "name":"测试单元"，"book_id":111}，

            "dataType": 101,
            "status": 0,
            "userStatus": 0

        }
        返回值字段 	字段类型 	字段说明 
        code	String 	返回状态编码,详情见状态描述
        dataArray	String	暂无作用
        dataType	string 	对象类型码101 对象  102 数组
        dataObject	String	新增单元的信息。如果错误会返回错误信息
        '''
        url = "emba/addSection"
        data = {
            "name": name,
            "bookId": bookId,
        }
        result = self.request(url, data, method="GET")
        code = result.get("code")
        if code:
            code = int(code)
            if code == 102:
                return result.get("dataObject").get("id")

    def addChapter(self, name, sectionId):
        '''
        1.3.	单元章节
        1.3.1.	说明
        Http请求方式： post
        URL: /api/emba/addChapter
        Description :  添加书本章节,只能操作本企业的书本，且名称不能重复
        1.3.2.	  参数说明

        参数名	必选	类型	功能描述	备注
        accessToken	True	String	访问token，从token接口取得。	
        name	True	String	章节名称	
        sectionId	True	Integer	单元ID	

        1.3.3.	返回值
        {
            "code": 102,
            "dataArray": [],
            "dataObject":{"id":1, "name":"测试单元"，"book_id":111，"section_id":222}，

            "dataType": 101,
            "status": 0,
            "userStatus": 0

        }
        返回值字段 	字段类型 	字段说明 
        code	String 	返回状态编码,详情见状态描述
        dataArray	String	暂无作用
        dataType	string 	对象类型码101 对象  102 数组
        dataObject	String	新增章节的信息。如果错误会返回错误信息
        '''
        url = "emba/addChapter"
        data = {
            "name": name,
            "sectionId": sectionId,
        }
        result = self.request(url, data, method="GET")
        code = result.get("code")
        if code:
            code = int(code)
            if code == 102:
                return result.get("dataObject").get("id")

    def addLesson(self, chapterId, courseId):
        '''
        1.4.	章节课程添加
        1.4.1.	说明
        Http请求方式： post
        URL: /api/emba/addLesson
        Description :  添加书本章节课程,只能操作本企业的书本，且名称不能重复
        1.4.2.	  参数说明

        参数名	必选	类型	功能描述	备注
        accessToken	True	String	访问token，从token接口取得。	
        chapterId	True	Integer	章节的ID	
        courseId	True	Integer	单元ID	

        1.4.3.	返回值
        {
            "code": 102,
            "dataArray": [],
            "dataObject":{"id":1, "courseId":3344，"book_id":111，"chapter_id":222}，

            "dataType": 101,
            "status": 0,
            "userStatus": 0

        }
        返回值字段 	字段类型 	字段说明 
        code	String 	返回状态编码,详情见状态描述
        dataArray	String	暂无作用
        dataType	string 	对象类型码101 对象  102 数组
        dataObject	String	新增课程的信息。如果错误会返回错误信息
        '''
        url = "emba/addLesson"
        data = {
            "chapterId": chapterId,
            "courseId": courseId,
        }
        # print(data)
        result = self.request(url, data, method="GET")
        # print(result)
        code = result.get("code")
        if code:
            code = int(code)
            if code == 102:
                return result.get("dataObject").get("id")

    def get(self):
        '''
        1.5.	获取商学院相关信息
        1.5.1.	说明
        Http请求方式： get
        URL: /api/emba/list
        Description :  根据名称获取不同层级的信息，层级书本 1、单元 2、章节 3  ，根据不同的层级返回对应的数据列表

        1.5.2.	  参数说明
        参数名	必选	类型	功能描述
        accessToken	True	String	访问token，从token接口取得。
        name	false	String	名称模糊搜索
        level	True	Integer	层级书本 1、单元 2、章节 3
        page	false	Integer	默认1
        rows	false	Integer	默认15

        1.5.3.	返回值
                {
                    "code": 102,
                    "dataArray": [],
                    "dataObject":[{}]—对应的信息 
                    "dataType": 101,
                    "status": 0,
                    "userStatus": 0
                }
        返回值字段 	字段类型 	字段说明 
        code	String 	返回状态编码,详情见状态描述
        dataArray	String	暂无作用
        dataType	string 	对象类型码101 对象  102 数组
        dataObject	String	新增课程的信息。如果错误会返回错误信息
        '''
        url = "emba/list"
        data = {
            "name": "从接口写的",
            "level": "接口写入的第一本书",
            "page": 1,
            "rows": 15,
        }
        result = self.request(url, data, method="POST")
        code = result.get("code")
        if code:
            code = int(code)
            if code == 102:
                return result.get("dataObject").get("id")


def testcase():
    # 商学院层级结构复杂
    # 一次创建，不需要更新。
    # 考虑到第三部分的创建是有可能多次更新的。

    acc, pwd = "itdev_morning@deppon", "8DCH0LRtQz4vZRRh"
    c = cjdgEmba(acc=acc, pwd=pwd)
    # 创建书籍
    book_id = c.addBook("超越指标捍卫尊严")

    # 创建单元
    section_id = c.addSection(name="今日聚焦", bookId=book_id)

    # 创建章节
    chapter_id = c.addChapter(name="今日聚焦", sectionId=section_id)

    # 创建课程
    lesson_id = c.addLesson(chapter_id, 85711)


def testcase1():
    # 测试书籍的优先级。
    token = "431c9cdaccf79ff26de784dcd053e3f1_deppon"
    c = cjdgEmba(token=token)
    book_id = c.addBook("早安快递：\n20191223期超越指标捍卫尊严优先级测试_11", order="11")
    print(book_id)


def testcase2():
    # 删除书籍的优先级。
    token = "431c9cdaccf79ff26de784dcd053e3f1_deppon"
    c = cjdgEmba(token=token)
    book_id = c.deleteBook(140609)
    print(book_id)


if __name__ == "__main__":
    # testcase1()
    testcase2()
