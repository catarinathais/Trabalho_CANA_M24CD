"""
Etapa 3: Análise Experimental e Geração de Medições Brutas / Gráficos
Autores: Catarina Pimentel e Hafiz Costa

Mede o tempo de execução para tamanhos crescentes de entrada (100, 200, 400, 800, 1600, 3200, 6400),
com média de 5 execuções por tamanho, além de um experimento de micro-benchmark para tamanhos pequenos
(n de 4 a 128) e varredura do limiar (threshold) da Etapa 2 (k de 2 a 256).
Salva todas as medições brutas em CSV e gera os gráficos em alta resolução.
"""

import os
import sys
import csv
import json
import time
import math
import random
import statistics
from typing import List, Dict, Any

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.etapa1_subarranjo import (
    subarranjo_forca_bruta,
    subarranjo_divisao_e_conquista,
    subarranjo_kadane_linear,
)
from src.etapa2_pontos_proximos import (
    par_mais_proximo_forca_bruta,
    par_mais_proximo_divisao_e_conquista,
)

REPO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(REPO_DIR, "data")
DOCS_DIR = os.path.join(REPO_DIR, "docs")
INTERMEDIATE_DIR = "/working_dir/c_4730cbeece04baf4/artifacts/file_generation/ttl=63d/intermediate"
OUTPUT_DIR = "/working_dir/c_4730cbeece04baf4/artifacts/file_generation/ttl=63d/output"

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(DOCS_DIR, exist_ok=True)


