import enum
import itertools
from typing import _GenericAlias  # type: ignore[attr-defined]
from typing import Dict, List, Optional, Type, Union

from classiq.interface.generator.arith.arithmetic import RegisterUserInput
from classiq.interface.generator.function_params import ArithmeticIODict, IOName

from classiq.exceptions import ClassiqQRegError


class RegisterRole(str, enum.Enum):
    INPUT = "input"
    OUTPUT = "output"
    AUXILIARY = "auxiliary"
    ZERO = "zero"


_GENERIC_ALIAS_KWARGS = {"inst": True, "special": False}


# This class is used for QReg, to support type-hint initialization
#   Due to the `size` property of QReg
class QRegGenericAlias(_GenericAlias, _root=True):  # type: ignore[call-arg]
    def __call__(self, *args, **kwargs):
        arith_info = {}
        if self.size is not None:
            arith_info["size"] = self.size
        if self.fraction_places is not None:
            arith_info["fraction_places"] = self.fraction_places

        return super().__call__(*args, **kwargs, **arith_info)

    @property
    def role(self) -> Optional[RegisterRole]:
        return getattr(self.__origin__, "role", None)

    @property
    def size(self) -> Optional[int]:
        if self.integer_places is not None:
            return self.integer_places + (self.fraction_places or 0)
        return None

    @property
    def integer_places(self) -> Optional[int]:
        if len(self.__args__) in (1, 2) and type(self.__args__[0]) is int:
            return self.__args__[0]
        return None

    @property
    def fraction_places(self) -> Optional[int]:
        if len(self.__args__) == 2 and type(self.__args__[1]) is int:
            return self.__args__[1]
        return None


class Qubit:
    pass


class QReg:
    """Represents a logical sequence of qubits.
    The QReg can be used as an `in_wires` or `out_wires` argument to ModelDesigner function calls,
    assisting in model connectivity.
    """

    def __init__(self, size: int) -> None:
        """Initializes a new QReg with the specified number of qubits.

        Args:
            size (int): The number of qubits in the QReg.
        """
        if size <= 0:
            raise ClassiqQRegError(f"Cannot create {size} new qubits")
        self._qubits = [Qubit() for _ in range(size)]

    @classmethod
    def _from_qubits(cls, qubits: List[Qubit]) -> "QReg":
        if (
            not isinstance(qubits, list)
            or not all(isinstance(qubit, Qubit) for qubit in qubits)
            or len(qubits) == 0
        ):
            raise ClassiqQRegError(f"Cannot create QReg from {qubits}")
        qreg = cls(size=1)
        qreg._qubits = qubits
        return qreg

    def __getitem__(self, key: Union[int, slice]) -> "QReg":
        state = self._qubits[key]
        return QReg._from_qubits(state if isinstance(state, list) else [state])

    def __setitem__(self, key: Union[int, slice], value: "QReg") -> None:
        if isinstance(key, int) and len(value) != 1:
            raise ClassiqQRegError(
                f"Size mismatch: value size {len(value)}, expected size 1"
            )
        self._qubits[key] = value._qubits[0] if isinstance(key, int) else value._qubits  # type: ignore[call-overload]

    def __eq__(self, other) -> bool:
        return isinstance(other, QReg) and self._qubits == other._qubits

    def isoverlapping(self, other: "QReg") -> bool:
        return isinstance(other, QReg) and not set(self._qubits).isdisjoint(
            set(other._qubits)
        )

    @classmethod
    def concat(cls, *qregs: "QReg") -> "QReg":
        """Concatenate two QRegs.

        Args:
            qregs: the QRegs to concat in order, as separate arguments.

        Returns:
            A QReg representing the concatenation of the given QRegs.

        """
        qubits = list(itertools.chain.from_iterable(qreg._qubits for qreg in qregs))
        return cls._from_qubits(qubits)

    def __len__(self) -> int:
        return len(self._qubits)

    @property
    def qubits(self) -> List[Qubit]:
        return self._qubits

    def __class_getitem__(cls, params) -> QRegGenericAlias:
        # Supporting python 3.7+, thus returning `typing._GenericAlias` instead of `types.GenericAlias`
        if type(params) is int:
            return QRegGenericAlias(cls, params, **_GENERIC_ALIAS_KWARGS)

        raise ClassiqQRegError(f"Invalid size: {params} ; int required")

    def to_register_user_input(self, name: str = "") -> RegisterUserInput:
        fraction_places = getattr(self, "fraction_places", 0)
        is_signed = getattr(self, "is_signed", False)
        return RegisterUserInput(
            name=name,
            size=len(self),
            is_signed=is_signed,
            fraction_places=fraction_places,
        )

    @staticmethod
    def from_register_user_input(reg_user_input: RegisterUserInput) -> "QReg":
        method = _get_qreg_type_from_register_user_input(reg_user_input)
        frac_attr = (
            {"fraction_places": reg_user_input.fraction_places}
            if reg_user_input.is_frac
            else {}
        )
        return method(size=reg_user_input.size, **frac_attr)


