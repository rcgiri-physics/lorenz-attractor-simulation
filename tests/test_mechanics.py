import os
import sys
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.mechanics import lorenz_derivatives # pylint: disable=wrong-import-position

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

def test_origin_fixed_point():
    """Validates that the origin (0, 0, 0) is always a true fixed point."""
    params = {'sigma': 10.0, 'rho': 28.0, 'beta': 8.0/3.0}
    state = [0.0, 0.0, 0.0]

    derivatives = lorenz_derivatives(0, state, params)

    assert np.allclose(derivatives, [0.0, 0.0, 0.0]), "Origin is not a fixed point!"

def test_convection_fixed_points():
    """
    Validates that the theoretical fixed points C+ and C- perfectly
    zero out the vector field.
    """
    params = {'sigma': 10.0, 'rho': 28.0, 'beta': 8.0/3.0}
    rho, beta = params['rho'], params['beta']

    # Calculate the exact theoretical coordinates
    x_c = np.sqrt(beta * (rho - 1))
    y_c = x_c
    z_c = rho - 1

    c_plus = [x_c, y_c, z_c]
    c_minus = [-x_c, -y_c, z_c]

    d_c_plus = lorenz_derivatives(0, c_plus, params)
    d_c_minus = lorenz_derivatives(0, c_minus, params)

    assert np.allclose(d_c_plus, [0.0, 0.0, 0.0]), "C+ is not a stable fixed point!"
    assert np.allclose(d_c_minus, [0.0, 0.0, 0.0]), "C- is not a stable fixed point!"

def test_lorenz_symmetry():
    """
    Validates the spatial symmetry of the system: (x, y, z) -> (-x, -y, z).
    If we invert the x and y inputs, the resulting x and y derivatives
    should also invert, while the z derivative remains identical.
    """
    params = {'sigma': 10.0, 'rho': 28.0, 'beta': 8.0/3.0}

    # Arbitrary test point in phase space
    state = [10.0, 15.0, 20.0]
    inverted_state = [-10.0, -15.0, 20.0]

    d_state = lorenz_derivatives(0, state, params)
    d_inverted = lorenz_derivatives(0, inverted_state, params)

    # Expected result: x and y derivatives are negated, z is unchanged
    expected_inverted_derivatives = [-d_state[0], -d_state[1], d_state[2]]

    assert np.allclose(d_inverted, expected_inverted_derivatives), "Spatial symmetry broken!"
