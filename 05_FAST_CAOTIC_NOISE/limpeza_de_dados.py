import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parent
DATA = BASE / "data" / "estocastico001.csv"


df = pd.read_csv(DATA, header=1)
n_remove = int(len(df) * 0.15)
df_filtrado = df.iloc[n_remove:].reset_index(drop=True)
OUTFILE = BASE / "data" / "estocastico001_limpo.csv"
df_filtrado.to_csv(OUTFILE, index=False)
print(f'Dados foram limpos e salvos em: {OUTFILE}')