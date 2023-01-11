import jax.numpy as np
from jax.lax import *
from jax import custom_jvp,jvp,interpreters
from functools import partial
from noloadj.ODE.ode45 import rk_step,rk_step_der,optimal_step,interpolation,\
    GetTimeofNextVarHit,init_etat

def odeint45_extract(f,y0,*args,h0=1e-5,tol=1.48e-8):
    return _odeint45(f,h0,tol,y0,*args)


@partial(custom_jvp,nondiff_argnums=(0,1,2))
def _odeint45(f,h0,tol,y0,*args):
    type,cond_stop=f.stop

    def cond_fn(state):
        y_prev2,_,y_prev,t_prev,h,cstr,_=state
        if type=='seuil':
            val,seuil=cond_stop(y_prev,f.names)
            valp,_=cond_stop(y_prev2,f.names)
            return (h>0) & (np.sign(val-seuil)==np.sign(valp-seuil))
        else:
            return (h > 0) & cond_stop(t_prev,t_prev+h,cstr)


    def body_fn(state):
        _,_,y_prev,t_prev,h,cstr,i=state
        y,yest,t_now,inew,hopt,condition=None,None,0.,0,0.,None
        if hasattr(f,'etat_actuel'):
            f.etat_actuel=i
        y,yest,t_now=rk_step(y_prev,t_prev,h,f.derivative,*args)
        if hasattr(f,'cond_etat'):
            tpdi=f.commande(t_now)
            inew=np.argmax(np.array(f.cond_etat(y,t_now)))
            y=cond(inew!=i,lambda y:init_etat(f,y,inew),lambda y:y,y)
            tevent=GetTimeofNextVarHit(t_now,t_prev,f,y,y_prev,tpdi)
            hopt = optimal_step(y,yest, h, tol)
            hopt=np.minimum(tevent-t_now,hopt)
            hopt=np.where(inew!=i,h0,hopt) # pour accelerer code
        else:
            inew=i
        if hasattr(f,'event'):
            for e in f.event:
                name,signe,seuil,name2,chgt_etat=e
                output,outputprev=get_indice(f.names,y,[name]),\
                                      get_indice(f.names,y_prev,[name])
                if signe=='<':
                    condition=np.bitwise_and(output<seuil,
                              np.bitwise_not(np.allclose(outputprev-seuil,0.)))
                elif signe=='>':
                    condition=np.bitwise_and(output>seuil,
                              np.bitwise_not(np.allclose(outputprev-seuil,0.)))
                hopt = optimal_step(y, yest, h, tol)
                y,h,_,_,t_now,_,_=cond(condition,interpolation,
                        lambda state:state,(y,h,y_prev,t_prev,t_now,
                                            output-seuil,outputprev-seuil))
                yevent=cond(condition,chgt_etat,lambda state:state,
                                        get_indice(f.names,y,[name2]))
                y=y.at[f.names.index(name2)].set(yevent)
        elif not hasattr(f,'event') and not hasattr(f,'cond_etat'):
            hopt = optimal_step(y, yest, h, tol)

        if type=='seuil':
            output,seuil=cond_stop(y,f.names)
            outputprev,_=cond_stop(y_prev,f.names)
            y,hopt,_,_,t_now,_,_=cond(
                np.sign(output-seuil)!=np.sign(outputprev-seuil),interpolation,
                lambda state:state,(y,hopt,y_prev,t_prev,t_now,output-seuil,
                                    outputprev-seuil))

        if f.constraints!={}:
            for i in f.constraints.keys():
                if isinstance(f.constraints[i][1],tuple):
                    test_exp,(_,expression,_,_,_,_)=f.constraints[i]
                else:
                    (_,expression,_,_,_,_)=f.constraints[i]
                    test_exp = lambda t: True
                cstr[i]=np.where(test_exp(t_now),expression(t_prev,
                            y_prev, t_now, y,cstr[i],h,T,f.names),cstr[i])

        return y_prev,t_prev,y,t_now,hopt,cstr,inew

    cstr=dict(zip(list(f.constraints.keys()),[0.]*len(f.constraints)))# INITIALISATION
    if f.constraints!={}:
        for i in f.constraints.keys():
            if isinstance(f.constraints[i][1],tuple):
                test_exp,(init,_,_,_,_,_)=f.constraints[i]
            else:
                (init,_,_,_,_,_)=f.constraints[i]
                test_exp=lambda t:True
            cstr[i]=np.where(test_exp(0.),init(y0,0.,h0,f.names),cstr[i])

    if hasattr(f,'etat_actuel'):
        i0=f.etat_actuel
        T=f.T
    else:
        i0=0
        T=0.
    _,_,yf,ts,h,cstr,_=while_loop(cond_fn,body_fn,(y0,0.,y0,0.,h0,cstr,i0))
    if f.constraints!={}:
        for i in f.constraints.keys():
            if isinstance(f.constraints[i][1],tuple):
                _,(_,_,fin,_,_,_)=f.constraints[i]
            else:
                (_,_,fin,_,_,_)=f.constraints[i]
            cstr[i]=fin(ts,cstr[i],T)

    return (ts,yf,cstr)


