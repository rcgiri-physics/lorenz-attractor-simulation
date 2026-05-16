import os
import sys
import numpy as np
from scipy.integrate import solve_ivp

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.mechanics import lorenz_derivatives # pylint: disable=wrong-import-position

def lorenz_jacobian(state, params):
    """Calculates the Jacobian matrix of the Lorenz system."""
    x, y, z = state
    sigma, rho, beta = params['sigma'], params['rho'], params['beta']

    return np.array([
        [-sigma,  sigma,  0],
        [rho - z, -1,    -x],
        [y,       x,     -beta]
    ])

def extended_system(_t, state_ext, params):
    """Integrates the state and the perturbation matrix simultaneously."""
    # Unpack state (first 3) and perturbation matrix W (next 9)
    state = state_ext[:3]
    w_matrix = state_ext[3:].reshape((3, 3))

    # Core derivatives
    d_state = lorenz_derivatives(0, state, params)

    # Perturbation derivatives: dW/dt = J * W
    jacobian = lorenz_jacobian(state, params)
    d_w_matrix = np.dot(jacobian, w_matrix)

    # Flatten back to a 12-element array
    return np.concatenate((d_state, d_w_matrix.flatten()))

def calculate_lyapunov():
    """Calculates the Lyapunov Exponents using continuous QR decomposition."""
    params = {'sigma': 10.0, 'rho': 28.0, 'beta': 8.0/3.0}

    # Initialize state and an Identity matrix for perturbations
    state = np.array([1.0, 1.0, 1.0])
    w_matrix = np.eye(3)
    initial_ext = np.concatenate((state, w_matrix.flatten()))

    t_step = 0.1
    total_steps = 10000

    # Array to accumulate the log of orthogonal expansion factors
    lyapunov_sums = np.zeros(3)

    print("Calculating Lyapunov Exponents (Benettin's Algorithm)...")

    current_ext = initial_ext
    for step in range(1, total_steps + 1):
        t_span = (0, t_step)

        # Integrate forward by one small time step
        sol = solve_ivp(extended_system, t_span, current_ext, args=(params,), method='RK45')

        # Extract new state and new W matrix
        new_state = sol.y[:3, -1]
        new_w_matrix = sol.y[3:, -1].reshape((3, 3))

        # Gram-Schmidt Orthogonalization via QR decomposition
        q_matrix, r_matrix = np.linalg.qr(new_w_matrix)

        # Accumulate the log of the diagonal of R (the expansion rates)
        lyapunov_sums += np.log(np.abs(np.diag(r_matrix)))

        # Reset W to the orthogonal Q matrix for the next step
        current_ext = np.concatenate((new_state, q_matrix.flatten()))

        if step % 2000 == 0:
            print(f"Step {step}/{total_steps} completed...")

    # Average over total time to get the final exponents
    total_time = total_steps * t_step
    lyapunov_exponents = lyapunov_sums / total_time

    print("\n--- Final Lyapunov Exponents ---")
    print(f"Lambda 1 (Chaos):      {lyapunov_exponents[0]:.4f}")
    print(f"Lambda 2 (Neutral):    {lyapunov_exponents[1]:.4f}")
    print(f"Lambda 3 (Contraction):{lyapunov_exponents[2]:.4f}")

    divergence = np.sum(lyapunov_exponents)
    expected_div = -(params['sigma'] + 1 + params['beta'])
    print(f"\nSum of Exponents: {divergence:.4f} (Expected: {expected_div:.4f})")

if __name__ == "__main__":
    calculate_lyapunov()
