import pandas as pd
import matplotlib.pyplot as plt

# Configurações de estilo do matplotlib
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

# Ler dados do CSV
df = pd.read_csv("stockmarket.csv")

# Plotar trajetória
plt.figure(figsize=(12, 8))
plt.plot(df['t'], df['x'], color="#0910aa", linewidth=2, alpha=0.75)
plt.xlabel('Tempo (t)')
plt.ylabel('Peço da Ação S(t)')
plt.title('Evolução do preço da ação ao longo de 1 ano')
plt.grid(True, alpha=0.3)
plt.tight_layout()

# Salvar figura
fig_path = 'stock_market_evolution.png'
plt.savefig(fig_path, bbox_inches='tight')
print(f'Figura salva em: {fig_path}')

