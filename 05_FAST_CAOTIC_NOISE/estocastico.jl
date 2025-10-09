using DifferentialEquations, Plots, DataFrames, CSV, Random
# sigma 100 =  3.386312749237008 <-- absoluto
# sigma 50 = 5.11993063128531
# sigma 10  =  7.758285992948718

sigma = 7.758285992948718
x0 = 0.1
tspan = (0.0, 50.0)

f1(X, p, t) = X - X^3
f2(X, p, t) = p

prob = SDEProblem(f1, f2, x0, tspan, sigma)
solucao_estocastico = solve(prob, EM(), dt = 1e-3, seed = 12)

df = DataFrame(t = solucao_estocastico.t, x = solucao_estocastico.u)
cd(@__DIR__)  
CSV.write("data/estocastico.csv", df)
println("Dados estocasticos salvos em: data/estocastico.csv")
