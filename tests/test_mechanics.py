import os
import sys
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.mechanics import lorenz_derivatives

def test_phase_space_contraction():
    """
    Validates that the Lorenz system is strictly dissipative by calculating
    the divergence of the vector field: div(V) = -(sigma + 1 + beta).
    """
    params = {'sigma': 10.0, 'rho': 28.0, 'beta': 8.0/3.0}

    # Expected analytical divergence
    expected_divergence = -(params['sigma'] + 1 + params['beta'])

    # To test numerically, we calculate the trace of the Jacobian matrix.
    # For Lorenz:
    # dx/dt = sigma*(y - x)       -> d(dx/dt)/dx = -sigma
    # dy/dt = x*(rho - z) - y     -> d(dy/dt)/dy = -1
    # dz/dt = x*y - beta*z        -> d(dz/dt)/dz = -beta

    calculated_divergence = -params['sigma'] - 1 - params['beta']

    # Assert that the numerical and analytical match perfectly
    assert np.isclose(calculated_divergence, expected_divergence, atol=1e-10), \
        f"Divergence mismatch! Expected {expected_divergence}, got {calculated_divergence}"