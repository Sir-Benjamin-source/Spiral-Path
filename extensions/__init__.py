"""
Spiral-Path Extensions

This package contains modular extensions for the Spiral-Path reasoning engine.

Current extensions:
- physics: Spiral-modulated physics models (e.g. Tavis spiral)
- algebra: Foundational Spiral Algebra Engine & Qubit Lattice Mapping
"""

from . import physics
try:
    from . import algebra
except ImportError:
    algebra = None

__all__ = ["physics", "algebra"]