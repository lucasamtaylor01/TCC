using DataFrames, Plots, CSV, Statistics, StatsBase, DSP

cd(@__DIR__)
df = CSV.read("data/deterministico.csv", DataFrame)

y2_vals = df[:, 2]
t_vals = df[:,1]
Δt = 1e-3

y2_centered = y2_vals .- mean(y2_vals)

acor = xcorr(y2_centered; scaling = :coeff)
n = length(y2_centered)
acor_pos = acor[n:end]  # lags ≥ 0

λ = 1.0

σ² = 2 * λ^2 * sum(acor_pos) * Δt
σ = sqrt(σ²)

println(σ)
