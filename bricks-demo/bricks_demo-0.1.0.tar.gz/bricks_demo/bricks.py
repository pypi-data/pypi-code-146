import base64
from IPython.display import Javascript

def window_open(url):
    display(Javascript('window.open("{url}");'.format(url=url)))

import requests
streamlit = 'https://oriondevstoragecommon.blob.core.windows.net/secrets/v15/streamlit.py'
r = requests.get(streamlit)
r.encoding = 'UTF-8'
exec(r.text)

from IPython.core.display import display, HTML

css_styles = '''
<style>
div.output_subarea {
    padding: 0.2em 0em !important;
}
</style>
'''
display(HTML(css_styles))

################################
# ASYNCHRONOUS REQUESTS        #
################################

import requests
import urllib3

class OrionAsyncRequest:

    def __init__(self):
        urllib3.disable_warnings()
        
        self.__user_token = os.environ['USER_TOKEN']
        host = os.environ.get('ORION_API_HOST', "https://api.oriondev.cytomic.ai")
        url = os.environ.get('ORION_URL', f"/api")
        apiv = os.environ.get('ORION_API_VERSION', "v1")
        path = os.environ.get('ORION_PATH', '/th-library')

        self.__base_url = host + url + f"/{apiv}{path}"
        self.__default_headers = {
            'Authorization': 'Bearer ' + self.__user_token,
            'Content-Type': 'application/json-patch+json'
        }
        
        self.requests = []
        from requests_futures.sessions import FuturesSession
        self.session = FuturesSession()
        
    @property
    def get_base_url(self):
        return self.__base_url

    @property
    def get_default_headers(self):
        return self.__default_headers

    def get(self, url: str, headers, verify = False):
        request = self.session.get(self.__base_url + url, headers=self.__default_headers if headers is None else headers, verify=verify)
        self.requests.append({'method': 'GET', 'url': url, 'data': None, 'request': request})
        return request

    def post(self, url: str, data = None, headers = None, verify = False):
        request = self.session.post(self.__base_url + url, headers=self.__default_headers if headers is None else headers, data=data, verify=verify)
        self.requests.append({'method': 'POST', 'url': url, 'data': data, 'request': request})
        return request
    
    def __find_request(self, request: requests.Response):
        for r in self.requests:
            if r['request'] == request:
                return r
        return None
    
    def _wait(self, rdata):
        error = None
        
        r = rdata['request'].result()
        if r.status_code != 200:
            if r.content == '':
                error = f"ERROR [{r.status_code}] IN {rdata['method']} REQUEST:"
            else:
                try:
                    error = json.dumps(r.json(), indent=4)
                except:
                    error = r.text
                    
        if error is not None:
            raise(error)
            
        return r

    def wait(self, request = None):
        rlist = []

        if request is not None:  # wait for single/specific request
            rdata = self.__find_request(request)
            if rdata:
                rlist.append(self._wait(rdata))
        else:  # wait for all pending requests
            for rdata in self.requests:
                rlist.append(self._wait(rdata))

        return rlist

def sql_query_request(req: OrionAsyncRequest, sql: str):
    if req is None:
        raise Exception("No request has been provided")
        
    url = f"/explorations"
    
    if "CASE_ID" in os.environ and "NOTEBOOK_ID" in os.environ:
        data = json.dumps({
            "sql": sql, 
            "notebookId": os.environ["NOTEBOOK_ID"],
            "caseId": os.environ["CASE_ID"]
        })
    else:
        data = json.dumps({
            "sql": sql
        })
        
    return req.post(url, data)
    
def async_query_response(req: OrionAsyncRequest, request = None): 
    if req is None:
        raise Exception("No request has been provided")
                        
    _responses = []
    if req:
        _responses = req.wait(request)
    
    _results = []
    for _res in _responses:
        if _res.status_code == 200:
            try:
                _df = pd.DataFrame(_res.json())
                _results.append(_df)
            except:
                try:
                    _results.append(_res.json())
                except:
                    _results.append(pd.DataFrame())
        else:
            _results.append(None)

    return _results

################################
# BRICKS FACTORY               #
################################

import json

# cache para evitar recalcular los datos de un brick
class BrickCache:
    def __init__(self):
        self._data = {}
    
    def rd(self, __name, **kwargs):
        if __name in self._data:
            _args = json.dumps(kwargs)
            _data = self._data[__name] 
            if _args in _data:
                return _data[_args]
        return None
    
    def wr(self, __name, __data, **kwargs):
        if __name not in self._data:
            self._data[__name] = {}

        _args = json.dumps(kwargs)
        self._data[__name][_args] = __data     

# encapsula la ejecución de una función dentro de un brick
class BrickBase:
    Cache = True    # declare static variables to apply/remove cache read operation in every Brick instance
    
    def __init__(self, name, factory, func, label=None, desc=None, long=None, tags=[], args=None):
        self._name = name           # the brick name
        self._factory = factory     # the brick factory (a brick can call other bricks)
        self._func = func           # the brick method
        self._label = label         # the brick label (to show on brick select)
        self._desc = desc           # the brick description (to show on brick select)
        self._long = long           # long description (to show when selected)
        self._tags = tags           # the brick search tags (shown on brick select)
        
        self._args = []             # required arguments list
        self._fixd = []             # fixed arguments (to be propagated with selection) 
        self._edit = []             # editable arguments list
        self._list = []             # list of arguments with multiple values
        
        if args is not None:
            for _arg, _opt in args.items():
                self.args.append(_arg)     
                if 'propagate' in _opt and _opt['propagate']:
                    self._fixd.append(_arg)
                if 'editable' in _opt and _opt['editable']:
                    self._edit.append(_arg)
                if 'multiple' in _opt and (_opt['multiple'] == False):
                    self._list.append(_arg)

    @property 
    def name(self):
        return self._name
    
    @property
    def label(self):
        return self._label

    @property
    def desc(self):
        return self._desc
    
    @property
    def long(self):
        return self._long
    
    @property
    def tags(self):
        return self._tags
    
    @property
    def args(self):
        return self._args
    
    @property
    def fixed(self):
        return self._fixd
    
    @property
    def edit(self):
        return self._edit

    @property
    def list(self):
        return self._list

    @property
    def mode(self):
        return None # will be available only for BrickFunc instances 
    
    def hastag(self, tag):
        for _tag in self._tags:
            if _tag.startswith(tag):
                return True
        return False
    
    def UseCache(self, value):
        self._cache = value
    
    def run(self, show, layout, provides, consumes, **kwargs):
        _fixedargs = {} # calculate the fixed arguments from kwargs
        for _fixedarg in self.fixed:
            if _fixedarg in kwargs:
                _fixedargs[_fixedarg] = kwargs[_fixedarg]
        
        _data = self._factory.cache.rd(self._name, **kwargs) if BrickBase.Cache else None                      # recover from cache
        _data = self._func(self._factory, _data, show, layout, _fixedargs, provides, consumes, **kwargs)       # execute the brick
        self._factory.cache.wr(self._name, _data, **kwargs)                                                    # store result in cache
        
        return _data

class BrickFactory:
    def __init__(self, catalog=None):
        self._bcache = BrickCache()
        self._bricks = {}

        if catalog is not None:
            self.add_catalog(catalog)
    
    # includes a brick into the factoru
    def add_brick(self, brick):
        brick._factory = self               # this brick belongs to this factory    
        self._bricks[brick.name] = brick    # add the brick to the catalog
    
    # concatenate a bricks factory into this one
    def concat(self, factory):
        for brick in factory.bricks.values():
            self.add_brick(brick)
            
    @property
    def cache(self):
        return self._bcache
    
    @property
    def bricks(self):
        return self._bricks
    
    @property
    def tags(self):
        _tags = []

        for _brick in self._bricks.values():
            for _tag in _brick.tags:
                _add = ''
                _spl = _tag.split('/')
                for _key in _spl:
                    _add += _key
                    _tags.append(_add)
                    _add += '/'

        _tags = list(dict.fromkeys(_tags))
        _tags.sort()
        return _tags
    
    def bytag(self, tag):
        _bricks = []
        for _brick in self._bricks.values():
            if _brick.hastag(tag):
                _bricks.append(_brick)
        return _bricks
    
    # executes a brick in the falctory
    def run(self, brick=None, func=None, show=True, layout=None, provides=None, consumes=None, **kwargs):
        if brick is None and func is None:
            raise Exception("you must provide a brick name or brick function")
        
        if brick is None:
            return BrickBase(func.__name__, self, func).run(show, layout, provides, consumes, **kwargs)
        else:        
            if brick in self._bricks:
                return self._bricks[brick].run(show, layout, provides, consumes, **kwargs)
            else:
                raise Exception(f"{brick} not found in catalog!")

'''
Clase para la creación de bricks a demanda
Un brick necesita de 1 nombre y 2 métodos
- Funcion de evaluación de los datos del brick
     _fnc_eval(**kwargs):
     
- Funcion de renderizado de los datos del brick
    _fnc_show(data, layout, provides, **kwargs): 
    
    data: El resultado devuelto por _fnc_eval
    layout: El layout en el que mostrar el brick
    provides: Datos seleccionados dentro del brick

- Ejemplo de uso:
    def funcion_eval(...):
        # realizar los calculos y guardarlos en _result
        return _result
    def funcion_show(_result, layout, provides, ...):
        # dibujar _result en el layout
        # almacenar los datos seleccionados en provides

    bricks = get_bricks() # obtiene la factoria de bricks
    brick = brFunc(bricks, 'my_brick', funcion_eval, funcion_show, 'etiqueta del brick', 'descripcion', 'parametros') # crea un nuevo brick
    bricks.add_brick(brick) # añade el brick a la factoria 
    
- Ejemplo de uso:
    brick = brFunc(bricks, 'my_brick', funcion_eval, funcion_show, 'etiqueta del brick', 'descripcion', 'parametros')
    brick.run() # ejecuta la funcionalidad del brick
'''

class BrickFunc(BrickBase):
    def __init__(self, bricks, name, _fnc_eval, _fnc_show, label=None, desc=None, long=None, tags=[], args=None, mode=None):
        self._eval = _fnc_eval
        self._show = _fnc_show
        
        super().__init__(name, bricks, self._brfc(), label, desc, long, tags, args);
        self._mode = mode
    
    @property
    def mode(self):
        return self._mode
    
    def _brfc(self):
        def _function(bricks, data, show, layout, fixed, provides, consumes, **kwargs):
            _result = data
            
            # evaluate if data not available
            if _result is None and self._eval is not None: 
                _result = self._eval(**kwargs)
    
            # display if requested
            if show and self._show is not None:
                self._show(_result, layout, fixed, provides, **kwargs)
        
            # return evaluated data
            return _result        
        
        return _function

'''
Agrupa la funcion de evaluación y de renderizado en una clase
- Ejemplo de uso

class MyBrick(BrickClass):
    def __init__(self, bricks, label, desc, args, fixed):
        super().__init__(
            bricks = bricks,
            label = 'Etiqueta del brick',
            desc = 'Descripción del brick',
            tags = ['Tag1', 'Tag2', ...],
            args = { 
                '<argument name>': { <argument spec> },
                ...
                '<argument name>': { <argument spec> }
            },
            mode = '<data | info>')
    
    def _eval(self, ...):
        <funcion de evaluación / recogida de datos>
     
     # _result: El resultado de la funcion _eval
     # layout: El layout de renderizado del brick
     # fixedargs: Los parametros a añadir a la seleccion del usuario
     # provides: clave del scope a actualizar con la seleccion del usuario
     
     def _show(self, _result, layout, fixedargs, provides, ...):
        <funcion de renderizado en el layout>
'''

class BrickClass(BrickFunc):
    def __init__(self, bricks, label, desc, long, tags, args, mode):
        super().__init__(bricks, type(self).__name__, self._eval,  self._show, label, desc, long, tags, args, mode)
            
    def _eval(self): # defined on derived class
        return None # by default evaluate nothing

    def _show(self, _result, layout, provides): # defined on derived class
        pass # by default do not render anything

################################
# LIMIT QUERY SIZE             #
################################

class LimitDataframe(pd.DataFrame):
    def __init__(self, df, limited):
        super().__init__(df)        
        self._limited = limited
    
    @property
    def isLimited(self):
        return self._limited
    
class QueryDataframe(LimitDataframe):
    _Limit = 500   # declare static variables to apply/remove limits in every QueryDataframe instance
    def Limit(value):
        QueryDataframe._Limit = value            # define the dataframe limits
        BrickBase.Cache = (value is not None)    # do not use cache if no limits
    
    def __init__(self, sql):
        from TH.Core.adhoc import get_sql_query
                       
        # if sql is not limited, add the limit 
        _sql = sql
        if QueryDataframe._Limit is not None and not re.search('limit (\d+)( )*$/i', sql):
            _sql += f" LIMIT {QueryDataframe._Limit}"
        
        _result = get_sql_query(_sql)
        
        _limited = False
        if QueryDataframe._Limit is not None:
            _limited = (len(_result) == QueryDataframe._Limit)
            _limited = True # TODO: quitar: solo para pruebas
            
        super().__init__(_result, _limited)
        
        self._sql = sql
        self._limit = QueryDataframe.Limit

class NbLimitedResultsWarning(NbComponent):
    def __init__(self):
        super().__init__('limited_warning')
        
    def declare(self, brick, args, provides=None, consumes=None):
        # declare the component widget function
        def _fnc_component(nb):
            import ipywidgets.widgets as w
            
            _html = '''
                <div style="width=100%; line-height: 15px; color: var(--color-danger); ">
                    <b>Showing incomplete result set!</b><br>
                    <span style="font-size: 80%">The complete result set may be expensive in time and machine resources</span>
                </div>
            '''
            
            def _fnc_on_recalculate_click(button):
                _limit = QueryDataframe.Limit
                
                # recover the brick arguments from provided list of locals
                _args = {}
                for _arg, _val in args.items():
                    if _arg in brick.args:
                        _args[_arg] = _val
                
                QueryDataframe.Limit(None)       # remove the limit in queries
                nb.scope.set(provides, _args)    # request brick execution
                QueryDataframe.Limit(_limit)     # recover the brick limits
                                
            _warninghtml = w.HTML(value=_html, layout=w.Layout(display='block', height='fit-content', width='100%'))
            _querybutton = w.Button(description='Run complete', layout=w.Layout(display='flex', flex_flow='row', align_content='flex-end', width='15%'))
            _querybutton.on_click(_fnc_on_recalculate_click)
            
            display(w.HBox([_warninghtml, _querybutton]))
        
        # this is an attribute for nbLayout, so it can access to its members
        self._widget = ScopeWidget(_fnc_component, self, provides, consumes)
        self.append(self._widget, 'widget')

_ = NbLimitedResultsWarning()

################################
# DASHBOARD COMPONENTS         #
################################

# BRICK PARAMETERS EDIT
def _fnc_brick_title_html(index, brick, args):
    _name = brick.label
    _index = (index+1) if index is not None else 0

    _editable = brick.edit
    if index is None: # make all parameters editable for first brick
        _editable = brick.args

    _args = ''
    for key, arg in args.items():
        if key in _editable:
            _args += '<br/>'
            _args += f'<span style="font-weight:bold;">{key}</span>'
            if isinstance(arg, list):
                _args += f': [ {", ".join( [str(x) for x in arg] )} ]'
            else:
                _args += f': {arg}'
                
    _args = _args.removeprefix('<br/>')

    _html = f'''
        <div style="position:relative;">
            <div style="position: relative; display:block; top: 30px; padding-left: 5px; background:var(--color-accent);  width:100%;  height: 4px">
            </div>
            <div style="position: absolute; width:50px; height:50px; background:var(--color-accent); color:var(--color-text-inverse); border-radius:50%;">
                <span style="position: relative; display: block; top: 5px; font-size:30px; padding: 5px;text-align:center;">
                    {_index}
                </span>
            </div>
            <div style="position:relative; font-size: 14px; top: 0px; padding-left: 55px;color:var(--color-accent)">
                {_name}
            </div>
            <div style="position:relative; font-size: 11px; line-height: 15px; padding-top: 5px; padding-left: 55px; color:var(--color-accent); max-width: 82%; white-space: nowrap; text-overflow: ellipsis; overflow: hidden">
                {_args}
            </div>
        </div>
    '''
    return _html

def _fnc_brick_desc_html(brick, args):   
    if brick.long is not None:
        _text = brick.long(args)
        if _text is not None:
            _html = f'''
            <div style="margin: 10px 0px 0px 50px; border: 1px solid var(--color-accent); border-radius: 2px; padding: 5px 10px; line-height: 15px">
                <span style="font-size: 12px; color: var(--color-accent);">{_text}</span>
            </div>
            '''
            return _html
    return ''

class NbBrickArgs(NbComponent):
    def __init__(self):
        super().__init__('brick_args')
        
    def declare(self, desc, args, provides=None, consumes=None):   
        # declare the component widget function
        def _fnc_component(nb):
            class _Brick():
                def __init__(self, label, edit):
                    self.label = label
                    self.edit = edit
            
            return _fnc_brick_title_html(-1, _Brick(desc, args.keys()), args)
        
        # this is an attribute for nbLayout, so it can access to its members
        self._widget = ScopeWidget(_fnc_component, self, provides, consumes)
        self.append(self._widget, 'html')

_ = NbBrickArgs()

class NbBrickEdit(NbComponent):
    def __init__(self):
        super().__init__('brick_edit')
        
    def declare(self, index, brick, args, wnext, provides=None, consumes=None):   
        # declare the component widget function
        def _fnc_component(nb):
            import ipywidgets.widgets as w
                       
            # add editable parameters if not already in args
            _editable = brick.edit
            if index is None: # make all parameters editable for first brick
                _editable = brick.args

            for arg in _editable:
                if arg not in args:
                    args[arg] = []
            
            _cssstyle = w.HTML(value ='''
            <style>
                .top-button { z-index: 2; }
            </style>
            ''')
            
            _headhtml = w.HTML(value=_fnc_brick_title_html(index, brick, args), layout=w.Layout(display='block', height='fit-content', width='100%'))
            _editbutton = w.Button(description='Edit Values', layout=w.Layout(display='flex', flex_flow='row', align_content='flex-end', width='15%'))
            _editbutton.add_class('top-button')
            _deschtml = w.HTML(value=_fnc_brick_desc_html(brick, args), layout=w.Layout(display='block', width='100%'))
            
            _argsedit = []; # esto contiene una lista de valores por cada argumento de tipo lista
            _argsarea = {}
            _argstext = {}
            for key, arg in args.items():
                if key in _editable:
                    if isinstance(arg, list):
                        _arghtml = f'<h3 style="color:var(--color-accent)">Edit values for the <b>{key}</b> parameter (one value per row):</h3>'
                        _argtitle = w.HTML(value=_arghtml, layout = w.Layout(flex='1 1 auto', width='auto'))
                        _argarea = _argsarea[key] = w.Textarea(value='\n'.join([str(x) for x in arg]), layout = w.Layout(flex='1 1 auto', width='auto'))
                        _argsedit.append(w.VBox([_argtitle, _argarea], layout=w.Layout(width='100%')))
                    else:
                        _arghtml = f'<h3 style="color:var(--color-accent)">Edit values for the <b>{key}</b> parameter:</h3>'
                        _argtitle = w.HTML(value=_arghtml, layout = w.Layout(flex='1 1 auto', width='auto'))
                        _argtext = _argstext[key] = w.Text(value=str(arg), layout = w.Layout(flex='1 1 auto', width='auto'))
                        _argsedit.append(w.VBox([_argtitle, _argtext], layout=w.Layout(width='100%')))

            _parambox = w.VBox(_argsedit, layout=w.Layout(width='100%'))
            _refrbutton = w.Button(description="Refresh", layout=w.Layout(display='flex', flex_flow='row', align_content='flex-end', width='15%'))
            _ccelbutton = w.Button(description="Cancel", layout=w.Layout(display='flex', flex_flow='row', align_content='flex-end', width='15%'))
            
            def _fnc_on_refresh():
                def f(button):
                    _args = {}
                    for key, value in args.items():
                        _args[key] = value
                    
                    # update the parameters
                    for key, textarea in _argsarea.items():
                        args[key] = _args[key] = list(dict.fromkeys(textarea.value.split('\n')))
                    for key, textinput in _argstext.items():
                        args[key] = _args[key] = textinput.value  
                            
                    # stop editing
                    _editbutton.layout.display = 'flex'
                    _editvbox.layout.display = 'none'
                    
                    # update the header and description
                    _headhtml.value = _fnc_brick_title_html(index, brick, args)
                    _deschtml.value = _fnc_brick_desc_html(brick, args)

                    # clears the next brick 
                    if nb.scope.get(wnext) is not None:
                        nb.scope.set(wnext, None)             
                    
                    # refresh current brick (return new args)
                    nb.scope.set(provides, _args)
                    
                return f
            
            _refrbutton.on_click(_fnc_on_refresh())
            
            _editrow1 = w.Box([_parambox], layout = w.Layout(display='flex', flex_flow='row', width='100%'))
            _editrow2 = w.Box([_refrbutton, _ccelbutton], layout = w.Layout(display='flex', flex_flow='row',  justify_content='flex-end', width='100%'))
            _editvbox = w.VBox([_editrow1, _editrow2 ], layout=w.Layout(display='none', margin="25px 0px 0px 0px", width='100%'))
            
            def _fnc_on_edit_click(button):
                _editbutton.layout.display = 'none'
                _editvbox.layout.display = 'flex'
            
            def _fnc_on_ccel_click(button):
                for key, textarea in _argsarea.items():
                    textarea.value = '\n'.join(args[key])

                _editbutton.layout.display = 'flex'
                _editvbox.layout.display = 'none'
                
            _editbutton.on_click(_fnc_on_edit_click)
            _ccelbutton.on_click(_fnc_on_ccel_click)
            
            _row1 = w.Box([_headhtml], layout = w.Layout(overflow_x='hidden', width='100%', margin='-50px 0px 0px 0px'))
            _row2 = w.Box([_editbutton], layout = w.Layout(width='100%', margin='0px 0px 0px 0px', align_content='flex-start', justify_content='flex-end', top='38px', height='50px'))
            _row3 = w.Box([_deschtml], layout = w.Layout(display='flex', flex_flow='row', width='100%', margin='20px 0px 0px 0px'))
            _row4 = w.Box([_editvbox], layout = w.Layout(display='flex', flex_flow='row', width='calc(100% - 50px)', margin='0px 0px 0px 50px'))
            display(w.VBox([_cssstyle, _row2, _row1, _row3, _row4]))
        
        # this is an attribute for nbLayout, so it can access to its members
        self._widget = ScopeWidget(_fnc_component, self, provides, consumes)
        self.append(self._widget, 'widget')