@_odeint45.defjvp
def _odeint45_jvp(f,h0,tol, primals, tangents):
  y0, *args = primals
  delta_y0, *delta_args = tangents
  nargs = len(args)

  def f_aug(y0,delta_y0, t, *args_and_delta_args):
    args, delta_args = args_and_delta_args[:nargs], args_and_delta_args[nargs:]
    primal_dot, tangent_dot = jvp(f.derivative, (y0, t, *args), (delta_y0,
                                                            0., *delta_args))
    return tangent_dot

  yf,cstr,ts,dts,yf_dot,cstr_dot=odeint45_etendu(f,f_aug,nargs,h0,
                tol, y0,delta_y0, *args, *delta_args)
  return (ts,yf,cstr),(dts,yf_dot,cstr_dot)


def odeint45_etendu(f,f_aug,nargs,h0,tol,y0,delta_y0,*args):
    args_red = args[:nargs]
    type,cond_stop=f.stop

    def cond_fn(state):
        y_prev2,_,_,y_prev,delta_y_prev, t_prev, h,cstr,_,_ = state
        if type=='seuil':
            val,seuil=cond_stop(y_prev,f.names)
            valp,_ = cond_stop(y_prev2,f.names)
            return (h>0) & (np.sign(val-seuil)==np.sign(valp-seuil))
        else:
            return (h > 0) & cond_stop(t_prev,t_prev+h,cstr)


    def body_fn(state):
        _,_,_,y_prev,delta_y_prev, t_prev, h,cstr,delta_cstr,i = state
        y,yest,delta_y,t_now,inew,hopt,condition = None, None, None,0.,None,0.,\
                                                   None
        if hasattr(f,'etat_actuel'):
            f.etat_actuel=i
        y,yest,t_now=rk_step(y_prev,t_prev,h,f.derivative,*args_red)
        if hasattr(f,'cond_etat'):
            tpdi=f.commande(t_now)
            inew=np.argmax(np.array(f.cond_etat(y,t_now)))
            y=cond(inew!=i,lambda y:init_etat(f,y,inew),lambda y:y,y)
            tevent=GetTimeofNextVarHit(t_now,t_prev,f,y,y_prev,tpdi)
            hopt = optimal_step(y,yest, h, tol)
            hopt=np.minimum(tevent-t_now,hopt)
            hopt=np.where(inew!=i,h0,hopt) # pour accelerer code
        else:
            inew=i
        if hasattr(f,'event'):
            for e in f.event:
                name,signe,seuil,name2,chgt_etat=e
                output,outputprev=get_indice(f.names,y,[name]),\
                                      get_indice(f.names,y_prev,[name])
                if signe=='<':
                    condition=np.bitwise_and(output<seuil,
                              np.bitwise_not(np.allclose(outputprev-seuil,0.)))
                elif signe=='>':
                    condition=np.bitwise_and(output>seuil,
                              np.bitwise_not(np.allclose(outputprev-seuil,0.)))
                hopt = optimal_step(y, yest, h, tol)
                y,h,_,_,t_now,_,_=cond(condition,interpolation,
                        lambda state:state,(y,h,y_prev,t_prev,t_now,
                                            output-seuil,outputprev-seuil))
                yevent=cond(condition,chgt_etat,lambda state:state,
                                        get_indice(f.names,y,[name2]))
                y=y.at[f.names.index(name2)].set(yevent)
        elif not hasattr(f,'event') and not hasattr(f,'cond_etat'):
            hopt = optimal_step(y, yest, h, tol)

        if type=='seuil':
            output,seuil=cond_stop(y,f.names)
            outputprev,_=cond_stop(y_prev,f.names)
            y,hopt,_,_,t_now,_,_=cond(
                np.sign(output-seuil)!=np.sign(outputprev-seuil),interpolation,
                        lambda state:state,(y,hopt,y_prev,t_prev,t_now,
                                            output-seuil,outputprev-seuil))

        delta_y=rk_step_der(y_prev,t_prev,delta_y_prev,h,f_aug,*args)

        if f.constraints!={}:
            for i in f.constraints.keys():
                if isinstance(f.constraints[i][1], tuple):
                    test_exp,(_,expression,_,_,der_expression,_)=f.constraints[i]
                else:
                    (_,expression,_,_,der_expression,_)=f.constraints[i]
                    test_exp = lambda t: True
                cstr[i] = np.where(test_exp(t_now),expression(t_prev, y_prev,
                            t_now,y, cstr[i],h,T,f.names),cstr[i])
                delta_cstr[i]= np.where(test_exp(t_now),der_expression(t_prev,
                    y_prev,delta_y_prev, t_now, y,delta_y,cstr[i],delta_cstr[i],
                    h,T,f.names),delta_cstr[i])

        return y_prev,delta_y_prev,t_prev,y, delta_y,t_now, hopt,cstr,\
               delta_cstr,inew

    cstr=dict(zip(list(f.constraints.keys()),[0.]*len(f.constraints)))#INITIALISATION
    delta_cstr=dict(zip(list(f.constraints.keys()),[0.]*len(f.constraints)))
    if f.constraints!={}:
        for i in f.constraints.keys():
            if isinstance(f.constraints[i][1], tuple):
                test_exp,(init,_,_,dinit,_,_) = f.constraints[i]
            else:
                (init,_,_,dinit,_,_) = f.constraints[i]
                test_exp = lambda t: True
            cstr[i] = np.where(test_exp(0.),init(y0,0.,h0,f.names),cstr[i])
            delta_cstr[i]=np.where(test_exp(0.),dinit(y0,delta_y0,0.,h0,f.names),
                                     delta_cstr[i])

    for element in f.__dict__.keys(): # pour eviter erreurs de code
        if isinstance(f.__dict__[element],interpreters.ad.JVPTracer):
            f.__dict__[element]=f.__dict__[element].primal
    if hasattr(f,'etat_actuel'):
        i0=f.etat_actuel
        T=f.T
    else:
        i0=0
        T=0.
    yfm1,_,_,yf,delta_yf,ts,h,cstr,delta_cstr,ifinal=while_loop(cond_fn,
        body_fn,(y0,delta_y0,0.,y0,delta_y0,0.,h0,cstr,delta_cstr,i0))

    if f.constraints!={}:
        for i in f.constraints.keys():
            if isinstance(f.constraints[i][1],tuple):
                _,(_,_,fin,_,_,der_fin)=f.constraints[i]
            else:
                (_,_,fin,_,_,der_fin)=f.constraints[i]
            cstr[i]=fin(ts,cstr[i],T)
            delta_cstr[i]=der_fin(ts,cstr[i],T,delta_cstr[i])

    if type=='seuil': # partial derivatives of ts
        dout,_=cond_stop(delta_yf,f.names)
        yseuil,_=cond_stop(f.derivative(yf,ts,*args_red),f.names)
        dts=-(1/yseuil)*dout
    elif type=='rp':
        f.etat_actuel=ifinal
        ind_rp=f.names.index(f.last_var_bf_rp)
        yseuil=f.derivative(yf,ts,*args_red)[ind_rp]
        dts=-(1/yseuil)*delta_yf[ind_rp]
    else:
        dts=0.
    return yf,cstr,ts,dts,delta_yf,delta_cstr


