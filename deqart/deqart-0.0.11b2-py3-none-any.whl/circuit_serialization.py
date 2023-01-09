import base64
import io


def encode_circuit(qc):
    """
    Encode a quantum circuit object from various quantum libraries to a
    portable format.
    """
    # We use the string representation of the object class so that we don't
    # have to require users to install Qiskit, Cirq, and Braket all at once.
    circuit_type = str(type(qc))
    if circuit_type == "<class 'cirq.circuits.circuit.Circuit'>":
        import cirq

        # https://quantumai.google/cirq/build/interop
        serialized = cirq.to_json(qc)
        return {"circuit_type": "Cirq", "circuit": serialized}
    elif circuit_type == "<class 'qiskit.circuit.quantumcircuit.QuantumCircuit'>":
        from qiskit import qpy

        # https://qiskit.org/documentation/apidoc/qpy.html
        with io.BytesIO() as f:
            qpy.dump(qc, f)
            # Rewind back to the beginning of the "file".
            f.seek(0)
            serialized = f.read()
            # Convert to base64
            serialized = base64.b64encode(serialized)
            # Convert bytes to str
            serialized = serialized.decode("utf-8")
        return {"circuit_type": "Qiskit", "circuit": serialized}
    elif circuit_type == "<class 'braket.circuits.circuit.Circuit'>":
        from braket.circuits.serialization import IRType

        serialized = qc.to_ir(IRType.OPENQASM).source
        return {"circuit_type": "Braket", "circuit": serialized}
    else:
        raise Exception("Unsupported circuit type", qc)


def decode_circuit(data):
    """
    Decode the output of encode_circuit.
    """
    if "circuit_type" not in data:
        raise Exception("Wrong data structure. 'circuit_type' must be present.")
    if "circuit" not in data:
        raise Exception("Wrong data structure. 'circuit' must be present.")
    circuit_type = data["circuit_type"]
    if circuit_type == "Cirq":
        import cirq

        return cirq.read_json(json_text=data["circuit"])
    elif circuit_type == "Qiskit":
        from qiskit import qpy

        _bytes = str.encode(data["circuit"])
        _bytes = base64.b64decode(_bytes)
        with io.BytesIO(_bytes) as f:
            circuits = qpy.load(f)
            if len(circuits) != 1:
                raise Exception(
                    f"Unexpected number of circuits: {len(circuits)}. Must be 1."
                )
            return circuits[0]
    elif circuit_type == "Braket":
        raise Exception("Braket decoding is not yet supported.")
    else:
        raise Exception("Unsupported circuit type", circuit_type)
