#!/usr/bin/python3
""" Command-line Mastodon tool """

# Copyright (C) 2022 Gwyn Ciesla

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from bs4 import BeautifulSoup

def dehtml(html_input):
    """ Drop any html tags """
    soup = BeautifulSoup(html_input, 'html.parser')
    return soup.get_text()

def display_status(mastodon, toot, cws):# pylint: disable=too-many-locals
    """ Display toot information """
    tid = toot.get('id')
    if toot.get('favourited'):
        faved = ' *'
    else:
        faved = ' '
    if toot.get('reblogged'):
        boosted = ' Boosted'
    else:
        boosted = ' '

    context = mastodon.status_context(tid)
    anc_num = len(context.get('ancestors'))
    if anc_num > 0:
        anc = ' vvv ' + str(anc_num)
    else:
        anc = '------'
    dec_num = len(context.get('descendants'))
    if dec_num > 0:
        dec = str(dec_num) + ' ^^^ '
    else:
        dec = '------'

    header = '--' + anc + '---ID: ' + str(tid) + ' ---' + dec + '--' + faved + boosted
    acct = toot.get('account').get('acct')
    disp_name = toot.get('account').get('display_name')
    url = str(toot.get('url'))
    if url == 'None':
        url = ''
    print(header + ' | ' + disp_name + '(' + acct + ') | ' + \
        str(toot.get('created_at').astimezone().ctime()) + ' | ' + url)

    if toot.get('spoiler_text'):
        print('CW: ' + toot.get('spoiler_text'))
        print('------------------------------')
    if not toot.get('spoiler_text') or cws:
        print(dehtml(toot.get('content')))
        media = list(toot.get('media_attachments'))
        for media_item in media:
            print(media_item.get('type') + ': ' + media_item.get('url'))
    print('\n')

def display_user(uacct):
    """ Display user information """
    print(uacct.get('display_name') + '(' + uacct.get('acct') + \
        ') : ' + uacct.get('display_name') + \
                ' : ' + uacct.get('url'))
