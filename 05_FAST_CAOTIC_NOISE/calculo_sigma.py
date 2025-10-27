import numpy as np
import pandas as pd
import os

def sigma_from_y2(y2, dt, lam=1.0):
    y = y2 - np.mean(y2)
    n = len(y)
    nfft = n
    fy = np.fft.rfft(y, n=nfft)
    ac = np.fft.irfft(fy * np.conj(fy), n=nfft)[:n] / np.arange(n, 0, -1)
    sigma2 = abs(2 * lam**2 * dt * np.sum(ac))
    return np.sqrt(max(sigma2, 0.0))


csv_path = os.path.join(os.path.dirname(__file__), "data", "deterministico02.csv")
df = pd.read_csv(csv_path, comment="#")
dt = df["t"][1] - df["t"][0]
sigma = sigma_from_y2(df["y2"].to_numpy(), dt)
print("σ =", sigma)
