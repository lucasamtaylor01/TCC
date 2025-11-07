from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# === CONFIGURAÇÕES ===
BASE = Path(__file__).resolve().parent
DATADIR = BASE / "data"
OUTDIR = BASE / "img"
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

eps = 0.01
eps_str = str(eps).replace(".", "")

# === DADOS ===
df_deterministico = pd.read_csv(DATADIR / f"deterministico_{eps_str}.csv", comment="#")
df_estocastico   = pd.read_csv(DATADIR / f"estocastico_{eps_str}.csv")

x_deterministico = df_deterministico.iloc[:, 2]
x_estocastico    = df_estocastico.iloc[:, 1]


# Comparação
plt.figure(figsize=(12, 9))
plt.hist(x_deterministico, bins=50, density=True,
         color=COL_DET, alpha=0.6, label="Determinístico", edgecolor="black")
plt.hist(x_estocastico, bins=50, density=True,
         color=COL_EST, alpha=0.6, label="Estocástico", edgecolor="black")
plt.title("Determinístico vs. Estocástico")
plt.xlabel("x")
plt.ylabel("Densidade")
plt.grid(True, alpha=0.75)
plt.legend(frameon=True)
plt.tight_layout()
plt.savefig(OUTDIR / f"hist_comparacao_densidade_{eps_str}.png")
plt.close()
