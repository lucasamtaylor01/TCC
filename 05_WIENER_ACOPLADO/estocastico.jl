using DifferentialEquations, Plots, DataFrames, CSV, Random
# sigma 100 =  3.386312749237008 <-- absoluto
# sigma 50 = 5.11993063128531
# sigma 10  =  7.758285992948718

sigma = 5.11993063128531
x0 = 0.1
tspan = (0.0, 50.0)

f1(X, p, t) = X - X^3
f2(X, p, t) = p


# θ = 1.0      # taxa de reversão
# μ = 0.0      # média de reversão
# σ = 1.0      # intensidade do ruído
# x0 = 0.1     # valor inicial
# t0 = 0.0     # tempo inicial

# W = OrnsteinUhlenbeckProcess(θ, μ, σ, x0, t0)


#prob = SDEProblem(f1, f2, x0, tspan, sigma; noise = W)
prob = SDEProblem(f1, f2, x0, tspan, sigma)
solucao_estocastico = solve(prob, EM(), dt = 1e-3, seed = 12)

df = DataFrame(t = solucao_estocastico.t, x = solucao_estocastico.u)
cd(@__DIR__)  
CSV.write("data/estocastico_50.csv", df)
print("Dados estocásticos salvos em: data/estocastico_50.csv")