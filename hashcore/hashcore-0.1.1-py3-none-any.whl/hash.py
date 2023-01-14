"""
Main hash module for calculating and storing hashes
"""

from dirhash import dirhash

from hash import logs

logger = logs.getLogger(__name__)

def setupLogger(output, level):
    logs.setOutput(logger, output)
    logs.setLevel(logger, level)

class Hash (object):
    """
    Docs for Hash class
    """
    __supported_algs = ["md5", "sha1", "sha256", "sha512"]
    def __init__(self, alg="sha256") -> None:
        if alg not in Hash.__supported_algs:
            raise ValueError(f"Algorith {alg} is not supported, please select from {Hash.__supported_algs}")
        self.alg = alg

    def hash(self, path, match=None) -> str:
        """
        hash method
        """
        if match:
            return dirhash(path, self.alg, match=match)
        return dirhash(path, self.alg)

    def __repr__(self) -> str:
        return f"<Hash alg: {self.alg}>"
