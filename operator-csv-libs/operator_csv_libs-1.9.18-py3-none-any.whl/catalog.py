import os
import sys
import logging
import json
from operator import itemgetter
from natsort import natsorted

# Setup logging to stdout
log = logging.getLogger(__name__)
out_hdlr = logging.StreamHandler(sys.stdout)
out_hdlr.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s', '%Y-%m-%d %H:%M:%S'))
out_hdlr.setLevel(logging.INFO)
log.addHandler(out_hdlr)
log.setLevel(logging.INFO)

'''
Base Class for Catalog Exceptions
'''
class CatalogError(Exception):
    pass


'''
Class for interacting with File based Catalog files
'''
class Catalog:
    #Constructor function for the Catalog class
    def __init__(self, file, indent=4):
        #Initialize some class variables for the Catalog class
        self.channels = []
        self.package = ''
        self.bundles = []
        self.indent = indent

        #If the provided path does not exist, then raise an exception
        if not os.path.exists(file):
            raise CatalogError(f"Catalog path does not exist: {file}")

        #Read in catalog data from a single catalog file, formatted as a json stream
        if os.path.isfile(file):
            self._load_catalog_from_json_stream_file(file)
        #Read in data from a directory of json files
        elif os.path.isdir(file):
            #Detect whether there is just one, or multiple files in the directory
            #If there is just one file in the directory, chances are it's a catalog.json
            #Therefore, in this case we try to load it from the file instead of the directory
            files_in_dir = os.listdir(file)
            if len(files_in_dir) == 1:
                self._load_catalog_from_json_stream_file(f"{file}/{files_in_dir[0]}")
            else:
                self._load_catalog_from_directory(file)

    #Load the Catalog object using a single json stream file
    def _load_catalog_from_json_stream_file(self, file):
        #Note that the catalog.json file is expected to be formatted as a json stream
        with open(file) as stream:
            #Initialize some variables for reading the json stream
            separators = []
            lines = stream.readlines()
            count = 0
            startValue = 0

            #Loop through the lines in the file and determine the length in lines of each json object
            for line in lines:
                if line == '}\n' or line == '}':
                    separators.append(count)
                count += 1

            #Use the length readings from above to loop back through and read in each json object
            for s in separators:
                #Load the nth json object
                data = json.loads(''.join(lines[startValue:s+1]))

                #Sanity check whether there is an olm schema value, if not then the json is invalid
                if 'schema' not in data:
                    raise CatalogError(f"Cannot find a schema value in {data}")

                #Read in the olm package object
                if data['schema'] == 'olm.package':
                    #Sanity check whether there are multiple packages, if so then this is invalid json
                    if self.package != '':
                        raise CatalogError(f"There are multiple package objects in your catalog file, but only one is expected.")
                    #Store the package object
                    self.package = data
                #Read in an olm channel object
                elif data['schema'] == 'olm.channel':
                    self.channels.append(data)
                #Read in an olm bundle object
                elif data['schema'] == 'olm.bundle':
                    self.bundles.append(data)

                #Increment the start value function to the initial line index of the next json object
                startValue = s+1
    
    #Load the Catalog object using multiple catalog files in a single directory
    def _load_catalog_from_directory(self, directory):
        #Loop through the files in the directory
        for file in os.listdir(directory):
            #Open each file
            with open(f"{directory}/{file}") as json_object:
                #Load the json from the file
                data = json.load(json_object)

                #Sanity check whether there is an olm schema value, if not then the json is invalid
                if 'schema' not in data:
                    raise CatalogError(f"Cannot find a schema value in {data}")

                #Read in the olm package object
                if data['schema'] == 'olm.package':
                    #Sanity check whether there are multiple packages, if so then this is invalid json
                    if self.package != '':
                        raise CatalogError(f"Found 2 packages in a single file, unexpected use case. Please update the code base")
                    #Store the package object
                    self.package = data
                #Read in an olm channel object
                elif data['schema'] == 'olm.channel':
                    self.channels.append(data)
                #Read in an olm bundle object
                elif data['schema'] == 'olm.bundle':
                    self.bundles.append(data)
    
    #Get the latest channel using natsort
    def _get_latest_channel(self):
        #Sanity check whether the channels are empty, in which case retern None
        if len(self.channels) == 0:
            return None
        
        #Natsort the channels by their name
        sorted_channels = natsorted(self.channels, key=itemgetter(*['name']))

        #Return the most up-to-date channel based on natsort result
        return sorted_channels[-1]

    def get_channels(self):
        return self.channels
    
    #Get all channels matching a provided substring
    def get_channels_by_substring(self, substring):
        #Initialize a list of channels matching the substring
        channels_matching_substring = []

        #Loop through all the channels
        for channel in self.channels:
            #If the substring belongs to the channel name string, then include it
            if substring in channel['name']:
                channels_matching_substring.append(channel)
        
        #Return the list of channels matching the substring
        return channels_matching_substring
    
    #Get a single channel matching a provided string, return none if not found
    def get_channel(self, channel):
        #Find the channel, and if not found, return none
        retrieved_channel = None
        for ch in self.channels:
            if ch['name'] == channel:
                retrieved_channel = ch
                break
        
        #If it is found, return the channel
        return retrieved_channel
    
    def get_bundles(self):
        return self.bundles

    #Get all bundles matching a provided substring
    def get_bundles_by_substring(self, substring):
        #Initialize a list of bundles matching the substring
        bundles_matching_substring = []

        #Loop through all the bundles
        for bundle in self.bundles:
            #If the substring belongs to the bundle name string, then include it
            if substring in bundle['name']:
                bundles_matching_substring.append(bundle)
        
        #Return the list of bundles matching the substring
        return bundles_matching_substring
    
    #Get a single bundle matching a provided string, return none if not found
    def get_bundle(self, bundle):
        #Find the bundle, and if not found, return none
        retrieved_bundle = None
        for b in self.bundles:
            if b['name'] == bundle:
                retrieved_bundle = b
                break
        
        #If it is found, return the channel
        return retrieved_bundle

    #Function returns a formatted dict containing a channel and its corresponding bundles
    #The output of this function can be plugged into the add_channel_and_bundles function
    #in order to add a channel and its corresponding bundles from one catalog to another
    def get_channel_and_bundles(self, channel):
        #Get the channel matching the provided channel name
        channel = self.get_channel(channel)

        #If channel is not found then return none
        if channel == None:
            return None
        
        #If channel exists, then retrieve all its bundles
        bundles = []
        for entry in channel['entries']:
            bundle = self.get_bundle(entry['name'])
            if bundle != None:
                bundles.append(bundle)
        
        #After retrieving all bundles corresponding to the channel, return the formatted dict
        return { 'channel' : channel, 'bundles' : bundles }

    def get_default_channel(self):
        return self.package['defaultChannel']

    def set_default_channel(self, channel):
        for ch in self.channels:
            if ch['name'] == channel:
                self.package['defaultChannel'] = channel
                return
        raise CatalogError("Channel not found: {}: cannot set default channel")

    def write_new_file(self, filename='./catalog.json'):
        with open(filename, 'w') as f:
            json.dump(self.package, f, indent=self.indent)
            f.write("\n")
            for c in self.channels:
                json.dump(c, f, indent=self.indent)
                f.write("\n")
            for b in self.bundles:
                json.dump(b, f, indent=self.indent)
                f.write("\n")
    
    def write_new_dir(self, directory='.'):
        with open(f"{directory}/olm.package-{self.package['name']}.json", 'w') as package_file:
            json.dump(self.package, package_file, indent=self.indent)
        for c in self.channels:
            with open(f"{directory}/olm.channel-{c['name']}.json", 'w') as channel_file:
                json.dump(c, channel_file, indent=self.indent)
        for b in self.bundles:
            with open(f"{directory}/olm.bundle-{b['name']}.json", 'w') as bundle_file:
                json.dump(b, bundle_file, indent=self.indent)

    #Remove a channel and all bundles that it contains
    def remove_channel(self, channel):
        #Loop through the channels and check to see if the provided channel name matches the found channel name
        for c in self.channels:
            if c['name'] == channel:
                #If so, first remove all the bundles it contains
                while len(c['entries']) > 0:
                    self.remove_bundle_from_channel(c['entries'][0]['name'], channel)
                #Then, remove the channel
                self.channels.remove(c)
                log.info("Removed channel %s", channel)
                #Check if there are any further channels remaining, if not, then return without updating the default channel
                if len(self.channels) == 0:
                    raise CatalogError("There are no channels remaining in catalog %s", self.package['name'])
                #Finally, if the removed channel is the current default channel and there exist remaining channels, update the default channel automatically
                if channel == self.get_default_channel():
                    latest_channel = self._get_latest_channel()
                    if 'name' not in latest_channel.keys():
                        raise CatalogError("Unnamed channel: %s", str(latest_channel))
                    self.set_default_channel(latest_channel['name'])
    
    #Remove a bundle, unless that bundle is contained in another channel, then do nothing
    def remove_bundle_from_channel(self, bundle_name, channel_name):
        #Initialize a boolean to track whether the bundle belongs to another channel
        multi_channel_bundle = False
        #Loop through all bundles in the object
        for bundle in self.bundles:
            #If the desired bundle is found, then proceed to check if it belongs to another channel
            if bundle['name'] == bundle_name:
                for channel in self.channels:
                    for entry in channel['entries']:
                        #First determine if the bundle is contained in the provided channel, and remove its reference there
                        if channel['name'] == channel_name:
                            if bundle['name'] == entry['name']:
                                channel['entries'].remove(entry)
                                log.info("Removed bundle entry %s from channel %s", bundle_name, channel_name)
                        #If it belongs to any other channel, set the multi-channel-bundle boolean to true so that the bundle is not removed
                        else:
                            if bundle['name'] == entry['name']:
                                multi_channel_bundle = True
                #Then, remove the bundle itself if the only channel it belongs to is the one provided
                if not multi_channel_bundle:
                    self.bundles.remove(bundle)
                    log.info("Removed bundle %s", bundle_name)

    #Remove a bundle, and if that bundle is contained in a channel, remove it from the channel as well
    def remove_bundle(self, name):
        #Loop through all bundles in the object
        for bundle in self.bundles:
            #If the desired bundle is found, then proceed to remove it
            if bundle['name'] == name:
                #First determine if the bundle is contained in any channels, and remove its reference there
                for channel in self.channels:
                    for entry in channel['entries']:
                        if bundle['name'] == entry['name']:
                            channel['entries'].remove(entry)
                #Then, remove the bundle itself
                self.bundles.remove(bundle)
                log.info("Removed bundle %s", name)

    def add_channel(self, channel, package, update_default_channel_to_latest=False):
        #Add the channel
        self.channels.append({
            "schema": "olm.channel",
            "name": channel,
            "package": package, 
            "entries": []
        })
        #Check if the added channel is the only channel in the Catalog
        if len(self.channels) != 1:
            #If update to latest flag is passed in, then update default channel to latest
            if update_default_channel_to_latest:
                self.set_default_channel(self._get_latest_channel()['name'])
            return
        #If so, check if the default channel in the package is the added channel
        if self.get_default_channel() == channel:
            #If update to latest flag is passed in, then update default channel to latest
            if update_default_channel_to_latest:
                self.set_default_channel(self._get_latest_channel()['name'])
            return
        #If not, then update the default channel to the added channel
        self.set_default_channel(channel)
    
    def add_channel_entry(self, channel, name, skiprange=None, replaces=None):
        data = {}
        data['name'] = name
        if skiprange:
            data['skiprange'] = skiprange
        if replaces:
            data['replaces'] = replaces
        for c in self.channels:
            if c['name'] == channel:
                if 'entries' in c:
                    c['entries'] = []
                c['entries'].append(data)
    
    #This function adds a channel and bundles from a formatted dict that is provided as a parameter
    #It expects the same format as is returned by the get_channel_and_bundles function
    def add_channel_and_bundles(self, channel_and_bundles, update_default_channel_to_latest=False):
        #Sanity check on the channel and bundles input parameters
        if channel_and_bundles == None: #Added since the get_channel_and_bundles function can return None now
            raise CatalogError("The provided channel and bundles parameter was None")
        if 'channel' not in channel_and_bundles.keys():
            raise CatalogError("No channel was provided")
        if 'name' not in channel_and_bundles['channel'].keys():
            raise CatalogError("The provided channel was unnamed")
        if 'bundles' not in channel_and_bundles.keys():
            raise CatalogError("No bundles were provided")
        
        #Sanity check on channel before appending
        for channel in self.channels:
            if channel['name'] == channel_and_bundles['channel']['name']:
                raise CatalogError(f"Channel already exists: {channel_and_bundles['channel']['name']}")
        
        #Add the channel to the catalog along with its entries
        self.channels.append(channel_and_bundles['channel'])

        #If the added channel is the only one in the catalog and the default channel does not align with the
        #state of the channels, then update the default channel to be the added channel
        if update_default_channel_to_latest:
            self.set_default_channel(self._get_latest_channel()['name'])
        elif (len(self.channels) == 1) and (self.get_default_channel() != channel_and_bundles['channel']['name']):
            self.set_default_channel(channel_and_bundles['channel']['name'])

        #Add the bundles corresponding to the channel entries into the catalog
        for bundle in channel_and_bundles['bundles']:
            #Sanity check that the bundle is named
            if 'name' not in bundle.keys():
                raise CatalogError("A provided bundle was unnamed")
            
            #Sanity check that the bundle doesn't already exist
            bundle_exists = False
            for b in self.bundles:
                if b['name'] == bundle['name']:
                    bundle_exists = True
            
            #If it doesn't already exist, then append it
            if not bundle_exists:
                self.bundles.append(bundle)

    def get_latest_channel_entry(self, channel):
        names = [e['name'] for e in channel['entries'] ]
        names = natsorted(names)
        return names[-1]
    
    def __str__(self):
        ret = ''
        ret += f"Package: {self.package['name']}\n"
        for c in self.channels:
            ret += f"\tChannel: {c['name']}\tLatest entry: {self.get_latest_channel_entry(c)}\n"
        return ret

