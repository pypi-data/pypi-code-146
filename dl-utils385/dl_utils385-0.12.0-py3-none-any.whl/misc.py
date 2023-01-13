import warnings
warnings.filterwarnings('ignore')
from datetime import datetime
from sklearn.metrics import normalized_mutual_info_score as mi_func
from pdb import set_trace
import math
try:
    import matplotlib.cm as cm
    import matplotlib.pyplot as plt
except ImportError:
    pass
import numpy as np
import os
import sys
from dl_utils.tensor_funcs import numpyify

def reload():
    import importlib, utils
    importlib.reload(utils)

def show_xb(xb): plt.imshow(xb[0,0]); plt.show()
def get_datetime_stamp(): return str(datetime.now()).split()[0][5:] + '_'+str(datetime.now().time()).split()[0][:-7]

def get_user_yesno_answer(question):
    answer = input(question+'(y/n)')
    if answer == 'y': return True
    elif answer == 'n': return False
    else:
        print("Please answer 'y' or 'n'")
        return(get_user_yesno_answer(question))

def set_experiment_dir(exp_dir, overwrite, use_datetime_as_dir=False, name_of_trials='try'):
    if exp_dir == "" or use_datetime_as_dir:
        exp_dir = get_datetime_stamp()
    if not os.path.isdir(exp_dir): os.makedirs(exp_dir)
    elif exp_dir.startswith(name_of_trials) or overwrite: pass
    elif not get_user_yesno_answer(f'An experiment with name {exp_dir} has already been run, do you want to overwrite?'):
        print('Please rerun command with a different experiment name')
        sys.exit()
    return exp_dir

def test_mods_eq(m1,m2):
    for a,b in zip(m1.parameters(),m2.parameters()):
        assert (a==b).all()

def compose(funcs):
    def _comp(x):
        for f in funcs: x=f(x)
        return x
    return _comp

def scatter_clusters(embeddings,labels,show=False):
    fig, ax = plt.subplots()
    palette = ['r','k','y','g','b','m','purple','brown','c','orange','thistle','lightseagreen','sienna']
    labels = numpyify([0]*len(embeddings)) if labels is None else numpyify(labels)
    palette = cm.rainbow(np.linspace(0,1,len(set(labels))))
    for i,label in enumerate(list(set(labels))):
        ax.scatter(embeddings[labels==label,0], embeddings[labels==label,1], s=0.2, c=[palette[i]], label=i)
    ax.legend()
    if show: plt.show()
    return ax

def asMinutes(s):
    h = math.floor(s/3600)
    s -= h*3600
    m = math.floor(s/60)
    s -= m*60
    return f'{h:.0f}h {m:.0f}m {s:.2f}s'

def compute_multihots(l,probs):
    assert len(l) > 0
    mold = np.expand_dims(np.arange(l.max()+1),0) # (num_aes, num_labels)
    hits = (mold==np.expand_dims(l,2)) # (num_aes, dset_size, num_labels)
    if probs != 'none': hits = np.expand_dims(probs,2)*hits
    multihots = hits.sum(axis=0) # (dset_size, num_labels)
    return multihots

def n_digitify(number,num_digits):
    """Turn 'number' into a string of length 'num_digits', adding leading zeroes as needed"""
    with_zeros = "0"*(num_digits-len(str(number))) + str(number)
    assert len(with_zeros) == num_digits and int(with_zeros) == number
    return with_zeros

def check_latents(dec,latents,show,stacked):
    _, axes = plt.subplots(6,2,figsize=(7,7))
    for i,latent in enumerate(latents):
        try:
            outimg = dec(latent[None,:,None,None])
            if stacked: outimg = outimg[-1]
            axes.flatten()[i].imshow(outimg[0,0])
        except: set_trace()
    if show: plt.show()
    plt.clf()

def dictify_list(x,key):
    assert isinstance(x,list)
    assert len(x) > 0
    assert isinstance(x[0],dict)
    return {item[key]: item for item in x}

def cont_factorial(x): return (x/np.e)**x*(2*np.pi*x)**(1/2)*(1+1/(12*x))
def cont_choose(ks): return cont_factorial(np.sum(ks))/np.prod([cont_factorial(k) for k in ks if k > 0])
def prob_results_given_c(results,cluster,prior_correct):
    """For single dpoint, prob of these results given right answer for cluster.
    ARGS:
        results (np.array): votes for this dpoint
        cluster (int): right answer to condition on
        prior_correct (\in (0,1)): guess for acc of each element of ensemble
        """

    assert len(results.shape) <= 1
    prob = 1
    results_normed = np.array(results)
    results_normed = results_normed / np.sum(results_normed)
    for c,r in enumerate(results_normed):
        if c==cluster: prob_of_result = prior_correct**r
        else: prob_of_result = ((1-prior_correct)/results.shape[0])**r
        prob *= prob_of_result
    partitions = cont_choose(results_normed)
    prob *= partitions
    try:assert prob <= 1
    except:set_trace()
    return prob

def prior_for_results(results,prior_correct):
    probs = [prob_results_given_c(results,c,prior_correct) for c in range(results.shape[0])]
    set_trace()
    return sum(probs)

def all_conditionals(results,prior_correct):
    """For each class, prob of results given that class."""
    cond_probs = [prob_results_given_c(results,c,prior_correct) for c in range(len(results))]
    assert np.sum(cond_probs) < 1.01
    return np.array(cond_probs)

def posteriors(results,prior_correct):
    """Bayes to get prob of each class given these results."""
    conditionals = all_conditionals(results,prior_correct)
    posterior_array = conditionals/np.sum(conditionals)
    return posterior_array

def posterior_corrects(results):
    probs = []
    for p in np.linspace(0.6,1.0,10):
        conditional_prob = np.prod([np.sum(all_conditionals(r,p)) for r in results])
        probs.append(conditional_prob)
    probs = np.array(probs)
    posterior_for_accs = 0.1*probs/np.sum(probs) # Prior was uniform over all accs in range
    assert posterior_for_accs.max() < 1.01
    return posterior_for_accs

def votes_to_probs(multihots,prior_correct):
    """For each dpoint, compute probs for each class, given these ensemble votes.
    ARGS:
        multihots (np.array): votes for each dpoint, size N x num_classes
        prior_correct (\in (0,1)): guess for acc of each element of ensemble
        """

    probs_list = [np.ones(multihots.shape[-1])/multihots.shape[-1] if r.max() == 0 else posteriors(r,prior_correct) for r in multihots]
    probs_array = np.array(probs_list)
    return probs_array

def check_dir(directory):
    exists_already = os.path.isdir(directory)
    if not exists_already:
        os.makedirs(directory)
    return exists_already

def np_save(array,directory,fname,verbose=False):
    check_dir(directory)
    save_path = os.path.join(directory,fname)
    if verbose: print('Saving to', save_path)
    np.save(save_path,array)

def np_savez(data_dict,directory,fname):
    check_dir(directory)
    np.savez(os.path.join(directory,fname),**data_dict)

def rmi_func(pred,gt): return round(mi_func(pred,gt),4)
