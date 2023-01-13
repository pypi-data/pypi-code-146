import numpy as np
from pdb import set_trace

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
