from django_rds_iam_auth.middleware.jwt_injector import JWTInjector
from django_rds_iam_auth.middleware.dynamic_conn_injector import ConnectionInjector
from django_rds_iam_auth.middleware.jwt_exposer import local

import jwt
from django.conf import settings

from django.utils.translation import ugettext_lazy as _
from django import forms

from api.models import User


def my_portal_authenticate(username, password):
    if username == 'fooDjango' and password == 'barDjango':
        return True
    return False


class RlsAuthenticator(object):

    def authenticate(self, request, username=None, password=None, **kwargs):
        '''
        kwargs will receive the python dict that may contain
        username & password to authenticate which will be
        received from the Custom admin site.
        '''

        user = None
        try:
            username = username
            password = password

            try:
                decoded_data = jwt.decode(str(local.ibrag_idToken), verify=False)
                sub = decoded_data.get('sub')
                injector = JWTInjector()
                injector(**user_data)
                connection_injector = ConnectionInjector(lambda x: x)
                connection_injector(request,False,sub)
                user = User.objects.using(sub).get(id=sub)
                if not user or not isinstance(user, User):
                    raise Exception
            except Exception as ex:
                raise forms.ValidationError(
                    _("Username / Password Mismatch")
                )
        except KeyError as e:
            raise forms.ValidationError(
                _("Programming Error")
            )

        except User.DoesNotExist:
            '''
            Add the username to the django_auth_users so 
            that login session can keep track of it. 
            Django Admin is heavily coupled with the 
            Django User model for the user instane in the 
            django_auth_users table. The request object then 
            map the request.user feild to this object of the
            data model.
            '''

            raise forms.ValidationError(
                _("Username / Password Mismatch")
            )
            # user = User(username=username)
            # # defining the user of access group of that particular user
            # user.is_staff = True
            # user.is_superuser = True
            # suer.save()

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            # Djano Admin treats None user as anonymous your who have no right at all.
            return None