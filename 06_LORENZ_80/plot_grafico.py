import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Caminhos
BASE = Path(__file__).resolve().parent
DATA = BASE / "data" / "python327.csv"
OUTDIR = BASE / "src"
OUTDIR.mkdir(parents=True, exist_ok=True)
OUTPNG = OUTDIR / "evolucao_xyz_python327.png"

# Ler CSV
df = pd.read_csv(DATA)

t = df["time"] # python n divide por 8
x1 = df["x1"]
y1 = df["y1"]
z1 = df["z1"]

# Plot
plt.figure(figsize=(12, 8), dpi=300)
plt.plot(t, x1, label="$x_1$", linewidth=1.5, color="green")
plt.plot(t, y1, label="$y_1$", linewidth=1.5, color="blue")
plt.plot(t, z1, label="$z_1$", linewidth=1.5, color="red")

plt.xlabel("t (dias)", fontsize=16)
plt.ylabel("Valores", fontsize=16)
plt.title("Evolução temporal de $x_1$, $y_1$ e $z_1$", fontsize=18)
plt.legend(fontsize=14)
plt.grid(True)

# Salvar figura
plt.savefig(OUTPNG, bbox_inches="tight")
plt.close()

print(f"Figura salva em: {OUTPNG}")
