"""Peak models and diffusion models used for fitting."""

from scipy.special import erf
import numpy as np
from scipy.integrate import solve_ivp


def Diffusion_Erf_Model(pars, x, y, residual_func=False):
    """Diffusion profile c(x) = A (1 - erf(x / (2 sqrt(D t)))) (constant surface concentration).
    pars = lmfit Parameters D (diffusion coefficient), t (time), A (scaling factor), x = depth, y = measured profile;
    residual_func = True -> model - y (for lmfit), else the model. Units of D, t and x must match (e.g. nm^2/s, s, nm)."""
    D = pars['D'].value # D is the diffusion coefficient # the value of the entry "D" in the dictionary pars is used as D
    t = pars['t'].value # t is the time
    A = pars['A'].value # A is a scaling factor

    y_model = A * (1 - erf(x / (2 * np.sqrt(D * t))))

    if residual_func is True:    # If Z_real_imag_measurement=None is set, the model data is returned instead of the residuals
        return y_model - y
    else:
        return y_model


def Step_Function_Initial_Condition(x, y_data):
    """Start profile for the diffusion simulation: the first measured value at x = 0, zero everywhere else.
    x = depth values, y_data = measured profile (series)."""
    x = np.asarray(x)
    #return np.where(x == 0, 1, 0)
    return np.where(x == 0, y_data.iloc[0], 0)


def Diffusion_Model_Concentration_Dependent(t, c, D0, alpha, dx):
    """Right-hand side for solve_ivp: dc/dt = D(c) * d2c/dx2 with D(c) = D0 (1 + alpha c) (finite differences, both end points constant).
    t = time, c = concentration profile, D0, alpha = model parameters, dx = depth step."""
    dcdt = np.zeros_like(c)  # Array for the time derivative of the concentration
    D = D0 * (1 + alpha * c)  # Concentration dependent diffusion coefficient
    dcdt[1:-1] = D[1:-1] * (c[2:] - 2*c[1:-1] + c[:-2]) / dx**2  # diffusion equation (finite difference form)
    return dcdt


def Solve_Diffusion(D0, alpha, T, c0, dx):
    """Concentration profile after the time T, solved with solve_ivp from the start profile c0.
    D0, alpha = model parameters, T = time, c0 = start profile, dx = depth step. Returns the profile at T."""
    sol = solve_ivp(Diffusion_Model_Concentration_Dependent, [0, T], c0, args=(D0, alpha, dx), t_eval=[T])  # Solve the PDE with the initial condition C0
    return sol.y[:, -1]


def Objective_Diffusion_Fit(params, C_exp, T, c0, dx):
    """Sum of squared differences between the simulated profile (Solve_Diffusion) and the measured profile C_exp, for scipy.optimize.
    params = [D0, alpha], T, c0, dx as in Solve_Diffusion."""
    D0, alpha = params  # Parameters of the diffusion model
    C_sim = Solve_Diffusion(D0, alpha, T, c0, dx)  # simulated concentration
    return np.sum((C_sim - C_exp)**2)
