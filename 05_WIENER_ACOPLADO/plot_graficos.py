from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


BASE = Path(__file__).resolve().parent
DATADIR = BASE / "data"
OUTDIR = BASE / "src"
OUTDIR.mkdir(parents=True, exist_ok=True)


df_deterministico = pd.read_csv(DATADIR / "deterministico.csv")
df_estocastico = pd.read_csv(DATADIR / "estocastico.csv")

t_deterministico = df_deterministico.iloc[:, 0]
t_estocastico = df_estocastico.iloc[:, 0]
x_deterministico = df_deterministico.iloc[:, 2]
x_estocastico = df_estocastico.iloc[:, 1]



# PLOT HISTOGRAMA SEPARADO
plt.figure(figsize=(12, 9), dpi=300)
plt.hist(x_deterministico, bins=50, color="red", alpha=0.7, edgecolor="black", density=True)
plt.title("Histograma Determinístico", fontsize=22)
plt.xlabel("x", fontsize=18)
plt.ylabel("Frequência", fontsize=18)
plt.grid(True, alpha=0.5)
plt.tight_layout()
plt.savefig(OUTDIR / "hist_deterministico_limpo.png", dpi=300)
plt.close()

plt.figure(figsize=(12, 9), dpi=300)
plt.hist(x_estocastico, bins=50, color="blue", alpha=0.7, edgecolor="black", density=True)
plt.title("Histograma Estocástico", fontsize=22)
plt.xlabel("x", fontsize=18)
plt.ylabel("Frequência", fontsize=18)
plt.grid(True, alpha=0.5)
plt.tight_layout()
plt.savefig(OUTDIR / "hist_estocastico_limpo.png", dpi=300)
plt.close()

"""
# PLOT HISTOGRAMA SOBREPOSTO

plt.figure(figsize=(12, 9), dpi=300)
plt.hist(x_deterministico, bins=50, color="red", alpha=0.6, label="Determinístico", density=True)
plt.hist(x_estocastico, bins=50, color="orange", alpha=0.6, label="Estocástico", density=True)
plt.title("Histograma Normalizado: Determinístico vs. Estocástico", fontsize=22)
plt.xlabel("x", fontsize=18)
plt.ylabel("Densidade", fontsize=18)
plt.grid(True, alpha=0.5)
plt.legend(fontsize=16)
plt.tight_layout()
plt.savefig(OUTDIR / "hist_comparacao_densidade.png", dpi=300)
plt.close()

"""