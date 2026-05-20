"""
Basic demonstration of QubitLattice with spiral modulation.

This example shows construction of a small lattice, application
of spiral-modulated couplings, and iterative refinement.

Intended as a minimal working example of the foundational primitives.
"""

import numpy as np
try:
    from algebra.core import SpiralOperator
    from algebra.qubit_lattice import QubitLattice, LatticeNode, SpiralCoupling
except ImportError:
    # Fallback for running directly from the algebra directory
    from core import SpiralOperator
    from qubit_lattice import QubitLattice, LatticeNode, SpiralCoupling


def main():
    print("=== Spiral Algebra Engine — Basic Qubit Lattice Demo ===\n")

    global_spiral = SpiralOperator(phase=0.0, amplitude=0.8, frequency=1.2)

    lattice = QubitLattice(global_spiral=global_spiral)

    q0 = LatticeNode(qubit_id="q0", state_vector=np.array([1.0, 0.0]))
    q1 = LatticeNode(qubit_id="q1", state_vector=np.array([0.0, 1.0]))
    q2 = LatticeNode(qubit_id="q2", state_vector=np.array([0.707, 0.707]))

    lattice.add_node(q0)
    lattice.add_node(q1)
    lattice.add_node(q2)

    c01 = SpiralCoupling(
        source_id="q0",
        target_id="q1",
        base_strength=0.6,
        spiral_operator=global_spiral
    )
    c12 = SpiralCoupling(
        source_id="q1",
        target_id="q2",
        base_strength=0.4,
        spiral_operator=global_spiral
    )

    lattice.add_coupling(c01)
    lattice.add_coupling(c12)

    print("Initial lattice summary:")
    print(lattice.get_lattice_summary())
    print()

    print("Running 5 refinement steps with spiral modulation...\n")
    lattice.step(steps=5)

    print("Final lattice summary:")
    print(lattice.get_lattice_summary())
    print()

    print("Demo complete. The lattice has undergone spiral-modulated refinement.")


if __name__ == "__main__":
    main()