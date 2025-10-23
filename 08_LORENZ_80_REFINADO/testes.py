from pathlib import Path
import simulacoes as sim
import pandas as pd
import condicoes_iniciais as ci

BASE = Path(__file__).resolve().parent
DATADIR = BASE / "data"
DATADIR.mkdir(parents=True, exist_ok=True)

print("OPÇÃO 01: PE Model")
print("OPÇÃO 02: BE Model")
print("OPÇÃO 03: QG Model")

opcao = int(input("Escolha a simulação: "))

if opcao == 1:
    df = sim.pe_simulate(ci.x0, ci.y0, ci.z0, ci.days)
    out_file = DATADIR / "pe_model.csv"
    df.to_csv(out_file, index=False)
    print("Processo concluído. Arquivo salvo em:", out_file)
elif opcao == 2:
    df = sim.be_simulate(ci.y0, ci.days)
    out_file = DATADIR / "be_model.csv"
    df.to_csv(out_file, index=False)
    print("Processo concluído. Arquivo salvo em:", out_file)    
elif opcao == 3:
    df = sim.qg_simulate(ci.y0, ci.days)
    out_file = DATADIR / "qg_model.csv"
    df.to_csv(out_file, index=False)
    print("Processo concluído. Arquivo salvo em:", out_file)
else:
    print("Opção inválida")
    exit()

