from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# Caminhos base
BASE = Path(__file__).resolve().parent
DATADIR = BASE / "data"
OUTDIR = BASE / "src"
OUTDIR.mkdir(parents=True, exist_ok=True)

# Ler os dados
df_deterministico = pd.read_csv(DATADIR / "deterministico.csv")
df_estocastico = pd.read_csv(DATADIR / "estocastico.csv")

# Extrair colunas
t = df_deterministico.iloc[:, 0]
x_deterministico = df_deterministico.iloc[:, 2]
x_estocastico = df_estocastico.iloc[:, 1]

# --- Plot determinístico ---
plt.figure(figsize=(12, 9), dpi=300)
plt.plot(t, x_deterministico, linewidth=2, color="red", label="x")
plt.title("Determinístico", fontsize=22)
plt.xlabel("t", fontsize=18)
plt.ylabel("x", fontsize=18)
plt.legend(fontsize=16)
plt.grid(True, alpha=0.5)
plt.tight_layout()
plt.savefig(OUTDIR / "deterministico_plot.png", dpi=300)
plt.close()

# --- Plot estocástico ---
plt.figure(figsize=(12, 9), dpi=300)
plt.plot(t, x_estocastico, linewidth=2, color="blue", label="x")
plt.title("Estocástico", fontsize=22)
plt.xlabel("t", fontsize=18)
plt.ylabel("x", fontsize=18)
plt.legend(fontsize=16)
plt.grid(True, alpha=0.5)
plt.tight_layout()
plt.savefig(OUTDIR / "estocastico_plot.png", dpi=300)
plt.close()

# --- Histograma determinístico ---
plt.figure(figsize=(12, 9), dpi=300)
plt.hist(x_deterministico, bins=50, color="red", alpha=0.7, edgecolor="black")
plt.title("Histograma Determinístico", fontsize=22)
plt.xlabel("x", fontsize=18)
plt.ylabel("Frequência", fontsize=18)
plt.grid(True, alpha=0.5)
plt.tight_layout()
plt.savefig(OUTDIR / "hist_deterministico.png", dpi=300)
plt.close()

# --- Histograma estocástico ---
plt.figure(figsize=(12, 9), dpi=300)
plt.hist(x_estocastico, bins=50, color="blue", alpha=0.7, edgecolor="black")
plt.title("Histograma Estocástico", fontsize=22)
plt.xlabel("x", fontsize=18)
plt.ylabel("Frequência", fontsize=18)
plt.grid(True, alpha=0.5)
plt.tight_layout()
plt.savefig(OUTDIR / "hist_estocastico.png", dpi=300)
plt.close()