def executar_experimentos() -> None:
    tamanhos_principais = [100, 200, 400, 800, 1600, 3200, 6400]
    num_execucoes = 5

    registros_brutos: List[Dict[str, Any]] = []
    resumo_etapa1: List[Dict[str, Any]] = []
    resumo_etapa2: List[Dict[str, Any]] = []

    print("=== Iniciando Experimentos da Etapa 1 (Subarranjo de Soma Máxima) ===")
    for n in tamanhos_principais:
        tempos_fb = []
        tempos_dc = []
        tempos_kd = []

        for rep in range(1, num_execucoes + 1):
            rng = random.Random(10000 * n + rep)
            vetor = [rng.randint(-1000, 1000) for _ in range(n)]

            # Força Bruta O(n^2)
            t0 = time.perf_counter()
            res_fb = subarranjo_forca_bruta(vetor)
            t_fb = (time.perf_counter() - t0) * 1000.0  # ms
            tempos_fb.append(t_fb)
            registros_brutos.append({
                "etapa": "Etapa 1 - Subarranjo",
                "algoritmo": "Forca Bruta O(n^2)",
                "n": n,
                "limiar": "-",
                "execucao": rep,
                "tempo_ms": round(t_fb, 6),
                "resultado_verificacao": res_fb[0]
            })

            # Divisão e Conquista O(n log n)
            t0 = time.perf_counter()
            res_dc = subarranjo_divisao_e_conquista(vetor)
            t_dc = (time.perf_counter() - t0) * 1000.0  # ms
            tempos_dc.append(t_dc)
            registros_brutos.append({
                "etapa": "Etapa 1 - Subarranjo",
                "algoritmo": "Divisao e Conquista O(n log n)",
                "n": n,
                "limiar": "-",
                "execucao": rep,
                "tempo_ms": round(t_dc, 6),
                "resultado_verificacao": res_dc[0]
            })

            # Kadane O(n) - Questão Desafio
            t0 = time.perf_counter()
            res_kd = subarranjo_kadane_linear(vetor)
            t_kd = (time.perf_counter() - t0) * 1000.0  # ms
            tempos_kd.append(t_kd)
            registros_brutos.append({
                "etapa": "Etapa 1 - Subarranjo",
                "algoritmo": "Kadane Desafio O(n)",
                "n": n,
                "limiar": "-",
                "execucao": rep,
                "tempo_ms": round(t_kd, 6),
                "resultado_verificacao": res_kd[0]
            })

            assert res_fb == res_dc == res_kd, f"Inconsistência na Etapa 1 para n={n}"

        m_fb, sd_fb = statistics.mean(tempos_fb), statistics.stdev(tempos_fb)
        m_dc, sd_dc = statistics.mean(tempos_dc), statistics.stdev(tempos_dc)
        m_kd, sd_kd = statistics.mean(tempos_kd), statistics.stdev(tempos_kd)
        resumo_etapa1.append({
            "n": n,
            "fb_media_ms": m_fb, "fb_dp_ms": sd_fb,
            "dc_media_ms": m_dc, "dc_dp_ms": sd_dc,
            "kd_media_ms": m_kd, "kd_dp_ms": sd_kd,
            "speedup_dc_vs_fb": m_fb / m_dc,
            "speedup_kd_vs_dc": m_dc / m_kd
        })
        print(f"n={n:4d} | FB={m_fb:9.3f} ms | D&C={m_dc:7.3f} ms | Kadane={m_kd:6.4f} ms | Speedup D&C={m_fb/m_dc:6.1f}x")

    print("\n=== Iniciando Experimentos da Etapa 2 (Par de Pontos Mais Próximos) ===")
    for n in tamanhos_principais:
        tempos_fb = []
        tempos_dc = []
        tempos_hyb = []

        for rep in range(1, num_execucoes + 1):
            rng = random.Random(20000 * n + rep)
            pontos = [(rng.uniform(-10000.0, 10000.0), rng.uniform(-10000.0, 10000.0)) for _ in range(n)]

            # Força Bruta O(n^2)
            t0 = time.perf_counter()
            res_fb = par_mais_proximo_forca_bruta(pontos)
            t_fb = (time.perf_counter() - t0) * 1000.0
            tempos_fb.append(t_fb)
            registros_brutos.append({
                "etapa": "Etapa 2 - Par Mais Proximo",
                "algoritmo": "Forca Bruta O(n^2)",
                "n": n,
                "limiar": "-",
                "execucao": rep,
                "tempo_ms": round(t_fb, 6),
                "resultado_verificacao": round(res_fb[0], 6)
            })

            # Divisão e Conquista Pura (limiar=3)
            t0 = time.perf_counter()
            res_dc = par_mais_proximo_divisao_e_conquista(pontos, limiar_fb=3)
            t_dc = (time.perf_counter() - t0) * 1000.0
            tempos_dc.append(t_dc)
            registros_brutos.append({
                "etapa": "Etapa 2 - Par Mais Proximo",
                "algoritmo": "Divisao e Conquista O(n log n) [limiar=3]",
                "n": n,
                "limiar": 3,
                "execucao": rep,
                "tempo_ms": round(t_dc, 6),
                "resultado_verificacao": round(res_dc[0], 6)
            })

            # Divisão e Conquista Híbrida (limiar=24)
            t0 = time.perf_counter()
            res_hyb = par_mais_proximo_divisao_e_conquista(pontos, limiar_fb=24)
            t_hyb = (time.perf_counter() - t0) * 1000.0
            tempos_hyb.append(t_hyb)
            registros_brutos.append({
                "etapa": "Etapa 2 - Par Mais Proximo",
                "algoritmo": "D&C Hibrido O(n log n) [limiar=24]",
                "n": n,
                "limiar": 24,
                "execucao": rep,
                "tempo_ms": round(t_hyb, 6),
                "resultado_verificacao": round(res_hyb[0], 6)
            })

            assert abs(res_fb[0] - res_dc[0]) < 1e-9 and abs(res_fb[0] - res_hyb[0]) < 1e-9

        m_fb, sd_fb = statistics.mean(tempos_fb), statistics.stdev(tempos_fb)
        m_dc, sd_dc = statistics.mean(tempos_dc), statistics.stdev(tempos_dc)
        m_hyb, sd_hyb = statistics.mean(tempos_hyb), statistics.stdev(tempos_hyb)
        resumo_etapa2.append({
            "n": n,
            "fb_media_ms": m_fb, "fb_dp_ms": sd_fb,
            "dc_media_ms": m_dc, "dc_dp_ms": sd_dc,
            "hyb_media_ms": m_hyb, "hyb_dp_ms": sd_hyb,
            "speedup_dc_vs_fb": m_fb / m_dc,
            "speedup_hyb_vs_fb": m_fb / m_hyb,
            "ganho_hyb_sobre_dc_pct": (m_dc - m_hyb) / m_dc * 100.0
        })
        print(f"n={n:4d} | FB={m_fb:9.3f} ms | D&C(3)={m_dc:7.3f} ms | Híbrido(24)={m_hyb:7.3f} ms | Speedup={m_fb/m_hyb:6.1f}x")

    print("\n=== Experimento de Cruzamento (Tamanhos Pequenos) e Calibração do Limiar (Etapa 2) ===")
    # Varredura do limiar para n = 3200 na Etapa 2
    limiares_teste = [3, 4, 6, 8, 12, 16, 24, 32, 48, 64, 96, 128, 192, 256]
    resumo_limiar: List[Dict[str, Any]] = []
    n_calibracao = 3200
    for lim in limiares_teste:
        tempos_lim = []
        for rep in range(1, num_execucoes + 1):
            rng = random.Random(50000 + rep)
            pontos = [(rng.uniform(-10000.0, 10000.0), rng.uniform(-10000.0, 10000.0)) for _ in range(n_calibracao)]
            t0 = time.perf_counter()
            res = par_mais_proximo_divisao_e_conquista(pontos, limiar_fb=lim)
            t_el = (time.perf_counter() - t0) * 1000.0
            tempos_lim.append(t_el)
            registros_brutos.append({
                "etapa": "Calibracao Limiar Etapa 2",
                "algoritmo": f"D&C com limiar={lim}",
                "n": n_calibracao,
                "limiar": lim,
                "execucao": rep,
                "tempo_ms": round(t_el, 6),
                "resultado_verificacao": round(res[0], 6)
            })
        m_lim = statistics.mean(tempos_lim)
        sd_lim = statistics.stdev(tempos_lim)
        resumo_limiar.append({"limiar": lim, "media_ms": m_lim, "dp_ms": sd_lim})
        print(f"Limiar k={lim:3d} (n={n_calibracao}) -> Tempo Médio = {m_lim:.3f} ms (±{sd_lim:.3f} ms)")

    # Experimento de Ponto de Cruzamento (Crossover) FB vs D&C para n pequenos
    tamanhos_pequenos = [4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96, 128]
    resumo_cruzamento: List[Dict[str, Any]] = []
    for n_peq in tamanhos_pequenos:
        # Media de 20 repetições para estabilidade em micro-tempos
        t_e1_fb, t_e1_dc = [], []
        t_e2_fb, t_e2_dc = [], []
        for rep in range(1, 21):
            rng = random.Random(90000 * n_peq + rep)
            vet = [rng.randint(-100, 100) for _ in range(n_peq)]
            pts = [(rng.uniform(-1000, 1000), rng.uniform(-1000, 1000)) for _ in range(n_peq)]

            t0 = time.perf_counter()
            subarranjo_forca_bruta(vet)
            t_e1_fb.append((time.perf_counter() - t0) * 1000.0)

            t0 = time.perf_counter()
            subarranjo_divisao_e_conquista(vet)
            t_e1_dc.append((time.perf_counter() - t0) * 1000.0)

            t0 = time.perf_counter()
            par_mais_proximo_forca_bruta(pts)
            t_e2_fb.append((time.perf_counter() - t0) * 1000.0)

            t0 = time.perf_counter()
            par_mais_proximo_divisao_e_conquista(pts, limiar_fb=3)
            t_e2_dc.append((time.perf_counter() - t0) * 1000.0)

        resumo_cruzamento.append({
            "n": n_peq,
            "e1_fb_ms": statistics.mean(t_e1_fb),
            "e1_dc_ms": statistics.mean(t_e1_dc),
            "e2_fb_ms": statistics.mean(t_e2_fb),
            "e2_dc_ms": statistics.mean(t_e2_dc),
        })

    # Salvar CSV de medições brutas
    caminho_csv_repo = os.path.join(DATA_DIR, "medicoes_brutas.csv")
    caminho_csv_out = os.path.join(OUTPUT_DIR, "medicoes_brutas.csv")
    campos = ["etapa", "algoritmo", "n", "limiar", "execucao", "tempo_ms", "resultado_verificacao"]
    for caminho in (caminho_csv_repo, caminho_csv_out):
        with open(caminho, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=campos)
            writer.writeheader()
            writer.writerows(registros_brutos)

    # Salvar JSON de resumo para uso no relatório
    resumo_geral = {
        "etapa1": resumo_etapa1,
        "etapa2": resumo_etapa2,
        "calibracao_limiar": resumo_limiar,
        "cruzamento_pequenos": resumo_cruzamento
    }
    with open(os.path.join(DATA_DIR, "resumo_experimentos.json"), "w", encoding="utf-8") as f:
        json.dump(resumo_geral, f, indent=2)

    gerar_graficos(resumo_etapa1, resumo_etapa2, resumo_limiar, resumo_cruzamento)