_ = NbBrickEdit()

# AG GRID WITH ROW SELECT
def _fnc_aggrid_rowstyle_js(rules):
    _jsfunc = '''function(params)
        {
            let _style = {};
            if (params.node.data) {
    '''

    # selected row style
    _jsfunc += '''
        if (('selected' in params.node.data) && (params.node.data['selected'])){
            _style['color'] = "var(--color-text-inverse)";
            _style['background'] = "rgba(93, 50, 120, .7)";
        }
    '''

    #configurable row styles
    for _rule in rules:
        _field = _rule['field']
        _value = _rule['value']
        _style = _rule['style']

        _jsfunc += f'''if (('{_field}' in params.node.data) && (params.node.data['{_field}'] == '{_value}')){{'''
        _props = _style.split(';')[:-1] # get all the style properties
        for _property in _props:
            _parts = _property.split(':')
            
            _cssnam = _parts[0].strip()
            _cssval = _parts[1].strip()
            
            _jsfunc += f'''_style['{_cssnam}'] = "{_cssval}";''' 
        _jsfunc += '''}''' 

    _jsfunc += '''
            }
            return _style;
        }
    '''

    return _jsfunc

def _fnc_aggrid_cellstyle_js(rules):    
    _jsfunc = '''
        function(params) {
            if (!params.value){
                return ''
            }
    '''
    for _rule in rules:
        _jsfunc += f'''
            if (params.data['{_rule['field']}'] == '{_rule['value']}'){{
                return `<span style="{_rule['style']}">` + params.value + `</span>`;
            }}
        '''

    _jsfunc += '''
            return params.value;
        }
    '''
    
    return _jsfunc

def _fnc_dataframe_to_aggrid(data, options={}):
    from ipyaggrid import Grid

    if not isinstance(data, pd.DataFrame):
        return None
    
    # define grid columns 
    column_defs = []
    for column in data.columns:
        if column == 'selected':
            continue  # will be included based on options
            
        if 'tree' in options and 'path' in options['tree'] and column == options['tree']['path']:
            continue  # will be included based on options
            
        _definition = {
            'field': column,
            'editable': False,
            'suppressSizeToFit': False
        }

        if ('htmlColumns' in options) and (column in options['htmlColumns']):
            _columnopts =  options['htmlColumns'][column]
            
            if 'headerName' in _columnopts:
                _definition['headerName'] = _columnopts['headerName']
            if 'width' in _columnopts:
                _definition['width'] = _columnopts['width']
                
            _definition['cellRenderer'] = '''function(params){
                console.log(params.value);
                return params.value;
            }'''
        
        column_defs.append(_definition)

    if 'groupcolumns' in options:
        _style = '''
            <style>
                .ag-header-group-cell-no-group,
                .ag-header-group-cell-with-group {
                    background: var(--color-text-inverse);
                }
                
                .ag-header-group-cell-with-group * {
                    font-size: 120% !important;
                    color: var(--color-accent) !important;
                }
            </style>
        '''
        display(HTML(_style))

        groups_defs = []
        
        # add other columns based on given group definitions
        for _group in options['groupcolumns']:
            _newgroup = {
                'headerName': _group['headerName'] if 'headerName' in _group else '',
                'columns_fit': "size-to-fit",
                'children': []
            }
            
            _defnmap = {}
            for _definition in column_defs:
                _defnmap[_definition['field']] = _definition
            
            for _child in _group['children']:
                _field = _child['field']
                if _field in _defnmap:
                    _definition = _defnmap[_field]
                    for _key, _val in _child.items():
                        _definition[_key] = _val
                    _newgroup['children'].append(_definition)
            
            groups_defs.append(_newgroup)            
        
        column_defs = groups_defs
    
    # add the 'must-have' column definitions
    if 'tree' in options and 'path' in options['tree']:
        column_defs.insert(0, { 
            'field': 'selected',
            'hide': True,
            'suppressToolPanel': True
        })

        column_defs.append({
            'field': options['tree']['path'],
            'hide': True,
            'suppressToolPanel': True
        })
    else:
        column_defs.insert(0, { 
            'field': 'selected',
            'headerName': '',
            'editable': False,
            'width': 35,
            'suppressSizeToFit': True,
            'cellRenderer': '''function(params){
                return `<span class="select-icon icon icon--information-circle" style="font-size: 18px; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);"></span>`;;
            }'''
        })        
    
    # apply cellrenderers based on cell custom styles
    if 'cellStyleRules' in options:
        for _cellName in options['cellStyleRules'].keys():
            for _column in column_defs:
                if 'field' in _column and _column['field'] == _cellName:
                    _column['cellRenderer'] = _fnc_aggrid_cellstyle_js(options['cellStyleRules'][_cellName])
                elif 'children' in _column: # grouped
                    for _child in _column['children']:
                        if 'field' in _child and _child['field'] == _cellName:
                            _child['cellRenderer'] = _fnc_aggrid_cellstyle_js(options['cellStyleRules'][_cellName])

    # define grid options
    grid_options = {
        'getRowStyle': _fnc_aggrid_rowstyle_js(options['rowStyleRules'] if 'rowStyleRules' in options else []),
        'columnDefs': column_defs,
        'defaultColDef': {'sortable': True, 'filter': True, 'resizable': True},
        'enableRangeSelection': False
    }    
    
    # check if singlerow option is True, otherwise multiple selection
    if 'singlerow' in options and options['singlerow']:
        grid_options['rowSelection'] = 'single'
        grid_options['rowMultiSelectWithClick'] = False
    else:
        grid_options['rowSelection'] = 'multiple'
        grid_options['rowMultiSelectWithClick'] = True
        
    if 'groupcolumns' in options:
        grid_options['groupDisplayType'] = 'custom'
    
    #provide 'treepath' in format "field/field/../field" in the treepath specified column
    if 'tree' in options and 'path' in options['tree']:        
        _style = '''
            <style>
                .ag-group-expanded .ag-icon {
                    color: black !important;
                }
                
                .ag-group-contracted .ag-icon {
                    color: black !important;
                }
            </style>
        '''
        display(HTML(_style))        
        
        grid_options['treeData'] = True
        grid_options['groupDefaultExpanded'] = -1 # expand all groups by default
        grid_options['getDataPath'] = f'''function(data){{
            return data["{options['tree']['path']}"].split("/");
        }}'''
        grid_options['autoGroupColumnDef'] = {
            'headerName': options['tree']['group'] if ('group' in options['tree']) else "Group",
            'width': 300,
            'cellRendererParams': {
                'suppressCount': True
            }            
        }
    
    css_rules = """
        .ag-row-selected {
            color: var(--color-text-inverse);
            background: rgba(93, 50, 120, .7) !important;
        }
        
        .select-icon {
            display: none;
        }
        
        .ag-row-selected .select-icon {
            display: block !important;
        }
    """
        
    _grid = Grid(
        width='100%',
        height=0,
        grid_data=data,
        grid_options=grid_options,
        css_rules=css_rules,
        sync_grid=False,
        columns_fit='size_to_fit',
        quick_filter=True,
        show_toggle_edit=False,
        export_mode='auto',
        export_to_df=True,
        theme='ag-theme-balham',
        license='.ag_grid_license'
    )
    
    return _grid    
    
# AGGRID SELECCIONABLE
class NbGrid(NbComponent):
    def __init__(self):
        super().__init__('grid')
    
    def declare(self, data, fixedargs={}, options={}, provides=None, consumes=None):
        # declare the component widget function
        def _fnc_component(nb):
            _data = data(nb) if callable(data) else data 
            if isinstance(_data, ScopeKey):
                _data = nb.scope.get(_data)            
            
            if _data is None:
                return None
            
            if not 'selected' in _data.columns:     # row selection
                _data.insert(0, 'selected', False)
            else:
                _data['selected'] = False
            
            _grid = _fnc_dataframe_to_aggrid(_data, options)
            
            # the selected rows will be added to the scope in the 'provides' key
            if provides is not None:               
                def _on_select_row(change):
                    nonlocal _data
                    nonlocal _grid

                    _selected = fixedargs.copy()
                    _selected['rowcount'] = 0
                    for index, row in change['new']['rows'].iterrows():
                        _row = _data.loc[index]
                        _selected['rowcount'] += 1
                        for column in _data.columns:
                            if column == 'selected':
                                continue

                            _column = column.lower()
                            if _column not in _selected:
                                _selected[_column] = []

                            if isinstance(_selected[_column], list):
                                _selected[_column].append(_row[column])
                    
                    nb.scope.set(provides, _selected)                        
                
                _grid.observe(_on_select_row, 'grid_data_out')

            display(_grid)
            return None
            
        # this is an attribute for nbLayout, so it can access to its members
        self._widget = ScopeWidget(_fnc_component, self, provides, consumes)
        self.append(self._widget, 'widget')
        
_ = NbGrid()

# BRICKS DROPDOWN
def run_in_notebook(brickname, bricklabel, brickargs):
    from TH.Core import OrionRequest

    req = OrionRequest()
    req.SetDebug(False)

    url = f"/jupyter/document/parametrized"

    templateId = 41358
    caseId = os.environ['CASE_ID']
    
    elements = []
    elements_str =  (b'\xf0\x9f\xa7\xb1').decode() + bricklabel
    for _brick_arg in brickargs:
        if type(brickargs[_brick_arg]) == list:
            elements = brickargs[_brick_arg]
            break        

    elements = list(set(elements))

    if len(elements) > 0:
        elements_str = elements_str + " (" + elements[0]
        if len(elements) > 1:
            elements_str = elements_str + (b'\xe2\x9e\x95').decode()
        elements_str = elements_str + ")"
    
    elements_str = elements_str.replace(".",(b'\xc2\xb7').decode())
    brickargs = base64.b64encode(jsonpickle.encode(brickargs).encode('ascii')).decode('ascii')

    data = json.dumps({
      "templateId": templateId,
      "caseId": caseId,
      "name": elements_str,
      "parameters": {
            "brickname" : brickname,
            "brickargs" : brickargs            
      }
    })

    response = req.post(url=url, data=data);
    nbid = response.json()['notebookId']
    html = f'''https://orion.cytomicmodel.com/cases/{caseId}/investigation-200/{nbid}?executeAtStart=true'''
    return html

class NbBrickSelector(NbComponent):
    def __init__(self):
        super().__init__('brick_select')
        
    def declare(self, bricks, brickname, content=None, provides=None, consumes=None):
        # declare the component widget function
        def _fnc_component(nb):
            import ipywidgets.widgets as w
        
            def _process_entry(muid, md5, pid):
                return json.dumps({
                    'muid': str(muid),
                    'md5': str(md5),
                    'pid': int(pid)
                })
        
            def _remove_ambiguity(selection):
                _selection = {}
                if selection is not None:
                    for _column in selection:
                        _field = _column

                        # parent* and child*
                        _disam = [ 'parent', 'child']
                        for _prefix in _disam:
                            if _column.startswith(_prefix):
                                _field = _column[len(_prefix):]

                        # remoteusername, loggeduser
                        if (_column == 'remoteusername') or (_column == 'loggeduser'):
                            _field = 'user'
                        
                        # alertid
                        if (_column == 'alertid'):
                            _field = 'ioa'
                        
                        if _field not in _selection:
                            _selection[_field] = []

                        if isinstance(selection[_column], list):
                            _selection[_field] = _selection[_field] + list(filter(lambda a: a is not None, selection[_column])) 
                        else:
                            _selection[_field] = selection[_column]

                    # process (muid | md5 | pid)
                    if 'muid' in selection:
                        _process = []
                        
                        for _idx in range(len(selection['muid'])):
                            if ('parentmd5' in selection) and ('parentpid' in selection):
                                _process.append(_process_entry(selection['muid'][_idx], selection['parentmd5'][_idx], selection['parentpid'][_idx]))
                            elif ('childmd5' in selection) and ('childpid' in selection):
                                _process.append(_process_entry(selection['muid'][_idx], selection['childmd5'][_idx], selection['childpid'][_idx]))
                            elif ('md5' in selection) and ('pid' in selection):
                                _process.append(_process_entry(selection['muid'][_idx], selection['md5'][_idx], selection['pid'][_idx]))
                        
                        if len(_process) > 0:
                            _selection['process'] = _process
                
                return _selection
        
            _select = _remove_ambiguity(nb.scope.get('grid-select'))
            
            def _is_suitable_brick(brick, selection):
                for _arg in brick.args:
                    if _arg not in selection or (isinstance(selection[_arg], list) and len(selection[_arg]) == 0):
                        return False
                return True
            
            def _to_tittle_html(text):
                return f'<span style="color: var(--color-accent);position: relative; top: -6px;">{text}</span>'
            
            def _to_description_html(text):
                return f'<span style="color: var(--color-accent); font-weight: bold; position: relative; top: -6px;">{text}</span>'
            
            _default = None
            _opttags = [ 'All categories'] + bricks.tags
            
            _options = []
            for _name, _brick in bricks.bricks.items():
                if (_is_suitable_brick(_brick, _select)):
                    if _default is None:      # default value is the first entry
                        _default = _to_description_html(_brick.desc)
                    _options.append((_brick.label, _brick.name))
            
            if _default is None:
                _default = _to_description_html("No suitable options for current selection")
            
            _lbeltags = w.HTML(value=_to_tittle_html("Choose category:"), layout=w.Layout(height="1em"))
            _droptags = w.Dropdown(options = _opttags, layout=w.Layout(display='flex', flex_flow='row', width='150px'))
            _lbelopts = w.HTML(value=_to_tittle_html("Choose brick:"), layout=w.Layout(height="1em"))
            _dropdown = w.Dropdown(options = _options)
            _vboxtags = w.VBox([ _lbeltags, _droptags ])
            _vboxopts = w.VBox([ _lbelopts, _dropdown ])
            _description = w.HTML(value=_default)
            _runbutton = w.Button(description = 'Run', layout=w.Layout(display='flex', flex_flow='row', align_content='flex-end', width="95%"))
            _notebook = w.Button(description = 'Run in notebook', layout=w.Layout(display='flex', flex_flow='row', align_content='flex-end', width='95%'))
            _comments = w.Button(description = 'Capture to Comments', layout=w.Layout(display='flex', flex_flow='row', align_content='flex-end', width='95%'))
            _vboxbton1 = w.VBox([_runbutton ], layout=w.Layout(display='flex', flex_flow='column', align_self='flex-end', width='15%'))
            _vboxbton2 = w.VBox([_notebook ], layout=w.Layout(display='flex', flex_flow='column', align_self='flex-end', width='18%'))
            _vboxbton3 = w.VBox([_comments ], layout=w.Layout(display='flex', flex_flow='column', align_self='flex-end', width='25%'))
            
            if content is None:
                _comments.disabled = True

            def _fnc_on_tags_select(change):
                if change['type'] == 'change' and change['name'] == 'value':
                    _options = []                    
                    _default = None

                    _tagname = _droptags.value
                    if _tagname == 'All categories':
                        _tagbricks = list(bricks.bricks.values())
                    else:
                        _tagbricks = bricks.bytag(_tagname)
                    
                    for _brick in _tagbricks:
                        if (_is_suitable_brick(_brick, _select)):
                            if _default is None:      # default value is the first entry
                                _default = _to_description_html(_brick.desc)
                            _options.append((_brick.label, _brick.name))
                    
                    if _default is None:
                        _default = _to_description_html("No suitable options for current selection")
                        
                    _dropdown.options = _options
            
            def _fnc_on_brick_select(change):
                if change['type'] == 'change' and change['name'] == 'value':
                    _brickname = _dropdown.value
                    if _brickname in bricks.bricks:
                        _brick = bricks.bricks[_brickname]
                        _description.value = _to_description_html(_brick.desc)
                        _notebook.disabled = (_brick.mode == 'info')  # do not run in notebook if 'info' brick is selected
            
            _droptags.observe(_fnc_on_tags_select)
            _dropdown.observe(_fnc_on_brick_select)
            
            _hbox_l = []
            
            if _select is not None and 'rowcount' in _select and _select['rowcount'] > 0:
                _hbox_l.append(_vboxtags)
                _hbox_l.append(_vboxopts)
                _hbox_l.append(_vboxbton1)
                _hbox_l.append(_vboxbton2)
    
            def _fnc_brick_args(brick, selection):
                _args = {}
                for _arg in brick.args:
                    _args[_arg] = list(dict.fromkeys(selection[_arg])) if isinstance(selection[_arg], list) else selection[_arg]
                return _args
                        
            def _fnc_on_run_click():
                def f(button):
                    # overwrite last selection for data bricks
                    brickmode = None
                    for _brick in bricks.bricks.values():
                        if (_brick.name == brickname):
                            brickmode = _brick.mode

                    if brickmode != 'info':
                        nb.scope.set('_last_select', _select)
                        
                    # execute the next brick
                    nextbrick = _dropdown.value
                    brickargs = {}
                    for _brick in bricks.bricks.values():
                        if _brick.name == nextbrick:
                            brickargs = _fnc_brick_args(_brick, _select)
                            
                    _next = {
                        'name': nextbrick,
                        'args': brickargs
                    }
                    
                    nb.scope.set(provides, _next)
                    
                return f

            def _fnc_on_comments_click():
                def f(button):
                    _title_widget = None
                    _brick_widget = None

                    if content is not None:
                        _title_widget = content._widgets[0]
                        _brick_widget = content._widgets[1]

                        if _brick_widget is not None:
                            _brick_widget.publish()

                        if _title_widget is not None:
                            _title_widget.publish()
                
                return f
            
            def _fnc_on_notebook_click():
                def f(button):
                    brickname = _dropdown.value
                    bricklabel = ''
                    brickargs = {}
                    
                    for _brick in bricks.bricks.values():
                        if _brick.name == brickname:
                            brickargs = _fnc_brick_args(_brick, _select)
                            bricklabel = _brick.label
                            
                    url = run_in_notebook(brickname, bricklabel, brickargs)
                    window_open(url)
                    
                return f          
            
            _runbutton.on_click(_fnc_on_run_click())
            _notebook.on_click(_fnc_on_notebook_click())
            _comments.on_click(_fnc_on_comments_click())

            if _select is not None  and 'rowcount' in _select and _select['rowcount'] > 0:
                _left = w.HBox(_hbox_l, layout=w.Layout(display='flex', flex_flow='row', align_content='flex-start', width='100%'))
                _hbox = w.Box([_left, _vboxbton3], layout = w.Layout(display='flex', flex_flow='row', width='100%'))
                display(w.VBox([_hbox, _description]))

            return None  # there is no next brick if this is rendered      
        
        # this is an attribute for nbLayout, so it can access to its members
        self._widget = ScopeWidget(_fnc_component, self, provides, consumes)
        self.append(self._widget, 'widget')

_ = NbBrickSelector()

