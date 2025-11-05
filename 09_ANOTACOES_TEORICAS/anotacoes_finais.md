# Slow manifold
1. Primeiro, temos que o sistema é um modelo rápido-lento, i.e., são sistemas que exibem interações entre variáveis que evoluem em escalas de tempo muito diferentes
2. O *slow manifold* é uma superfície no espaço de fases onde as variáveis rápidas estão em equilíbrio em função das lentas.
    > Dynamically, the slow OPM provides the manifold on which lies the average motion of the neglected fast variables as a function of the resolved scales.
3. Temos que as variáveis são
    - $y_i$: rotacionais lentos (movimentos geostróficos);
    - $x_i, z_i$: componentes rápidos (ondas de gravidade).

4. Reinterpretação **estatística** de *Slow Manifold*: *slow optimal parameterizing manifold (OPM)*. 
    >“Recently, in the context of the slow manifold problem for the atmosphere, the concept of a slow manifold has been revisited as that of a slow optimal parameterizing manifold (OPM) (16).

O artigo formaliza o OPM como o minimizador do erro médio quadrático entre $Y$ e $\Psi(X)$

5. O acoplamento entre lento e rápido se torna tão forte que um slow manifold determinístico deixa de existir.
    >$R > R^*_0$ an explosive breakdown of slow-to-fast deterministic parameterizations is observed… After this transition, a stochastic parameterization of the fast oscillations is required 

    o equilíbrio que definia a variedade lenta é destruído — as variáveis rápidas passam a oscilar fortemente e de modo imprevisível.

# BE Manifold 
1. **O modelo BE é um manifold?**

    O modelo BE define o que o artigo chama de BE manifold, que é uma aproximação determinística de um slow manifold. Na seção “The L80 Model and the Balance Equation Closure”, os autores explicam que o BE (Balance Equation) surge como uma forma analítica de filtrar as oscilações rápidas (ondas de gravidade) e descrever apenas a evolução lenta (ondas de Rossby)
    
    > Leith’s idea was to filter out, on an analytical basis, the fast gravity waves for the initialization of the primitive equations of the atmosphere… The L80 model … is its paradigmatic successor both for the generalization of slow balance and for slow–fast coupling.
2. **Por que ele é usado como base da aproximação estatística?**

    Pelo trabalho anterior, chegou-se a conclusão de que: reproduz bem o valor médio condicional das rápidas ($\Psi^*$).

3. **Como ele é definido?** 

    Ver *Material and Methods*

# Ruído
## Ruelle-Pollicot Ressonances
> The RP resonances are defined as the eigenvalues of the generator (Kolmogorov operator) of a given stochastic system

RPR são os autovalores do gerador (operador de Kolmogorov) associado a um sistema estocástico de equações diferenciais (SDE):
$$dX = F(X) dt + D(X)dW_t$$

e o gerador atua como:
$$Kf = F \cdot \nabla f + \frac{1}{2} \nabla \cdot (\Sigma \nabla f) \quad \Sigma = DD^T$$

Descrevem o decaimento e as frequências das correlações

