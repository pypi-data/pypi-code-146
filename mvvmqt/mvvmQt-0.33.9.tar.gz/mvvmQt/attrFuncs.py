from mvvmQt.Elements import Element

def __updateObValue(ob, v, t):
    if t == bool:
        ob.value = bool(v - 1)
    else:
        ob.value = v

def groupChecked(*params):
    v = params[0]
    o: Element = params[-2]
    ob = params[-1]

    attr = list(filter(lambda _: _.key == 'checked', o.attrs))[0]

    if attr.twoWay and not getattr(o.qt, '_bindClicked', False):
        o.qt.buttonClicked[int].connect(lambda id: __updateObValue(ob, id, type(v)))
        o.qt._bindClicked = True

    o.qt.buttons()[int(v)].setChecked(True)