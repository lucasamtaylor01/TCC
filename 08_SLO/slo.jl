using DifferentialEquations
using CSV
using DataFrames


alpha = 0.5
omega = 2.0
beta = 1.0 + 0.5im
sigma = 0.25

f(z, p, t) = (alpha + im*omega) * z - beta * z * abs2(z)
g(z, p, t) = sigma                   

z0    = 1.0 + 0.0im
tspan = (0.0, 75.0)

prob = SDEProblem(f, g, z0, tspan)
sol  = solve(prob, EM(), dt=0.001)  

df = DataFrame(t=sol.t, real=real.(sol.u), imag=imag.(sol.u))

outfile = joinpath(@__DIR__, "slo.csv")
CSV.write(outfile, df)
println("Dados salvos em: $outfile")