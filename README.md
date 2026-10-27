# Trabalho Prático: Divisão e Conquista

**Dupla:** Catarina Pimentel e Hafiz Costa  
**Data de Entrega:** 28/10/2026  
**Linguagem de Programação:** Python 3.11+

---

## 1. Visão Geral do Projeto

Este repositório contém a implementação completa, a bateria de testes de borda, os dados brutos de avaliação experimental e o relatório técnico do **Trabalho Prático de Divisão e Conquista**, contemplando:

1. **Etapa 1 — Subarranjo de Soma Máxima (`src/etapa1_subarranjo.py`)**:
   - **Força Bruta** em $\Theta(n^2)$: testa todos os intervalos possíveis $[i, j]$ com acumulador incremental.
   - **Divisão e Conquista** em $\Theta(n \log n)$: divide o vetor ao meio, resolve recursivamente as metades esquerda e direita e calcula em $\Theta(n)$ o melhor subarranjo que cruza o ponto médio.
   - **Questão Desafio (Algoritmo de Kadane)** em $\Theta(n)$: varredura linear mantendo a mesma regra determinística de desempate (maior soma $
ightarrow$ menor índice inicial $
ightarrow$ menor índice final).

2. **Etapa 2 — Par de Pontos Mais Próximos no Plano (`src/etapa2_pontos_proximos.py`)**:
   - **Força Bruta** em $\Theta(n^2)$: compara todos os $n(n-1)/2$ pares de estações.
   - **Divisão e Conquista Pura** em $\Theta(n \log n)$ (`limiar_fb = 3`): pré-ordena os pontos por $x$ e por $y$, divide na mediana de $x$, resolve recursivamente cada metade ($\delta$) e inspeciona a faixa central de largura $2\delta$ comparando cada ponto com **no máximo 7 vizinhos** ordenados por $y$.
   - **Divisão e Conquista Híbrida** em $\Theta(n \log n)$ (`limiar_fb = 24`): aciona a Força Bruta nas folhas da árvore de recursão quando $n \le 24$, reduzindo em até ~34% o tempo de execução ao eliminar o *overhead* de chamadas recursivas em subproblemas pequenos.

3. **Etapa 3 — Análise Experimental e Relatório (`src/etapa3_experimentos.py`, `data/` e `docs/`)**:
   - Medições de tempo para entradas crescentes ($n \in \{100, 200, 400, 800, 1.600, 3.200, 6.400\}$) com média e desvio padrão de 5 execuções por tamanho, além de varredura do limiar $k$ e análise do ponto de cruzamento (*crossover*).

---

## 2. Estrutura de Diretórios

```text
repo_divisao_e_conquista/
├── README.md                                           # Instruções de execução e especificação da máquina
├── .gitignore                                          # Arquivos ignorados pelo Git
├── src/
│   ├── __init__.py
│   ├── etapa1_subarranjo.py                            # Etapa 1: Força Bruta O(n²), D&C O(n log n) e Kadane O(n)
│   ├── etapa2_pontos_proximos.py                       # Etapa 2: Força Bruta O(n²), D&C Puro e D&C Híbrido (k=24)
│   └── etapa3_experimentos.py                          # Etapa 3: Benchmark automatizado, geração de CSV e gráficos
├── tests/
│   ├── casos_de_teste.txt                              # Arquivo legível com as entradas, saídas esperadas e justificativas
│   ├── casos_de_teste.json                             # Casos de teste estruturados para leitura automatizada
│   └── test_suite.py                                   # Bateria de testes unitários e testes de estresse aleatórios
├── data/
│   ├── medicoes_brutas.csv                             # Arquivo CSV com todas as medições brutas (315 execuções)
│   └── resumo_experimentos.json                        # Médias, desvios padrões e speedups consolidados
└── docs/
    ├── Relatorio_Divisao_e_Conquista_Catarina_Hafiz.pdf # Relatório Técnico final em PDF (8 páginas)
    ├── fig1_etapa1_tempos.png                          # Gráficos da Etapa 1 (Linear e Log-Log)
    ├── fig2_etapa2_tempos.png                          # Gráficos da Etapa 2 (Linear e Log-Log)
    ├── fig3_limiar_e_cruzamento.png                    # Gráficos de cruzamento e calibração do limiar k
    └── fig4_geometria_faixa_7_vizinhos.png             # Diagrama geométrico da faixa 2δ × δ (7 vizinhos)
```

---

## 3. Instruções de Execução

### 3.1. Pré-requisitos
- **Python 3.10+** (testado em Python 3.11.2).
- As implementações das **Etapas 1 e 2** e a **bateria de testes (`test_suite.py`)** utilizam exclusivamente a **biblioteca padrão do Python** (`math`, `sys`, `unittest`, `json`, `random`, `time`), não exigindo instalação de pacotes externos para avaliação na bateria do professor.
- Apenas para regerar os gráficos da Etapa 3 (`etapa3_experimentos.py`), utiliza-se `matplotlib`.

### 3.2. Executando a Bateria Completa de Testes Automatizados
A partir da raiz do repositório, execute:

```bash
python3 tests/test_suite.py
```

### 3.3. Executando a Etapa 1 (Subarranjo de Soma Máxima)
O script `src/etapa1_subarranjo.py` lê da entrada padrão (`stdin`) ou de um arquivo (`--arquivo`) no formato do enunciado (`n` seguido de `n` inteiros):

```bash
# Executar todos os algoritmos (Força Bruta, Divisão e Conquista e Kadane O(n)):
echo "16 13 -3 -25 20 -3 -16 -23 18 20 -7 12 -5 -22 15 -4 7" | python3 src/etapa1_subarranjo.py

# Executar apenas um algoritmo específico (fb, dc ou kadane) com saída enxuta "<soma> <inicio> <fim>":
echo "6 -15 -8 -23 -3 -12 -9" | python3 src/etapa1_subarranjo.py --algoritmo dc
```

### 3.4. Executando a Etapa 2 (Par de Pontos Mais Próximos)
O script `src/etapa2_pontos_proximos.py` lê um inteiro `n` seguido de `n` pares de coordenadas `x y`:

```bash
# Executar todos os algoritmos (Força Bruta, D&C Puro k=3 e D&C Híbrido k=24):
printf "6\n-10 0\n-10 10\n-0.2 5\n0.2 5\n10 0\n10 10\n" | python3 src/etapa2_pontos_proximos.py

# Executar apenas Divisão e Conquista Híbrida com limiar customizado:
printf "6\n-10 0\n-10 10\n-0.2 5\n0.2 5\n10 0\n10 10\n" | python3 src/etapa2_pontos_proximos.py --algoritmo hibrido --limiar 24
```

### 3.5. Reproduzindo os Experimentos e Gráficos da Etapa 3
```bash
python3 src/etapa3_experimentos.py
```

---

## 4. Configuração da Máquina Utilizada nos Experimentos

- **Processador (CPU):** Intel(R) Xeon(R) Platinum 8481C @ 2.20 GHz (2 vCPUs, x86_64, Cache L1d 48 KiB, L1i 32 KiB, L2 2 MiB, L3 105 MiB)
- **Memória RAM:** 7,8 GiB DDR5
- **Sistema Operacional:** Linux Kernel 6.12.105+ SMP x86_64
- **Interpretador:** Python 3.11.2 (CPython)
