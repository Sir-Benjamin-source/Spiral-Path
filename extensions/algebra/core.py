"""
Core spiral-modulated algebraic structures.

This module defines the foundational operators and structures for applying
helical/spiral modulation to algebraic objects (rings, fields, transformations).

These are the "bones" of the Spiral Algebra Engine — kept deliberately
lightweight and extensible.
"""

from dataclasses import dataclass
from typing import Callable, Optional
import numpy as np


@dataclass
class SpiralOperator:
    """
    A helical modulation operator.

    Applies oscillatory refinement between expansive (creative) and
    contractive (refining) phases. The phase parameter controls position
    within the current spiral cycle.

    Attributes
    ----------
    phase : float
        Current position in the spiral cycle (typically [0, 2π)).
    amplitude : float
        Strength of the modulation.
    frequency : float
        Number of oscillations per full spiral cycle.
    """
    phase: float = 0.0
    amplitude: float = 1.0
    frequency: float = 1.0

    def modulate(self, value: float) -> float:
        """
        Apply spiral modulation to a scalar value.

        Parameters
        ----------
        value : float
            Input value to modulate.

        Returns
        -------
        float
            Modulated output.
        """
        modulation = self.amplitude * np.sin(self.frequency * self.phase)
        return value + modulation

    def advance(self, step: float = 0.1) -> None:
        """Advance the spiral phase."""
        self.phase = (self.phase + step) % (2 * np.pi)


@dataclass
class ModulatedRing:
    """
    A ring structure with spiral modulation applied to its operations.

    This is a conceptual building block for algebraic structures that
    evolve through helical refinement cycles rather than static rules.
    """
    elements: list
    operator: SpiralOperator

    def spiral_add(self, a: float, b: float) -> float:
        """Addition modulated by current spiral phase."""
        raw = a + b
        return self.operator.modulate(raw)

    def spiral_multiply(self, a: float, b: float) -> float:
        """Multiplication modulated by current spiral phase."""
        raw = a * b
        return self.operator.modulate(raw)


@dataclass
class HelicalField:
    """
    A field-like structure whose operations are modulated by a spiral operator.

    Useful for representing geometric or transformation spaces that benefit
    from iterative helical refinement between exploration and precision.
    """
    base_field: Callable
    spiral_operator: SpiralOperator

    def apply(self, x: np.ndarray) -> np.ndarray:
        """Apply the helical field transformation."""
        raw = self.base_field(x)
        modulated = np.vectorize(self.spiral_operator.modulate)(raw)
        return modulated

    def refine(self, x: np.ndarray, steps: int = 3) -> np.ndarray:
        """
        Perform multiple refinement passes with advancing spiral phase.

        This is the core "spiral refinement" pattern.
        """
        result = x.copy()
        for _ in range(steps):
            result = self.apply(result)
            self.spiral_operator.advance(0.3)
        return result