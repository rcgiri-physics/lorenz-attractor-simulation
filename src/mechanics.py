def lorenz_derivatives(_t, state, params):
    """
    Computes the time derivatives for the Lorenz system.

    Parameters:
    t : float : Current time
    state : list or array : Current state [x, y, z]
    params : dict : Dictionary containing 'sigma', 'rho', and 'beta'

    Returns:
    list : Time derivatives [dx/dt, dy/dt, dz/dt]
    """
    x, y, z = state
    sigma = params["sigma"]
    rho = params["rho"]
    beta = params["beta"]

    dxdt = sigma * (y - x)
    dydt = x * (rho - z) - y
    dzdt = x * y - beta * z

    return [dxdt, dydt, dzdt]
