# -*- coding: utf-8 -*-

##########################################################################
# OpenLP - Open Source Lyrics Projection                                 #
# ---------------------------------------------------------------------- #
# Copyright (c) 2008-2023 OpenLP Developers                              #
# ---------------------------------------------------------------------- #
# This program is free software: you can redistribute it and/or modify   #
# it under the terms of the GNU General Public License as published by   #
# the Free Software Foundation, either version 3 of the License, or      #
# (at your option) any later version.                                    #
#                                                                        #
# This program is distributed in the hope that it will be useful,        #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
# GNU General Public License for more details.                           #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
# along with this program.  If not, see <https://www.gnu.org/licenses/>. #
##########################################################################
import logging
from openlp.core.api.lib import login_required
from openlp.core.common.registry import Registry
from openlp.core.lib.plugin import PluginStatus, StringContent
from openlp.core.state import State

from flask import jsonify, request, abort, Blueprint

core = Blueprint('core', __name__)
log = logging.getLogger(__name__)


@core.route('/display', methods=['POST'])
@login_required
def toggle_display():
    ALLOWED_ACTIONS = ['hide', 'show', 'blank', 'theme', 'desktop']
    data = request.json
    if not data:
        log.error('Missing request data')
        abort(400)
    display = data.get('display', '').lower()
    if display not in ALLOWED_ACTIONS:
        abort(400)
    Registry().get('live_controller').slidecontroller_toggle_display.emit(display)
    return '', 204


@core.route('/plugins')
def plugin_list():
    searches = []
    for plugin in State().list_plugins():
        if plugin.status == PluginStatus.Active and plugin.media_item and plugin.media_item.has_search:
            searches.append({'key': plugin.name, 'name': str(plugin.text_strings[StringContent.Name]['plural'])})
    return jsonify(searches)


@core.route('/system')
def system_information():
    data = {}
    data['websocket_port'] = Registry().get('settings_thread').value('api/websocket port')
    data['login_required'] = Registry().get('settings_thread').value('api/authentication enabled')
    return jsonify(data)


@core.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data:
        log.error('Missing request data')
        abort(400)
    username = data.get('username', '')
    password = data.get('password', '')
    if username == Registry().get('settings_thread').value('api/user id') and \
            password == Registry().get('settings_thread').value('api/password'):
        return jsonify({'token': Registry().get('authentication_token')})
    else:
        log.error('Unauthorised Request for ' + username)
        return '', 401


@core.route('/live-image')
def main_image():
    controller = Registry().get('live_controller')
    img = 'data:image/jpeg;base64,{}'.format(controller.grab_maindisplay())
    return jsonify({'binary_image': img})
