import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

OUTDIR = Path("src")
OUTDIR.mkdir(parents=True, exist_ok=True)


def get_model_prefix(model_type):

    if model_type == 1:
        return "pe_"
    elif model_type == 2:
        return "be_"
    elif model_type == 3:
        return "qg_"
    else:
        raise ValueError("model_type deve ser 1, 2 ou 3")


def plotagem_y2y3(df, model_type):

    y2, y3 = df["y2"], df["y3"]
    prefix = get_model_prefix(model_type)
    filename = f"{prefix}y3y2.png"

    plt.figure(figsize=(12, 5))
    plt.plot(y3, y2, linewidth=1.5, color="#dc3220")
    plt.title("Projeção bidimensional $y_3$ x $y_2$")
    plt.xlabel("y3")
    plt.ylabel("y2")
    plt.grid(True)
    plt.savefig(OUTDIR / filename)
    plt.show()
    plt.close()
    
    return filename

def plotagem_y1y3(df, model_type):
    
    y1,y3 = df["y1"], df["y3"]
    prefix = get_model_prefix(model_type)
    filename = f"{prefix}y1y3.png"

    plt.figure(figsize=(12, 5))
    plt.plot(y1, y3, linewidth=1.5, color="#dc3220")
    plt.title("Projeção bidimensional $y_1$ x $y_3$")
    plt.xlabel("y1")
    plt.ylabel("y3")
    plt.grid(True)
    plt.savefig(OUTDIR / filename)
    plt.show()
    plt.close()
    
    return filename

def plotagem_y1y2(df, model_type):

    y1, y2= df["y1"], df["y2"]
    prefix = get_model_prefix(model_type)
    filename = f"{prefix}y1y2.png"

    plt.figure(figsize=(12, 5))
    plt.plot(y1, y2, linewidth=1.5, color="#dc3220")
    plt.title("Projeção bidimensional $y_1$ x $y_2$")
    plt.xlabel("y1")
    plt.ylabel("y2")
    plt.grid(True)
    plt.savefig(OUTDIR / filename)
    plt.show()
    plt.close()
    
    return filename

def plotagem_xyz_temporal(df, model_type):
    t, x1, y1, z1 = df["time"], df["x1"], df["y1"], df["z1"]

    prefix = get_model_prefix(model_type)    # Plot
    filename = f"{prefix}time_x1y1z1.png"


    plt.figure(figsize=(12, 8))
    plt.plot(t, x1, label="$x_1$", linewidth=2, color="#0b8126", linestyle="-")   # contínua
    plt.plot(t, y1, label="$y_1$", linewidth=2, color="#0910aa", linestyle="--")  # tracejada
    plt.plot(t, z1, label="$z_1$", linewidth=2, color="#dc3220", linestyle=":")   # pontilhada

    plt.xlabel("Tempo")
    plt.ylabel("Valores de $x_1$, $y_1$ e $z_1$")
    plt.title("Evolução temporal de $x_1$, $y_1$ e $z_1$")
    plt.legend()

    plt.grid(True)
    plt.savefig(OUTDIR / filename)
    plt.show()
    plt.close()
    return filename

def plotagem_temporal(df, model_type, yi):
    t = df["time"]
    prefix = get_model_prefix(model_type)

    if yi == "y1":
        y = df["y1"]
        ylabel = "y1"
    elif yi == "y2":
        y = df["y2"]
        ylabel = "y2"
    elif yi == "y3":
        y = df["y3"]
        ylabel = "y3"
    else:
        raise ValueError("yi deve ser 1, 2 ou 3")
    
    filename = f"{prefix}time{ylabel}.png"
    
    plt.figure(figsize=(12, 5))
    plt.plot(t, y, linewidth=1.5, color="#dc3220")
    plt.title(f"Evolução temporal de ${ylabel}$")
    plt.xlabel("time")
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.savefig(OUTDIR / filename)
    plt.show()
    plt.close()
    
    return filename

