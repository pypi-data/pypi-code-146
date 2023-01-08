import typing as t

if t.TYPE_CHECKING:
    from quantalpy.circuit import Circuit

_circuit_ctx = []


def _get_current_circuit() -> "Circuit":
    if not _circuit_ctx:
        raise RuntimeError("No circuit currently in context")
    return _circuit_ctx[-1]
