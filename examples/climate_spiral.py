import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import argparse

# Import the engine
from spiral_engine import SpiralEngine

def spiral_climate_forecast(csv_file=None, num_months=12):
    """
    Spiral forecast on temp time-series: Baseline linear vs. Path-refined with noise.
    """
    # Load or generate toy data (monthly temps, 2020-2025)
    if csv_file:
        df = pd.read_csv(csv_file, parse_dates=['date'], index_col='date')
    else:
        # Toy data: Rising trend with noise
        dates = pd.date_range('2020-01-01', periods=60, freq='M')
        temps = 15 + np.cumsum(np.random.normal(0.05, 0.2, 60)) + np.sin(np.arange(60) * np.pi / 6)  # Trend + seasonal
        df = pd.DataFrame({'temp': temps}, index=dates)
    
    # Baseline: Simple linear regression forecast
    from sklearn.linear_model import LinearRegression
    X_base = np.arange(len(df)).reshape(-1, 1)
    model_base = LinearRegression().fit(X_base, df['temp'])
    forecast_base = model_base.predict(np.arange(len(df), len(df) + num_months).reshape(-1, 1))
    
    # Spiral Refinement: Path cycles on trend params
    engine = SpiralEngine()
    params = {'td': len(df), 'rf': 1.2, 'tw': 3.0, 'cir': 2.5, 'am': 0.15, 'da': np.pi/4}
    spiral_values = engine.simulate_spiral(params, iterations=6, noise_level=0.03, sign='+')
    
    # Apply spirals: Weight trend with cumulative paths + noise bands
    cum_spiral = np.cumsum(spiral_values) / np.sum(spiral_values)
    trend_spiral = np.polyval(np.polyfit(X_base.flatten(), df['temp'], 1), np.arange(len(df), len(df) + num_months))
    forecast_spiral = trend_spiral * cum_spiral[-1] + np.mean(np.random.normal(0, 0.3, num_months))  # Noise for realism
    
    # Metrics: MSE on holdout (last 6 months as "test")
    holdout_start = len(df) - 6
    mse_base = np.mean((df['temp'].iloc[holdout_start:] - model_base.predict(X_base[holdout_start:])) ** 2)
    mse_spiral = np.mean((df['temp'].iloc[holdout_start:] - (trend_spiral[:6] * cum_spiral[-1] + np.random.normal(0, 0.3, 6))) ** 2)
    uplift = (mse_base - mse_spiral) / mse_base * 100
    
    results = {
        'mse_baseline': mse_base,
        'mse_spiral': mse_spiral,
        'uplift_pct': uplift,
        'forecast_base': forecast_base.tolist(),
        'forecast_spiral': forecast_spiral.tolist(),
        'provenance': engine.get_provenance()[-1]
    }
    
    return df, results

def plot_forecast(df, results, num_months=12):
    """Plot baseline vs. spiral forecast with uncertainty bands."""
    future_dates = pd.date_range(df.index[-1] + pd.DateOffset(months=1), periods=num_months, freq='M')
    
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['temp'], label='Historical Temps', color='blue')
    
    # Baseline
    plt.plot(future_dates, results['forecast_base'], label='Linear Baseline', color='red', linestyle='--')
    
    # Spiral with bands (noise std as proxy)
    upper_spiral = np.array(results['forecast_spiral']) + 0.3
    lower_spiral = np.array(results['forecast_spiral']) - 0.3
    plt.fill_between(future_dates, lower_spiral, upper_spiral, alpha=0.3, color='green')
    plt.plot(future_dates, results['forecast_spiral'], label='Spiral Forecast', color='green', linewidth=2)
    
    plt.title('Climate Trend Forecast: Linear vs. Spiral Path')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('climate_spiral_forecast.png', dpi=150)
    plt.show()
    print("Forecast plot saved as climate_spiral_forecast.png")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Spiral Climate Forecaster")
    parser.add_argument('--csv', type=str, help="Path to temp CSV (date,temp columns)")
    parser.add_argument('--months', type=int, default=12, help="Forecast horizon")
    parser.add_argument('--output', type=str, default='climate_results.json', help="Output JSON")
    
    args = parser.parse_args()
    
    df, results = spiral_climate_forecast(args.csv, args.months)
    print(f"Baseline MSE: {results['mse_baseline']:.3f}")
    print(f"Spiral MSE: {results['mse_spiral']:.3f}")
    print(f"Uplift: {results['uplift_pct']:.1f}%")
    
    with open(args.output, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Results saved to {args.output}")
    
    plot_forecast(df, results, args.months)
