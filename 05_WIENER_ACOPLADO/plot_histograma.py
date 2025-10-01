from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# === CONFIGURAÇÕES ===
BASE = Path(__file__).resolve().parent
DATADIR = BASE / "data"
OUTDIR = BASE / "src"
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
df_deterministico = pd.read_csv(DATADIR / "deterministico.csv")
df_estocastico   = pd.read_csv(DATADIR / "estocastico.csv")

x_deterministico = df_deterministico.iloc[:, 2]
x_estocastico    = df_estocastico.iloc[:, 1]

# Histograma determinístico
plt.figure(figsize=(12, 9))
plt.hist(x_deterministico, bins=50, density=True, color=COL_DET, edgecolor="black", alpha=0.85)
plt.title("Histograma Determinístico")
plt.xlabel("x")
plt.ylabel("Densidade")
plt.grid(True, alpha=0.75)
plt.legend(handles=[Patch(facecolor=COL_DET, edgecolor="black", label="Determinístico")])
plt.tight_layout()
plt.savefig(OUTDIR / "hist_deterministico_1.png")
plt.close()

# Histograma estocástico
plt.figure(figsize=(12, 9))
plt.hist(x_estocastico, bins=50, density=True,
         color=COL_EST, edgecolor="black", alpha=0.85)
plt.title("Histograma Estocástico")
plt.xlabel("x")
plt.ylabel("Densidade")
plt.grid(True, alpha=0.75)
plt.legend(handles=[Patch(facecolor=COL_EST, edgecolor="black", label="Estocástico")])
plt.tight_layout()
plt.savefig(OUTDIR / "hist_estocastico.png")
plt.close()

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
plt.savefig(OUTDIR / "hist_comparacao_densidade.png")
plt.close()
