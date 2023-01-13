from fuzzywuzzy import fuzz
import os
from dotenv import load_dotenv
load_dotenv()  # Charge toutes les variables du fichier .env

variables_environnement = os.environ
default_mot_un = variables_environnement['DEFAULT_MOT_UN'] \
    if 'DEFAULT_MOT_UN' in variables_environnement else "Pikachu"
default_mot_deux = variables_environnement['DEFAULT_MOT_DEUX'] \
    if 'DEFAULT_MOT_DEUX' in variables_environnement else "Carapuce"


def ratio():
    return fuzz.ratio(default_mot_un, default_mot_deux)
