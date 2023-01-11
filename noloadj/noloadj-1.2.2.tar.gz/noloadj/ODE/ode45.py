import jax.numpy as np
from jax.lax import *
from jax import custom_jvp,jvp,interpreters
from functools import partial

def odeint45(f,y0,t,*args,h0=1e-5,tol=1.48e-8):
    return _odeint45(f,h0,tol,y0,t,*args)


def rk_step(y_prev, t_prev, h,f,*args):
    k1=f(y_prev, t_prev,*args)
    k2 = f(y_prev + h*0.2 * k1, t_prev + 0.2 * h,*args)
    k3 = f(y_prev + h*(3 * k1 + 9 * k2) / 40,t_prev + 3 * h / 10,*args)
    k4 = f(y_prev + h*(44 * k1 / 45 - 56 * k2 / 15 + 32 * k3 / 9),t_prev +
           4 * h / 5,*args)
    k5 = f(y_prev + h*(19372 * k1 / 6561 - 25360 * k2 / 2187 +
            64448 * k3 / 6561- 212 * k4 / 729),
           t_prev + 8 * h / 9,*args)
    k6 = f(y_prev + h*(9017 * k1 / 3168 - 355 * k2 / 33 + 46732 * k3 / 5247+
            49 * k4 / 176 - 5103 * k5 / 18656),t_prev + h,*args)
    k7 = f(y_prev + h*(35 * k1 / 384 + 500 * k3 / 1113 +
            125 * k4 / 192 -2187 * k5 / 6784 + 11 * k6 / 84),t_prev + h,*args)

    y = y_prev + h *(35 * k1 / 384 + 500 * k3 / 1113 + 125 * k4 / 192
             -2187 * k5 / 6784 + 11 * k6 / 84)
    yest = y_prev + h *(5179 * k1 / 57600 + 7571* k3 / 16695 + 393 * k4 /640
            - 92097 * k5 / 339200 + 187 * k6 / 2100 + k7 / 40)
    t_now = t_prev + h
    return y, yest, t_now


def optimal_step(y,yest,h,tol,errcon=1.89e-4):
    est=np.linalg.norm(y-yest)
    R = (est+1e-16) / h
    err_ratio = R / tol
    delta = (2*err_ratio)**(-0.2)
    h=np.where(est>=errcon,h*delta,1.0*h)
    return h

def prediction(t,tprev,val_seuil,output,outputprev):
    return t+(t-tprev)*(val_seuil-output)/(output-outputprev)

def interpolation(state):
    y,h,y_prev,t_prev,t_now,output,outputprev=state
    tchoc=(-t_prev*output+t_now*outputprev)/(outputprev-output)
    h=tchoc-t_prev
    ychoc=(y_prev-y)*tchoc/(t_prev-t_now)+(t_prev*y-t_now*y_prev)/(t_prev-t_now)
    return ychoc,h,y_prev,t_prev,tchoc,output,outputprev

def GetTimeofNextVarHit(t,tprev,f,y,y_prev,tevent):
    for element in f.zero_crossing:
        _,i,outputi=element
        ind=f.names.index(i)
        if isinstance(outputi,float):
            val_seuil=outputi
        else:
            val_seuil=y[f.names.index(outputi)]
        temp=prediction(t,tprev,val_seuil,y[ind],y_prev[ind])
        tevent=cond(temp>t,lambda tevent:np.minimum(tevent,temp),
                    lambda tevent:tevent,tevent)
    return tevent+1e-12

def init_etat(f,y,inew):
    for element in f.zero_crossing:
        new_state,i,outputi=element
        ind=f.names.index(i)
        if isinstance(outputi,float):
            y=y.at[ind].set(np.where(inew==new_state,outputi,y[ind]))
        else:
            y=y.at[ind].set(np.where(inew==new_state,y[f.names.index(outputi)],
                                   y[ind]))
    return y

