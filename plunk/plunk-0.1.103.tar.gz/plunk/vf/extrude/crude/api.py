import os
from extrude import mk_api, run_api

from plunk.vf.extrude.crude import funcs, mall


_app = mk_api(funcs, mall)
api_url = _app.openapi_spec['servers'][0]['url']

if __name__ == '__main__':
    run_api(_app)
