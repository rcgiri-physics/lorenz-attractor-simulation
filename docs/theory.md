# Theoretical Foundation: The Lorenz System

## 1. Physical Origin: Rayleigh-Bénard Convection
The Lorenz equations (1963) are a highly simplified mathematical model for atmospheric convection. They describe a 2D fluid cell being heated from below and cooled from above. 

The variables $x, y, z$ do **not** represent 3D spatial coordinates. Instead, they represent macroscopic physical state variables of the fluid:
* **$x$**: The rate of convective overturning (how fast the fluid is spinning).
* **$y$**: The horizontal temperature variation across the convection cell.
* **$z$**: The vertical temperature variation (deviation from a linear temperature gradient).

## 2. The Governing Equations
The system is defined by three coupled, non-linear ordinary differential equations:
$$\dot{x} = \sigma (y - x)$$
$$\dot{y} = x (\rho - z) - y$$
$$\dot{z} = xy - \beta z$$

### System Parameters
* **$\sigma$ (Prandtl Number):** The ratio of fluid momentum diffusivity (viscosity) to thermal diffusivity. Historically set to $10$.
* **$\rho$ (Rayleigh Number):** The normalized temperature difference driving the convection. This is our primary bifurcation parameter.
* **$\beta$ (Geometric Factor):** The physical aspect ratio of the convection rolls. Historically set to $8/3$.

## 3. Dissipation and Phase Space Volume Contraction
Unlike Hamiltonian systems (e.g., the frictionless double pendulum) where phase space volume is strictly conserved (Liouville's Theorem), the Lorenz system is deeply dissipative.

We can prove this by calculating the divergence of the vector field $\mathbf{V} = (\dot{x}, \dot{y}, \dot{z})$:
$$\nabla \cdot \mathbf{V} = \frac{\partial \dot{x}}{\partial x} + \frac{\partial \dot{y}}{\partial y} + \frac{\partial \dot{z}}{\partial z}$$
$$\nabla \cdot \mathbf{V} = (-\sigma) + (-1) + (-\beta) = -(\sigma + 1 + \beta)$$

Since $\sigma, \beta > 0$, the divergence is strictly negative. For standard parameters ($\sigma=10, \beta=8/3$), the divergence is $\approx -13.67$. This means any initial volume of initial conditions in phase space shrinks exponentially toward zero, eventually collapsing onto a manifold of dimension less than 3—the **Strange Attractor**.

## 4. Equilibria (Fixed Points)
By setting $\dot{x} = \dot{y} = \dot{z} = 0$, we find the system's equilibrium points:
1.  **The Origin (Conduction state):** $(0, 0, 0)$. Stable for $\rho < 1$.
2.  **Convection Rolls ($C^+$ and $C^-$):** $(\pm \sqrt{\beta(\rho-1)}, \pm \sqrt{\beta(\rho-1)}, \rho-1)$. These emerge when $\rho > 1$ and become unstable via a subcritical Hopf bifurcation at $\rho \approx 24.74$, unleashing chaos.