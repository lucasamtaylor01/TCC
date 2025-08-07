using DataFrames, Plots, CSV

cd(@__DIR__) 

# Ler os dados
df_deterministico = CSV.read("data/deterministico.csv", DataFrame)
df_estocastico = CSV.read("data/estocastico.csv", DataFrame)

# Extrair colunas
t = df_deterministico[:, 1]
x_deterministico = df_deterministico[:, 3]
x_estocastico = df_estocastico[:, 2]

# Plot determinístico
plt1 = plot(t, x_deterministico, title="Determinístico", xlabel="t", ylabel="x")
savefig(plt1, "src/deterministico_plot.png")

# Plot estocástico
plt2 = plot(t, x_estocastico, title="Estocástico", xlabel="t", ylabel="x")
savefig(plt2, "src/estocastico_plot.png")

# Histograma determinístico
hist1 = histogram(x_deterministico, bins=100, title="Histograma Determinístico", xlabel="x", ylabel="Frequência")
savefig(hist1, "src/hist_deterministico.png")

# Histograma estocástico
hist2 = histogram(x_estocastico, bins=100, title="Histograma Estocástico", xlabel="x", ylabel="Frequência")
savefig(hist2, "src/hist_estocastico.png")
