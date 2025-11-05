"""Spiral Path Tricorder: Exports core scan func and SpiralPath class stub."""

from .core import tricorder_scan
from .main import main as tricorder_cli

# Stub for SpiralPath class (extend later for full framework)
class SpiralPath:
    """Placeholder for Spiral Path eq wrapper."""
    def __init__(self, alpha=0.7, beta=0.3):
        self.alpha = alpha
        self.beta = beta

__all__ = ['tricorder_scan', 'tricorder_cli', 'SpiralPath']
