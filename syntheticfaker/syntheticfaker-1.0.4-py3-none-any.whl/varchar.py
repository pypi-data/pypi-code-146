from faker import Faker
import random

fake = Faker()

class varchar_fake_data:
    
    def __init__(self, num, field_object,column, field_name, data_dict):
        
        self.num = num
        self.field_object = field_object
        self.column = column
        self.field_name = field_name
        self.data_dict=data_dict
        self.varchar_list = []

    def my_lib(self, code, data_dict):
        return random.choice(data_dict['model'][code])

    def varchar_fake(self):
        
        for n in range(self.num):
            if self.column not in self.field_object:
                self.varchar_list.append(fake.pystr())
                
            elif self.field_name['fields'][self.column] == 'harcoded_value':
                hard_code=self.field_name['constraints'][self.column]
                self.varchar_list.append(hard_code)

            elif self.field_name['fields'][self.column] == 'first_name':
                self.varchar_list.append(fake.first_name())

            elif self.field_name['fields'][self.column] == 'last_name':
                self.varchar_list.append(fake.last_name())

            elif self.field_name['fields'][self.column] == 'name':
                self.varchar_list.append(fake.name())

            elif self.field_name['fields'][self.column] == 'first_name_male':
                self.varchar_list.append(fake.first_name_male())

            elif self.field_name['fields'][self.column] == 'first_name_male':
                self.varchar_list.append(fake.first_name_female())

            elif self.field_name['fields'][self.column] == 'name_male':
                self.varchar_list.append(fake.name_male())

            elif self.field_name['fields'][self.column] == 'name_female':
                self.varchar_list.append(fake.name_female())

            elif self.field_name['fields'][self.column] == 'email':
                self.varchar_list.append(fake.ascii_safe_email())

            elif self.field_name['fields'][self.column] == 'random_letter':
                self.varchar_list.append(fake.random_letter())

            elif self.field_name['fields'][self.column] == 'product_number':
                self.varchar_list.append(fake.bothify(text='????-########'))

            elif self.field_name['fields'][self.column] == 'ip_address':
                self.varchar_list.append(fake.hexify(text='^^:^^:^^:^^:^^:^^'))

            elif self.field_name['fields'][self.column] == 'language_code':
                self.varchar_list.append(fake.language_code())

            elif self.field_name['fields'][self.column] == 'building_number':
                self.varchar_list.append(fake.building_number())

            elif self.field_name['fields'][self.column] == 'city':
                self.varchar_list.append(fake.city())

            elif self.field_name['fields'][self.column] == 'country':
                self.varchar_list.append(fake.country())     

            elif self.field_name['fields'][self.column] == 'country_code':
                self.varchar_list.append(fake.country_code())

            elif self.field_name['fields'][self.column] == 'postcode':
                self.varchar_list.append(fake.postcode())

            elif self.field_name['fields'][self.column] == 'street_address':
                self.varchar_list.append(fake.street_address())

            elif self.field_name['fields'][self.column] == 'street_name':
                self.varchar_list.append(fake.country_code())

            elif self.field_name['fields'][self.column] == 'license_plate':
                self.varchar_list.append(fake.license_plate())

            elif self.field_name['fields'][self.column] == 'bban':
                self.varchar_list.append(fake.bban())     

            elif self.field_name['fields'][self.column] == 'iban':
                self.varchar_list.append(fake.iban())

            elif self.field_name['fields'][self.column] == 'postcode':
                self.varchar_list.append(fake.postcode())

            elif self.field_name['fields'][self.column] == 'street_address':
                self.varchar_list.append(fake.street_address())

            elif self.field_name['fields'][self.column] == 'street_name':
                self.varchar_list.append(fake.country_code())

            elif self.field_name['fields'][self.column] == 'license_plate':
                self.varchar_list.append(fake.license_plate())

            elif self.field_name['fields'][self.column] == 'alphanum8':
                self.varchar_list.append(fake.swift8())

            elif self.field_name['fields'][self.column] == 'alphanum11':
                self.varchar_list.append(fake.swift11())

            elif self.field_name['fields'][self.column] == 'swid':
                self.varchar_list.append('{'+fake.bothify(text='?##?-?###-#??#-#???'+'}'))

            elif self.field_name['fields'][self.column] == 'credit_card_number':
                self.varchar_list.append(fake.credit_card_number()) 

            elif self.field_name['fields'][self.column] == 'currency_symbol':
                self.varchar_list.append(fake.currency_symbol())  

            elif self.field_name['fields'][self.column] == 'amount':
                self.varchar_list.append(fake.pricetag()) 

            elif self.field_name['fields'][self.column] == 'day_of_month':
                self.varchar_list.append(fake.day_of_month()) 

            elif self.field_name['fields'][self.column] == 'day_of_week':
                self.varchar_list.append(fake.day_of_week()) 

            elif self.field_name['fields'][self.column] == 'month_name':
                self.varchar_list.append(fake.month_name()) 

            elif self.field_name['fields'][self.column] == 'month':
                self.varchar_list.append(fake.month()) 

            elif self.field_name['fields'][self.column] == 'free_email':
                self.varchar_list.append(fake.free_email()) 

            elif self.field_name['fields'][self.column] == 'http_method':
                self.varchar_list.append(fake.http_method()) 

            elif self.field_name['fields'][self.column] == 'ipv4':
                self.varchar_list.append(fake.ipv4()) 

            elif self.field_name['fields'][self.column] == 'ipv6':
                self.varchar_list.append(fake.ipv6()) 

            elif self.field_name['fields'][self.column] == 'uri':
                self.varchar_list.append(fake.uri()) 

            elif self.field_name['fields'][self.column] == 'user_name':
                self.varchar_list.append(fake.user_name())

            elif self.field_name['fields'][self.column] == 'boolean':
                self.varchar_list.append(fake.boolean())

            elif self.field_name['fields'][self.column] == 'prefix':
                self.varchar_list.append(fake.prefix())

            elif self.field_name['fields'][self.column] == 'phone_number':
                self.varchar_list.append(fake.phone_number())

            elif self.field_name['fields'][self.column] == 'float_number':
                self.varchar_list.append(fake.pyfloat())

            elif self.field_name['fields'][self.column] == 'decimal_number':
                self.varchar_list.append(fake.pydecimal())

            elif self.field_name['fields'][self.column] == 'color' or self.field_name['fields'][self.column] == 'colour':
                colors=self.my_lib('color',self.data_dict)
                self.varchar_list.append(colors)

            elif self.field_name['fields'][self.column] == 'shoe_brand':
                brands=self.my_lib('shoe_brand',self.data_dict)
                self.varchar_list.append(brands)

            elif self.field_name['fields'][self.column] == 'shoe_name':
                shoe_name=self.my_lib('shoe_name',self.data_dict)
                self.varchar_list.append(shoe_name)

            elif self.field_name['fields'][self.column] == 'electronics_brand':
                electronics_brand=self.my_lib('electronics_brand',self.data_dict)
                self.varchar_list.append(electronics_brand)

            elif self.field_name['fields'][self.column] == 'songs':
                songs=self.my_lib('songs',self.data_dict)
                self.varchar_list.append(songs)

            elif self.field_name['fields'][self.column] == 'restaurant_names':
                restaurant_names=self.my_lib('restaurant_names',self.data_dict)
                self.varchar_list.append(restaurant_names)

            elif self.field_name['fields'][self.column] == 'wdw_park_name':
                wdw_park_name=self.my_lib('wdw_park_name',self.data_dict)
                self.varchar_list.append(wdw_park_name)

            elif self.field_name['fields'][self.column] == 'dlr_park_name':
                dlr_park_name=self.my_lib('dlr_park_name',self.data_dict)
                self.varchar_list.append(dlr_park_name)

            elif self.field_name['fields'][self.column] == 'wdw_entertainment_name':
                wdw_entertainment_name=self.my_lib('wdw_entertainment_name',self.data_dict)
                self.varchar_list.append(wdw_entertainment_name)

            elif self.field_name['fields'][self.column] == 'd_characters':
                d_characters=self.my_lib('d_characters',self.data_dict)
                self.varchar_list.append(d_characters)

            elif self.field_name['fields'][self.column] == 'd_movies_series':
                d_movies_series=self.my_lib('d_movies_series',self.data_dict)
                self.varchar_list.append(d_movies_series)

            elif self.field_name['fields'][self.column] == 'd_toys':
                d_toys=self.my_lib('d_toys',self.data_dict)
                self.varchar_list.append(d_toys)

            elif self.field_name['fields'][self.column] == 'd_toys_collectibles':
                d_toys_collectibles=self.my_lib('d_toys_collectibles',self.data_dict)
                self.varchar_list.append(d_toys_collectibles)

            elif self.field_name['fields'][self.column] == 'd_clothing':
                d_clothing=self.my_lib('d_clothing',self.data_dict)
                self.varchar_list.append(d_clothing)

            elif self.field_name['fields'][self.column] == 'alcohol':
                alcohol=self.my_lib('alcohol',self.data_dict)
                self.varchar_list.append(alcohol)

            elif self.field_name['fields'][self.column] == 'diseases':
                diseases=self.my_lib('diseases',self.data_dict)
                self.varchar_list.append(diseases)

            elif self.field_name['fields'][self.column] == 'pharma_company':
                pharma_company=self.my_lib('pharma_company',self.data_dict)
                self.varchar_list.append(pharma_company)

            elif self.field_name['fields'][self.column] == 'pharma_medicines':
                pharma_medicines=self.my_lib('pharma_medicines',self.data_dict)
                self.varchar_list.append(pharma_medicines)

            elif self.field_name['fields'][self.column] == 'pharma_drugs':
                pharma_drugs=self.my_lib('pharma_drugs',self.data_dict)
                self.varchar_list.append(pharma_drugs)

            elif self.field_name['fields'][self.column] == 'm_womens_clothing':
                m_womens_clothing=self.my_lib('m_womens_clothing',self.data_dict)
                self.varchar_list.append(m_womens_clothing)

            elif self.field_name['fields'][self.column] == 'm_mens_clothing':
                m_mens_clothing=self.my_lib('m_mens_clothing',self.data_dict)
                self.varchar_list.append(m_mens_clothing)
                
            elif self.field_name['fields'][self.column] == 'm_baby_clothing':
                m_baby_clothing=self.my_lib('m_baby_clothing',self.data_dict)
                self.varchar_list.append(m_baby_clothing)

            elif self.field_name['fields'][self.column] == 'm_girls_clothing':
                m_girls_clothing=self.my_lib('m_girls_clothing',self.data_dict)
                self.varchar_list.append(m_girls_clothing)

            elif self.field_name['fields'][self.column] == 'm_boys_clothing':
                m_boys_clothing=self.my_lib('m_boys_clothing',self.data_dict)
                self.varchar_list.append(m_boys_clothing)

            elif self.field_name['fields'][self.column] == 'm_toys':
                m_toys=self.my_lib('m_toys',self.data_dict)
                self.varchar_list.append(m_toys)

            elif self.field_name['fields'][self.column] == 'm_home_luggage':
                m_home_luggage=self.my_lib('m_home_luggage',self.data_dict)
                self.varchar_list.append(m_home_luggage)
                
            elif self.field_name['fields'][self.column] == 'm_dining':
                m_dining=self.my_lib('m_dining',self.data_dict)
                self.varchar_list.append(m_dining)

            elif self.field_name['fields'][self.column] == 'm_home_bath_shower':
                m_home_bath_shower=self.my_lib('m_home_bath_shower',self.data_dict)
                self.varchar_list.append(m_home_bath_shower)

            elif self.field_name['fields'][self.column] == 'm_home_cleaning':
                m_home_cleaning=self.my_lib('m_home_cleaning',self.data_dict)
                self.varchar_list.append(m_home_cleaning)

            elif self.field_name['fields'][self.column] == 'm_home_bed':
                m_home_bed=self.my_lib('m_home_bed',self.data_dict)
                self.varchar_list.append(m_home_bed)

            elif self.field_name['fields'][self.column] == 'm_home_kitchen':
                m_home_kitchen=self.my_lib('m_home_kitchen',self.data_dict)
                self.varchar_list.append(m_home_kitchen)
                
            elif self.field_name['fields'][self.column] == 'm_mens_shoes':
                m_mens_shoes=self.my_lib('m_mens_shoes',self.data_dict)
                self.varchar_list.append(m_mens_shoes)

            elif self.field_name['fields'][self.column] == 'm_womens_shoes':
                m_womens_shoes=self.my_lib('m_womens_shoes',self.data_dict)
                self.varchar_list.append(m_womens_shoes)

            elif self.field_name['fields'][self.column] == 'm_handbags_wallets':
                m_handbags_wallets=self.my_lib('m_handbags_wallets',self.data_dict)
                self.varchar_list.append(m_handbags_wallets)
                
            elif self.field_name['fields'][self.column] == 'm_jewelry':
                m_jewelry=self.my_lib('m_jewelry',self.data_dict)
                self.varchar_list.append(m_jewelry)
                    
        return (self.varchar_list)

