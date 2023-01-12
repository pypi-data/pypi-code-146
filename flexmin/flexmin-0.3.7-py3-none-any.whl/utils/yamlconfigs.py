#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
General purpose module for opening yaml versions of config files and
generating the applications native version of the file.

Currently only supports NGINX configuration files (limited testing so far)
"""

import os, yaml, re, shutil

class EasyDict(dict):
    """
    Dictionary, but with added resolve method which provides a safe method to
    get a value from a dictionary 'tree'.
    
    TODO extend to enumerate lists and convert any dictionies within to EasyDict
    """
    def __init__(self, d=None):
        if type(d) is dict:
            if d is not None: self.update(d)
            # convert any nested dictionaries
            for k in self:
                if type(self[k]) is dict:
                    self[k] = EasyDict(self[k])

    def resolve(obj, path, default=None):
        """
        Safe way to find a value within a nested dictionary.
        Instead of throwing an error if the keys don't exist, it returns None 
          or a default value if supplied.
        x.resolve('a.b.c','not found') will find obj['a']['b']['c'] within nested 
          dictionary or return 'not found' if any of these keys don't exist.
        """
        for name in path.split("."):
            if name in obj:
                obj = obj[name]
            else:
                obj = default
                break
        return obj

class Config():

    def __init__(self,src_file,params=None):
        """
        load specified yaml config file
        src_file = path of yaml file
        params = dictionary of parameters to substitue in source
        
        """
        self.source = src_file
        self.source_local = re.sub(r'^(.*)\.yaml',r'\1.local.yaml',src_file)
        self.params = params
        if os.path.isfile(self.source):
            with open(self.source,'r') as src:
                src_text = src.read()
        else:
            self.data = {}
            return False
            
        if os.path.isfile(self.source_local):
            with open(self.source_local,'r') as src:
                src_local_text = src.read()
        else:
            src_local_text = 'source: []'

        #params = {"condition1": "", "condition2": "text"} # define desired replacements here

        if params:
            # create regex, enclosing variable in {}
            params = dict((re.escape('{'+k+'}'), v) for k, v in params.items()) 
            # compile regexes
            pattern = re.compile("|".join(params.keys()))
            # do replacement
            #print("Initial yaml source:" + src_text)
            out_text = pattern.sub(lambda m: params[re.escape(m.group(0))], src_text)
            out_local_text = pattern.sub(lambda m: params[re.escape(m.group(0))], src_local_text)
            #print("Final yaml source:" + out_text)
        else:
            # no changes to source text
            out_text = src_text
            out_local_text = src_local_text

        self.data = EasyDict(yaml.load(out_text, Loader=yaml.SafeLoader))
        self.data_local = EasyDict(yaml.load(out_local_text, Loader=yaml.SafeLoader))
        

    def find(self,key=None,value='.*',obj=None,path=[],pkey=None,found=[]):
        """
        Find key and/or value within yaml config
            obj = object to search, normally not specified as it will search the loaded config
            key = dictionary key within object
            value = regex to match required value string, defaults to wildcard match anything
            path = path to this object within original object
            pkey = key of this object within parent, if parent was a dict
        Returns a list of paths, the paths are themselves a list of keys and indexes 
        e.g. ['a',3,'b',2] which means self.config['a'][3]['b'][2] will get the relevant value
        """
        x = None
        if not obj:
            obj = self.config
        lf = []
        if type(obj) is dict:
            if key and key in obj: # object has matching key
                if (type(obj[key]) is str):
                    if re.match(value,obj[key]):  # == value:
                        #print "found1:", [path + [key]]
                        lf = lf + [path + [key]]
                else: # i
                    x = self.find(obj[key],key=key,value=value,path=path+[key],pkey=key)
                    if x:
                        lf = lf + x
            else: # no matching key, search object children
                for i in obj:
                    if (not key) and (type(obj[i]) is str): 
                        # no key specified just looks for matching value
                        if re.match(value,obj[i]): # == value:
                            #print "found2:", [path + [i]]
                            lf = lf + [path + [i]]  # found
                    else:
                        x = self.find(obj[i],key=key,value=value,path=path+[i])
                        if x:
                            lf = lf + x
            return lf  # not found
        elif type(obj) is list:
            for i,j in enumerate(obj):  # i=index, j=list item
                if (type(j) is str):
                    if pkey and re.match(value,j):  # checking value match in matched key's child list
                        #print "found3:", [path + [i]]
                        lf = lf + [path + [i]]
                    elif not key and re.match(value,j):  # check value anyway if no key specified
                        #print "found4:", [path + [i]]
                        lf = lf + [path + [i]]

                else: # not a string so search object children
                    x = self.find(j,key=key,value=value,path=path+[i])
                    if x:  # exit loop and return if found it
                        lf = lf + x
            return lf


    def native(self,destination=None,params=None):
        """
        Convert yaml based config to it's native format. Reads 'type' value from
        the yaml data to determine what format is to be generated. 
        
        destination = explicit path for output file

        Types supported:
        - nginx: nginx configuration format
        - shell-vars: output shell variable names and values to shell script
        """
        # use destination specified in yaml file if none specified in call
        if 'destination' in self.data:
            for d in self.data['destination']:
                doctype = d['type']
                destination = d['path']
                #print("Writing out to: " + destination)
                if doctype == 'nginx':
                    lines = self.to_nginx()
                if doctype == 'fm-menu':
                    lines = self.to_menu()
                elif doctype == 'ini':
                    lines = self.to_ini(d)
                elif doctype == 'shell-vars':
                    lines = self.to_shellvars(d)
                elif doctype == 'python-vars':
                    lines = self.to_pythonvars(d)

                with open(destination,'w') as dst:
                    dst.write('\n'.join(lines))
            #for l in lines:
            #    print l
            
    def to_menu(self):
        #destopts = EasyDict(destopts)
        #dest = destopts.resolve('path',None)
        source = self.data.resolve('source',{})
        source_local = self.data_local.resolve('source',{})
        #print("source: " + str(source))
        out_lines = ['# Managed by flexmin yaml file, do not edit here']
        
        self._menu_local(source_local)   # prepare local menu for cross referenceing
        group_local_list = []
        
        num = 1
        menu_len = len(source)
        
        # process groups from main menu (source) and local menu file (source_local)
        for m in source + source_local:

            data = m['group'].split(';')
            section = dict()
            tasks = []
            group = data[0]
            
            # skip this group if already processed (local group merged with main group)
            if group in group_local_list:
                num += 1
                continue
            
            m_local = self._menu_local_get(group)
            data_local = m_local['group'].split(';')
            
            # if local group data found then we are merging groups 
            if data_local:
                group_local_list.append(group)  # don't process this local group later

            if len(data_local) > 2:
                data = data_local   # use menu local group definition if 3 items specified
                data[1] = '+' + data[1]  # prefix with + to indicate a local group setting
                
            if 'active' in m_local and not m_local['active']:
                pass  # skip if local config says not active
                num += 1
            elif not 'active' in m_local and 'active' in m and not m['active']:
                pass  # skip if not specified in local, and main config says not active
                num += 1
            else:
                # If this group doesn't pass the specified checks, skip it
                if not self._menu_checks(m, m_local):
                    continue  # abandon this iteration of group
                                                                  
                line_data = ['0']
                if len(data)>1:
                    line_data.append(data[1])   # item name
                if len(data)>2:
                    line_data.append(data[2])   # icon filename
                else:
                    line_data.append('')
                    
                line_data.append('')   # action script, not for group
                
                if len(data)>3:
                    line_data.append(data[3])   # description
                else:
                    line_data.append('')
                    
                out_lines.append(";".join(line_data))
                
                if num < menu_len:  # if working on original main menu items 
                    task_local_list = []
                    # process items from main menu config while checking local
                    if 'tasks' in m:
                        for item in m['tasks']:
                            task = item['item'].split(';')
                            #print(f"{num} {menu_len} task: {task}")
                            task_script = task[0]
                            
                            # Check if we should use menu local task item details
                            item_local = self._menu_local_get(group, task_script)
                            task_local = item_local['item'].split(';')
                            #if task_script == 'sys_general.sh':
                            #    print("item_local: " + str(item_local))
                            #    exit(1)
                            if len(task_local) > 2:
                                task = task_local  # use menu local copy of task item
                                task_local_list.append(task_script)  # record that this local task item has been used
                                line = self._menu_task_line(task, local=True)                            
                            else:
                                line = self._menu_task_line(task, local=False)
                            if line: out_lines.append(line)
                    num += 1
                                            
                # Process task items that only exist in local menu copy
                if 'tasks' in m:
                    for item in m_local['tasks']:
                        task = item['item'].split(';')
                        #print("l_task: " + str(task))
                        line = self._menu_task_line(task, task_local_list, local=True)
                        if line: out_lines.append(line)

        
        return out_lines
    
    def _menu_group_process(self, group, exclude_list=[]):
        pass
    
    def _menu_task_line(self, task, exclude_list=[], local = False):
        """
        Generate the line for individual tasks in menu
        """
        if local:
            prefix = '+'
        else:
            prefix = ''
        line_data = ['1']
        if len(task)>0:
            if task[0] in exclude_list:
                return ''
            else:
                line_data.append(prefix + task[1])   # item name
        line_data.append('')  # no icon for task entry
        if len(task)>0:
            script = task[0]
            # Filtering menu happens in Flexmin Service now
            """
            if 'FM_SCRIPTS' in self.params:
                script_path = os.path.join(self.params['FM_SCRIPTS'], script)
                if not os.path.isfile(script_path):
                    return ''   # skip this item as specified script does not exist
            """
            line_data.append(script)   # action script
            if len(task)>2:
                line_data.append(task[2])   # description
            else:
                line_data.append('No description')
        else:
            line_data.append('no_script.sh')  # action script
            line_data.append('No script specified in menu configuration')  # description
            
        return ";".join(line_data)
   
    
    def _menu_local(self, menu):
        """
        Enumerate groups and items in local menu, return a dictionary like this:
        
        {'system': {'index': 0, 'tasks': {'sys_general.sh': 0, 'sys_time.sh': 1} },
         'network': {'index': 1, 'tasks': { ... } } }
        """
        ref = EasyDict({})
        for i, group in enumerate(menu):
            kg = group['group'].split(';')[0]      # group identifier
            ref[kg] = EasyDict({'index': i,  # which item holds this group
                                'tasks': {}}) # items will hold index of items
            for j, item in enumerate(group['tasks']):
                ki = item['item'].split(';')[0]
                ref[kg]['tasks'][ki] = i

        self.menu_local = menu
        self.menu_local_ref = ref


    def _menu_local_get(self, group, task=None):
        """
        Find the relevant group details and task details if specified
        """
        mli = self.menu_local_ref.resolve(group + ".index",None)
        if not mli is None:
            m_local = self.menu_local[mli]  # equivalent group in local
        else:
            if task:
                return {'item': ''}
            else:
                return {'group': '', 'tasks': []}

        if not task: # return menu group if task not specified
            return m_local
        else:  # track down task item from local menu and return that
            #print("local_menu: " + str(self.menu_local))
            #print("local_ref: " + str(self.menu_local_ref))
            try:
                tli = self.menu_local_ref[group]['tasks'][task]
                t_local = self.menu_local[mli]['tasks'][tli]
            except:
                t_local = {'item': ''}
            return t_local
            
    
    def _menu_checks(self, item, item_local={}):
        """
        Looks at check_ properties of current item and carries out the required
        checks return True of all passed or False if any fail.
        """

        # if any checks specified locally, use the checks in the local item
        if ( ('check_executable' in item_local) or
             ('check_file' in item_local) or
             ('check_folder' in item_local)
           ):
            item = item_local
            
        pass_checks = True
        if 'check_executable' in item:
            if not shutil.which(item['check_executable']): pass_checks = False
        if 'check_file' in item:
            # Look for any of the files listed, if one found then okay
            found_file = False
            for f in item['check_file']:
                if os.path.isfile(f): found_file = True
            if not found_file:
                pass_checks = False  # none of the files found, fail
        if 'check_folder' in item:
            # Look for any of the folders listed, if one found then okay
            found_folder = False
            for f in item['check_folder']:
                if os.path.isdir(f): found_folder = True
            if not found_folder:
                pass_checks = False  # none of the folders found, fail
        return pass_checks

            
    def to_ini(self, destopts):
        destopts = EasyDict(destopts)
        method = destopts.resolve('method','replace')
        dest = destopts.resolve('path',None)
        source = self.data.resolve('source',{})
        out_message = '# Managed by flexmin yaml file, do not edit here'
        if method == 'insert':
            insert = True
            start = re.compile(destopts.resolve('insert_start','^#.-{2,}.*'))
            end = re.compile(destopts.resolve('insert_end','^#.-{2,}.*'))
            #print("Insert")
        else:
            insert = False
        if method == 'merge':
            merge = True
        else:
            merge = False
            
        out_lines = []
        before_lines = []
        after_lines = []
        
        if merge:
            # get list of ini sections (groups) included in this yaml
            groups = {}
            current_group = ''
            if 'groups' in source:
                for i, group in enumerate(source['groups']):
                    if 'name' in group:
                        groups[group['name']] = i  # store name and index in dict
            
            # open destination file for processing
            if dest and os.path.isfile(dest):
                dst = open(dest,'r')
            else:
                dst = []
                
            section = re.compile('^\s*\[\s*([a-zA-Z0-9_\- ]+?)\s*\]\s*$')
            
            # process existing sections
            for line in dst:
                line = line.strip('\n').strip()
                m = section.match(line)
                if m:  # it is a section header
                    if m[1] in groups:  # handled by yaml config
                        print("Recognised group: " + m[1])
                        current_group = m[1]   # name of section handled by yaml
                        # get dictionary for this group from source group list
                        group_dict = source['groups'][groups[current_group]]
                        # insert generated lines for this group
                        out_lines = out_lines +\
                                    self.to_ini_section(group_dict, destopts, out_message)
                        del groups[current_group]  # remove from dictionary
                    else:
                        print("Original group: " + m[1])
                        current_group = ''  # by setting current_group to '' we output it as is
                        
                # if not handling this group duplicate lines in to output
                if not current_group:  # not handling group from yaml
                    if line != out_message:
                        out_lines.append(line)
            
            # add blank line if last line was not blank and we are planning to add more sections
            if line != "" and len(group) > 0:
                out_lines.append("")
                        
            # if groups not found, add them at the end
            for group, index in groups.items():
                group_dict = source['groups'][index]
                out_lines = out_lines +\
                            self.to_ini_section(group_dict, destopts, out_message)
            
            # close file if we opened it
            if dest and os.path.isfile(dest):
                dst.close()
                
            # kepp end of file tidy by removing last blank lines
            if len(out_lines) > 1 and out_lines[-1] == "":
                del out_lines[-1]  
        
        if insert:
            # Section inserted into destination file
            if dest and os.path.isfile(dest):
                dst = open(dest,'r')
            else:
                dst = []
            before = True
            after = False
            # get original output file (excluding bit between start and end insert
            for line in dst:
                line = line.strip('\n').strip()
                if before:
                    before_lines.append(line)
                    #print("before: " + line)
                    if start.search(line):
                        before_lines.append("")
                        before = False
                elif not after:
                    if end.search(line):
                        after_lines.append(line)
                        #print("after: " + line)
                        after = True
                else:
                    after_lines.append(line)
                    #print("after: " + line)
                    
            # close file if opened
            if dest and os.path.isfile(dest):
                dst.close()

        if not merge:
            if 'groups' in source:
                for group in source['groups']:
                    out_lines = out_lines + self.to_ini_section(group, destopts, out_message)
            
        return before_lines + out_lines + after_lines
                        
    def to_ini_section(self, group, destopts, group_message=''):
        """
        Return a section of ini file with a section name and a set of values
        as a list of lines
        """
        if group_message:
            out = [group_message]  # first output line is the yaml group header message
        else:
            out = []
        group = EasyDict(group)
        group_active = group.resolve('active', True)    # if not active, we will exclude from output
        group_name = group.resolve('name', 'no_name')
        
        if group_active:
            separator = destopts.resolve('separator',' = ')
            group_type = group.resolve('type', group_name)  # if group type not specified use name
            
            # group name not mandatory, it might be desirable to group 
            # settings together that do not officially belong in a separate group
            if group_name and group_name != 'no_name':
                out.append('[{}]'.format(group_name))
                
            for settings in group.resolve('settings',[]):
                #print("Settings: " + str(settings))
                try:
                    for k, v in settings.items():
                        v_type = self.data.resolve('metadata.' + group_type + '.' + str(k) + '.type','')
                        # if a single value, convert to list
                        if not type(v) is list:
                            v = [v]
                        for i in v:
                            if v_type == 'quoted':
                                out.append(str(k) + separator + "'" + str(i) + "'")
                            else:
                                out.append(str(k) + separator + str(i))
                except:
                    out.append("# YAML Config - error processing: " + str(settings))
                    
        else:
            # Flag up ignore group
            out.append("# Ignored [" + group_name + "] marked as inactive in yaml source")

        out.append("")
                    
        return out  #lines
        
                
    def to_pythonvars(self,destopts):
        lines = ["# Generated from YAML at: " + self.source,
                 "# Do not edit this file, edit YAML source file instead",
                 ""]
        destopts = EasyDict(destopts)
        parent = destopts.resolve('parent',None)
        if parent:
            lines.append("%s = {}" % parent)
            strTemplate = "%s['{}'] = '{}'" % parent
            numTemplate = "%s['{}'] = {}" % parent
        else:
            strTemplate = "{} = '{}'"
            numTemplate = "{} = {}"
        for k in self.data.resolve('source',{}):
            value = self.data.resolve('source.'+k+'.value')
            if type(value) is str:
                varline = strTemplate.format(k,value)
            else:
                varline = numTemplate.format(k,value)
            lines.append(varline)
        lines.append('')
        return lines

    def to_shellvars(self,destopts):
        destopts = EasyDict(destopts)
        insert = destopts.resolve('insert',None)
        dest = destopts.resolve('path',None)
        if insert:
            insert = True
            start = re.compile(destopts.resolve('insert_start','^#.-{2,}.*'))
            end = re.compile(destopts.resolve('insert_end','^#.-{2,}.*'))
            print("Insert")
        else:
            insert = False
        out = []
        inserting = False
        """
        # Old way, section inserted into common.sh script
        if dest:
            with open(dest,'r') as dst:
                for line in dst:
                    line = line.strip('\n')
                    if not inserting:
                        out.append(line)
                    if insert and start.search(line):
                        print("begin insert")
                        inserting = True
                        for k in self.data.resolve('source',{}):
                            value = self.data.resolve('source.'+k+'.value')
                            if type(value) is str:
                                varline = "export {}='{}'".format(k,value)
                            else:
                                varline = "export {}={}".format(k,value)
                            out.append(varline)
                    if insert and end.search(line):
                        print("end insert")
                        inserting = False
                        out.append(line)
        """
        out.append('# Main shell parameters file')
        out.append('# Managed by flexmin application, do not edit here')
        for k in self.data.resolve('source',{}):
            value = self.data.resolve('source.'+k+'.value')
            if type(value) is str:
                varline = "export {}='{}'".format(k,value)
            else:
                varline = "export {}={}".format(k,value)
            out.append(varline)
        return out  #lines

    def to_nginx(self):
        lines = ["# Generated from YAML at: " + self.source,
                 "# Managed config file, do not edit this file",
                 ""]
        lines = lines + self.render_nginx(self.data['source'],0)
        lines.append('')
        return lines

    def render_nginx(self,obj,level,key=None, context=None, terminator=";"):
        # obj = dictionary like object
        # level = how deep into the hierarchy we are (for output indentation)
        # key = key of this obj within parent object.
        lines = []
        
        if key and (type(obj) is list):
            if key == 'upstream':  # upstream servers block
                for li in obj:
                    lines.append("  "*level + key + " " + li['name'] + " {")
                    del li['name'] # don't process name as directive
                    lines = lines + self.render_nginx(li,level+1)
                    lines.append("  "*level + "}")
                    
            elif key == 'server':
                # server block, not a block if within upstream definition block
                for li in obj:
                    if (type(li) is dict) or (type(li) is EasyDict):
                        lines.append("  "*level + key + " {")
                        lines = lines + self.render_nginx(li,level+1)
                        lines.append("  "*level + "}")
                    else:
                        lines.append("  "*level + key + " " + str(li) + ";")
                        
            elif key == 'location': # location block
                # obj is a list of locations (each one a dict)
                for li in obj:
                    lines.append("  "*level + key + " " + li['path'] + " {")
                    if 'comment' in li:
                        lines.append("  "*(level+1) + "# " + li['comment'])
                        del li['comment'] # used comment, don't process again
                    lines.append
                    del li['path'] # don't process path as directive
                    lines = lines + self.render_nginx(li,level+1)
                    lines.append("  "*level + "}")
                    
            elif key == 'access':   # access control list
                # go through each item and render line entry for each
                lines.append("")  # add break before the set of network access control lines
                lines.append("  "*(level) + "# Network access control")
                for d in obj:
                    lines = lines + self.render_nginx(d,level)
                    

            else: # not a block, list of parameters/directives
                for li in obj:
                    #print "l:", level, "k:", key, "o:", obj
                    if (type(li) is dict) or (type(li) is EasyDict):
                        # not a block so no extra indentation
                        if 'PROXY_FOR' in li:
                            lines.append("  "*level + key + " PROXY_FOR " + str(li['PROXY_FOR'] + ';'))
                        else:
                            lines.append("  "*level + key + " ? " + str(li))
                        # passes dict with context='uwsgi_param' level=2
                        #self.render_nginx(li,level,context=key)
                    else:
                        lines.append("  "*level + key + " " + str(li) + ";")
        # this elif allows for EasyDict not converting dicts within lists to EasyDict
        elif (type(obj) is EasyDict) or (type(obj) is dict):
            if context:
                context = context + ' '
            else:
                context = ''
            for key in obj:
                if type(obj[key]) is list:
                    # if list probably needs to be supplied key
                    lines = lines + self.render_nginx(obj[key],level,key=key)
                else:
                    # just a set of directives and values
                    if key == 'comment':
                        lines.append("  "*level + "# " + str(obj[key]) + ";")
                    if key == 'literal':   # direct nginx code
                        # go through each item and render line entry for each
                        lines.append("")
                        lines.append("  "*(level) + "# NGINX directives")
                        for line in obj[key].split('\n'):
                            lines.append("  "*level + line)

                    else:
                        lines.append("  "*level + context + key + " " + str(obj[key]) + ";")
        return lines
