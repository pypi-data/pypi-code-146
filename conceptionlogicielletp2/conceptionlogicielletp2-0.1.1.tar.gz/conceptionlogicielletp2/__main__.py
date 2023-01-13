from dotenv import load_dotenv
import os
from conceptionlogicielle.ratio import ratio

load_dotenv()
environnement = os.environ["ENVIRONNEMENT"] if "ENVIRONNEMENT" in os.environ else "local"
print("ENVIRONNEMENT: "+environnement)
ratio = ratio()
mot_1 = (
        os.environ["MOT_UN"]
        if "MOT_UN" in os.environ
        else "conception_logicielle"
    )
mot_2 = (
        os.environ["MOT_DEUX"]
        if "MOT_DEUX" in os.environ
        else "configuration"
    )
print("mot 1: "+mot_1 + " (changeme by setting env var MOT_UN)")
print("mot 2: "+mot_2+" (changeme by setting env var MOT_DEUX)")
print(f"Distance de Levenshtein : {ratio}")
