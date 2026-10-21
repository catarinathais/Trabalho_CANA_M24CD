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

3. **Etapa 3 — Análise Experimental e Relatório
