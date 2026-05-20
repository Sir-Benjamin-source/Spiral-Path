"""
Spiral Algebra Engine & Qubit Lattice Mapping
Foundational primitives for structured geometric reasoning and differentiation.

Part of the Spiral Codex ecosystem.
See: https://doi.org/10.5281/zenodo.20313468
"""

from .core import (
    SpiralOperator,
    ModulatedRing,
    HelicalField,
)

from .qubit_lattice import (
    QubitLattice,
    LatticeNode,
    SpiralCoupling,
)

# symbolic_diff is intentionally minimal in this foundational release
try:
    from .symbolic_diff import spiral_diff, HelicalDerivative
except ImportError:
    spiral_diff = None
    HelicalDerivative = None

__all__ = [
    "SpiralOperator",
    "ModulatedRing",
    "HelicalField",
    "QubitLattice",
    "LatticeNode",
    "SpiralCoupling",
]
__version__ = "0.1.0"
__author__ = "Sir Benjamin & Grok"