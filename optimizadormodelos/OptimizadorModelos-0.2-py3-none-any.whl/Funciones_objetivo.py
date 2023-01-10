import math
import calculos as pl

def fobj1(param, sistema):

    # ---------------Calculo de parametros de la ecuacion de wilson   -------------------------------------------------


    l1 = param[0]
    l2 = param[1]
    x = sistema.x
    gama1exp = sistema.gama1
    gama2exp = sistema.gama2
    gibbsexp = sistema.Gibbs
    V2 = sistema.V2
    V1 = sistema.V1
    a12 = (V2 / V1) * math.exp(-l1 / (1.987 * 298.15))
    a21 = (V1 / V2) * math.exp(-l2 / (1.987 * 298.15))
    # ------------------------------------------------------------------------------------------------------------------

    # --------------- Getting experimental data through the function "exp" in file plot   ------------------------------
    #x, gama1exp, gama2exp, gibbsexp = pl.experimental(t, x1, y1, Coef, Coef2, P)
    n = len(gibbsexp)
    x2 = pl.c2(x)

    #print(x, gama1exp, gama2exp, gibbsexp)
    # ------------------------------------------------------------------------------------------------------------------

    suma = 0

    for i in range(0, n):
        # Funcion objetivo (gamaexp1 -gamacalc1)^2 + (gamaexp2 -gamacalc2)^2
        r = (gama1exp[i] - math.exp(-math.log(x[i] + a12 * x2[i]) + x2[i] * (a12 / (x[i] + a12 * x2[i]) - a21/(x2[i] + a21 * x[i]))))**2 +\
            (gama2exp[i] - math.exp(-math.log(x2[i] + a21 * x[i]) + x[i] * (-a12 / (x[i] + a12 * x2[i]) + a21/(x2[i] + a21 * x[i]))))**2

        suma += r

    return suma


# ----------------------------------------------------------------------------------------------------------------------
def fobj2(param, sistema):
    # ---------------DATOS NECESARIOS QUE SE INTRODUZCAN POR EL USUARIO O CON ALGUNA BASE DE DATOS  --------------------
    # ------------------------------------------------------------------------------------------------------------------
    x = sistema.x
    gama1exp = sistema.gama1
    gama2exp = sistema.gama2
    gibbsexp = sistema.Gibbs
    V2 = sistema.V2
    V1 = sistema.V1
    t = sistema.T
    y1 = sistema.y
    Coef = sistema.CoefA
    P = sistema.P
    # ---------------Calculo de paramestros de la ecuacion de wilson   -------------------------------------------------
    l1 = param[0]
    l2 = param[1]
    a12 = (V2 / V1) * math.exp(-l1 / (1.987 * 298.15))
    a21 = (V1 / V2) * math.exp(-l2 / (1.987 * 298.15))
    # ------------------------------------------------------------------------------------------------------------------

    # --------------- Getting experimental data through the function "exp" in file plot   ------------------------------
    n = len(gibbsexp)
    x2 = pl.c2(x)
    # ------------------------------------------------------------------------------------------------------------------

    t1= pl.cortar(t)
    y_1 = pl.cortar(y1)

    psat1= pl.psatalternativa(Coef, t1)


    suma = 0

    for i in range(0, n):

        gama1 = math.exp(-math.log(x[i]+a12*x2[i])+x2[i]*(a12/(x[i]+a12*x2[i]) - a21/(x2[i]+a21*x[i])))

        r = (y_1[i] - gama1*x[i]*psat1[i]/P)**2

        suma += r

    return suma

# ----------------------------------------------------------------------------------------------------------------------


