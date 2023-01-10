import matplotlib.pyplot as plt
import math
import numpy as np
from scipy.optimize import root_scalar

from .friction_law import f_barr_bathurst

RHO_PUREWATER = 1000
RHO_SEAWATER = 1025
KIN_VISCOSITY = 1.e-6
GRAVITY = 9.81

BED_LOAD=1
SUSPENDED_LOAD_50=2
SUSPENDED_LOAD_100=3
WASH_LOAD=4

""" 
@author : Pierre Archambeau
@date : 2022

Chezy : u = C (RJ)**.5
Strickler : C = K R**(1/6)

 --> u = K R**(2/3) J**.5
 
 en 2D : R = h
 
 --> u = K h**(2/3) J**.5
 
 J = u**2 / K**2 / h**(4/3)
 
 mais aussi
 
 J = f/D * u**2 /2 /g 
     avec D = 4h
 
 --> J = f/(4h) *u**2 /2 /g
 --> tau = J * rho * h * g

 Shields : 
   Theta = tau / ((rhom-rho) * g * d)
   Theta = tau / rho / ((s-1) * g * d)  avec s = rhom/rho

   Theta = J * h / ((s-1) * d)

 Strickler :
   J = u**2 / K**2 / h**(4/3)
   tau = J * rho * h * g

   tau = (q/K)**2 / h**(7/3) * rho  * g

Autres :
   J = f/(4h) *u**2 /2 /g
   tau = J * rho * h * g
   
   tau = f/8 * (q/h)**2 * rho  

 References:
      Telemac-Mascaret, https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/main/sources/gaia/shields.f

      Yalin, Ferraira da Silva (2001), Fluvial Processes, IAHR Monograph
      
      Fredsoe,  Jorgen and Deigaard Rolf. (1992). Mechanics of Coastal Sediment.
            Sediment Transport. Advanced Series on Ocean Engineering - Vol. 3.
            World Scientific. Singapure.
            
      Madsen, Ole S., Wood, William. (2002).  Sediment Transport Outside the 
            Surf Zone. In: Vincent, L., and Demirbilek, Z. (editors), 
            Coastal Engineering Manual, Part III, Combined wave and current 
            bottom boundary layer flow, Chapter III-6, 
            Engineer Manual 1110-2-1100, U.S. Army Corps of Engineers,
            Washington, DC.
            
      Nielsen, Peter. (1992). Coastal Bottom Boundary Layers and
            Sediment Transport. Advanced Series on Ocean Engineering - Vol. 4.
            World Scientific. Singapure.
 
"""

def get_sadim(d,rhom=2650,rho=RHO_PUREWATER):
      """ 
      s_adim = d**(3/2) * ((s-1) * g)**.5 / (4 * nu)
      
      [-] = [m^1.5 ] * [m^.5 s^-1] / [m^2 s^-1]
      """
      s=rhom/rho
      return d**(3./2.) * ((s-1) * GRAVITY)**.5 / (4 * KIN_VISCOSITY)

def get_dstar(d,rhom=2650.,rho=RHO_PUREWATER):
      
      s = rhom/rho
      return d*(GRAVITY*(s-1)/KIN_VISCOSITY**2)**(1./3.) #VanRijn Formula 

def sadim2dstar(sadim):            
      return (4*sadim)**(2/3)

def dstar2sadim(dstar):
      return dstar**(3./2.) / 4

def get_d_from_sadim(sadim,rhom=2650,rho=RHO_PUREWATER):
      """ 
      s_adim = d**(3/2) * ((s-1) * g)**.5 / (4 * nu)
      
      [-] = [m^1.5 ] * [m^.5 s^-1] / [m^2 s^-1]
      """
      s=rhom/rho
      return (sadim*(4*KIN_VISCOSITY)/math.sqrt((s-1)*GRAVITY))**(2/3)

