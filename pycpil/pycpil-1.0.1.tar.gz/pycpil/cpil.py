import numpy as np

print('-'*70)
print('pkg imported sucessfully.')

initital_intro = '''
                -----------------------------------------------------------------
                Predict heat capacity of IL or INF by PyCpil
                
                import pycpil as cp     # load pkg
                cp.calculate.help()     # quick help
                cp.calculate.info()     # brief info on pkg

                more details: https://github.com/nirmalparmarphd/PyCpil
                -----------------------------------------------------------------
'''
print(initital_intro)

pkg_help = '''
                -----------------------------------------------------------------
                Predict heat capacity of IL or INF by PyCpil
                
                IL - Ionic liquids
                INF - Nanofluid or IoNanoFluid

                import pycpil as cp         # load pkg
                cp.calculate.help()         # quick help
                cp.calculate.info()         # brief info on pkg
                cp.calculate.list()         # list ILs and INFs

                # to calculate heat capacity of IL
                # temperature range 20 to 70 [C]
                cp.calculate.il('IL-Name', Temperature[C])

                # to calculate heat capacity of INF
                cp.calculate.inf('INF-Name', Concentration[wt.%], Temperature [C])

                more details: https://github.com/nirmalparmarphd/PyCpil
                -----------------------------------------------------------------

'''

pkg_info = '''
                -----------------------------------------------------------------
                PyCpil

                PyCpil pkg calculates isobaric heat capacity of ionic liquids (IL)
                and ionanofluids (INF).
                
                Experimental isobaric heat capacity data were assessed by a novel 
                non-statistical data analysis method named as mathematical gnosti
                -cs (MG). MG marginal analysis was used to evaluate most probable
                values from the measured data set. A robust linear regression alo
                -ng a gnostic influence function was also used to find the best 
                fit to correlate measured data.
                
                PyCpil pkg is a part of the reserch work and can be further used
                with a proper citation.

                [1] doi:10.1021/acs.iecr.0c06008
                [2] doi:10.1039/D2CP02110B

                more details: https://github.com/nirmalparmarphd/PyCpil
                -----------------------------------------------------------------

'''

pkg_list = '''
                -----------------------------------------------------------------
                List of ionic liquids and ionanofluids or nanofluids

                Ionic liquids           Nanoparticle    Concentration

                [C2mim][Tf2N]           MWCNT           0.1, 0.25, 0.5, 0.75, 1
                [C4mim][Tf2N]           MWCNT           0.5, 1, 3
                [C6mim][Tf2N]           MWCNT           1
                [C8mim][Tf2N]           MWCNT           1
                [C10mim][Tf2N]          MWCNT           1
                [C12mim][Tf2N]          MWCNT           1
                
                # temperature range 20 to 70 [C] 

                more details: https://github.com/nirmalparmarphd/PyCpil
                -----------------------------------------------------------------

'''

T_low = 20
T_up = 70

