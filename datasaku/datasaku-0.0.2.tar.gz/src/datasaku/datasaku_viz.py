"""vizualisation code for quick and dirty analysis"""

import seaborn as sns
from matplotlib import pyplot as plt
import pandas as pd
import plotly.graph_objects as go

def viz_sankey(df_def, col1_var_def, col2_var_def, metric_var_def):
    """
    Create sankey visualisation from pre-curatted and aggregate dataframe.  
    The format would be something like: col1_var_def|col2_var_def|metric_var_def.   
    - col1_var_def = first columns would be the left hand side of sankey chart.  
    - col2_var_def = Second columns would be the right hand side of sankey chart
    """
    trans1 = pd.DataFrame({'label': df_def[col1_var_def]
                            , 'code': df_def[col1_var_def].astype("category").cat.codes
                            })
    trans1 = dict(zip(trans1.label, trans1.code))
    trans2 = pd.DataFrame({'label': df_def[col2_var_def]
                            , 'code': df_def[col2_var_def].astype("category").cat.codes + max(trans1.values()) + 1
                            })
    trans2 = dict(zip(trans2.label, trans2.code))
    df_def[col1_var_def+"_code"] = df_def[col1_var_def].map(trans1)
    df_def[col2_var_def+"_code"] = df_def[col2_var_def].map(trans2)

    label_list = list(trans1.keys()) + list(trans2.keys())
    source = df_def[df_def[col1_var_def]+"_code"].tolist()
    target = df_def[df_def[col2_var_def]+"_code"].tolist()
    count = df_def[metric_var_def].tolist()

    fig = go.Figure(data=[go.Sankey(
        node = {"label": label_list},
        link = {"source": source, "target": target, "value": count}
        )])

    fig.update_layout(
        hovermode = 'x',
        title=f"Sankey <br>between {col1_var_def} and {col2_var_def}",
        font=dict(size = 10)
    )

    return fig.show()