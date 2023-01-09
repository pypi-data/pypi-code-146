import os
from extrude import mk_api, run_api
from py2http.decorators import handle_form_req, send_binary_resp
from i2 import Sig

from plunk.vf.extrude.edge_impulse_like import tag_wf, get_tagged_wf, mall


@handle_form_req
@Sig(tag_wf)
def tag_wf_input_handler(**kwargs):
    return kwargs


@send_binary_resp
def get_tagged_wf_output_handler(output, **input_kwargs):
    return output


handlers = [
    dict(endpoint=tag_wf, input_mapper=tag_wf_input_handler,),
    dict(endpoint=get_tagged_wf, output_mapper=get_tagged_wf_output_handler,)
    # get_tagged_wf
]
_app = mk_api(handlers, mall)
api_url = _app.openapi_spec['servers'][0]['url']


if __name__ == '__main__':
    run_api(_app)