def get_d_from_dstar(dstar,rhom=2650,rho=RHO_PUREWATER):
      """ 
      d_star = d * (g * (s-1) / nu**2)**(1/3)
      
      [-] = [m] * ([m s^-2] / [m^4 s^-2])^(1/3)
      """
      s=rhom/rho
      return dstar / (GRAVITY*(s-1)/KIN_VISCOSITY**2)**(1./3.)

def get_psi_cr(s_adim):
      """ 
      https://nl.mathworks.com/matlabcentral/fileexchange/97447-modified-shields-diagram-and-criterion?tab=reviews
      """
      if s_adim<0.8:
            psicr = 0.1*(s_adim**(-2/7))
      elif s_adim >= 300:
            psicr = 0.06
      elif ( s_adim>=0.8 ) and ( s_adim<300 ):
            polpsi = _poly(math.log10(s_adim))
            psicr = 10**polpsi
            
      return psicr

def get_psi_cr2(dstar):
      """ 
      http://docs.opentelemac.org/doxydocs/v8p2r0/html/shields_8f_source.html
      """
      if dstar <= 4.0:
            psicr = 0.24/dstar
      elif dstar <= 10.:
            psicr= 0.14*dstar**(-0.64)
      elif dstar <= 20.:
            psicr= 0.04*dstar**(-0.1)
      elif dstar <= 72.:
            psicr= 0.013*dstar**0.29
      else:
            psicr= 0.045
      return psicr

def get_psi_cr3(dstar):
      """ 
      Fluvial Processes, IAHR 2001, pp 6-9
      """
      
      psicr = 0.13*dstar**-0.392*math.exp(-0.015*dstar**2.)+0.045*(1-math.exp(-0.068*dstar))
      return psicr

def get_shields_cr(d,rhom=2650.,rho=RHO_PUREWATER,which=2):
      """
       Example: 
        [critical_shear_velocity,taocr,S] = shieldsmodbonlay(2650,0.2E-3)
       
       critical_shear_velocity = 
         0.012649
       taocr =
         0.16399 
      """

      funcs = [(get_sadim,get_psi_cr),(get_dstar,get_psi_cr2),(get_dstar,get_psi_cr3)]
      # % Getting the sediment-fluid parameter
      s = rhom/rho # [-]
      denom_shields= (s-1)*GRAVITY*d  # [m²/s²] en réalité denom/rho

      xadim_val = funcs[which][0](d,rhom,rho)
      psicr = funcs[which][1](xadim_val)
            
      # Using the critical value of Shields parameter
      # Knowing the maximum bottom shear stress
      tau_cr = rho * denom_shields * psicr  # Pa
      critical_shear_velocity = math.sqrt(denom_shields * psicr) # m/s

      return [critical_shear_velocity,tau_cr,xadim_val,psicr]

def _poly(x):
    return ((0.002235*x**5)-(0.06043*x**4)+(0.20307*x**3)+ \
                   (0.054252*x**2)-(0.636397*x)-1.03167)

def _dpolydx(x):
    return ((0.002235*5*x**4)-(0.06043*4*x**3)+(0.20307*3*x**2)+ \
                   (0.054252*2*x)-(0.636397))

def get_sadim_min():
      return root_scalar(_dpolydx,method='bisect',bracket=[10, 20]).root

def get_tau_from_psiadim(psiadim,d,rhom=2650,rho=RHO_PUREWATER):
      s=rhom/rho
      denom_shields= (s-1)*GRAVITY*d  ## en réalité denom/rho
      return rho * denom_shields * psiadim

def get_d_min(rhom=2650,rho=RHO_PUREWATER):
      return get_d_from_sadim(get_sadim_min(),rhom,rho)

def _d_cr(x,tau_obj,rhom,rho,xadim,yadim):

      s=rhom/rho
      denom_shields= (s-1)*GRAVITY*x  ## en réalité denom/rho
      psi_obj = tau_obj/denom_shields/rho
      psi_cr=yadim(xadim(x,rhom,rho))
      return psi_obj-psi_cr

