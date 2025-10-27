using DifferentialEquations, Plots, DataFrames, CSV, Random


"""
    DADOS SUJOS
    epsilon // sigma
    0.5 // 262.7908097705843
    0.2 // 205.05745681770404
    0.1 // 142.6677313864854
    0.01 // 5.754046294922591
    0.001 // 

    DADOS LIMPO
    epsilon // sigma
    0.5 // 242.69367736299662
    0.1 // 131.61514092019132
    0.01 // 3.6184719820043227
    0.001 // 
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
