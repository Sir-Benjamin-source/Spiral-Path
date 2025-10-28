import numpy as np
import matplotlib.pyplot as plt  # Optional for visualization

class SpiralEngine:
    """
    Core engine for Spiral Theory's Path equation.
    Computes (TD / RF) * TW + (CIR * SC) ± (AM * DA) for iterative spirals.
    """
    
    def __init__(self, sc=1.618):  # Default Spiral Constant: golden ratio φ
        self.sc = sc
        self.log = []  # Provenance tracking: iterations and values
    
    def compute_path(self, td, rf, tw, cir, am, da, sign='+'):
        """
        Single cycle computation.
        Args:
            td (float): Task Density
            rf (float): Refinement Factor
            tw (float): Twist Weight
            cir (float): Cycle Intensity Ratio
            am (float): Adjustment Magnitude
            da (float): Differentiation Angle
            sign (str): '+' for expansive, '-' for convergent
        Returns:
            float: Path value
        """
        base = (td / rf) * tw + (cir * self.sc)
        adjustment = am * da if sign == '+' else -(am * da)
        path_value = base + adjustment
        self.log.append({
            'cycle': len(self.log) + 1,
            'params': {'td': td, 'rf': rf, 'tw': tw, 'cir': cir, 'am': am, 'da': da},
            'sign': sign,
            'value': path_value
        })
        return path_value
    
    def simulate_spiral(self, params, iterations=5, sign='+', growth_rate=0.01):
        """
        Multi-cycle simulation with optional growth (e.g., td *= 1 + growth_rate).
        Args:
            params (dict): Initial {'td':, 'rf':, 'tw':, 'cir':, 'am':, 'da':}
            iterations (int): Number of cycles
            sign (str): '+' or '-'
            growth_rate (float): Parametric evolution per cycle (default minimal)
        Returns:
            list: Path values over iterations
        """
        values = []
        current_params = params.copy()
        for i in range(iterations):
            value = self.compute_path(
                current_params['td'], current_params['rf'], current_params['tw'],
                current_params['cir'], current_params['am'], current_params['da'], sign
            )
            values.append(value)
            # Apply growth (subtle spiral expansion)
            current_params['td'] *= (1 + growth_rate)
            current_params['rf'] *= (1 + growth_rate / 2)
        return values
    
    def visualize_spiral(self, values, title='Spiral Path Evolution'):
        """Optional plot of simulation values."""
        plt.figure(figsize=(8, 5))
        plt.plot(values, marker='o', linewidth=2)
        plt.title(title)
        plt.xlabel('Iteration')
        plt.ylabel('Path Value')
        plt.grid(True, alpha=0.3)
        plt.savefig('spiral_viz.png', dpi=150)
        plt.show()
        print("Viz saved as spiral_viz.png")
    
    def get_provenance(self):
        """Return log for traceability."""
        return self.log

# Quick Demo (run in examples/)
if __name__ == "__main__":
    engine = SpiralEngine()
    params = {'td': 10.0, 'rf': 2.0, 'tw': 5.0, 'cir': 3.0, 'am': 1.0, 'da': 2.0}
    
    # Single cycle
    single_value = engine.compute_path(**params, sign='+')
    print(f"Single Cycle Value (+): {single_value}")
    
    # Simulation
    spiral_values = engine.simulate_spiral(params, iterations=5)
    print("Simulation Values:", spiral_values)
    
    # Viz
    engine.visualize_spiral(spiral_values)
    
    # Provenance
    print("Provenance Log (last entry):", engine.get_provenance()[-1])
