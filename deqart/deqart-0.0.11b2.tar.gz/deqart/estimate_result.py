class EstimateResult:
    """This class contains information about the estimated runtime/cost that
    will be incurred from running the given circuit on the given quantum
    machine/simulator. WARNING: this is just an estimate, the actual runtime
    may be less or more."""

    def __init__(self, data):
        self.device = data.get("device")
        self.estimate_ms = data.get("estimate_ms")
        self.num_qubits = data.get("num_qubits")
        self.circuit = data.get("qc")
        self.warning_message = data.get("warning_message")
        self.error_message = data.get("error_message")

    def __str__(self):
        if self.error_message is not None:
            return f"Estimation failed due to error: {self.error_message}."
        return f"Estimation time in milliseconds: {self.estimate_ms}. {self.warning_message}"
