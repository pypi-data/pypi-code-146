from dotenv import load_dotenv
import os
from conceptionlogicielle.ratio import ratio

load_dotenv()
environnement = os.environ["ENVIRONNEMENT"] if "ENVIRONNEMENT" in os.environ else "local"
print("ENVIRONNEMENT: "+environnement)
ratio = ratio()
print(f"Ratio : {ratio}")