def _get_d_cr(tau_cr,rhom=2650,rho=RHO_PUREWATER):
      
      dminabs = 1.e-6
      dmaxabs = .5
      d_cr = root_scalar(_d_cr,(tau_cr,rhom,rho,get_sadim,get_psi_cr),'bisect',bracket=[dminabs, dmaxabs])
      
      return d_cr

def get_d_cr(q,h,K,rhom=2650,rho=RHO_PUREWATER,method='brenth',which=2):
      """ 
      Diamètre critique d'emportement par :
            - Shields
            - Izbach
      """
      if q==0.:
            return 0.,0.

      tau_cr = (q/K)**2 / h**(7/3) * rho  * GRAVITY
      dminabs = 1.e-100
      dmaxabs = 20

      funcs = [(get_sadim,get_psi_cr),(get_dstar,get_psi_cr2),(get_dstar,get_psi_cr3)]

      try:
            d_cr = root_scalar(_d_cr,(tau_cr,rhom,rho,funcs[which][0],funcs[which][1]),method,bracket=[dminabs, dmaxabs],rtol = 1e-2)
            return d_cr.root, izbach_d_cr(q,h,rhom,rho)
      except:
            izbach = izbach_d_cr(q,h,rhom,rho)
            return izbach,izbach

def get_settling_vel(d,rhom=2650,rho=RHO_PUREWATER):
      """ 
      Vitesse de chute
      """
      dstar = get_dstar(d,rhom,rho)
      ws = KIN_VISCOSITY/d*(math.sqrt(25+1.2*dstar**2.)-5)**(3./2.)
      return ws

def get_Rouse(d,q,h,K,rhom=2650,rho=RHO_PUREWATER):
      """ 
      Vitesse de chute
      """
      # tau_cr = (q/K)**2 / h**(7/3) * rho  * GRAVITY
      # shear_vel = math.sqrt(tau_cr/rho)
      shear_vel = q/K / h**(7/6)* math.sqrt(GRAVITY)
      ws = get_settling_vel(d,rhom,rho)
      # von Kármán constant
      k = 0.40
      
      return ws/(k*shear_vel)

def _get_Rouse(d,q,h,K,rhom=2650,rho=RHO_PUREWATER,frac=50):
      """ 
      Vitesse de chute
      """
      # tau_cr = (q/K)**2 / h**(7/3) * rho  * GRAVITY
      # shear_vel = math.sqrt(tau_cr/rho)
      shear_vel = q/K / h**(7/6)* math.sqrt(GRAVITY)
      ws = get_settling_vel(d,rhom,rho)
      # von Kármán constant
      k = 0.40
      denom = k*shear_vel
      if denom>0.:
            rouse = ws/(k*shear_vel)
      else:
            rouse = 0.
            
      if frac==50:
            return rouse-2.5
      elif frac==100:
            return rouse-1.2

def get_transport_mode(d,q,h,K,rhom=2650,rho=RHO_PUREWATER):
      
      rouse = get_Rouse(d,q,h,K,rhom,rho)
      if rouse>=2.5:
            return BED_LOAD
      elif rouse>=1.2:
            return SUSPENDED_LOAD_50
      elif rouse>=0.8:
            return SUSPENDED_LOAD_100
      else:
            return WASH_LOAD
      
def get_d_cr_susp(q,h,K,rhom=2650,rho=RHO_PUREWATER,method='brenth',which=50):
      """ 
      Diamètre critique d'emportement par suspension à 50% --> cf Rouse 1.2
      """
      if q==0.:
            return 0.
      
      dminabs = 1.e-100
      dmaxabs = 20
      try:
            d_cr = root_scalar(_get_Rouse,(q,h,K,rhom,rho,which),method,bracket=[dminabs, dmaxabs],rtol = 1e-2)
            return d_cr.root
      except:
            return 0.

