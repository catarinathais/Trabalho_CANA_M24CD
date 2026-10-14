"""
Etapa 2: Par de Pontos Mais Próximos (Closest Pair of Points)
Autores: Catarina Pimentel e Hafiz Costa

Descrição:
Dadas as coordenadas de n estações de monitoramento em um plano, encontra as duas
estações mais próximas entre si (menor distância euclidiana).

Implementações:
1. Força Bruta: Compara todos os pares em O(n²).
2. Divisão e Conquista pura: Divide na mediana de x, resolve recursivamente cada metade (limiar base n <= 3)
   e verifica a faixa central de largura 2*delta comparando cada ponto com no máximo 7 vizinhos ordenados por y.
   Complexidade: O(n log n).
3. Divisão e Conquista Híbrida (com limiar ajustável): Utiliza Força Bruta quando o subproblema atinge
   n <= limiar (threshold) experimentalmente calibrado, reduzindo o overhead de chamadas recursivas.
"""

import sys
import math
from typing import List, Tuple

Ponto = Tuple[float, float, int]  # (x, y, id_original)
ResultadoPar = Tuple[float, Tuple[float, float], Tuple[float, float], Tuple[int, int]]


def distancia_euclidiana(p1: Ponto, p2: Ponto) -> float:
    """Calcula a distância euclidiana entre dois pontos no plano."""
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])


def _normalizar_par(p1: Ponto, p2: Ponto) -> Tuple[Ponto, Ponto]:
    """Ordena o par de pontos pelo índice original para garantir determinismo."""
    return (p1, p2) if p1[2] <= p2[2] else (p2, p1)


def _melhor_par(
    cand1: Tuple[float, Ponto, Ponto],
    cand2: Tuple[float, Ponto, Ponto],
    tol: float = 1e-12
) -> Tuple[float, Ponto, Ponto]:
    """
    Desempata dois pares candidatos (dist, p1, p2) de forma determinística:
    1. Menor distância (com tolerância numérica de ponto flutuante);
    2. Menor par de índices originais (id1, id2).
    """
    d1, a1, b1 = cand1
    d2, a2, b2 = cand2
    if abs(d1 - d2) > tol:
        return cand1 if d1 < d2 else cand2
    par_ids1 = (a1[2], b1[2])
    par_ids2 = (a2[2], b2[2])
    return cand1 if par_ids1 <= par_ids2 else cand2


def _forca_bruta_nucleo(pontos: List[Ponto]) -> Tuple[float, Ponto, Ponto]:
    """Núcleo O(n²) que compara todos os pares de uma lista de pontos."""
    n = len(pontos)
    a0, b0 = _normalizar_par(pontos[0], pontos[1])
    melhor = (distancia_euclidiana(a0, b0), a0, b0)

    for i in range(n):
        p_i = pontos[i]
        for j in range(i + 1, n):
            p_j = pontos[j]
            d = distancia_euclidiana(p_i, p_j)
            if d <= melhor[0] + 1e-12:
                pa, pb = _normalizar_par(p_i, p_j)
                melhor = _melhor_par(melhor, (d, pa, pb))
    return melhor


def par_mais_proximo_forca_bruta(coordenadas: List[Tuple[float, float]]) -> ResultadoPar:
    """
    1. Força Bruta: Compara todos os n(n-1)/2 pares de pontos em O(n²).

    Retorna:
        (menor_distancia, (x1, y1), (x2, y2), (id1, id2))
    """
    if len(coordenadas) < 2:
        raise ValueError("São necessários pelo menos 2 pontos.")
    pontos: List[Ponto] = [(float(x), float(y), idx) for idx, (x, y) in enumerate(coordenadas)]
    d, p1, p2 = _forca_bruta_nucleo(pontos)
    return (d, (p1[0], p1[1]), (p2[0], p2[1]), (p1[2], p2[2]))


def _dc_recursivo(px: List[Ponto], py: List[Ponto], limiar_fb: int) -> Tuple[float, Ponto, Ponto]:
    """
    Passo recursivo de Divisão e Conquista mantendo pontos pré-ordenados por X (px) e por Y (py).
    Recorrência: T(n) = 2T(n/2) + Theta(n) => O(n log n).
    """
    n = len(px)
    if n <= limiar_fb:
        return _forca_bruta_nucleo(px)

    meio = n // 2
    ponto_mediano = px[meio - 1]
    x_mediano = ponto_mediano[0]

    px_esq = px[:meio]
    px_dir = px[meio:]

    # Particiona py em py_esq e py_dir em O(n) preservando a ordenação por y
    ids_esq = {p[2] for p in px_esq}
    py_esq = [p for p in py if p[2] in ids_esq]
    py_dir = [p for p in py if p[2] not in ids_esq]

    melhor_esq = _dc_recursivo(px_esq, py_esq, limiar_fb)
    melhor_dir = _dc_recursivo(px_dir, py_dir, limiar_fb)
    melhor = _melhor_par(melhor_esq, melhor_dir)
    delta = melhor[0]

    # Filtra apenas os pontos na faixa de largura 2*delta em torno de x_mediano (ordenados por y)
    faixa = [p for p in py if abs(p[0] - x_mediano) <= delta + 1e-12]

    # Para cada ponto na faixa, compara com no máximo os 7 vizinhos seguintes ordenados por y
    m = len(faixa)
    for i in range(m):
        p_i = faixa[i]
        limite_j = min(i + 8, m)  # no máximo 7 vizinhos: i+1, i+2, ..., i+7
        for j in range(i + 1, limite_j):
            p_j = faixa[j]
            if (p_j[1] - p_i[1]) > delta + 1e-12:
                break
            d = distancia_euclidiana(p_i, p_j)
            if d <= delta + 1e-12:
                pa, pb = _normalizar_par(p_i, p_j)
                melhor = _melhor_par(melhor, (d, pa, pb))
                delta = melhor[0]

    return melhor


