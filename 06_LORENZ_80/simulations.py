import numpy as np
from scipy.integrate import solve_ivp
import pandas as pd
from pathlib import Path


# REVISARRRR

a = [1, 1, 3]
b = [
    0.5 * (a[0] - a[1] - a[2]),
    0.5 * (a[1] - a[2] - a[0]),
    0.5 * (a[2] - a[0] - a[1]),
]
c = np.sqrt(b[0]*b[1] + b[1]*b[2] + b[2]*b[0])

h = [-1, 0, 0]
f = [0.1, 0, 0]
g_0 = 8
kappa_0 = 1 / 48
nu_0 = kappa_0

def pe_model(t, state):
    x = state[0:3]
    y = state[3:6]
    z = state[6:9]
    dx = np.zeros(3)
    dy = np.zeros(3)
    dz = np.zeros(3)
    for i in range(3):
        j = (i + 1) % 3
        k = (i + 2) % 3
        dx[i] = (
            a[i] * b[i] * x[j] * x[k]
            - c * (a[i] - a[k]) * x[j] * y[k]
            + c * (a[i] - a[k]) * x[j] * y[k]
            - c * (a[i] - a[j]) * y[j] * x[k]
            - 2 * c**2 * y[i] * y[k]
            - nu_0 * a[i] ** 2 * x[i]
            + a[i] * y[i]
            - a[i] * z[i]
        ) / a[i]
        dy[i] = (
            -a[k] * b[k] * x[j] * y[k]
            - a[j] * b[j] * y[j] * x[k]
            + c * (a[k] - a[j]) * y[j] * y[k]
            - a[i] * x[i]
            - nu_0 * a[i] ** 2 * y[i]
        ) / a[i]
        dz[i] = (
            -b[k] * x[j] * (z[k] - h[k])
            - b[j] * (z[j] - h[j]) * x[k]
            + c * y[j] * (z[k] - h[k])
            - c * (z[j] - h[j]) * y[k]
            + g_0 * a[i] * x[i]
            - kappa_0 * a[i] * z[i]
            + f[i]
        )
    return np.concatenate([dx, dy, dz])

def simulate(x0, y0, z0, days): # revisar funcao muita coisa é inutil em rel a tempo
    initial_state = np.concatenate([x0, y0, z0])
    t_final = days * 8
    t_span = (0, t_final)
    t_eval = np.linspace(0, t_final, int(t_final * 24)) 
    sol = solve_ivp(pe_model, t_span, initial_state, t_eval=t_eval, method="RK45", atol=1e-8, rtol=1e-6)
    return sol.t / 8, sol.y[:3].T, sol.y[3:6].T, sol.y[6:].T


days = 400

# HARDLEY
y1 = f[0]/(a[0]*nu_0*(1+a[0]*g_0))
x1 = -nu_0*a[0]*y1
z1 = y1


x0 = [x1, 0, 0]
y0 = [y1, -(10 ** (-5)), 0]
z0 = [z1, 10 ** (-5), 0]

t, x, y, z = simulate(x0, y0, z0, days)

x = np.asarray(x)
y = np.asarray(y)
z = np.asarray(z)
t = np.squeeze(np.asarray(t))

df = pd.DataFrame(
    {
        "time": t,
        "x1": x[:, 0],
        "x2": x[:, 1],
        "x3": x[:, 2],
        "y1": y[:, 0],
        "y2": y[:, 1],
        "y3": y[:, 2],
        "z1": z[:, 0],
        "z2": z[:, 1],
        "z3": z[:, 2],
    }
)

BASE = Path(__file__).resolve().parent
DATADIR = BASE / "data"
DATADIR.mkdir(parents=True, exist_ok=True)
out_file = DATADIR / "python01.csv"
df.to_csv(out_file, index=False)

print(f"CSV salvo em: {out_file}")
