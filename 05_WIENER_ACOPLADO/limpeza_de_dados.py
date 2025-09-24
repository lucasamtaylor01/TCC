import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parent
DATA = BASE / "data" / "deterministico.csv"


df = pd.read_csv(DATA)
n_remove = int(len(df) * 0.3)
df_filtrado = df.iloc[n_remove:].reset_index(drop=True)
OUTFILE = BASE / "data" / "deterministico.csv"
df_filtrado.to_csv(OUTFILE, index=False)