################################################################################
def T_pair(T):
    return lambda t:(t//T)%2==0

def T_impair(T):
    return lambda t:(t//T)%2!=0

def T_numero(T,n,i):
    return lambda t:(t//T)%n!=i

def Min(ind):
    return lambda y0,t0,h0,names:y0[names.index(ind)],\
        lambda t_prev,y_prev,t,y,cstr,h,_,names:np.minimum(
               y[names.index(ind)],cstr), \
        lambda tchoc,cstr,_:cstr,\
        lambda y0,dy0,t0,h0,names:dy0[names.index(ind)],\
        lambda t_prev,y_prev,dprev,t,y,dy,cstr,dcstr,h,_,names:\
               np.where(np.minimum(cstr,y[names.index(ind)])==
                        y[names.index(ind)],dy[names.index(ind)],dcstr),\
        lambda tchoc,cstr,_,dcstr:dcstr

def Max(ind):
    return lambda y0,t0,h0,names:y0[names.index(ind)],\
        lambda t_prev,y_prev,t,y,cstr,h,_,names:np.maximum\
               (y[names.index(ind)],cstr), \
        lambda tchoc,cstr,_:cstr,\
        lambda y0,dy0,t0,h0,names:dy0[names.index(ind)],\
        lambda t_prev,y_prev,dprev,t,y,dy,cstr,dcstr,h,_,names:\
               np.where(np.maximum(cstr,y[names.index(ind)])==
                        y[names.index(ind)],dy[names.index(ind)],dcstr),\
        lambda tchoc,cstr,_,dcstr:dcstr

def moy(ind):
    return lambda y0,t0,h0,names:0.,\
        lambda t_prev,y_prev,t,y,cstr,h,_,names:cstr+0.5*h*\
          (y_prev[names.index(ind)]+y[names.index(ind)]),\
        lambda tchoc,cstr,_:cstr/tchoc,\
        lambda y0,dy0,t0,h0,names:0.,\
        lambda t_prev,y_prev,dprev,t,y,dy,cstr,dcstr,h,_,names: \
            dcstr+0.5*h*(dprev[names.index(ind)]+ dy[names.index(ind)]),\
        lambda tchoc,cstr,_,dcstr:dcstr/tchoc

def eff(ind):
    return lambda y0,t0,h0,names:0.,\
        lambda t_prev,y_prev,t,y,cstr,h,_,names: cstr+0.5*h*\
            (y_prev[names.index(ind)]**2+y[names.index(ind)]**2),\
        lambda tchoc,cstr,_:np.sqrt(cstr/tchoc),\
        lambda y0,dy0,t0,h0,names:0.,\
        lambda t_prev,y_prev,dprev,t,y,dy,cstr,dcstr,h,_,names: \
        dcstr+0.5*h*(2*y_prev[names.index(ind)]*dprev[names.index(ind)]+
                     2*y[names.index(ind)]* dy[names.index(ind)]),\
        lambda tchoc,cstr,_,dcstr:dcstr/(2*tchoc*cstr)

def min_T(T,ind):
    return lambda y0,t0,h0,names:y0[names.index(ind)],\
        lambda t_prev,y_prev,t,y,cstr,h,_,names:np.where((t_prev//T)==(t//T),
            np.minimum(y[names.index(ind)],cstr),y[names.index(ind)]), \
        lambda tchoc,cstr,_:cstr, \
        lambda y0,dy0,t0,h0,names:dy0[names.index(ind)],\
        lambda t_prev,y_prev,dprev,t,y,dy,cstr,dcstr,h,_,names:\
            np.where((t_prev//T)==(t//T),np.where(np.minimum(cstr,
                y[names.index(ind)])==y[names.index(ind)],dy[names.index(ind)],
                                                  dcstr),dy[names.index(ind)]),\
        lambda tchoc,cstr,_,dcstr:dcstr

def max_T(T,ind):
    return lambda y0,t0,h0,names:y0[names.index(ind)],\
        lambda t_prev,y_prev,t,y,cstr,h,_,names:np.where((t_prev//T)==(t//T),
            np.maximum(y[names.index(ind)],cstr),y[names.index(ind)]),\
        lambda tchoc,cstr,_:cstr,\
        lambda y0,dy0,t0,h0,names:dy0[names.index(ind)],\
        lambda t_prev,y_prev,dprev,t,y,dy,cstr,dcstr,h,_,names:\
            np.where((t_prev//T)==(t//T),np.where(np.maximum(cstr,
                y[names.index(ind)])==y[names.index(ind)],dy[names.index(ind)],
                                                  dcstr),dy[names.index(ind)]),\
        lambda tchoc,cstr,_,dcstr:dcstr

def moy_T(ind):
    return lambda y0,t0,h0,names:0.,\
        lambda t_prev,y_prev,t,y,cstr,h,T,names:np.where((t_prev//T)==(t//T),
        cstr+0.5*h*(y_prev[names.index(ind)]+y[names.index(ind)]), 0.),\
        lambda tchoc,cstr,T:cstr/T,\
        lambda y0,dy0,t0,h0,names:0.,\
        lambda t_prev,y_prev,dprev,t,y,dy,cstr,dcstr,h,T,names: \
        np.where((t_prev//T)==(t//T),dcstr+0.5*h*(dprev[names.index(ind)]+
            dy[names.index(ind)]),0.),\
        lambda tchoc,cstr,T,dcstr:dcstr/T

def eff_T(ind):
    return lambda y0,t0,h0,names:0.,\
        lambda t_prev,y_prev,t,y,cstr,h,T,names: np.where((t_prev//T)==(t//T),
        cstr+0.5*h*(y_prev[names.index(ind)]**2+y[names.index(ind)]**2),0.),\
        lambda tchoc,cstr,T:np.sqrt(cstr/T),\
        lambda y0,dy0,t0,h0,names:0.,\
        lambda t_prev,y_prev,dprev,t,y,dy,cstr,dcstr,h,T,names: \
        np.where((t_prev//T)==(t//T),dcstr+0.5*h*(2*y_prev[names.index(ind)]*
            dprev[names.index(ind)]+2*y[names.index(ind)]*
            dy[names.index(ind)]),0.),\
        lambda tchoc,cstr,T,dcstr:dcstr/(2*T*cstr)


def reg_perm(T,nbT,names_var,a=1e-5):
    constr = {}
    for i in range(len(names_var)):
        constr[names_var[i]+'_min']=(T_pair(nbT * T),
                                     min_T(nbT * T, names_var[i]))
        constr[names_var[i]+'_minimp']=(T_impair(nbT * T),
                                     min_T(nbT * T, names_var[i]))
        constr[names_var[i]+'_max']=(T_pair(nbT * T),
                                     max_T(nbT * T, names_var[i]))
        constr[names_var[i]+'_maximp']=(T_impair(nbT * T),
                                     max_T(nbT * T, names_var[i]))
    def regime_perm(t_prev,t,cstr):
        vectp,vectimp=np.zeros(2*len(names_var)),np.zeros(2*len(names_var))
        for i in range(len(names_var)):
            vectp=vectp.at[i].set(cstr[names_var[i]+'_min'])
            vectp=vectp.at[2*i+1].set(cstr[names_var[i]+'_max'])
            vectimp=vectimp.at[i].set(cstr[names_var[i]+'_minimp'])
            vectimp=vectimp.at[2*i+1].set(cstr[names_var[i]+'_maximp'])
        return np.bitwise_not(np.bitwise_and(np.allclose(vectp,vectimp,atol=a),
                    np.not_equal(t_prev//T,t//T)))
    return ('rp',regime_perm),constr

def seuil(ind,seuil=0.):
    return ('seuil', lambda y,names: (y[names.index(ind)], seuil))

def temps_final(tf):
    return ('tf',lambda t_prev,t,cstr:t_prev<tf)

def get_indice(names,valeur,output):
    if len(output)==1:
        return valeur[names.index(output[0])]
    else:
        return (valeur[names.index(i)] for i in output)
