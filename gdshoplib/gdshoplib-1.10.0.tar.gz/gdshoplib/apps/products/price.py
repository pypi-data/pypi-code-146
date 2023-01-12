import datetime
import functools

from dateutil.parser import parse

from gdshoplib.core.settings import PriceSettins

price_settings = PriceSettins()


class Price:
    def __init__(self, product):
        self.product = product

    def get_score(self):
        # Получить текущий % наценки
        return (self.allowance_score or 0) + -(self.time_discount or 0)

    def get_kit_price(self, base_price="now"):
        if not self.product.kit:
            return None

        result = self[base_price] if self.product.quantity else 0
        for product in self.product.kit:
            if product.quantity:
                result += product.price[base_price]
        return result

    @property
    def allowance_score(self):
        # Наценка категорий
        categories_score = 0
        for category in self.product.categories:
            categories_score += category.price_coefficient

        # Наценка бренда
        brand_score = self.product.brand.price_coefficient if self.product.brand else 0
        return sum([self.product.price_coefficient, brand_score, categories_score])

    @property
    def current_discount(self):
        # Получить текущую скидку
        return 100 - round(self.now / self.profit * 100)

    @property
    def time_discount(self):
        created_time = self.product.discount_from_date or self.product.created_time
        created_time = (
            parse(created_time).date()
            if isinstance(created_time, str)
            else created_time
        )
        created_at = (datetime.date.today() - created_time).days

        if created_at > 60:
            return 15
        elif created_at > 30:
            return 10

        return 0

    def handle_ratio(*rations):
        def decor(func):
            @functools.wraps(func)
            def wrap(self, *args, **kwargs):
                ration = sum([1, *rations])
                return func(self, *args, **kwargs) * ration

            return wrap

        return decor

    def round(func):
        @functools.wraps(func)
        def wrap(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            return int(round(result, 0))

        return wrap

    @property
    @round
    def now(self):
        if not self.product.quantity:
            return self.neitral

        discount = self.get_score()
        if discount:
            _now = self.profit + self.profit * (discount * 0.01)
            if _now < self.neitral:
                return self.neitral
            return _now

        return self.profit

    @property
    def eur(self):
        # Цена в EUR
        return self.product.price_eur

    @property
    @round
    def net(self):
        # Цена в рублях
        return self.eur * price_settings.EURO_PRICE

    @property
    @round
    @handle_ratio(price_settings.PRICE_VAT_RATIO)
    def gross(self):
        # Цена с учетом расходов и налогов на закупку
        return self.net

    @property
    @round
    @handle_ratio(price_settings.PRICE_VAT_RATIO, price_settings.PRICE_NEITRAL_RATIO)
    def neitral(self):
        # Цена безубыточности
        return self.net

    @property
    @round
    @handle_ratio(
        price_settings.PRICE_VAT_RATIO,
        price_settings.PRICE_NEITRAL_RATIO,
        price_settings.PRICE_PROFIT_RATIO,
    )
    def profit(self):
        return self.net

    def __getitem__(self, key):
        try:
            return super(Price, self).__getattribute__(key)
        except AttributeError:
            return self.__getattr__(key)
