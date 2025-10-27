import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp
from pathlib import Path
import time

eps = 0.2
lam = 1.0

progress_tracker = {'last_printed_percent': -1}

def rhs(t, u):
    # --- Monitoramento de Progresso ---
    current_percent = int((t - t0) / (tf - t0) * 10) * 10
    if current_percent > progress_tracker['last_printed_percent']:
        if current_percent <= 100:
            print(f"{current_percent}% concluído...")
            progress_tracker['last_printed_percent'] = current_percent
    # --------------------------------

    x, y1, y2, y3 = u
    dx = x - x**3 + (lam/eps) * y2
    dy1 = (10 / eps**2) * (y2 - y1)
    dy2 = (1 / eps**2) * (28*y1 - y2 - y1*y3)
    dy3 = (1 / eps**2) * (y1*y2 - (8/3)*y3)
    return [dx, dy1, dy2, dy3]

# --- Ajuste adaptativo de tolerâncias conforme eps ---
p = 2.0  # expoente de escala
rtol = 1e-3 * eps**p
atol = 1e-6 * eps**p

print(f"Usando rtol={rtol:.2e}, atol={atol:.2e}")

t0, tf = 0.0, 100.0
x0 = 0.1
y0 = [x0, 1e-2, 1e-2, 1e-2]
t_eval = np.arange(t0, tf, 1e-3)

start_time = time.time()
sol = solve_ivp(rhs, (t0, tf), y0, method="RK45",
                t_eval=t_eval, rtol=rtol, atol=atol)
end_time = time.time()

execution_time = end_time - start_time

x_vals = sol.y[0]
y2_vals = sol.y[2]

BASE = Path(__file__).resolve().parent if "__file__" in globals() else Path(".")
DATADIR = BASE / "data"
DATADIR.mkdir(parents=True, exist_ok=True)
out_file = DATADIR / f"deterministico02.csv"

df = pd.DataFrame({"t": sol.t, "y2": y2_vals, "x": x_vals})
with open(out_file, 'w') as f:
    f.write(f'# eps={eps}, rtol={rtol:.2e}, atol={atol:.2e}, tempo={execution_time:.2f}s\n')
    df.to_csv(f, index=False)

print(f"Dados salvos em: {out_file}")
print(f"Tempo de execução: {execution_time:.2f} s")
