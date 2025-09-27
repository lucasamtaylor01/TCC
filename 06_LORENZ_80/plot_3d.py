import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

BASE = Path(__file__).resolve().parent
DATA = BASE / "data" / "f03027d400_cond_hardley_limpo.csv"
OUTDIR = BASE / "src"
OUTDIR.mkdir(parents=True, exist_ok=True)

# Ler CSV
df = pd.read_csv(DATA)
t, y1, y2, y3 = df["time"],df["y1"], df["y2"], df["y3"]

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot(y1, y2, y3, linewidth=1.5, color="blue")
ax.set_title("Projeção tridimensional $y_1$ x $y_2$ x $y_3$", fontsize=18)
ax.set_xlabel("y1")
ax.set_ylabel("y2")
ax.set_zlabel("y3")
plt.grid(True)

plt.show()
