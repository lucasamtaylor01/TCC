using DifferentialEquations, DataFrames, CSV, Random

"""
    epsilon // sigma
    0.5 // 262.7908097705843
    0.2 // 205.05745681770404
    0.1 // 142.6677313864854
    0.01 // 5.754046294922591
"""

eps = 0.1

if eps == 0.5
    sigma = 242.69367736299662
elseif eps == 0.2
    sigma = 205.05745681770404
elseif eps == 0.1
    sigma = 142.6677313864854
elseif eps == 0.01
    sigma = 5.754046294922591
else
    error("Valor de epsilon inválido. Use 0.5, 0.2 ou 0.1.")
    exit()
end
x0 = 0.1
tspan = (0.0, 100.0)

f1(X, p, t) = X - X^3
f2(X, p, t) = p

prob = SDEProblem(f1, f2, x0, tspan, sigma)
solucao_estocastico = solve(prob, EM(), dt = 1e-3, seed = 13865062)

df = DataFrame(t = solucao_estocastico.t, x = solucao_estocastico.u)
cd(@__DIR__)

# Gerar nome do arquivo baseado no epsilon
if eps == 0.5
    eps_suffix = "_05"
elseif eps == 0.2
    eps_suffix = "_02"
elseif eps == 0.1
    eps_suffix = "_01"
elseif eps == 0.01
    eps_suffix = "_001"
end

filename = "data/estocastico$(eps_suffix).csv"
CSV.write(filename, df)
println("Dados estocasticos salvos em: $filename")
