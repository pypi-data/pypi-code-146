import jax.numpy as np
from jax.lax import switch
from jax import custom_jvp,jvp
import jax
from functools import partial

def fonction(res):
    return lambda _: res()

def vect_temporel(debut,fin,pas):
    return np.linspace(debut,fin,int((fin-debut)/pas))

def indice_t(t,pas,debut=0.):
    return ((t-debut)/pas).astype(int)

def Switch(etat,funcs):
    return switch(etat,[fonction(func) for func in funcs],None)

###################################################### external functions
@partial(custom_jvp,nondiff_argnums=(1,2))
def compute_external(inputs,len_output,Extfunc):
    output_type=jax.ShapeDtypeStruct((len_output,),'float64')
    def compute_intermediary_function(inputs):
        outputs=Extfunc.compute(inputs)
        return np.array(outputs)
    outputs=jax.pure_callback(compute_intermediary_function,output_type,inputs)
    return outputs

def jacobien(len_output,Extfunc,primals,tangents):
    inputs,=primals
    dinputs,=tangents
    output_type=jax.ShapeDtypeStruct((len_output,),'float64')
    def compute_intermediary_function(inputs):
        outputs=Extfunc.compute(inputs)
        return np.array(outputs)
    def jacobian_intermediary_function(inputs):
        gradients=Extfunc.jacobian(inputs)
        return np.array(gradients)
    outputs=jax.pure_callback(compute_intermediary_function,output_type,inputs)
    gradient_type=jax.ShapeDtypeStruct((len_output,len(inputs)),'float64')
    gradients=jax.pure_callback(jacobian_intermediary_function,gradient_type,
                                inputs)
    return outputs,np.dot(gradients,dinputs)

compute_external.defjvp(jacobien)
#####################################################

###################################################### integrale
@partial(custom_jvp,nondiff_argnums=(0,1,2,3))
def integrale(t0,tf,pas,f,*inputs):
    longueur=(tf-t0)/int(tf/pas)
    res=f(*inputs)
    S=2*np.sum(res)-res[0]-res[-1]
    S*=longueur*0.5
    return S

@integrale.defjvp
def integrale_jvp(t0,tf,pas,f,primals,tangents):
    longueur=(tf-t0)/int(tf/pas)
    primal_dot,tangent_dot=jvp(f,primals,tangents)
    S=2*np.sum(primal_dot)-primal_dot[0]-primal_dot[-1]
    S*=longueur*0.5
    dS = 2*np.sum(tangent_dot)-tangent_dot[0]-tangent_dot[-1]
    dS *= longueur * 0.5
    return S,dS
############################################################################