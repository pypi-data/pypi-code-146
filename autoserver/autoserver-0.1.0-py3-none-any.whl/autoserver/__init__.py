import fastapi.responses
from fastapi import FastAPI
import uvicorn
import jinja2
import pathlib
import inspect
import collections
import pydantic
import docstring_parser

class TemplateBase():
    jinjaPath = pathlib.Path(__file__).resolve().parent / 'resources/'
    jinjaEnv = jinja2.Environment(loader=jinja2.FileSystemLoader(jinjaPath))
    homepage = jinjaEnv.get_template("homepage.html.jinja2")
    frontfunc = jinjaEnv.get_template("frontfunc.html.jinja2")

class funcData(TemplateBase):
    formDatum = collections.namedtuple("formDatum", "varName varType")
    def __init__(self, newfunc):
        self.fn = newfunc
        docdata = docstring_parser.parse(newfunc.__doc__)
        self.name = newfunc.__name__
        self.desc = docdata.short_description
        self.paramDesc = {param.arg_name: param.description for param in docdata.params }
        self.typeDict = self.inputTypeDict(newfunc)
        self.frontEndPoint = f"/front/{newfunc.__name__}"
        self.backEndPoint = f"/back/{newfunc.__name__}"
        self.model = self.createModel(newfunc)

    @classmethod
    def inputTypeDict(cls, newfunc):
        argData = inspect.getfullargspec(newfunc)
        argList = argData.args
        typeDict = argData.annotations
        return {argVal: typeDict.get(argVal, str) for argVal in argList}

    def createFrontEnd(self, fnObjList):
        formData = [self.formDatum(argVal, self.typeDict[argVal].__name__) for argVal in self.typeDict]
        return self.frontfunc.render(fnList = fnObjList,
                                     fnObj = self,
                                     formRows=formData)

    @classmethod
    def createModel(cls, newfunc):
        typeDict = cls.inputTypeDict(newfunc)
        modelTypeDict = {varName: (typeDict[varName], ...) for varName in typeDict}
        return pydantic.create_model(f"{newfunc.__name__}_model", **modelTypeDict)





class AutoServer(TemplateBase):
    def __init__(self):
        self.app = FastAPI()
        self.funcDataList = []

    def addfunc(self, newfunc):
        fData = funcData(newfunc)
        self.funcDataList.append(fData)

        #webpage = fData.createFrontEnd(self.funcDataList)
        @self.app.get(fData.frontEndPoint, response_class=fastapi.responses.HTMLResponse)
        def show_page():
            return fData.createFrontEnd(self.funcDataList)

        @self.app.post(fData.backEndPoint)
        def back_endpoint(inputData: fData.model):
            return newfunc(**inputData.__dict__)

        return newfunc

    def run(self):
        @self.app.get("/",response_class=fastapi.responses.HTMLResponse)
        def homepage():
            return self.homepage.render(fnList=self.funcDataList)

        uvicorn.run(self.app,
                    host="127.0.0.1",
                    port=8000,
                    log_level="debug")
