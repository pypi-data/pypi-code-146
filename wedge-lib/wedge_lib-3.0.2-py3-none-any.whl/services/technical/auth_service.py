from django.core.signing import BadSignature

from w.services.abstract_service import AbstractService


class AuthService(AbstractService):
    @classmethod
    def generate_token(cls):  # pragma: no cover
        # generate unique token
        import uuid

        return uuid.uuid4().hex

    @classmethod
    def generate_random_pwd(cls):
        return cls.generate_token()

    @classmethod
    def get_crypto_hash(cls, text: str, salt: str) -> str:
        """
        Returns:
            str: signature hash
        """
        from django.core.signing import Signer

        signer = Signer(salt)
        signed_text = signer.sign(text)
        return signed_text.replace(f"{text}:", "")

    @classmethod
    def is_crypto_hash_valid(cls, text: str, hash: str, salt: str) -> bool:
        """
        check signature (<text>:<crypto hash>) and return text on success
        else raise RuntimeError
        """
        from django.core.signing import Signer

        signer = Signer(salt)
        try:
            signer.unsign(f"{text}:{hash}")
            return True
        except BadSignature:
            return False
