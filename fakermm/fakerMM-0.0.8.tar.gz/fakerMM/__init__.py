import numpy as np
from faker import Faker
import random
fake = Faker('es-ES')

#                     NOMBRE Y APELLIDOS DE PERSONA FISICA
#------------------------------------------------------------------------------------------
#Datos sinteticos de nombre y apellidos cuando no hay una columna que especifique el sexo
def full_name_MM_gender_random(row):

    name = ''
    sex = np.random.randint(0, 1) 
    if sex==1: # female
        name = fake.last_name() + ' ' + fake.last_name() + '; ' + fake.first_name_female()
    else: # male
        name = fake.last_name() + ' ' + fake.last_name() + '; ' + fake.first_name_male()
    
    return(name)

#Nombre y apellidos con formato Nombre Apellido1 Apellido2
def full_name_gender_random(row):

    name = ''
    sex = np.random.randint(0, 1) 
    if sex==1: # female
        name = fake.first_name_female() + ' ' + fake.last_name() + ' ' + fake.last_name() 
    else: # male
        name = fake.first_name_male() + ' ' + fake.last_name() + ' ' + fake.last_name() 
    
    return(name)

#Nombre propio con género aleatorio
def first_name_gender_random(row):

    name = ''
    sex = np.random.randint(0, 1) 
    if sex==1: # female
        name = fake.first_name_female()
    else: # male
        name = fake.first_name_male()
    
     
    return(name)

#Apellido 
def last_name(row):
    last_name = fake.last_name() 
            
    return(last_name)

#Nombre propio cuando el género sea especificado como H para hombre y M para mujer
def first_name_gender_Hmale_Mfemale(row):
    if row['gender'] == 'M':
        name_sex = fake.first_name_female()
    else:
        name_sex = fake.first_name_male()
    return name_sex

#Nombre propio cuando el género sea especificado como 0 para hombre y 1 para mujer
def first_name_gender_0male_1female(row):
    if row['gender'] == 1:
        name_sex = fake.first_name_female()
    else:
        name_sex = fake.first_name_male()
    return name_sex

#Nombre propio cuando el género sea especificado como M para hombre y F para mujer     
def first_name_gender_Male_Female(row):
    if row['gender'] == 'F':
        name_sex = fake.first_name_female()
    else:
        name_sex = fake.first_name_male()
    return name_sex   

#Nombre completo con formato Apellido1 Apellido2; Nombre cuando el género se especifica como H hombre y M mujer
def full_name_MM_gender_Hmale_Mfemale(row):
    if row['gender'] == 'M':
        name_sex = fake.last_name() + ' ' + fake.last_name() + '; ' + fake.first_name_female()
    else:
        name_sex = fake.last_name() + ' '+ fake.last_name() + '; '+ fake.first_name_male()
    return name_sex

#Nombre completo con formato Apellido1 Apellido2; Nombre cuando el género se especifica como 0 hombre y 1 mujer
def full_name_MM_gender_0male_1female(row):
    if row['gender'] == 1:
        name_sex = fake.last_name() + ' ' + fake.last_name() + '; ' + fake.first_name_female()
    else:
        name_sex = fake.last_name() + ' '+ fake.last_name() + '; '+ fake.first_name_male()
    return name_sex

#Nombre completo con formato Apellido1 Apellido2; Nombre cuando el género se especifica como M hombre y F mujer      
def full_name_MM_gender_Male_Female(row):
    if row['gender'] == 'F':
        name_sex = fake.last_name() + ' ' + fake.last_name() + '; ' + fake.first_name_female()
    else:
        name_sex = fake.last_name() + ' '+ fake.last_name() + '; '+ fake.first_name_male()
    return name_sex

#Nombre completo con formato  Nombre Apellido1 Apellido2 cuando el género se especifica como H hombre y M mujer

def full_name_gender_Hmale_Mfemale(row):

    if row['gender'] == 'M':#female
         name = fake.first_name_female() + ' ' + fake.last_name() + ' ' + fake.last_name() 
    else: # male
        name = fake.first_name_male() + ' ' + fake.last_name() + ' ' + fake.last_name() 
    
    return(name)

#Nombre completo con formato  Nombre Apellido1 Apellido2 cuando el género se especifica como 0 hombre y 1 mujer

def full_name_gender_0male_1female(row):

    if row['gender'] == '1':#female
         name = fake.first_name_female() + ' ' + fake.last_name() + ' ' + fake.last_name() 
    else: # male
        name = fake.first_name_male() + ' ' + fake.last_name() + ' ' + fake.last_name() 
    
    return(name)

#Nombre completo con formato  Nombre Apellido1 Apellido2 cuando el género se especifica como M hombre y F mujer

def full_name_gender_Male_Female(row):

    if row['gender'] == 'F':#female
         name = fake.first_name_female() + ' ' + fake.last_name() + ' ' + fake.last_name() 
    else: # male
        name = fake.first_name_male() + ' ' + fake.last_name() + ' ' + fake.last_name() 
    
    return(name)

#                           EMAIL
#------------------------------------------------------------------------------------------
#Correo electronico
def email(row):
    return(fake.ascii_safe_email())

#                          TELEFONO
#------------------------------------------------------------------------------------------
#Numero de telefono sin prefijo +34
def phone_number_no_national_prefix(row):
    
    phone=fake.phone_number().replace(' ', '')
    phone=phone.replace('+34','')
    
    return(phone)

#Numero de telefono con prefijo
def phone_number_with_national_prefix(row):
    
    phone=fake.phone_number().replace(' ', '')
    
    return(phone)


