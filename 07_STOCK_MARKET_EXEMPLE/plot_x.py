import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Configurações de diretórios
BASE = Path(__file__).resolve().parent
DATADIR = BASE / "data"
OUTDIR = BASE / "src"
OUTDIR.mkdir(parents=True, exist_ok=True)

# Cores
COL_OU = "#DC3220"  # vermelho para Ornstein-Uhlenbeck

# Ler dados do CSV
ou_path = DATADIR / 'stock_market.csv'
df = pd.read_csv(ou_path)

# Plotar trajetória
plt.figure(figsize=(12, 8))
plt.plot(df['t'], df['x'], color=COL_OU, linewidth=2, alpha=0.8)
plt.xlabel('Tempo (t)', fontsize=12)
plt.ylabel('X(t)', fontsize=12)
plt.title('Evolução do preço da ação ao longo de 1 ano', fontsize=18)
plt.grid(True, alpha=0.3)
plt.tight_layout()

for t in [i / 10 for i in range(1, 10)]:
    plt.axvline(x=t, color='gray', linestyle='--', linewidth=1, alpha=0.5)
# Salvar figura
fig_path = OUTDIR / 'stock_market_evolution.png'
plt.savefig(fig_path, dpi=300, bbox_inches='tight')
print(f'Figura salva em: {fig_path}')

