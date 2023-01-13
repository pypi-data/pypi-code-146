from typing import Dict, List

def setup_config(room_id: int) -> Dict[str, List[str]]:
    """Setup room specific configuration
    
    Config types
    ------------
    root_variable : string
        Variable which may not be null - this might be redundant. Consider logging to check if this actually removes cases.
    closed_ptype_variable : string
        ptypeXc variables which are removed from data.
    cpr_variable : string
        Name of variable holding cpr.
    room_specific_variables : List[str]
        Individual variables which are relevant for the specific room - i.e. uni id for 729
    archive_variables : List[str]
        List of variables storing information on archive ptypes
    clients_query : string
        Query string selecting only client area(s)
    testarea_variables : List[str]
        List of variables from which test areas should be removed 

    
    """
    
    room_specific_config = {
        'root_variable': {
            491: ['background/ptype24'],
            729: ['background/ptype1'],
            999999: []
        },
        'closed_ptype_variable': {
            491: ['background__ptype24c'],
            729: ['background__ptype3c'],
            999999: []
        },
        'cpr_variable': {
            491: ['barnbg__cpr'],
            729: ['barnbackground__cpr'],
            999999: []
        },
        'room_specific_variables': {
            491: [],
            729: ['skolebg__uni_id'],
            999999: []
        },
        'consent_variables': {
            491: ['barnbg__s_2', 'barnbg__s_5'],
            729: [],
            999999: []
        },
        'archive_variables': {
            491: ['background__ptype220', 'background__ptype47', 'background__ptype221'],
            729: ['background__ptype20', 'background__ptype33', 'background__ptype287'],
            999999: []
        },
        'clients_query': {
            491: ['(background__ptype65 == 7352477)'],
            729: ['(background__ptype2 == 23318479 or background__ptype2 == 9523670 or background__ptype2 == 178975647)'],
            999999: []
        },
        'testarea_variables': {
            491: ['background__ptype20t', 'background__ptype25t'], 
            729: [],
            999999: []
        },
        'municipality_variable': {
            491: ['background__ptype24'],
            729: ['background__ptype3'],
            999999: []
        }
    }
    
    config = {}

    # Adding the room specific configuration
    for key in room_specific_config:
        config[key] = room_specific_config[key].get(room_id)
    
    # Adding general configuration types
    config['must_include_variables'] = ['respondent__created', 'respondent__closetime', 'respondent__respondentid']
            
    return config