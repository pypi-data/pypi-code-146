import logging
logger = logging.getLogger(__name__)

import os

# load the environment variables for this setup
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

LOG_LEVEL = os.environ.get("LOG_LEVEL") or "INFO"

# setup logging infrastructure

# logging.getLogger("urllib3").setLevel(logging.WARN)

FORMAT  = "[%(asctime)s] [%(name)s] [%(process)d] [%(levelname)s] %(message)s"
DATEFMT = "%Y-%m-%d %H:%M:%S %z"

logging.basicConfig(level=LOG_LEVEL, format=FORMAT, datefmt=DATEFMT)
formatter = logging.Formatter(FORMAT, DATEFMT)

# adjust gunicorn logger to global level and formatting 
logging.getLogger("gunicorn.error").handlers[0].setFormatter(formatter)
logging.getLogger("gunicorn.error").setLevel(logging.INFO)
logging.getLogger("engineio.client").setLevel(logging.WARN)
logging.getLogger("engineio.server").setLevel(logging.WARN)
logging.getLogger("socketio.client").setLevel(logging.WARN)
logging.getLogger("socketio.server").setLevel(logging.WARN)

logging.getLogger().handlers[0].setFormatter(formatter)

from baseweb.config import app

app["baseweb-demo"] = {
  "a few" : "app specific",
  "configuration" : "settings"
}

# import baseweb server object to expose it from this application
from baseweb.web import server

from baseweb.security import add_authenticator

def authenticator(scope, request, *args, **kwargs):
  logger.debug("AUTH: scope:{} / request:{} / args:{} / kwargs:{}".format(
    scope, str(request), str(args), str(kwargs)
  ))
  return True

add_authenticator(authenticator)

from baseweb.interface import register_component, register_static_folder, register_external_script

HERE       = os.path.dirname(__file__)
COMPONENTS = os.path.join(HERE, "components")

register_static_folder(os.path.join(HERE, "static"))

register_component("app.js",        HERE)
register_component("SourceView.js", COMPONENTS)
register_component("logo.js",       COMPONENTS)

register_external_script("https://www.google.com/recaptcha/api.js?render=6LcbsOEjAAAAAABrd1kwa0eciF8AZK2v6vSTxRzZ")

from .pages            import index, page1, page2, page3, page4, page5
from .pages.components import CollectionView, PageWithBanner
