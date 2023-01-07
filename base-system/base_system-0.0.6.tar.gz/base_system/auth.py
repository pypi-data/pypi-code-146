from asyncio import exceptions

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from django.contrib.auth.models import User


# Hasura > JWT Specifics
from rest_framework_simplejwt.state import token_backend


class HasuraTokenObtainPairSerializer(TokenObtainPairSerializer):
    """jwtoken序列化器
    """

    @classmethod
    def get_token(cls, user):
        """
        生成hasura jwtoken
        """
        token = super().get_token(user)
        token['user_name'] = user.username
        token['user_email'] = user.email
        token['https://hasura.io/jwt/claims'] = {}
        # token['https://hasura.io/jwt/claims']['x-hasura-allowed-roles'] = [g.name for g in user.roles.all()]
        token['https://hasura.io/jwt/claims']['x-hasura-allowed-roles'] = ["admin", "public"]

        # default_role = user.get_default_role
        #
        # if default_role:
        #     # token['https://hasura.io/jwt/claims']['x-hasura-default-role'] = default_role.name
        #     token['https://hasura.io/jwt/claims']['x-hasura-default-role'] = "admin"
        #     token['https://hasura.io/jwt/claims']['x-hasura-default-role-id'] = str(default_role.id)
        #
        # # token['https://hasura.io/jwt/claims']['x-hasura-allowed-org-ids'] = [str(org.id) for org in
        # # user.organizations.all()]
        #
        # default_org = user.get_default_organization
        # if default_org:
        #     token['https://hasura.io/jwt/claims']['x-hasura-default-org'] = default_org.name
        #     token['https://hasura.io/jwt/claims']['x-hasura-default-org-id'] = str(default_org.id)

        token['https://hasura.io/jwt/claims']['x-hasura-user-id'] = str(user.id)

        return token


class ValidateTokenRefreshSerializer(TokenRefreshSerializer):
    """
    validate token
    """
    error_msg = 'No active account found with the given credentials'

    def validate(self, attrs):
        """_summary_
        Args:
            attrs (_type_): _description_
        Raises:
            exceptions.AuthenticationFailed: _description_
            exceptions.AuthenticationFailed: _description_
            exceptions.AuthenticationFailed: _description_
        Returns:
            _type_: _description_
        """
        token_payload = token_backend.decode(attrs['refresh'])
        try:
            user = User.objects.get(pk=token_payload['user_id'])
        except User.DoesNotExist:
            print('User does not exist')
            raise exceptions.AuthenticationFailed(
                self.error_msg, 'no_active_account'
            )

        if not user.is_active or user.email != token_payload['user_email']:
            print('Email Does Not Exist / Non-Active')
            raise exceptions.AuthenticationFailed(
                self.error_msg, 'no_active_account'
            )

        if user.profile.role != token_payload['https://hasura.io/jwt/claims']['x-hasura-default-role']:
            print(user.profile.role)
            print(token_payload['https://hasura.io/jwt/claims']
                  ['x-hasura-default-role'])
            print('Roles Dont Match')
            raise exceptions.AuthenticationFailed(
                self.error_msg, 'no_active_account'
            )

        return super().validate(attrs)
