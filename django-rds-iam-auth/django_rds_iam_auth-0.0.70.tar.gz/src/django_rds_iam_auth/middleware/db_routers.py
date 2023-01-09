from django.conf import settings
from django_rds_iam_auth.middleware.jwt_exposer import local
import jwt



class GenericRLSSecuredRouter:
    """
    DB Router to controll which type of connection pool will be used, defaut / RLS secured
    The RLS secured pool stores connections in REDIS cache ( the rls_iam_auth package generates the cache for any new instance useing
    cognito service, the TTL is taken from cognito token experation dateTime

    if the type of DB is mongo you sould add is_mongo() method to your Django Model that returns True. in such case this
    router will not be used (punch through on all actions)

    Notice this router is for operational work only and will not (and should not be) used for running migrations
    the responsibility for migrations resides with the host app.
    """
    excluded_apps = settings.EXCLUDE_APP_FROM_SECURE_RLS

    @staticmethod
    def has_method(o, name):
        return callable(getattr(o, name, None))

    def db_for_read(self, model, **hints):
        """
        If Model is not in excluded app and not of type mongo - use RLS Secure Connection.
        """
        if model._meta.app_label not in self.excluded_apps and (not self.has_method(model,'is_mongo') or not model.is_mongo()):
            try:
                token = jwt.decode(local.ibrag_idToken, verify=False)
            except Exception:
                return None
            if not token or not isinstance(token, dict) or 'sub' not in token:
                return None
            return token.get('sub', None)
        return None

    def db_for_write(self, model, **hints):
        """
        If Model is not in excluded app and not of type mongo - use RLS Secure Connection.
        """
        if model._meta.app_label not in self.excluded_apps and (
                not self.has_method(model, 'is_mongo') or not model.is_mongo()):
            try:
                token = jwt.decode(local.ibrag_idToken, verify=False)
            except Exception:
                return None
            if not token or not isinstance(token, dict) or 'sub' not in token:
                return None
            return token.get('sub', None)
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Responsibility of host app.
        """
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Responsibility of host app.
        """
        return None