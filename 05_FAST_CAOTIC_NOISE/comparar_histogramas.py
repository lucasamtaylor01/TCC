from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# === CONFIGURAÇÕES ===
BASE = Path(__file__).resolve().parent
DATADIR = BASE / "data"
OUTDIR = BASE / "img"
OUTDIR.mkdir(parents=True, exist_ok=True)

# Paleta Okabe–Ito (color-blind safe)
COL_01 = "#005AB5"   # azul para eps=0.1
COL_02 = "#DC3220"   # vermelho para eps=0.2

plt.rcParams.update({
    "axes.titlesize": 22,
    "axes.labelsize": 18,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14,
    "legend.fontsize": 16,
    "lines.linewidth": 2.2,
    "savefig.dpi": 150
})

# === CARREGAR DADOS ===
df_estocastico_01 = pd.read_csv(DATADIR / "estocastico_01.csv")
df_estocastico_02 = pd.read_csv(DATADIR / "estocastico_02.csv")

x_est_01 = df_estocastico_01.iloc[:, 1]  # coluna x para eps=0.1
x_est_02 = df_estocastico_02.iloc[:, 1]  # coluna x para eps=0.2

# === PLOT: COMPARAÇÃO DE HISTOGRAMAS ===
plt.figure(figsize=(12, 9))
plt.hist(x_est_01, bins=50, density=True, color=COL_01, alpha=0.6, 
         label="Estocástico (ε=0.1)", edgecolor="black")
plt.hist(x_est_02, bins=50, density=True, color=COL_02, alpha=0.6, 
         label="Estocástico (ε=0.2)", edgecolor="black")
plt.title("Comparação de Distribuição: Estocástico ε=0.1 vs. ε=0.2")
plt.xlabel("x")
plt.ylabel("Densidade")
plt.grid(True, alpha=0.75)
plt.legend(frameon=True)
plt.tight_layout()
plt.savefig(OUTDIR / "comparacao_histograma_01_02.png")
plt.close()

print(f"Gráfico salvo em: {OUTDIR / 'comparacao_histograma_01_02.png'}")
