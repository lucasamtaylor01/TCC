# COMPARANDO DIFERENTES SOLVERS COM tspan = (0.0, 1.0)
## Input

```julia
@benchmark solve(prob, Tsit5())
```


## Output

```
BenchmarkTools.Trial: 40 samples with 1 evaluation per sample.
 Range (min … max):   51.833 ms … 596.956 ms  ┊ GC (min … max):  0.00% … 87.89%
 Time  (median):      97.369 ms               ┊ GC (median):    33.91%
 Time  (mean ± σ):   125.675 ms ± 111.888 ms  ┊ GC (mean ± σ):  45.83% ± 28.42%

   █▄                                                            
  ▃██▃▃▅▆▃▆█▁▅▃▁▁▁▃▁▃▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▃▁▁▁▃ ▁
  51.8 ms          Histogram: frequency by time          597 ms <

 Memory estimate: 114.34 MiB, allocs estimate: 2325119.
``` 

## Input

```julia
@benchmark solve(prob, Rodas4())
```


## Output
```
BenchmarkTools.Trial: 11 samples with 1 evaluation per sample.
 Range (min … max):  393.699 ms … 889.444 ms  ┊ GC (min … max):  0.00% … 53.90%
 Time  (median):     422.862 ms               ┊ GC (median):     0.00%
 Time  (mean ± σ):   479.776 ms ± 141.263 ms  ┊ GC (mean ± σ):  13.91% ± 16.69%

    █          ▃                                                 
  ▇▇█▇▇▁▁▁▁▇▁▁▁█▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▇ ▁
  394 ms           Histogram: frequency by time          889 ms <

 Memory estimate: 131.08 MiB, allocs estimate: 2118013.
``` 


## Input
```julia
@benchmark solve(prob, Rosenbrock23())
``` 

## Output
```
BenchmarkTools.Trial: 9 samples with 1 evaluation per sample.
 Range (min … max):  414.657 ms …    1.122 s  ┊ GC (min … max):  0.00% … 60.59%
 Time  (median):     543.681 ms               ┊ GC (median):    19.31%
 Time  (mean ± σ):   625.557 ms ± 234.621 ms  ┊ GC (mean ± σ):  31.40% ± 19.72%

  █   █   ██ ███                             █                █  
  █▁▁▁█▁▁▁██▁███▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁█▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁█ ▁
  415 ms           Histogram: frequency by time          1.12 s <

 Memory estimate: 231.30 MiB, allocs estimate: 3668550.
 ```


Melhor desempenho: `Tsit5()`

# TESTE StaticArrays

Pedi pro chat, adicionar StaticArrays, ele sugeriu algumas mudanças. Vamos comparar a forma que eu fiz, com a forma que ele fez


## Meu jeito


```
BenchmarkTools.Trial: 40 samples with 1 evaluation per sample.
 Range (min … max):   51.833 ms … 596.956 ms  ┊ GC (min … max):  0.00% … 87.89%
 Time  (median):      97.369 ms               ┊ GC (median):    33.91%
 Time  (mean ± σ):   125.675 ms ± 111.888 ms  ┊ GC (mean ± σ):  45.83% ± 28.42%

   █▄                                                            
  ▃██▃▃▅▆▃▆█▁▅▃▁▁▁▃▁▃▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▃▁▁▁▃ ▁
  51.8 ms          Histogram: frequency by time          597 ms <

 Memory estimate: 114.34 MiB, allocs estimate: 2325119.
``` 

## Jeito do chat
```
BenchmarkTools.Trial: 42 samples with 1 evaluation per sample.
 Range (min … max):   60.205 ms … 808.596 ms  ┊ GC (min … max):  0.00% … 91.50%
 Time  (median):      95.929 ms               ┊ GC (median):    28.98%
 Time  (mean ± σ):   121.236 ms ± 115.237 ms  ┊ GC (mean ± σ):  41.05% ± 25.88%

   █                                                             
  ▆█▅█▅▄▅▁▃▄▃▁▁▁▃▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▃ ▁
  60.2 ms          Histogram: frequency by time          809 ms <

 Memory estimate: 114.37 MiB, allocs estimate: 2325767.
 ``` 
 mesma coisa...