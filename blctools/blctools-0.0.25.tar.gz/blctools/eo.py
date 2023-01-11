
import numpy as __np

def rosa_de_los_vientos(bins=16):
    
    if isinstance(bins,(int,float)):
    
        if bins == 32:
            return duplicar_rosa(rosa_de_los_vientos(bins=16))
        elif bins == 16:
            return duplicar_rosa(rosa_de_los_vientos(bins=8))
        elif bins == 8:
            return duplicar_rosa(rosa_de_los_vientos(bins=4))
        elif bins == 4:
            return ["N","E","S","W"]
        else:
            raise ValueError('El parámetro bins sólo puede ser 4, 8, 16 ó 32')
    elif isinstance(bins,str):
        try:
            return rosa_de_los_vientos(int(bins))
        except:
            raise Exception(f'Imposible convertir el valor {bins} a int')
    else:
        raise TypeError('El DataType del parámetro "bins" debe ser int, float o str')
    
def __get_indices_rosa(i,k):
    '''Esta función devuelve un tuple, 
    indicando cómo combinar los valores de la rosa'''
    
    # i = índice actual
    # k = cantidad de elementos en la rosa actual
    max_i = k -1
    is_even = bool(i % 2)
    if i < max_i:
        if is_even:
            return (i+1,i)
        else:
            return (i,i+1)
    else:
            return (0,i)
        
def duplicar_rosa(rosa):
    'Convierte de rosa de 4 direcciones, a 8, a 16, a 32'
    new_rosa = []
    k = len(rosa)
    
    if k == 4 or k == 8:
        for i,v in enumerate(rosa):
            i1, i2  = __get_indices_rosa(i,k)
            new_dir = rosa[i1] + rosa[i2]
            
            new_rosa.append(v)
            new_rosa.append(new_dir)
    elif k == 16:
        for i,v in enumerate(rosa):
            
            if (i%4 == 0):
                new_dir = rosa[i+1][0] + "." + rosa[i+1][1:]
                
            elif (i%4 == 1):
                new_dir = v[1:] + "." + v[0]
                
            elif (i%4 == 2):
                new_dir = v + "." + v[1]
                
            else: #(i%4 == 3)
                new_dir = v[0] + "." + v[1:]

            new_rosa.append(v)
            new_rosa.append(new_dir)
    else:
        raise Exception('Esta función no está definida para rosas que no tengan 4,8 ó 16 elementos')
        
    return new_rosa

def __get_rosa_aux(rosa):
    # Duplica los bins ['N', 'NNE', 'NNE', 'NE', 'NE' .... 'N']
    # Al desplazar el bin 'N' un lugar hacia la izquierda, obteniendo una N al principio de la lista y otra al final,
    # la categorización de la dirección de viento queda "centrada" en el ángulo medio de cada bin. en español:
        # Dirección de viento entre 348.75 grados y 0 = 'N',
        # Dirección de viento entre 0 grados y 11.25 grados = 'N'
    
    return [rosa[0],] + [bin for bin in rosa[1:] for _ in (0, 1)] + [rosa[0],]

def convertir_a_rosa_de_los_vientos(val,rosa=None,estricto=True):
    '''Toma un valor int o float y asume que es una dirección de vientos en 360° grados Norte.
    
    val: Valor de la dirección de viento (int o float).
    
    estricto=True (por defecto) devuelve un error al ingresar un tipo de dato no numérico.
    estructo=False devuelve el dato original ante errores'''
    
    if rosa is None:
        rosa = rosa_de_los_vientos(bins=16)
    
    if isinstance(val,(int,float)):
        val %= 360

        #Calcular cuantos grados representa cada bin de dirección de viento 
        # Para la lista de 16 posiciones, son 32 medios bins.
        medio_bin = 180/len(rosa)
        i = int(val//medio_bin)
        rosa_aux = __get_rosa_aux(rosa)
        
        return rosa_aux[i]
    
    else:
        if estricto:
            raise ValueError('La dirección de viento debe ser un número int o float')
        else:
            return val
        
def crear_bins_viento_vel(lower_val=0,upper_val=50,step=0.5,return_dict=False):
    
    labels = __np.arange(lower_val,upper_val+step,step)
    
    hstep = step/2
    bins = [lower_val] + [ x+hstep for  x in labels]
    
    rangos = [tuple(bins[i:i+2]) for i in range(len(bins)-1)]
    
    if return_dict:
        return dict(zip(labels,rangos))
    else:
        return bins,labels
    
def crear_bins_viento_dir(rosa=None):
    
    if rosa is None:
        rosa = rosa_de_los_vientos(bins=16)
    
    step = 360/len(rosa)
    start= step/2
    stop = 360

    bins = __np.concatenate(
        [
            __np.array([0]), 
            __np.arange(start,stop,step),
            __np.array([360])
        ]
    )
    
    rangos = [tuple(bins[i:i+2]) for i in range(len(bins)-1)]
    
    labels = [convertir_a_rosa_de_los_vientos(x[0]) for x in rangos]
    
    return bins, labels

def interpolar_ppos(df_curva,wind):
    return __np.interp(wind,df_curva['WS'],df_curva.iloc[:,-1],left=0,right=0)