def par_mais_proximo_divisao_e_conquista(
    coordenadas: List[Tuple[float, float]],
    limiar_fb: int = 3
) -> ResultadoPar:
    """
    2. Divisão e Conquista em O(n log n):
    - Ordena inicialmente os pontos por x e por y com a função padrão da linguagem (Timsort).
    - Divide pela mediana das coordenadas x.
    - Resolve recursivamente cada metade obtendo delta.
    - Verifica a faixa de largura 2*delta comparando cada ponto com no máximo 7 vizinhos ordenados por y.

    Parâmetros:
        coordenadas: lista de tuplas (x, y).
        limiar_fb: tamanho do caso base em que a recursão delega para força bruta (padrão=3 para D&C puro,
                   ou limiar experimental ótimo como 24 na versão híbrida).

    Retorna:
        (menor_distancia, (x1, y1), (x2, y2), (id1, id2))
    """
    if len(coordenadas) < 2:
        raise ValueError("São necessários pelo menos 2 pontos.")
    if limiar_fb < 3:
        limiar_fb = 3

    pontos: List[Ponto] = [(float(x), float(y), idx) for idx, (x, y) in enumerate(coordenadas)]

    # Ordenação inicial por X e por Y usando a biblioteca padrão
    px = sorted(pontos, key=lambda p: (p[0], p[1], p[2]))
    py = sorted(pontos, key=lambda p: (p[1], p[0], p[2]))

    d, p1, p2 = _dc_recursivo(px, py, limiar_fb=limiar_fb)
    return (d, (p1[0], p1[1]), (p2[0], p2[1]), (p1[2], p2[2]))


def ler_pontos_texto(texto: str) -> List[Tuple[float, float]]:
    """
    Lê pontos no formato:
    Inteiro n na primeira linha (ou primeiro token), seguido de n pares de coordenadas (x, y).
    """
    tokens = texto.strip().split()
    if not tokens:
        raise ValueError("Entrada vazia.")
    n = int(tokens[0])
    coords = []
    idx = 1
    for _ in range(n):
        x = float(tokens[idx])
        y = float(tokens[idx + 1])
        coords.append((x, y))
        idx += 2
    return coords


def main() -> None:
    """Execução via linha de comando."""
    import argparse
    parser = argparse.ArgumentParser(description="Etapa 2: Par de Pontos Mais Próximos")
    parser.add_argument(
        "--algoritmo",
        choices=["fb", "dc", "hibrido", "todos"],
        default="todos",
        help="Algoritmo a executar: fb, dc (limiar=3), hibrido (limiar=24) ou todos."
    )
    parser.add_argument(
        "--limiar",
        type=int,
        default=24,
        help="Limiar para o caso base do algoritmo híbrido (padrão: 24)."
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

    pontos = ler_pontos_texto(conteudo)

    if args.algoritmo in ("fb", "todos"):
        d, p1, p2, ids = par_mais_proximo_forca_bruta(pontos)
        if args.algoritmo == "fb":
            print(f"{d:.6f} ({p1[0]}, {p1[1]}) ({p2[0]}, {p2[1]}) {ids[0]} {ids[1]}")
        else:
            print(f"[Força Bruta O(n²)]           Dist = {d:.6f}, Pontos = {p1} e {p2} (índices {ids[0]}, {ids[1]})")

    if args.algoritmo in ("dc", "todos"):
        d, p1, p2, ids = par_mais_proximo_divisao_e_conquista(pontos, limiar_fb=3)
        if args.algoritmo == "dc":
            print(f"{d:.6f} ({p1[0]}, {p1[1]}) ({p2[0]}, {p2[1]}) {ids[0]} {ids[1]}")
        else:
            print(f"[Divisão e Conquista O(nlogn)] Dist = {d:.6f}, Pontos = {p1} e {p2} (índices {ids[0]}, {ids[1]})")

    if args.algoritmo in ("hibrido", "todos"):
        d, p1, p2, ids = par_mais_proximo_divisao_e_conquista(pontos, limiar_fb=args.limiar)
        if args.algoritmo == "hibrido":
            print(f"{d:.6f} ({p1[0]}, {p1[1]}) ({p2[0]}, {p2[1]}) {ids[0]} {ids[1]}")
        else:
            print(f"[D&C Híbrido (limiar={args.limiar:2d})]      Dist = {d:.6f}, Pontos = {p1} e {p2} (índices {ids[0]}, {ids[1]})")


if __name__ == "__main__":
    main()