# QReg with arithmetic properties
class QSFixed(QReg):
    is_signed: bool = True

    def __init__(self, size: int, fraction_places: int) -> None:
        self.fraction_places: int = fraction_places
        super().__init__(size=size)

    def __class_getitem__(cls, params) -> QRegGenericAlias:
        # Supporting python 3.7+, thus returning `typing._GenericAlias` instead of `types.GenericAlias`
        if (
            type(params) is tuple
            and len(params) == 2
            and type(params[0]) is int
            and type(params[1]) is int
        ):
            return QRegGenericAlias(cls, params, **_GENERIC_ALIAS_KWARGS)

        raise ClassiqQRegError(f"Invalid info: {params} ; Tuple[int, int] required")


QFixed = QSFixed


class QUFixed(QFixed):
    is_signed: bool = False


class QSInt(QFixed):
    def __init__(self, size: int):
        super().__init__(size=size, fraction_places=0)

    def __class_getitem__(cls, params) -> QRegGenericAlias:
        # Integers have fraction_places always set to 0,
        # thus, their type hint is identical to that of QReg.
        return super(QSFixed, cls).__class_getitem__(params)


QInt = QSInt


class QUInt(QInt):
    is_signed: bool = False


# QReg with synthesis properties
class ZeroQReg(QReg):
    role: RegisterRole = RegisterRole.ZERO
    wire_to_zero: bool = True


class AuxQReg(ZeroQReg):
    role: RegisterRole = RegisterRole.AUXILIARY


_PROP_TO_QREG_TYPE = {
    (False, False): QUInt,
    (False, True): QUFixed,
    (True, False): QSInt,
    (True, True): QSFixed,
}


def _get_qreg_type_from_register_user_input(
    reg_user_input: RegisterUserInput,
) -> Type["QReg"]:
    qreg_arith_props = (reg_user_input.is_signed, reg_user_input.is_frac)
    return _PROP_TO_QREG_TYPE[qreg_arith_props]


def _get_qreg_generic_alias_from_register_user_input(
    reg_user_input: RegisterUserInput,
) -> QRegGenericAlias:
    qreg_type = _get_qreg_type_from_register_user_input(reg_user_input)
    if reg_user_input.fraction_places == 0:
        return QRegGenericAlias(qreg_type, reg_user_input.size, **_GENERIC_ALIAS_KWARGS)
    params = (
        reg_user_input.size - reg_user_input.fraction_places,
        reg_user_input.fraction_places,
    )
    return QRegGenericAlias(qreg_type, params, **_GENERIC_ALIAS_KWARGS)


def get_type_and_size_dict(
    rui_dict: ArithmeticIODict,
) -> Dict[IOName, QRegGenericAlias]:
    return {
        io_name: _get_qreg_generic_alias_from_register_user_input(rui)
        for io_name, rui in rui_dict.items()
    }


__all__ = [
    "QReg",
    "QInt",
    "QSInt",
    "QUInt",
    "QFixed",
    "QSFixed",
    "QUFixed",
    "ZeroQReg",
    "AuxQReg",
]
