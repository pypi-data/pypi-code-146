from collections        import Counter, defaultdict, Iterable
from functools          import lru_cache  


          
            
            
            
#############################################################################################################
###
### List
###
############################################################################################################# 



def remove_dups(seq):
    '''Remove dups from a list whilst-preserving-order''' 
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


 



# Sort list by a list of prioritized objects
# You can prepare the priority object with make_priority_dict,
# if you want to use always the same in pandas
def sort_by_priority_list(sortme_list, priority):
    '''Sort a list by a list or tuple of prioritized objects.
    (You can prepare the priority object with make_priority_dict,
    if you want to use always the same priorities in pandas)    
    '''
    
    if len(sortme_list) < 2:
        return sortme_list

    if type(priority) is tuple:
        priority = make_priority_dict(priority)
        
    elif type(priority) is list:
        priority = make_priority_dict(tuple(priority))        
        
    priority_getter = priority.__getitem__  # dict.get(key)
    return sorted(sortme_list, key=priority_getter)



@lru_cache
def make_priority_dict(priority_tuple):
    #print('Neuberechnung')
    priority_list = list(priority_tuple)
    return defaultdict(   lambda: len(priority_list), zip(priority_list, range(len(priority_list)),),   )    




#############################################################################################################
###
### Counter
###
############################################################################################################# 



def cut_counter( counts, cut_percent ):
    '''Truncates rare values of a counter, given a percent value 0..100'''
    if cut_percent <= 0:
        return counts
    if cut_percent >= 100:
        return Counter()    
    minvalue = int(0.5 + sum(counts.values()) * (cut_percent / 100.0))
    #print(minvalue)
    filtered = { k:counts[k] for k in counts if counts[k] > minvalue } 
    return Counter(filtered)

counter_belöschen = cut_counter    




def ranking_from_counter( counts ):
    '''Converts a counter into a ranking.
    Returns a sorted dict.'''
    ranking = {pair[0]: rank  for rank, pair in enumerate(counts.most_common())}   
    return ranking     





#############################################################################################################
###
### Iterable
###
############################################################################################################# 


def flatten(items):
    """Yield all items from any nested iterable"""
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
            for sub_x in flatten(x):
                yield sub_x
        else:
            yield x


            
    
    
