# Explicação do cálculo de σ (sigma) em calculo_sigma.py

Este documento explica, linha a linha, o funcionamento do código Python utilizado para calcular o coeficiente de difusão efetivo σ a partir de uma série temporal, conforme a teoria de ruído caótico rápido.

---

```python
def sigma_from_y2(y2, dt, lam=1.0):
```
Define uma função para calcular σ a partir da série temporal `y2`, do passo de tempo `dt` e do parâmetro λ (`lam`).

```python
    y = y2 - np.mean(y2)
```
Centraliza a série removendo a média (necessário para autocorrelação correta).

```python
    n = len(y)
```
Obtém o número de pontos da série temporal.

```python
    nfft = n
```
Define o tamanho da FFT igual ao tamanho da série (sem zero-padding).

```python
    fy = np.fft.rfft(y, n=nfft)
```
Calcula a FFT rápida (apenas frequências reais) da série centralizada.

```python
    ac = np.fft.irfft(fy * np.conj(fy), n=nfft)[:n] / np.arange(n, 0, -1)
```
Calcula a autocorrelação via FFT e normaliza cada lag pelo número de pares disponíveis.

```python
    sigma2 = 2 * lam**2 * dt * np.sum(ac)
```
Aproxima a integral da autocorrelação multiplicando pela constante \(2\lambda^2\) e pelo passo de tempo.

```python
    return np.sqrt(max(sigma2, 0.0))
```
Retorna σ (raiz quadrada de σ²), garantindo que não seja negativo.

---

```python
csv_path = os.path.join(os.path.dirname(__file__), "data", "deterministico.csv")
```
Monta o caminho para o arquivo CSV de dados, relativo ao diretório do script.

```python
df = pd.read_csv(csv_path)
```
Lê o arquivo CSV em um DataFrame do pandas.

```python
dt = df["t"][1] - df["t"][0]
```
Calcula o passo de tempo a partir da coluna de tempo do DataFrame.

```python
sigma = sigma_from_y2(df["y2"].to_numpy(), dt)
```
Chama a função para calcular σ usando os dados da coluna `y2` e o passo de tempo.

```python
print("σ ≈", sigma)
```
Imprime o valor aproximado de σ.

---