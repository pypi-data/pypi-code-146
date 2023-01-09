from extrude import mk_web_app
from front import APP_KEY

from plunk.vf.extrude.crude import funcs
from plunk.vf.extrude.crude.api import api_url


if __name__ == '__main__':
    app = mk_web_app(funcs, api_url=api_url, config={APP_KEY: {'title': 'Crude App'},})
    app()
