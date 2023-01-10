import numpy as np
import calculos as cl
import optimizadores as op
from Funciones_objetivo import fWILSON,fNRTL,UNIQUAC

class sistema:

    def completardatos(self):
        self.x, self.gama1, self.gama2, self.Gibbs = cl.experimental(self.T, self.x, self.y, self.CoefA, self.CoefB, self.P)

    def __init__(self, Temp, frac_molar_x, frac_molar_y, CoefA, CoefB, V1,V2,P, *args,**kwargs):
        self.T = Temp
        self.x = frac_molar_x
        self.y = frac_molar_y
        self.CoefA = CoefA
        self.CoefB = CoefB
        self.V1 = V1
        self.V2 = V2
        self.P = P
        self.q = kwargs.get('q',None)
        self.qprima = kwargs.get('qprima', None)
        self.r = kwargs.get('r', None)
        self.nombre = kwargs.get('Nombre', None)
        self.completardatos()

    def resolver(self, limites_inferiores, limites_superiores, dimension, poblacion, iteraciones,**kwargs):
        self.modelo = kwargs.get('modelo', None)
        self.size = kwargs.get('size', None)
        if self.modelo == 1:
            self.error_Wilson, mejor_ruta, self.Parametros_WILSON , self.tiempo_WILSON= op.pso(np.array(limites_inferiores), np.array(limites_superiores), dimension, poblacion, iteraciones,
                                                           fWILSON, self)
            datos = cl.BublxP_Wilson(self.size, self, self.Parametros_WILSON)
            self.data_WILSON = cl.imprimir(datos)
            self.resultados = cl.res([self.Parametros_WILSON, self.tiempo_WILSON, self.error_Wilson], 1, self)
            cl.Graficador(datos, self, self.modelo)

        elif self.modelo == 2:
            self.error_NRTL, mejor_ruta, self.Parametros_NRTL, self.tiempo_NRTL = op.pso(cl.agregar(0,np.array(limites_inferiores)),
                                                                                        cl.agregar(1,np.array(limites_superiores)),
                                                                                        dimension+1, poblacion,
                                                                                        iteraciones,
                                                                                        fNRTL, self)
            datos = cl.BublxP_NRTL(self.size, self, self.Parametros_NRTL)
            cl.Graficador(datos, self, self.modelo)
            self.data_NRTL = cl.imprimir(datos)
            self.resultados = cl.res([self.Parametros_NRTL,self.tiempo_NRTL, self.error_NRTL],2,self )

        elif self.modelo == 3:
            self.error_UNIQUAC, mejor_ruta, self.Parametros_UNIQUAC, self.tiempo_UNIQUAC = op.pso(np.array(limites_inferiores),
                                                                                    np.array(limites_superiores),
                                                                                    dimension, poblacion,
                                                                                    iteraciones,
                                                                                    UNIQUAC, self)
            datos = cl.Bublx_UNIQUAC(self.size, self, self.Parametros_UNIQUAC)
            cl.Graficador(datos, self, self.modelo)
            self.data_UNIQUAC = cl.imprimir(datos)
            self.resultados = cl.res([self.Parametros_UNIQUAC, self.tiempo_UNIQUAC, self.error_UNIQUAC], 3, self)

        elif self.modelo == None or self.modelo == 4:
            self.error_Wilson, mejor_ruta, self.Parametros_WILSON, self.tiempo_WILSON = op.pso(np.array(limites_inferiores),
                                                                                        np.array(limites_superiores),
                                                                                        dimension, poblacion,
                                                                                        iteraciones,
                                                                                        fWILSON, self)
            datosW = cl.BublxP_Wilson(self.size, self, self.Parametros_WILSON)
            self.error_NRTL, mejor_ruta, self.Parametros_NRTL, self.tiempo_NRTL = op.pso(cl.agregar(0,np.array(limites_inferiores)),
                                                                                        cl.agregar(1,np.array(limites_superiores)),
                                                                                        dimension+1, poblacion,
                                                                                        iteraciones,
                                                                                        fNRTL, self)
            datosN = cl.BublxP_NRTL(self.size, self, self.Parametros_NRTL)

            self.error_UNIQUAC, mejor_ruta, self.Parametros_UNIQUAC, self.tiempo_UNIQUAC = op.pso(np.array(limites_inferiores),
                                                                                          np.array(limites_superiores),
                                                                                          dimension, poblacion,
                                                                                          iteraciones,
                                                                                          UNIQUAC, self)

            datosQ = cl.Bublx_UNIQUAC(self.size, self, self.Parametros_UNIQUAC)

            datos = [datosW, datosN, datosQ]
            cl.Graficadores(datos, self)
            self.data_WILSON = cl.imprimir(datosW)
            self.data_NRTL = cl.imprimir(datosN)
            self.data_UNIQUAC = cl.imprimir(datosQ)

            self.resultados  = cl.res([[self.Parametros_WILSON, self.tiempo_WILSON, self.error_Wilson], [self.Parametros_NRTL,self.tiempo_NRTL, self.error_NRTL], [self.Parametros_UNIQUAC, self.tiempo_UNIQUAC, self.error_UNIQUAC]], 4, self, val= False)


    #def setAtributos(self, Temp, frac_molar_x, frac_molar_y, CoefA, CoefB, V1,V2,P):


#Data set
'''
t = np.array([100, 98.59, 95.09, 91.05, 88.96, 88.26, 87.96, 87.79, 87.66, 87.83, 89.34, 92.3, 97.18])
x = np.array([0, 0.003, 0.0123, 0.0322, 0.0697, 0.139, 0.231, 0.311, 0.412, 0.545, 0.73, 0.878, 1])
y = np.array([0, 0.0544, 0.179, 0.304, 0.365, 0.384, 0.397, 0.406, 0.428, 0.465, 0.567, 0.721, 1])
CoefA = np.array([17.5439, 3166.38, 193])
CoefB = np.array([18.3036, 3816.44, 227.02])
V1 = 218.5
V2 = 56
P = 101.3
q = np.array([2.5129, 1.4])
r = np.array([2.7799, 0.92])
q_prima = np.array([0.89, 1])

Propanol_Agua = sistema(t, x, y, CoefA, CoefB, V1, V2, P, q = q, qprima = q_prima, r = r, Nombre= 'Propanol_Agua')
Propanol_Agua.resolver([-1000.0, -1000.0], [2500.0, 2500.0], 2, 30, 150, size = 50, modelo= 4)
print(Propanol_Agua.resultados)
'''

