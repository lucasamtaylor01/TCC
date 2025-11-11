from pathlib import Path
import simulations as sim
import pandas as pd
import initial_conditions as ic
import plot

BASE = Path(__file__).resolve().parent
DATADIR = BASE / "data"
DATADIR.mkdir(parents=True, exist_ok=True)

print("""==============================
>>  SELECIONE O MODELO L80  <<
==============================""")

print("1: PE Model")
print("2: BE Model")
print("3: QG Model")

model_type = int(input("\nOpção selecionada: "))

if model_type == 1:
    df = sim.pe_simulate(ic.x0, ic.y0, ic.z0, ic.days)
    out_file = DATADIR / "pe_model.csv"
    df.to_csv(out_file, index=False)
    print("Processo concluído. Arquivo salvo em:", out_file)
elif model_type == 2:
    df = sim.be_simulate(ic.y0, ic.days)
    out_file = DATADIR / "be_model.csv"
    df.to_csv(out_file, index=False)
    print("\nProcesso concluído. Arquivo salvo em:", out_file)    
elif model_type == 3:
    df = sim.qg_simulate(ic.y0, ic.days)
    out_file = DATADIR / "qg_model.csv"
    df.to_csv(out_file, index=False)
    print("\nProcesso concluído. Arquivo salvo em:", out_file)
else:
    print("Opção inválida")
    exit()

limpeza_de_dados = input("\nDeseja eliminar 25% dos dados? (s/n): ").strip().lower()
if limpeza_de_dados == 's':
    print("Limpando dados...")
    df = pd.read_csv(out_file)
    n_remove = int(len(df) * 0.25)
    df_filtrado = df.iloc[n_remove:].copy()
    df_filtrado.to_csv(out_file, index=False)
    df = df_filtrado
    print(f"Limpeza concluída. Foram removidos ({n_remove/len(df)*100:.1f}% dos dados).")
elif limpeza_de_dados == 'n':
    print("Dados mantidos sem alteração.")
else:
    print("Opção inválida. Dados mantidos sem alteração.")

print("""\n==============================
>>  SELECIONE A OPÇÃO GRÁFICA  <<
==============================""")

while True:
    if model_type == 2 or model_type == 3:
        print("1: Projeção y1 vs y2")
        print("2: Projeção y1 vs y3")
        print("3: Projeção y2 vs y3")
        print("4: Evolução temporal de y1")
        print("5: Evolução temporal de y2")
        print("6: Evolução temporal de y3")
        print("7: Evolução temporal empilhada de y1, y2, y3")
        print("8: Gerar todos os gráficos")

        opcao_grafica = int(input("\nEscolha a opção gráfica: "))
        if opcao_grafica == 1:
            print("Gráfico salvo em: img/", plot.plot_y1y2(df, model_type))
        elif opcao_grafica == 2:
            print("Gráfico salvo em: img/", plot.plot_y1y3(df, model_type))
        elif opcao_grafica == 3:
            print("Gráfico salvo em: img/", plot.plot_y2y3(df, model_type))
        elif opcao_grafica == 4:
            print("Gráfico salvo em: img/", plot.plot_temporal(df, model_type, "y1"))
        elif opcao_grafica == 5:
            print("Gráfico salvo em: img/", plot.plot_temporal(df, model_type, "y2"))
        elif opcao_grafica == 6:
            print("Gráfico salvo em: img/", plot.plot_temporal(df, model_type, "y3"))
        elif opcao_grafica == 4:
            print("Gráfico salvo em: img/", plot.plot_temporal(df, model_type, "y1"))
        elif opcao_grafica == 5:
            print("Gráfico salvo em: img/", plot.plot_temporal(df, model_type, "y2"))
        elif opcao_grafica == 6:
            print("Gráfico salvo em: img/", plot.plot_temporal(df, model_type, "y3"))
        elif opcao_grafica == 7:
            print("Gráfico salvo em: img/", plot.evolucao_temporal_y(df, model_type))
        elif opcao_grafica == 8:
            plot.gerar_todos_graficos(df, model_type)
            print("Gráficos gerados com sucesso.")
        else:
            print("Opção inválida.")
            continue
    
    if model_type == 1:
        print("1: Projeção y1 vs y2")
        print("2: Projeção y1 vs y3")
        print("3: Projeção y2 vs y3")
        print("4: Evolução temporal de y1, x1, z1")
        print("5: Evolução temporal empilhada de y1, y2, y3")
        print("6: Gerar todos os gráficos")

        opcao_grafica = int(input("Opção selecionada: "))
        if opcao_grafica == 1:
            print("Gráfico salvo em:", plot.plot_y1y2(df, model_type))
        elif opcao_grafica == 2:    
            print("Gráfico salvo em:", plot.plot_y1y3(df, model_type))
        elif opcao_grafica == 3:    
            print("Gráfico salvo em:", plot.plot_y2y3(df, model_type))
        elif opcao_grafica == 4:
            print("Gráfico salvo em:", plot.plot_xyz_temporal(df, model_type))
        elif opcao_grafica == 5:
            print("Gráfico salvo em:", plot.evolucao_temporal_y(df, model_type))
        elif opcao_grafica == 6:
            plot.gerar_todos_graficos(df, model_type)
            print("Gráficos gerados com sucesso.")
        else:
            print("Opção inválida.")
            continue
    
    sair_confirm = False
    while True:
        confirmar = input("\nDeseja prosseguir para as plotagens? (s/n): ").strip().lower()
        if confirmar == 'n':
            print("Encerrando o programa.")
            sair_confirm = True
            exit()
        elif confirmar == 's':
            break
        else:
            print("Opção inválida. Por favor, responda com 's' ou 'n'.")
