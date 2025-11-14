import numpy as np
from scipy.integrate import solve_ivp
import pandas as pd
from pathlib import Path
from parameters import a, b, c, h, f, nu_0, kappa_0, g_0
from initial_conditions import x0, y0, z0
from plot import gerar_todos_graficos

TIMESCALE_FACTOR = 8.0
N_STEPS = int(5e5)
DT = 0.004166666666667
DATA_DIR = Path("data")
DATA_DIR.mkdir(parents=True, exist_ok=True)

def cyc(i):
    return i, (i + 1) % 3, (i + 2) % 3

def pe_model_scaled(t, u, eps, a, b, c, nu_0, kappa_0, g_0, f, h):
    x = u[0:3]
    y = u[3:6]
    z = u[6:9]

    dx = np.zeros(3)
    dy = np.zeros(3)
    dz = np.zeros(3)

    for i in range(3):
        i_, j, k = cyc(i)

        rhs_x = (
            eps**3 * a[i] * b[i] * x[j] * x[k]
            - eps**2 * c * (a[i] - a[k]) * x[j] * y[k]
            + eps**2 * c * (a[i] - a[j]) * y[j] * x[k]
            - 2.0 * eps * c**2 * y[j] * y[k]
            - eps**2 * nu_0 * a[i]**2 * x[i]
            + a[i] * (y[i] - z[i])
        )
        dx[i] = rhs_x / (eps**2 * a[i])

        rhs_y = (
            - eps * a[k] * b[k] * x[j] * y[k]
            - eps * a[j] * b[j] * y[j] * x[k]
            + c * (a[k] - a[j]) * y[j] * y[k]
            - a[i] * x[i]
            - nu_0 * a[i]**2 * y[i]
        )
        dy[i] = rhs_y / a[i]

        rhs_z = (
            - eps * b[k] * x[j] * (z[k] - h[k])
            - eps * b[j] * (z[j] - h[j]) * x[k]
            + c * y[j] * (z[k] - h[k])
            - c * (z[j] - h[j]) * y[k]
            + g_0 * a[i] * x[i]
            - kappa_0 * a[i] * z[i]
            + f[i]
        )
        dz[i] = rhs_z

    return np.concatenate([dx, dy, dz])

def pe_simulate(x0, y0, z0, n_steps, dt, eps, a, b, c, nu_0, kappa_0, g_0, f, h):
    # ESCALONAMENTO DAS VARIÁVEIS INICIAIS
    x0_scaled = np.array(x0) / eps**2
    y0_scaled = np.array(y0) / eps
    z0_scaled = np.array(z0) / eps

    # ESCALONAMENTO DOS PARÂMETROS
    nu_0_scaled = nu_0 / eps
    kappa_0_scaled = kappa_0 / eps
    f_scaled = np.array(f) / eps**2
    h_scaled = np.array(h) / eps

    initial_u = np.concatenate([x0_scaled, y0_scaled, z0_scaled])
    t_final = n_steps * dt
    t_eval = np.linspace(0.0, t_final, n_steps + 1)
    t_span = (0.0, t_final)

    sol = solve_ivp(
        pe_model_scaled,
        t_span,
        initial_u,
        t_eval=t_eval,
        method="RK45",
        atol=1e-8,
        rtol=1e-6,
        args=(eps, a, b, c, nu_0_scaled, kappa_0_scaled, g_0, f_scaled, h_scaled)
    )

    print(f"Integração concluída. Pontos gerados: {len(sol.t)}")
    t_out = sol.t / TIMESCALE_FACTOR
    x, y, z = sol.y[0:3].T, sol.y[3:6].T, sol.y[6:9].T

    df = pd.DataFrame({
        "time": t_out,
        "x1": x[:, 0], "x2": x[:, 1], "x3": x[:, 2],
        "y1": y[:, 0], "y2": y[:, 1], "y3": y[:, 2],
        "z1": z[:, 0], "z2": z[:, 1], "z3": z[:, 2],
    })

    return df

if __name__ == "__main__":
    eps = 1.5522
    t_total = N_STEPS * DT
    dias_equivalentes = t_total / TIMESCALE_FACTOR

    df_pe = pe_simulate(
        x0, y0, z0,
        N_STEPS, DT,
        eps, a, b, c,
        nu_0, kappa_0, g_0, f, h
    )

    output_file = DATA_DIR / "pe_model_passos.csv"
    df_pe.to_csv(output_file, index=False)

    print(f"\nResultados salvos em: {output_file}")

    limpeza_de_dados = input("\nDeseja eliminar 25% dos dados? (s/n): ").strip().lower()
    if limpeza_de_dados == 's':
        print("Limpando dados...")
        df = pd.read_csv(output_file)
        n_remove = int(len(df) * 0.25)
        df_filtrado = df.iloc[n_remove:].copy()
        df_filtrado.to_csv(output_file, index=False)
        df_pe = df_filtrado
        print(f"Limpeza concluída. Foram removidos ({n_remove/len(df)*100:.1f}% dos dados).")
    elif limpeza_de_dados == 'n':
        print("Dados mantidos sem alteração.")

    print("\nGerando gráficos...")
    model_type = 1
    graficos = gerar_todos_graficos(df_pe, model_type)
    print("\nSimulação concluída!")