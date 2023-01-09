from snakewrapper import main_wrapper


if __name__ == "__main__":
    dico_tool = {
        "soft_path": "/media/work/GIT/PodiumASM-forge/podiumASM",
        "url": "https://forge.ird.fr/phim/sravel/PodiumASM/",
        "docs": "https://forge.ird.fr/phim/sravel/PodiumASM/",
        "description_tool": """ 
    Welcome to PodiumASM version: VERSION! Created on January 2022
    @author: Sebastien Ravel (CIRAD), Theo Durand, Simon Bache
    @email: sebastien.ravel@cirad.fr
    Please cite our github: GIT_URL
    Licencied under CeCill-C (http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html)
    and GPLv3 Intellectual property belongs to CIRAD and authors.
    Documentation avail at: DOCS""",
        "singularity_url_files": [('http://nas-bgpi.myds.me/DOC/rattleSNP/Singularity.rattleSNP_tools.sif',
                                   'INSTALL_PATH/containers/Singularity.rattleSNP_tools.sif'),
                                  ('http://nas-bgpi.myds.me/DOC/rattleSNP/Singularity.report.sif',
                                   'INSTALL_PATH/containers/Singularity.report.sif')
                                  ],
        "datatest_url_files": (
            "http://nas-bgpi.myds.me/DOC/rattleSNP/data_test_rattleSNP.zip", "data_test_rattleSNP.zip")

    }
    main_wrapper(**dico_tool)()
