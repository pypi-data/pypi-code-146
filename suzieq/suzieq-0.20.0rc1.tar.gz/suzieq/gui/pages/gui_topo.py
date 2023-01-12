from suzieq.gui.guiutils import display_help_icon
from suzieq.gui.guiutils import gui_get_df, get_base_url, get_session_id
from suzieq.sqobjects.topology import TopologyObj
from copy import copy
from urllib.parse import quote
import graphviz as graphviz
import pandas as pd
import streamlit as st
from dataclasses import dataclass, asdict, field


# def get_title():
#     return 'Topology'


@dataclass
class TopologySessionState:
    run: bool = False
    namespace: str = ''
    topoobj: TopologyObj = None
    topoview: str = ''
    start_time: str = ''
    end_time: str = ''


def build_graphviz_obj(df: pd.DataFrame, summ_df: pd.DataFrame, topoview: str):
    '''Returns a graphviz object of the topology specified

    '''
    pass


def topology_sidebar(state, sqobjs):
    '''Draw the topology sidebar'''

    devdf = gui_get_df(sqobjs['device'], columns=['namespace'])
    if devdf.empty:
        st.error('Unable to retrieve any namespace info')
        st.stop()

    namespaces = sorted(devdf.namespace.unique().tolist())
    if state.namespace:
        nsidx = namespaces.index(state.namespace)
    else:
        nsidx = 0

    url = '&amp;'.join([
        f'{get_base_url()}?page=_Help_',
        'help=yes',
        'help_on=Topology',
    ])
    display_help_icon(url)

    topoviews = ['lldp', 'ospf', 'bgp']
    if state.topoview:
        topoidx = topoviews.index(state.topoview)
    else:
        topoidx = 0

    ok_button = st.sidebar.button('Draw')
    namespace = st.sidebar.selectbox('Namespace',
                                     namespaces, index=nsidx)

    topoview = st.sidebar.selectbox('View For',
                                    topoviews, index=topoidx)

    state.start_time = st.sidebar.text_input('Start Time',
                                             value=state.start_time,
                                             key='start-time')
    state.end_time = st.sidebar.text_input('End Time',
                                           value=state.end_time,
                                           key='end-time')

    if all(not x for x in [state.namespace, state.topoview]):
        state.run = False
    elif ok_button:
        state.run = True

    state.namespace = namespace
    state.topoview = topoview

    return


def page_work(state_container):
    '''Main workhorse routine for topology'''

    if not state_container.topoSessionState:
        state_container.topoSessionState = TopologySessionState()

    state = state_container.topoSessionState

    url_params = st.experimental_get_query_params()
    page = url_params.pop('page', '')

    if not state and get_title() in page:
        if url_params and not all(not x for x in url_params.values()):
            url_params.pop('search_text', '')
            for key in url_params:
                val = url_params.get(key, '')
                if isinstance(val, list):
                    val = val[0]
                    url_params[key] = val
                if key == 'run':
                    if val == 'True':
                        url_params[key] = True
                    else:
                        url_params[key] = False

            state.__init__(**url_params)

    state_container.topoSessionState = state

    topology_sidebar(state, state_container.sqobjs)

    pgbar = st.empty()

    if state.run:
        pgbar.progress(0)
