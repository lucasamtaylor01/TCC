from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# Base = pasta onde está este script (06_LORENZ_80)
BASE = Path(__file__).resolve().parent
DATA = BASE / "data" / "solucao_01.csv"
OUTDIR = BASE / "src"
OUTDIR.mkdir(parents=True, exist_ok=True)
OUTPNG = OUTDIR / "evolucao_temporal_01.png"

# Ler CSV
df = pd.read_csv(DATA)

td = df["time"] / 8

plt.figure(figsize=(12,9), dpi=300)

plt.plot(td, df["x1"], label="x1", linewidth=2, color='green')
plt.plot(td, df["y1"], label="y1", linewidth=2, color='blue')
plt.plot(td, df["z1"], label="z1", linewidth=2, color='red')

plt.xlabel("t (dias)", fontsize=18)
plt.ylabel("Valores", fontsize=18)
plt.title("Evolução temporal (1 dia)", fontsize=22)
plt.legend(fontsize=16)
plt.tight_layout()
plt.grid(True, alpha=0.5)

# Salvar
plt.savefig(OUTPNG, dpi=300)
print(f"Figura salva em: {OUTPNG}")
