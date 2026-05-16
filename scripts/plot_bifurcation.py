import os
import sys

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.signal import find_peaks

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.mechanics import lorenz_derivatives # pylint: disable=wrong-import-position

def compute_bifurcation():
    """Sweeps the Rayleigh parameter and plots the local maxima of z."""

    # We will sweep rho from 0 to 40.
    # (Chaos technically starts around 24.74)
    rho_values = np.linspace(0, 40, 400)

    # Lists to store the scatter plot data
    rho_scatter = []
    z_scatter = []

    params = {'sigma': 10.0, 'beta': 8.0/3.0}
    initial_state = [1.0, 1.0, 1.0]

    # We need a long t_span to let transients decay,
    # but we only save the second half of the data
    t_span = (0, 50)
    t_eval = np.linspace(0, 50, 5000)

    print("Computing Lorenz Bifurcation Diagram... This may take a minute or two.")

    for rho in rho_values:
        params['rho'] = rho

        sol = solve_ivp(
            lorenz_derivatives, t_span, initial_state,
            args=(params,), method='RK45', t_eval=t_eval,
            rtol=1e-6, atol=1e-8
        )

        # Discard the first 50% of the data (Transient removal)
        transient_cutoff = len(sol.t) // 2
        z_steady_state = sol.y[2][transient_cutoff:]

        # Find local maxima (peaks) in the steady state z-data
        peaks, _ = find_peaks(z_steady_state)
        z_maxima = z_steady_state[peaks]

        # Store the data for plotting
        for z_max in z_maxima:
            rho_scatter.append(rho)
            z_scatter.append(z_max)

        # Optional: Print progress so you know it hasn't frozen
        if int(rho) % 10 == 0 and rho == int(rho):
            print(f"Sweeping rho = {int(rho)}/40...")

    # Plotting
    __fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
    ax.scatter(rho_scatter, z_scatter, s=0.5, color='black', alpha=0.5)

    ax.set_title("Lorenz Attractor: Bifurcation Diagram (Local Maxima of $z$)", fontsize=14, fontweight='bold')
    ax.set_xlabel("Rayleigh Number ($\\rho$)", fontsize=12)
    ax.set_ylabel("Local Maxima of $z$", fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.5)

    os.makedirs('data/analysis', exist_ok=True)
    filepath = 'data/analysis/lorenz_bifurcation.png'
    plt.savefig(filepath, bbox_inches='tight')
    print(f"Saved bifurcation diagram to {filepath}")

    plt.show()

if __name__ == "__main__":
    compute_bifurcation()
