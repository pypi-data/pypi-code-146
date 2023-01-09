import math
from decimal import Decimal


def to_decimal(num):
    try:
        return Decimal(str(num))
    except Exception:
        return Decimal('0.0')


def to_decimal_n(num, n):
    try:
        num_str = '{:.' + str(n) + 'f}'
        num_str = num_str.format(num)
        return Decimal(num_str)
    except Exception:
        return Decimal('0.0')


def is_decimal(num):
    response = False
    if (to_decimal(num) - int(num)) > to_decimal('0.0'):
        response = True
    return response


def normalize_number_to_print(valor):
    valor_decimal = to_decimal(valor)
    if valor_decimal - int(valor_decimal) != 0:
        return '{:.2f}'.format(valor_decimal)
    else:
        return int(valor_decimal)


# verifica se um número é par
def se_e_par(n):
    n = int(n)
    if (n % 2) == 0:
        return True
    else:
        return False


# função criada para arredondar um valor usando a norma ABNT 5891/77
# onde valor=o valor a ser arredondado
# n=limitador da quantidade de casas
def round_abnt_video(valor, n: int):
    try:
        vl_str = str(valor)
        if '.' in vl_str:
            inteira, decimal = str(valor).split('.')
        else:
            inteira = str(valor)
            decimal = '00'
    except Exception:
        print('Erro na conversão do valor!')

    decimal = (decimal + ('0' * 10))
    if len(decimal) > (n+2):
        prox = int(decimal[n])
        pos_prox = int(decimal[n+1])
        if ((prox >= 5 and pos_prox != 0) or
           (prox == 5 and pos_prox == 0 and se_e_par(decimal[n-1]) is False)):
            aux = int(decimal[n-1]) + 1
            decimal = decimal[:n-1] + str(aux) + decimal[n:]
    decimal = decimal[:n]
    return Decimal(f'{inteira}.{decimal}')

def preencher_decimal(valor):
    try:
        vl_str = str(valor)
        if '.' not in vl_str:
            vl_str = vl_str + '.0'
    except Exception:
        print('Erro na conversão do valor!')
    
    return vl_str

def float_to_string(n: float):
    if 'e-' in str(n):
        values = str(n).split('e-')
        a = values[0].replace('.', '')
        b = int(values[1])
        return '0.' + ('0' * (b-1)) + a
    else:
        return str(n)

# função criada para arredondar um valor usando a norma ABNT do delphi onde:
# valor=0 valor a ser arredondado
# n=limitador da quantidade de casas
def round_abnt(valor, n: int):
    valor = float(valor)
    negativo = valor < 0

    delta = 0.00001
    pow_aux = pow(10, n)
    pow_value = abs(valor) / 10
    int_value = math.trunc(pow_value)
    frac_value = float('0.' + float_to_string(pow_value).split('.')[1])
    pow_value = (
        (frac_value * 10 * pow_aux/ pow(10.0, -9)) + 0.5) * pow(10.0, -9)
    int_calc = math.trunc(pow_value)
    frac_calc = float('0.' + float_to_string(pow_value).split('.')[1])
    frac_calc = math.trunc(frac_calc * 100)

    if (frac_calc > 50):
        int_calc += 1
    elif (frac_calc == 50):
        valor_temp = int_calc / 10
        last_number = round((float('0.' + float_to_string(valor_temp).split('.')[1])) * 10)
        if (last_number % 2) == 1:
            int_calc += 1
        else:
            valor_temp = pow_value * 10
            rest_part = float('0.' + float_to_string(valor_temp).split('.')[1])
            if rest_part > delta:
                int_calc += 1
    
    resultado = ((int_value * 10) + (int_calc / pow_aux))
    if negativo:
        resultado *= -1
    return resultado