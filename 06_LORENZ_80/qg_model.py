import numpy as np
from scipy.integrate import solve_ivp
import pandas as pd
from pathlib import Path


a = [1, 1, 3]
b = [
    0.5 * (a[0] - a[1] - a[2]),
    0.5 * (a[1] - a[2] - a[0]),
    0.5 * (a[2] - a[0] - a[1]),
]
c = np.sqrt(b[0]*b[1] + b[1]*b[2] + b[2]*b[0])

h = [-1.0, 0.0, 0.0]
F = [0.3027, 0.0, 0.0]
g0 = 8.0
kappa0 = 1/48
nu0 = kappa0               


def eq43_rhs(t, y):
    y = np.asarray(y)
    dy = np.zeros(3)

    for i in range(3):
        j = (i + 1) % 3
        k = (i + 2) % 3

        dy[i] = (g0 * c * (a[k] - a[j]) * y[j] * y[k]
            - a[i] * (a[i] * g0 * nu0 + kappa0) * y[i]
            - c * h[k] * y[j]
            + c * h[j] * y[k]
            + F[i]) / (a[i] * g0 + 1.0)

    return dy

def qgmodel(y0, t_final):
    t_span = (0.0, float(t_final))
    sol = solve_ivp(eq43_rhs, t_span, np.asarray(y0, dtype=float), method="RK45", rtol=1e-6, atol=1e-8)
    return sol.t, sol.y.T  

if __name__ == "__main__":
    y0 = [0.53333, 0, 0]

    t_final = 400*8

    t, Y = qgmodel(y0, t_final)

    Y = np.asarray(Y)
    df = pd.DataFrame(
        {
            "time": t,
            "y1": Y[:, 0],
            "y2": Y[:, 1],
            "y3": Y[:, 2],
        }
    )

    BASE = Path(__file__).resolve().parent
    DATADIR = BASE / "data"
    DATADIR.mkdir(parents=True, exist_ok=True)
    out_file = DATADIR / "qg_model.csv"
    df.to_csv(out_file, index=False)

    print(f"CSV salvo em: {out_file}")
