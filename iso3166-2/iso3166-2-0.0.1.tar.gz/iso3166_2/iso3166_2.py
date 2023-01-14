import os
import sys
import json
import iso3166

#instead of loading all at once, only load json and country per call
#canada_iso3166_2 = iso.subdivisions["CA"] <- only load json and CA data in

class Subdivisions():
    """


    """
    def __init__(self, iso3166_json_filename="iso3166-2.json"):

        #get module path
        self.iso3166_2_module_path = os.path.dirname(os.path.abspath(sys.modules[self.__module__].__file__))
        self.iso3166_json_filename= iso3166_json_filename
        self.data_folder = "iso3166-2-data"
        
        print("iso3166_2_module_path", os.path.join(self.iso3166_2_module_path, self.data_folder, self.iso3166_json_filename))
        #raise error if iso3166-2 json doesnt exist in the data folder
        if not (os.path.isfile(os.path.join(self.iso3166_2_module_path, self.data_folder, self.iso3166_json_filename))):
            raise OSError("Issue finding iso3166-2.json in data dir.")

        #open iso3166-2 json file and load it into class variable
        with open(os.path.join(self.iso3166_2_module_path, self.data_folder, self.iso3166_json_filename)) as iso3166_2_json:
            self.all_iso3166_2_data = json.load(iso3166_2_json)
        
        #get list of all countries by 2 letter alpha3 code
        # self.alpha2 = sorted(list(self.all_iso3166_2_data.keys()))
        self.alpha2 = sorted(list(iso3166.countries_by_alpha2.keys()))

        #get list of all countries by 3 letter alpha3 code
        self.alpha3 = sorted(list(iso3166.countries_by_alpha3.keys()))

        # self.name = "" {AD: Andorra} etc #only initilaise these if they are called 
        # self.name = "" {AD: Andorra} etc

    def load_json(self):
        """ """
        with open(os.path.join(self.iso3166_2_module_path, self.data_folder, self.iso3166_json_filename)) as iso3166_2_json:
            self.all_iso3166_2_data = json.load(iso3166_2_json)

    # def __repr__(self):
    #     """ Return object representation of class instance. """
    #     return "<Subdivisions: {}>".format(self)

    def __sizeof__(self):
        """ Return size of instance of Subdivisions class. """
        return self.__sizeof__()

    def __getitem__(self, alpha2_code):
        """
        Return all of a countrys data and subdivision by making the class
        subscriptable.

        Parameters
        ----------
        : alpha2_code : str
            2 letter alpha2 code for sought country/territory e.g (AD, EG, DE).

        Returns
        -------
        : country: dict
            dict object of country/subdivision info for inputted alpha2_code.

        Usage
        -----
        import iso3166_2 as iso

        #get country & subdivision info for Ethiopia
        iso.subdivisions["ET"]

        #get country & subdivision info for GA, HU, ID
        iso.subdivisions["ga,hu,id"] # OR iso.subdivisions["GA,HU,ID"]
        """
        #stripping input of whitespace, if not a string type raise Type Error
        try:
            alpha2_code = alpha2_code.strip().upper()
        except:
            raise TypeError('Input parameter {} is not of correct datatype string, got {}' \
                .format(alpha2_code, type(alpha2_code)))

        print("alpha2_code", alpha2_code)

        alpha2_code = alpha2_code.split(',')

        # alpha2_code = [code.strip() for code in alpha2_code]
        # alpha2_code = [code.upper() for code in alpha2_code]

        print("alpha2_code", alpha2_code)

        country = {}

        for code in alpha2_code:
            
            print("code", code)
            if (len(code) == 2):
                if (code in self.alpha2):      
                    code = iso3166.countries_by_alpha2[code].alpha2
                else:
                    #raise error if 2 letter alpha2 code not valid
                    raise ValueError("")            
            
            #if 3 letter code input, check it is value then convert into its 2 letter alpha2 code
            if (len(code) == 3):
                if (code in self.alpha3):      
                    code = iso3166.countries_by_alpha3[code].alpha2
                else:
                    #raise error if 3 letter alpha3 code not valid
                    raise ValueError("") 

            #create instance of Map class so dict can be accessed via dot notation 
            country[code] = Map(self.all_iso3166_2_data[code]) 
            # country.append(Map(self.all_iso3166_2_data[code]))

        country = Map(country)
                 
        
        # country = Map(self.all_iso3166_2_data[alpha2_code])

        return country

class Map(dict):
    """
    Class that accepts a dict and allows you to use dot notation to access
    members of the dictionary. 

    Parameters
    ----------
    : dict
        input dictionary to convert into instance of map class so the keys/vals
        can be accessed via dot notation.

    Usage
    -----
    # create instance of map class
    m = Map({'first_name': 'Eduardo'}, last_name='Pool', age=24, sports=['Soccer'])
    # Add new key
    m.new_key = 'Hello world!'
    # Or
    m['new_key'] = 'Hello world!'
    # Update values
    m.new_key = 'Yay!'
    # Or
    m['new_key'] = 'Yay!'
    # Delete key
    del m.new_key
    # Or
    del m['new_key']

    References
    ----------
    [1]: https://stackoverflow.com/questions/2352181/how-to-use-a-dot-to-access-members-of-dictionary

    """
    def __init__(self, *args, **kwargs):
        super(Map, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    self[k] = v
        if kwargs:
            for k, v in kwargs.items():
                self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Map, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(Map, self).__delitem__(key)
        del self.__dict__[key]

#create instance of Subdivisions class
subdivisions = Subdivisions()