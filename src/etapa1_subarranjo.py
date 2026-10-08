"""
Etapa 1: Subarranjo de Soma Máxima (Maximum Subarray Problem)
Autores: Catarina Pimentel e Hafiz Costa

Descrição:
Dada a variação diária do preço de uma ação (com valores positivos e negativos),
encontra o intervalo contínuo de dias [inicio, fim] em que um investidor teria obtido
o maior ganho acumulado.

Critério de desempate padronizado (determinístico):
1. Maior soma acumulada;
2. Menor índice de início (intervalo que ocorre mais cedo);
3. Menor índice de fim (menor comprimento em caso de empate no início, ex: prefixo de soma zero).

Nota sobre indexação:
As funções internas retornam índices baseados em 0 (0-indexed: 0 <= inicio <= fim < n).
A interface de linha de comando (CLI) suporta exibição em base 0 (padrão) ou base 1 (--one-indexed).
"""

import sys
from typing import List, Tuple


def _melhor_intervalo(cand1: Tuple[int, int, int], cand2: Tuple[int, int, int]) -> Tuple[int, int, int]:
    """
    Compara dois intervalos candidatos (soma, inicio, fim) aplicando a regra determinística
    de desempate: maior soma -> menor índice de início -> menor índice de fim.
    """
    s1, i1, f1 = cand1
    s2, i2, f2 = cand2
    if s1 != s2:
        return cand1 if s1 > s2 else cand2
    if i1 != i2:
        return cand1 if i1 < i2 else cand2
    return cand1 if f1 <= f2 else cand2


def subarranjo_forca_bruta(arr: List[int]) -> Tuple[int, int, int]:
    """
    1. Força Bruta: Testa todos os intervalos possíveis [i, j] em O(n²).
    Mantém um acumulador incremental a partir de i para evitar um terceiro laço O(n³).

    Retorna:
        (soma_maxima, indice_inicio, indice_fim) em indexação base 0.
    """
    n = len(arr)
    if n == 0:
        raise ValueError("O vetor de entrada não pode ser vazio.")

    melhor = (arr[0], 0, 0)

    for i in range(n):
        soma_atual = 0
        for j in range(i, n):
            soma_atual += arr[j]
            candidato = (soma_atual, i, j)
            melhor = _melhor_intervalo(melhor, candidato)

    return melhor


def _subarranjo_cruzando_meio(arr: List[int], esq: int, meio: int, dir_: int) -> Tuple[int, int, int]:
    """
    Calcula em O(n) o melhor subarranjo que obrigatoriamente cruza o índice `meio`
    (ou seja, contém arr[meio] e arr[meio + 1]).
    """
    # Expande do meio para a esquerda
    soma_esq = arr[meio]
    melhor_soma_esq = soma_esq
    melhor_i = meio

    for i in range(meio - 1, esq - 1, -1):
        soma_esq += arr[i]
        # Em caso de empate na soma à esquerda, preferimos o menor índice i (regra de desempate)
        if soma_esq >= melhor_soma_esq:
            melhor_soma_esq = soma_esq
            melhor_i = i

    # Expande de meio + 1 para a direita
    soma_dir = arr[meio + 1]
    melhor_soma_dir = soma_dir
    melhor_j = meio + 1

    for j in range(meio + 2, dir_ + 1):
        soma_dir += arr[j]
        # Em caso de empate na soma à direita, preferimos o menor índice j (regra de desempate)
        if soma_dir > melhor_soma_dir:
            melhor_soma_dir = soma_dir
            melhor_j = j

    return (melhor_soma_esq + melhor_soma_dir, melhor_i, melhor_j)


def _subarranjo_dc_recursivo(arr: List[int], esq: int, dir_: int) -> Tuple[int, int, int]:
    """
    Função auxiliar recursiva para Divisão e Conquista.
    Recorrência: T(n) = 2T(n/2) + Theta(n) => Theta(n log n).
    """
    if esq == dir_:
        return (arr[esq], esq, esq)

    meio = (esq + dir_) // 2

    cand_esq = _subarranjo_dc_recursivo(arr, esq, meio)
    cand_dir = _subarranjo_dc_recursivo(arr, meio + 1, dir_)
    cand_meio = _subarranjo_cruzando_meio(arr, esq, meio, dir_)

    melhor = _melhor_intervalo(cand_esq, cand_meio)
    melhor = _melhor_intervalo(melhor, cand_dir)
    return melhor


