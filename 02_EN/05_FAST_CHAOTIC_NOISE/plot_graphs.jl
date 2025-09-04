using DataFrames, Plots, CSV

cd(@__DIR__)

df_deterministic = CSV.read("data/deterministic.csv", DataFrame)
df_stochastic = CSV.read("data/stochastic.csv", DataFrame)

t = df_deterministic[:, 1]
x_deterministic = df_deterministic[:, 3]
x_stochastic = df_stochastic[:, 2]

isdir("src") || mkdir("src")

figsize = (1280, 720)

plt1 = plot(t, x_deterministic, title="Deterministic", xlabel="t", ylabel="x", size=figsize)
savefig(plt1, "src/deterministic_plot.png")

plt2 = plot(t, x_stochastic, title="Stochastic", xlabel="t", ylabel="x", size=figsize)
savefig(plt2, "src/stochastic_plot.png")

hist1 = histogram(x_deterministic, bins=100, title="Deterministic Histogram", xlabel="x", ylabel="Frequency", size=figsize)
savefig(hist1, "src/hist_deterministic.png")

hist2 = histogram(x_stochastic, bins=100, title="Stochastic Histogram", xlabel="x", ylabel="Frequency", size=figsize)
savefig(hist2, "src/hist_stochastic.png")
