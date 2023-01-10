import requests
from .base import base


class cjdgMaterial(base):
    '''
    Cjdg素材接口：
    素材的增加参考/api/sync/addmaterial接口
    素材的查询参考/api/material/findMaterialListByType接口
    '''

    def __init__(self, token, app_secret=None):
        super().__init__(token, app_secret)

    def add(self, title, source):
        '''
        1.1.	素材添加
        1.1.1.	说明
        Http请求方式： post
        URL: /api/sync/addmaterial
        Description :  添加素材
        1.1.2.	  参数说明
        '''
        url = "sync/addmaterial"
        data = {
            "title": title,
            "source": source,
            "sourceType": "text",
            "sourceCode":  1,

        }
        result = self.request(url, data, method="POST")
        code = result.get("code")
        if code:
            code = int(code)
            if code == 102:
                return result.get("dataObject")

    def get(self):
        '''
        1.1.	素材添加
        1.1.1.	说明
        Http请求方式： post
        URL: /api/sync/addmaterial
        Description :  添加素材
        1.1.2.	  参数说明
        '''
        url = "material/findMaterialListByType"
        data = {
            "title": "任秋锴创建的素材1",
            "source": "<h1>任秋锴是无敌的！",
            "sourceCode": "text",
            # sourceCode:  text/video
        }
        result = self.request(url, data, method="POST")
        code = result.get("code")
        if code:
            code = int(code)
            if code == 102:
                return result

    def edit(self, material_id, title, source):
        url = "sync/addmaterial"
        data = {
            "id": material_id,
            "title": title,
            "source": source,
            "sourceType": "text",
            "sourceCode":  1,

        }
        result = self.request(url, data, method="POST")
        code = result.get("code")
        if code:
            code = int(code)
            if code == 102:
                return result.get("dataObject")

    def delete(self, material_id, material_type="imgText"):
        '''
        素材的删除  /api/material/del/$1/$2  $1有  video imgText  pageResources  三个选项  $2 为素材id
        '''
        url = f"material/del/{material_type}/{material_id}"
        result = self.request(url, data={}, method="GET")
        code = result.get("code")
        if code:
            code = int(code)
            if code == 102:
                return result


def testcase1():
    # 1，新增素材是否有问题。
    token = "a9211faef3c16f25eabecf81ab1c538a_deppon"
    c = cjdgMaterial(token=token)
    data = {
        "title": "14741_1",
        "source": '<div class="inputbody"><p><span style="font-size: 18px;"><strong>【床垫开单规范】</strong></span><br></p><p><br><span style="font-size: 18px;"></span></p><p>1）<span style="color: rgb(255, 0, 0);"><strong>宽≤1.5m、无需安装</strong></span>的床垫（三边和不限，30kg＜重量≤60kg）</p><p>操作：开单时可开<span style="color: rgb(255, 0, 0);"><strong>360特重件</strong></span>，<span style="color: rgb(255, 0, 0);"><strong>超长费每张最低收30元</strong></span>，开单时<span style="color: rgb(255, 0, 0);"><strong>超长费标签仅能选“床垫1.5m非安装”</strong></span>。</p><p>2）宽＞1.5m的床垫，且三边和＞3.5m</p><p>操作：按照<span style="color: rgb(255, 0, 0);"><strong>家具送装平台开单</strong></span>，并按照家具送装要求收取费用，<span style="color: rgb(255, 0, 0);"><strong>不允许开大件快递，违规开单可上报拒收品差错</strong></span>。</p><p><br></p><p>如有疑问，可联系赵苗-家具床垫产品组</p></div>',
    }
    print(c.add(**data))


def testcase2():
    # 2，当ID一样时素材是否可以进行更新。
    # 缺少编辑素材的接口。
    pass


def testcase3():
    # 删除素材
    token = "a9211faef3c16f25eabecf81ab1c538a_deppon"
    c = cjdgMaterial(token=token)
    print(c.delete(1162794))


def testcase4():
    # 编辑素材
    token = "a9211faef3c16f25eabecf81ab1c538a_deppon"
    c = cjdgMaterial(token=token)
    print(c.edit("1121772", "任秋锴20191218测试修改后", "<h2>超级导购天下无敌</h2>"))


if __name__ == "__main__":
    # testcase1()
    # testcase2()
    # testcase3()
    testcase4()