def shieldsdia_sadim(s_psicr=None,dstar_psicr=None,rhom=2650,rho=RHO_PUREWATER,figax=None):

      smax = 1000
      rangoS = np.arange(0.1,smax,0.1)
      psicri = np.asarray([get_psi_cr(curx) for curx in rangoS])
      psicri2 = np.asarray([get_psi_cr2(sadim2dstar(curx)) for curx in rangoS])
      psicri3 = np.asarray([get_psi_cr3(sadim2dstar(curx)) for curx in rangoS])

      if figax is None:
            fig, ax = plt.subplots(1,1)
            ax.set_title('Modified Shields diagram')
      else:
            fig, ax = figax
            
      ax.plot(rangoS,psicri,linewidth=4,color=[0,0,.8],label='Madsen and Grant, 1976')        
      ax.plot(rangoS,psicri2,linewidth=4,color=[0.8,0,.8],label='Telemac-Mascaret, 2022')        
      ax.plot(rangoS,psicri3,linewidth=4,color=[0.5,0,.8],label='Yalin and Ferreira da Silva, 2001')        
      
      ylabel=r'$ {\theta}_{cr} =  \frac{u^*}{g \left( s-1 \right) d}$'
      xlabel = r'$ {S^*} = d^{3/2} \frac{ {\left( \left( s-1 \right) g \right)}^{1/2}}{4 \nu} $'

      ax.set_ylabel('Critical shields '+ylabel+'  (dimensionless)')
      ax.set_xlabel('Sediment - fluid parameter  '+xlabel+ ' (dimensionless)')

      if s_psicr is not None:
            S = s_psicr[0]
            psicr = s_psicr[1]
            x = [S,0.1,S]
            y = [psicr,psicr,.01]
            ax.scatter(x,y,50,c='red')

            ax.plot([0.8, 0.8],[0.01,1],color=[0.75,0.75,0.75],linestyle=':')
            ax.text(S+.005,psicr+0.005,'$S^*$')

      if dstar_psicr is not None:
            S = dstar2sadim(dstar_psicr[0])
            psicr = dstar_psicr[1]
            x = [S,0.1,S]
            y = [psicr,psicr,.01]
            ax.scatter(x,y,50,c='red')

            ax.plot([0.8, 0.8],[0.01,1],color=[0.75,0.75,0.75],linestyle=':')
            ax.text(S+.005,psicr+0.005,'$S^*$')

      ax.set_xlim([.1,smax])
      ax.set_ylim([0.01,1])
      ax.set_xscale('log')
      ax.set_yscale('log')
      ax.grid(True,'both',axis='both')
      ax.legend()

      # plt.show()

      return fig,ax

