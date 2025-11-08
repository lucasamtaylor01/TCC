
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ---- CONFIG ----
DATA_DIR = Path("data")
OUTDIR   = Path("img")
CSV_FILES = {"PE": "pe_model.csv", "QG": "qg_model.csv", "BE": "be_model.csv"}     
VARS = ["y1", "y2", "y3"]
COLORS = {"PE": "black", "QG": "red", "BE": "blue"}
OUTFILE = OUTDIR / "amplitudes.png"

def read_df(path: Path):
    df = pd.read_csv(path)
    # garante numérico e ordenado por tempo
    df = df.sort_values("time").reset_index(drop=True)
    df["time"] = pd.to_numeric(df["time"], errors="coerce")
    df = df.dropna(subset=["time"]).reset_index(drop=True)
    return df

def cut_transient(df: pd.DataFrame, frac: float = 0.0):
    if frac <= 0:
        return df
    n0 = int(len(df) * frac)
    return df.iloc[n0:].reset_index(drop=True)

def main():
    OUTDIR.mkdir(exist_ok=True)

    # Lê CSVs
    D = {m: read_df(DATA_DIR / f) for m, f in CSV_FILES.items()}

    # Intervalo comum de tempo (interseção)
    t0 = max(D[m]["time"].iloc[0] for m in D)
    t1 = min(D[m]["time"].iloc[-1] for m in D)
    if t1 <= t0:
        t0 = min(D[m]["time"].iloc[0] for m in D)
        t1 = max(D[m]["time"].iloc[-1] for m in D)

    # Limites comuns por variável
    ylims = {}
    for v in VARS:
        vals = np.concatenate([D[m][v].to_numpy(dtype=float) for m in D])
        rng = vals.max() - vals.min()
        pad = 0.05 * (rng if rng > 0 else 1.0)
        ylims[v] = (vals.min() - pad, vals.max() + pad)

    order = ["PE", "QG", "BE"]
    nrows = len(VARS) * len(order)
    fig, axes = plt.subplots(nrows=nrows, ncols=1, figsize=(12, 10), sharex=True)

    # --- PLOTAGEM ---
    row = 0
    for v in VARS:
        for m in order:
            ax = axes[row]
            ax.plot(D[m]["time"].to_numpy(),
                    D[m][v].to_numpy(),
                    lw=0.9, color=COLORS[m])
            ax.axhline(0.0, lw=0.6, color="gray", alpha=0.6)
            ax.grid(True, linewidth=0.4, alpha=0.35)
            ax.set_ylim(*ylims[v])
            ax.set_xlim(t0, t1)
            ax.text(0.005, 0.88, v, transform=ax.transAxes, fontsize=10, weight="bold")
            ax.text(0.995, 0.88, m, transform=ax.transAxes, fontsize=10,
                    ha="right", color=COLORS[m])
            ax.tick_params(axis="y", labelsize=8, length=3)
            if row < nrows - 1:
                ax.tick_params(axis="x", labelbottom=False)
            row += 1

    axes[0].set_title("Séries temporais de $y$ para os modelos PE, QG e BE", pad=8, fontsize=12)
    axes[-1].set_xlabel("time")
    plt.subplots_adjust(hspace=0.12, top=0.95, bottom=0.07, left=0.07, right=0.985)
    fig.savefig(OUTFILE)
    plt.close(fig)
    print(f"Figura salva em: {OUTFILE.resolve()}")

    # --- CÁLCULO DAS AMPLITUDES ---
    amps = {}
    for m in D:
        amps[m] = {v: D[m][v].max() - D[m][v].min() for v in VARS}
    df_amp = pd.DataFrame(amps).T
    df_amp.index.name = "Modelo"

    print("\nAmplitudes Δy_i = max(y_i) - min(y_i):")
    print(df_amp.round(3))

if __name__ == "__main__":
    main()
