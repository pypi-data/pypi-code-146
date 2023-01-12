#!/usr/bin/env python
# -*- coding: utf-8 -*-

# only needed for flexmin_test.py to replicate work done by web application
import re

def display(output):
    """
    Convert outputs without a display attribute into a display attribute
    """
    if not output.has_key('display'):
        display = []
        for item in ['note','table','text','task','edit','form']:
            if output.has_key(item):
                display.append( { item : output[item] })
                del output[item]
        output['display'] = display

    for item in output['display']:
        form(item)
        table(item)

def authenticate(request,output):
    """
    Check output to see if login is required, adjust output dictionary 
    accordingly
    """
    # Handle authentication errors
    if output.has_key('error'):
        if 'ERROR - Login Required' in output['error']:
            output['method'] = 'popup'
            output['title'] = 'Flexmin Login'
            output['text'] = output['error']
            output['login'] = 'flexmin_login.py'
            if "flexmin_login" in request.args[0]:
                # it is a login prompt
                # reload (based on browser path, as pane won't be updated yet).
                output['next_action'] = "reload"
            elif request.post_vars:
                # don't reload pane if form submit action was attempted as
                # form content will be lost forcing end user to re-enter
                output['next_action'] = "nothing"
            else:
                # no form submit, so no data to lose by reload
                output['next_action'] = "reload"
        else: # not an error prompting for login
            output['method'] = 'popup'
            output['title'] = 'Flexmin Login'
            output['text'] = output['error']

def form(output):
    """
    Process data in output['form'] so it is ready for view
    """
    # help out with some of the yaml in forms
    if output.has_key('form'):
        for field in output['form']['fields']:
            if field.has_key('select') and field.has_key('delimiter'):
                field['select'] = re.split(field['delimiter'],field['select'])
            if field.has_key('type') and field['type'] == "multiselect":
                # convert text field to list of check box values and labels
                cl = field['options'].split('\n')
                data = []
                for c in cl:
                    vl = c.split(";")
                    if len(vl)>1:
                        vd = {'value': vl[0],
                              'label': vl[1]}
                    else:
                        vd = {'value': vl[0],
                              'label': vl[0]}
                    data.append(vd)
                field['options'] = data
            # TODO selectformat is deprecated, to be removed when no scripts need it
            if field.has_key('selectformat'):
                if field['selectformat'] == 'spacesep':
                    field['select'] = re.split(r'\s',field['select'])
                elif field['selectformat'] == 'linesep':
                    field['select'] = re.split(r'\s*\n',field['select'])

def table(output):
    """
    Process data in output['table'] so it is ready for view
    """
    if output.has_key('table'):
        table = output['table']
        # get table rows (records)
        if table.has_key('delimiter_row'):
            table['data'] = re.split(table['delimiter_row'],table['data'])
        else:
            table['data'] = table['data'].splitlines()

        # Convert actions_bulk boolean into actions list for view porcessing
        if table.has_key('actions_bulk') and table.has_key('actions') and table['actions_bulk']:
            table['actions_bulk'] = table['actions'].split('.')

        # split rows into fields
        nd = []  # new data : list of table rows
        for r in table['data']:
            if table.has_key('delimiter'):
                if table.has_key('header'):
                    cn = len(table['header'])  # no. of columns
                    if table.has_key('actions') and table['actions'] == 'per_row':
                        pass  # allow for actions entry
                    else:
                        cn = cn - 1  # reduce split count as no actions entry
                    nr = re.split(table['delimiter'],r,cn)
                    nr = nr + [''] * (cn + 1 - len(nr))  # pad out to match no. of columns
                    # filter out excluded columns (header begins with -)
                    for i,h in enumerate(table['header']):
                        if h[0] == '-':
                            del nr[i]
                else:
                    nr = re.split(table['delimiter'],r)
            else:
                nr = [ r ]  # put in list on it's own

            if table.has_key('actions'):
                if table['actions'] == 'per_row':  # actions specified in row
                    # actions should be a list, but might be a string separated by .
                    if isinstance(nr[-1], basestring):
                        acts = nr[-1].strip().split('.')
                        nr[-1] = acts
                else:  # actions same for all rows
                    if isinstance(table['actions'], basestring):
                        acts = table['actions'].strip().split('.')
                    else:
                        acts = table['actions']
                    nr.append(acts)
            nd.append(nr)

        # filter out excluded columns
        if table.has_key('header'):
            nh = []
            for h in table['header']:
                if h[0] != '-':
                    nh.append(h)
            table['header'] = nh

        table['data'] = nd
