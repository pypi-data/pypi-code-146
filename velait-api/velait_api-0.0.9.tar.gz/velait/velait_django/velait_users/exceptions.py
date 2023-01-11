from django.utils.translation import gettext_lazy as _

from velait.common.database.exceptions import VelaitError


class UserAuthenticationError(VelaitError):
    def __init__(self):
        super(UserAuthenticationError, self).__init__(name="auth", description=_('Ошибка аутентификации'))
