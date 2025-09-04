using CSV, DataFrames, Plots

df = CSV.read("data/solution.csv", DataFrame)

td = df.time ./ 8

plot(td, df.x1, label="x1", color=:green, lw=1.5)
plot!(td, df.y1, label="y1", color=:blue, lw=1.5)
plot!(td, df.z1, label="z1", color=:red, lw=1.5)

xlabel!("t (days)")
title!("Time evolution (1 day)")

savefig("src/lorenz80_1day.png")
