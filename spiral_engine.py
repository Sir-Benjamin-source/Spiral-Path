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
            'base': base,
            'adjustment': adjustment,
            'value': path_value
        })
        return path_value
    
    def simulate_spiral(self, params, iterations=5, sign='+', growth_rate=0.01, noise_level=0.05):
        """
        Multi-cycle simulation with optional growth and stochastic noise.
        Args:
            params (dict): Initial {'td':, 'rf':, 'tw':, 'cir':, 'am':, 'da':}
            iterations (int): Number of cycles
            sign (str): '+' or '-'
            growth_rate (float): Parametric evolution per cycle (default minimal)
            noise_level (float): Std dev for Gaussian noise on params per cycle (default 0 for deterministic).
        Returns:
            list: Path values over iterations
        """
        values = []
        current_params = params.copy()
        for i in range(iterations):
            # Add noise if enabled (jitter key params for realism)
            if noise_level > 0:
                current_params['td'] += np.random.normal(0, noise_level * current_params['td'])
                current_params['da'] += np.random.normal(0, noise_level * current_params['da'])
                # Clamp to positive
                current_params['td'] = max(0.1, current_params['td'])
                current_params['da'] = max(0.1, current_params['da'])
            
            value = self.compute_path(
                current_params['td'], current_params['rf'], current_params['tw'],
                current_params['cir'], current_params['am'], current_params['da'], sign
            )
            values.append(value)
            # Apply growth (subtle spiral expansion)
            current_params['td'] *= (1 + growth_rate)
            current_params['rf'] *= (1 + growth_rate / 2)
        return values
    
    def simulate_spiral_with_indicators(self, params, iterations=5, sign='+', growth_rate=0.01, noise_level=0.05):
        """
        Multi-cycle simulation with detailed path indicators per iteration.
        Returns values and a list of dicts with base, adjustment, value per cycle.
        """
        values = []
        indicators = []
        current_params = params.copy()
        for i in range(iterations):
            if noise_level > 0:
                current_params['td'] += np.random.normal(0, noise_level * current_params['td'])
                current_params['da'] += np.random.normal(0, noise_level * current_params['da'])
                current_params['td'] = max(0.1, current_params['td'])
                current_params['da'] = max(0.1, current_params['da'])
            
            base = (current_params['td'] / current_params['rf']) * current_params['tw'] + (current_params['cir'] * self.sc)
            adjustment = current_params['am'] * current_params['da'] if sign == '+' else -(current_params['am'] * current_params['da'])
            path_value = base + adjustment
            
            indicators.append({
                'cycle': i + 1,
                'base': base,
                'adjustment': adjustment,
                'value': path_value,
                'params': current_params.copy()
            })
            values.append(path_value)
            
            current_params['td'] *= (1 + growth_rate)
            current_params['rf'] *= (1 + growth_rate / 2)
        return values, indicators
    
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
    
    # Simulation (deterministic)
    spiral_values = engine.simulate_spiral(params, iterations=5, noise_level=0)
    print("Deterministic Simulation Values:", spiral_values)
    
    # Stochastic sim
    noisy_values = engine.simulate_spiral(params, iterations=5, noise_level=0.05)
    print("Stochastic Simulation Values:", noisy_values)
    
    # New: Simulation with indicators
    values, indicators = engine.simulate_spiral_with_indicators(params, iterations=5, noise_level=0.05)
    print("Simulation Values:", values)
    print("Path Indicators (Last Cycle):", indicators[-1])
    
    # Viz the noisy one
    engine.visualize_spiral(noisy_values, title='Stochastic Spiral Path')
    
    # Provenance
    print("Provenance Log (last entry):", engine.get_provenance()[-1])
