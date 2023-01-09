import numpy as np

def ERRORS(N_data,fsup,error,c,R,Threshold_upp,V,e,eps0,me,Bande,CC):

    def H(R,Threshold_Atmneu):
        if R<=Threshold_Atmneu:
            H = 10E3 # m
        else:
            H = 25E3 # m   P.Whiters et al.(2010)
        return H

    error_ref = np.full(N_data, np.nan)
    error_elec = np.full(N_data, np.nan)
    error_neut = np.full(N_data, np.nan)

    if Bande == 'X':
        f = fsup*880./749.
    else:
        f = fsup*240./749.

    kappa = CC

    ######## ERREURS ###########
    for i in range(N_data):

            error_ref[i]  = c*error[i]/(V*f)*np.sqrt(H(R[i],Threshold_upp)/(2*np.pi*R[i]))
            error_elec[i] = 4*np.pi*error[i]*f*c*me*eps0/(V*e**2)*np.sqrt(2*np.pi*25E3/R[i])
            error_neut[i] = c*error[i]/(V*f*kappa)*np.sqrt(10E3/(2*np.pi*R[i]))
    print('\t ERRORS DONE\n')
    return error_ref,error_elec, error_neut
