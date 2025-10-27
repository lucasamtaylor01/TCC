using DifferentialEquations
using CSV
using DataFrames

# legal mudar os valores
alpha = 0.5
omega = 2.0
beta = 1.0 + 0.5im    # pode ser complexo
sigma = 0.25

# Forma OUT-OF-PLACE (retorna Complex)
f(z, p, t) = (alpha + im*omega) * z - beta * z * abs2(z)
g(z, p, t) = sigma                   

z0    = 1.0 + 0.0im
tspan = (0.0, 75.0)

prob = SDEProblem(f, g, z0, tspan)
sol  = solve(prob, EM(), dt=0.001)  

# Criar DataFrame com os resultados
df = DataFrame(t=sol.t, real=real.(sol.u), imag=imag.(sol.u))

outfile = joinpath(@__DIR__, "slo.csv")
CSV.write(outfile, df)
println("Dados salvos em: $outfile")