"""Implements a variety of prediction models."""
from collections import Counter


def principal_delta(principal, other, potential):
    modification = abs(principal - other)*potential
    if other < principal:
        return principal - modification
    elif other > principal:
        return principal + (abs(other - principal)*potential)

def model_per_emotive(ensemble, emotive, potential_normalization_factor):
    "Using a Weighted Moving Average, though the 'moving' part refers to the prediction index."
    ## using a weighted posterior_probability = potential/marginal_probability
    ## FORMULA: pv + ( (Uprediction_2-pv)*(Wprediction_2) + (Uprediction_3-pv)*(Wprediction_3)... )/mp
    _found = False
    while not _found:
        for i in range(0,len(ensemble)):
            if emotive in ensemble[i]['emotives'].keys():
                _found = True
                principal_value = ensemble[i]['emotives'][emotive]  ## Let's use the "best" match (i.e. first showing of this emotive) as our starting point. Alternatively, we can use,say, the average of all values before adjusting.
                break
        if i == len(ensemble) and not _found:
            return 0
        if i == len(ensemble) and _found:
            return principal_value
    marginal_probability = sum([x["potential"] for x in ensemble])
    v = principal_value
    for x in ensemble[i+1:]:
        if emotive in x['emotives']:
            v += (x["potential"]/potential_normalization_factor) * (principal_value - x['emotives'][emotive])
            potential_normalization_factor
    return v

def average_emotives(record):
    '''Averages the emotives in a list (e.g. predictions ensemble or percepts).
    The emotives in the record are of type: [{'e1': 4, 'e2': 5}, {'e2': 6}, {'e1': 5 'e3': -4}]
    '''
    new_dict = {}
    for bunch in record:
        for e,v in bunch.items():
            if e not in new_dict:
                new_dict[e] = [v]
            else:
                new_dict[e].append(v)
    avg_dict = {}
    for e,v in new_dict.items():
        avg_dict[e] = float(sum(v)/len(v))
    return avg_dict

def bucket_predictions(ensemble):
    bucket_dict = {}
    
    for pred in ensemble:
        
        if pred['potential'] in bucket_dict.keys():
            bucket_dict[pred['potential']].append(pred)
        else:
            bucket_dict[pred['potential']] = [pred]
    
    new_ensemble = []
    for k,v in bucket_dict.items():
        
        singular_pred = v[0]
        singular_pred['emotives'] = average_emotives([p['emotives'] for p in v])
        
        new_ensemble.append(singular_pred)
    
    return new_ensemble
         
    
def make_modeled_emotives(ensemble):
    '''The emotives in the ensemble are of type: 'emotives':[{'e1': 4, 'e2': 5}, {'e2': 6}, {'e1': 5 'e3': -4}]'''
    

    emotives_set = set()
    potential_normalization_factor = sum([p['potential'] for p in ensemble])
    
    filtered_ensemble = []
    for p in ensemble:
        new_record = p
        new_record['emotives'] = average_emotives([p['emotives']])
        filtered_ensemble.append(new_record)
    
    filtered_ensemble = bucket_predictions(filtered_ensemble)
    
    for p in filtered_ensemble:
        emotives_set = emotives_set.union(p['emotives'].keys())
    return {emotive: model_per_emotive(ensemble, emotive, potential_normalization_factor) for emotive in emotives_set}


def hive_model_emotives(ensembles):
    """Average of final node predictions."""
    return average_emotives(ensembles)

def prediction_ensemble_model_classification(ensemble):
    """For classifications, we don't bother with marginal_probability because classifications are discrete symbols, not numeric values."""
    boosted_prediction_classes = Counter()
    for prediction in ensemble:
        for symbol in prediction['future'][-1]:
            if "|" in symbol:
                symbol = symbol.split("|")[-1]  # grab the value, remove the piped keys
            boosted_prediction_classes[symbol] += prediction['potential']
    if len(boosted_prediction_classes) > 0:
        return boosted_prediction_classes.most_common(1)[0][0]
    else:
        return None

def hive_model_classification(ensembles):
    """Every node gets a vote."""
    if ensembles:
        # This just takes the first "most common", even if there are multiple that have the same frequency.
        boosted_classifications = [prediction_ensemble_model_classification(c) for c in ensembles.values()]
        votes = Counter([p for p in boosted_classifications if p is not None]).most_common()
        if votes:
            return votes[0][0]
    return None
