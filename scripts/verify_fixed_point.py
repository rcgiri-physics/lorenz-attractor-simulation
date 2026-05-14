import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Ensure Python can find your 'src' module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.mechanics import lorenz_derivatives

if __name__ == "__main__":
    # Standard Prandtl and geometric factors, but a LOW Rayleigh number
    params = {'sigma': 10.0, 'rho': 10.0, 'beta': 8.0/3.0}

    # Start somewhere slightly off-center
    initial_state = [1.0, 1.0, 1.0]

    t_span = (0, 20)
    t_eval = np.linspace(t_span[0], t_span[1], 2000)

    print("Integrating Lorenz equations at stable regime (rho=10)...")
    sol = solve_ivp(
        lorenz_derivatives, t_span, initial_state,
        args=(params,), method='RK45', t_eval=t_eval,
        rtol=1e-8, atol=1e-10
    )

    # Plotting x, y, and z over time to watch them settle
    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
    ax.plot(sol.t, sol.y[0], label='x (Convection)', color='royalblue')
    ax.plot(sol.t, sol.y[1], label='y (Horiz. Temp)', color='crimson')
    ax.plot(sol.t, sol.y[2], label='z (Vert. Temp)', color='forestgreen')

    ax.set_title("Lorenz System: Settling to a Fixed Point ($\\rho = 10$)", fontsize=14, fontweight='bold')
    ax.set_xlabel("Time", fontsize=12)
    ax.set_ylabel("State Variables", fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend()

    os.makedirs('data/analysis', exist_ok=True)
    plt.savefig('data/analysis/fixed_point_rho10.png', bbox_inches='tight')
    print("Saved plot to data/analysis/fixed_point_rho10.png")

    plt.show()

