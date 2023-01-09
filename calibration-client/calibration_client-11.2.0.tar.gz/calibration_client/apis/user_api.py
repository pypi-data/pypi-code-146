"""UserApi module class"""

from ..common.base import Base


class UserApi(Base):
    def get_current_user(self):
        api_url = self.__get_api_url(model_name='me')
        return self.api_get(api_url)

    #
    # Private Helper Methods
    #
    def __get_api_url(self, model_name='user', api_specifics=''):
        return self.get_api_url(model_name, api_specifics)
