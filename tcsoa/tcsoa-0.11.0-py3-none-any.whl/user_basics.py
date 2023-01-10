from tcsoa.basics import TcSoaBasics
from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.search_basics import TcSearchBasics


class TcUserBasics:
    @classmethod
    def find_users(cls, user_id=None, person_name=None):
        if not (user_id or person_name):
            raise ValueError('Please pass at least one of the arguments!')
        args = dict()
        if user_id:
            args['User ID'] = user_id
        if person_name:
            args['Person Name'] = person_name

        query = TcSearchBasics.get_query_by_name('Admin - Employee Information')
        matched_users = TcSearchBasics.exec_query(query, args)
        return matched_users

    @classmethod
    def get_person(cls, user: BusinessObject):
        return TcSoaBasics.getPropObject(user, 'person')

    @classmethod
    def set_person_data(
            cls,
            person: BusinessObject,
            address: str = None,
            city: str = None,
            state: str = None,
            zip_code: str = None,
            country: str = None,
            organisation: str = None,
            employee_number: str = None,
            internal_mail_code: str = None,
            mail_address: str = None,
            phone: str = None):
        if person.className == 'User':
            person = cls.get_person(person)
        if person.className != 'Person':
            raise ValueError('Please pass a User or Person object')

        attrs = dict()
        if address is not None:
            attrs['PA1'] = address
        if city is not None:
            attrs['PA2'] = city
        if state is not None:
            attrs['PA3'] = state
        if zip_code is not None:
            attrs['PA4'] = zip_code
        if country is not None:
            attrs['PA5'] = country
        if organisation is not None:
            attrs['PA6'] = organisation
        if employee_number is not None:
            attrs['PA7'] = employee_number
        if internal_mail_code is not None:
            attrs['PA8'] = internal_mail_code
        if mail_address is not None:
            attrs['PA9'] = mail_address
        if phone is not None:
            attrs['PA10'] = phone
        for prop_name, prop_val in attrs.items():
            TcSoaBasics.setPropString(person, prop_name, prop_val)
