# Lorenz Attractor Simulation: Dissipative Chaos

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-Vectorized-013243?style=flat&logo=numpy&logoColor=white)
![SciPy](https://img.shields.io/badge/SciPy-Validation-8CAAE6?style=flat&logo=scipy&logoColor=white)
![LaTeX](https://img.shields.io/badge/LaTeX-Documentation-008080?style=flat)

This repository serves as a numerical laboratory for exploring continuous 3D dissipative chaos. Modeling the Rayleigh-Bénard convection equations, this project visualizes phase space volume contraction, Hopf bifurcations, and the topological bounds of the canonical "Butterfly" strange attractor.

## Repository Focus
Transitioning from conservative Hamiltonian systems, this project utilizes high-order numerical integration to explore non-linear systems where energy is continuously injected and dissipated, forcing infinite trajectories to collapse onto fractal topological manifolds.

## Current Validation: Phase Space Contraction
Before exploring the chaotic regime, the engine's dissipative accuracy was validated below the critical Rayleigh threshold ($\rho < 24.74$). At $\rho = 10$, the system rapidly sheds energy and the initial transient oscillations collapse perfectly into a stable equilibrium (fixed point).

![Fixed Point Validation](data/analysis/fixed_point_rho10.png)

## Phase 2: The Strange Attractor
Transitioning the Rayleigh parameter into the chaotic regime ($\rho = 28$) shatters the stable equilibria. The system continuously evolves along a bounded, non-intersecting fractal manifold, tracing the iconic 3D "Butterfly" wings.

![Lorenz Butterfly](data/trajectories/lorenz_butterfly_3d.png)

## Phase 3: Bifurcation & The Transition to Chaos
By sweeping the Rayleigh number ($\rho$) from 0 to 40 and plotting the local maxima of the $z$-coordinate, we can visualize the exact moment of the subcritical Hopf bifurcation ($\rho \approx 24.74$). The system transitions instantly from a predictable, stable equilibrium into aperiodic chaotic oscillation.

![Bifurcation Diagram](data/analysis/lorenz_bifurcation.png)

## Phase 4: Chaos Quantification
Utilizing continuous QR decomposition via Benettin's algorithm on the system's Jacobian, the spectrum of Lyapunov exponents was extracted as $\lambda = [0.8948, 0.0005, -14.5620]$ (DOP853, rtol $10^{-10}$, transient of 50 time units discarded, average over 1000 time units; the literature value of $\lambda_1$ is about 0.906, and the last digits shift by about 0.01 with the averaging time). The positive maximum exponent ($\lambda_1 > 0$) establishes deterministic chaos. The sum of the exponents ($-13.6667$) matches the trace of the Jacobian, $-(\sigma + 1 + \beta) = -13.6667$, which checks the phase-space contraction rate. An earlier run with SciPy's default tolerances (rtol $10^{-3}$) gave $[0.8885, 0.0031, -14.5549]$; the gap in the sum ($-13.6633$) was solver error.

## Project Roadmap
- [x] **Phase 1:** Core Physics Engine & Fixed-Point Validation
- [x] **Phase 2:** 3D Phase Space Kinematics (The Butterfly Attractor)
- [x] **Phase 3:** 1D Parameter Sweeps & Bifurcation Diagram
- [x] **Phase 4:** Dissipative Chaos Quantification (Lyapunov Exponents)

## Repository Structure
* `src/`: Contains the core non-linear ODEs in `mechanics.py`.
* `scripts/`: Execution scripts for time-series validation, 3D plotting, and bifurcation sweeping.
* `data/`: Output directory for generated phase-space renders and analytical plots.
* `docs/`: Contains formal mathematical derivations (`theory.md`) and the project timeline (`research_journal.md`).

## Mathematical Foundation
The system integrates the following coupled differential equations:
* $\dot{x} = \sigma (y - x)$
* $\dot{y} = x (\rho - z) - y$
* $\dot{z} = xy - \beta z$

*(For full derivations on phase space volume contraction, see `docs/theory.md`)*

## Getting Started

### Installation
```bash
pip install -r requirements.txt