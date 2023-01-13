from __future__ import annotations

import hashlib
import hmac

from .patterns import PatternGenerator


def encode_int(number: int) -> bytes:
    n_bytes = (number.bit_length() + 7) // 8
    return number.to_bytes(n_bytes, "little")


def generate_entropy(topic: str, seed: bytes, space: int) -> int:
    blocks_needed = ((space + 1).bit_length() + 31) // 32
    data = b"".join(hmac.digest(topic.encode(), f"{i}:".encode() + seed, "sha256") for i in range(blocks_needed))
    return int.from_bytes(data, "little") % space


class DefaultGenerator:
    def __init__(self, config: dict[str, str]):
        if "seed" not in config:
            raise ValueError("secrets.seed is not configured--set it to a cryptographically random globally unique string")
        self.seed = config["seed"]

        self.secret_generators = {name: PatternGenerator(format) for name, format in config.items() if name != "seed"}
        if "token" not in self.secret_generators:
            self.secret_generators["token"] = PatternGenerator("[a-z0-9]{16}")


    def get_secret(self, name: str, seed: str, mac: bool=False) -> str:
        if name not in self.secret_generators:
            raise ValueError(f"{name} is not a valid secret name because secrets.{name} is not set")

        secret_generator = self.secret_generators[name]
        entropy_space = secret_generator.get_entropy_space()

        if mac:
            subject_entropy_space = int(entropy_space ** 0.5)
            signature_entropy_space = entropy_space // subject_entropy_space
            subject = generate_entropy(f"subject_{name}", seed.encode(), subject_entropy_space)
            signature = generate_entropy(f"signature_{name}", encode_int(subject), signature_entropy_space)
            entropy = subject + signature * subject_entropy_space
        else:
            entropy = generate_entropy(f"secret_{name}", seed.encode(), entropy_space)

        return secret_generator.generate(entropy)


    def validate_secret(self, name: str, secret: str) -> bool:
        if name not in self.secret_generators:
            raise ValueError(f"{name} is not a valid secret name because secrets.{name} is not set")

        secret_generator = self.secret_generators[name]
        entropy_space = secret_generator.get_entropy_space()

        subject_entropy_space = int(entropy_space ** 0.5)
        signature_entropy_space = entropy_space // subject_entropy_space

        entropy = secret_generator.extract_entropy(secret)
        if entropy is None or entropy >= subject_entropy_space * signature_entropy_space:
            return False
        signature, subject = divmod(entropy, subject_entropy_space)

        # TODO: can we make this take constant time?
        return signature == generate_entropy(f"signature_{name}", encode_int(subject), signature_entropy_space)
