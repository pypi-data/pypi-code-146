import iso3166_2 as iso
import iso3166
import requests
import json
import os
from importlib import metadata
import unittest
unittest.TestLoader.sortTestMethodsUsing = None

__version__ = "1.0.0"

class ISO3166_2_Updates(unittest.TestCase):

    def setUp(self):
        """ Initialise test variables, import json. """
        #initalise User-agent header for requests library 
        self.user_agent_header = {'User-Agent': 'iso3166-2/{} ({}; {})'.format(__version__,
                                            'https://github.com/amckenna41/iso3166-2', getpass.getuser())}

        #import main iso3166-2 json 
        with open(os.path.join("iso3166_2", "iso3166-2-data", "iso3166-2.json")) as iso3166_2_json:
            self.all_iso3166_2_data = json.load(iso3166_2_json)

        #import min iso3166-2 json
        with open(os.path.join("iso3166_2", "iso3166-2-data", "iso3166-2-min.json")) as iso3166_2_json:
            self.all_iso3166_2_min_data = json.load(iso3166_2_json)


    def test_iso3166_2_metadata(self): 
        """ Testing correct iso3166-2 software version and metadata. """
        self.assertEqual(metadata.metadata('iso3166_2')['version'], "0.0.6", "iso3166-2 version is not correct, got: {}".format(metadata.metadata('iso3166_2')['version']))
        self.assertEqual(metadata.metadata('iso3166_2')['name'], "iso3166-2", "iso3166-2 software name is not correct, got: {}".format(metadata.metadata('iso3166_2')['name']))
        self.assertEqual(metadata.metadata('iso3166_2')['author'], "AJ McKenna, https://github.com/amckenna41", "iso3166-updates author is not correct, got: {}".format(metadata.metadata('iso3166_2')['author']))
        self.assertEqual(metadata.metadata('iso3166_2')['author-email'], "amckenna41@qub.ac.uk", "iso3166-updates author email is not correct, got: {}".format(metadata.metadata('iso3166_2')['author-email']))
        self.assertEqual(metadata.metadata('iso3166_2')['summary'], "", 
            "iso3166-updates package summary is not correct, got: {}".format(metadata.metadata('iso3166_2')['summary']))
        self.assertEqual(metadata.metadata('iso3166_2')['keywords'], "", 
            "iso3166-updates keywords are not correct, got: {}".format(metadata.metadata('iso3166_2')['keywords']))
        self.assertEqual(metadata.metadata('iso3166_2')['home-page'], "https://github.com/amckenna41/iso3166-updates", "iso3166-updates home page url is not correct, got: {}".format(metadata.metadata('iso3166_2')['home-page']))
        self.assertEqual(metadata.metadata('iso3166_2')['maintainer'], "AJ McKenna", "iso3166-updates maintainer is not correct, got: {}".format(metadata.metadata('iso3166_2')['maintainer']))
        self.assertEqual(metadata.metadata('iso3166_2')['license'], "MIT", "iso3166-updates license type is not correct, got: {}".format(metadata.metadata('iso3166_2')['license']))


    def test_iso3166_2(self):
        """ """
        #create instance of subdivisions class
        all_subdivisions = iso.subdivisions
        

     
    def test_iso3166_2_json(self):
        """ """
        test_alpha2_ = self.all_iso3166_2_min_data["AU"]
        test_alpha2_ = self.all_iso3166_2_min_data["LU"]
        test_alpha2_ = self.all_iso3166_2_min_data["MG"]
        test_alpha2_ = self.all_iso3166_2_min_data["NA"]
        test_alpha2_ = self.all_iso3166_2_min_data["OM"]
        test_alpha2_ = self.all_iso3166_2_min_data["RS"]

        all_alpha2 = sorted(list(iso3166.countries_by_alpha2.keys()))


#1.)
        au_subdivision_codes = ["AU-NT", "AU-QLD", "AU-SA", "AU-TAS", "AU-ACT", "AU-VIC", "AU-NSW", "AU-WA"]
        au_subdivision_names = ["Northern Territory", "Queensland", "South Australia", "Tasmania", 
            "Australian Capital Territory", "Victoria", "New South Wales", "Western Australia"]

        self.assertEqual(test_alpha2_au["Name"], "Austrlia", "")
        self.assertEqual(len(test_alpha2_au["Subdivisions"]), 10, "")

        for code in list(self.all_iso3166_2_data.keys()):
            self.assertIn(code, all_alpha2, "")
            self.assertIn("Name", list(self.all_iso3166_2_data[code].keys()), "")
            self.assertIn("Subdivisions", list(self.all_iso3166_2_data[code].keys()), "")

            for subd in self.all_iso3166_2_data[code]:
                self.assertIn("Name", list(self.all_iso3166_2_data[code][subd].keys()), "")
                self.assertIn("Type", list(self.all_iso3166_2_data[code][subd].keys()), "")
                self.assertIn("Parent Code", list(self.all_iso3166_2_data[code][subd].keys()), "")
                self.assertIn("Flag URL", list(self.all_iso3166_2_data[code][subd].keys()), "")

        for subd_code in list(test_alpha2_au.keys()):
            self.assertIn(subd_code, au_subdivision_codes, "")
            self.assertIn(test_alpha2_au[subd_code]["Name"], au_subdivision_names, "")
            self.assertIn(test_alpha2_au[subd_code]["Parent Code"], null, "")
            self.assertIn(test_alpha2_au[subd_code]["Flag URL"], lu_subdivision_names, "")




    def test_iso3166_2_min_json(self):
        """ """
        test_alpha2_au = self.all_iso3166_2_min_data["AU"]
        test_alpha2_lu = self.all_iso3166_2_min_data["LU"]
        test_alpha2_mg = self.all_iso3166_2_min_data["MG"]
        test_alpha2_na = self.all_iso3166_2_min_data["NA"]
        test_alpha2_om = self.all_iso3166_2_min_data["OM"]
        test_alpha2_rs = self.all_iso3166_2_min_data["RS"]

        all_alpha2 = sorted(list(iso3166.countries_by_alpha2.keys()))

