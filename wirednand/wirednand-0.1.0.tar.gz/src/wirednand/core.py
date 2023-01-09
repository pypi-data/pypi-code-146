from __future__ import annotations

from typing import List, Optional


class Component:
    pass


class Wire(Component):
    def __init__(
        self, origin: Optional[Component] = None, default: Optional[bool] = None
    ):
        self.origin = origin
        self.default = default


class Bus(Component):
    def __init__(self, size: int, origin: Optional[Component] = None):
        self.wires: List[Wire] = [Wire(origin) for _ in range(size)]
        self.size = size

    def __getitem__(self, wire_index: int):
        return self.wires[wire_index]

    def __setitem__(self, wire_index: int, value: Wire):
        self.wires[wire_index] = value


class Nand(Component):
    def __init__(self, a: Wire, b: Wire):
        self.a = a
        self.b = b
        self.out = Wire(self)


class NandBus(Component):
    def __init__(self, a: Bus, b: Bus):
        assert a.size == b.size
        self.a = a
        self.b = b
        out = Bus(a.size, self)
        for i in range(out.size):
            out[i] = Nand(a[i], b[i]).out
        self.out = out


class Not(Component):
    def __init__(self, a):
        nand = Nand(a, a)
        self.out = nand.out


class And(Component):
    def __init__(self, a, b):
        nand = Nand(a, b)
        not_ = Not(nand.out)
        self.out = not_.out


class Or(Component):
    def __init__(self, a, b):
        not_a = Not(a)
        not_b = Not(b)
        nand = Nand(not_a.out, not_b.out)
        self.out = nand.out


class Xor(Component):
    def __init__(self, a, b):
        nand = Nand(a, b)
        nand_a = Nand(nand.out, a)
        nand_b = Nand(nand.out, b)
        last_nand = Nand(nand_a.out, nand_b.out)
        self.out = last_nand.out


class Clock(Component):
    def __init__(self):
        one = Wire(default=True)
        nand = Nand(one, Wire())
        nand.b = nand.out
        self.out = nand.out


class SRLatch(Component):
    def __init__(self, s: Wire, r: Wire):
        nand0 = Nand(s, Wire())
        nand1 = Nand(r, nand0.out)
        nand0.b = nand1.out
        self.q = nand0.out
        self.q_ = nand1.out


class FlipFlop(Component):
    def __init__(self, s: Wire, r: Wire, clock: Wire):
        nand0 = Nand(s, clock)
        nand1 = Nand(r, clock)
        nand2 = Nand(nand0.out, Wire())
        nand2.out = Wire(nand2, default=False)
        nand3 = Nand(nand1.out, nand2.out)
        nand2.b = nand3.out
        nand3.out = Wire(nand3, default=False)
        self.q = nand2.out
        self.q_ = nand3.out


def find_nands(components: List[Component]):
    visited = set()
    nand_gates = set()

    def _find_nands(obj):
        if isinstance(obj, (Component, Wire)):
            if obj in visited:
                return
            visited.add(obj)
            if isinstance(obj, Component):
                if isinstance(obj, Nand):
                    nand_gates.add(obj)
                for _, attr_value in vars(obj).items():
                    _find_nands(attr_value)
            elif isinstance(obj, Wire):
                if obj.origin is not None:
                    _find_nands(obj.origin)
        elif isinstance(obj, list):
            for i in obj:
                _find_nands(i)

    for c in components:
        _find_nands(c)
    return nand_gates


class Simulation:
    def __init__(
        self,
        components: Component | List[Component],
        wire_to_value: Optional[dict] = None,
    ):
        if isinstance(components, list):
            self.components = components
        else:
            self.components = [components]
        self.nand_gates = find_nands(self.components)
        self.wire_to_value = wire_to_value or {}
        self.time = 0

    def step(self) -> Simulation:
        """Update the values of all components in the circuit."""
        new_wire_to_value = self.wire_to_value.copy()
        for nand in self.nand_gates:
            a = self[nand.a]
            b = self[nand.b]
            if a is not None and b is not None:
                new_wire_to_value[nand.out] = not (a and b)
        self.wire_to_value = new_wire_to_value
        self.time += 1
        return self

    def steps(self, steps: int) -> Simulation:
        for _ in range(steps):
            self.step()
        return self

    def __getitem__(self, wire) -> bool:
        """Return the value of the given wire at the current time."""
        default = False
        if wire.default is not None:
            default = wire.default
        return self.wire_to_value.get(wire, default)

    def __setitem__(self, wire, value):
        """Return the value of the given wire at the current time."""
        self.wire_to_value[wire] = value
