from qbeast.utils import send_post


def login_with_password(username, password):
    json_body = {
        "email": username,
        "password": password
    }
    return send_post("/login", json_body)
