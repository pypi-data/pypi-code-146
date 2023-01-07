'''Assetto Corsa Websocket Protocol Class'''

import json

from ac_websocket_server.objects import EnhancedJSONEncoder


class Protocol:
    '''Google JSON style protocol factory'''

    @classmethod
    def success(cls, data: any = None, msg: str = None) -> str:
        '''Return a success response with data or data message'''
        if msg:
            return json.dumps({'data': {'msg': msg}},
                              cls=EnhancedJSONEncoder, indent=4)
        return json.dumps({'data': data},
                          cls=EnhancedJSONEncoder, indent=4)

    @classmethod
    def error(cls, error: any = None, msg: str = None) -> str:
        '''Return an error response with error or error message'''
        if msg:
            return json.dumps({'error': {'msg': msg}},
                              cls=EnhancedJSONEncoder, indent=4)
        return json.dumps({'error': error},
                          cls=EnhancedJSONEncoder, indent=4)
