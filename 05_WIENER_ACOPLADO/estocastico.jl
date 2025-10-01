using DifferentialEquations, Plots, DataFrames, CSV, Random

sigma = 6.358148733765899
x0 = 0.1
tspan = (0.0, 10.0)

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
CSV.write("data/estocastico.csv", df)