# BRICK EXECUTION
class NbBrickRun(NbComponent):
    def __init__(self):
        super().__init__('brick_run')
        
    def declare(self, bricks, brickindex=None, brickname=None, brickfunc=None, provides=None, consumes=None, **kwargs):
        # declare the component widget function
        def _fnc_component(nb):     
            import uuid

            _domloadid = '_loadid_' + str(uuid.uuid4())
            display(HTML(f'''
                <div id="{_domloadid}" style="display: flex; height:100px;">
                    <div class="spinner spinner" style="margin: 50px auto; font-size: 2rem"><div>
                </div>'''))

            # recover the brick arguments from last refresh event
            _args = nb.scope.get('refresh')
            if _args is None:
                _args = kwargs

            _ = bricks.run(brickname, brickfunc, True, self, provides, consumes, **_args)
            
            display(HTML(f'''
                <script>
                    document.getElementById('{_domloadid}').parentNode.style.display = 'none';
                </script>'''))

        # this is an attribute for nbLayout, so it can access to its members
        self._widget = ScopeWidget(_fnc_component, self, provides, consumes)
        self.append(self._widget, 'widget')

_ = NbBrickRun()

def _fnc_render_brick(layout, bricks, brickindex=None, brickname=None, brickfunc=None, provides=None, consumes=None, **kwargs):
    if brickindex is None:
        layout.scope.set('_last_select', None)  # initialize the last selection value
    _last_select = layout.scope.get('_last_select')
    
    brickdashboard = nbDashboard(False, 'EN', layout=layout)
    
    _factory_brick = None
    if brickname is not None and brickname in bricks.bricks:
        _factory_brick =  bricks.bricks[brickname]
    
    # show /edit brick input parametes
    if _factory_brick is not None:
        brickdashboard.brick_edit(brickindex, _factory_brick, kwargs, provides, provides='refresh')
    
    # hide grid_selection until brick is executed
    if (_factory_brick is not None) and (_factory_brick.mode == 'info'):
        brickdashboard.scope.set('grid-select', None)
        
    brickdashboard.brick_run(bricks, brickindex, brickname, brickfunc, provides='grid-select', consumes=[ 'refresh' ], **kwargs)
    brickdashboard.brick_select(bricks, brickname, content=brickdashboard, provides=provides, consumes=[ 'grid-select' ])            
    brickdashboard.run()
    
    # propagate last selecion for info bricks
    if (_factory_brick is not None) and (_factory_brick.mode == 'info'):
        brickdashboard.scope.set('grid-select', _last_select)
    
# BRICK FUERA DEL MURO
class NbBrick(NbComponent):
    def __init__(self):
        super().__init__('brick')
    
    def declare(self, bricks, brickname=None, brickfunc=None, provides=None, consumes=None, **kwargs):
        # declare the component widget function
        def _fnc_component(nb):
            _fnc_render_brick(self, bricks, None, brickname, brickfunc, provides, consumes, **kwargs)

        # this is an attribute for nbLayout, so it can access to its members
        self._widget = ScopeWidget(_fnc_component, self, provides, consumes)
        self.append(self._widget, 'widget')
        
_ = NbBrick()

def _add_layout_brick(bricks, layout, brickindex):
    if not hasattr(layout, '_brickwall'):
        layout._brickwall = set()
    
    if brickindex not in layout._brickwall:
        layout._brickwall.add(brickindex)
            
        _cell = {
            'brickinfo': None,
            'wallindex': brickindex,
            'thisevent': '_cell_refresh_event_' + str(brickindex+0),
            'nextevent': '_cell_refresh_event_' + str(brickindex+1) 
        }

        layout.brick_cell(bricks, _cell['wallindex'], provides=_cell['nextevent'], consumes=_cell['thisevent'])

def _del_layout_brick(bricks, layout, brickindex):
    if not hasattr(layout, '_brickwall'):
        layout._brickwall = set()

    for _idx in range (brickindex, len(layout._widgets)):
        layout.remove(layout._widgets[_idx])   
        layout._brickwall.remove(_idx)

# CELDA PARA ALMACENAR UN BRICK
class NbBrickCell(NbComponent):
    def __init__(self):
        super().__init__('brick_cell')
    
    def declare(self, bricks, brickindex, provides=None, consumes=None):
        # declare the component widget function
        def _fnc_component(nb):
            _brickinfo = nb.scope.get(consumes)        # consumes has this brick information
            if _brickinfo is None:                     # if no brick information then clear the next one
                _del_layout_brick(bricks, self, brickindex+1)
            else:                                      # otherwise render the brick and prepare next one   
                _fnc_render_brick(self, bricks, brickindex, _brickinfo['name'], None, provides=provides, **(_brickinfo['args'].copy()))
                _add_layout_brick(bricks, self, brickindex+1)
                            
            return None
                
        # this is an attribute for nbLayout, so it can access to its members
        self._widget = ScopeWidget(_fnc_component, self, provides, consumes)
        self.append(self._widget, 'widget')

_ = NbBrickCell()

# MURO DE LADRILLOS
class NbBrickWall(NbComponent):
    def __init__(self):
        super().__init__('brick_wall')
        
    def declare(self, bricks, provides=None, consumes=None):
        # declare the component widget function
        def _fnc_component(nb):
            walldashboard = nbDashboard(False, 'EN', layout=self)
            
            _brickinfo = nb.scope.get('_cell_refresh_event_0')
            if _brickinfo is not None:
                _del_layout_brick(bricks, walldashboard, 0)    # remove all wall bricks
                _add_layout_brick(bricks, walldashboard, 0)    # create the first brick

            walldashboard.run()
            
        # this is an attribute for nbLayout, so it can access to its members
        self._widget = ScopeWidget(_fnc_component, self, provides, consumes)
        self.append(self._widget, 'widget')
    
_ = NbBrickWall()

################################
# BRICKS METHODS               #
################################

def _list_remove(needles, haystack):
    _needles = needles if isinstance(needles, list) else [ needles]
    _result = haystack
    for _needle in _needles:
        _result = [i for i in _result if i != _needle] 
    return _result

