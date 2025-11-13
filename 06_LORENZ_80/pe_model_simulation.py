"""
Simulação do modelo PE (Primitive Equations) do sistema Lorenz 80.
Gera dados de simulação e salva no diretório data/.
"""

import numpy as np
from scipy.integrate import solve_ivp
import pandas as pd
from pathlib import Path
from parameters import a, b, c, h, f, nu_0, kappa_0, g_0
from initial_conditions import x0, y0, z0
from plot import gerar_todos_graficos

# Fator de escala temporal
TIMESCALE_FACTOR = 8.0

# Parâmetros de simulação
N_STEPS = int(5e5)  
DT = 0.004166666666667

# Criar diretório de saída
DATA_DIR = Path("data")
DATA_DIR.mkdir(parents=True, exist_ok=True)


def cyc(i):
    """Retorna índices cíclicos para i, i+1, i+2 (mod 3)"""
    return i, (i + 1) % 3, (i + 2) % 3


def pe_model(t, u):
    """
    Modelo PE (Primitive Equations) completo.
    
    Args:
        t: tempo
        u: vetor de estado [x1, x2, x3, y1, y2, y3, z1, z2, z3]
    
    Returns:
        Derivadas temporais du/dt
    """
    x = u[0:3]
    y = u[3:6]
    z = u[6:9]
    dx = np.zeros(3)
    dy = np.zeros(3)
    dz = np.zeros(3)

    for i in range(3):
        i_, j, k = cyc(i)
        
        # Equação para x
        dx[i] = (
            a[i] * b[i] * x[j] * x[k]
            - c * (a[i] - a[k]) * x[j] * y[k]
            + c * (a[i] - a[j]) * y[j] * x[k]
            - 2 * c**2 * y[j] * y[k]
            - nu_0 * (a[i] ** 2) * x[i]
            + a[i] * y[i]
            - a[i] * z[i]
        ) / a[i]
        
        # Equação para y
        dy[i] = (
            -a[k] * b[k] * x[j] * y[k]
            - a[j] * b[j] * y[j] * x[k]
            + c * (a[k] - a[j]) * y[j] * y[k]
            - a[i] * x[i]
            - nu_0 * (a[i] ** 2) * y[i]
        ) / a[i]
        
        # Equação para z
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


def pe_simulate(x0, y0, z0, n_steps, dt):
    """
    Simula o modelo PE.
    
    Args:
        x0: condições iniciais para x [x1, x2, x3]
        y0: condições iniciais para y [y1, y2, y3]
        z0: condições iniciais para z [z1, z2, z3]
        n_steps: número de passos de tempo
        dt: tamanho do passo temporal
    
    Returns:
        DataFrame com os resultados da simulação
    """
    # Condição inicial completa
    initial_u = np.concatenate([x0, y0, z0])
    
    # Tempo final e pontos de avaliação
    t_final = n_steps * dt
    t_eval = np.linspace(0.0, t_final, n_steps + 1)
    t_span = (0.0, t_final)
    
    # Calcular equivalente em dias
    days_equivalent = t_final / TIMESCALE_FACTOR
    
    # Resolver o sistema de EDOs
    sol = solve_ivp(
        pe_model, 
        t_span, 
        initial_u,
        t_eval=t_eval,
        method="RK45", 
        atol=1e-8, 
        rtol=1e-6
    )
    
    print(f"Integração concluída. Pontos gerados: {len(sol.t)}")

    # Converter tempo de volta para dias
    t_out = sol.t / TIMESCALE_FACTOR
    
    # Extrair componentes
    x, y, z = sol.y[0:3].T, sol.y[3:6].T, sol.y[6:9].T

    # Criar DataFrame
    df = pd.DataFrame({
        "time": t_out,
        "x1": x[:, 0], "x2": x[:, 1], "x3": x[:, 2],
        "y1": y[:, 0], "y2": y[:, 1], "y3": y[:, 2],
        "z1": z[:, 0], "z2": z[:, 1], "z3": z[:, 2],
    })
    
    return df


if __name__ == "__main__":
    
    df_pe = pe_simulate(x0, y0, z0, N_STEPS, DT)
    
    # Salvar resultados
    output_file = DATA_DIR / "pe_model_passos.csv"
    df_pe.to_csv(output_file, index=False)
    
    print(f"\nResultados salvos em: {output_file}")
    
    # Limpeza de dados
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

    # Gerar gráficos
    print("\nGerando gráficos...")
    model_type = 1  # PE model
    graficos = gerar_todos_graficos(df_pe, model_type)
    print("\nSimulação concluída!")