def subarranjo_divisao_e_conquista(arr: List[int]) -> Tuple[int, int, int]:
    """
    2. Divisão e Conquista: Divide o vetor ao meio, resolve cada metade recursivamente
    e calcula, em O(n), o melhor subarranjo que cruza o meio.
    Complexidade de tempo: O(n log n). Complexidade de espaço: O(log n) na pilha.

    Retorna:
        (soma_maxima, indice_inicio, indice_fim) em indexação base 0.
    """
    n = len(arr)
    if n == 0:
        raise ValueError("O vetor de entrada não pode ser vazio.")
    return _subarranjo_dc_recursivo(arr, 0, n - 1)


def subarranjo_kadane_linear(arr: List[int]) -> Tuple[int, int, int]:
    """
    3. Questão Desafio — Algoritmo de Kadane em O(n):
    Percorre o vetor uma única vez mantendo a soma máxima do subarranjo terminando
    na posição atual, respeitando exatamente a mesma regra determinística de desempate
    (maior soma -> menor início -> menor fim).

    Complexidade de tempo: O(n). Complexidade de espaço: O(1).
    """
    n = len(arr)
    if n == 0:
        raise ValueError("O vetor de entrada não pode ser vazio.")

    melhor = (arr[0], 0, 0)
    soma_atual = arr[0]
    inicio_atual = 0

    for j in range(1, n):
        # Se soma_atual >= 0, estender o subarranjo anterior mantém ou aumenta a soma
        # com um índice de início menor (`inicio_atual` < `j`), satisfazendo o desempate!
        if soma_atual >= 0:
            soma_atual += arr[j]
        else:
            soma_atual = arr[j]
            inicio_atual = j

        candidato = (soma_atual, inicio_atual, j)
        melhor = _melhor_intervalo(melhor, candidato)

    return melhor


def ler_entrada_texto(texto: str) -> List[int]:
    """
    Lê a entrada no formato especificado pelo enunciado:
    'um inteiro n seguido de uma sequência de n inteiros.'
    """
    tokens = texto.strip().split()
    if not tokens:
        raise ValueError("Entrada vazia.")
    n = int(tokens[0])
    valores = [int(x) for x in tokens[1:1 + n]]
    if len(valores) != n:
        raise ValueError(f"Esperados {n} inteiros, mas foram fornecidos {len(valores)}.")
    return valores


def main() -> None:
    """Execução via linha de comando lendo da entrada padrão (stdin) ou argumentos."""
    import argparse
    parser = argparse.ArgumentParser(description="Etapa 1: Subarranjo de Soma Máxima")
    parser.add_argument(
        "--algoritmo",
        choices=["fb", "dc", "kadane", "todos"],
        default="todos",
        help="Algoritmo a executar: fb (Força Bruta), dc (Divisão e Conquista), kadane (Linear O(n)), ou todos."
    )
    parser.add_argument(
        "--arquivo",
        type=str,
        default=None,
        help="Caminho para arquivo de entrada (se omitido, lê de stdin)."
    )
    args = parser.parse_args()

    if args.arquivo:
        with open(args.arquivo, "r", encoding="utf-8") as f:
            conteudo = f.read()
    else:
        conteudo = sys.stdin.read()

    arr = ler_entrada_texto(conteudo)

    if args.algoritmo in ("fb", "todos"):
        s, ini, fim = subarranjo_forca_bruta(arr)
        if args.algoritmo == "fb":
            print(f"{s} {ini} {fim}")
        else:
            print(f"[Força Bruta O(n²)]          Soma Máxima = {s}, Início = {ini}, Fim = {fim}")

    if args.algoritmo in ("dc", "todos"):
        s, ini, fim = subarranjo_divisao_e_conquista(arr)
        if args.algoritmo == "dc":
            print(f"{s} {ini} {fim}")
        else:
            print(f"[Divisão e Conquista O(nlogn)] Soma Máxima = {s}, Início = {ini}, Fim = {fim}")

    if args.algoritmo in ("kadane", "todos"):
        s, ini, fim = subarranjo_kadane_linear(arr)
        if args.algoritmo == "kadane":
            print(f"{s} {ini} {fim}")
        else:
            print(f"[Desafio Kadane O(n)]        Soma Máxima = {s}, Início = {ini}, Fim = {fim}")


if __name__ == "__main__":
    main()
