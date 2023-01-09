from wdb.ext import WdbMiddleware, add_w_builtin

from .wsgi import application

add_w_builtin()
application = WdbMiddleware(application, start_disabled=True)