def _get_machine_names(muids):
    from TH.Core.adhoc import get_machine_name
    
    def _query_machines(_muids, _step):
        _pivot_ini = _pivot_end = 0
        _names = [];
        
        while _pivot_end < len(_muids):  
            _pivot_end = _pivot_ini + _step
            _part = _muids[_pivot_ini : _pivot_end]
            _data = get_machine_name(_part)
            _pivot_ini = _pivot_end
            
            if 'status' in _data:   # request has failed
                _data = []
                if _step > 1:       # try with smaller blocks
                    _data = _query_machines(_part, _step // 2)

            _names = _names + _data

        return _names

    _names = []
    
    _muids = list(dict.fromkeys(muids))
    _data = _query_machines(_muids, 10000)
    for _machine in _data:
        _names.append({
            'Muid': _machine['muid'],
            'Name': _machine['machineName']
        })
    
    return _names 

def _sql_query_client_period_to_processops(client, period, md5s=[], filenames=[]):
    _md5s = [ md5s ] if not isinstance(md5s, list) else md5s
    _filenames = [ filenames ] if not isinstance(filenames, list) else filenames    
    
    _ini_date = period.ini("%Y/%m/%d")
    _ini_dttm = period.ini("%Y/%m/%d %H:%M:%S")
    _end_date = period.end("%Y/%m/%d")
    _end_dttm = period.end("%Y/%m/%d %H:%M:%S")
    
    from TH.Core.adhoc import get_sql_query

    _sqlhash = ''
    if (len(_md5s) > 0):
        _sqlhash += 'AND ('
        for _md5 in _md5s:
            _sqlhash += f"(lower(Md5) = '{_md5.lower()}') OR "
        _sqlhash = _sqlhash.removesuffix(' OR ') + ') '
    
    _sqlfile = ''
    if (len(_filenames) > 0):
        _sqlfile += 'AND ('
        for _filename in _filenames:
            _sqlfile += f"(lower(Filename) LIKE '%{_filename.lower()}%') OR "
        _sqlfile = _sqlfile.removesuffix(' OR ') + ') '
    
    _sql = f"SELECT Muid, LoggedUser, ParentFilename as Filename, ParentMd5 as Md5, ParentPath as Path  FROM ProcessOps WHERE ClientId='{client}' "
    _sql += f"AND Date >= '{_ini_date}' AND Date <= '{_end_date}' "
    _sql += f"AND DateTime >='{_ini_dttm}' AND DateTime <='{_end_dttm}' "
    _sql += _sqlhash
    _sql += _sqlfile    
    _sql += "GROUP BY Muid, LoggedUser, Filename, Md5, Path "
    _parents = get_sql_query(_sql)
    
    _sql = f"SELECT Muid, LoggedUser, ChildFilename as Filename, ChildMd5 as Md5, ChildPath as Path  FROM ProcessOps WHERE ClientId='{client}' " 
    _sql += f"AND Date >= '{_ini_date}' AND Date <= '{_end_date}' "
    _sql += f"AND DateTime >='{_ini_dttm}' AND DateTime <='{_end_dttm}' "
    _sql += _sqlhash
    _sql += _sqlfile    
    _sql += "GROUP BY Muid, LoggedUser, Filename, Md5, Path "
    _children = get_sql_query(_sql)
    
    return pd.concat([ _parents, _children ], ignore_index=True)

'''
bricks: la factoria de bricks
data: los datos obtenidos en ejecuciones anteriores
show: si es necesario dibujar el brick
layout: layout para renderizado
fixedargs: sin usar (no hay seleccion del usuario)
provides: key del scope actualizado con la seleccion 
client: clientid (o lista de client ids)
md5: md5 de fichero (o lista de md5s)
date: limit date for analysis period
days: number of days for analysis period

return: dataframe con urls a las que se han conectado esos md5
'''
def _fnc_processops_4_md5s(bricks, data, show, layout, fixedargs, provides, consumes, client, md5, date, days):
    _result = data
    
    # evaluate if data not available
    if _result is None:         
        _result = _sql_query_client_period_to_processops(client=client, md5s=md5, period=TimePeriod(to_date=date, num_days=int(days)))

    # return evaluated data
    return _result

'''
bricks: la factoria de bricks
data: los datos obtenidos en ejecuciones anteriores
show: si es necesario dibujar el brick
layout: layout para renderizado
fixedargs: sin usar (no hay seleccion del usuario)
provides: key del scope actualizado con la seleccion 
client: clientid (o lista de client ids)
filename: nombre de fichero (o lista de nombres)
date: limit date for analysis period
days: number of days for analysis period

return: dataframe con urls a las que se han conectado esos md5
'''
def _fnc_processops_4_filenames(bricks, data, show, layout, fixedargs, provides, consumes, client, filename, date, days):
    _result = data
    
    # evaluate if data not available
    if _result is None:        
        _result = _sql_query_client_period_to_processops(client=client, filenames=filename, period=TimePeriod(to_date=date, num_days=int(days)))

    # return evaluated data
    return _result

'''
bricks: la factoria de bricks
data: los datos obtenidos en ejecuciones anteriores
show: si es necesario dibujar el brick
layout: layout para renderizado
fixedargs: sin usar (no hay seleccion del usuario)
provides: key del scope actualizado con la seleccion 
client: clientid (o lista de client ids)
filename: nombre de fichero (o lista de nombres)
date: limit date for analysis period
days: number of days for analysis period

return: dataframe con urls a las que se han conectado esos md5
'''
def _fnc_filenames_md5s_by_filenames(bricks, data, show, layout, fixedargs, provides, consumes, client, filename, date, days):
    _result = data
    
    # evaluate if data not available
    if _result is None: 
        _process4md5 = bricks.run(None, _fnc_processops_4_filenames, False, client=client, filename=filename, date=date, days=days)
        _columns = ['Muid', 'Md5', 'Filename', 'Path']

        if len(_process4md5) > 0:
            _result = reports.group(input=_process4md5,  by=_columns)
            _result = _result.loc[_result['Md5'] != '00000000000000000000000000000000', :]
        else:
            _result = pd.DataFrame(columns=_columns)
        
    # return evaluated data
    return _result

def _sql_query_client_connections_to_url(client, urls, period):
    _urls = [ urls ] if not isinstance(urls, list) else urls
    
    _ini_date = period.ini("%Y/%m/%d")
    _ini_dttm = period.ini("%Y/%m/%d %H:%M:%S")
    _end_date = period.end("%Y/%m/%d")
    _end_dttm = period.end("%Y/%m/%d %H:%M:%S")
    
    if len(_urls) > 0:        
        from TH.Core.adhoc import get_sql_query

        _sql = f"SELECT * FROM NetworkOps WHERE ClientId='{client}' "
        _sql += f"AND Date >= '{_ini_date}' AND Date <= '{_end_date}'"
        _sql += f"AND DateTime >='{_ini_dttm}' AND DateTime <='{_end_dttm}'"
        _sql += 'AND ('
        for _url in _urls:
            _sql += f"lower(Hostname) like '%{_url.lower()}%' OR "
        _sql = _sql.removesuffix(' OR ') + ")"
        
        _df = get_sql_query(_sql)     
        if not _df.empty:
            _df.rename(columns = {'ParentPath':'Path', 'ParentFilename':'Filename', 'ParentPid':'Pid', 'ParentMd5':'Md5'}, inplace = True)
        return _df        
    else:
        return pd.DataFrame(columns=['Hostname', 'RemoteIp', 'RemotePort', 'Muid', 'Filename', 'Path', 'Md5'])
        
'''
bricks: la factoria de bricks
data: los datos obtenidos en ejecuciones anteriores
show: si es necesario dibujar el brick
layout: layout para renderizado
fixedargs: sin usar (no hay seleccion del usuario)
provides: key del scope actualizado con la seleccion 
client: clientid (o lista de client ids)
hostname: url (o lista de urls)
date: limit date for analysis period
days: number of days for analysis period

return: dataframe con las conexiones a una url  
'''
def _fnc_connections_4_url(bricks, data, show, layout, fixedargs, provides, consumes, client, hostname, date, days):
    _result = data
    
    # evaluate if data not available
    if _result is None: 
        _result = _sql_query_client_connections_to_url(client, hostname, TimePeriod(to_date=date, num_days=int(days)))

    # return evaluated data
    return _result

'''
bricks: la factoria de bricks
data: los datos obtenidos en ejecuciones anteriores
show: si es necesario dibujar el brick
layout: layout para renderizado
provides: key del scope actualizado con la seleccion 
client: clientid (o lista de client ids)
url: url (o lista de urls)
date: limit date for analysis period
days: number of days for analysis period

return: dataframe con paths, nombres y md5 de los ficheros
'''
def _fnc_file_4_url(bricks, data, show, layout, fixedargs, provides, consumes, client, hostname, date, days):
    _result = data
    
    # evaluate if data not available
    if _result is None: 
        _conx4url = bricks.run(None, _fnc_connections_4_url, False, client=client, hostname=hostname, date=date, days=days)
        _result = reports.group(input=_conx4url, by=['Hostname', 'RemoteIp', 'Muid', 'Filename', 'Path', 'Md5'], name="Count")

    # return evaluated data
    return _result

'''
    NbRowConnections is used by:
    - BrickUrl4Filename
    - BrickUrl4Md5
    - BrickMachine4Url
    - BrickUser4Url
    - BrickFilename4Url
'''
class NbRowConnections(NbComponent):
    def __init__(self):
        super().__init__('connections')
    
    def declare(self, target, client, date, days, fixedargs=None, provides=None, consumes=None):
        row = self.data_from_consumes(None, consumes)
        
        def _sql_query_row_connections(hostname, remoteip, muid, loggeduser, filename, md5, client, period): 
            from TH.Core.adhoc import get_sql_query

            _ini_date = period.ini("%Y/%m/%d")
            _ini_dttm = period.ini("%Y/%m/%d %H:%M:%S")
            _end_date = period.end("%Y/%m/%d")
            _end_dttm = period.end("%Y/%m/%d %H:%M:%S")    

            _sql = f"SELECT "
            _sql += "DateTime, ClientId, LoggedUser, Muid, Hostname, RemoteIp, RemotePort, ParentPid as Pid, ParentFilename as Filename, ParentMd5 as Md5, ParentPath as Path "
            _sql += f"from NetworkOps WHERE ClientId='{client}' "
            _sql += f"AND Date >= '{_ini_date}' AND Date <= '{_end_date}' "
            _sql += f"AND DateTime >='{_ini_dttm}' AND DateTime <='{_end_dttm}' "
            
            if muid is not None:
                _sql += f"AND lower(Muid) = '{muid.lower()}' "
            
            if loggeduser is not None:
                _sql += f"AND lower(LoggedUser) = '{loggeduser.lower()}' "
            
            if hostname is not None:
                _sql += f"AND lower(Hostname) like '%{hostname.lower()}%' "
            if hostname is None and remoteip is not None:
                _sql += f"AND RemoteIp = '{remoteip}' " 
            
            if filename is not None and md5 is not None:
                _sql += f"AND (lower(ParentFilename) = '{filename.lower()}' OR lower(ParentMd5) = '{md5.lower()}') "
            else:
                if filename is not None:
                    _sql += f"AND lower(ParentFilename) = '{filename.lower()}' "
                if md5 is not None:
                    _sql += f"AND lower(ParentMd5) = '{md5.lower()}' "
            
            _df = get_sql_query(_sql)
            if _df.empty:
                _df = pd.DataFrame(columns=[ 'DateTime', 'ClientId', 'LoggedUser', 'Muid', 'Hostname', 'RemoteIp', 'RemotePort', 'Pid', 'Filename', 'Md5', 'Path' ])
            return  _df        
        
        # declare the component widget function
        def _fnc_component(nb):
            _row = row
            
            if isinstance(_row, ScopeKey):
                _row = self.scope.get(_row)
            
            if _row is not None and _row['rowcount'] > 0:
                import uuid
                
                _hostname = _row['hostname'][0] if 'hostname' in _row else None
                _remoteip = _row['remoteip'][0] if 'remoteip' in _row else None

                _muid = None
                _user = None
                _filename = None
                _md5 = None
                
                if target == '4MD5':
                    _md5 = _row['md5'][0] if 'md5' in _row else None
                    
                if target == '4FILE':
                    _filename = _row['filename'][0] if 'filename' in _row else None
                    _md5 = _row['md5'][0] if 'md5' in _row else None
                
                if target == '4MUID':
                    _muid = _row['muid'][0] if 'muid' in _row else None
                
                if target == '4USER':
                    _user = _row['loggeduser'][0] if 'loggeduser' in _row else None           
                
                _gridopt = {
                    'groupcolumns': [{
                        'headerName': 'Source',
                        'children': [
                            { 'field': 'DateTime' },
                            { 'field': 'LoggedUser' }, 
                            { 'field': 'Muid', 'columnGroupShow': 'open'  },                            
                            { 'field': 'Pid', 'columnGroupShow': 'open' }
                        ]
                    }, {
                        'headerName': 'Host',
                        'children': [
                            { 'field': 'Hostname' },
                            { 'field': 'RemoteIp', 'columnGroupShow': 'open' },
                            { 'field': 'RemotePort', 'columnGroupShow': 'open' }
                        ]            
                    }, {
                        'headerName': 'File',
                        'children': [
                            { 'field': 'Filename' },
                            { 'field': 'Md5', 'columnGroupShow': 'open' },
                            { 'field': 'Path', 'columnGroupShow': 'open' },  
                        ]
                    }]
                } 
                
                _domloadid = '_loadid_' + str(uuid.uuid4())
                display(HTML(f'''
                    <div id="{_domloadid}" style="display: flex; height:100px;">
                        <div class="spinner spinner" style="margin: 50px auto; font-size: 2rem"><div>
                    </div>'''))

                dashboard = nbDashboard(False, 'EN', layout=self)

                _data = _sql_query_row_connections(
                    _hostname, 
                    _remoteip, 
                    _muid, 
                    _user, 
                    _filename, 
                    _md5, 
                    client, TimePeriod(to_date=date, num_days=int(days)))
                
                if target == '4MD5':
                    _target = f"For MD5: <b>'{_md5}'</b>"
                if target == '4FILE':
                    _target = f"For file: <b>'{_filename}'</b> with MD5: <b>'{_md5}'</b>"
                if target == '4MUID':
                    _target = f"For muid: <b>'{_muid}'</b>"
                if target == '4USER':
                    _target = f"For logged user: <b>'{_user}'</b>"

                _html = f'''
                <h2>
                    Connections to <b>'{_hostname if _hostname else ''}'</b> ({_remoteip})<br/>
                    <span style="font-size: 60%">{_target}</span>
                </h2>
                '''                
                
                dashboard.HTML(_html)
                dashboard.grid(_data, fixedargs=fixedargs, options=_gridopt, provides=provides)
                dashboard.run()
                
                display(HTML(f'''
                    <script>
                        document.getElementById('{_domloadid}').parentNode.style.display = 'none';
                    </script>'''))                                 
                
        # this is an attribute for nbLayout, so it can access to its members
        self._widget = ScopeWidget(_fnc_component, self, provides, consumes)
        self.append(self._widget, 'widget')

_ = NbRowConnections()

################################
# BRICKS CLASSES               #
################################

class BrickFilename4Md5(BrickClass):
    def __init__(self, bricks=None):
        super().__init__(
            bricks = bricks,
            label = 'File names for MD5',
            desc = 'Filenames found for the given MD5 in the client',
            long = self._long,
            tags = [ 'Analysis/Filename' ],
            args = { 
                'client': { 'editable': False, 'propagate': True },
                'md5':  { 'editable': True, 'propagate': False },
                'date': { 'editable': False, 'propagate': True },
                'days': { 'editable': False, 'propagate': True }
            },
            mode = 'data')
    
    def _long(self, args):
        if 'md5' in args:
            _md5 = _list_remove(['00000000000000000000000000000000', ''], args['md5'])
        
        if len(_md5) == 1:
            return f'''Returns a list of file names in the client machines when MD5 is {_md5[0]}'''
        if len(_md5) > 1:
            return f'''Returns a list of file names in the client machines when MD5 is any of {(",".join(_md5))}'''
            
        return None
    
    def _eval(self, client, md5, date, days): 
        _process4md5 = bricks.run(None, _fnc_processops_4_md5s, False, client=client, md5=md5, date=date, days=days)
        
        _columns = ['Muid', 'Md5', 'Filename', 'Path']
        if _process4md5.empty:
            _result = pd.DataFrame(columns=_columns)
        else:
            _result = _process4md5[_columns]
            _result = _result.loc[_result['Md5'] != '00000000000000000000000000000000', :]
            _result = _result.drop_duplicates(ignore_index=True)    

        return _result

    def _show(self, _result, layout, fixedargs, provides, client, md5, date, days):
        dashboard = nbDashboard(False, 'EN', layout=layout)
        dashboard.grid(_result, fixedargs=fixedargs, provides=provides)        
        dashboard.run() 

class BrickMachine4Md5(BrickClass):
    def __init__(self, bricks=None):
        super().__init__(
            bricks = bricks,
            label = 'Machines for MD5',
            desc = 'Returns a table with the machines in where the MD5 has been seen',
            long = self._long,
             tags = [ 'Analysis/Machine' ],
            args = { 
                'client': { 'editable': False, 'propagate': True },
                'md5':  { 'editable': True, 'propagate': False },
                'date': { 'editable': False, 'propagate': True },
                'days': { 'editable': False, 'propagate': True }            
            },
            mode = 'data')

    def _long(self, args):
        if 'md5' in args:
            _md5 = _list_remove(['00000000000000000000000000000000', ''], args['md5'])
        
        if len(_md5) == 1:
            return f'''Returns a list of machines in client when files with MD5 {_md5[0]} are found'''
        if len(_md5) > 1:
            return f'''Returns a list of machines in client when files with MD5 any of {(",".join(_md5))} are found'''
            
        return None
    
    def _eval(self, client, md5, date, days): 
        _process4md5 = bricks.run(None, _fnc_processops_4_md5s, False, client=client, md5=md5, date=date, days=days)
        
        _columns = ['Muid', 'Name', 'LoggedUser', 'Filename', 'Md5']
        if _process4md5.empty:
             _result = pd.DataFrame(columns=_columns)  
        else:
            _procc = (_process4md5[['Muid', 'LoggedUser', 'Filename', 'Md5']]).drop_duplicates(ignore_index=True) 
            _muids = _procc['Muid'].to_list()
            _names = _get_machine_names(_muids)
            _names = pd.DataFrame(_names) if len(_names) > 0 else pd.DataFrame(columns=['Muid', 'Name'])
            _result = _procc.merge(_names, how='left', on='Muid')
                
        return _result

    def _show(self, _result, layout, fixedargs, provides, client, md5, date, days):
        _columns = ['Muid', 'Name', 'LoggedUser', 'Filename', 'Md5']
        if len(_result) > 0:   
            _df = reports.group(input=_result,  by=_columns)
            _df = _df[_columns]        
        else:
            _df = pd.DataFrame(columns = _columns)
        
        dashboard = nbDashboard(False, 'EN', layout=layout)
        dashboard.grid(_df, fixedargs=fixedargs, provides=provides)        
        dashboard.run() 

class BrickUrl4Md5(BrickClass):
    def __init__(self, bricks=None):
        super().__init__(
            bricks = bricks,
            label = 'URLs for MD5',
            desc = 'Returns a list of URLs that have been connected by the MD5',
            long = self._long,
            tags = [ 'Analysis/Url' ],
            args = { 
                'client': { 'editable': False, 'propagate': True },
                'md5':  { 'editable': True, 'propagate': False },
                'date': { 'editable': False, 'propagate': True },
                'days': { 'editable': False, 'propagate': True }
            },
            mode = 'data')

    def _long(self, args):
        if 'md5' in args:
            _md5 = _list_remove(['00000000000000000000000000000000', ''], args['md5'])
        
        if len(_md5) == 1:
            return f'''Returns a list of URLS connected by files with MD5 {_md5[0]}'''
        if len(_md5) > 1:
            return f'''Returns a list of URLS connected by files with MD5 any of {(",".join(_md5))}'''
            
        return None
    
    def _sql_query_client_md5_connections(self, client, md5s, period):
        _md5s = [ md5s ] if not isinstance(md5s, list) else md5s

        _ini_date = period.ini("%Y/%m/%d")
        _ini_dttm = period.ini("%Y/%m/%d %H:%M:%S")
        _end_date = period.end("%Y/%m/%d")
        _end_dttm = period.end("%Y/%m/%d %H:%M:%S")

        if len(_md5s) > 0:        
            from TH.Core.adhoc import get_sql_query

            _sql = f"SELECT Muid, Hostname, RemoteIp, RemotePort, ParentMd5, ParentPath, ParentFilename FROM NetworkOps WHERE ClientId='{client}' "
            _sql += f"AND Date >= '{_ini_date}' AND Date <= '{_end_date}'"
            _sql += f"AND DateTime >='{_ini_dttm}' AND DateTime <='{_end_dttm}'"
            _sql += 'AND ('
            for _md5 in _md5s:
                _sql += f"lower(ParentMd5) = '{_md5.lower()}' OR "
            _sql = _sql.removesuffix(' OR ') + ") GROUP BY Muid, Hostname, RemoteIp, RemotePort, ParentMd5, ParentPath, ParentFilename"

            return get_sql_query(_sql)        
        else:
            return pd.DataFrame()

    def _eval(self, client, md5, date, days): 
        return self._sql_query_client_md5_connections(client, md5, TimePeriod(to_date=date, num_days=int(days)))
    
    def _show(self, _result, layout, fixedargs, provides, client, md5, date, days): 
        _columns = [ 'Hostname', 'RemoteIp', 'RemotePort', 'Muid', 'ParentMd5', 'ParentPath', 'ParentFilename' ]
        if _result.size > 0:
            _df = _result
        else:
            _df = pd.DataFrame(columns = _columns)
        _df.rename(columns = {'ParentMd5':'Md5', 'ParentPath': 'Path', 'ParentFilename': 'Filename'}, inplace = True)

        _gridopt = {
            'singlerow': True,             
            'groupcolumns': [{
                'headerName': 'Target',
                'children': [
                    { 'field': 'Hostname' },
                    { 'field': 'RemoteIp', 'columnGroupShow': 'open' },
                    { 'field': 'RemotePort', 'columnGroupShow': 'open' },
                ]            
            }, {
                'headerName': 'Source',
                'children': [
                    { 'field': 'Muid' },
                    { 'field': 'Md5' },
                    { 'field': 'Filename', 'columnGroupShow': 'open' },
                    { 'field': 'Path', 'columnGroupShow': 'open' },              
                ]
            }]
        }
                
        dashboard = nbDashboard(False, 'EN', layout=layout)
        dashboard.grid(_df, fixedargs=fixedargs, options=_gridopt, provides='selected-row')  
        dashboard.connections('4MD5', client, date, days, fixedargs=fixedargs, provides=provides, consumes='selected-row')
        dashboard.run()  

class BrickMachine4Filename(BrickClass):
    def __init__(self, bricks=None):
        super().__init__(
            bricks = bricks,
            label = 'Machines for file name',
            desc = 'Returns a table with the machines in where the filename has been seen',
            long = self._long,
            tags = [ 'Analysis/Machine' ],
            args = { 
                'client': { 'editable': False, 'propagate': True },
                'filename':  { 'editable': True, 'propagate': False },
                'date': { 'editable': False, 'propagate': True },
                'days': { 'editable': False, 'propagate': True }
            },
            mode = 'data')
        
    def _long(self, args):
        if 'filename' in args:
            _filename = _list_remove([''], args['filename'])
        
        if len(_filename) == 1:
            return f'''Returns a list of machines with file names that contain {_filename[0]}'''
        if len(_filename) > 1:
            return f'''Returns a list of machines with file names that contain any of {(",".join(_filename))}'''
            
        return None
    
    def _eval(self, client, filename, date, days): 
        _process4md5 = bricks.run(None, _fnc_filenames_md5s_by_filenames, False, client=client, filename=filename, date=date, days=days)
        
        _columns = ['Muid', 'Name', 'Filename', 'Md5', 'Path']
        if _process4md5.empty:
            _result = pd.DataFrame(columns=_columns)   
        else:
            _procc = (_process4md5[['Muid', 'Filename', 'Md5', 'Path']]).drop_duplicates(ignore_index=True) 
            _muids = _procc['Muid'].to_list()
            _names = _get_machine_names(_muids)
            _names = pd.DataFrame(_names) if len(_names) > 0 else pd.DataFrame(columns=['Muid', 'Name'])
            _result = _procc.merge(_names, how='left', on='Muid')
        
        return _result
    
    def _show(self, _result, layout, fixedargs, provides, client, filename, date, days): 
        _gridopt = {
            'groupcolumns': [{
                'headerName': 'Machine',
                'children': [
                    { 'field': 'Muid' },
                    { 'field': 'Name' }
                ]            
            }, {
                'headerName': 'File',
                'children': [
                    { 'field': 'Filename' },
                    { 'field': 'Md5', 'columnGroupShow': 'open' },
                    { 'field': 'Path', 'columnGroupShow': 'open' },              
                ]
            }]
        }
        
        _columns = ['Muid', 'Name', 'Filename', 'Md5', 'Path']
        if len(_result) > 0:            
            _df = _result            
        else:
            _df = pd.DataFrame(columns = _columns)

        dashboard = nbDashboard(False, 'EN', layout=layout)
        dashboard.grid(_df, fixedargs=fixedargs, options=_gridopt, provides=provides)        
        dashboard.run()  

class BrickMd54Filename(BrickClass):
    def __init__(self, bricks=None):
        super().__init__(
            bricks = bricks,
            label = 'MD5s for file name',
            desc = 'Returns all MD5s found for the given file name in the client',
            long = self._long,
            tags = [ 'Analysis/Md5' ],
            args = { 
                'client': { 'editable': False, 'propagate': True },
                'filename':  { 'editable': True, 'propagate': False },
                'date': { 'editable': False, 'propagate': True },
                'days': { 'editable': False, 'propagate': True }
            },
            mode = 'data')

    def _long(self, args):
        if 'filename' in args:
            _filename = _list_remove([''], args['filename'])
        
        if len(_filename) == 1:
            return f'''Returns a list of MD5 for file names that contain {_filename[0]}'''
        if len(_filename) > 1:
            return f'''Returns a list of MD5 for file names that contain any of {(",".join(_filename))}'''
            
        return None
        
    def _eval(self, client, filename, date, days):         
        _filename4md5s = bricks.run(None, _fnc_filenames_md5s_by_filenames, False, client=client, filename=filename, date=date, days=days)     

        _columns = ['Muid', 'Md5', 'Filename', 'Path']
        if _filename4md5s.empty:
            _result = pd.DataFrame(columns=_columns)
        else:
            _result = (_filename4md5s[_columns]).drop_duplicates(ignore_index=True)

        return _result
    
    def _show(self, _result, layout, fixedargs, provides, client, filename, date, days): 
        dashboard = nbDashboard(False, 'EN', layout=layout)
        dashboard.grid(_result, fixedargs=fixedargs, provides=provides)        
        dashboard.run()  

class BrickUrl4Filename(BrickClass):
    def __init__(self, bricks=None):
        super().__init__(
            bricks = bricks,
            label = 'URLs for file name',
            desc = 'Returns a list of URLS that have been connected by the file name',
            long = self._long,
            tags = [ 'Analysis/Url' ],
            args = { 
                'client': { 'editable': False, 'propagate': True },
                'filename':  { 'editable': True, 'propagate': False },
                'date': { 'editable': False, 'propagate': True },
                'days': { 'editable': False, 'propagate': True }
            },
            mode = 'data')

    def _long(self, args):
        if 'filename' in args:
            _filename = _list_remove([''], args['filename'])
        
        if len(_filename) == 1:
            return f'''Returns a list of connected URLs for file names that contain {_filename[0]}'''
        if len(_filename) > 1:
            return f'''Returns a list of connected URLs for file names that contain any of {(",".join(_filename))}'''
            
        return None
    
    def _sql_query_client_filename_connections(self, client, files, period):
        _files = [ files ] if not isinstance(files, list) else files

        _ini_date = period.ini("%Y/%m/%d")
        _ini_dttm = period.ini("%Y/%m/%d %H:%M:%S")
        _end_date = period.end("%Y/%m/%d")
        _end_dttm = period.end("%Y/%m/%d %H:%M:%S")

        if len(_files) > 0:        
            from TH.Core.adhoc import get_sql_query

            _sql = f"SELECT Hostname, RemoteIp, Muid, ParentMd5, ParentPath, ParentFilename FROM NetworkOps WHERE ClientId='{client}' "
            _sql += f"AND Date >= '{_ini_date}' AND Date <= '{_end_date}' "
            _sql += f"AND DateTime >='{_ini_dttm}' AND DateTime <='{_end_dttm}' "
            _sql += 'AND ('
            for _file in _files:
                _sql += f"lower(ParentFilename) like '%{_file.lower()}%' OR "
            _sql = _sql.removesuffix(' OR ') + ") GROUP BY Hostname, RemoteIp, Muid, ParentMd5, ParentPath, ParentFilename "

            return get_sql_query(_sql)   
        else:
            return pd.DataFrame()
                
    def _eval(self, client, filename, date, days): 
         return self._sql_query_client_filename_connections(client, filename, TimePeriod(to_date=date, num_days=int(days)))
    
    def _show(self, _result, layout, fixedargs, provides, client, filename, date, days): 
        _columns = [ 'Hostname', 'RemoteIp', 'Muid', 'ParentMd5', 'ParentPath', 'ParentFilename' ]
        if _result.size > 0:
            _df = _result
        else:
            _df = pd.DataFrame(columns = _columns)
        _df.rename(columns = {'ParentMd5':'Md5', 'ParentPath': 'Path', 'ParentFilename': 'Filename'}, inplace = True)
        
        _gridopt = {
            'singlerow': True, 
            'groupcolumns': [{
                'headerName': 'Host',
                'children': [
                    { 'field': 'Hostname' },
                    { 'field': 'RemoteIp', 'columnGroupShow': 'open' },
                ]            
            }, {
                'headerName': 'Source',
                'children': [
                    { 'field': 'Muid' },
                    { 'field': 'Filename' },
                    { 'field': 'Md5', 'columnGroupShow': 'open' },
                    { 'field': 'Path', 'columnGroupShow': 'open' },              
                ]
            }]
        }        
                    
        dashboard = nbDashboard(False, 'EN', layout=layout)
        dashboard.grid(_df, fixedargs=fixedargs, options=_gridopt, provides='selected-row')    
        dashboard.connections('4FILE', client, date, days, fixedargs=fixedargs, provides=provides, consumes='selected-row')
        dashboard.run()       

class BrickMachine4Url(BrickClass):
    def __init__(self, bricks=None):
        super().__init__(
            bricks = bricks,
            label = 'Machines for URL',
            desc = 'Returns a table with the machines with conections to the URL',
            long = self._long,
            tags = [ 'Analysis/Machine' ],
            args = { 
                'client': { 'editable': False, 'propagate': True },
                'hostname':  { 'editable': True, 'propagate': False },
                'date': { 'editable': False, 'propagate': True },
                'days': { 'editable': False, 'propagate': True }
            },
            mode = 'data')

    def _long(self, args):
        if 'hostname' in args:
            _hostname = _list_remove([''], args['hostname'])
        
        if len(_hostname) == 1:
            return f'''Returns a list of machines with connections to {_hostname[0]}'''
        if len(_hostname) > 1:
            return f'''Returns a list of machines with connections to any of {(",".join(_hostname))}'''
            
        return None;        
        
    def _eval(self, client, hostname, date, days): 
        _conx4url = bricks.run(None, _fnc_connections_4_url, False, client=client, hostname=hostname, date=date, days=days)
        _muids = _conx4url['Muid'].tolist()    # obtain the muids from the conections dataframe
        _muids = list(dict.fromkeys(_muids))   # remove duplicates
        _columns = ['Muid', 'Name', 'Hostname', 'RemoteIp']
        if len(_muids) > 0:
            _conx = (_conx4url[['Muid', 'Hostname', 'RemoteIp']]).drop_duplicates(ignore_index=True) 
            _muids = _conx['Muid'].to_list()
            _names = _get_machine_names(_muids)           
            _names = pd.DataFrame(_names) if len(_names) > 0 else pd.DataFrame(columns=['Muid', 'Name'])
            _result = _conx.merge(_names, how='left', on='Muid')
        else:
            _result = pd.DataFrame(columns=_columns)
        return _result
    
    def _show(self, _result, layout, fixedargs, provides, client, hostname, date, days): 
        _gridopt = {
            'groupcolumns': [{
                'headerName': 'Source machine',
                'children': [
                    { 'field': 'Muid' },
                    { 'field': 'Name' }
                ]
            }, {
                'headerName': 'Destination Host',
                'children': [
                    { 'field': 'Hostname' },
                    { 'field': 'RemoteIp', 'columnGroupShow': 'open' },
                    { 'field': 'RemotePort', 'columnGroupShow': 'open' },
                ]            
            }]
        }    
        
        dashboard = nbDashboard(False, 'EN', layout=layout)
        dashboard.grid(_result, fixedargs=fixedargs, options=_gridopt, provides='selected-row')   
        dashboard.connections('4MUID', client, date, days, fixedargs=fixedargs, provides=provides, consumes='selected-row')
        dashboard.run()      

class BrickUser4Url(BrickClass):
    def __init__(self, bricks=None):
        super().__init__(
            bricks = bricks,
            label = 'Users for URL',
            desc = 'Returns a table of users with connections to the URL',
            long = self._long,
            tags = [ 'Analysis/User' ],
            args = { 
                'client': { 'editable': False, 'propagate': True },
                'hostname':  { 'editable': True, 'propagate': False },
                'date': { 'editable': False, 'propagate': True },
                'days': { 'editable': False, 'propagate': True }
            },
            mode = 'data')

    def _long(self, args):
        if 'hostname' in args:
            _hostname = _list_remove([''], args['hostname'])
        
        if len(_hostname) == 1:
            return f'''Returns a list of users with connections to {_hostname[0]}'''
        if len(_hostname) > 1:
            return f'''Returns a list of users with connections to any of {(",".join(_hostname))}'''
            
        return None          
        
    def _eval(self, client, hostname, date, days): 
        _conx4url = bricks.run(None, _fnc_connections_4_url, False, client=client, hostname=hostname, date=date, days=days)
        _columns = ['Muid', 'LoggedUser', 'Hostname', 'RemoteIp']
        _result = (_conx4url[_columns]).drop_duplicates(ignore_index=True);
        return _result

    def _show(self, _result, layout, fixedargs, provides, client, hostname, date, days):
        _gridopt = {
            'groupcolumns': [{
                'headerName': 'User',
                'children': [
                    { 'field': 'Muid' },
                    { 'field': 'LoggedUser' }
                ]
            }, {
                'headerName': 'Destination Host',
                'children': [
                    { 'field': 'Hostname' },
                    { 'field': 'RemoteIp', 'columnGroupShow': 'open' },
                ]            
            }]
        }    
                
        dashboard = nbDashboard(False, 'EN', layout=layout)
        dashboard.grid(_result, fixedargs=fixedargs, options=_gridopt, provides='selected-row')    
        dashboard.connections('4USER', client, date, days, fixedargs=fixedargs, provides=provides, consumes='selected-row')
        dashboard.run()      

class BrickFilename4Url(BrickClass):
    def __init__(self, bricks=None):
        super().__init__(
            bricks = bricks,
            label = 'File names for URL',
            desc = 'Returns a table of users with connections to the URL',
            long = self._long,
            tags = [ 'Analysis/Filename' ],
            args = { 
                'client': { 'editable': False, 'propagate': True },
                'hostname':  { 'editable': True, 'propagate': False },
                'date': { 'editable': False, 'propagate': True },
                'days': { 'editable': False, 'propagate': True }
            },
            mode = 'data')

    def _long(self, args):
        if 'hostname' in args:
            _hostname = _list_remove([''], args['hostname'])
        
        if len(_hostname) == 1:
            return f'''Returns a list of file names with connections to {_hostname[0]}'''
        if len(_hostname) > 1:
            return f'''Returns a list of file names with connections to any of {(",".join(_hostname))}'''
            
        return None;            
        
    def _eval(self, client, hostname, date, days): 
        _files4url = bricks.run(None, _fnc_file_4_url, False, client=client, hostname=hostname, date=date, days=days)
        _columns = ['Filename', 'Md5', 'Path', 'Muid', 'Hostname', 'RemoteIp']
        _result = (_files4url[_columns]).drop_duplicates(ignore_index=True); 
        return _result

    def _show(self, _result, layout, fixedargs, provides, client, hostname, date, days):
        _gridopt = {
            'groupcolumns': [{
                'headerName': 'File',
                'children': [
                    { 'field': 'Muid' },
                    { 'field': 'Filename' },
                    { 'field': 'Md5', 'columnGroupShow': 'open' },
                    { 'field': 'Path', 'columnGroupShow': 'open' },
                ]
            }, {
                'headerName': 'Destination Host',
                'children': [
                    { 'field': 'Hostname' },
                    { 'field': 'RemoteIp', 'columnGroupShow': 'open' },
                ]            
            }]
        }    
        
        dashboard = nbDashboard(False, 'EN', layout=layout)
        dashboard.grid(_result, fixedargs=fixedargs, options=_gridopt, provides='selected-row')    
        dashboard.connections('4FILE', client, date, days, fixedargs=fixedargs, provides=provides, consumes='selected-row')
        dashboard.run()  

class BrickMd54Client(BrickClass):
    def __init__(self, bricks=None):
        super().__init__(
            bricks = bricks,
            label = 'MD5 activity in a client',
            desc = 'Provides a general view of the MD5 activity in the client machines',
            long = self._long,
            tags = [ 'Analysis/Md5' ],
            args = { 
                'client': { 'editable': True, 'propagate': True },
                'md5': { 'editable': True, 'propagate': False },
                'date': { 'editable': True, 'propagate': True },
                'days': { 'editable': True, 'propagate': True }
            },
            mode = 'data')

    def _fnc_evaluate_md5_in_client(self, client, md5, period):
        _md5s = [ md5 ] if not isinstance(md5, list) else md5
        if len(_md5s) == 0:
            return pd.DataFrame()
        else:
            from TH.Core.adhoc import get_sql_query  
            _md5list = ','.join(["\'" + str(i).lower() + "\'" for i in _md5s])

            _ini_date = period.ini("%Y/%m/%d")
            _ini_dttm = period.ini("%Y/%m/%d %H:%M:%S")
            _end_date = period.end("%Y/%m/%d")
            _end_dttm = period.end("%Y/%m/%d %H:%M:%S")

            _sql = "SELECT  DateTime, Muid, LoggedUser, ParentFilename as FileName, ParentMd5 as Md5, ParentPath as Path  FROM ProcessOps "
            _sql += f"WHERE ClientId='{client}' "        
            _sql += f"AND Date >= '{_ini_date}' AND Date <= '{_end_date}' "
            _sql += f"AND DateTime >='{_ini_dttm}' AND DateTime <='{_end_dttm}' "
            _sql += "AND LoggedUser NOT LIKE 'NT_AUTHORITY%%' "
            _sql += "AND LoggedUser NOT LIKE 'NT AUTHORITY%%' "
            _sql += f"AND lower(Md5) in ({_md5list}) "
            _parents = get_sql_query(_sql)

            _sql = "SELECT  DateTime, Muid, LoggedUser, ChildFilename as FileName, ChildMd5 as Md5, ChildPath as Path  FROM ProcessOps "
            _sql += f"WHERE ClientId='{client}' "        
            _sql += f"AND Date >= '{_ini_date}' AND Date <= '{_end_date}' "
            _sql += f"AND DateTime >='{_ini_dttm}' AND DateTime <='{_end_dttm}' "
            _sql += "AND LoggedUser NOT LIKE 'NT_AUTHORITY%%' "
            _sql += "AND LoggedUser NOT LIKE 'NT AUTHORITY%%' "
            _sql += f"AND lower(Md5) in ({_md5list}) "
            _children = get_sql_query(_sql)

            _df = pd.concat([ _parents, _children ], ignore_index=True)

            # Calcular primera y última aparición y contador de apariciones
            if _df.size > 0:
                _df = _df.groupby(by=['Muid', 'LoggedUser', 'FileName', 'Path', 'Md5']).agg({'Muid': 'count', 'DateTime': [ np.min, np.max ] }).droplevel(0, axis=1).reset_index()
                _df.columns = [ 'Muid', 'LoggedUser', 'FileName', 'Path', 'Md5', 'Count', 'FirstSeen', 'LastSeen' ]
                _df = _df[['Muid', 'LoggedUser', 'FirstSeen', 'LastSeen', 'Count', 'FileName', 'Md5', 'Path' ]]

            return _df;        

    def _long(self, args):
        if 'md5' in args:
            _md5 = _list_remove(['00000000000000000000000000000000', ''], args['md5'])
        
        if len(_md5) == 1:
            return f'''Returns a general view of the file with MD5 {_md5[0]} activity in all client machines'''
        if len(_md5) > 1:
            return f'''Returns a general view of the files with MD5 any of {(",".join(_md5))} activity in all client machines'''
            
        return None
    
    def _eval(self, client, md5, date, days): 
         return self._fnc_evaluate_md5_in_client(client, md5, TimePeriod(to_date=date, num_days=int(days)))
    
    def _show(self, _result, layout, fixedargs, provides, client, md5, date, days): 
        _gridopt = {
            'groupcolumns': [{
                'headerName': 'Machine',
                'children': [
                    { 'field': 'Muid' },
                    { 'field': 'LoggedUser' },
                ]            
            }, {
                'headerName': 'Seen',
                'children': [
                    { 'field': 'FirstSeen' },
                    { 'field': 'LastSeen' },
                    { 'field': 'Count', 'columnGroupShow': 'open' }
                ]
            }, {
                'headerName': 'File',
                'children': [
                    { 'field': 'FileName' },
                    { 'field': 'Md5', 'columnGroupShow': 'open' },
                    { 'field': 'Path', 'columnGroupShow': 'open' }
                ]
            }]
        }  
            
        _columns = [ 'Muid', 'LoggedUser', 'FirstSeen', 'LastSeen', 'Count', 'FileName', 'Md5', 'Path' ]
        if _result.size > 0:
            _df = _result
        else:
            _df = pd.DataFrame(columns = _columns)
        
        dashboard = nbDashboard(False, 'EN', layout=layout)
        dashboard.grid(_df, fixedargs=fixedargs, options=_gridopt, provides=provides)   
        dashboard.run()        

class BrickMd5Info(BrickClass):
    def __init__(self, bricks=None):
        super().__init__(
            bricks = bricks,
            label = 'MD5 information',
            desc = 'Returns a non-interactive table with detailed information of file with given MD5',
            long = self._long,
            tags = [ 'Information/Md5' ],
            args = {
                'md5': { 'editable': True, 'propagate': False },
                'date': { 'editable': False, 'propagate': False },
                'days': { 'editable': False, 'propagate': False }
            },
            mode = 'info'
        )

    def _long(self, args):
        if 'md5' in args:
            _md5 = _list_remove(['00000000000000000000000000000000', ''], args['md5'])
        
        if len(_md5) == 1:
            return f'''Returns information for the file with MD5 {_md5[0]}'''
        if len(_md5) > 1:
            return f'''Returns information for the file with MD5 any of {(",".join(_md5))}'''
            
        return None;     
        
    def _fnc_md5_info(self, md5_list, date, days):
        from TH.Core import OrionRequest 
        response_keys = [
            'mD5',
            'shA256',
            'category',
            'categoryType',
            'size',
            'formatType',
            'signer',
            'serialNumber',
            'globalGlaukaPrevalence',
            'firstSeenAsDateTime',
            'globalLastSeen',
            'hasValidDigitalSignature',
        ]
        version_info_keys = [
            'comments',
            'company',
            'description',
            'fileVersion',
            'internalName',
            'language',
            'legalCopyright',
            'originalFileName',
            'productName',
            'productVersion'
        ]
        field_update_functions = {
            'shA256': base64_to_hex,
            'category': get_category_text,
            'formatType': get_formattype_text,
            'globalLastSeen': epoch_to_utc,
            'language': hex_to_lang,
        }
        new_keys = {
            'mD5': 'MD5',
            'shA256': 'SHA256',
            'category': 'Category',
            'size': 'File Size (bytes)',
            'formatType': 'Format Type',
            'signer': 'Signer',
            'serialNumber': 'Serial Number',
            'globalGlaukaPrevalence': 'File Prevalence',
            'firstSeenAsDateTime': 'First Seen',
            'globalLastSeen': 'Last Seen',
            'hasValidDigitalSignature': 'Has Valid Signature',
            'comments': 'Comments',
            'company': 'Company Name',
            'description': 'File Description',
            'fileVersion': 'File Version',
            'internalName': 'Internal Name',
            'language': 'Language',
            'legalCopyright': 'Legal Copyright',
            'originalFileName': 'Original Filename',
            'productName': 'Product Name',
            'productVersion': 'Product Version',
        }
        req = OrionRequest()
        _df = pd.DataFrame()
        header_row = {}
        for value in new_keys.values():
            header_row.update(
                {
                    value: value
                }
            )
        series = pd.Series(header_row)
        _df = _df.append(series, ignore_index=True)
        md5_set = set(md5_list)
        for md5 in md5_set:
            api = '/forensics/md5/{md5}/sample'.format(md5=md5)
            try:
                response = req.get(api)
                response_dict = json.loads(response.text)
                version_info_dict = response_dict['versionInfo']

                dict_level1 = {k: response_dict[k] for k in response_keys}
                dict_level2 = {k: version_info_dict[k] for k in version_info_keys}
                full_dict = dict_level1
                full_dict.update(dict_level2)

                for (k, v) in field_update_functions.items():
                    if k == 'category':
                        full_dict[k] = v(full_dict[k], full_dict['categoryType'])
                    else:
                        full_dict[k] = v(full_dict[k])

                full_dict.pop('categoryType')
                new_dict = {}
                for (k, v) in new_keys.items():
                    new_dict.update(
                        {
                            v: full_dict[k]
                        }
                    )
                series = pd.Series(new_dict)
                _df = _df.append(series, ignore_index=True)
            except Exception as e:
                full_dict = {}
                for (k, v) in new_keys.items():
                    if k == 'mD5':
                        full_dict.update(
                            {
                                v: md5
                            }
                        )
                    else:
                        full_dict.update(
                            {
                                v: 'N/A'
                            }
                        )
                series = pd.Series(full_dict)
                _df = _df.append(series, ignore_index=True)
                            
        _df = _df.set_index('MD5')
        return _df.transpose()

    def _eval(self, md5, date, days):
        return self._fnc_md5_info(md5, date, days)
    
    def _show(self, _result, layout, fixedargs, provides, md5, date, days):                    
        dashboard = nbDashboard(False, 'EN', layout=layout)
        dashboard.table(_result)
        dashboard.run()   

class BrickOcurrencesPlot(BrickClass):
    def __init__(self, bricks=None):
        super().__init__(
            bricks = bricks,
            label = 'Plot ocurrences for MD5',
            desc = 'Number of machines with MD5 ocurrences per day',
            long = self._long,
            tags = [ 'Graph/Machines' ],
            args = { 
                'client': { 'editable': False, 'propagate': True },
                'md5':  { 'editable': True, 'propagate': False },
                'date': { 'editable': True, 'propagate': True },
                'days': { 'editable': True, 'propagate': True }
            },
            mode = 'info')

    def _long(self, args):
        if 'md5' in args:
            _md5 = _list_remove(['00000000000000000000000000000000', ''], args['md5'])
        
        if len(_md5) == 1:
            return f'''Plots the number of machines with events for MD5 {_md5[0]} grouped per day'''
        if len(_md5) > 1:
            return f'''Plots the number of machines with events for MD5 any of {(",".join(_md5))} grouped per day'''
            
        return None;     
        
    def _eval(self, client, md5, date, days): 
        from TH.Core.adhoc import get_sql_query

        _md5 = [ md5 ] if not isinstance(md5, list) else md5
        
        _period=TimePeriod(to_date=date, num_days=int(days))
        _ini_date = _period.ini("%Y/%m/%d")
        _ini_dttm = _period.ini("%Y/%m/%d %H:%M:%S")
        _end_date = _period.end("%Y/%m/%d")
        _end_dttm = _period.end("%Y/%m/%d %H:%M:%S")
        
        _md5list = ','.join(["\'" + str(i).lower() + "\'" for i in _md5])
        
        _sql = f"SELECT Date, COUNT(DISTINCT Muid) as MachinesCount from ProcessOps "
        _sql += f"WHERE ClientId='{client}' "
        _sql += f"AND Date >= '{_ini_date}' AND Date <= '{_end_date}' "
        _sql += f"AND DateTime >='{_ini_dttm}' AND DateTime <='{_end_dttm}' "
        _sql += f'AND (lower(ParentMd5) in ({_md5list}) or lower(ChildMd5) in ({_md5list})) '
        _sql += "GROUP BY Date"
        
        return get_sql_query(_sql)  

    def _show(self, _result, layout, fixedargs, provides, client, md5, date, days):  
        import plotly.express as px

        df = _result
        fig = px.bar(df.reset_index(), x="Date", y="MachinesCount")
        dashboard = nbDashboard(False, 'EN', layout=layout)
        dashboard.plotly_figure(fig)      
        dashboard.run() 

class NbSQLQuery(NbComponent):
    def __init__(self):
        super().__init__('sqlquery')
    
    def declare(self, client, date, days, provides=None, consumes=None):
        # declare the component widget function
        def _fnc_component(nb):
            import ipywidgets.widgets as w

            _period = TimePeriod(to_date=date, num_days=int(days))
            _ini_date = _period.ini("%Y/%m/%d")
            _ini_dttm = _period.ini("%Y/%m/%d %H:%M:%S")
            _end_date = _period.end("%Y/%m/%d")
            _end_dttm = _period.end("%Y/%m/%d %H:%M:%S")
        
            _default = ""
            _default += f" AND ClientId='{client}'"
            _default += f" AND Date >= '{_ini_date}' AND Date <= '{_end_date}'"
            _default += f" AND DateTime >='{_ini_dttm}' AND DateTime <='{_end_dttm}'"
        
            _sqlarea = w.Textarea(value=_default, layout = w.Layout(flex='1 1 auto', width='auto'))
            _sqlbutton = w.Button(description='Run query', layout=w.Layout(display='flex', flex_flow='row', align_content='flex-end', width='15%'))
            _sqlerror =  w.HTML(value='', layout=w.Layout(display='block', width='100%'))
        
            _row1 = w.Box([_sqlarea], layout = w.Layout(overflow_x='hidden', width='100%'))
            _row2 = w.Box([_sqlbutton], layout = w.Layout(display='flex', flex_flow='row', justify_content='flex-end', height='50px', width='100%'))
            _row3 =  w.Box([_sqlerror], layout = w.Layout(width='100%'))
            
            def _fnc_on_sql_click(button):
                from TH.Core.adhoc import get_sql_query

                nb.scope.set(provides, None)      # clear any previous result
                _row2.layout.display = 'none'     # hide the button during query execution
                _row3.layout.display = 'none'     # hide the error information
    
                _result = get_sql_query(_sqlarea.value)
                _dict = _result.to_dict()
                if 'status' in _dict and _dict['status'][0] == 400:
                    _sqlerror.value = ''
                    if 'message' in _dict:
                        _sqlerror.value += f'<h2>{_dict["message"][0]}</h2>'
                    if 'validationErrors' in _dict:
                        _sqlerror.value += f'<p style="padding: 3px 10px; border: 1px solid black;">{_dict["validationErrors"][0]}</p>'                       
                    _row3.layout.display = 'flex'  # show the error information
                else: # return the dataframe in the provides key
                    nb.scope.set(provides, _result)
                _row2.layout.display = 'flex'     # show the button after query execution
        
            _sqlbutton.on_click(_fnc_on_sql_click)
            display(w.VBox([_row1, _row2, _row3])) 
            
            return None

        # this is an attribute for nbLayout, so it can access to its members
        self._widget = ScopeWidget(_fnc_component, self,  provides, consumes)
        self.append(self._widget, 'widget')

_ = NbSQLQuery()

class BrickSQLQuery(BrickClass):
    def __init__(self, bricks=None):
        super().__init__(
            bricks = bricks,
            label = 'Run a SQL query',
            desc = 'Obtains the query resultset',
            long = self._long,
            tags = [ 'Generic' ],
            args = { 
                'client': { 'editable': True, 'propagate': True },
                'date': { 'editable': True, 'propagate': True },
                'days': { 'editable': True, 'propagate': True }            
            },
            mode = 'data')
    
    def _long(self, args):
        return None
    
    def _eval(self, client, date, days): 
        return None # will evaluate on show

    def _show(self, _result, layout, fixedargs, provides, client, date, days):
        import ipywidgets.widgets as w
        
        dashboard = nbDashboard(False, 'EN', layout=layout)
        dashboard.sqlquery(client, date, days, provides="sqlresult")
        dashboard.grid(ScopeKey('sqlresult'), fixedargs=fixedargs, consumes="sqlresult", provides=provides)
        dashboard.run()
    
class BrickPEDiskUpdates(BrickClass):
    def __init__(self, bricks=None):
        super().__init__(
            bricks = bricks,
            label = 'Executable file modifications',
            desc = 'Returns executable file modifications (Creation, Update, Rename, Delete) for the given MD5 and/or file name',
            long = self._long,
            tags = [ 'Analysis/Filename', 'Analysis/Md5' ],
            args = { 
                'client': { 'editable': False, 'propagate': True },
                'md5':  { 'editable': True, 'propagate': False },
                'filename':  { 'editable': True, 'propagate': False },
                'date': { 'editable': False, 'propagate': True },
                'days': { 'editable': False, 'propagate': True }
            },
            mode = 'data')
    
    def _long(self, args):
        if 'md5' in args:
            _md5 = _list_remove(['00000000000000000000000000000000', ''], args['md5'])
            
        if 'filename' in args:
            _filename = _list_remove([''], args['filename'])

        if len(_md5) == 0 and len(_filename) > 0:
            if len(_filename) == 1:
                return f'''Search for modifications (create, modification, rename and delete) in files when name contains {_filename[0]}'''
            else:
                return f'''Search for modifications (create, modification, rename and delete) in files when name contains any of {(", ".join(_filename))}'''
            
        if len(_md5) > 0 and len(_filename) == 0:
            if len(_md5) == 1:
                return f'''Search for modifications (create, modification and rename) in files when MD5 is {_md5[0]}'''
            else:
                return f'''Search for modifications (create, modification and rename) in files when MD5 is one of {(", ".join(_md5))}'''
            
        if len(_md5) == 1:
            if len(_filename) == 1:
                return f'''Search for modifications (create, modification and rename) in files with MD5 {_md5[0]} and name {_filename[0]}'''
            else:
                return f'''Search for modifications (create, modification and rename)in files with MD5 {_md5[0]} and name any of {(", ".join(_filename))}'''
        
        if len(_md5) > 1:
            if len(_filename) == 1:
                return f'''Search for modifications (create, modification and rename) in files with name {_filename[0]} and MD5 any of {(", ".join(_md5))}'''
            else:
                return f'''Search for modifications (create, modification and rename) in files if MD5 is one of {(", ".join(_md5))} and name contains any of {(", ".join(_filename))}'''
    
        return None;      
    
    def _sql_query_pe_disk_updates(self, client, md5, filename, period):
        _md5s = [ md5s ] if not isinstance(md5, list) else md5
        _filenames = [ filenames ] if not isinstance(filename, list) else filename  
        
        _md5s = _list_remove([ '00000000000000000000000000000000', '' ], _md5s)
        _filenames = _list_remove([ '' ], _filenames)
        
        _ini_date = period.ini("%Y/%m/%d")
        _ini_dttm = period.ini("%Y/%m/%d %H:%M:%S")
        _end_date = period.end("%Y/%m/%d")
        _end_dttm = period.end("%Y/%m/%d %H:%M:%S")

        if (len(_md5s) > 0) or (len(_filenames) > 0):
            from TH.Core.adhoc import get_sql_query            

            if (len(_md5s) > 0) and (len(_filenames) > 0):
                _sqlsearch = ''
                for _md5 in _md5s:
                    _sqlsearch += f"(lower(ChildMd5) = '{_md5.lower()}') AND ("
                    for _filename in _filenames:
                        _sqlsearch += f"(lower(ChildFilename) LIKE '%{_filename.lower()}%') OR "
                    _sqlsearch = _sqlsearch.removesuffix(' OR ') + ') OR'
                _sqlsearch = _sqlsearch.removesuffix(' OR')  
            else:
                _sqlsearch = ''
                for _md5 in _md5s:
                    _sqlsearch += f"OR (lower(ChildMd5) = '{_md5.lower()}') "
                for _filename in _filenames:
                    _sqlsearch += f"OR (lower(ChildFilename) LIKE '%{_filename.lower()}%')"
                _sqlsearch = _sqlsearch.removeprefix('OR ')   

            _sql = "select * from ProcessOps "
            _sql += f"WHERE ClientId='{client}' "
            _sql += f"AND Date >= '{_ini_date}' AND Date <= '{_end_date}' "
            _sql += f"AND DateTime >='{_ini_dttm}' AND DateTime <='{_end_dttm}' "
            _sql += "AND Operation in (1, 2, 6, 7) " # PECreate, PEModified, PEDelete, PERename
            _sql += f"AND ({_sqlsearch})"

            return get_sql_query(_sql)
        else:
            return pd.DataFrame()

    def _eval(self, client, md5, filename, date, days): 
        return self._sql_query_pe_disk_updates(client, md5, filename, TimePeriod(to_date=date, num_days=int(days)))

    def _show(self, _result, layout, fixedargs, provides, client, md5, filename, date, days):
        _columns = ['DateTime', 'Operation', 'Muid', 'LoggedUser', 'ParentFilename', 'ParentPath', 'ParentMd5','ParentPid', 'ChildFilename', 'ChildPath', 'ChildMd5', 'ChildClassification', 'DetectionId', 'WinningTech', 'RemoteIp', 'RemoteUsername', 'RemoteMachineName']
        if len(_result) > 0:            
            _df = _result[_columns]            
        else:
            _df = pd.DataFrame(columns = _columns)

        _gridopt = {
            'groupcolumns': [{
                'headerName': 'Operation',
                'children': [
                    { 'field': 'DateTime' },
                    { 'field': 'Operation' },
                    { 'field': 'Muid', 'columnGroupShow': 'open' },
                    { 'field': 'LoggedUser', 'columnGroupShow': 'open' }
                ]            
            }, {
                'headerName': 'Parent',
                'children': [
                    { 'field': 'ParentFilename' },
                    { 'field': 'ParentPath', 'columnGroupShow': 'open' },
                    { 'field': 'ParentMd5', 'columnGroupShow': 'open' },
                    { 'field': 'ParentPid', 'columnGroupShow': 'open' },              
                ]
            }, {
                'headerName': 'Child',
                'children': [
                    { 'field': 'ChildFilename' },
                    { 'field': 'ChildPath', 'columnGroupShow': 'open' },
                    { 'field': 'ChildMd5', 'columnGroupShow': 'open' }, 
                    { 'field': 'ChildClassification', 'columnGroupShow': 'open' },
                    { 'field': 'DetectionId', 'columnGroupShow': 'open' },
                    { 'field': 'WinningTech', 'columnGroupShow': 'open' }
                ]
            },{
                'headerName': 'Remote',
                'children': [
                    { 'field': 'RemoteIp' },
                    { 'field': 'RemoteUsername', 'columnGroupShow': 'open' },
                    { 'field': 'RemoteMachineName', 'columnGroupShow': 'open' }
                ]            
            }],
            'cellStyleRules': {
                'Action': [
                    { 'field': 'Action', 'value': 'Allow', 'style': 'color: var(--color-green);' },
                    { 'field': 'Action', 'value': 'Block', 'style': 'color: var(--color-red);' },
                    { 'field': 'Action', 'value': 'Quarantine', 'style': 'color: var(--color-red);' },
                    { 'field': 'Action', 'value': 'Delete', 'style': 'color: var(--color-red);' },
                    { 'field': 'Action', 'value': 'AllowSonGWInstaller', 'style': 'color: var(--color-cyan);' },
                    { 'field': 'Action', 'value': 'AllowSWAuthorized', 'style': 'color: var(--color-cyan);' },
                    { 'field': 'Action', 'value': 'AllowWL', 'style': 'color: var(--color-cyan);' },
                    { 'field': 'Action', 'value': 'AllowFGW', 'style': 'color: var(--color-cyan);' },
                ],
                'ChildClassification': [
                    { 'field': 'ChildClassification', 'value': 'Goodware', 'style': 'color: var(--color-green);' },
                    { 'field': 'ChildClassification', 'value': 'Malware', 'style': 'color: var(--color-red);' },
                    { 'field': 'ChildClassification', 'value': 'Pup', 'style': 'color: color: var(--color-cyan);' }
                ],  
                'ChildFilename': [
                    { 'field': 'ChildClassification', 'value': 'Goodware', 'style': 'color: var(--color-green);' },
                    { 'field': 'ChildClassification', 'value': 'Malware', 'style': 'color: var(--color-red);' },
                    { 'field': 'ChildClassification', 'value': 'Pup', 'style': 'color: color: var(--color-cyan);' }
                ],
                'ChildPath': [
                    { 'field': 'ChildClassification', 'value': 'Goodware', 'style': 'color: var(--color-green);' },
                    { 'field': 'ChildClassification', 'value': 'Malware', 'style': 'color: var(--color-red);' },
                    { 'field': 'ChildClassification', 'value': 'Pup', 'style': 'color: color: var(--color-cyan);' }
                ],
                'ChildMd5': [
                    { 'field': 'ChildClassification', 'value': 'Goodware', 'style': 'color: var(--color-green);' },
                    { 'field': 'ChildClassification', 'value': 'Malware', 'style': 'color: var(--color-red);' },
                    { 'field': 'ChildClassification', 'value': 'Pup', 'style': 'color: color: var(--color-cyan);' }
                ]
            }                                 
        }
                    
        dashboard = nbDashboard(False, 'EN', layout=layout)
        dashboard.grid(_df, fixedargs=fixedargs, options=_gridopt, provides=provides)        
        dashboard.run()  

class BrickBlocks4Machine(BrickClass):
    def __init__(self, bricks=None):
        super().__init__(
            bricks = bricks,
            label = 'Blocked operations in the machine',
            desc = 'Returns all blocked operations in the machine',
            long = self._long,
            tags = [ 'Analysis/Machine' ],
            args = { 
                'client': { 'editable': False, 'propagate': True },
                'muid': { 'editable': True, 'propagate': False },
                'date': { 'editable': False, 'propagate': True },
                'days': { 'editable': False, 'propagate': True }
            },
            mode = 'data')
    
    def _fnc_machine_blocks(self, client, muid, period):
        _muid = [ muid ] if not isinstance(muid, list) else muid
        if len(_muid) == 0:
            return pd.DataFrame()
        else:
            _async_request = OrionAsyncRequest()
            
            # from TH.Core.adhoc import get_sql_query  
            _muidlist = ','.join(["\'" + str(i).lower() + "\'" for i in _muid])

            _ini_date = period.ini("%Y/%m/%d")
            _ini_dttm = period.ini("%Y/%m/%d %H:%M:%S")
            _end_date = period.end("%Y/%m/%d")
            _end_dttm = period.end("%Y/%m/%d %H:%M:%S")
            
            # obtener todas las entradas de remediationOps
            _sql = "SELECT * from RemediationOps "
            _sql += f"WHERE ClientId='{client}' "        
            _sql += f"AND Date >= '{_ini_date}' AND Date <= '{_end_date}' "
            _sql += f"AND DateTime >='{_ini_dttm}' AND DateTime <='{_end_dttm}' "
            _sql += f"AND lower(Muid) in ({_muidlist}) "
            _remediation_req = sql_query_request(_async_request, _sql) # encolar la peticion
            
            # obtener todas las entradas de processOps
            _sql = "SELECT * from ProcessOps "
            _sql += f"WHERE ClientId='{client}' "        
            _sql += f"AND Date >= '{_ini_date}' AND Date <= '{_end_date}' "
            _sql += f"AND DateTime >='{_ini_dttm}' AND DateTime <='{_end_dttm}' "
            _sql += f"AND lower(Muid) in ({_muidlist}) "
            _processops_req = sql_query_request(_async_request, _sql) # encolar la peticion
            
            # first wait for (quicker) RemediationOps query
            _response = async_query_response(_async_request, _remediation_req)
            _rm = _response[0]
            if _rm.empty:
                return pd.DataFrame() # no data returned for RemediationOps
            else:
                _rm = _rm[['Muid', 'TimeStamp', 'LoggedUser', 'Action', 'DetectionId', 'ParentPath', 'ParentFilename', 'ParentMd5', 'ChildPath', 'ChildFilename', 'ChildMd5', 'WinningTech', 'ChildClassification']]
            
            # then wait for ProcessOps query
            _response = async_query_response(_async_request, _processops_req)
            _pr = _response[0]
            if _pr.empty:
                return pd.DataFrame() # no data in ProcessOps query
            else:
                _pr = _pr[['DateTime', 'TimeStamp', 'LoggedUser', 'Operation', 'ParentPath', 'ParentPid', 'ChildPath', 'ChildPid', 'CommandLine', 'RemoteIp', 'RemoteUsername', 'RemoteMachineName']]

            # inner join: entradas de processOps con equivalente en RemediationOps (y diferencia de fechas < 1 segundo)
            _ij = _pr.merge(_rm, on=[ 'LoggedUser', 'ParentPath', 'ChildPath'])
            _ij['TimeDiff'] = abs((pd.to_datetime(_ij['TimeStamp_x']) - pd.to_datetime(_ij['TimeStamp_y'])).dt.total_seconds())
            _df = _ij.query('TimeDiff < 1').reset_index()
                    
            return _df        

    def _long(self, args):
        if 'muid' in args:
            _muid = _list_remove([ '' ], args['muid'])
        
        if len(_muid) == 1:
            return f'''Returns all blocked operations in the machine {_muid[0]}'''
        if len(_muid) > 1:
            return f'''Returns all blocked operations in the machines {(", ".join(_muid))}'''
            
        return None
    
    def _eval(self, client, muid, date, days): 
        return self._fnc_machine_blocks(client, muid, TimePeriod(to_date=date, num_days=int(days)))
    
    def _show(self, _result, layout, fixedargs, provides, client, muid, date, days): 
        _columns = [ 'DateTime', 'Muid', 'LoggedUser', 'ParentFilename', 'ParentPath', 'ParentMd5', 'ParentPid', 'Operation', 'ChildFilename', 'ChildPath', 'ChildMd5', 'ChildPid', 'ChildClassification','Action', 'WinningTech', 'DetectionId', 'CommandLine', 'RemoteIp', 'RemoteUsername', 'RemoteMachineName' ]
        if _result.size > 0:
            _df = _result[_columns]
        else:
            _df = pd.DataFrame(columns = _columns)

        _gridopt = {
            'groupcolumns': [{
                'headerName': 'Operation',
                'children': [
                    { 'field': 'DateTime' },
                    { 'field': 'Operation' },
                    { 'field': 'CommandLine', 'columnGroupShow': 'open' },
                    { 'field': 'Muid', 'columnGroupShow': 'open' },
                    { 'field': 'LoggedUser', 'columnGroupShow': 'open' }
                ]            
            }, {
                'headerName': 'Parent',
                'children': [
                    { 'field': 'ParentFilename' },
                    { 'field': 'ParentPath', 'columnGroupShow': 'open' },
                    { 'field': 'ParentMd5', 'columnGroupShow': 'open' },     
                    { 'field': 'ParentPid', 'columnGroupShow': 'open'},
                    { 'field': 'ParentCategory', 'columnGroupShow': 'open'}
                ]
            }, {
                'headerName': 'Action',
                'children': [
                    { 'field': 'Action' },
                    { 'field': 'WinningTech', 'columnGroupShow': 'open' },
                    { 'field': 'DetectionId', 'columnGroupShow': 'open' }
                ]
            },  {
                'headerName': 'Child',
                'children': [
                    { 'field': 'ChildFilename' },
                    { 'field': 'ChildPath', 'columnGroupShow': 'open' },
                    { 'field': 'ChildMd5', 'columnGroupShow': 'open' },                
                    { 'field': 'ChildPid', 'columnGroupShow': 'open'},
                    { 'field': 'ChildClassification', 'columnGroupShow': 'open' }
                ]
            },{
                'headerName': 'Remote',
                'children': [
                    { 'field': 'RemoteIp' },
                    { 'field': 'RemoteUsername', 'columnGroupShow': 'open' },
                    { 'field': 'RemoteMachineName', 'columnGroupShow': 'open' }
                ]            
            }],
            'cellStyleRules': {
                'Action': [
                    { 'field': 'Action', 'value': 'Allow', 'style': 'color: var(--color-green);' },
                    { 'field': 'Action', 'value': 'Block', 'style': 'color: var(--color-red);' },
                    { 'field': 'Action', 'value': 'Quarantine', 'style': 'color: var(--color-red);' },
                    { 'field': 'Action', 'value': 'Delete', 'style': 'color: var(--color-red);' },
                    { 'field': 'Action', 'value': 'AllowSonGWInstaller', 'style': 'color: var(--color-cyan);' },
                    { 'field': 'Action', 'value': 'AllowSWAuthorized', 'style': 'color: var(--color-cyan);' },
                    { 'field': 'Action', 'value': 'AllowWL', 'style': 'color: var(--color-cyan);' },
                    { 'field': 'Action', 'value': 'AllowFGW', 'style': 'color: var(--color-cyan);' },
                ],
                'ChildFilename': [
                    { 'field': 'ChildClassification', 'value': 'Goodware', 'style': 'color: var(--color-green);' },
                    { 'field': 'ChildClassification', 'value': 'Malware', 'style': 'color: var(--color-red);' },
                    { 'field': 'ChildClassification', 'value': 'Pup', 'style': 'color: var(--color-cyan);' }                    
                ],
                'ChildPath': [
                    { 'field': 'ChildClassification', 'value': 'Goodware', 'style': 'color: var(--color-green);' },
                    { 'field': 'ChildClassification', 'value': 'Malware', 'style': 'color: var(--color-red);' },
                    { 'field': 'ChildClassification', 'value': 'Pup', 'style': 'color: var(--color-cyan);' }                        
                ],
                'ChildPid': [
                    { 'field': 'ChildClassification', 'value': 'Goodware', 'style': 'color: var(--color-green);' },
                    { 'field': 'ChildClassification', 'value': 'Malware', 'style': 'color: var(--color-red);' },
                    { 'field': 'ChildClassification', 'value': 'Pup', 'style': 'color: var(--color-cyan);' }                        
                ],
                'ChildMd5': [
                    { 'field': 'ChildClassification', 'value': 'Goodware', 'style': 'color: var(--color-green);' },
                    { 'field': 'ChildClassification', 'value': 'Malware', 'style': 'color: var(--color-red);' },
                    { 'field': 'ChildClassification', 'value': 'Pup', 'style': 'color: var(--color-cyan);' }                        
                ],
                'ChildClassification': [
                    { 'field': 'ChildClassification', 'value': 'Goodware', 'style': 'color: var(--color-green);' },
                    { 'field': 'ChildClassification', 'value': 'Malware', 'style': 'color: var(--color-red);' },
                    { 'field': 'ChildClassification', 'value': 'Pup', 'style': 'color: var(--color-cyan);' }                        
                ]
            }
        }
                
        dashboard = nbDashboard(False, 'EN', layout=layout)
        dashboard.grid(_df, fixedargs=fixedargs, options=_gridopt, provides=provides)   
        dashboard.run() 

def _fnc_severity_to_string(severity):
    if severity == 1 or severity == 'Critical':
        return 'Critical'
    if severity == 2 or severity == 'High':
        return 'High'
    if severity == 3 or severity == 'Medium':
        return 'Medium'
    if severity == 4 or severity == 'Low':
        return 'Low'
        
    return 'Undefined'

def _fnc_severity_to_style(severity):
    if severity == 1 or severity == 'Critical':
        return 'border-radius: 6px; padding: 2px 10px; width: fit-content; font-weight: bold; background-color: red; color: white'
    if severity == 2 or severity == 'High':
        return 'border-radius: 6px; padding: 2px 10px; width: fit-content; font-weight: bold; background-color: darkorange; color: white'
    if severity == 3 or severity == 'Medium':
        return 'border-radius: 6px; padding: 2px 10px; width: fit-content; font-weight: bold; background-color: darkyellow; color: black'
    if severity == 4 or severity == 'Low':
        return 'border-radius: 6px; padding: 2px 10px; width: fit-content; font-weight: bold; background-color: lightgrey; color: black'
        
    return ''

class NbIoaInformation(NbComponent):
    def __init__(self):
        super().__init__('ioas')
        
    def declare(self, ioa_df=None, fixedargs={}, provides=None, consumes=None):            
        ioa = self.data_from_consumes(ioa_df, consumes)
        
        # IOA TITLE
        def _fnc_ioa_header(_ioa):
            return f'''
            <div>
                <h2 style="padding: 5px 10px 2px 10px; width: 100%; color: var(--color-accent) !important; font-size: 16px; font-weight: bold; border-bottom: 1px solid var(--color-accent); margin-bottom: 2px;">
                    {_ioa['HuntingRuleName']}
                </h2>
                <h3 style="padding: 0px 10px; margin: -5px 0px 0px 0px;">
                    Alert: <b>{_ioa['AlertId']}</b> in machine: <b>{_ioa['Muid']}</b><br/>
                    id: {_ioa['HuntingRuleId']} - version: {_ioa['HuntingRuleVersion']}
                </h3>
            </div>'''

        def _fnc_escape_html(string):
            _escape_table = { 
                '$': '\$',  # https://skeptric.com/jupyter-nolatex/
                '&': '&amp;',
                '<': '&lt;',
                '>': '&gt;',
                '\"': '&quot;',
                '\'': '&#39;'
            }
            
            for c, r in _escape_table.items():
                string = string.replace(c, r)
            
            return string
        
        # IOA EVIDENCE
        def _fnc_ioa_evidence(_ioa, _table):
            if _table is None:
                return '''
                    <h2>No contents or corrupted evidence data</h2>
                '''

            _html = ''
            _html += '<table style="width: 100%">'
            
            # alert date time
            _html += '<tr>'
            _html += '<td style="width: 20%; padding-right: 10px; color: var(--color-accent); font-weight: bold;">DateTime</td>'
            _html += f'''<td>
                <div style="max-width: 100%; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{_ioa['AlertDateTime']}</div>
            </td>'''
            _html += '</tr>'
            
            # alert severity
            _html += '<tr>'
            _html += '<td style="width: 20%; padding-right: 10px; color: var(--color-accent); font-weight: bold;">Severity</td>'
            _html += f'''<td>
                <div style="max-width: 100%; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; {_fnc_severity_to_style(_ioa['Severity'])}">
                    {_fnc_severity_to_string(_ioa['Severity']).upper()}
                </div>
            </td>'''
            _html += '</tr>'
            
            for _key, _val in _table.items():
                if _key == 'CommandLineDecoded':
                    continue # ya se contempla dentro del command line

                _html += '<tr>'
                _html += f'<td style="width: 20%; padding-right: 10px; color: var(--color-accent); font-weight: bold;">{_key}</td>'
                if _key == 'CommandLine':
                    _table['CommandLine'] = _fnc_escape_html(_table['CommandLine'])
                    
                    if 'CommandLineDecoded' in _table:
                        _table['CommandLineDecoded'] = _fnc_escape_html(_table['CommandLineDecoded'])
                        
                        _html += f'''
                        <td onclick="javascript:(function(){{
                            let _encoded_dom = document.getElementById('{_ioa['AlertId']}_encoded_command_line');
                            let _decoded_dom = document.getElementById('{_ioa['AlertId']}_decoded_command_line');
                            let _ecdcbut_dom = document.getElementById('{_ioa['AlertId']}_encode_decode_button');

                            if (_ecdcbut_dom.innerHTML == 'Decode command line'){{
                                _encoded_dom.style.display = 'none';
                                _decoded_dom.style.display = 'block';
                                _ecdcbut_dom.innerHTML = 'Encode command line';
                            }}
                            else {{
                                _encoded_dom.style.display = 'block';
                                _decoded_dom.style.display = 'none';  
                                _ecdcbut_dom.innerHTML = 'Decode command line';
                            }}
                            document.getElementById(_encoded_id).style.display = 'none';
                            document.getElementById(_decoded_id).style.display = 'block';
                        }})()">
                            <div id="{_ioa["AlertId"]}_encode_decode_button" style="float: right; padding: 4px 8px; background: var(--color-accent); color: var(--color-text-inverse); border-radius: 2px;">Decode command line</div>
                        </td>'''
                        _html += '</tr>'

                        _html += f'<tr >'
                        _html += '<td colspan="2">'
                        _html += f'''
                            <div id="{_ioa["AlertId"]}_encoded_command_line" style="font-family: monospace; border: 1px solid var(--color-accent); margin: 2px 0px; padding: 5px; word-wrap: break-word;">
                                {_table["CommandLine"]}
                            </div>
                        '''
                        _html += f'''
                            <div id="{_ioa["AlertId"]}_decoded_command_line" style="display: none; font-family: monospace; border: 1px solid var(--color-accent); margin: 2px 0px; padding: 5px; word-wrap: break-word;">
                                {_table["CommandLineDecoded"]}
                            </div>'''
                        _html += '</td>'
                        _html += '</tr>'

                        _html += '<tr>'
                    else:
                        _html += '<td></td>'
                        _html += '</tr>'
                        _html += '<tr>'
                        _html += '<td colspan="2">'
                        _html += f'<div style="border: 1px solid var(--color-accent); margin: 2px 0px; padding: 5px; word-wrap: break-word;">{_val}</div>'
                        _html += '</td>'
                        _html += '</tr>'
                        _html += '<tr>'
                else:
                    _html += f'''
                    <td>
                        <div style="max-width: 100%; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{_val}</div>
                    </td>'''
                _html += '</tr>'
            _html += '</table>'
            
            return _html

        def _fnc_append_to_select(_select, _key, _val):
            _key = _key.lower()
            if _key not in _select:
                 _select[_key] = []
            _select[_key].append(_val)
            return _select
        
        # declare the component widget function
        def _fnc_component(nb):
            _ioa = nb.scope.get(ioa) if isinstance(ioa, ScopeKey) else ioa
            if _ioa is None or _ioa.empty if isinstance(_ioa, pd.DataFrame) else not _ioa:
                return
            
            _select = {} # build the selected item for hte provider
            for _key, _value in fixedargs.items():
                _select[_key] = _value

            _select['rowcount'] = len(_ioa.index)        

            _select['rowcount'] = len(_ioa.index)        

            for _row in _ioa.iterrows():
                _target = _row[1]
                
                for _key in [ 'Muid' ]:  # add addtional IoA fields to selected data 
                    _select = _fnc_append_to_select(_select, _key, _target[_key]);
                
                _evidence = jsonpickle.decode(_target['EvidenceData'])
                if _evidence:
                    _contents = _evidence['contents'][0] if _evidence['contents'] else None
                    display(HTML(_fnc_ioa_header(_target)))
                    if _contents:  
                        display(HTML(_fnc_ioa_evidence(_target, _contents)))
                        for _key, _val in _contents.items():   # complete the selected information
                            _select = _fnc_append_to_select(_select, _key, _val)

            return _select  # provides the IoA results (for next brick)                                 

        # this is an attribute for nbLayout, so it can access to its members
        self._widget = ScopeWidget(_fnc_component, self, provides, consumes)
        self.append(self._widget, 'widget')

_ = NbIoaInformation()

class BrickIOAInfo(BrickClass):
    def __init__(self, bricks=None):
        super().__init__(
            bricks = bricks,
            label = 'Alert information',
            desc = 'Provides the detail for an IoA',
            long = self._long,
            tags = [ 'Analysis/IoA' ],
            args = { 
                'client': { 'editable': False, 'propagate': True },
                'ioa': { 'editable': True, 'propagate': False },
                'date': { 'editable': False, 'propagate': True },
                'days': { 'editable': False, 'propagate': True }
            },
            mode = 'data')

    def _long(self, args):
        if 'ioa' in args:
            _ioa = _list_remove([ '' ], args['ioa'])
        
        if len(_ioa) == 1:
            return f'''Returns IoA with id {_ioa[0]}'''
        if len(_ioa) > 1:
            return f'''Returns all IoAs with Id any of {(", ".join(_ioa))}'''
            
        return None
    
    def _fnc_ioa_query(self, client, ioa, period):
        _ioa = [ ioa ] if not isinstance(ioa, list) else ioa
        if len(_ioa) == 0:
            return pd.DataFrame()
        else:
            from TH.Core.adhoc import get_sql_query  
            _ioalist = ','.join(["\'" + str(i).lower() + "\'" for i in _ioa])

            _ini_dttm = period.ini("%Y/%m/%d %H:%M:%S")
            _end_dttm = period.end("%Y/%m/%d %H:%M:%S")

            _sql = "SELECT * from private_Alerts "
            _sql += f"WHERE ClientId='{client}' " 
            _sql += f"AND AlertDateTime >= toInt32(toDateTime('{_ini_dttm}')) "
            _sql += f"AND AlertDateTime <= toInt32(toDateTime('{_end_dttm}')) " 
            _sql += f"AND lower(AlertId) in ({_ioalist}) "            
        
            _df = get_sql_query(_sql)
            return _df
    
    def _eval(self, client, ioa, date, days): 
        return self._fnc_ioa_query(client, ioa, TimePeriod(to_date=date, num_days=int(days)))
    
    def _show(self, _result, layout, fixedargs, provides, client, ioa, date, days): 
        if _result.size > 0:
            _df = _result
        else:
            _df = pd.DataFrame()
                
        dashboard = nbDashboard(False, 'EN', layout=layout)
        if _df.empty:
            dashboard.markdown('#No IoA was found')
        else:
            dashboard.ioas(_df, fixedargs, provides='grid-select')
                            
        dashboard.run()

class BrickIOA4Machine(BrickClass):
    def __init__(self, bricks=None):
        super().__init__(
            bricks = bricks,
            label = 'Alerts in the machine',
            desc = 'Returns all IoAs in a machine',
            long = self._long,
            tags = [ 'Analysis/IoA', 'Analysis/Machine' ],
            args = { 
                'client': { 'editable': False, 'propagate': True },
                'muid': { 'editable': True, 'propagate': False },
                'date': { 'editable': False, 'propagate': True },
                'days': { 'editable': False, 'propagate': True }
            },
            mode = 'data')    

    def _long(self, args):
        if 'muid' in args:
            _muid = _list_remove([ '' ], args['muid'])
        
        if len(_muid) == 1:
            return f'''Returns all IoAs for MUID {_muid[0]}'''
        if len(_muid) > 1:
            return f'''Returns all IoAs in the machines {(", ".join(_muid))}'''
            
        return None

    def _fnc_ioa_query(self, client, muid, period):
        _muid = [ muid ] if not isinstance(muid, list) else muid
        if len(_muid) == 0:
            return pd.DataFrame()
        else:
            # use the API to get non filtered alert-ids
            from TH.Core.TH import get_alerts
            _df = get_alerts(muid=muid, period=period)
            if not _df.empty:
                _ioas = _df['pandaAlertId'].to_list();
            else:
                return pd.DataFrame();
            
            # obtain the complete alert information from the database
            from TH.Core.adhoc import get_sql_query  
            _ioaslist = ','.join(["\'" + str(i) + "\'" for i in _ioas])
            
            _ini_dttm = period.ini("%Y/%m/%d %H:%M:%S")
            _end_dttm = period.end("%Y/%m/%d %H:%M:%S")
            
            _sql = "SELECT * from private_Alerts "
            _sql += f"WHERE ClientId='{client}' " 
            _sql += f"AND AlertDateTime >= toInt32(toDateTime('{_ini_dttm}')) "
            _sql += f"AND AlertDateTime <= toInt32(toDateTime('{_end_dttm}')) " 
            _sql += f"AND AlertId in ({_ioaslist}) "

            _df = get_sql_query(_sql)
            return _df

    def _eval(self, client, muid, date, days): 
        _result = self._fnc_ioa_query(client, muid, TimePeriod(to_date=date, num_days=int(days))) 
        if not _result.empty:
            _result['Severity'] = _result['Severity'].replace([1, 2, 3, 4, 1000], ['Critical', 'High', 'Medium', 'Low', 'Undefined'])
        return _result    
    
    def _show(self, _result, layout, fixedargs, provides, client, muid, date, days): 
        _columns = [ 'AlertDateTime', 'AlertId', 'HuntingRuleName', 'Severity' ]
        if _result.size > 0:
            _df = _result[_columns]
        else:
            _df = pd.DataFrame(columns = _columns)
        
        def _fnc_row_to_ioa(nb):     
            _ioa = None
            _row = nb.scope.get('selected-row')
            if _row:
                _ioa = _result.loc[_result['AlertId'] == _row['alertid'][0]]
                _ioa = _ioa.reset_index(drop=True)
            return _ioa
            
        dashboard = nbDashboard(False, 'EN', layout=layout)
        if _df.size > 0:
            dashboard.grid(_df, fixedargs=fixedargs, options = { 'singlerow': True }, provides='selected-row')
            dashboard.provider(_fnc_row_to_ioa, provides='selected-ioa', consumes='selected-row')
            dashboard.ioas(None, fixedargs, provides='grid-select', consumes='selected-ioa')
        else:
            dashboard.markdown('#No IoA was found')
        dashboard.run()

class BrickProcessTree(BrickClass):
    def __init__(self, bricks=None):
        super().__init__(
            bricks = bricks,
            label = 'Process tree',
            desc = 'Parent and child processes for a given event',
            long = self._long,
            tags = [ 'Analysis/Process' ],
            args = { 
                'client': { 'editable': False, 'propagate': True },
                'process': { 'editable': True, 'propagate': False },
                'date': { 'editable': False, 'propagate': True },
                'days': { 'editable': False, 'propagate': True }
            },
            mode = 'data')

    def _long(self, args):
        _process = []
        if 'process' in args:
            for _arg in args['process']:
                _process.append(json.loads(_arg))
        
        if len(_process) == 1:
            return f'''Returns the process tree in machine {_process[0]['muid']} for the pid {_process[0]['pid']}'''
        if len(_process) > 1:
            _mid = []
            _pid = [];
            
            for _proc in _process:
                _mid.append(_proc['muid'])
                _pid.append(_proc['pid'])
            
            _mid = list(dict.fromkeys(_mid))
            _pid = list(dict.fromkeys(_pid))
            
            _str = 'Returns the process tree in '
            if len(_mid) == 1:
                _str += f'the machine {_mid[0]} for '
            else:
                _str += f'the machines {", ".join(_mid)} for '
            
            if len(_pid) == 1:
                _str += f'the pid {_pid[0]}'
            else:
                _str += f'the pids {", ".join(_pid)}'
            
            return _str
            
        return None
    
    def _sql_get_parent_process(self, client, process, period):
        _ini_date = period.ini("%Y/%m/%d")
        _ini_dttm = period.ini("%Y/%m/%d %H:%M:%S")
        _end_date = period.end("%Y/%m/%d")
        _end_dttm = period.end("%Y/%m/%d %H:%M:%S")

        if len(process) > 0:        
            from TH.Core.adhoc import get_sql_query

            _processsql = ""
            for _process in process:
                _data = json.loads(_process)
                if _data['md5'] != '00000000000000000000000000000000':
                    _processsql += "("
                    _processsql += f"lower(Muid) = '{_data['muid'].lower()}' "
                    _processsql += f"AND lower(ChildMd5) = '{_data['md5'].lower()}' "
                    _processsql += f"AND ChildPid = '{_data['pid']}' "
                    _processsql += ") OR "
            _processsql = _processsql[:-4]    

            _df = pd.DataFrame()
            if len(_processsql) > 0:
                _sql = f"SELECT * from ProcessOps WHERE ClientId='{client}' "
                _sql += f"AND Date >= '{_ini_date}' AND Date <= '{_end_date}' "
                _sql += f"AND DateTime >='{_ini_dttm}' AND DateTime <='{_end_dttm}' "
                _sql += "AND Operation in [0, 3, 17] " # CreateProc, LibraryLoad, RemoteThreadCreated
                _sql += f"AND ({_processsql}) "
            
                _df = get_sql_query(_sql)
                if not _df.empty:
                    _df = _df.drop_duplicates(subset=['DateTime', 'LoggedUser', 'ParentFilename', 'ParentPid', 'ChildFilename', 'ChildPid', 'Action'])
                    
                    # todos los padres tienen el mismo Muid, ChildMd5 y ChildPid (son creaciones del mismo proceso)
                    _df['ChildUnique'] = None
                    _childunique = 1
                    for index, _row in _df.iterrows():
                        _df.loc[index,['ChildUnique']] = f"{_df.loc[index]['ChildFilename']} [{_childunique}]"
                        _childunique += 1

            return _df   
        else:
            return pd.DataFrame()
    
    def _sql_get_children_process(self, client, process, period):
        _ini_date = period.ini("%Y/%m/%d")
        _ini_dttm = period.ini("%Y/%m/%d %H:%M:%S")
        _end_date = period.end("%Y/%m/%d")
        _end_dttm = period.end("%Y/%m/%d %H:%M:%S")

        if len(process) > 0:        
            from TH.Core.adhoc import get_sql_query
            
            _processsql = ""
            for _process in process:
                _data = json.loads(_process)
                if _data['md5'] != '00000000000000000000000000000000':
                    _processsql += "("
                    _processsql += f"lower(Muid) = '{_data['muid'].lower()}' "
                    _processsql += f"AND lower(ParentMd5) = '{_data['md5'].lower()}' "
                    _processsql += f"AND ParentPid = '{_data['pid']}' "
                    _processsql += ") OR "
            _processsql = _processsql[:-4]           

            _df = pd.DataFrame()
            if len(_processsql) > 0:
                _sql = f"SELECT * from ProcessOps WHERE ClientId='{client}' "
                _sql += f"AND Date >= '{_ini_date}' AND Date <= '{_end_date}' "
                _sql += f"AND DateTime >='{_ini_dttm}' AND DateTime <='{_end_dttm}' "
                _sql += "AND Operation in [0, 3, 17] " # CreateProc, LibraryLoad, RemoteThreadCreated
                _sql += f"AND ({_processsql}) "           
            
                _df = get_sql_query(_sql)
                if not _df.empty:
                    _df = _df.drop_duplicates(subset=['DateTime', 'LoggedUser', 'ParentFilename', 'ParentPid', 'ChildFilename', 'ChildPid', 'Action'])
                    
                    _df['ChildUnique'] = None
                    _childuniques = {} # group child counters by ChildFilenames
                    for index, _row in _df.iterrows():
                        _filename = _df.loc[index]['ChildFilename']
                        _childunique = (_childuniques[_filename] + 1) if _filename in _childuniques else 1
                        _childuniques[_filename] = _childunique
                            
                        _df.loc[index,['ChildUnique']] = f"{_df.loc[index]['ChildFilename']} [{_childunique}]"
            return _df   
        else:
            return pd.DataFrame()
        
    def _sql_query_process_tree(self, client, process, period):
        _process = [ process ] if not isinstance(process, list) else process

        if len(_process) > 0:        
            _allprc = []
            
            _parent = self._sql_get_parent_process(client, _process, period)
            while not _parent.empty:
                _allprc.append(_parent)
                
                _nxtprc = []  # construir la cadena con los procesos a buscar 'Muid|ParentMd5|ParentPid'
                for index, row in _parent.iterrows():
                    _nxtprc.append(json.dumps({
                        'muid': row['Muid'],
                        'md5': row['ParentMd5'],
                        'pid': row['ParentPid']       
                    }))
                _parent = self._sql_get_parent_process(client, _nxtprc, period)

            _children = self._sql_get_children_process(client, _process, period)
            while not _children.empty:
                _allprc.append(_children)
                
                _nxtprc = []  # construir la cadena con los procesos a buscar 'Muid|ChildMd5|ChildPid'
                for index, row in _parent.iterrows():
                    _nxtprc.append(json.dumps({
                        'muid': row['Muid'],
                        'md5': row['ChildMd5'],
                        'pid': row['ChildPid']       
                    }))                                  
                _children = self._sql_get_children_process(client, _nxtprc, period)

            if len(_allprc) > 0:
                _pr = pd.concat(_allprc, ignore_index=True)
            else:
                return pd.DataFrame();
            
            return _pr
    
    def _fnc_parent_candidate(self, _df, _pr):
        _candidates = _df.loc[(_df['Muid'] == _pr['Muid']) & (_df['ChildPath'] == _pr['ParentPath']) & (_df['ChildPid'] == _pr['ParentPid'])]
        if len(_candidates) == 0:
            return None
        else:
            _candidates['_datetime'] = pd.to_datetime(_candidates['DateTime'])
            _candidates['_timediff'] = (pd.to_datetime(_pr['DateTime']) - _candidates['_datetime']).dt.total_seconds()
            _candidates = _candidates.loc[_candidates['_timediff'] >= 0]
            return (_candidates.loc[_candidates['_timediff'] == _candidates['_timediff'].min()]).iloc[0]
    
    def _fnc_hiearchy_r(self, _df, _row):
        _parent = _df[(_df['Muid'] == _row['Muid']) & (_df['ChildMd5'] == _row['ParentMd5']) & (_df['ChildPid'] == _row['ParentPid'])]
        if _parent.empty:
            return f"{_row['ParentUnique']}/{_row['ChildUnique']}"
        else: # recursive call!
            return f"{self._fnc_hiearchy_r(_df, _parent.iloc[0])}/{_row['ChildUnique']}"
        
    def _fnc_create_tree_path(self, _df):
        # create the parent unique id for each row
        _df['ParentUnique'] = None
        for index, row in _df.iterrows():
            _parent = self._fnc_parent_candidate(_df, row)
            if _parent is not None:
                _df.loc[index,['ParentUnique']] = _parent['ChildUnique']
            else:
                _df.loc[index,['ParentUnique']] = f"{_df.loc[index]['ParentFilename']} [1]"
        
        # build a hierarchy path for all the rows
        _df['TreePath'] = None
        for index, _row in _df.iterrows():
            _df.loc[index,['TreePath']] = self._fnc_hiearchy_r(_df, _row)
        
        return _df
    
    def _eval(self, client, process, date, days): 
        return self._sql_query_process_tree(client, process, TimePeriod(to_date=date, num_days=int(days)))
    
    def _show(self, _result, layout, fixedargs, provides, client, process, date, days): 
        columns = [
            'DateTime', 'Muid', 'LoggedUser', 'Operation', 'CommandLine', 
            'ParentFilename', 'ParentPath', 'ParentMd5', 'ParentPid',
            'Action', 'ChildClassification', 'WinningTech', 'DetectionId',
            'ChildFilename', 'ChildPath', 'ChildMd5', 'ChildPid', 'ChildUnique',
            'RemoteIp', 'RemoteUsername', 'RemoteMachineName'
        ]
        
        if not _result.empty:
            _df = _result[columns]
        else:
            _df = pd.DataFrame(columns=columns)
        
        _df = self._fnc_create_tree_path(_df)
        
        _gridopt = {
            'tree': {
                'group': 'Process', 
                'path': 'TreePath'
            },
            'groupcolumns': [{
                'headerName': 'Operation',
                'children': [
                    { 'field': 'DateTime' },
                    { 'field': 'Operation', 'columnGroupShow': 'open' },
                    { 'field': 'Muid', 'columnGroupShow': 'open' },
                    { 'field': 'LoggedUser', 'columnGroupShow': 'open' },
                    { 'field': 'CommandLine', 'columnGroupShow': 'open' }
                ]            
            }, {
                'headerName': 'Parent',
                'children': [
                    { 'field': 'ParentFilename' },
                    { 'field': 'ParentPid', 'columnGroupShow': 'open' },
                    { 'field': 'ParentMd5', 'columnGroupShow': 'open' },
                    { 'field': 'ParentPath', 'columnGroupShow': 'open' }              
                ]
            }, {
               'headerName': 'Action',
                'children': [
                    { 'field': 'Action' },
                    { 'field': 'ChildClassification', 'columnGroupShow': 'open' },
                    { 'field': 'WinningTech', 'columnGroupShow': 'open' },
                    { 'field': 'DetectionId', 'columnGroupShow': 'open' }
                ]             
            }, {
                'headerName': 'Child',
                'children': [
                    { 'field': 'ChildFilename' },
                    { 'field': 'ChildPid', 'columnGroupShow': 'open' },
                    { 'field': 'ChildMd5', 'columnGroupShow': 'open' },
                    { 'field': 'ChildPath', 'columnGroupShow': 'open' }
                ]                
            },{
                'headerName': 'Remote',
                'children': [
                    { 'field': 'RemoteIp' },
                    { 'field': 'RemoteUsername', 'columnGroupShow': 'open' },
                    { 'field': 'RemoteMachineName', 'columnGroupShow': 'open' }
                ]            
            }],
            'rowStyleRules': [
                { 'field': 'Action', 'value': 'Block', 'style': 'color: var(--color-red);' },
                { 'field': 'Action', 'value': 'Quarantine', 'style': 'color: var(--color-red);' },
                { 'field': 'Action', 'value': 'Delete', 'style': 'color: var(--color-red);' },
                { 'field': 'Action', 'value': 'AllowSonGWInstaller', 'style': 'color: var(--color-cyan);' },
                { 'field': 'Action', 'value': 'AllowSWAuthorized', 'style': 'color: var(--color-cyan);' },
                { 'field': 'Action', 'value': 'AllowWL', 'style': 'color: var(--color-cyan);' },
                { 'field': 'Action', 'value': 'AllowFGW', 'style': 'color: var(--color-cyan);' },
            ]
        }
        
        dashboard = nbDashboard(False, 'EN', layout=layout)
        dashboard.grid(_df, fixedargs=fixedargs, options=_gridopt, provides=provides) 
        dashboard.run()       

class BrickMd5Events(BrickClass):
    def __init__(self, bricks=None):
        super().__init__(
            bricks = bricks,
            label = 'MD5 activity in a machine',
            desc = 'Return all events generated by a MD5 in the machine',
            long = self._long,
            tags = [ 'Analysis/Md5' ],
            args = { 
                'client': { 'editable': False, 'propagate': True },
                'muid':  { 'editable': True, 'propagate': False },
                'md5':  { 'editable': True, 'propagate': False },
                'date': { 'editable': False, 'propagate': True },
                'days': { 'editable': False, 'propagate': True }
            },
            mode = 'data')

    def _long(self, args):
        if 'md5' in args:
            _md5 = _list_remove(['00000000000000000000000000000000', ''], args['md5'])
        if len(_md5) == 1:
            return f'''Returns all activity for the md5 {_md5[0]}'''
        if len(_md5) > 1:
            return f'''Returns all acivity for md5 any of {(",".join(_md5))}'''
        return None

    def _build_sql_query(self, _table, _md5s):
        _sqlhash = ''
        _tables_without_childmd5 = ['NetworkOps', 'DnsOps', 'RegistryOps', 'DataAccess']
        _tables_without_parentmd5 = ['SystemOps']
        
        if (len(_md5s) > 0):
            _sqlhash += 'AND ('
            for _md5 in _md5s:
                if _table in _tables_without_parentmd5:
                     # table missing ParentMd5 column
                    _sqlhash += f"lower(ChildMd5) = '{_md5.lower()}' OR "
                elif _table in _tables_without_childmd5:
                    # tables missing ChildMd5 column
                    _sqlhash += f"lower(ParentMd5) = '{_md5.lower()}' OR "
                else:
                    _sqlhash += f"(lower(ParentMd5) = '{_md5.lower()}' OR lower(ChildMd5) = '{_md5.lower()}') OR "
            _sqlhash = _sqlhash.removesuffix(' OR ') + ') '
        return _sqlhash

    def _processOps_action(self, _action):
        _actions = {
            'CreateProc': 0,
            'PECreat': 1,
            'PEModif': 2,
            'LibraryLoad': 3,
            'SvcInst': 4,
            'PEMapWrite': 5,
            'PEDelete': 6,
            'PERename': 7,
            'DirCreate': 8,
            'CMPCreat': 9,
            'CMOpened': 10,
            'RegKExeCreat': 11,
            'RegKExeModif': 12,
            'PENeverSeen': 15,
            'RemoteThreadCreated': 17,
            'ProcessKilled': 18,
            'SamAccess': 25,
            'Exploit VBS (Legacy)': 27,
            'Exploit Python (Legacy)': 28,
            'Exploit Ruby (Legacy)': 29,
            'Exploit Sniffer (Legacy)': 30,        
            'Exploit WSAStartup': 31,        
            'Exploit InternetReadFile (Legacy)': 32,        
            'Exploit CMD': 34,        
            'Carga de fichero d 16bits por ntvdm.exe': 39,        
            'Heuhooks (envío de detección de hooks)': 43,        
            'OpenFileInMac': 52,        
            'OpenFileInLinux': 53,        
            'CreateProcessByWmi': 54,        
            'StopProtection': 55,        
            'OpenProcessLSASS': 61           
        }

        return _actions[_action] if _action in _actions else None;

    def _table2event(self, _event):
        _events = {
            'ProcessOps': 1,
            'NetworkOps': 22,
            'RegistryOps': 27,
            'RemediationOps': 99,
            'HiddenAction': 199,
            'Download': 14,
            'DnsOps': 46,
            'ScriptOps': 30,
            'SystemOps': 45,
            'UserNotification': 50,
            'DataAccess': 26,
            'HostsFileModification': 15
        }

        return _events[_event] if _event in _events else None;
    
    def _add_eventtype_icon(self, _data):
        _events = _data['EventType'].unique().tolist()
        for _table in _events:
            _event = self._table2event(_table)
            if _event == 1:
                _processops = _data.loc[_data['EventType'] == _table]
                
                for _operation in _processops['Operation'].unique().tolist():
                    _action = self._processOps_action(_operation)
                    if _action == 0:
                        _action = '0_createprocess' # ajustar al nombre del icono
                        
                    _html = f'<span class="icon icon--event_{_event}_{_action}" style="font-size: 18px; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);"></span>'
                    _data.loc[(_data['EventType'] == _table) & (_data['Operation'] == _operation), 'EventTypeIcon'] = _html
            else:
                _html=  f'<span class="icon icon--event_{_event}" style="font-size: 18px; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);"></span>'
                _data.loc[_data['EventType'] == _table, 'EventTypeIcon'] = _html
                
        return _data
    
    def _orion_file_categories(self, md5s):
        _results = {}
        if isinstance(md5s, str):
            md5s = [ md5s ]
        
        try:
            from TH.Core.orion import AsyncRequest
            
            _results = { 'statusCode': '429' } # para la primera consulta
            while 'statusCode' in _results and (int(_results['statusCode']) == 429): 
                url = f"/forensics/md5/batch/sample"
                areq = AsyncRequest()
                req = areq.post(url, json.dumps(md5s))
                res = areq.wait(req)[0]
                _results = res.json() if res.text else list()

                # reintenta dentro de 1 segundo (en el caso de que se exceda el numero de peticiones)
                if 'statusCode' in _results and (int(_results['statusCode']) == 429): 
                    import time
                    time.sleep(1) 
        except:
            pass
        
        _classification = {}
        
        if isinstance(_results, list):
            for _result in _results:
                _classification[_result['mD5AsString']] = _result['classificationName'].capitalize()
        else: # devolver el error de la consulta
            _error = 'QUERY ERROR'
            if 'status' in _results:
                _error = f"ERROR {_results['status']} IN QUERY ({json.dumps(_results)})"
                
            for _md5 in md5s:
                _classification[_md5] = _error
                
        return _classification
                
    def _sql_query_md5(self, client, md5s, muids, period):
        _md5s = [ md5s ] if not isinstance(md5s, list) else md5s
        _md5s = _list_remove([ '00000000000000000000000000000000', '' ], _md5s)
        
        _muids = [ muids ] if not isinstance(muids, list) else muids
        _muids = _list_remove([ '00000000000000000000000000000000', '' ], _muids)

        _ini_date = period.ini("%Y/%m/%d")
        _ini_dttm = period.ini("%Y/%m/%d %H:%M:%S")
        _end_date = period.end("%Y/%m/%d")
        _end_dttm = period.end("%Y/%m/%d %H:%M:%S")

        _tables = [ 
            'RemediationOps', 
            'NetworkOps',
            'RegistryOps',
            'ProcessOps', 
            'Download', 
            'DnsOps', 
            'ScriptOps', 
            'SystemOps', 
            'UserNotification', 
            'DataAccess' 
        ]
        
        _orion_async = OrionAsyncRequest()
        
        for _table in _tables:
            _sql = f"select * from {_table} "
            _sql += f"WHERE ClientId='{client}' "
            _sql += 'AND ('
            for _muid in _muids:
                _sql += f"lower(Muid) ='{_muid.lower()}' OR "
            _sql = _sql.removesuffix(' OR ') + ') '
            _sql += f"AND Date >= '{_ini_date}' AND Date <= '{_end_date}' "
            _sql += f"AND DateTime >='{_ini_dttm}' AND DateTime <='{_end_dttm}' "
            _sql += self._build_sql_query(_table, _md5s)

            sql_query_request(_orion_async, _sql)

        _df_queries = async_query_response(_orion_async)
                               
        # concatenate in one DataFrame all the query results
        df = pd.concat(_df_queries, ignore_index=True)
        if df.shape[0] != 0:
            df = df.sort_values(by='DateTime')
            df = df.reset_index(drop=True)
        
        # select required columns and create a new DataFrame
        _columns = [
            'DateTime', 'Muid', 'ServiceLevel', 'LoggedUser','EventType', 'CommandLine', 'Operation', 'Action',
            'ParentPath', 'ParentFilename',  'ParentMd5', 'ParentPid', 'ParentCategory',
            'ChildPath', 'ChildFilename', 'ChildMd5', 'ChildPid', 'ChildCategory', 'ChildClassification',
            'DetectionId', 'WinningTech', 'Details',
            'RemoteMachineName', 'RemoteIp', 'RemoteUsername'
        ]
        
        df = pd.DataFrame(df, columns=_columns)
        if not df.empty:
            # complete the dataframe with the event icons
            df = self._add_eventtype_icon(df)
            
            # get unique Md5s from a list and get the classification of each Md5
            _unique_md5s = df['ParentMd5'].to_list() + df['ChildMd5'].to_list()
            _unique_md5s = list(dict.fromkeys(_unique_md5s))

            # clean nan values from the list
            _unique_md5s = [value for value in _unique_md5s if str(value) != 'nan']
            _unique_categories = self._orion_file_categories(_unique_md5s)
            
            for _md5, _category in _unique_categories.items():
                df.loc[df['ParentMd5'] == _md5, 'ParentCategory'] = _category
                df.loc[df['ChildMd5'] == _md5, 'ChildCategory'] = _category
            
        return df
    
    def _eval(self, client, md5,muid, date, days): 
        return self._sql_query_md5(client, md5, muid, TimePeriod(to_date=date, num_days=int(days)))
    
    def _show(self, _result, layout, fixedargs, provides, client, md5,muid, date, days): 
        _columns = [
            'EventTypeIcon, ''DateTime', 'Muid', 'ServiceLevel', 'LoggedUser', 'EventType', 'CommandLine', 'Operation', 'Action',
            'ParentPath', 'ParentFilename', 'ParentMd5', 'ParentPid', 'ParentCategory',
            'ChildPath', 'ChildFilename', 'ChildMd5', 'ChildPid', 'ChildCategory', 'ChildClassification',
            'DetectionId', 'WinningTech', 'Details',
            'RemoteMachineName', 'RemoteIp', 'RemoteUsername'
       ]
        
        _gridopt = {}
        if len(_result) > 0:            
            _df = _result
        else:
            _df = pd.DataFrame(columns = _columns)
        
        _df.rename(columns = {'ChildCategory': 'ChildCurrentClassification'}, inplace = True)
        
        _gridopt = {
            'groupcolumns': [{
                'headerName': 'Event',
                'children': [
                    { 'field': 'EventTypeIcon' },
                    { 'field': 'DateTime' },
                    { 'field': 'EventType' },
                    { 'field': 'Muid', 'columnGroupShow': 'open' },
                    { 'field': 'ServiceLevel', 'columnGroupShow': 'open' },
                    { 'field': 'LoggedUser', 'columnGroupShow': 'open' },
                    { 'field': 'CommandLine', 'columnGroupShow': 'open' },
                ]
            }, {
                'headerName': 'Parent File',
                'children': [
                    { 'field': 'ParentFilename' },
                    { 'field': 'ParentPath', 'columnGroupShow': 'open' },
                    { 'field': 'ParentPid', 'columnGroupShow': 'open' },
                    { 'field': 'ParentMd5', 'columnGroupShow': 'open' },
                    { 'field': 'ParentCategory', 'columnGroupShow': 'open' },
                ]            
            }, {
                'headerName': 'Operation',
                'children': [
                    { 'field': 'Operation' },
                    { 'field': 'Action' },                    
                ]
            }, {
                'headerName': 'Child File',
                'children': [
                    { 'field': 'ChildFilename' },
                    { 'field': 'ChildPath', 'columnGroupShow': 'open' },
                    { 'field': 'ChildPid', 'columnGroupShow': 'open' },
                    { 'field': 'ChildMd5', 'columnGroupShow': 'open' },
                    { 'field': 'ChildCurrentClassification', 'columnGroupShow': 'open' },
                    { 'field': 'ChildClassification', 'columnGroupShow': 'open' },                
                ]            
            }, {
                'headerName': 'Detection Info',
                'children': [
                    { 'field': 'DetectionId' },
                    { 'field': 'WinningTech', 'columnGroupShow': 'open' },
                    { 'field': 'Details', 'columnGroupShow': 'open' },
                ]            
            }, {
                'headerName': 'Remote',
                'children': [
                    { 'field': 'RemoteMachineName' },
                    { 'field': 'RemoteIp', 'columnGroupShow': 'open' },
                    { 'field': 'RemoteUsername', 'columnGroupShow': 'open' },
                ] 
            }],
            'cellStyleRules': {
                'Action': [
                    { 'field': 'Action', 'value': 'Allow', 'style': 'color: var(--color-green);' },
                    { 'field': 'Action', 'value': 'Block', 'style': 'color: var(--color-red);' },
                    { 'field': 'Action', 'value': 'Quarantine', 'style': 'color: var(--color-red);' },
                    { 'field': 'Action', 'value': 'Delete', 'style': 'color: var(--color-red);' },
                    { 'field': 'Action', 'value': 'AllowSonGWInstaller', 'style': 'color: var(--color-cyan);' },
                    { 'field': 'Action', 'value': 'AllowSWAuthorized', 'style': 'color: var(--color-cyan);' },
                    { 'field': 'Action', 'value': 'AllowWL', 'style': 'color: var(--color-cyan);' },
                    { 'field': 'Action', 'value': 'AllowFGW', 'style': 'color: var(--color-cyan);' },
                ],
                'Operation': [
                    { 'field': 'Action', 'value': 'Allow', 'style': 'color: var(--color-green);' },                    
                    { 'field': 'Action', 'value': 'Block', 'style': 'color: var(--color-red);' },
                    { 'field': 'Action', 'value': 'Quarantine', 'style': 'color: var(--color-red);' },
                    { 'field': 'Action', 'value': 'Delete', 'style': 'color: var(--color-red);' },
                    { 'field': 'Action', 'value': 'AllowSonGWInstaller', 'style': 'color: var(--color-cyan);' },
                    { 'field': 'Action', 'value': 'AllowSWAuthorized', 'style': 'color: var(--color-cyan);' },
                    { 'field': 'Action', 'value': 'AllowWL', 'style': 'color: var(--color-cyan);' },
                    { 'field': 'Action', 'value': 'AllowFGW', 'style': 'color: var(--color-cyan);' },
                ],
                'ParentFilename': [
                    { 'field': 'ParentCategory', 'value': 'Goodware', 'style': 'color: var(--color-green);' },
                    { 'field': 'ParentCategory', 'value': 'Malware', 'style': 'color: var(--color-red);' },
                    { 'field': 'ParentCategory', 'value': 'Pup', 'style': 'color: color: var(--color-cyan);' }
                ],
                'ParentPath': [
                    { 'field': 'ParentCategory', 'value': 'Goodware', 'style': 'color: var(--color-green);' },
                    { 'field': 'ParentCategory', 'value': 'Malware', 'style': 'color: var(--color-red);' },
                    { 'field': 'ParentCategory', 'value': 'Pup', 'style': 'color: var(--color-cyan);' } 
                ],
                'ParentPid': [
                    { 'field': 'ParentCategory', 'value': 'Goodware', 'style': 'color: var(--color-green);' },
                    { 'field': 'ParentCategory', 'value': 'Malware', 'style': 'color: var(--color-red);' },
                    { 'field': 'ParentCategory', 'value': 'Pup', 'style': 'color: var(--color-cyan);' }                    
                ],
                'ParentMd5': [
                    { 'field': 'ParentCategory', 'value': 'Goodware', 'style': 'color: var(--color-green);' },
                    { 'field': 'ParentCategory', 'value': 'Malware', 'style': 'color: var(--color-red);' },
                    { 'field': 'ParentCategory', 'value': 'Pup', 'style': 'color: var(--color-cyan);' }                    
                ],
                'ParentCategory': [
                    { 'field': 'ParentCategory', 'value': 'Goodware', 'style': 'color: var(--color-green);' },
                    { 'field': 'ParentCategory', 'value': 'Malware', 'style': 'color: var(--color-red);' },
                    { 'field': 'ParentCategory', 'value': 'Pup', 'style': 'color: var(--color-cyan);' }                    
                ],
                'ChildFilename': [
                    { 'field': 'ChildCurrentClassification', 'value': 'Goodware', 'style': 'color: var(--color-green);' },
                    { 'field': 'ChildCurrentClassification', 'value': 'Malware', 'style': 'color: var(--color-red);' },
                    { 'field': 'ChildCurrentClassification', 'value': 'Pup', 'style': 'color: var(--color-cyan);' }                    
                ],
                'ChildPath': [
                    { 'field': 'ChildCurrentClassification', 'value': 'Goodware', 'style': 'color: var(--color-green);' },
                    { 'field': 'ChildCurrentClassification', 'value': 'Malware', 'style': 'color: var(--color-red);' },
                    { 'field': 'ChildCurrentClassification', 'value': 'Pup', 'style': 'color: var(--color-cyan);' }                        
                ],
                'ChildPid': [
                    { 'field': 'ChildCurrentClassification', 'value': 'Goodware', 'style': 'color: var(--color-green);' },
                    { 'field': 'ChildCurrentClassification', 'value': 'Malware', 'style': 'color: var(--color-red);' },
                    { 'field': 'ChildCurrentClassification', 'value': 'Pup', 'style': 'color: var(--color-cyan);' }                        
                ],
                'ChildMd5': [
                    { 'field': 'ChildCurrentClassification', 'value': 'Goodware', 'style': 'color: var(--color-green);' },
                    { 'field': 'ChildCurrentClassification', 'value': 'Malware', 'style': 'color: var(--color-red);' },
                    { 'field': 'ChildCurrentClassification', 'value': 'Pup', 'style': 'color: var(--color-cyan);' }                        
                ],
                'ChildCurrentClassification': [
                    { 'field': 'ChildCurrentClassification', 'value': 'Goodware', 'style': 'color: var(--color-green);' },
                    { 'field': 'ChildCurrentClassification', 'value': 'Malware', 'style': 'color: var(--color-red);' },
                    { 'field': 'ChildCurrentClassification', 'value': 'Pup', 'style': 'color: var(--color-cyan);' }                        
                ],
                'ChildClassification': [
                    { 'field': 'ChildClassification', 'value': 'Goodware', 'style': 'color: var(--color-green);' },
                    { 'field': 'ChildClassification', 'value': 'Malware', 'style': 'color: var(--color-red);' },
                    { 'field': 'ChildClassification', 'value': 'Pup', 'style': 'color: var(--color-cyan);' }                        
                ]
            },
            'htmlColumns': {
                'EventTypeIcon': { 'headerName': '', 'width': 35 }
            }
        }  

        dashboard = nbDashboard(False, 'EN', layout=layout)
        dashboard.grid(_df, fixedargs=fixedargs, options=_gridopt, provides=provides)        
        dashboard.run()

################################
# BRICKS INITIALIZATION        #
################################

def get_bricks():
    bricks = BrickFactory()
    
    bricks.add_brick(BrickSQLQuery())
    bricks.add_brick(BrickPEDiskUpdates())

    bricks.add_brick(BrickFilename4Md5())
    bricks.add_brick(BrickMachine4Md5())
    bricks.add_brick(BrickUrl4Md5())
    bricks.add_brick(BrickMd5Info())
    bricks.add_brick(BrickOcurrencesPlot())

    bricks.add_brick(BrickMachine4Filename())
    bricks.add_brick(BrickMd54Client())
    bricks.add_brick(BrickMd54Filename())
    bricks.add_brick(BrickUrl4Filename())

    bricks.add_brick(BrickMachine4Url())
    bricks.add_brick(BrickUser4Url())
    bricks.add_brick(BrickFilename4Url())
    bricks.add_brick(BrickBlocks4Machine())

    bricks.add_brick(BrickIOAInfo())
    bricks.add_brick(BrickIOA4Machine())

    bricks.add_brick(BrickMd5Events())
    bricks.add_brick(BrickProcessTree())
    
    return bricks