def shieldsdia_dstar(s_psicr=None,dstar_psicr=None,rhom=2650,rho=RHO_PUREWATER,figax=None):

      smax = 1000
      d_stars = np.arange(0.1,smax,0.1)
      diams = np.asarray([get_d_from_dstar(curx) for curx in d_stars])
      rangoS = np.asarray([get_sadim(curx) for curx in diams])      
      
      psicri = np.asarray([get_psi_cr(curx) for curx in rangoS])
      
      psicri2 = np.asarray([get_psi_cr2(curx) for curx in d_stars])
      psicri3 = np.asarray([get_psi_cr3(curx) for curx in d_stars])

      if figax is None:
            fig, ax = plt.subplots(1,1)
            ax.set_title('Modified Shields diagram')
      else:
            fig, ax = figax

      ax.plot(d_stars,psicri,linewidth=4,color=[0,0,.8],label='Madsen and Grant, 1976')        
      ax.plot(d_stars,psicri2,linewidth=4,color=[0.8,0,.8],label='Telemac-Mascaret, 2022')        
      ax.plot(d_stars,psicri3,linewidth=4,color=[0.5,0,.8],label='Yalin and Ferreira da Silva, 2001')        
                  
      ylabel=r'$ {\theta}_{cr} =  \frac{u^*}{g \left( s-1 \right) d}$'
      xlabel = r'$ {D^*} = d \left( \frac{\rho_s g}{\rho \nu^2} \right) ^{1/3} $'

      ax.set_ylabel('Critical shields '+ylabel+'  (dimensionless)')
      ax.set_xlabel('Sediment - fluid parameter  '+xlabel+ ' (dimensionless)')

      if s_psicr is not None:
            S = s_psicr[0]
            psicr = s_psicr[1]
            S = sadim2dstar(S)
            x = [S,0.1,S]
            y = [psicr,psicr,.01]
            ax.scatter(x,y,50,c='red')
            ax.plot([0.8, 0.8],[0.01,1],color=[0.75,0.75,0.75],linestyle=':')
            ax.text(S+.005,psicr+0.005,'$S^*$')

      if dstar_psicr is not None:
            S = dstar_psicr[0]
            psicr = dstar_psicr[1]
            x = [S,0.1,S]
            y = [psicr,psicr,.01]
            ax.scatter(x,y,50,c='red')
            ax.plot([0.8, 0.8],[0.01,1],color=[0.75,0.75,0.75],linestyle=':')
            ax.text(S+.005,psicr+0.005,'$S^*$')

      ax.set_xlim([.1,smax])
      ax.set_ylim([0.01,1])
      ax.set_xscale('log')
      ax.set_yscale('log')
      ax.grid(True,'both',axis='both')
      ax.legend()

      # plt.show()

      return fig,ax

def shieldsdia_dim(figax=None):
      smax=1e6
      rangoS = np.concatenate([np.arange(0.1,300,0.1),np.arange(300.,smax,5.)])
      psicri = np.asarray([get_psi_cr(curx) for curx in rangoS])
      psicri2 = np.asarray([get_psi_cr2(sadim2dstar(curx)) for curx in rangoS])
      psicri3 = np.asarray([get_psi_cr3(sadim2dstar(curx)) for curx in rangoS])

      if figax is None:
            fig, ax = plt.subplots(1,1)
            ax.set_title('Modified Shields diagram')
      else:
            fig, ax = figax

      d = get_d_from_sadim(rangoS)
      tau = [get_tau_from_psiadim(psi,curd) for psi,curd in zip(psicri,d)]
      tau2 = [get_tau_from_psiadim(psi,curd) for psi,curd in zip(psicri2,d)]
      tau3 = [get_tau_from_psiadim(psi,curd) for psi,curd in zip(psicri3,d)]
      
      ax.plot(d,tau,linewidth=4,color=[0,0,.8],label='Madsen and Grant, 1976') 
      ax.plot(d,tau2,linewidth=4,color=[0.8,0,.8],label='Telemac-Mascaret, 2022') 
      ax.plot(d,tau3,linewidth=4,color=[0.5,0,.8],label='Yalin and Ferreira da Silva, 2001') 

      ax.set_ylabel('Critical shear stress [Pa]')
      ax.set_xlabel('Sediment diameter [m]')

      ax.set_xlim([np.min(d),np.max(d)])
      ax.set_ylim([np.min(tau),np.max(tau)])
      ax.set_xscale('log')
      ax.set_yscale('log')
      ax.grid(True,'both',axis='both')
      ax.legend()

      # plt.show()

      return fig,ax

def get_Shields_2D_pw(s,d,q_abs,h,k_rough):
      """
      """
      # calcul de terme de pente de frottement
      k_sur_h = k_rough/(4.0*h)
      Reynolds = 4.0 * q_abs /KIN_VISCOSITY # u*4h/nu == 4q/nu
      j = f_barr_bathurst(k_sur_h,Reynolds)/(4.0*h) * (q_abs/h)**2.0/2.0/GRAVITY

      shields = j*h / (d*(s-1))
      
      # shields = f/4 * u**2 /2 /g /(d * (rho_s-rho_w) / rho_w)
      # shields = tau / (rho_s - rho_w) /g /d
      # tau = f/8 * rho_w * u**2 

      return shields

