# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['data_france',
 'data_france.admin',
 'data_france.data',
 'data_france.management',
 'data_france.management.commands',
 'data_france.migrations']

package_data = \
{'': ['*']}

install_requires = \
['django-countries>=7.3.1,<8.0.0', 'django>=3.1', 'psycopg2>=2.9.5']

setup_kwargs = {
    'name': 'data-france',
    'version': '0.14.4',
    'description': "Paquet agrégeant des données administratives publiques pour en rendre l'utilisation facile.",
    'long_description': "data-france\n=============\n\nUn ensemble de données administratives et géographiques pour la France. Elle double comme application Django\npour permettre l'intégration aisée de ces données.\n\n\nInstaller le paquet\n-------------------\n\nInstallez ce paquet avec pip::\n\n  pip install data-france\n\n\nImporter les données\n--------------------\n\nPour importer les données, appliquez les migrations et utilisez la commande de management::\n\n  ./manage.py update_data_france\n\n\nModèles\n--------\n\nCirconscriptions administratives et collectivités locales\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\nL'application django comporte les modèles suivants :\n\n* `Commune`\n\n  * Inclut les communes délégués / communes associées / arrondissements PLM /\n    secteurs électoraux PLM\n  * Les différents types d'entités sont différenciés par le champ `type`\n\n* `EPCI`\n\n  * Il s'agit des EPCI à fiscalité propre : CA, CC, CU et métropoles\n  * N'inclut pas encore les EPT du Grand Paris\n\n* Canton\n\n  * N'inclut pas encore les géométries\n\n* `Departement` et `Region` pour les départements et régions comme\n  circonscriptions administratives de l'État\n\n* `CollectiviteDepartementale` et `CollectiviteRegionale` pour les départements\n  et régions comme collectivités territoriales :\n\n  * La métropole de Lyon (aux compétences départementales) est référencée comme\n    une collectivité départementale ;\n  * les collectivités territoriales uniques (par exemple l'Assemblée de Corse)\n    sont référencées comme des collectivités régionales (cela inclut, de façon\n    contre-intuitive, le département de Mayotte) ;\n  * À noter que comme le conseil de Paris est déjà référencé comme une\n    `Commune`, il n'est pas référencé de nouveau comme collectivité\n    départementale.\n\n* Les codes postaux\n\n* Circonscriptions législatives\n\n* Cisconscriptions consulaires\n\nToutes ces entités (sauf les codes postaux, les cantons, les circonscriptions\nconsulaires, et les collectivités régionales, dont la géométrie est\nsystématiquement celle de la région correspondante) viennent avec une géometrie\net les articles + charnière.\n\nÉlu·es\n~~~~~~\n\nLes fichiers suivants du répertoire national des élus sont importés et\ndisponibles sous forme de modèle Django\xa0:\n\n* Les élus municipaux\n\n* Les députés\n\n\nVues JSON\n----------\n\nRecherche de communes\n~~~~~~~~~~~~~~~~~~~~~\n\nUne vue de recherche renvoyant les résultats en JSON est disponible, à l'URL\n`chercher/communes/` si vous importez `data_france.urls` (en utilisant le\nparamètre GET `q`). Il est possible d'obtenir les résultats au format geojson en\najoutant le paramètre GET `geojson` à une valeur non vide.\n\nRecherche de circonscriptions consulaires\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\nUne vue de recherche des circonscriptions consulaires, à l'adresse\n`circonscriptions-consulaires/chercher/`, en utilisant le paramètre `q`.\n\nDes vues d'affichage par code\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\nDes vues existent pour afficher une des entités suivantes en la référençant par son code INSEE usuel\xa0:\n\n* Les communes, `communes/par-code/`\n* Les epci, `epci/par-code/`\n\n  * Il faut utiliser les codes SIREN\n\n* Les départements, `departements/par-code/`\n* Les régions, `regions/par-code/`\n* Les codes postaux, `code-postal/par-code/`\n* Les collectivités de niveau départemental, `collectivite-departementale/par-code/`\n\n  * Le code du département considéré comme une collectivité départementale\n    plutôt que comme une circonscription administrative de l'État est\n    généralement `<code dep>D`.\n\n* Les collectivités de niveau régional, `collectivite-regionale/par-code/`\n\n  * Généralement\n\nAutres remarques\n----------------\n\n**ATTENTION** : Ce paquet ne fonctionne que si votre projet Django utilise\n**PostGIS** car il utilise certaines fonctionnalités propres à PostgreSQL.\n",
    'author': 'Salomé Cheysson',
    'author_email': 'salome@cheysson.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/aktiur/data-france',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
