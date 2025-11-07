import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp
from pathlib import Path
import time
from tqdm import tqdm

eps = 0.1
lam = 1.0

# Variáveis globais para barra de progresso
progress_bar = None
last_time = None

def rhs(t, u):
    global progress_bar, last_time
    
    # Atualizar barra de progresso
    if progress_bar is not None and (last_time is None or t - last_time > 0.1):
        progress = min(100, int(100 * t / 100.0))  # tf = 100.0
        if progress > progress_bar.n:
            progress_bar.update(progress - progress_bar.n)
        last_time = t
    
    x, y1, y2, y3 = u
    dx = x - x**3 + (lam/eps) * y2
    dy1 = (10 / eps**2) * (y2 - y1)
    dy2 = (1 / eps**2) * (28*y1 - y2 - y1*y3)
    dy3 = (1 / eps**2) * (y1*y2 - (8/3)*y3)
    return [dx, dy1, dy2, dy3]


p = 2.0  
rtol = 1e-3 * eps**p
atol = 1e-6 * eps**p

print(f"Usando rtol={rtol:.2e}, atol={atol:.2e}")

t0, tf = 0.0, 100.0
x0 = 0.1
y0 = [x0, 1e-2, 1e-2, 1e-2]
t_eval = np.arange(t0, tf, 1e-3)

print("Iniciando integração numérica...")

# Inicializar barra de progresso
progress_bar = tqdm(total=100, desc="Integrando EDO", unit="%", 
                   bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]")

start_time = time.time()
sol = solve_ivp(rhs, (t0, tf), y0, method="RK45",t_eval=t_eval, rtol=rtol, atol=atol)
end_time = time.time()

# Finalizar barra de progresso
progress_bar.update(100 - progress_bar.n)
progress_bar.close()

execution_time = end_time - start_time

x_vals = sol.y[0]
y2_vals = sol.y[2]

BASE = Path(__file__).resolve().parent if "__file__" in globals() else Path(".")
DATADIR = BASE / "data"
DATADIR.mkdir(parents=True, exist_ok=True)
eps_str = str(eps).replace(".", "")
out_file = DATADIR / f"deterministico_{eps_str}.csv"

print("\nSalvando dados...")
df = pd.DataFrame({"t": sol.t, "y2": y2_vals, "x": x_vals})
with open(out_file, 'w') as f:
    f.write(f'# eps={eps}, rtol={rtol:.2e}, atol={atol:.2e}, tempo={execution_time:.2f}s\n')
    df.to_csv(f, index=False)

print(f"✅ Dados salvos em: {out_file}")
print(f"⏱️  Tempo total de execução: {execution_time:.2f}s")
print(f"📊 Pontos calculados: {len(sol.t)}")
