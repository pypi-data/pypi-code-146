import logging

logger = logging.getLogger("deqart-python-sdk")


class DeqartBaseException(Exception):
    def __init__(
        self, status_code="Unknown Status Code", message="Unknown Error Message"
    ):
        self.status_code = status_code
        self.message = message
        super().__init__(status_code, message)


class DeqartUnauthorizedException(DeqartBaseException):
    def __init__(self):
        super().__init__(
            401,
            "Wrong API key. You can find your API key once you log in to https://www.deqart.com",
        )


class DeqartStatevectorTooLarge(DeqartBaseException):
    def __init__(self, num_qubits):
        super().__init__(
            0,
            f"Statevector is too large for {num_qubits} qubits. Use .get_counts() instead.",
        )
