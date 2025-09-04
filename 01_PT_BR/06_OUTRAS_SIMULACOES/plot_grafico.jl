using CSV, DataFrames, Plots

# Ler a solução salva
df = CSV.read("data/solucao.csv", DataFrame)

# Tempo em dias
td = df.time ./ 8

# Plotar apenas primeiras componentes
plot(td, df.x1, label="x1", color=:green, lw=1.5)
plot!(td, df.y1, label="y1", color=:blue, lw=1.5)
plot!(td, df.z1, label="z1", color=:red, lw=1.5)

xlabel!("t (dias)")
title!("Evolução temporal (10 dias)")

# Salvar figura
savefig("src/to_funcionando.png")
