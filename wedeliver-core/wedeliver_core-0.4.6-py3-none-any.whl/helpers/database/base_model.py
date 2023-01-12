from wedeliver_core import WeDeliverCore
from wedeliver_core.helpers.auth import Auth


def init_base_model():
    app = WeDeliverCore.get_app()
    db = app.extensions['sqlalchemy'].db

    class BaseModel(db.Model):
        __abstract__ = True
        id = db.Column(db.Integer, primary_key=True)
        creation = db.Column(db.DateTime, default=db.func.now())
        created_by = db.Column(db.String(64), default=Auth.get_user_str)

        modification = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

        # def __init__(self, created_by=None):
        #     self.created_by = created_by or Auth.get_user().get("email", "Guest")

    return BaseModel
