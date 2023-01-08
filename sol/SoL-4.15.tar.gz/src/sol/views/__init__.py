# -*- coding: utf-8 -*-
# :Project:   SoL -- Views configuration
# :Created:   lun 15 apr 2013 11:42:48 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2013, 2014, 2018, 2020 Lele Gaifax
#

from functools import wraps
import logging

from metapensiero.sqlalchemy.proxy.json import register_json_decoder_encoder
from metapensiero.sqlalchemy.proxy.pyramid import expose
from rapidjson import Decoder, Encoder, DM_ISO8601, DM_NAIVE_IS_UTC, NM_NATIVE, NM_DECIMAL

from ..i18n import translatable_string as _, translator
from ..models.bio import save_changes


logger = logging.getLogger(__name__)


class LoggerAdapter(logging.LoggerAdapter):
    "Add username and remote IP to the logged message"

    def process(self, msg, kwargs):
        extra = self.extra
        msg = "[%s@%s] " % (extra['user'], extra['ip']) + msg
        return msg, kwargs


def get_request_logger(request, logger):
    "Get a specialized `logger` for a Pyramid `request`"

    extra = dict(
        ip=request.client_addr,
        user=request.session.get('user_name') or 'anonymous')
    return LoggerAdapter(logger, extra)


def unauthorized_for_guest(f):
    """Prevent `guest` users to perform the operation."""

    @wraps(f)
    def wrapper(request):
        t = translator(request)

        log = get_request_logger(request, logger)

        if 'user_name' in request.session:
            if not request.session['is_guest']:
                return f(request)

            message = t(_(
                'Guest users are not allowed to perform this operation, sorry!'))
        else:
            message = t(_('You must logon to perform this operation!'))

        log.warning('Not allowed to perform %s', f.__name__)

        return dict(success=False, message=message)

    return wrapper


json_decode = Decoder(datetime_mode=DM_ISO8601,
                      number_mode=NM_NATIVE).__call__
"Custom JSON decoder."


json_encode = Encoder(datetime_mode=DM_ISO8601 | DM_NAIVE_IS_UTC,
                      number_mode=NM_NATIVE | NM_DECIMAL,
                      ensure_ascii=False).__call__
"Custom JSON encoder."


register_json_decoder_encoder(json_decode, json_encode)
expose.create_session = staticmethod(lambda request: request.dbsession)
expose.save_changes = staticmethod(save_changes)
