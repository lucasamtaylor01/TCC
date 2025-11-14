import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pathlib import Path

# Configuração global do matplotlib
plt.rcParams.update({
    "font.size": 14,
    "axes.titlesize": 22,
    "axes.labelsize": 18,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14,
    "legend.fontsize": 14,
    "lines.linewidth": 1.5,
    "savefig.dpi": 300,
    "figure.autolayout": True,
    "axes.grid": True
})

# Criar diretório de saída
OUTDIR = Path("img")
OUTDIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv("slo.csv")

plt.figure(figsize=(8, 6))
plt.plot(df['real'], df['imag'], color='#0910aa')
plt.title('Parte Imaginária vs. Parte Real')
plt.xlabel('Parte Real')
plt.ylabel('Parte Imaginária')
plt.grid(True)
plt.savefig(OUTDIR / "plot_real_vs_imag.png")
plt.close()


plt.figure(figsize=(8, 6))
plt.plot(df['t'], df['real'], color='#0910aa')
plt.title('Evolução Temporal da Parte Real')
plt.xlabel('Tempo')
plt.ylabel('Parte Real')
plt.grid(True)
plt.savefig(OUTDIR / "plot_evolucao_real.png")
plt.close()


plt.figure(figsize=(8, 6))
plt.plot(df['t'], df['imag'], color='#0910aa')
plt.title('Evolução Temporal da Parte Imaginária')
plt.xlabel('Tempo')
plt.ylabel('Parte Imaginária')
plt.grid(True)
plt.savefig(OUTDIR / "plot_evolucao_imag.png")
plt.close()


"""
fig_3d = plt.figure(figsize=(10, 8))
ax_3d = fig_3d.add_subplot(111, projection='3d')

ax_3d.plot(df['t'], df['real'], df['imag'], color='#0910aa')
ax_3d.set_xlabel('Tempo')
ax_3d.set_ylabel('Parte Real')
ax_3d.set_zlabel('Parte Imaginária')
ax_3d.set_title('Evolução 3D da Solução')
fig_3d.savefig(OUTDIR / "plot_3d.png")

plt.show()
"""