class calculate():
    def __init__(self):
        print('-'*70)
        print('''
                PyCpil loaded, You are Awesome!
                ''')
        print(initital_intro)

    def info():
        print(pkg_info)

    def help():
        print(pkg_help)

    def list():
        print(pkg_list)

    def il(il_name, x):
        print('-'*70)
        # -------------------------------- PURE IL ---------------------------------
        if il_name == '[c2mim][tf2n]' and x in range(T_low, T_up):
            cp = 7.52919e-05+0.0079646*x**1-1.456e-05*x**2+8.14479e-09*x**3
            print ('Isobaric heat capacity of ionic liquid', il_name, 'is :', np.round(cp,4), '[J/gK]' )
        
        elif il_name == '[c4mim][tf2n]' and x in range(T_low, T_up):
            cp = 0.105648+11.1784*x**1-0.0553523*x**2+8.12781e-05*x**3
            print ('Isobaric heat capacity of ionic liquid', il_name, 'is :', np.round(cp,4), '[J/gK]' )
        
        elif il_name == '[c6mim][tf2n]' and x in range(T_low, T_up):
            cp = 1.3998+0.000884568*x**1+1.43574e-05*x**2-1.10043e-07*x**3
            print ('Isobaric heat capacity of ionic liquid', il_name, 'is :', np.round(cp,4), '[J/gK]' )
        
        elif il_name == '[c8mim][tf2n]' and x in range(T_low, T_up):
            cp = 1.44558+0.00126882*x**1+7.70355e-06*x**2-5.99227e-08*x**3
            print ('Isobaric heat capacity of ionic liquid', il_name, 'is :', np.round(cp,4), '[J/gK]' )
        
        elif il_name == '[c10mim][tf2n]' and x in range(T_low, T_up):
            cp = 1.4695+0.0014262*x**1+1.73213e-06*x**2-1.33802e-08*x**3
            print ('Isobaric heat capacity of ionic liquid', il_name, 'is :', np.round(cp,4), '[J/gK]' )
        
        elif il_name == '[c12mim][tf2n]' and x in range(T_low, T_up):
            cp = 1.51727+0.00130435*x**1+7.4496e-06*x**2-5.136e-08*x**3
            print ('Isobaric heat capacity of ionic liquid', il_name, 'is :', np.round(cp,4), '[J/gK]' )
        
        else:
            print('Please, enter the correct ionic liquid name or/and temperature range')
            print(pkg_help)
        
    def inf(inf_name, wt, x): 
        print('-'*70)  
        # -------------------------------- INF [c2mim][tf2n} + mwcnt ---------------------------------
        if inf_name == '[c2mim][tf2n]' and x in range(T_low, T_up) and wt == 0.1:
            cp = 1.25636+0.000881573*x**1+9.02222e-06*x**2-7.76111e-08*x**3
            print ('Isobaric heat capacity of IoNanoFluid', inf_name, '+', wt, 'wt.(%) MWCNT is :', np.round(cp,4), '[J/gK]' )
        
        elif inf_name == '[c2mim][tf2n]' and x in range(T_low, T_up) and wt == 0.25:
            cp = 1.24868+0.00111527*x**1+1.06882e-05*x**2-1.44005e-07*x**3
            print ('Isobaric heat capacity of IoNanoFluid', inf_name, '+', wt, 'wt.(%) MWCNT is :', np.round(cp,4), '[J/gK]' )
        
        elif inf_name == '[c2mim][tf2n]' and x in range(T_low, T_up) and wt == 0.5:
            cp = 1.26586+0.000820295*x**1+1.08596e-05*x**2-9.7208e-08*x**3
            print ('Isobaric heat capacity of IoNanoFluid', inf_name, '+', wt, 'wt.(%) MWCNT is :', np.round(cp,4), '[J/gK]' )
        
        elif inf_name == '[c2mim][tf2n]' and x in range(T_low, T_up) and wt == 0.75:
            cp = 1.25983+0.000836631*x**1+1.59238e-05*x**2-1.73766e-07*x**39
            print ('Isobaric heat capacity of IoNanoFluid', inf_name, '+', wt, 'wt.(%) MWCNT is :', np.round(cp,4), '[J/gK]' )
        
        elif inf_name == '[c2mim][tf2n]' and x in range(T_low, T_up) and wt == 1:
            cp = 1.25103+0.000460472*x**1+1.5437e-05*x**2-1.08904e-07*x**3
            print ('Isobaric heat capacity of IoNanoFluid', inf_name, '+', wt, 'wt.(%) MWCNT is :', np.round(cp,4), '[J/gK]' )
        
        # -------------------------------- INF [c4mim][tf2n} + mwcnt ---------------------------------
        elif inf_name == '[c4mim][tf2n]' and x in range(T_low, T_up) and wt == 0.5:
            cp = 1.26959+0.000718138*x**1+1.86851e-05*x**2-1.90169e-07*x**3
            print ('Isobaric heat capacity of IoNanoFluid', inf_name, '+', wt, 'wt.(%) MWCNT is :', np.round(cp,4), '[J/gK]' )
        
        elif inf_name == '[c4mim][tf2n]' and x in range(T_low, T_up) and wt == 1:
            cp = 1.3205+0.00112918*x**1+6.94142e-06*x**2-6.09204e-08*x**3
            print ('Isobaric heat capacity of IoNanoFluid', inf_name, '+', wt, 'wt.(%) MWCNT is :', np.round(cp,4), '[J/gK]' )
        
        elif inf_name == '[c4mim][tf2n]' and x in range(T_low, T_up) and wt == 3:
            cp = 1.31813+0.00113388*x**1+7.45173e-06*x**2-5.81182e-08*x**3
            print ('Isobaric heat capacity of IoNanoFluid', inf_name, '+', wt, 'wt.(%) MWCNT is :', np.round(cp,4), '[J/gK]' )
        
        # -------------------------------- INF [c6mim][tf2n} + mwcnt ---------------------------------
        elif inf_name == '[c6mim][tf2n]' and x in range(T_low, T_up) and wt == 1:
            cp = 1.39219+0.000920109*x**1+1.49108e-05*x**2-1.20458e-07*x**3
            print ('Isobaric heat capacity of IoNanoFluid', inf_name, '+', wt, 'wt.(%) MWCNT is :', np.round(cp,4), '[J/gK]' )
        
        # -------------------------------- INF [c8mim][tf2n} + mwcnt ---------------------------------
        elif inf_name == '[c8mim][tf2n]' and x in range(T_low, T_up) and wt == 1:
            cp = 1.43265+0.00136038*x**1+6.08842e-06*x**2-5.11474e-08*x**3
            print ('Isobaric heat capacity of IoNanoFluid', inf_name, '+', wt, 'wt.(%) MWCNT is :', np.round(cp,4), '[J/gK]' )
        
        # -------------------------------- INF [c10mim][tf2n} + mwcnt ---------------------------------
        elif inf_name == '[c10mim][tf2n]' and x in range(T_low, T_up) and wt == 1:
            cp = 1.46758+0.00145524*x**1+3.94941e-06*x**2-4.46511e-08*x**3
            print ('Isobaric heat capacity of IoNanoFluid', inf_name, '+', wt, 'wt.(%) MWCNT is :', np.round(cp,4), '[J/gK]' )
        
        # -------------------------------- INF [c12mim][tf2n} + mwcnt ---------------------------------
        elif inf_name == '[c12mim][tf2n]' and x in range(T_low, T_up) and wt == 1:
            cp = 1.53403+0.00106384*x**1+1.17053e-05*x**2-7.68105e-08*x**3
            print ('Isobaric heat capacity of IoNanoFluid', inf_name, '+', wt, 'wt.(%) MWCNT is :', np.round(cp,4), '[J/gK]' )
        
        else:
            print('Please, enter the correct ionic liquid name or/and temperature range or/and nano-particle concentration')
            print(pkg_help)
        
