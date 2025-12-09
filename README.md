# Uma abordagem estocástica para modelos rápidos-lentos 🔀

## 📝 Descrição

O presente trabalho tem como objetivo estudar a aproximação de sistemas dinâmicos rápidos-lentos por meio de equações diferenciais estocásticas, com ênfase no modelo de Lorenz 80. Como principal referência metodológica, este trabalho segue a abordagem proposta no artigo [_Stochastic rectification of fast oscillations on slow manifold closures_](https://doi.org/10.1073/pnas.2113650118)

Este repositório tem o objetivo de organizar todos os arquivos e materiais relacionados ao desenvolvimento do meu Trabalho de Conclusão de Curso (TCC).



## ⚙️ Instalação
   1. Clone o repositório:
      ```bash
      git clone https://github.com/lucasamtaylor01/Lorenz80_SDE.git
      ```
   2. Instale as dependências necessárias
      ```bash
      python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements_python.txt
      ```

      ```bash
      julia -e 'using Pkg; Pkg.add.(readlines("requirements_julia.txt"))'
      ```
   3. Executar programa selecionado

# 📹 Vídeo de divugação

[Divulgação TCC: Uma abordagem estocástica para modelos rápidos-lentos](https://youtu.be/KnpaK2REErE?si=Z3FjLvyAioy-mtbh)
