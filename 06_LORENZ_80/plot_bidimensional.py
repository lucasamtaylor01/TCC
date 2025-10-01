import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE = Path(__file__).resolve().parent
DATA = BASE / "data" / "f03027d400_cond_hardley_limpo.csv"
OUTDIR = BASE / "src"
OUTDIR.mkdir(parents=True, exist_ok=True)

# Ler CSV
df = pd.read_csv(DATA)
t, y1, y2, y3 = df["time"],df["y1"], df["y2"], df["y3"]


plt.figure(figsize=(12, 5))
plt.plot(y3, y2, linewidth=1.5, color="#dc3220")
plt.title("Projeção bidimensional $y_3$ x $y_2$", fontsize=18)
plt.xlabel("y3")
plt.ylabel("y2")
plt.grid(True)
plt.savefig(OUTDIR / "l80_y3_x_y2.png")
plt.close()