#                          DIRECCION
#------------------------------------------------------------------------------------------
#Direccion completa linea 1
def full_address_line1(row):
      address = fake.street_address() + ', ' + fake.city()
    
      return(address) 

types_street=['CL', 'AV', 'PG', 'AP', 'CR', 'LG', 'AC', 'UR', 'RD',
       'RO', 'AT', 'CM', 'ZO', 'CO', 'C1', 'PD', 'PZ', 'VA', 'PS', 'RB',
       'ED', 'CD', 'RU', 'TR', 'PQ', 'CA', 'PC', 'CI', 'BO', 'VD', 'CU',
       'CJ', 'PA', 'AU', 'VI', 'CZ', 'BD', 'GV', 'CC', 'PE', 'FN', 'GT',
       'CT', 'ST', 'AL', 'MO', 'CH', 'AB', 'CS', 'PO', 'PT', 'TU', 'SA',
       'EA', 'AR', 'MT', 'GR', 'PR', 'CE', 'AM', 'RA', 'ET', 'OT', 'EX',
       'AE', 'PB', 'AG', 'PJ', 'BC', 'CÑ', 'BL', 'ES', 'TV', 'PU', 'GA',
       'FU', 'RS', 'EN', 'TS', 'MC', 'TT', 'RM', 'QT', 'ER', 'GL', 'MN',
       'P1', 'SI', 'FT', 'NC', 'SN', 'EM', 'VN', 'SD', 'SC', 'CG']

#Tipo de via
def street_type_code(row):
      street_type = random.choice(types_street)
    
      return(street_type)

#Nombre de la calle   
def street_name(row):
      street_name = fake.street_name() 
    
      return(street_name) 

#Portal   
def building_number(row):
      buildingNumber = random.randint(1, 300)
    
      return(buildingNumber) 

      
#informacion ampliada. Piso y letra
door = {0:'B', 1:'D', 2:'F', 3:'A', 4:'G', 5:'C', 
              6:'E', 7:'F', 8:'H', 9:'IZQ', 10:'DCH', 11:'I'}

def building_flat_door(row):
    num = "".join(["{}".format(np.random.randint(0, 2)) for i in range(2)])
    letter = door[int(num) % 12]
    infoampl = str(num) +' '+ str(door)  
    return(infoampl) 

#Ciudad-localidad
def city(row):
      city = fake.city()
    
      return(city) 

#Pendientes de construir las funciones de enmascaramiento de CP y provincia


#                         DNI
#------------------------------------------------------------------------------------------

#DNI

letter_map = {0:'T', 1:'R', 2:'W', 3:'A', 4:'G', 5:'M', 
              6:'Y', 7:'F', 8:'P', 9:'D', 10:'X', 11:'B', 
              12:'N', 13:'J', 14:'Z', 15:'S', 16:'Q', 
              17:'V', 18:'H', 19:'L', 20:'C', 21:'K', 22:'E'}

def national_id(row):
    id_num = "".join(["{}".format(np.random.randint(0, 9)) for i in range(8)])
    letter = letter_map[int(id_num) % 23]
    national_id = str(id_num) + str(letter)
       
    return(national_id)   


#          MATRICULA
#-------------------------------------------------------------------------------------------------
#Matricula de coche

def license_plate(row):
    letter_map1 = {0:'T', 1:'R', 2:'W', 3:'G', 4:'M', 5:'Y', 6:'F', 7:'P', 8:'D', 9:'X', 10:'B', 
              11:'N', 12:'J', 13:'Z', 14:'S', 15:'Q', 16:'V', 17:'H', 18:'L', 19:'C', 20:'K'}
    
    letter_map2 = {0:'W', 1:'G', 2:'C', 3:'Z', 4:'T', 5:'X', 6:'L', 7:'J', 8:'B', 9:'P', 10:'D', 
              11:'F', 12:'H', 13:'R', 14:'K', 15:'N', 16:'S', 17:'Q', 18:'Y', 19:'V', 20:'M'}
    
    letter_map3 = {0:'F', 1:'B', 2:'N', 3:'C', 4:'Q', 5:'G', 6:'P', 7:'D', 8:'S', 9:'V', 10:'H', 
              11:'M', 12:'Y', 13:'L', 14:'J', 15:'T', 16:'Z', 17:'K', 18:'R', 19:'X', 20:'W'}
    
    num_gen = "".join(["{}".format(np.random.randint(0, 9)) for i in range(4)])
    let_gen1= letter_map1[int(num_gen) % 21]
    let_gen2= letter_map2[int(num_gen) % 21]
    let_gen3= letter_map3[int(num_gen) % 21]
    plate = str(num_gen) + str(let_gen1)+ str(let_gen2)+ str(let_gen3)
    return (plate)


#           BASTIDOR
#----------------------------------------------------------------------------
#Numero de bastidor del coche

def car_frame(row):
    random_str_seq = "0123456789ABCDEFGHJKLMNPRSTUVWXYZ" 
    res = ''.join(random.choices(random_str_seq, k=17))
    return (res)


#        PASSWORD
#----------------------------------------------------------
#Contraseña sintetica

def password(row):
    random_str_seq = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz@?!._-#" 
    res = ''.join(random.choices(random_str_seq, k=15))
    return (res)

#    CUENTA CORRIENTE
#----------------------------------------------------------------------
#Cuenta corriente fija

def current_account(row):
    campo='99999999509999999999'
    return (campo)

#     IBAN
#---------------------------------------------------------------------
#Iban fijo

def iban(row):
    campo='ES1299999999509999999999'
    return (campo)