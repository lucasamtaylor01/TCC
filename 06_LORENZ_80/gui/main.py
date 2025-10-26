import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
import simulacoes as sim
import pandas as pd
import condicoes_iniciais as ci
import plotagens as plt
import threading

BASE = Path(__file__).resolve().parent
DATADIR = BASE / "data"
DATADIR.mkdir(parents=True, exist_ok=True)

class Lorenz80GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Lorenz80 - Simulador de Modelos")
        self.root.geometry("600x500")

        # Centralizar a janela principal
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Variáveis de controle
        self.model_type = tk.IntVar()
        self.df = None
        self.out_file = None
        
        # Valores iniciais
        self.x0 = ci.x0
        self.y0 = ci.y0
        self.z0 = ci.z0
        self.days = ci.days
        self.f = ci.f

        # Configurar estilo
        style = ttk.Style()
        style.configure('TLabel', anchor=tk.CENTER)
        style.configure('TLabelframe.Label', anchor=tk.CENTER)
        style.theme_use('clam')
        
        # Criar interface principal
        self.create_main_interface()
        self.open_initial_conditions_window()

    def open_initial_conditions_window(self):
        ic_window = tk.Toplevel(self.root)
        ic_window.title("Definir Condições Iniciais")
        ic_window.geometry("500x500")
        ic_window.resizable(False, False)
        
        ic_window.transient(self.root)
        ic_window.grab_set()
        ic_window.grid_columnconfigure(0, weight=1)

        frame = ttk.Frame(ic_window, padding="20")
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)
        
        ttk.Label(frame, text="Condições Iniciais", font=('Arial', 14, 'bold')).grid(row=0, column=0, columnspan=3, pady=(0, 10))

        # Entradas para x, y, z
        labels = ["X", "Y", "Z"]
        self.entries = {}
        for i, var_name in enumerate(labels):
            ttk.Label(frame, text=f"{var_name}:").grid(row=i*2+1, column=0, columnspan=3, sticky="w", pady=(5,0))
            for j in range(3):
                key = f"{var_name.lower()}{j+1}"
                self.entries[key] = ttk.Entry(frame, width=10)
                self.entries[key].grid(row=i*2+2, column=j, padx=5, pady=2)

        # Entradas para f e dias
        ttk.Label(frame, text="f:").grid(row=7, column=0, columnspan=3, sticky="w", pady=(10,0))
        for j in range(3):
            key = f"f{j+1}"
            self.entries[key] = ttk.Entry(frame, width=10)
            self.entries[key].grid(row=8, column=j, padx=5, pady=2)

        ttk.Label(frame, text="Dias:").grid(row=9, column=0, sticky="w", pady=(10,0))
        self.entries['days'] = ttk.Entry(frame, width=10)
        self.entries['days'].grid(row=9, column=1, columnspan=2, sticky="w", padx=5)

        def set_harley_conditions():
            self.entries['x1'].delete(0, tk.END); self.entries['x1'].insert(0, str(ci.x0[0]))
            self.entries['x2'].delete(0, tk.END); self.entries['x2'].insert(0, str(ci.x0[1]))
            self.entries['x3'].delete(0, tk.END); self.entries['x3'].insert(0, str(ci.x0[2]))
            self.entries['y1'].delete(0, tk.END); self.entries['y1'].insert(0, str(ci.y0[0]))
            self.entries['y2'].delete(0, tk.END); self.entries['y2'].insert(0, str(ci.y0[1]))
            self.entries['y3'].delete(0, tk.END); self.entries['y3'].insert(0, str(ci.y0[2]))
            self.entries['z1'].delete(0, tk.END); self.entries['z1'].insert(0, str(ci.z0[0]))
            self.entries['z2'].delete(0, tk.END); self.entries['z2'].insert(0, str(ci.z0[1]))
            self.entries['z3'].delete(0, tk.END); self.entries['z3'].insert(0, str(ci.z0[2]))

        # set_harley_conditions() # Preenche com os valores iniciais

        def save_conditions():
            try:
                self.x0 = [float(self.entries['x1'].get()), float(self.entries['x2'].get()), float(self.entries['x3'].get())]
                self.y0 = [float(self.entries['y1'].get()), float(self.entries['y2'].get()), float(self.entries['y3'].get())]
                self.z0 = [float(self.entries['z1'].get()), float(self.entries['z2'].get()), float(self.entries['z3'].get())]
                self.f = [float(self.entries['f1'].get()), float(self.entries['f2'].get()), float(self.entries['f3'].get())]
                self.days = int(self.entries['days'].get())
                
                # Atualiza ci para que as simulações usem os novos valores
                ci.x0, ci.y0, ci.z0 = self.x0, self.y0, self.z0
                ci.f, ci.days = self.f, self.days

                ic_window.destroy()
            except ValueError:
                messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos.", parent=ic_window)

        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=10, column=0, columnspan=3, pady=20)
        
        harley_btn = ttk.Button(btn_frame, text="Usar Condições de Harley", command=set_harley_conditions)
        harley_btn.pack(pady=5)

        save_btn = ttk.Button(btn_frame, text="Salvar", command=save_conditions)
        save_btn.pack(pady=5)

        cancel_btn = ttk.Button(btn_frame, text="Cancelar", command=ic_window.destroy)
        cancel_btn.pack(pady=5)

        self.root.wait_window(ic_window)
    
    def create_main_interface(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="SIMULADOR LORENZ80", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="ew")
        
        # Seção de seleção de modelo
        model_frame = ttk.LabelFrame(main_frame, text="Seleção do Modelo", padding="15")
        model_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        model_frame.grid_columnconfigure(0, weight=1)
        
        pe_radio = ttk.Radiobutton(model_frame, text="PE Model", variable=self.model_type, value=1)
        pe_radio.grid(row=0, column=0, pady=5)
        
        be_radio = ttk.Radiobutton(model_frame, text="BE Model", variable=self.model_type, value=2)
        be_radio.grid(row=1, column=0, pady=5)
        
        qg_radio = ttk.Radiobutton(model_frame, text="QG Model", variable=self.model_type, value=3)
        qg_radio.grid(row=2, column=0, pady=5)
        
        # Botão para executar simulação
        simulate_btn = ttk.Button(main_frame, text="Executar Simulação", command=self.execute_simulation)
        simulate_btn.grid(row=2, column=0, columnspan=2, pady=15)
        
        # Frame para botões de funcionalidades
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=3, column=0, columnspan=2, pady=15)
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=1)
        
        # Botões das funcionalidades
        self.clean_btn = ttk.Button(buttons_frame, text="Limpeza de Dados", 
                                   command=self.open_data_cleaning_window, state='disabled')
        self.clean_btn.grid(row=0, column=0, padx=(0, 5), sticky="e")
        
        self.plot_btn = ttk.Button(buttons_frame, text="Opções Gráficas", 
                                  command=self.open_plotting_window, state='disabled')
        self.plot_btn.grid(row=0, column=1, padx=(5, 0), sticky="w")
        
        # Barra de progresso
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=4, column=0, columnspan=2, sticky="ew", pady=15)
        
        # Label de status
        self.status_label = ttk.Label(main_frame, text="Selecione um modelo e execute a simulação")
        self.status_label.grid(row=5, column=0, columnspan=2, pady=10, sticky="ew")
    
    def execute_simulation(self):
        if self.model_type.get() == 0:
            messagebox.showerror("Erro", "Por favor, selecione um modelo!")
            return
        
        # Executar simulação em thread separada
        self.progress.start()
        self.status_label.config(text="Executando simulação...")
        
        thread = threading.Thread(target=self._run_simulation)
        thread.daemon = True
        thread.start()
    
    def _run_simulation(self):
        try:
            model = self.model_type.get()
            
            if model == 1:  # PE Model
                self.df = sim.pe_simulate(ci.x0, ci.y0, ci.z0, ci.days)
                self.out_file = DATADIR / "pe_model.csv"
                model_name = "PE Model"
            elif model == 2:  # BE Model
                self.df = sim.be_simulate(ci.y0, ci.days)
                self.out_file = DATADIR / "be_model.csv"
                model_name = "BE Model"
            elif model == 3:  # QG Model
                self.df = sim.qg_simulate(ci.y0, ci.days)
                self.out_file = DATADIR / "qg_model.csv"
                model_name = "QG Model"
            
            self.df.to_csv(self.out_file, index=False)
            
            # Atualizar interface na thread principal
            self.root.after(0, self._simulation_complete, model_name)
            
        except Exception as e:
            self.root.after(0, self._simulation_error, str(e))
    
    def _simulation_complete(self, model_name):
        self.progress.stop()
        self.status_label.config(text=f"Simulação {model_name} concluída!")
        self.clean_btn.config(state='normal')
        self.plot_btn.config(state='normal')
        messagebox.showinfo("Sucesso", f"Simulação {model_name} concluída!\nArquivo salvo em: {self.out_file}")
    
    def _simulation_error(self, error_msg):
        self.progress.stop()
        self.status_label.config(text="Erro na simulação")
        messagebox.showerror("Erro", f"Erro durante a simulação: {error_msg}")
    
    def open_data_cleaning_window(self):
        # Janela de limpeza de dados
        clean_window = tk.Toplevel(self.root)
        clean_window.title("Limpeza de Dados")
        clean_window.geometry("400x350")
        clean_window.resizable(False, False)
        
        # Centralizar janela
        clean_window.transient(self.root)
        clean_window.grab_set()
        clean_window.grid_columnconfigure(0, weight=1)

        frame = ttk.Frame(clean_window, padding="20")
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)
        
        ttk.Label(frame, text="Limpeza de Dados", font=('Arial', 14, 'bold'), anchor=tk.CENTER).grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="ew")
        
        # Opções de limpeza
        ttk.Label(frame, text="Percentual de dados para remover:", anchor=tk.CENTER).grid(row=1, column=0, columnspan=2, sticky="ew", pady=5)
        
        clean_var = tk.DoubleVar(value=15.0)
        clean_scale = ttk.Scale(frame, from_=0, to=50, variable=clean_var, orient=tk.HORIZONTAL)
        clean_scale.grid(row=2, column=0, columnspan=2, sticky="ew", pady=5)
        
        clean_label = ttk.Label(frame, text="15.0%", anchor=tk.CENTER)
        clean_label.grid(row=3, column=0, columnspan=2, pady=5, sticky="ew")
        
        def update_label(val):
            clean_label.config(text=f"{float(val):.1f}%")
        
        clean_scale.config(command=update_label)
        
        # Informações sobre os dados
        if self.df is not None:
            ttk.Label(frame, text=f"Total de registros: {len(self.df)}", anchor=tk.CENTER).grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")
        
        # Barra de progresso e status
        progress = ttk.Progressbar(frame, mode='indeterminate')
        progress.grid(row=5, column=0, columnspan=2, sticky="ew", pady=15)
        status_label = ttk.Label(frame, text="", anchor=tk.CENTER)
        status_label.grid(row=6, column=0, columnspan=2, sticky="ew")

        # Botões
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=7, column=0, columnspan=2, pady=20)
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)

        def apply_cleaning():
            percentage = clean_var.get()
            if percentage > 0:
                progress.start()
                status_label.config(text="Limpando dados...")
                
                def do_cleaning():
                    try:
                        original_len = len(self.df)
                        n_remove = int(original_len * (percentage / 100))
                        self.df = self.df.iloc[n_remove:].reset_index(drop=True)
                        self.df.to_csv(self.out_file, index=False)
                        
                        def on_complete():
                            progress.stop()
                            messagebox.showinfo("Sucesso", 
                                              f"Limpeza concluída!\nRemovidos {n_remove} registros ({percentage:.1f}%)")
                            clean_window.destroy()
                        
                        self.root.after(0, on_complete)
                    except Exception as e:
                        def on_error():
                            progress.stop()
                            messagebox.showerror("Erro", f"Falha na limpeza: {e}")
                        self.root.after(0, on_error)

                threading.Thread(target=do_cleaning, daemon=True).start()
            else:
                messagebox.showinfo("Info", "Nenhuma limpeza aplicada.")
                clean_window.destroy()
        
        apply_btn = ttk.Button(btn_frame, text="Aplicar", command=apply_cleaning)
        apply_btn.grid(row=0, column=0, padx=(0, 5), sticky="e")
        
        cancel_btn = ttk.Button(btn_frame, text="Cancelar", command=clean_window.destroy)
        cancel_btn.grid(row=0, column=1, padx=(5, 0), sticky="w")
    
    def open_plotting_window(self):
        # Janela de opções gráficas
        plot_window = tk.Toplevel(self.root)
        plot_window.title("Opções Gráficas")
        plot_window.geometry("500x600")
        plot_window.resizable(False, False)
        
        # Centralizar janela
        plot_window.transient(self.root)
        plot_window.grab_set()
        plot_window.grid_columnconfigure(0, weight=1)
        
        frame = ttk.Frame(plot_window, padding="20")
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)
        
        ttk.Label(frame, text="Opções Gráficas", font=('Arial', 14, 'bold'), anchor=tk.CENTER).grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="ew")
        
        # Variável para seleção do gráfico
        plot_option = tk.IntVar()
        
        # Opções baseadas no tipo de modelo
        model = self.model_type.get()
        if model == 2 or model == 3:  # BE ou QG Model
            options = [
                (1, "Projeção y1 vs y2"),
                (2, "Projeção y1 vs y3"),
                (3, "Projeção y2 vs y3"),
                (4, "Evolução temporal de y1"),
                (5, "Evolução temporal de y2"),
                (6, "Evolução temporal de y3")
            ]
        else:  # PE Model
            options = [
                (1, "Projeção y1 vs y2"),
                (2, "Projeção y1 vs y3"),
                (3, "Projeção y2 vs y3"),
                (4, "Evolução temporal de y1, x1, z1")
            ]
        
        # Criar radiobuttons para as opções
        radio_frame = ttk.Frame(frame)
        radio_frame.grid(row=1, column=0, columnspan=2, sticky="ew")
        radio_frame.grid_columnconfigure(0, weight=1)

        for i, (value, text) in enumerate(options):
            ttk.Radiobutton(radio_frame, text=text, variable=plot_option, 
                           value=value).grid(row=i, column=0, sticky="w", pady=2)
        
        # Barra de progresso e status
        progress = ttk.Progressbar(frame, mode='indeterminate')
        progress.grid(row=2, column=0, columnspan=2, sticky="ew", pady=15)
        status_label = ttk.Label(frame, text="", anchor=tk.CENTER)
        status_label.grid(row=3, column=0, columnspan=2, sticky="ew")

        # Botões
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)
        
        def generate_plot():
            option = plot_option.get()
            if option == 0:
                messagebox.showerror("Erro", "Por favor, selecione uma opção gráfica!")
                return
            
            progress.start()
            status_label.config(text="Gerando gráfico...")

            def do_plotting():
                try:
                    model = self.model_type.get()
                    filename = ""
                    
                    if model == 2 or model == 3:  # BE ou QG Model
                        if option == 1: filename = plt.plotagem_y1y2(self.df, model)
                        elif option == 2: filename = plt.plotagem_y1y3(self.df, model)
                        elif option == 3: filename = plt.plotagem_y2y3(self.df, model)
                        elif option == 4: filename = plt.plotagem_temporal(self.df, model, "y1")
                        elif option == 5: filename = plt.plotagem_temporal(self.df, model, "y2")
                        elif option == 6: filename = plt.plotagem_temporal(self.df, model, "y3")
                    else:  # PE Model
                        if option == 1: filename = plt.plotagem_y1y2(self.df, model)
                        elif option == 2: filename = plt.plotagem_y1y3(self.df, model)
                        elif option == 3: filename = plt.plotagem_y2y3(self.df, model)
                        elif option == 4: filename = plt.plotagem_xyz_temporal(self.df, model)
                    
                    def on_complete():
                        progress.stop()
                        status_label.config(text="")
                        messagebox.showinfo("Sucesso", f"Gráfico salvo em: src/{filename}")
                    
                    self.root.after(0, on_complete)
                    
                except Exception as e:
                    def on_error():
                        progress.stop()
                        status_label.config(text="Erro!")
                        messagebox.showerror("Erro", f"Erro ao gerar gráfico: {str(e)}")
                    self.root.after(0, on_error)

            threading.Thread(target=do_plotting, daemon=True).start()
        
        generate_btn = ttk.Button(btn_frame, text="Gerar Gráfico", command=generate_plot)
        generate_btn.grid(row=0, column=0, padx=(0, 5), sticky="e")
        
        close_btn = ttk.Button(btn_frame, text="Fechar", command=plot_window.destroy)
        close_btn.grid(row=0, column=1, padx=(5, 0), sticky="w")

def main():
    root = tk.Tk()
    app = Lorenz80GUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
