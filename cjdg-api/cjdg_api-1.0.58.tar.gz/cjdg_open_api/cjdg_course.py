import requests
from .base import base


class cjdgCourse(base):
    '''
    Cjdg课程接口使用：
    1.6.	培训课程添加	7
    1.7.	获取课程分类	8
    '''

    def __init__(self, token, app_secret=None):
        super().__init__(token, app_secret)

    def addcourse(self, name, materialId, img="https://xxy-1258031202.picsh.myqcloud.com/eda1c4c2-56a0-4ded-8603-f7a52cf51863.png"):
        '''
        1.6.	培训课程添加
        1.6.1.	说明
        Http请求方式： post
        URL: /api/course/add
        Description :  添加课程
        1.6.2.	  参数说明

        参数名	必选	类型	功能描述	备注
        accessToken	True	String	访问token，从token接口取得。	
        cate	True	Integer	课程分类	
        name	True	String	课程名称	
        intro	False	String	导语	
        desc	False	String	描述	
        materialId	True	Integer	素材ID	
        type	True	Integer	课程类型 0:视频,1:图文,2:页面资源	
        ability	False	Integer	能力类型 0—基本能力（默认）1—陈列能力 2--销售能力 3—商品能力	

        1.6.3.	返回值
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
        url = "course/add"
        data = {
            "cate": 41257,
            "name": name,
            "materialId": materialId,
            "type": 1,
            "img": img,
        }
        result = self.request(url, data, method="GET")
        code = result.get("code")
        if code:
            code = int(code)
            if code == 102:
                return result.get("dataObject").get("courseId")

    def getCourseType(self):
        '''
        1.7.	获取课程分类
        1.7.1.	说明
        Http请求方式： post
        URL: /api/course/type
        Description : 获取课程分类，应用到课程时level为3
        1.7.2.	  参数说明

        参数名	必选	类型	功能描述	备注
        accessToken	True	String	访问token，从token接口取得。	
        name	false	String	名称模糊搜索	
        level	false	Integer	层级1、2、3（叶子节点）	
        page	false	Integer	默认1	
        rows	false	Integer	默认15	
        parent	false	Integer	父节点ID	

        1.7.3.	返回值
        {
            "code": 102,
            "dataArray": [],
            "dataObject":

            "dataType": 101,
            "status": 0,
            "userStatus": 0

        }
        返回值字段 	字段类型 	字段说明 
        code	String 	返回状态编码,详情见状态描述
        dataArray	String	暂无作用
        dataType	string 	对象类型码101 对象  102 数组
        dataObject	String	分类信息列表，课程分类字段courseTypeId。如果错误会返回错误信息
        '''
        url = "course/type"
        data = {
            "name": "",
            "level": "",
            "page": "",
            "rows": "",
            "parent": "",
        }
        result = self.request(url, data, method="POST")
        code = result.get("code")
        if code:
            code = int(code)
            if code == 102:
                return result.get("dataObject")

    def delete(self, course_id):
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Length": "17",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": f"JSESSIONID=1006E2056DB2849B3D821848FEEF12DC; Hm_lvt_5e3170920dadcb2f29dfb66f63b9b6aa=1574042672; accessToken={self.token}",
            "Host": "bms.chaojidaogou.com",
            "Pragma": "no-cache",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
        }
        url = "http://bms.chaojidaogou.com/shopguide/coursedelCourse.jhtml"
        data = {
            "courseId_cf": course_id,
        }
        response = requests.post(url, data=data, headers=headers)
        if response.status_code == 200:
            result = response.json()
            return (result)