def get_effective_d_2D(s,theta_cr,q_abs,h,k_rough):
      """
      Calcul du diamètre de grain emporté par une approche basée sur une tension efficace
      
      Portage du code de calcul de WOLF2D
      @authors : Pierre Archambeau (2022)
      """

      #if which_friction_law#=rough_Barr_Bathurst:
       ##les autres lois de frottement ne sont pas implémentées mais aucune difficulté particulière
      ##ne devraient empêcher cela

      my_exp = [0.0, 0.10, 0.20, 0.30, 0.40, 0.420, 0.440, 0.460, 0.480, 
                0.50, 0.52, 0.54, 0.56, 0.58, 
                0.6, 0.62, 0.64, 0.66, 0.68, 
                0.7, 0.71, 0.72, 0.73, 0.74, 0.75]

      ##calcul du coefficient de frottement (point de vue de l'écoulement)    
      u_abs = q_abs/h
      Reynolds = q_abs * 4 / KIN_VISCOSITY
      k_sur_h = k_rough/(4*h)
      f_flow = f_barr_bathurst(k_sur_h,Reynolds)

      #valeur initiale (pas de tension efficace)
      exp = my_exp[0]
      d = f_flow**(1-exp)*u_abs**2/(8*(s-1)*GRAVITY*theta_cr)
      #boucle pour approcher les exposants requis
      for cur_exponent in range(1,25):
            exp = my_exp[cur_exponent]
            #partie constante du rapport d = lamda'^(3/4)*lambda^(1/4)*U^2/8/(s-1)/g/theta_cr
            cst = f_flow**(1-exp)*u_abs**2/(8*(s-1)*GRAVITY*theta_cr)
            #boucle pour converger sur un diamètre qui respecte l'égalité
            k_sur_h = d/(4*h)
            f_grain = f_barr_bathurst(k_sur_h,Reynolds)
            f_obj = d-f_grain**exp*cst
            nb_ite = 0
            while abs(f_obj) > 1.e-6 and nb_ite < 20:
                  #calcul de la dérivée numérique
                  k_sur_h = (d+1.e-6)/(4*h)
                  f_pert1 = f_barr_bathurst(k_sur_h,Reynolds)
                  k_sur_h = (d-1.e-6)/(4*h)
                  f_pert2 = f_barr_bathurst(k_sur_h,Reynolds)
                  dfdd = 1-cst*exp*f_grain**(exp-1)*(f_pert1-f_pert2)/2.e-6
                  frac = f_obj/dfdd
                  #modifiation de d
                  if abs(frac) > 0.5*d:
                        if frac>0:
                              frac = 0.5*d
                        else:
                              frac = -0.5*d
                  d = d - frac
                  #calcul de la nouvelle donction objectif
                  k_sur_h = d/(4*h)
                  f_grain = f_barr_bathurst(k_sur_h,Reynolds)
                  f_obj = d-f_grain**exp*cst
                  nb_ite = nb_ite + 1
                  
      return d

def izbach_d_cr(q,h,rhom=2650,rho=RHO_PUREWATER,method='ridder'):
      """
      https://en.wikipedia.org/wiki/Izbash_formula
      
      u_c/ ((s-1) * g * d)**.5 = 1.7

      avec  : 
            (s-1) = (rho_m - rho) / rho
            u_c = 85% u_moyen)

      --> d = u_c**2 / (s * g) / 1.7**2

      --> d = (0.85 * q/h)**2 / (s * g) / 1.7**2
      """
      s = rhom/rho
      # return (0.85 * q/h)**2. / ((s-1.) * GRAVITY) / 1.7**2.
      # return 0.7 * (0.85*q/h)**2. / (2 * GRAVITY) / (s-1.)
      # return (q/h)**2. / (2 * GRAVITY) / (s-1.) / .86**2
      return (q/h)**2. / (2 * GRAVITY) / (s-1.) / 1.2**2
      
