# Brownian motion

using DifferentialEquations, DataFrames, CSV
import StochasticDiffEq as SDE

f(u,p,t) = mu*u
g(u,p,t)= sigma
dt = 1/365
mu = 0.05
sigma = 0.3
tspan = (0.0, 1.0)
u0= 12
prob = SDEProblem(f,g,u0,tspan, seed=15)
sol = SDE.solve(prob, EM(), dt = dt);

# Salvar dados em CSV
df = DataFrame(t = sol.t, x = sol.u)
cd(@__DIR__)  
CSV.write("data/stock_market.csv", df)
println("Dados salvos em: data/stock_market.csv")