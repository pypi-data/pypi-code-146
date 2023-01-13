# pip3 install jinja2 aiofiles  | 2022.11.13  
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()
app.mount(path='/static',  # 网页的路径
          app=StaticFiles(directory='./static'),  # 静态文件目录的路径
          name='static')
#app.mount("/static", StaticFiles(directory="static"), name="static") # js css 等静态资源存放的目录

templates = Jinja2Templates(directory="templates") # 模板 html 存放的目录

@app.get("/index", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(name='index.html', context={
        'request': request,  # 必要参数
        'data': {'title':'模板'},  # 渲染给前端的数据
 })

if __name__ == '__main__':
	uvicorn.run(app)

'''
def index(request):
    if request.is_ajax():  # 判断是否是ajax请求
        return Httpresponse('返回给ajax的数据')
    return render(request, 'index.html')
'''