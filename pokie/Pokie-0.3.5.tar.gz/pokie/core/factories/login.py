import uuid

from flask_login import LoginManager
from rick.base import Di

from pokie.constants import DI_CONFIG, DI_SERVICES, CFG_AUTH_SECRET, DI_FLASK
from pokie.contrib.auth.constants import SVC_AUTH


def FlaskLogin(_di: Di):
    """
    FlaskLogin factory
    :param _di:
    :return:
    """
    cfg = _di.get(DI_CONFIG)
    app = _di.get(DI_FLASK)
    app.secret_key = cfg.get(CFG_AUTH_SECRET, uuid.uuid4().hex)
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # restores user profile from auth service
        return _di.get(DI_SERVICES).get(SVC_AUTH).load_id(user_id)