@partial(custom_jvp,nondiff_argnums=(0,1,2))
def _odeint45(f,h0,tol,y0,t,*args):

    def scan_fun(state,t):

        def cond_fn(state):
            y_prev,t_prev,h,_=state
            return (t_prev<t) & (h>0)

        def body_fn(state):
            y_prev,t_prev,h,i=state
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

            return y,t_now,hopt,inew

        y,t1,h,i = while_loop(cond_fn, body_fn, state)
        return (y,t1,h,i),y

    if hasattr(f,'etat_actuel'):
        i0=f.etat_actuel
    else:
        i0=0
    _,ys=scan(scan_fun,(y0,t[0],h0,i0),t[1:])
    ys=np.transpose(np.concatenate((y0[None], ys)))
    return ys


@_odeint45.defjvp
def _odeint45_jvp(f,h0,tol, primals, tangents):
  y0, t, *args = primals
  delta_y0, _, *delta_args = tangents
  nargs = len(args)

  def f_aug(y0,delta_y0, t, *args_and_delta_args):
    args, delta_args = args_and_delta_args[:nargs], args_and_delta_args[nargs:]
    primal_dot, tangent_dot = jvp(f.derivative, (y0, t, *args), (delta_y0,
                                                    0., *delta_args))
    return tangent_dot

  ys,ys_dot = odeint45_etendu(f,f_aug,nargs,h0,tol, y0,delta_y0,
                                        t, *args, *delta_args)
  return ys,ys_dot

def rk_step_der(y_prev, t_prev, delta_y_prev,h,f_aug,*args):
    k1 = f_aug(y_prev, delta_y_prev, t_prev, *args)
    k2 = f_aug(y_prev, delta_y_prev + h * 0.2 * k1,t_prev + 0.2 * h , *args)
    k3 = f_aug(y_prev, delta_y_prev + h * (3 * k1 + 9 * k2) / 40,t_prev
               +3 * h / 10, *args)
    k4 = f_aug(y_prev,delta_y_prev + h*(44 * k1 / 45 - 56 * k2 /15+32*k3/9),
               t_prev + 4 * h / 5,*args)
    k5 = f_aug(y_prev, delta_y_prev + h * (19372 * k1 / 6561 - 25360*k2/2187
                + 64448 * k3 / 6561 - 212 * k4 / 729),t_prev + 8 * h / 9, *args)
    k6 = f_aug(y_prev,delta_y_prev+h*(9017 * k1 / 3168 -355 *k2/33 +46732*k3
            / 5247 + 49 * k4 / 176 - 5103 * k5 / 18656),t_prev + h, *args)
    delta_y = delta_y_prev + h *(35 * k1 / 384 + 500 * k3 / 1113 +
            125 * k4 / 192 - 2187 * k5 / 6784 + 11 * k6 / 84)
    return delta_y


def odeint45_etendu(f,f_aug,nargs,h0,tol,y0,delta_y0,t,*args):
    args_red = args[:nargs]

    def scan_fun(state, t):

        def cond_fn(state):
            y_prev,delta_y_prev, t_prev, h,_ = state
            return (t_prev < t) & (h > 0)

        def body_fn(state):
            y_prev,delta_y_prev, t_prev, h,i = state
            y,yest,delta_y,t_now,inew,hopt,condition=None,None,None,0.,0,0.,None
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

            delta_y=rk_step_der(y_prev,t_prev,delta_y_prev,h,f_aug,*args)

            return y, delta_y,t_now, hopt,inew

        y, delta_y,t1, h,i = while_loop(cond_fn, body_fn, state)
        return (y,delta_y, t1, h,i), (y,delta_y)

    for element in f.__dict__.keys(): # pour eviter erreurs de code
        if isinstance(f.__dict__[element],interpreters.ad.JVPTracer):
            f.__dict__[element]=f.__dict__[element].primal
    if hasattr(f,'etat_actuel'):
        i0=f.etat_actuel
    else:
        i0=0
    _, (ys,delta_ys) = scan(scan_fun, (y0, delta_y0,t[0], h0,i0), t[1:])
    ys=np.transpose(np.concatenate((y0[None], ys)))
    delta_ys=np.transpose(np.concatenate((delta_y0[None], delta_ys)))
    return ys,delta_ys


def get_indice(names,valeur,output):
    if len(output)==1:
        return valeur[names.index(output[0])]
    else:
        return (valeur[names.index(i)] for i in output)