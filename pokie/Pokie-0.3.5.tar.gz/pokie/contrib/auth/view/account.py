from flask_login import login_user, logout_user
from rick.event import EventManager

from pokie.constants import DI_EVENTS
from pokie.contrib.auth.constants import SVC_USER, SVC_AUTH, SVC_ACL
from pokie.contrib.auth.service import UserService, AuthService, AclService
from pokie.http.view import PokieView, PokieAuthView
from rick.form import field, RequestRecord


class LoginRequest(RequestRecord):
    fields = {
        "username": field(validators="required"),
        "password": field(validators="required"),
        "remember": field(validators="bool"),
    }


class LoginView(PokieView):
    request_class = LoginRequest

    def post(self):
        username = self.request.get("username")
        pwd = self.request.get("password")
        remember = bool(self.request.get("remember"))

        user = self.svc_auth().authenticate(username, pwd)
        if user is None:
            return self.error("invalid credentials")

        user.password = None

        result = self.svc_acl().get_user_acl_info(user.id)
        result["user"] = user.asdict()

        self.mgr_event().dispatch(self.di, "afterLogin", result)

        # flask-login
        login_user(user, bool(remember))

        return self.success(result)

    def mgr_event(self) -> EventManager:
        return self.di.get(DI_EVENTS)

    def svc_user(self) -> UserService:
        return self.get_service(SVC_USER)

    def svc_auth(self) -> AuthService:
        return self.get_service(SVC_AUTH)

    def svc_acl(self) -> AclService:
        return self.get_service(SVC_ACL)


class LogoutView(PokieAuthView):
    def get(self):
        logout_user()
        return self.success()
