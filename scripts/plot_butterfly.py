import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Ensure Python can find your 'src' module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.mechanics import lorenz_derivatives

if __name__ == "__main__":
    # The canonical chaotic parameters
    params = {'sigma': 10.0, 'rho': 28.0, 'beta': 8.0/3.0}

    # Standard initial conditions
    initial_state = [1.0, 1.0, 1.0]

    # We run it for 50 seconds to give it plenty of time to trace the wings
    t_span = (0, 50)
    # 10,000 points ensures high-definition, smooth curves
    t_eval = np.linspace(t_span[0], t_span[1], 10000)

    print("Integrating Lorenz equations in chaotic regime (rho=28)...")
    sol = solve_ivp(
        lorenz_derivatives, t_span, initial_state,
        args=(params,), method='RK45', t_eval=t_eval,
        rtol=1e-8, atol=1e-10
    )

    # Initialize the 3D plot
    fig = plt.figure(figsize=(10, 8), dpi=150)
    ax = fig.add_subplot(111, projection='3d')

    # Plot the full continuous trajectory
    ax.plot(sol.y[0], sol.y[1], sol.y[2], color='crimson', lw=0.5, alpha=0.8)

    ax.set_title("The Lorenz Strange Attractor ($\\rho = 28$)", fontsize=16, fontweight='bold')
    ax.set_xlabel("x (Convection)", fontsize=10)
    ax.set_ylabel("y (Horizontal Temp)", fontsize=10)
    ax.set_zlabel("z (Vertical Temp)", fontsize=10)

    # Optional styling: Strip away the background panes for a cleaner, void-like aesthetic
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.grid(True, linestyle='--', alpha=0.3)

    # Adjust initial viewing angle for the best perspective of the "wings"
    ax.view_init(elev=25, azim=-45)

    os.makedirs('data/trajectories', exist_ok=True)
    filepath = 'data/trajectories/lorenz_butterfly_3d.png'
    plt.savefig(filepath, bbox_inches='tight')
    print(f"Saved chaotic 3D phase space plot to {filepath}")

    plt.show()