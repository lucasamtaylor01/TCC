import numpy as np
from scipy.integrate import solve_ivp
import pandas as pd
from pathlib import Path


# REVISARRRR

vector_a = [1, 1, 3]
vector_b = [
    0.5 * (vector_a[0] - vector_a[1] - vector_a[2]),
    0.5 * (vector_a[1] - vector_a[2] - vector_a[0]),
    0.5 * (vector_a[2] - vector_a[0] - vector_a[1]),
]
c = np.sqrt(3 / 4)
vector_h = [-1, 0, 0]
vector_f = [0.327, 0, 0]
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
            vector_a[i] * vector_b[i] * x[j] * x[k]
            - c * (vector_a[i] - vector_a[k]) * x[j] * y[k]
            + c * (vector_a[i] - vector_a[k]) * x[j] * y[k]
            - c * (vector_a[i] - vector_a[j]) * y[j] * x[k]
            - 2 * c**2 * y[i] * y[k]
            - nu_0 * vector_a[i] ** 2 * x[i]
            + vector_a[i] * y[i]
            - vector_a[i] * z[i]
        ) / vector_a[i]
        dy[i] = (
            -vector_a[k] * vector_b[k] * x[j] * y[k]
            - vector_a[j] * vector_b[j] * y[j] * x[k]
            + c * (vector_a[k] - vector_a[j]) * y[j] * y[k]
            - vector_a[i] * x[i]
            - nu_0 * vector_a[i] ** 2 * y[i]
        ) / vector_a[i]
        dz[i] = (
            -vector_b[k] * x[j] * (z[k] - vector_h[k])
            - vector_b[j] * (z[j] - vector_h[j]) * x[k]
            + c * y[j] * (z[k] - vector_h[k])
            - c * (z[j] - vector_h[j]) * y[k]
            + g_0 * vector_a[i] * x[i]
            - kappa_0 * vector_a[i] * z[i]
            + vector_f[i]
        )
    return np.concatenate([dx, dy, dz])

def simulate(x_initial, y_initial, z_initial, days):
    initial_state = np.concatenate([x_initial, y_initial, z_initial])
    t_final = days * 8
    t_span = (0, t_final)
    t_eval = np.linspace(0, t_final, int(t_final * 24))
    sol = solve_ivp(pe_model, t_span, initial_state, t_eval=t_eval, method="RK45", atol=1e-8, rtol=1e-6)
    return sol.t / 8, sol.y[:3].T, sol.y[3:6].T, sol.y[6:].T

# DIAS AQUI!!!!!!!1
hadley01_days = 400

y1 = (vector_f[0] / vector_a[1]) * nu_0 * (1 + vector_a[1] * g_0 + (nu_0**2) * (vector_a[1] ** 2))
z1 = (1 + (nu_0**2) * (vector_a[1] ** 2)) * y1
x1 = -nu_0 * vector_a[1] * y1

hadley01_initial_x = [x1, 0, 0]
hadley01_initial_y = [y1, -(10 ** (-5)), 0]
hadley01_initial_z = [z1, 10 ** (-5), 0]

t_hadley01, x_hadley01, y_hadley01, z_hadley01 = simulate(
    hadley01_initial_x, hadley01_initial_y, hadley01_initial_z, hadley01_days
)

x = np.asarray(x_hadley01)
y = np.asarray(y_hadley01)
z = np.asarray(z_hadley01)
t = np.squeeze(np.asarray(t_hadley01))

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
out_file = DATADIR / "python0327.csv"
df.to_csv(out_file, index=False)

print(f"CSV salvo em: {out_file}")
