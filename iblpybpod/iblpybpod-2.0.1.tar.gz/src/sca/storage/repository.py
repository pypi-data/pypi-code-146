import os, shutil
from pathlib import Path
from sca.formats import json, csv
from sca import format_flags as flags
from sca.utils.send2trash_wrapper import send2trash


class Repository(json.scadict):

    def __init__(self, path, data=None, uuid4_id=None, def_url=None, def_text=None, software=None, fileformat='json', parent=None):
        json.scadict.__init__(self, data, uuid4_id, def_url, def_text, software)

        self.parent     = parent  # parent repository
        self.fileformat = fileformat
        self.name       = os.path.basename(path)
        self.path       = os.path.abspath(path)
        
        self.children   = []    # children repositories
        self.updaterepo = False

    def __add__(self, repo):
        """
        Add a repository recursively
        """
        repo_location = repo.path[len(self.path):]
        repos_names   = [x for x in repo_location.split(os.sep) if len(x.strip())>0]

        if len(repos_names)==0: return self

        current = self
        for repo_name in repos_names[:-1]:
            r = None

            for tmp in current.children:
                if tmp.name==repo_name:
                    r = tmp
                    break

            if r is None:
                r = Repository( os.path.join(current.path, repo_name), parent=current )
                current.children.append(r)
            current = r

        current.children.append(repo)
        return self


    @property
    def updaterepo(self):
        if self._updaterepo: return True

        for child in self.children:
            if child.updaterepo: return True
        return False
        
    @updaterepo.setter
    def updaterepo(self, value):
        self._updaterepo = value

        # when the value is false reset all the childrens ##
        if value==False:
            for c in self.children:
                c.updaterepo = False
        ####################################################

    
    @property
    def path(self):
        if self._path is None: return None
        return os.path.join(self.parent.path, self._path) if self.parent else self._path
        
    @path.setter
    def path(self, value):
        self._path = os.path.relpath(value, self.parent.path) if self.parent else value

    #######################################################################
    ### IO Functions ######################################################
    #######################################################################


    def open(self):
        """
        Open a repository and all its children
        """

        # check the fileformat of the repository, it can be json or csv
        #print(self.path, self.name)
        settings_file = os.path.join(self.path, self.name+'.json')  
        if os.path.isfile(settings_file):

            self.fileformat = 'json'
            # for json format
            with open(settings_file, 'r') as jsonfile:
                data = json.load(jsonfile)
                self.update(data, update_meta=True)
        else: 
            # for csv format
            settings_file = os.path.join(self.path, self.name+'.csv')
            if os.path.isfile(settings_file):
                self.fileformat = 'csv'

                with open(settings_file, 'r') as csvfile:

                    # load the file header to get the uid
                    csvreader = csv.reader(csvfile)

                    try:
                        next(csvreader)
                    except StopIteration:
                        pass

                    data = {}
                    
                    if csvreader.uuid4:          data.update({flags.UUID4_FLAG:           csvreader.uuid4})
                    if csvreader.created_on:     data.update({flags.CREATED_ON_FLAG:      csvreader.created_on})
                    if csvreader.updated_on:     data.update({flags.UPDATED_ON_FLAG:      csvreader.updated_on})
                    if csvreader.software:       data.update({flags.SOFTWARE_REF_FLAG:    csvreader.software})
                    if csvreader.def_text:       data.update({flags.DEFINITION_TEXT_FLAG: csvreader.def_text})
                    if csvreader.def_url:        data.update({flags.DEFINITION_URL_FLAG:  csvreader.def_url})
                    if csvreader.parents:        data.update({flags.PARENT_REF_FLAG:      csvreader.parents})
                    if csvreader.externals:      data.update({flags.EXTERNAL_REF_FLAG:    csvreader.externals})
                    if csvreader.external_files: data.update({flags.EXTERNAL_FILE_FLAG:   csvreader.external_files})
                    if csvreader.external_urls:  data.update({flags.DEFINITION_URL_FLAG:  csvreader.external_urls})
                   
                    self.update(data, update_meta=True)

        #load all the subrepositories
        for folder_name in sorted( os.listdir(self.path) ):
            folder_path = os.path.join(self.path, folder_name)
            if not os.path.isdir(folder_path): continue

            repo = self.find(folder_path)
            if repo is None:
                self += Repository(folder_path, parent=self).open()
        return self

    
    def commit(self):
        """
        Save the repository settings
        """
        self.updaterepo = True

        #for child in self.children: child.commit()
        
        # check if the repository was renamed and rename it if so #####
        renamed = self.name!=os.path.basename(self.path)
        # only rename the path if it was created
        if renamed: self.renameto(self.name)
        ###############################################################


        # create the folder if it does not exists ############################################
        if not os.path.exists(self.path): Path(self.path).mkdir(parents=True, exist_ok=True)
        #####################################################################################
        
        if self.fileformat=='json': self.dump2json(self.name+'.json', self)


        for child in self.children:
            if not child.updaterepo:
                shutil.rmtree(child.path) if os.path.isdir(child.path) else os.remove(child.path)
                self.children.remove(child)

        if self.parent is None: self.updaterepo = False

        return self.path


    def dump2json(self, jsonfile, data):
        """
        Dump to the repository a object to a jsonfile
        """
        jsonfile_path = os.path.join(self.path, jsonfile)
        with open(jsonfile_path, 'w') as jsonfile:
            json.dump(data, jsonfile)
        return self.path



    #######################################################################
    ### Utils Functions ###################################################
    #######################################################################

    def list(self):
        return sorted([v for v in self.children], key=lambda x:x.name )


    def sub_repository(self, *args, **kwargs):
        """
        Create a child repository recursively
        """
        uuid4       = kwargs.get('uuid4',       None )
        fileformat  = kwargs.get('fileformat', 'json')
        
        # if the uuid4 argument is defined, the function will look
        # to the previous repository in the hierarchy for an existing repository
        # and return it
        if uuid4:
            subpaths    = os.path.join(*args[:-1])
            parent_repo = self.find( subpaths )
            if parent_repo is not None:
                for repo in parent_repo.list():
                    if repo.uuid4==uuid4:
                        repo.name = args[-1]
                        return repo

        # if no uuid4 was passed in the argument or no repo was found
        # then we create a new repository
        subpaths = os.path.join(*args)
        repo     = Repository( os.path.join(self.path, subpaths), fileformat=fileformat, parent=self )
        repo.add_parent_ref(self.uuid4)
        self += repo

        return repo

    def find_uuid4(self, path, uuid4):
        repo = self.find(path)
        for r in self.list():
            if r.uuid4==uuid4: return r
        return None

    def find(self, path):
        """
        Find a repository by the path
        """
        repo_location = path
        repos_names   = [x for x in repo_location.split(os.sep) if len(x.strip())>0]

        if len(repos_names)==0: 
            return self
        elif len(repos_names)==1:
            base_location = repos_names[0]
            for c in self.children:
                if c.name==base_location: return c
            return None
        else:
            base_location = repos_names[0]
            if base_location in self.children:
                for c in self.children:
                    if c.name==base_location: 
                        repo = c
                        break
                return repo.find(os.sep.join(repos_names[1:]))
        
        return None


    def renameto(self, newname):

        # rename the repository file to the new name
        oldname        = os.path.basename(self.path)
        old_configfile = os.path.join(self.path, oldname+'.'+self.fileformat)
        new_configfile = os.path.join(self.path, newname+'.'+self.fileformat)
        
        # rename the repository folder to the new name
        newpath = os.path.join( os.path.dirname(self.path), newname)
        
        if os.path.exists(old_configfile):  shutil.move( old_configfile, new_configfile )
        shutil.move( self.path, newpath )

        self.path = newpath
        self.name = newname



    def pprint(self, prefix=''):
        print(prefix, self.name, self.path)
        for r in self.list():
            r.pprint(prefix+'  ')
