import numpy as np
from scipy.integrate import solve_ivp
import pandas as pd
from pathlib import Path
from phi import Phi
from parameters import a, b, c, h, f, nu_0, y

try:
    BASE = Path(__file__).resolve().parent
except NameError:
    BASE = Path.cwd()

OUTDIR = BASE / "data"
OUTDIR.mkdir(parents=True, exist_ok=True)
SAVE_PATH = OUTDIR / "be_model.csv"

def cyc(i):
    return i, (i + 1) % 3, (i + 2) % 3

def be_model(tau, y, phi_vec):
    dydt = np.zeros(3, dtype=float)
    for i in range(3):
        i_, j, k = cyc(i)
        dydt[i] = (
            - (a[k] * b[k] / a[i]) * phi_vec[j] * y[k]
            - (a[j] * b[j] / a[i]) * y[j] * phi_vec[k]
            + (c * (a[k] - a[j]) / a[i]) * y[j] * y[k]
            - phi_vec[i]
            - nu_0 * a[i] * y[i]
        )
    return dydt

dias = 200
t0, tf = 0.0, dias*8            
dt = 0.001                         

tau_span = (t0, tf)       
tau_eval = np.arange(t0, tf + dt, dt)    

phi_vec = Phi(y)

print("Iniciando integração numérica...")
sol = solve_ivp(be_model, tau_span, y, t_eval=tau_eval, method='RK45', args=(phi_vec,))
print("Aguarde...")

sol_t = sol.t
sol_y = sol.y

df = pd.DataFrame({
    "time": sol_t,
    "y1": sol_y[0],
    "y2": sol_y[1],
    "y3": sol_y[2],
})


df.to_csv(SAVE_PATH, index=False)
print(f"Resultados salvos em '{SAVE_PATH}'.")
