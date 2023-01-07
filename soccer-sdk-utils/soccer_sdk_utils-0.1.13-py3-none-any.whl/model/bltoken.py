class BlacklistToken:
    """
    This method is used to save a token to the blacklist table
    """

    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.token = kwargs.get("token")
        self.blacklisted_on = kwargs.get("blacklisted_on")

    def __repr__(self):
        return f"BlacklistToken(id={self.id}, token={self.token}, blacklisted_on={self.blacklisted_on})"
