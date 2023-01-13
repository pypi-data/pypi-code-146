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
from openlp.core.api.lib import old_auth, old_success_response
from openlp.core.common.registry import Registry
from openlp.core.lib.plugin import PluginStatus, StringContent
from openlp.core.state import State

from flask import jsonify, Blueprint

core_views = Blueprint('old_core', __name__)


@core_views.route('/api/poll')
def poll():
    return jsonify(Registry().get('poller').poll())


@core_views.route('/api/display/<display>')
@old_auth
def toggle_display(display):
    ALLOWED_ACTIONS = ['hide', 'show', 'blank', 'theme', 'desktop']
    display = display.lower()
    if display in ALLOWED_ACTIONS:
        Registry().get('live_controller').slidecontroller_toggle_display.emit(display)
    return old_success_response()


@core_views.route('/api/plugin/search')
def plugin_list():
    searches = []
    for plugin in State().list_plugins():
        if plugin.status == PluginStatus.Active and plugin.media_item and plugin.media_item.has_search:
            searches.append([plugin.name, str(plugin.text_strings[StringContent.Name]['plural'])])
    return jsonify({'results': {'items': searches}})


@core_views.route('/main/image')
def main_image():
    img = 'data:image/jpeg;base64,{}'.format(Registry().get('live_controller').grab_maindisplay())
    return jsonify({'slide_image': img})
