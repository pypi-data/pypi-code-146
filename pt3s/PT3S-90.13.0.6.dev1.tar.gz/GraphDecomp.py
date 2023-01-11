__version__='90.12.4.0.dev1'

import re
import pandas as pd
import numpy as np

def GraphDecomp(
    logfile # Logfile der Graphenzerlegung
    ):
    
    """
    Liest die SIR3S Graphenzerlegungs-logfile in ein Dictionary ein
    """

    f=open(logfile, 'r')
    lines = f.readlines()

    for line in lines:
        if re.search('^Nodes',line):
            idx_NODES = lines.index(line)
        elif re.search('^Links',line):
            idx_LINKS = lines.index(line)


    df_NODES = pd.DataFrame(np.row_stack([row.split(';') for row in lines[idx_NODES+2:idx_LINKS-1]]))
    df_NODES = df_NODES.iloc[: , :-1]

    df_NODES_ColNames = lines[idx_NODES+1].split(';')
    for x in range(len(df_NODES_ColNames)):
        df_NODES_ColNames[x] = df_NODES_ColNames[x].strip()

    df_NODES.columns = df_NODES_ColNames


    df_LINKS = pd.DataFrame(np.row_stack([row.split(';') for row in lines[idx_LINKS+2:]]))

    df_LINKS_ColNames = lines[idx_LINKS+1].split(';')
    for x in range(len(df_LINKS_ColNames)):
        df_LINKS_ColNames[x] = df_LINKS_ColNames[x].strip()

    df_LINKS[df_LINKS.columns[-1]] = df_LINKS[df_LINKS.columns[-1]].apply(lambda x: x.strip())

    df_LINKS.columns = df_LINKS_ColNames


    GraphDecomp = {'NODES':df_NODES, 'LINKS':df_LINKS}
    return GraphDecomp