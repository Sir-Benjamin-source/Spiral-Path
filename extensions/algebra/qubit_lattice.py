"""
Qubit lattice mapping primitives with spiral modulation.

This module provides lightweight lattice structures for representing
and transforming qubit states using spiral-modulated coupling.

These are conceptual and structural primitives, not a full quantum
simulation engine. They are designed to be composable with the
Spiral Algebra Engine and higher-level geometric reasoning systems.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import numpy as np

from .core import SpiralOperator


@dataclass
class LatticeNode:
    """
    A single node in a qubit lattice.

    Represents a localized qubit or small cluster with associated
    spiral-modulated state information.
    """
    qubit_id: str
    state_vector: np.ndarray
    local_phase: float = 0.0
    metadata: Dict = field(default_factory=dict)

    def apply_local_modulation(self, operator: SpiralOperator) -> None:
        """Apply spiral modulation directly to this node's state."""
        modulated = np.vectorize(operator.modulate)(self.state_vector)
        self.state_vector = modulated
        operator.advance(0.15)


@dataclass
class SpiralCoupling:
    """
    Spiral-modulated coupling between lattice nodes.

    The coupling strength varies with the global spiral phase,
    allowing entanglements to strengthen and weaken rhythmically.
    """
    source_id: str
    target_id: str
    base_strength: float
    spiral_operator: SpiralOperator

    def effective_strength(self) -> float:
        """Return current coupling strength after spiral modulation."""
        modulation = 0.5 + 0.5 * np.sin(self.spiral_operator.phase)
        return self.base_strength * modulation


@dataclass
class QubitLattice:
    """
    A lattice of qubits with spiral-modulated couplings.

    This is the core data structure for spiral-modulated qubit mapping.
    It supports construction of lattice topologies and iterative
    refinement through helical coupling cycles.
    """
    nodes: Dict[str, LatticeNode] = field(default_factory=dict)
    couplings: List[SpiralCoupling] = field(default_factory=list)
    global_spiral: SpiralOperator = field(default_factory=SpiralOperator)

    def add_node(self, node: LatticeNode) -> None:
        """Add a qubit node to the lattice."""
        self.nodes[node.qubit_id] = node

    def add_coupling(self, coupling: SpiralCoupling) -> None:
        """Add a spiral-modulated coupling between two nodes."""
        self.couplings.append(coupling)

    def step(self, steps: int = 1) -> None:
        """
        Advance the lattice by one or more refinement steps.

        Each step applies local modulation to nodes and updates
        effective coupling strengths.
        """
        for _ in range(steps):
            for node in self.nodes.values():
                node.apply_local_modulation(self.global_spiral)
            self.global_spiral.advance(0.2)

    def get_lattice_summary(self) -> Dict:
        """Return a lightweight summary of the current lattice state."""
        return {
            "num_nodes": len(self.nodes),
            "num_couplings": len(self.couplings),
            "global_phase": self.global_spiral.phase,
            "node_ids": list(self.nodes.keys()),
        }