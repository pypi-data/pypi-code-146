import datetime
import functools

from dateutil.parser import parse

from gdshoplib.core.settings import PriceSettins

price_settings = PriceSettins()


class Price:
    def __init__(self, product):
        self.product = product

    def get_discount(self):
        # Получить текущий % наценки
        return (self.allowance_score or 0) + -(self.time_discount or 0)

    @property
    def kit(self):
        result = self.now if self.product.quantity else 0
        for product in self.product.kit:
            if product.quantity:
                result += product.price.now
        return result

    @property
    def allowance_score(self):
        # Наценка бренда
        brand_score = self.product.brand.price_coefficient if self.product.brand else 0
        # Наценка категорий

        return sum([self.product.price_coefficient, brand_score])

    @property
    def current_discount(self):
        # Получить текущую скидку
        if self.now >= self.profit:
            return 0
        return 100 - round(self.now / self.profit * 100)

    @property
    def time_discount(self):
        created_time = (
            parse(self.product.created_time)
            if isinstance(self.product.created_time, str)
            else self.product.created_time
        )
        created_at = (datetime.date.today() - created_time.date()).days
        if created_at > 60:
            return 15

        if created_at > 30:
            return 10

        return

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

        discount = self.get_discount()
        if discount:
            _now = self.profit + self.profit * (discount * 0.01)
            if _now < self.neitral:
                return self.neitral
            return _now

        return self.profit

    @property
    def eur(self):
        return self.product.price_eur

    @property
    @round
    def net(self):
        return self.eur * price_settings.EURO_PRICE

    @property
    @round
    @handle_ratio(price_settings.PRICE_VAT_RATIO)
    def gross(self):
        return self.net

    @property
    @round
    @handle_ratio(price_settings.PRICE_VAT_RATIO, price_settings.PRICE_NEITRAL_RATIO)
    def neitral(self):
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
