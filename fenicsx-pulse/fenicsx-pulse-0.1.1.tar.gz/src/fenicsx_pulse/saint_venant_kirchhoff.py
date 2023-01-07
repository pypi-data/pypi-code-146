from __future__ import annotations

from dataclasses import dataclass

import dolfinx
import ufl

from .material_model import MaterialModel


@dataclass(frozen=True, slots=True)
class SaintVenantKirchhoff(MaterialModel):
    r"""
    Class for Saint Venant-Kirchhoff material

    Let

    .. math::
        \epsilon =  \frac{1}{2} ( \nabla u + \nabla u^T  +  \nabla u + \nabla u^T )

    Then

    .. math
        \psi(F) = \frac{\lambda}{2} \mathrm{tr} \left( \epsilon \right)^2
        + \mu \mathrm{tr} \left( \epsilon \cdot \epsilon \right)

    """

    mu: float | dolfinx.fem.Function | dolfinx.fem.Constant
    lmbda: float | dolfinx.fem.Function | dolfinx.fem.Constant

    def strain_energy(self, F):

        dim = ufl.domain.find_geometric_dimension(F)
        gradu = F - ufl.Identity(dim)
        epsilon = 0.5 * (gradu + gradu.T)
        return self.lmbda / 2 * (ufl.tr(epsilon) ** 2) + self.mu * ufl.tr(
            epsilon * epsilon,
        )
