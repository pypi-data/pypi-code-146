#!/usr/bin/env python3
#
#

import os
import sys
import os.path

def j(*args):
    if not args: return
    todo = list(map(str, filter(None, args)))
    return os.path.join(*todo)

if sys.version_info.major < 3:
    print("you need to run president with python3")
    os._exit(1)

try:
    use_setuptools()
except:
    pass

try:
    from setuptools import setup
except Exception as ex:
    print(str(ex))
    os._exit(1)

target = "president"
upload = []

def uploadfiles(dir):
    upl = []
    if not os.path.isdir(dir):
        print("%s does not exist" % dir)
        os._exit(1)
    for file in os.listdir(dir):
        if not file or file.startswith('.'):
            continue
        d = dir + os.sep + file
        if not os.path.isdir(d):
            if file.endswith(".pyc") or file.startswith("__pycache"):
                continue
            upl.append(d)
    return upl

def uploadlist(dir):
    upl = []

    for file in os.listdir(dir):
        if not file or file.startswith('.'):
            continue
        d = dir + os.sep + file
        if os.path.isdir(d):   
            upl.extend(uploadlist(d))
        else:
            if file.endswith(".pyc") or file.startswith("__pycache"):
                continue
            upl.append(d)

    return upl

setup(
    name='president',
    version='101',
    url='https://bitbucket.org/bthate/president',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="@KarimKhanQC reconsider OTP-CR-117/19",
    license='Public Domain',
    packages=["president"],
    include_package_data=True,
    zip_safe=False,
    scripts=["bin/president"],
    long_description='''
Geachte Minister-President,

Ik ben Bart Thate, een 50 jaar oude schizofrenie patient.

Op 20 Oktober 2012 heb ik na correspondentie met de Koningin een klacht tegen de Nederland ingedient (Thate tegen Nederland 69389/12). De klacht betrof het falen van de
(F)ACT methodiek, de methode die GGZ Nederland gebruikt om vorm te geven aan de wetten die gedwongen behandeling in Nederland mogelijk maken. De uitspraak is niet-ontvankelijk.

Omdat de Koningin gemeld heeft dat ze vanwege ministeriele verantwoordelijkheden geen tussenkomst kan bieden, wend ik mij tot u.

Er is bewijs dat antipsychotica schadelijk voor de hersenen zijn, bijv. Haldol brengt 4% aantasting van de hippocampus:

1) http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3476840/ 
2) https://jamanetwork.com/journals/jamapsychiatry/article-abstract/2672208

De geneesmiddelenwet zegt dat u stoffen van de geneesmiddelenmarkt dient te halen als deze schadelijk blijken te zijn.
Daarom eis ik van u dat u direct medicijnen die gifstoffen blijken te zijn van de geneesmiddelmarkt haalt.

Er is bewijs dat antipsychotica gif zijn:

1) clozapine (leponex) - https://echa.europa.eu/substance-information/-/substanceinfo/100.024.831
2) olanzapine (zyprexa) - https://echa.europa.eu/substance-information/-/substanceinfo/100.125.320
3) aripriprazole (abilify) https://echa.europa.eu/substance-information/-/substanceinfo/100.112.532
4) haloperiodol (haldol) - https://echa.europa.eu/substance-information/-/substanceinfo/100.000.142

Dat het hier gif betreft en niet een onschadelijk medicijn maakt dat men een strafbaar feit pleegt. 
Daarom eis ik van u dat u gif toedieningen laat vervolgen door het Openbaar Ministerie.

Het is voor mij niet mogelijk gebleken om aangifte te doen van mishandeling als de psychiater zijn patient met gif mishandelt:

1) De IGZ treft geen structurele onzorgvuldigheid in de afhandeling van klachten bij GGZ-NHN aan.
2) De Hoge Raad concludeert dat het geen verantwoordelijkheid heeft en verwijst naar het Openbaar Ministerie, dat niet reageert.
3) Daarna heb ik het Europeese Hof voor de Rechten van de Mens aangeschreven om een klacht tegen Nederland in te dienen.
4) Pas na een gang langs het EVRM reageert Het Openbaar Ministerie wel en verwijst naar de IGZ, die de klacht melding al heeft afgesloten.

Het ontbreekt de GGZ patient aan een daadwerkelijke remedie om een einde te kunnen maken aan de mishandeling die een arts pleegt als hij gif toedient.
Daarom eis ik ook dat u voor de GGZ patient gif toedienende artsen laat vervolgen.

Mijn eisen zijn dus:

1) medicijnen die gif blijken te zijn van de markt af.
2) gif toedieningen door het Openbaar Ministerie laten vervolgen.
3) voor de GGZ patient deze vervolging te doen..

Er van uitgaande dat u mijn eisen inwilligt,


Bart Thate 
    

''',
   data_files=[
               ('share/doc/president', uploadlist("docs")),
               ('share/doc/president/_static', uploadlist("docs/_static")),
               ('share/doc/president/_templates', uploadlist("docs/_templates"))
              ],
   classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Utilities'],
)