def fWILSON(param, sistema):

    l1 = param[0]
    l2 = param[1]
    x = sistema.x
    gama1exp = sistema.gama1
    gama2exp = sistema.gama2
    gibbsexp = sistema.Gibbs
    V2 = sistema.V2
    V1 = sistema.V1

    #x = np.array([0.1008, 0.1989, 0.301, 0.4012, 0.4993, 0.5998, 0.6989, 0.8001, 0.8976])
    #y = np.array([0.120355947163574, 0.36281859108538, 0.613547124059236, -0.061070855531744, -0.0496705413090824, 0.888657442475681, 0.669078589972542, 0.457330457630938, 0.243741235318766])



    n = len(x)

    if n != len(gibbsexp):
        print("el numero de datos en x y y es diferente ")

    suma = 0

    a12 = (V2 / V1) * math.exp(-l1 / (1.987 * 298.15))
    a21 = (V1 / V2) * math.exp(-l2 / (1.987 * 298.15))


    for i in range(0, n):
        # Funcion objetivo (Ge/RTexp - Ge/RTcalc)^2
        r = (gibbsexp[i] - (- x[i] * math.log(x[i] + (1 - x[i]) * a12) - (1-x[i]) * math.log(1 - x[i] + x[i] * a21)))**2

        suma += r

    return suma

def UNIQUAC(param, sistema):
    param_qprima = sistema.qprima
    param_q = sistema.q
    param_r = sistema.r
    x = sistema.x
    gama1exp = sistema.gama1
    gama2exp = sistema.gama2
    gibbsexp = sistema.Gibbs
    V2 = sistema.V2
    V1 = sistema.V1

    u12 = param[0]
    u21 = param[1]


    Ge_combinatoria= pl.valoresUNIQUAC( param_r , param_q, param_qprima, x)[0]
    thetaprimas = pl.valoresUNIQUAC( param_r , param_q, param_qprima, x)[1]

    #x = np.array([0.1008, 0.1989, 0.301, 0.4012, 0.4993, 0.5998, 0.6989, 0.8001, 0.8976])
    #y = np.array([0.120355947163574, 0.36281859108538, 0.613547124059236, -0.061070855531744, -0.0496705413090824, 0.888657442475681, 0.669078589972542, 0.457330457630938, 0.243741235318766])



    n = len(x)

    if n != len(gibbsexp):
        print("el numero de datos en x y y es diferente ")

    suma = 0
    x2 = pl.c2(x)
    t12 = math.exp(-u12 / (1.987 * 298.15))
    t21 = math.exp(-u21 / (1.987 * 298.15))


    for i in range(0, n):
        # Funcion objetivo (Ge/RTexp - Ge/RTcalc)^2
        r = (gibbsexp[i] - (Ge_combinatoria[i]+(-x[i]*param_qprima[0]*math.log(thetaprimas[0][i] + thetaprimas[1][i]*t21) - x2[i] * param_qprima[1]*math.log(thetaprimas[1][i] + thetaprimas[0][i]*t12))))**2

        suma += r

    return suma


#----------------------------------------------------------------------------------------------------------------------
def fNRTL(param, sistema):

    a = param[0]
    b12 = param[1]
    b21 = param[2]
    x = sistema.x
    gama1exp = sistema.gama1
    gama2exp = sistema.gama2
    gibbsexp = sistema.Gibbs
    V2 = sistema.V2
    V1 = sistema.V1



    #x = np.array([0.1008, 0.1989, 0.301, 0.4012, 0.4993, 0.5998, 0.6989, 0.8001, 0.8976])
    #y = np.array([0.120355947163574, 0.36281859108538, 0.613547124059236, -0.061070855531744, -0.0496705413090824, 0.888657442475681, 0.669078589972542, 0.457330457630938, 0.243741235318766])

    x2 = pl.c2(x)

    n = len(x)

    if n != len(gibbsexp):
        print("el numero de datos en x y y es diferente ")

    suma = 0

    #a12 = (V2 / V1) * math.exp(-l1 / (1.987 * 298.15))
    #a21 = (V1 / V2) * math.exp(-l2 / (1.987 * 298.15))

    t12 = b12 / (1.987 * 298.15)
    t21 = b21 / (1.987 * 298.15)
    G12 = math.exp(- a * t12)
    G21 = math.exp(- a * t21)



    for i in range(0, n):
        # Funcion objetivo (Ge/RTexp - Ge/RTcalc)^2
        r = (gibbsexp[i] - (x[i]*x2[i]*(t21*G21/(x[i]+G21*x2[i]) + t12*G12/(x2[i]+G12*x[i]))))**2

        suma += r

    return suma