'''
Class for interacting with file-based operator catalogs with many operators
'''
class OperatorCatalog:
    #Constructor for the OperatorCatalog class
    def __init__(self, path):
        #Initialize some class variables for the OperatorCatalog class
        self.catalogs = {}

        #Sanity check to ensure that the path to the operator catalog exists
        if not os.path.exists(path):
            raise CatalogError(f"Operator catalog path does not exist: {path}")
        
        #If the operator catalog path does exist, then loop through its subdirectories
        for subdirectory in os.listdir(path):
            if os.path.isdir(f"{path}/{subdirectory}"):
                #If the directory only contains one file, then attempt to load the catalog from the file
                files = os.listdir(f"{path}/{subdirectory}")
                if len(files) == 1:
                    self.add_catalog_from_file(f"{path}/{subdirectory}/{files[0]}")
                else:
                    self.add_catalog_from_directory(f"{path}/{subdirectory}")
    
    #Add a new catalog into the operator catalog by loading it from a file
    def add_catalog_from_file(self, path):
        #Sanity check whether the provided path is a file
        if not os.path.isfile(path):
            raise CatalogError(f"The catalog path is not a file: {path}")
        
        #Load the file into a Catalog object
        #If any errors occur an exception will by thrown by the Catalog object constructor
        catalog = Catalog(path)

        #Sanity check whether the operator name already exists
        if catalog.package['name'] in self.catalogs.keys():
            raise CatalogError(f"Catalog already exists: {catalog.package['name']}")
        
        #Add the catalog to the operator catalog
        self.catalogs[catalog.package['name']] = catalog

    #Add a new catalog into the operator catalog by loading it from a directory
    def add_catalog_from_directory(self, path):
        #Sanity check whether the provided path is a directory
        if not os.path.isdir(path):
            raise CatalogError(f"The catalog path is not a directory: {path}")
        
        #Load the directory into a Catalog object
        #If any errors occur, an exception will be thrown by the Catalog object constructor
        catalog = Catalog(path)

        #Sanity check whether the operator name already exists
        if catalog.package['name'] in self.catalogs.keys():
            raise CatalogError(f"Catalog already exists: {catalog.package['name']}")

        #Add the catalog to the operator catalog under the operator name found/provided
        self.catalogs[catalog.package['name']] = catalog
            
    
    #Get the operator-to-catalog mapping from the catalog object
    def get_catalogs(self):
        return self.catalogs
    
    #Get a subset of the catalogs whose operator names match a provided substring
    def get_catalogs_by_substring(self, substring):
        #Initialize a dict to store the results
        catalogs_by_substring = {}

        #Loop through the operator names and determine which operator names match the provided substring
        for operator_name in self.catalogs.keys():
            if substring in operator_name:
               catalogs_by_substring[operator_name] = self.catalogs[operator_name]

        #Return the dict storing the results
        return catalogs_by_substring
    
    #Get a particular catalog whose operator name matches the one provided
    def get_catalog(self, operator_name):
        #Sanity check whether the catalog exists for the provided operator name
        if operator_name not in self.catalogs.keys():
            raise CatalogError(f"Catalog not found for operator {operator_name}")
        
        #Return the catalog
        return self.catalogs[operator_name]
    
    #Remove a particular catalog whose operator name matches the one provided
    def remove_catalog(self, operator_name):
        #Sanity check whether the catalog exists for the provided operator name
        if operator_name not in self.catalogs.keys():
            raise CatalogError(f"Catalog not found for operator {operator_name}")
        
        #Remove the catalog
        return self.catalogs.pop(operator_name)
    
    #Writes the operator catalog in its current state to a provided directory path
    def write_catalogs(self, directory):
        #Sanity check whether the path provided is a directory
        if not os.path.isdir(directory):
            raise CatalogError(f"The provided path is not a directory: {directory}")
        
        #Sanity check whether there exist catalogs to write
        if len(self.catalogs.keys() == 0):
            raise CatalogError(f"There are currently no catalogs to write")
        
        #If there exist catalogs to write, then loop through the catalogs
        for operator_name in self.catalogs.keys():
            #Make sure there exists a subdirectory of the provided directory that is the operator name
            if not os.path.exists(f"{directory}/{operator_name}"):
                os.mkdir(f"{directory}/{operator_name}")
            #If the subdirectory of this name already exists, then make sure it's a directory
            else:
                if not os.path.isdir(f"{directory}/{operator_name}"):
                    raise CatalogError(f"The catalog path already exists and is not a directory: {directory}/{operator_name}")
            
            #Write the catalog for this operator to its respective operator subdirectory
            catalog = self.catalogs[operator_name]
            catalog.write_new_dir(f"{directory}/{operator_name}")
    
    #Details the entire operator catalog as a string
    def __str__(self):
        ret = ''
        for operator_name in self.catalogs.keys():
            ret += f'{operator_name}: {str(self.catalogs[operator_name])}'
        return ret
