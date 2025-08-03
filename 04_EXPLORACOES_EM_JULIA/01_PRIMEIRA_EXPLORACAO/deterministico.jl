<<<<<<< HEAD
using DifferentialEquations, ModelingToolkit, Plots, BenchmarkTools, Sundials
=======
using DifferentialEquations, ModelingToolkit, Plots
>>>>>>> 268b12396ba343992d39f3f750afb01bdfdcaa83

@independent_variables t
@variables x(t)=0.1 y1(t)=0.01 y2(t)=0.01 y3(t)=0.01
@parameters ϵ=0.01 λ=1.0
D = Differential(t)

eqs = [
    D(x) ~  x - x^3 + (λ/ϵ) * y2,
    D(y1) ~ (10 / ϵ^2) * (y2 - y1),
    D(y2) ~ (1 / ϵ^2) * (28*y1 - y2 - y1*y3),  
    D(y3) ~ (1 / ϵ^2) * (y1*y2 - (8/3)*y3)
]

@mtkbuild sys = ODESystem(eqs, t)

tspan = (0.0, 1.0)
prob = ODEProblem(sys, [], tspan)
solucao_deterministico = solve(prob, Tsit5(), reltol=1e-6, abstol=1e-7, saveat=1e-3)


y2_vals = solucao_deterministico[3, :]
y2_centered = y2_vals .- mean(y2_vals)
plot(solucao_deterministico.t, y2_vals)
