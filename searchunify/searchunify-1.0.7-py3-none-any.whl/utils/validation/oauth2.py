from schema import Schema, And, Use, Regex

class OauthValidator:
    def instance_url(**args):
        schema = {
            'instance': And(Use(str), Regex(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"), error="Invalid Instance URL.")
        }
        Schema(schema, ignore_extra_keys=True).validate(args)

    def access_token(**args):
        schema = {
            'username': And(Use(str), lambda s: len(s) > 0, error="username is required."),
            'password': And(Use(str), lambda s: len(s) > 0, error="password is required."),
            'client_id': And(Use(str), lambda s: len(s) > 0, error="client_id is required."),
            'client_secret': And(Use(str), lambda s: len(s) > 0, error="client_secret is required.")
        }
        Schema(schema, ignore_extra_keys=True).validate(args)

    def api_key_token(**args):
        schema = {
            'api_token': And(Use(str), lambda s: len(s) > 0, error="api_token is required.")
        }
        Schema(schema, ignore_extra_keys=True).validate(args)

    def jwt_token(**args):
        schema = {
            'jwt_token': And(Use(str), lambda s: len(s) > 0, error="jwt_token is required.")
        }
        Schema(schema, ignore_extra_keys=True).validate(args)


