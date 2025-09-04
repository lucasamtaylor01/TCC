using DifferentialEquations, Plots, DataFrames, CSV

sigma = 8.880502080440465
x0 = 0.1
tspan = (0.0, 1.0)

f1(X, p, t) = X - X^3
f2(X, p, t) = p

W = WienerProcess(0.0, 0.0)
prob = SDEProblem(f1, f2, x0, tspan, sigma; noise = W)
stochastic_solution = solve(prob, EM(), dt = 1e-3)

df = DataFrame(t = stochastic_solution.t, x = stochastic_solution.u)
cd(@__DIR__)  
CSV.write("data/stochastic.csv", df)
