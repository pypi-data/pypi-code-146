EMPTY_NODE = ""
ECHAD_EXT = """!function(){htmx.defineExtension("echad",{onEvent:function(t,e){if("htmx:beforeProcessNode"==t){let t=e.target.id,n=e.target.getAttribute("theme")||"vintage",s="data-"+t,a=document.getElementById(s);if(a){let e=JSON.parse(a.innerText),s=echarts.init(document.getElementById(t),n);echarts.getInstanceById(s.id).setOption(e)}else echarts.init(document.getElementById(t),n)}if("htmx:afterSwap"==t){let t=e.target.getAttribute("_echarts_instance_"),n=echarts.getInstanceById(t),s=e.detail.xhr.responseText,a=JSON.parse(s);n.setOption(a)}},transformResponse:function(t,e,n){let s=JSON.parse(t),a=n.getAttribute("_echarts_instance_");return echarts.getInstanceById(a).setOption(s),t}})}();"""
REL = "stylesheet"
JS_TYPE = "text/javascript"
JSON_TYPE = "application/json"


class CDN:
    HTMX = "https://cdnjs.cloudflare.com/ajax/libs/htmx/1.7.0/htmx.min.js"
    ECHARTS = "https://cdnjs.cloudflare.com/ajax/libs/echarts/5.3.1/echarts.min.js"