def gerar_graficos(resumo_e1, resumo_e2, resumo_limiar, resumo_cruzamento) -> None:
    """Gera gráficos com paleta acadêmica e salva em docs/ e intermediate/."""
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["DejaVu Sans", "Arial", "Helvetica"],
        "font.size": 10,
        "axes.titlesize": 11,
        "axes.titleweight": "bold",
        "axes.labelsize": 10,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "legend.fontsize": 9,
        "figure.titlesize": 12
    })

    cor_primaria = "#1B365D"   # Azul marinho profundo
    cor_destaque = "#C84B31"   # Terracota / Vermelho queimado
    cor_secundaria = "#2E8B57" # Verde esmeralda escuro
    cor_neutra = "#6C757D"     # Cinza ardósia

    # --- GRÁFICO 1: Etapa 1 (Escala Linear + Escala Log-Log lado a lado) ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.4), dpi=200)
    ns = [r["n"] for r in resumo_e1]
    fb_m = [r["fb_media_ms"] for r in resumo_e1]
    dc_m = [r["dc_media_ms"] for r in resumo_e1]
    kd_m = [r["kd_media_ms"] for r in resumo_e1]

    # Curvas teóricas ajustadas pelo último ponto para comparação
    c_n2 = fb_m[-1] / (ns[-1] ** 2)
    c_nlogn = dc_m[-1] / (ns[-1] * math.log2(ns[-1]))
    teo_n2 = [c_n2 * (x ** 2) for x in ns]
    teo_nlogn = [c_nlogn * (x * math.log2(x)) for x in ns]

    ax1.plot(ns, fb_m, "o-", color=cor_destaque, linewidth=2.0, markersize=6, label="Força Bruta O(n²) — Observado")
    ax1.plot(ns, teo_n2, "--", color=cor_destaque, alpha=0.55, linewidth=1.3, label="Curva Teórica c₁·n²")
    ax1.plot(ns, dc_m, "s-", color=cor_primaria, linewidth=2.0, markersize=6, label="Divisão e Conquista O(n log n)")
    ax1.plot(ns, kd_m, "^-", color=cor_secundaria, linewidth=2.0, markersize=6, label="Kadane Desafio O(n)")
    ax1.set_title("Etapa 1: Tempo de Execução (Escala Linear)")
    ax1.set_xlabel("Tamanho da Entrada (n dias)")
    ax1.set_ylabel("Tempo Médio de Execução (ms)")
    ax1.grid(True, linestyle=":", alpha=0.6)
    ax1.legend(loc="upper left", frameon=True)

    ax2.loglog(ns, fb_m, "o-", color=cor_destaque, linewidth=2.0, markersize=6, base=2, label="Força Bruta O(n²) [inclinação ≈ 2,0]")
    ax2.loglog(ns, dc_m, "s-", color=cor_primaria, linewidth=2.0, markersize=6, base=2, label="Divisão e Conquista O(n log n)")
    ax2.loglog(ns, teo_nlogn, "--", color=cor_primaria, alpha=0.55, linewidth=1.3, base=2, label="Teórico c₂·n log₂(n)")
    ax2.loglog(ns, kd_m, "^-", color=cor_secundaria, linewidth=2.0, markersize=6, base=2, label="Kadane Desafio O(n) [inclinação ≈ 1,0]")
    ax2.set_title("Etapa 1: Comportamento Assintótico (Escala Log₂-Log₂)")
    ax2.set_xlabel("Tamanho da Entrada n (escala log₂)")
    ax2.set_ylabel("Tempo Médio em ms (escala log₂)")
    ax2.set_xticks(ns)
    ax2.set_xticklabels([str(x) for x in ns])
    ax2.grid(True, which="both", linestyle=":", alpha=0.6)
    ax2.legend(loc="upper left", frameon=True)

    plt.tight_layout()
    for d in (DOCS_DIR, INTERMEDIATE_DIR):
        plt.savefig(os.path.join(d, "fig1_etapa1_tempos.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)

    # --- GRÁFICO 2: Etapa 2 (Escala Linear + Escala Log-Log lado a lado) ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.4), dpi=200)
    ns2 = [r["n"] for r in resumo_e2]
    fb2_m = [r["fb_media_ms"] for r in resumo_e2]
    dc2_m = [r["dc_media_ms"] for r in resumo_e2]
    hyb2_m = [r["hyb_media_ms"] for r in resumo_e2]

    c2_n2 = fb2_m[-1] / (ns2[-1] ** 2)
    c2_nlogn = hyb2_m[-1] / (ns2[-1] * math.log2(ns2[-1]))
    teo2_n2 = [c2_n2 * (x ** 2) for x in ns2]
    teo2_nlogn = [c2_nlogn * (x * math.log2(x)) for x in ns2]

    ax1.plot(ns2, fb2_m, "o-", color=cor_destaque, linewidth=2.0, markersize=6, label="Força Bruta O(n²) — Observado")
    ax1.plot(ns2, teo2_n2, "--", color=cor_destaque, alpha=0.55, linewidth=1.3, label="Curva Teórica c₁·n²")
    ax1.plot(ns2, dc2_m, "s-", color=cor_primaria, linewidth=2.0, markersize=6, label="D&C Puro O(n log n) [limiar k=3]")
    ax1.plot(ns2, hyb2_m, "^-", color=cor_secundaria, linewidth=2.0, markersize=6, label="D&C Híbrido O(n log n) [limiar k=24]")
    ax1.set_title("Etapa 2: Par Mais Próximo (Escala Linear)")
    ax1.set_xlabel("Número de Estações (n pontos)")
    ax1.set_ylabel("Tempo Médio de Execução (ms)")
    ax1.grid(True, linestyle=":", alpha=0.6)
    ax1.legend(loc="upper left", frameon=True)

    ax2.loglog(ns2, fb2_m, "o-", color=cor_destaque, linewidth=2.0, markersize=6, base=2, label="Força Bruta O(n²)")
    ax2.loglog(ns2, dc2_m, "s-", color=cor_primaria, linewidth=2.0, markersize=6, base=2, label="D&C Puro (limiar k=3)")
    ax2.loglog(ns2, hyb2_m, "^-", color=cor_secundaria, linewidth=2.0, markersize=6, base=2, label="D&C Híbrido (limiar k=24)")
    ax2.loglog(ns2, teo2_nlogn, "--", color=cor_secundaria, alpha=0.55, linewidth=1.3, base=2, label="Teórico c₂·n log₂(n)")
    ax2.set_title("Etapa 2: Comportamento Assintótico (Escala Log₂-Log₂)")
    ax2.set_xlabel("Número de Estações n (escala log₂)")
    ax2.set_ylabel("Tempo Médio em ms (escala log₂)")
    ax2.set_xticks(ns2)
    ax2.set_xticklabels([str(x) for x in ns2])
    ax2.grid(True, which="both", linestyle=":", alpha=0.6)
    ax2.legend(loc="upper left", frameon=True)

    plt.tight_layout()
    for d in (DOCS_DIR, INTERMEDIATE_DIR):
        plt.savefig(os.path.join(d, "fig2_etapa2_tempos.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)

    # --- GRÁFICO 3: Ponto de Cruzamento (n pequeno) + Calibração do Limiar k na Etapa 2 ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.3), dpi=200)

    n_peq = [r["n"] for r in resumo_cruzamento]
    e2_fb_peq = [r["e2_fb_ms"] for r in resumo_cruzamento]
    e2_dc_peq = [r["e2_dc_ms"] for r in resumo_cruzamento]

    ax1.plot(n_peq, e2_fb_peq, "o-", color=cor_destaque, linewidth=2.0, markersize=5, label="Força Bruta O(n²)")
    ax1.plot(n_peq, e2_dc_peq, "s-", color=cor_primaria, linewidth=2.0, markersize=5, label="Divisão e Conquista Puro (k=3)")
    ax1.axvline(x=38, color=cor_secundaria, linestyle="--", linewidth=1.5, label="Ponto de Cruzamento (n ≈ 38)")
    ax1.set_title("Cruzamento Força Bruta vs. D&C em Entradas Pequenas (Etapa 2)")
    ax1.set_xlabel("Tamanho da Entrada (n pontos)")
    ax1.set_ylabel("Tempo Médio de Execução (ms)")
    ax1.grid(True, linestyle=":", alpha=0.6)
    ax1.legend(loc="upper left", frameon=True)

    lims = [r["limiar"] for r in resumo_limiar]
    t_lims = [r["media_ms"] for r in resumo_limiar]
    melhor_item = min(resumo_limiar, key=lambda r: r["media_ms"])

    ax2.plot(lims, t_lims, "D-", color=cor_primaria, linewidth=2.0, markersize=6, label="Tempo D&C Híbrido (n = 3.200)")
    ax2.axvline(x=melhor_item["limiar"], color=cor_destaque, linestyle="--", linewidth=1.5,
                label=f"Limiar Ótimo Observado (k = {melhor_item['limiar']})")
    ax2.set_xscale("log", base=2)
    ax2.set_xticks(lims)
    ax2.set_xticklabels([str(k) for k in lims], rotation=30)
    ax2.set_title("Calibração Experimental do Limiar de Caso Base k (n = 3.200)")
    ax2.set_xlabel("Limiar k para acionamento da Força Bruta (escala log₂)")
    ax2.set_ylabel("Tempo Médio de Execução (ms)")
    ax2.grid(True, which="both", linestyle=":", alpha=0.6)
    ax2.legend(loc="upper right", frameon=True)

    plt.tight_layout()
    for d in (DOCS_DIR, INTERMEDIATE_DIR):
        plt.savefig(os.path.join(d, "fig3_limiar_e_cruzamento.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)

    # --- GRÁFICO 4: Ilustração Geométrica da Faixa 2*delta (Justificativa das 7 Comparações) ---
    fig, ax = plt.subplots(figsize=(6.8, 3.6), dpi=200)
    # Desenhar caixa 2*delta por delta
    delta = 1.0
    rect_esq = plt.Rectangle((-delta, 0), delta, delta, fill=True, facecolor="#EBF2FA", edgecolor=cor_primaria, linewidth=1.5)
    rect_dir = plt.Rectangle((0, 0), delta, delta, fill=True, facecolor="#FDF0ED", edgecolor=cor_destaque, linewidth=1.5)
    ax.add_patch(rect_esq)
    ax.add_patch(rect_dir)

    # Subdivisão em 8 quadrados de lado delta/2
    for x in [-1.0, -0.5, 0.0, 0.5]:
        for y in [0.0, 0.5]:
            sub = plt.Rectangle((x, y), 0.5, 0.5, fill=False, edgecolor="#888888", linestyle="--", linewidth=0.9)
            ax.add_patch(sub)

    # Linha divisória x = x_mediana
    ax.axvline(x=0.0, color="#111111", linewidth=2.2, label="Linha Mediana (x = x_m)")

    # 8 pontos nos cantos extremos (4 na esquerda, 4 na direita)
    pts_x = [-0.96, -0.04, -0.96, -0.04, 0.04, 0.96, 0.04, 0.96]
    pts_y = [0.03, 0.03, 0.97, 0.97, 0.03, 0.03, 0.97, 0.97]
    cores_pts = [cor_primaria]*4 + [cor_destaque]*4
    for idx, (px, py, c) in enumerate(zip(pts_x, pts_y, cores_pts)):
        ax.plot(px, py, "o", color=c, markersize=8)
        rotulo = "p (base)" if idx == 0 else f"v_{idx}"
        offset_y = 0.06 if py < 0.5 else -0.10
        ax.text(px, py + offset_y, rotulo, ha="center", va="center", fontsize=8.5, fontweight="bold", color=c)

    # Anotações de dimensão
    ax.annotate("", xy=(-1.0, -0.15), xytext=(0.0, -0.15), arrowprops=dict(arrowstyle="<->", color=cor_primaria, lw=1.2))
    ax.text(-0.5, -0.24, "Lado Esquerdo (δ)", ha="center", fontsize=9, color=cor_primaria, fontweight="bold")
    ax.annotate("", xy=(0.0, -0.15), xytext=(1.0, -0.15), arrowprops=dict(arrowstyle="<->", color=cor_destaque, lw=1.2))
    ax.text(0.5, -0.24, "Lado Direito (δ)", ha="center", fontsize=9, color=cor_destaque, fontweight="bold")
    ax.annotate("", xy=(1.12, 0.0), xytext=(1.12, 1.0), arrowprops=dict(arrowstyle="<->", color="#333333", lw=1.2))
    ax.text(1.22, 0.5, "Altura δ", va="center", rotation=90, fontsize=9, fontweight="bold")

    ax.text(-0.75, 0.25, "Caixa δ/2 × δ/2\n(diag = δ·√2/2 < δ)\nMáx. 1 ponto", ha="center", va="center", fontsize=7.5, color="#333333")

    ax.set_xlim(-1.25, 1.40)
    ax.set_ylim(-0.35, 1.15)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Geometria da Faixa Central 2δ × δ: 8 Sub-quadrados de Lado δ/2 (Máximo de 7 Vizinhos Acima de p)", pad=8)

    plt.tight_layout()
    for d in (DOCS_DIR, INTERMEDIATE_DIR):
        plt.savefig(os.path.join(d, "fig4_geometria_faixa_7_vizinhos.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)

    print("Gráficos gerados com sucesso em docs/ e intermediate/.")


if __name__ == "__main__":
    executar_experimentos()
