using DifferentialEquations, ModelingToolkit, Plots

@parameters t
@variables x[1:3](t) y[1:3](t) z[1:3](t)
D = Differential(t)

vector_a = [1.0, 1.0, 3.0]
vector_b = [
    0.5 * (vector_a[1] - vector_a[2] - vector_a[3]),
    0.5 * (vector_a[2] - vector_a[3] - vector_a[1]),
    0.5 * (vector_a[3] - vector_a[1] - vector_a[2])
]
c = sqrt(3/4)
vector_h = [-1.0, 0.0, 0.0]
vector_f = [0.1, 0.0, 0.0]
g_0, kappa_0, nu_0 = 8.0, 1/48, 1/48

eqs = [
    D(x[i]) ~ (
        vector_a[i]*vector_b[i]*x[(i % 3) + 1]*x[((i+1) % 3) + 1]
        - c*(vector_a[i]-vector_a[((i+1) % 3) + 1])*x[(i % 3) + 1]*y[((i+1) % 3) + 1]
        + c*(vector_a[i]-vector_a[((i+1) % 3) + 1])*x[(i % 3) + 1]*y[((i+1) % 3) + 1]
        - c*(vector_a[i]-vector_a[(i % 3) + 1])*y[(i % 3) + 1]*x[((i+1) % 3) + 1]
        - 2*c^2*y[i]*y[((i+1) % 3) + 1]
        - nu_0*vector_a[i]^2*x[i]
        + vector_a[i]*y[i] - vector_a[i]*z[i]
    ) / vector_a[i] for i in 1:3
]

append!(eqs, [
    D(y[i]) ~ (
        -vector_a[((i+1) % 3) + 1]*vector_b[((i+1) % 3) + 1]*x[(i % 3) + 1]*y[((i+1) % 3) + 1]
        - vector_a[(i % 3) + 1]*vector_b[(i % 3) + 1]*y[(i % 3) + 1]*x[((i+1) % 3) + 1]
        + c*(vector_a[((i+1) % 3) + 1]-vector_a[(i % 3) + 1])*y[(i % 3) + 1]*y[((i+1) % 3) + 1]
        - vector_a[i]*x[i] - nu_0*vector_a[i]^2*y[i]
    ) / vector_a[i] for i in 1:3
])

append!(eqs, [
    D(z[i]) ~ (
        -vector_b[((i+1) % 3) + 1]*x[(i % 3) + 1]*(z[((i+1) % 3) + 1]-vector_h[((i+1) % 3) + 1])
        - vector_b[(i % 3) + 1]*(z[(i % 3) + 1]-vector_h[(i % 3) + 1])*x[((i+1) % 3) + 1]
        + c*y[(i % 3) + 1]*(z[((i+1) % 3) + 1]-vector_h[((i+1) % 3) + 1])
        - c*(z[(i % 3) + 1]-vector_h[(i % 3) + 1])*y[((i+1) % 3) + 1]
        + g_0*vector_a[i]*x[i] - kappa_0*vector_a[i]*z[i] + vector_f[i]
    ) for i in 1:3
])

@mtkbuild sys = ODESystem(eqs, t)

x0, y0, z0 = [0.1, 0.0, 0.0], [0.1, 0.0, 0.0], [0.1, 0.0, 0.0]
u0 = vcat(x0, y0, z0)
tspan = (0.0, 8*1.0)

prob = ODEProblem(sys, u0, tspan)
sol = solve(prob, RK4(); abstol=1e-6, reltol=1e-8, saveat=0.01)

td = sol.t ./ 8
U = Array(sol)
X, Y, Z = U[1:3, :]', U[4:6, :]', U[7:9, :]'

plot(td, X[:,1], label="x1", color=:green, lw=1.5)
plot!(td, Y[:,1], label="y1", color=:blue, lw=1.5)
plot!(td, Z[:,1], label="z1", color=:red, lw=1.5)
xlabel!("t (dias)")
title!("Evolução temporal (10 dias)")
