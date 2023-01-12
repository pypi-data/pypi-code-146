# -*- coding: utf-8 -*-
from mvvmQt.rewriteContorls import Widget, Window, Label
from PyQt5.QtWidgets import QWidget, QFrame, QPushButton, QGridLayout, QLayout, QHBoxLayout, QVBoxLayout, QLabel, QTabWidget\
    , QStatusBar, QButtonGroup, QAbstractButton, QRadioButton, QComboBox
from mvvmQt.Observable import ObservableBase
import asyncio

class RowOrCol:
    def __init__(self, e):
        self.e = e

    @property
    def offset(self):
        return int(self.e.attrsToDict.get('offset', 0))

    @property
    def span(self):
        return int(self.e.attrsToDict.get('span', 0))

class Row(RowOrCol):
    def __init__(self, e):
        super().__init__(e)

class Col(RowOrCol):
    def __init__(self, e):
        super().__init__(e)

class Element:
    def __init__(self, parser, parent, name, dom):
        self.topWidget = ['widget', 'window']
        self.parser = parser
        self.name = name.lower()
        self.parent = parent
        self.qt = None
        self.isVitrual = False #如果为虚拟元素，则会将其子元素加到上级元素的子元素列表中
        self.dom = dom
        self.childs = []
        self.attrs = []
        self.events = []

        self.useFunc = {
            'window': [self.createWindow, self.bindAll],
            'widget': [self.createWidget, self.bindAll],
            'frame': [self.createFrame, self.afterCreateFrame],
            'row': [self.createRow, None],
            'col': [self.createCol, None],
            'grid': [self.createGridLayout, self.afterCreateGridLayout],
            'hbox': [self.createBox, self.afterCreateBox],
            'vbox': [self.createBox, self.afterCreateBox],
            'button-group': [self.createButtonGroup, self.afterCreateButtonGroup],
            'button': [self.createButton, self.bindAll],
            'radio': [self.createRadio, self.bindAll],
            'label': [self.createLabel, self.bindAll],
            'tab': [self.createTab, self.afterCreateTab],
            'select': [self.createCombo, self.afterCreateCombo],
            'option': [self.createOption, None],
            'status': [self.createStatusBar, self.bindAll]
        }

        self.create()

    def create(self):
        self.useFunc[self.name][0]()

    def make(self):
        if self.useFunc[self.name][1]:
            self.useFunc[self.name][1]()

    @property
    def attrsToDict(self):
        d = {}
        for attr in self.attrs:
            d.update(attr.toDict())
        return d

    def changeValue(self, c, v):
        if c is None:
            return v
        if type(c) is list:
            if type(v) is not c[-1]:
                for _ in c:
                    v = _(v)
        else:
            v = c(v)
        return v

    def useQtFunc(self, f, params, ob=None):
        if type(params) is not list:
            params = [params]
        if type(f) is str:
            #字符串则代表使用qt内置函数
            f = getattr(self.qt, f)
        else:
            #非字符串则表示使用自定义函数
            params.extend([self, ob])

        f(*params)

    def addSubscribe(self, ob, c):
        if type(c[1]) is str:
            ob.subscribe(lambda v: self.useQtFunc(c[0], c[1] % v, ob), init=True)
        else:
            ob.subscribe(lambda v: self.useQtFunc(c[0], self.changeValue(c[1], v), ob), init=True)

    def callFunc(self, f, params):
        if asyncio.iscoroutinefunction(f):
            asyncio.get_event_loop().create_task(f(*params))
        else:
            f(*params)

    def addEvent(self, e):
        event = getattr(self.qt, e.key)
        if e.param:
            event[str if e.param == 'str' else int].connect(lambda v: self.callFunc(e.func, [v, self]))
        else:
            event.connect(lambda: self.callFunc(e.func, [self]))

    def bindAttr(self):
        for attr in self.attrs:
            k = attr.key
            v = attr.value or ''
            if k not in self.parser.ElementAttrConfig[self.name].keys():
                continue
            _ = [*self.parser.ElementAttrConfig[self.name][k]]
            if isinstance(v, ObservableBase):
                if attr.dom.attr('format'):
                    #属性中包含format，则展现值是经过format处理的
                    _[1] = attr.dom.attr('format')
                self.addSubscribe(v, _)
            else:
                self.useQtFunc(_[0], self.changeValue(_[1], v))

    def bindEvent(self):
        for e in self.events:
            self.addEvent(e)

    def bindAll(self):
        self.bindAttr()
        self.bindEvent()

    def findParentWidget(self):
        o = self
        while 1:
            if type(o.parent.qt) in [Widget, Window]:
                return o.parent.qt
            o = o.parent

    def createWindow(self):
        self.qt = Window()

    def createWidget(self):
        self.qt = Widget()

    def createFrame(self):
        self.qt = QFrame(self.parent.qt if self.parent.name in self.topWidget else None)

    def afterCreateFrame(self):
        self.bindAttr()

        for c in self.childs:
            if isinstance(c.qt, QLayout):
                self.qt.setLayout(c.qt)

    def createRow(self):
        self.qt = Row(self)

    def createCol(self):
        self.qt = Col(self)

    def createGridLayout(self):
        self.qt = QGridLayout()

    def afterCreateGridLayout(self):
        self.bindAttr()
        es = []
        row_num = 0
        for row in filter(lambda c: type(c.qt) is Row, self.childs):
            row = row.qt
            col_num = 0
            cols = list(filter(lambda c: type(c.qt) is Col, row.e.childs))
            if len(cols) == 0:
                continue
            row_num += row.offset
            row_span_add = 0
            for col in cols:
                col = col.qt
                if len(col.e.childs) == 0:
                    continue
                col_num += col.offset
                if row.span > 0 or col.span > 0:
                    rowSpan = row.span or 1
                    colSpan = col.span or 1
                    row_span_add += rowSpan - 1
                    es.append([col.e.childs[0].qt, row_num, col_num, rowSpan, colSpan])
                    col_num += colSpan - 1
                else:
                    es.append([col.e.childs[0].qt, row_num, col_num])
                col_num += 1
            row_num += 1
            row_num += row_span_add

        for e in es:
            if isinstance(e[0], QLayout):
                self.qt.addLayout(*e)
            elif isinstance(e[0], QWidget):
                self.qt.addWidget(*e)

        if self.parent and self.parent.name in self.topWidget:
            self.parent.qt.setLayout(self.qt)

    def createBox(self):
        if self.name == 'hbox':
            self.qt = QHBoxLayout()
        else:
            self.qt = QVBoxLayout()

    def afterCreateBox(self):
        for c in self.childs:
            params = [c.qt]
            if 'stretch' in c.attrsToDict.keys():
                params.append(int(c.attrsToDict['stretch']))
            if isinstance(c.qt, QLayout):
                self.qt.addLayout(*params)
            elif isinstance(c.qt, QWidget):
                if 'align' in c.attrsToDict.keys():
                    params.append(self.parser.ElementAlignConfig[c.attrsToDict['align']])
                self.qt.addWidget(*params)
        if 'spacing' in self.attrsToDict.keys():
            self.qt.addSpacing(int(self.attrsToDict['spacing']))

        if self.parent and self.parent.name in self.topWidget:
            self.parent.qt.setLayout(self.qt)

    def createButtonGroup(self):
        self.qt = QButtonGroup()
        self.isVitrual = True

    def afterCreateButtonGroup(self):
        #循环所有后代元素，gid相同时则添加到组内
        childs = self.childs
        store = []
        while 1:
            store.extend(list(filter(lambda c: len(c.childs) == 0, childs)))
            l = list(filter(lambda c: len(c.childs) > 0, childs))
            childs = []
            for c in l:
                childs.extend(c.childs)
            if len(childs) == 0:
                break
        id = 1
        for c in store:
            if isinstance(c.qt, QAbstractButton) and 'gid' in c.attrsToDict.keys() and c.attrsToDict['gid'] == self.attrsToDict['gid']:
                self.qt.addButton(c.qt, id)
                id += 1
        self.bindAll()

    def createButton(self):
        self.qt = QPushButton(self.dom.text())

    def createRadio(self):
        self.qt = QRadioButton(self.dom.text())

    def createLabel(self):
        self.qt = Label(self.dom.text())

    def createTab(self):
        self.qt = QTabWidget()

    def afterCreateTab(self):
        tab_index = 0
        for c in self.childs:
            if c.name in self.topWidget:
                self.qt.addTab(c.qt, 'Tab %d' % tab_index)
                tab_index += 1
        self.bindAll()

    def createCombo(self):
        self.qt = QComboBox()

    def afterCreateCombo(self):
        items = [c.qt for c in self.childs]
        self.qt.addItems(items)

        if 'index' in self.attrsToDict.keys() and isinstance(self.attrsToDict['index'], ObservableBase):
            self.qt.currentIndexChanged[int].connect(lambda v: self.attrsToDict['index'].setValue(v))
        self.bindAll()

    def createOption(self):
        self.qt = self.dom.text()
        self.isVitrual = True

    def createStatusBar(self):
        self.qt = QStatusBar()