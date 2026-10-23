"""physverify spec for the Lorenz system in src/mechanics.py.

    physverify run tests/verify_lorenz.py

The reference equations are written from Lorenz (1963):

    dx/dt = sigma (y - x)
    dy/dt = rho x - y - x z
    dz/dt = -beta z + x y

with sigma = 10, rho = 28, beta = 8/3. The project has no fixed-step solver of
its own (the scripts call SciPy's solve_ivp), so lorenz_derivatives is stepped
with physverify's RK4 and the order studies expect 4: they check the equations,
not SciPy.

What is checked:
- lorenz_derivatives: manufactured solution, reference solution up to t = 1
  (before chaos amplifies differences much), whole trajectory, exact patch test
  (at 4 to 32 steps, where round-off stays near 1e-12).
- The fixed points (0, 0, 0) and (+-sqrt(beta (rho - 1)), +-sqrt(beta (rho - 1)), rho - 1)
  are zeros of lorenz_derivatives, also at rho = 10 (scripts/verify_fixed_point.py).
- The divergence of the field is -(sigma + 1 + beta) everywhere.
- The hand-written Jacobian in scripts/calculate_lyapunov.py is the derivative
  of lorenz_derivatives.
- The Lyapunov exponents from the script's extended_system sum to the trace
  -(sigma + 1 + beta), as the README states (short run of 20 time units).
"""
# pylint: disable=import-error,wrong-import-position,missing-function-docstring

import importlib.util
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from physverify import Check, ManufacturedODE, Result, ode_checks, patch_study
from physverify.steppers import integrate_fixed, rk4
from src.mechanics import lorenz_derivatives

SIGMA, RHO, BETA = 10.0, 28.0, 8.0 / 3.0
PARAMS = {"sigma": SIGMA, "rho": RHO, "beta": BETA}
Y0 = np.array([1.0, 1.0, 1.0])
T_END = 1.0
NS = (100, 200, 400, 800)


def _load_script(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def reference_rhs(_t, state, sigma=SIGMA, rho=RHO, beta=BETA):
    x, y, z = state
    return np.array([sigma * y - sigma * x, rho * x - y - x * z, x * y - beta * z])


def integrate(source, y0, t_end, n, trajectory=False):
    def rhs(t, y):
        return np.asarray(lorenz_derivatives(t, y, PARAMS), dtype=float) + source(t)

    if not trajectory:
        return integrate_fixed(rhs, y0, 0.0, t_end, n, rk4)
    h = t_end / n
    y = np.array(y0, dtype=float)
    states = [y]
    for i in range(n):
        y = rk4(rhs, i * h, y, h)
        states.append(y)
    return np.array(states)


def manufactured(t):
    return np.array([np.sin(1.1 * t) + 0.5, 0.8 * np.cos(0.9 * t), 2.0 + 0.3 * np.sin(1.7 * t)])


def fixed_points():
    worst = 0.0
    for rho in (RHO, 10.0):
        c = np.sqrt(BETA * (rho - 1.0))
        params = {"sigma": SIGMA, "rho": rho, "beta": BETA}
        for p in ([0.0, 0.0, 0.0], [c, c, rho - 1.0], [-c, -c, rho - 1.0]):
            worst = max(worst, float(np.max(np.abs(lorenz_derivatives(0.0, np.array(p), params)))))
    if worst <= 1e-12:
        return Result("EXACT", f"all six fixed points (rho = 28 and 10) are zeros (largest |f| {worst:.1e})")
    return Result("FAIL", f"a fixed point is not a zero of the field: |f| = {worst:.3g}")


def _fd_jacobian(state, h=1e-6):
    jac = np.zeros((3, 3))
    for k in range(3):
        e = np.zeros(3)
        e[k] = h
        jac[:, k] = (np.asarray(lorenz_derivatives(0, state + e, PARAMS)) -
                     np.asarray(lorenz_derivatives(0, state - e, PARAMS))) / (2 * h)
    return jac


def _states():
    rng = np.random.default_rng(3)
    return [rng.uniform([-20, -25, 0], [20, 25, 50]) for _ in range(20)]


def divergence():
    worst = max(abs(np.trace(_fd_jacobian(s)) + SIGMA + 1.0 + BETA) for s in _states())
    if worst <= 1e-6:
        return Result("PASS", f"div f = -(sigma + 1 + beta) at 20 states (largest difference {worst:.1e})")
    return Result("FAIL", f"divergence differs from -(sigma + 1 + beta) by {worst:.3g}")


def jacobian_matches():
    lyap = _load_script("calculate_lyapunov")
    worst = max(float(np.max(np.abs(lyap.lorenz_jacobian(s, PARAMS) - _fd_jacobian(s)))) for s in _states())
    if worst <= 1e-6:
        return Result("PASS", f"matches the finite-difference derivative at 20 states (largest difference {worst:.1e})")
    return Result("FAIL", f"lorenz_jacobian differs from the derivative of the field by {worst:.3g}")


def lyapunov_sum():
    """Benettin's QR method with the script's extended_system, over 20 time units on the attractor."""
    lyap = _load_script("calculate_lyapunov")
    state = solve_ivp(lorenz_derivatives, (0, 50), Y0, args=(PARAMS,), method="DOP853", rtol=1e-10, atol=1e-12).y[:, -1]
    ext = np.concatenate([state, np.eye(3).ravel()])
    sums = np.zeros(3)
    t_step, steps = 0.1, 200
    for _ in range(steps):
        sol = solve_ivp(lyap.extended_system, (0, t_step), ext, args=(PARAMS,), method="DOP853", rtol=1e-10, atol=1e-12)
        q, r = np.linalg.qr(sol.y[3:, -1].reshape(3, 3))
        sums += np.log(np.abs(np.diag(r)))
        ext = np.concatenate([sol.y[:3, -1], q.ravel()])
    total = float(np.sum(sums)) / (steps * t_step)
    trace = -(SIGMA + 1.0 + BETA)
    if abs(total - trace) <= 1e-6:
        return Result("PASS", f"sum of exponents {total:.7f}, trace {trace:.7f}")
    return Result("FAIL", f"sum of exponents {total:.7f} differs from the trace {trace:.7f}")


def checks():
    """The checks physverify runs."""
    out = ode_checks(
        "lorenz_derivatives + physverify RK4",
        integrate,
        rhs_ref=reference_rhs,
        mms=ManufacturedODE(manufactured, reference_rhs),
        y0_free=Y0,
        t_end=T_END,
        ns=NS,
        order=4.0,
        integrate_trajectory=lambda s, y0, t, n: integrate(s, y0, t, n, trajectory=True),
    )
    # Coarse steps for the patch test: at 800 steps the accumulated round-off reaches 1e-10.
    patch_args = (integrate, reference_rhs, np.array([0.5, -0.3, 2.0]), np.array([1.0, 0.4, -0.7]),
                  T_END, (4, 8, 16, 32))
    return out + [
        Check("patch", "lorenz_derivatives + physverify RK4", lambda: patch_study(*patch_args)),
        Check("limit", "fixed points are zeros of lorenz_derivatives", fixed_points),
        Check("invariant", "phase-space contraction rate -(sigma + 1 + beta)", divergence),
        Check("limit", "calculate_lyapunov.lorenz_jacobian is the derivative of the field", jacobian_matches),
        Check("invariant", "Lyapunov exponents sum to the trace", lyapunov_sum),
    ]
