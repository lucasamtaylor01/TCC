using DifferentialEquations, DataFrames, CSV
import StochasticDiffEq as SDE

f(u,p,t) = mu*u
g(u,p,t)= sigma
dt = 1/(365*24)
mu = 0.05
sigma = 1.0
tspan = (0.0, 1.0)
u0= 12
prob = SDEProblem(f,g,u0,tspan, seed=13865062)
sol = SDE.solve(prob, EM(), dt = dt);

# Salvar dados em CSV
df = DataFrame(t = sol.t, x = sol.u)

outfile = joinpath(@__DIR__, "stockmarket.csv")
CSV.write(outfile, df)
println("Dados salvos em: $outfile")