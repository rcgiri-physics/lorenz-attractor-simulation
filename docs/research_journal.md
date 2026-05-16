# Research Journal: Lorenz Attractor Simulation
**Project Focus:** Dissipative Chaos & Bifurcation Analysis

## Log 01: Engine Initialization & Fixed Point Validation
**Phase:** 1
**Objective:** Establish the numerical integration engine and verify non-chaotic dissipative settling.

### 1. Engine Configuration
Implemented the decoupled Lorenz ODEs using `scipy.integrate.solve_ivp`. Because the system is dissipative and naturally bounded, standard `RK45` integration is sufficient for topological mapping, avoiding the strict symplectic requirements of Hamiltonian systems.

### 2. Validation Run ($\rho = 10$)
To verify the engine, we simulated the system below the chaotic threshold ($\rho \approx 24.74$).
* **Parameters:** $\sigma = 10, \rho = 10, \beta = 8/3$
* **Initial State:** Off-center perturbation at $[1.0, 1.0, 1.0]$.
* **Result:** The time-series analysis (`fixed_point_rho10.png`) confirmed that $x$, $y$, and $z$ experience brief transient oscillations before exponentially decaying into flat, stable horizontal lines.
* **Conclusion:** The engine accurately models energy dissipation. The fluid settles into steady convective rolling without chaotic variance.

## Log 02: 3D Phase Space Kinematics & The Strange Attractor
**Phase:** 2
**Objective:** Map the chaotic regime and visualize the fractal "butterfly" manifold.

### 1. The Chaotic Transition
By increasing the Rayleigh number past the critical threshold to $\rho = 28$, the system undergoes a subcritical Hopf bifurcation. The previously stable fixed points ($C^+$ and $C^-$) become unstable, repelling the trajectory rather than attracting it.

### 2. Visualization Results
Integrating the system over $t = 50$ seconds with $10,000$ high-definition steps reveals the canonical dual-lobe structure of the Lorenz attractor.
* **The Dynamics:** The trajectory spirals outward from the center of one unstable lobe until it hits a topological boundary, gets ejected, and is caught by the other lobe.
* **The Topology:** Because the system is deterministic, trajectories can never cross. Because it is dissipative, it is confined to a bounded volume. The result is an infinitely complex, non-repeating fractal shape in 3D phase space.

## Log 03: 1D Parameter Sweeps & The Bifurcation Diagram
**Phase:** 3
**Objective:** Map the critical transition from stable equilibria into dissipative chaos.

### 1. The Parameter Sweep
To visualize the onset of chaos, we swept the Rayleigh parameter ($\rho$) from $0 \to 40$. For each discrete $\rho$ value, the system was integrated over a long time horizon ($t=50$). The initial transient data (the first 50%) was discarded, and the local maxima of the $z$-coordinate were extracted from the steady-state trajectory.

### 2. Analysis of the 1D Map
The resulting bifurcation diagram mathematically visualizes the Hopf bifurcation:
* **Stable Regime ($\rho < 24.74$):** The local maxima form a single, clean curve. The fluid convection settles into a stable, non-fluctuating state.
* **The Chaotic Onset ($\rho \approx 24.74$):** The solid line instantly explodes into a dense, scattered vertical band. This visually proves that the system never settles; instead, it continuously oscillates with aperiodic, unpredictable peak values, bounded only by the global topology of the strange attractor.

## Log 04: Quantification of Chaos (Lyapunov Exponents)
**Phase:** 4
**Objective:** Mathematically verify extreme sensitivity to initial conditions.

### 1. Benettin's Algorithm
To quantify the separation rate of infinitesimally close trajectories, we integrated the extended variational equations (the Jacobian) alongside the main ODEs. By applying continuous QR decomposition over $t=1000$, we extracted the three Lyapunov exponents.

### 2. Results & Proof of Dissipative Chaos
* **$\lambda_1 \approx 0.90$**: The strictly positive maximum exponent confirms chaotic divergence (The Butterfly Effect).
* **$\lambda_2 \approx 0.00$**: The neutral exponent, characteristic of continuous-time autonomous flows.
* **$\lambda_3 \approx -14.57$**: The highly negative exponent forces phase space volume contraction.
* **Validation:** $\sum \lambda_i \approx -13.67$, perfectly matching our analytical divergence calculation from Phase 1.