import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Configurações de diretórios
BASE = Path(__file__).resolve().parent
DATADIR = BASE / "data"
OUTDIR = BASE / "src"
OUTDIR.mkdir(parents=True, exist_ok=True)


COL_DET = "#005AB5"   # azul
COL_EST = "#DC3220"   # laranja

deterministico_path = DATADIR / 'deterministico_100.csv'
estocastico_path = DATADIR / 'estocastico_100.csv'
df_det = pd.read_csv(deterministico_path)
df_est = pd.read_csv(estocastico_path)

tempo_col = 't'
x_col = 'x'

# Gráfico determinístico
plt.figure(figsize=(10, 6))
plt.plot(df_det[tempo_col], df_det[x_col], color=COL_DET)
plt.xlabel('Tempo')
plt.ylabel('x')
plt.title('Evolução da variável x (Determinístico)')
plt.grid(True)
plt.tight_layout()
fig_det = OUTDIR / 'evolucao_x_deterministico_100.png'
plt.savefig(fig_det)
print(f'Figura determinística salva em: {fig_det}')
plt.close()

# Gráfico estocástico
plt.figure(figsize=(10, 6))
plt.plot(df_est[tempo_col], df_est[x_col], color=COL_EST)
plt.xlabel('Tempo')
plt.ylabel('x')
plt.title('Evolução da variável x (Estocástico)')
plt.grid(True)
plt.tight_layout()
fig_est = OUTDIR / 'evolucao_x_estocastico_100.png'
plt.savefig(fig_est)
print(f'Figura estocástica salva em: {fig_est}')
plt.close()
