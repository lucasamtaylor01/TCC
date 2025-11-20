from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# === CONFIGURAÇÕES ===
BASE = Path(__file__).resolve().parent
DATADIR = BASE / "data"

eps = 0.05
eps_str = str(eps).replace(".", "")

# Criar pasta específica para o valor de eps
OUTDIR = BASE / "img" / eps_str
OUTDIR.mkdir(parents=True, exist_ok=True)

# Paleta Okabe–Ito (color-blind safe)
COL_DET = "#005AB5"   # azul
COL_EST = "#DC3220"   # laranja

plt.rcParams.update({
    "axes.titlesize": 22,
    "axes.labelsize": 18,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14,
    "legend.fontsize": 16,
    "lines.linewidth": 2.2,
    "savefig.dpi": 150
})

# === DADOS ===
df_deterministico = pd.read_csv(DATADIR / f"deterministico_{eps_str}.csv", comment="#")
df_estocastico   = pd.read_csv(DATADIR / f"estocastico_{eps_str}.csv")

t_deterministico = df_deterministico.iloc[:, 0]  # coluna t
x_deterministico = df_deterministico.iloc[:, 2]  # coluna x

t_estocastico = df_estocastico.iloc[:, 0]        # coluna t
x_estocastico = df_estocastico.iloc[:, 1]        # coluna x


plt.figure(figsize=(14, 8))

# Filtrar dados para o intervalo 50-52s
mask_det = (t_deterministico >= 50) & (t_deterministico <= 51)
mask_est = (t_estocastico >= 50) & (t_estocastico <= 51)

plt.plot(t_deterministico[mask_det], x_deterministico[mask_det], 
         color=COL_DET, label="Determinístico", linewidth=1.5)
plt.plot(t_estocastico[mask_est], x_estocastico[mask_est], 
         color=COL_EST, label="Estocástico", linewidth=1.5)

plt.title("Evolução Temporal de x: Determinístico vs. Estocástico")
plt.xlabel("Tempo (t)")
plt.ylabel("x(t)")
plt.grid(True, alpha=0.3)
plt.legend(frameon=True)
plt.tight_layout()
plt.savefig(OUTDIR / f"{eps_str}_serie_temporal_x.png")
plt.close()

# === PLOT: COMPARAÇÃO DE DENSIDADE ===
plt.figure(figsize=(12, 9))
plt.hist(x_deterministico, bins=50, density=True, color=COL_DET, alpha=0.6, label="Determinístico", edgecolor="black")
plt.hist(x_estocastico, bins=50, density=True, color=COL_EST, alpha=0.6, label="Estocástico", edgecolor="black")
plt.title("Distribuição da Variável x: Determinístico vs. Estocástico")
plt.xlabel("x")
plt.ylabel("Densidade")
plt.grid(True, alpha=0.75)
plt.legend(frameon=True)
plt.tight_layout()
plt.savefig(OUTDIR / f"{eps_str}_hist_comparacao_densidade.png")
plt.close()

print(f"Gráficos salvos na pasta: {OUTDIR}")
print(f"- Série temporal: {eps_str}_serie_temporal_x.png")
print(f"- Histograma de densidade: {eps_str}_hist_comparacao_densidade.png")