#1.)
        au_subdivision_codes = ["AU-NT", "AU-QLD", "AU-SA", "AU-TAS", "AU-ACT", "AU-VIC", "AU-NSW", "AU-WA"]
        au_subdivision_names = ["Northern Territory", "Queensland", "South Australia", "Tasmania", 
            "Australian Capital Territory", "Victoria", "New South Wales", "Western Australia"]

        self.assertEqual(test_alpha2_au["Name"], "Austrlia", "")
        self.assertEqual(len(test_alpha2_au["Subdivisions"]), 10, "")

        for code in list(self.all_iso3166_2_min_data.keys()):
            self.assertIn(code, all_alpha2, "")
            self.assertIn("Name", list(self.all_iso3166_2_min_data[code].keys()), "")
            self.assertIn("Subdivisions", list(self.all_iso3166_2_min_data[code].keys()), "")

            for subd in self.all_iso3166_2_min_data[code]:
                self.assertIn("Name", list(self.all_iso3166_2_min_data[code][subd].keys()), "")
                self.assertIn("Type", list(self.all_iso3166_2_min_data[code][subd].keys()), "")
                self.assertIn("Parent Code", list(self.all_iso3166_2_min_data[code][subd].keys()), "")
                self.assertIn("Flag URL", list(self.all_iso3166_2_min_data[code][subd].keys()), "")

        for subd_code in list(test_alpha2_au.keys()):
            self.assertIn(subd_code, au_subdivision_codes, "")
            self.assertIn(test_alpha2_au[subd_code]["Name"], au_subdivision_names, "")
            self.assertIn(test_alpha2_au[subd_code]["Parent Code"], null, "")
            self.assertIn(test_alpha2_au[subd_code]["Flag URL"], lu_subdivision_names, "")

#2.)
        lu_subdivision_codes = ["LU-RD", "LU-EC", "LU-RM", "LU-ES", "LU-VD", "LU-GR", "LU-CA",
            "LU-WI", "LU-LU", "LU-CL", "LU-ME", "LU-DI"]
        lu_subdivision_names = ["Capellen", "Clerf", "Echternach", "Esch an der Alzette",
            "Grevenmacher", "Luxembourg", "Mersch", "Redange", "Remich", "Veianen", "Wiltz"]

        self.assertEqual(test_alpha2_lu["Name"], "Luxembourg", "")
        self.assertEqual(len(test_alpha2_lu["Subdivisions"]), 10, "")

        for code in list(self.all_iso3166_2_min_data.keys()):
            self.assertIn(code, all_alpha2, "")
            self.assertIn("Name", list(self.all_iso3166_2_min_data[code].keys()), "")
            self.assertIn("Subdivisions", list(self.all_iso3166_2_min_data[code].keys()), "")

            for subd in self.all_iso3166_2_min_data[code]:
                self.assertIn("Name", list(self.all_iso3166_2_min_data[code][subd].keys()), "")
                self.assertIn("Type", list(self.all_iso3166_2_min_data[code][subd].keys()), "")
                self.assertIn("Parent Code", list(self.all_iso3166_2_min_data[code][subd].keys()), "")
                self.assertIn("Flag URL", list(self.all_iso3166_2_min_data[code][subd].keys()), "")

        for subd_code in list(test_alpha2_lu.keys()):
            self.assertIn(subd_code, au_subdivision_codes, "")
            self.assertIn(test_alpha2_lu[subd_code]["Name"], lu_subdivision_names, "")
            self.assertIn(test_alpha2_lu[subd_code]["Parent Code"], null, "")
            self.assertIn(test_alpha2_lu[subd_code]["Flag URL"], lu_subdivision_names, "")

#3.)
        mg_subdivision_codes = ["MG-A", "MG-D", "MG-F", "MG-M", "MG-T", "MT-U"]
        mg_subdivision_names = ["Toamasina", "Antsiranana", "Fianarantsoa", "Mahajanga",
            "Antananarivo", "Toliara"]

        self.assertEqual(test_alpha2_mg["Name"], "Madagascar", "")
        self.assertEqual(len(test_alpha2_mg["Subdivisions"]), 10, "")

        for code in list(self.all_iso3166_2_min_data.keys()):
            self.assertIn(code, all_alpha2, "")
            self.assertIn("Name", list(self.all_iso3166_2_min_data[code].keys()), "")
            self.assertIn("Subdivisions", list(self.all_iso3166_2_min_data[code].keys()), "")

            for subd in self.all_iso3166_2_min_data[code]:
                self.assertIn("Name", list(self.all_iso3166_2_min_data[code][subd].keys()), "")
                self.assertIn("Type", list(self.all_iso3166_2_min_data[code][subd].keys()), "")
                self.assertIn("Parent Code", list(self.all_iso3166_2_min_data[code][subd].keys()), "")

        for subd_code in list(test_alpha2_mg.keys()):
            self.assertIn(subd_code, au_subdivision_codes, "")
            self.assertIn(test_alpha2_mg[subd_code]["Name"], mg_subdivision_names, "")
            self.assertIn(test_alpha2_mg[subd_code]["Parent Code"], null, "")


    def tearDown(self):
        """ Delete all iso3166-2 json objects or instances. """
        del self.all_subdivisions
        del self.all_iso3166_2_data
        del self.all_iso3166_2_min_data
    
if __name__ == '__main__':
    #run all unit tests
    unittest.main(verbosity=2)    

