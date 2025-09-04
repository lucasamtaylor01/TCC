using DifferentialEquations, ModelingToolkit, CSV, DataFrames

@parameters t
@variables x[1:3](t) y[1:3](t) z[1:3](t)
D = Differential(t)

a = [1.0, 1.0, 3.0]
b = [0.5 * (a[1] - a[2] - a[3]), 0.5 * (a[2] - a[3] - a[1]), 0.5 * (a[3] - a[1] - a[2])]
c = sqrt(3/4)
h = [-1.0, 0.0, 0.0]
f = [0.1, 0.0, 0.0]
g_0, kappa_0, nu_0 = 8.0, 1/48, 1/48

eqs = [
    D(x[i]) ~ (
        a[i]*b[i]*x[(i % 3) + 1]*x[((i+1) % 3) + 1]
        - c*(a[i]-a[((i+1) % 3) + 1])*x[(i % 3) + 1]*y[((i+1) % 3) + 1]
        - 2*c^2*y[i]*y[((i+1) % 3) + 1]
        - nu_0*a[i]^2*x[i]
        + a[i]*y[i] - a[i]*z[i]
    ) / a[i] for i in 1:3
]
append!(eqs, [
    D(y[i]) ~ (
        -a[((i+1) % 3) + 1]*b[((i+1) % 3) + 1]*x[(i % 3) + 1]*y[((i+1) % 3) + 1]
        - a[(i % 3) + 1]*b[(i % 3) + 1]*y[(i % 3) + 1]*x[((i+1) % 3) + 1]
        - a[i]*x[i] - nu_0*a[i]^2*y[i]
    ) / a[i] for i in 1:3
])
append!(eqs, [
    D(z[i]) ~ (
        -b[((i+1) % 3) + 1]*x[(i % 3) + 1]*(z[((i+1) % 3) + 1]-h[((i+1) % 3) + 1])
        - b[(i % 3) + 1]*(z[(i % 3) + 1]-h[(i % 3) + 1])*x[((i+1) % 3) + 1]
        + c*y[(i % 3) + 1]*(z[((i+1) % 3) + 1]-h[((i+1) % 3) + 1])
        - c*(z[(i % 3) + 1]-h[(i % 3) + 1])*y[((i+1) % 3) + 1]
        + g_0*a[i]*x[i] - kappa_0*a[i]*z[i] + f[i]
    ) for i in 1:3
])

@mtkbuild sys = ODESystem(eqs, t)

x0, y0, z0 = [0.1, 0.0, 0.0], [0.1, 0.0, 0.0], [0.1, 0.0, 0.0]
u0 = vcat(x0, y0, z0)
tspan = (0.0, 80.0)

sol = solve(ODEProblem(sys, u0, tspan), Tsit5(); abstol=1e-6, reltol=1e-8, saveat=0.01)

U = Array(sol)
df = DataFrame(time = sol.t, x1 = U[1,:], x2 = U[2,:], x3 = U[3,:], y1 = U[4,:], y2 = U[5,:], y3 = U[6,:],z1 = U[7,:], z2 = U[8,:], z3 = U[9,:])

cd(@__DIR__)  
isdir("data") || mkdir("data")
CSV.write("data/solucao.csv", df)
