#https://aladin.cds.unistra.fr/AladinLite/doc/tutorials/interactive-finding-chart/

begin = """
<link rel="stylesheet" href="http://aladin.u-strasbg.fr/AladinLite/api/v2/latest/aladin.min.css" />
<script type="text/javascript" src="http://code.jquery.com/jquery-1.9.1.min.js" charset="utf-8"></script>
\n"""

class Aladin:
    def __init__(self, target, fov=1, survey="P/DSS2/color", width=700, height=700):

        self.target = target
        self.fov = fov
        self.survey = survey
        self.width = width
        self.height = height
        self.html = None
        
        self.h1 = begin + \
            f'<div id="aladin-lite-div" style="width:{width}px;height:{height}px;"></div>\n'
        self.h999 = '\n<script type="text/javascript" src="http://aladin.u-strasbg.fr/AladinLite/api/v2/latest/aladin.min.js" charset="utf-8"></script>\n'

        self.b1 = '\n<script type="text/javascript">\n' + \
        f"""\tvar aladin = A.aladin('#aladin-lite-div', {{survey: "{survey}", fov:{fov}, target: "{target}", cooFrame: "ICRSd"}});\n\n"""
        self.b999 = '</script>'
        
        self.__buttons = ''
        self.__butfunc = ''
        self.__markers = ''
        self.__simbad = ''
        self.__vizier = ''
        #self.__image = ''
        self.__imgovlyr = ''


    def create(self):
        self.html = self.h1 + self.__buttons + self.h999 + \
                    self.b1 + self.__butfunc + \
                    self.__markers + self.__simbad + self.__vizier + self.__imgovlyr + \
                    self.b999

    def __add_survey_btn(self, value, id, label):
        return f'<input id="{id}" type="radio" name="survey" value="{value}"><label for="{id}">{label}<label>\n'

    def add_survey_buttons(self, buttons):
        self.__buttons = '\n'
        for i in range(len(buttons)):
            self.__buttons = self.__buttons + self.__add_survey_btn(buttons[i][0], 'id'+str(i+1), buttons[i][1])
        self.__butfunc = "\n\t$('input[name=survey]').change(function() {\n" + \
                         "\t\taladin.setImageSurvey($(this).val());\n" + "\t});\n\n"
        

    def __add_marker(self, n, ra, dec, title, desc):
        return f"\tvar marker{n} = A.marker({ra}, {dec}, {{popupTitle: '{title}', popupDesc: '{desc}'}});\n"

    def add_markers(self, markers):
        self.__markers = ''
        for i in range(len(markers)):
            self.__markers = self.__markers + self.__add_marker(i+1, markers[i][0], markers[i][1], markers[i][2], markers[i][3])
        self.__markers = self.__markers + "\tvar markerLayer = A.catalog({color: '#800080'});\n"
        self.__markers = self.__markers + "\taladin.addCatalog(markerLayer);\n"
        tmp = ''
        for i in range(len(markers)):
            tmp = tmp + f'marker{i+1}, '
        self.markers = self.markers + f"\tmarkerLayer.addSources([{tmp}]);\n"
        

    def add_simbad(self, target=None, radius=None):
        if target is None:
            target = self.target
        if radius is None:
            radius = self.fov / 3
        self.__simbad = f"\n\taladin.addCatalog(A.catalogFromSimbad('{target}', {radius}, {{shape: 'plus', color: '#5d5', onClick: 'showTable'}}));"
        

    def add_vizier(self, table=None, target=None , radius=None):
        if table is None:
            table = 'I/239/hip_main'
        if target is None:
            target = self.target
        if radius is None:
            radius = self.fov / 4
        self.__vizier = f"\n\taladin.addCatalog(A.catalogFromVizieR('{table}', '{target}', {radius}, {{shape: 'square', sourceSize: 8, color: 'red', onClick: 'showPopup'}}));"

##    def add_image(self, url):
##        self.__image = f"\n\taladin.displayJPG('{url}');"

    def add_image_overlayer(self, hips_id, hips_name, hips_base_url, hips_max_ord, coord_frame='equatorial', format='png', slider=False):
        tmp = '\n\taladin.setOverlayImageLayer(aladin.createImageSurvey(' + \
              f"'{hips_id}', '{hips_name}', '{hips_base_url}', '{coord_frame}', {hips_max_ord}, {{imgFormat: '{format}'}}));\n" + \
              '\tvar ovim = aladin.getOverlayImageLayer();\n'
        
        if slider:
            self.h999 = self.h999 + '\n<div class="slidecontainer">' + \
                    f'  <input type="range" min="0" max="1" step="0.1" value="1" class="slider" id="myRange" style="width:{self.width}px";>\n' + \
                    '  <p>Opacity: <span id="demo"></span></p>\n' + '</div>\n\n'
            slider1 = '\n\tvar slider = document.getElementById("myRange");\n' + \
                      '\tvar output = document.getElementById("demo");\n' + \
                      '\toutput.innerHTML = slider.value;\n\n'
            slider2 = '\n\tslider.oninput = function() {\n' + \
                      '\t  output.innerHTML = this.value;\n' + \
                      '\t  var ovim = aladin.getOverlayImageLayer();\n' + \
                      '\t  ovim.setAlpha(this.value);\n' + '\t}\n'
            tmp = tmp + '\tovim.setAlpha($(slider.value));\n\n'
            self.__imgovlyr = slider1 + tmp + slider2
        else:
            self.__imgovlyr = tmp + '\tovim.setAlpha(1.0);\n'
        

    def save(self, filename='index.html'):
        with open(filename, 'w') as f:
            f.write(self.html)

