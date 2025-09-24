import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp
from pathlib import Path

eps = 0.01
lam = 1.0

def rhs(t, u):
    x, y1, y2, y3 = u
    dx = x - x**3 + (lam/eps) * y2
    dy1 = (10 / eps**2) * (y2 - y1)
    dy2 = (1 / eps**2) * (28*y1 - y2 - y1*y3)
    dy3 = (1 / eps**2) * (y1*y2 - (8/3)*y3)
    return [dx, dy1, dy2, dy3]

t0, tf = 0.0, 10.0
y0 = [0.1, 0.01, 0.01, 0.01]
t_eval = np.arange(t0, tf + 1e-12, 1e-3)

sol = solve_ivp(rhs, (t0, tf), y0, method="RK45", t_eval=t_eval, rtol=1e-6, atol=1e-7)

x_vals = sol.y[0]
y2_vals = sol.y[2]

BASE = Path(__file__).resolve().parent if "__file__" in globals() else Path(".")
DATADIR = BASE / "data"
DATADIR.mkdir(parents=True, exist_ok=True)

df = pd.DataFrame({"t": sol.t, "y2": y2_vals, "x": x_vals})
df.to_csv(DATADIR / "deterministico.csv", index=False)
