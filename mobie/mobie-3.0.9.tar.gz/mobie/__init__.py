import subprocess

import jgo.util
import os
import pathlib
import sys

_picocli_autocomplete    = 'picocli.AutoComplete'
_mobie_main_class        = 'org.embl.mobie.cmd.MoBIECommandLineInterface'
_groupId                 = 'org.embl.mobie'
_artifactId              = 'mobie-viewer-fiji'

def launch_mobie():
    return jgo.util.main_from_endpoint(
        argv=sys.argv[1:],
        primary_endpoint=f'{_groupId}:{_artifactId}',
        primary_endpoint_main_class=_mobie_main_class)

if __name__ == '__main__':
    launch_mobie()