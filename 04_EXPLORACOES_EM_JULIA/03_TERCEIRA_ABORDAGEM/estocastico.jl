# Sistema estocástico

using DifferentialEquations, Plots

sigma = 0.9
x0 = 0.1
tspan = (0.0, 1.0)

f1(X, p, t) = X - X^3
f2(X, p, t) = sigma

W = WienerProcess(0.0, 0.0, 0.0)
prob = SDEProblem(f1, f2, x0, tspan, noise=W)
sola = solve(prob, EM(), dt=0.01)

plot(sola.t, sola.u;
     label = "X(t)",
     xlabel = "Tempo",
     ylabel = "X",
     title = "Modelo estocástico",
     size = (960, 540),
     color = :red,
     linewidth = 1.5)

