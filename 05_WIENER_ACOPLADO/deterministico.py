import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp
from pathlib import Path
import sys

eps = 0.01
lam = 1.0

# Variáveis para barra de progresso
last_percentage = 0

def rhs(t, u):
    global last_percentage
    x, y1, y2, y3 = u
    dx = x - x**3 + (lam/eps) * y2
    dy1 = (10 / eps**2) * (y2 - y1)
    dy2 = (1 / eps**2) * (28*y1 - y2 - y1*y3)
    dy3 = (1 / eps**2) * (y1*y2 - (8/3)*y3)
    
    # Barra de progresso
    progress = (t - t0) / (tf - t0) * 100
    percentage = int(progress)
    if percentage > last_percentage and percentage % 1 == 0:
        print(f"Progresso: {percentage}%")
        last_percentage = percentage
    
    return [dx, dy1, dy2, dy3]

t0, tf = 0.0, 50.0
x0 = 0.1
y0_vals = [1e-2, 1e-2, 1e-2]
y0 = [x0] + y0_vals
t_eval = np.arange(t0, tf, 1e-3)

print("Iniciando integração...")
sol = solve_ivp(rhs, (t0, tf), y0, method="RK45", t_eval=t_eval, rtol=1e-4, atol=1e-6)
print("Integração concluída!")

x_vals = sol.y[0]
y2_vals = sol.y[2]

BASE = Path(__file__).resolve().parent if "__file__" in globals() else Path(".")
DATADIR = BASE / "data"
DATADIR.mkdir(parents=True, exist_ok=True)


df = pd.DataFrame({"t": sol.t, "y2": y2_vals, "x": x_vals})
df.to_csv(DATADIR / "deterministico_50.csv", index=False)
print(f"Dados salvos em: {DATADIR / 'deterministico_50.csv'}")
        