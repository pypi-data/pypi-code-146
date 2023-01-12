from datetime import datetime, timedelta
from pprint import pprint
from bson import ObjectId
from ..utilities.dates import today_argentina, DIAS_ANTICIPO_DE_PAGO


class Boleta:
    def __init__(self):
        # self.date_created = None
        # self.status = None
        # self.merchant_id = None
        # self.member_id = None
        # self.tries = []
        pass

    def create(self,
               cliente_id,
               merchant_id,
               plan_id,
               source: str,
               status: str = 'error_not_proccesed',
               charges_detail: dict = dict(),
               opd: datetime = today_argentina(),
               date_created: datetime = today_argentina(),
               additional_fields: dict = dict(),
            ):

        ids = [cliente_id, merchant_id, plan_id]
        for field_id in ids:
            try:
                field_id = ObjectId(field_id)
            except:
                pass
        self.member_id = cliente_id
        self.date_created = date_created
        self.original_payment_date = opd
        self.source = source
        self.tries = list()
        self.status = status
        self.merchant_id = merchant_id
        self.charges_detail = charges_detail
        self.period = None
        # Plan
        self.plan_id = plan_id
        # Si existen campos adicionales a los tradicionales se agregan
        for key, value in additional_fields.items():
            setattr(self, key, value)

    def push_to_db(self, db, id_return=False):
        #db = init_mongo()
        if hasattr(self, '_id'):
            result = db.boletas.update_one(
                {'_id': self._id}, {'$set': self.__dict__})
            if id_return:
                return self._id
        else:
            result = db.boletas.insert_one(self.__dict__)
            self._id = result.inserted_id
            if id_return:
                return result.inserted_id
        pass

    def import_from_db(self, boleta: dict):
        for key in boleta.keys():
            setattr(self, key, boleta[key])

    def add_try(self, payment_data: dict, card_data: dict = dict()):
        # Complete with card data
        if card_data != dict():
            for e in ["card_brand", "card_id", "payment_type"]:
                if e in card_data:
                    payment_data[e] = card_data[e]
                elif e not in "payment_data":
                    payment_data[e] = None

        if 'payment_type' not in payment_data:
            try:
                payment_data['payment_type'] = payment_data['card']['card_type']
            except:
                payment_data['payment_type'] = None
        # Genera el nuevo try
        new_try = {
            'try_number': len(self.tries)+1,
            'payment_day': payment_data['payment_day'],
            'payment_type': payment_data['payment_type'],
            'status': payment_data['status'],
            'status_detail': payment_data['status_detail'],
            'card_id': payment_data['card_id'],
            'card_brand': payment_data['card_brand'],
            'payment_id': payment_data['id'],
            'processor': payment_data['processor'] if 'processor' in payment_data else None
        }
        self.tries.append(new_try)
        self.status = new_try['status']
        pass

    def make_period(self, fecha_de_cobro: datetime, DIAS_DE_ANTICIPO: int = 0):
        if 'recurring' in self.source:
            DIAS_DE_ANTICIPO = DIAS_ANTICIPO_DE_PAGO
        fecha_de_cobro += timedelta(days=DIAS_DE_ANTICIPO)
        period = f"{fecha_de_cobro.month}/{fecha_de_cobro.year}"
        self.period = period

    def print(self):
        pprint(self.__dict__)

    def to_dict(self):
        return self.__dict__
