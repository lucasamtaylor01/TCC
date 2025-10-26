using DifferentialEquations, Plots, DataFrames, CSV, Random

"""
epsilon // sigma
1 // 310.58595100575906
0.1 // 142.6677313864854
0.001 // 5.754046294922591
"""
sigma = 5.754046294922591
x0 = 0.1
tspan = (0.0, 100.0)

f1(X, p, t) = X - X^3
f2(X, p, t) = p

prob = SDEProblem(f1, f2, x0, tspan, sigma)
solucao_estocastico = solve(prob, EM(), dt = 1e-3, seed = 13865062)

df = DataFrame(t = solucao_estocastico.t, x = solucao_estocastico.u)
cd(@__DIR__)  
CSV.write("data/estocastico001.csv", df)
println("Dados estocasticos salvos em: data/estocastico001.csv")
