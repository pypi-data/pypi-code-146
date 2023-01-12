# -*- coding: utf-8 -*-
import re, types
from PyQt5.QtWidgets import QApplication
from qasync import QEventLoop
import sys, asyncio, os
from jinja2 import FileSystemLoader, Environment
from pyquery import PyQuery as pq
from mvvmQt.Attributes import Attribute
from mvvmQt.Events import Event
from mvvmQt.Elements import Element
from mvvmQt.attrConfig import ElementAttr
from mvvmQt.alignConfig import ElementAlign
from mvvmQt.Observable import Computed

class Parser:
    ElementAttrConfig = ElementAttr
    ElementAlignConfig = ElementAlign
    ElementObj = Element
    AttributeObj = Attribute
    EventObj = Event

    def __init__(self, src, tempDir='templates', indexName='index', obj={}, models=None, events=None):
        self.env = Environment(loader=FileSystemLoader(searchpath=os.path.join(src, tempDir), encoding='utf-8'))
        self.obj = obj
        self.indexName = indexName
        self.elements = [] #元素列表
        self.btnGroups = {} #按键组
        self.models = models
        self.events = events

    def create_loop(self):
        self.loop = QEventLoop(self.app)
        asyncio.set_event_loop(self.loop)

    def build(self):
        self.app = QApplication(sys.argv)
        self.create_loop()

        self.obj['desktop'] = QApplication.desktop()
        t = self.env.get_template("%s.jinja2" % self.indexName)
        html = t.render(**self.obj)
        doc = pq(html)
        self.createElements(doc)
        self.idElements = {}
        for e in self.elements:
            e.make()
            if 'id' in e.attrsToDict.keys():
                self.idElements[e.attrsToDict['id']] = e

    def reloadEvent(self, id, name, func):
        obj = self.idElements[id]
        setattr(obj.qt, name, types.MethodType(func(), getattr(obj, 'qt')))

    # Event Example
    # def mainCloseEvent(self):
    #     main = self
    #     def _event(self, event):
    #         result = QMessageBox.question(self, "操作询问", "是否关闭程序?", QMessageBox.Yes | QMessageBox.No)
    #         if(result == QMessageBox.Yes):
    #             main.events.box.close()
    #             event.accept()
    #         else:
    #             event.ignore()
    #     return _event

    def run(self):
        with self.loop:
            self.loop.run_forever()

    def createElements(self, doc):
        list(map(self.loopChild, doc.children()))

    def tagName(self, dom):
        s = str(dom).strip()
        c = re.compile(r'\<(.*?)\>')
        return c.findall(s)[0].split(' ')[0]

    def not_value(self, v):
        return not v[0]

    def loopChild(self, e, parent=None):
        dom = pq(e)
        tagName = self.tagName(dom)
        #检查是否为属性设置
        if tagName.startswith('attr'):
            ob_value = dom.attr('ob')
            is_not = False
            is_two_way = False
            if ob_value:
                if '@' in ob_value:
                    ob_value = ob_value.replace('@', '')
                    is_two_way = True
                if ob_value.startswith('!'):
                    is_not = True
                    ob_value = ob_value.replace('!', '')
                arr_index = re.findall(r'.*\[(\d+)\]', ob_value)
                if len(arr_index) > 0:
                    value = getattr(self.models, ob_value.replace("[%s]" % arr_index[0], ''))[int(arr_index[0])]
                else:
                    value = getattr(self.models, ob_value)
                if is_not:
                    value = Computed([value], self.not_value)
            else:
                value = dom.attr('v')
            return self.AttributeObj(tagName.replace('attr-', ''), value, dom, is_two_way)
        
        if tagName.startswith('event'):
            name = dom.attr('v')
            param = dom.attr('param')
            f = getattr(self.events, name)
            return self.EventObj(tagName.replace('event-', ''), param, f)

        e = self.ElementObj(self, parent, tagName, dom)
        l = list(map(lambda c: self.loopChild(c, e), dom.children()))
        attrs = []
        events = []
        childs = []
        for c in l:
            if type(c) is self.AttributeObj:
                attrs.append(c)
            elif type(c) is self.EventObj:
                events.append(c)
            elif type(c) is self.ElementObj:
                childs.append(c)
                if c.isVitrual:
                    childs.extend(c.childs)

        e.childs = childs
        e.attrs = attrs
        e.events = events
        self.elements.append(e)
        return e

if __name__ == "__main__":
    p = Parser('./')
    p.parser()