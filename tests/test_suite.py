"""
Bateria Automatizada de Testes (Etapas 1 e 2 + Testes de Estresse Aleatórios)
Autores: Catarina Pimentel e Hafiz Costa
"""

import os
import sys
import json
import math
import random
import unittest

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


class TestDivisaoEConquista(unittest.TestCase):
    """Valida todos os casos do arquivo casos_de_teste.json e testes de estresse."""

    @classmethod
    def setUpClass(cls):
        caminho_json = os.path.join(os.path.dirname(__file__), "casos_de_teste.json")
        with open(caminho_json, "r", encoding="utf-8") as f:
            cls.dados = json.load(f)

    def test_etapa1_casos_catalogados(self):
        """Verifica Força Bruta, Divisão e Conquista e Kadane O(n) em todos os casos catalogados."""
        for caso in self.dados["etapa1_subarranjo_soma_maxima"]:
            vetor = caso["entrada_vetor"]
            esp = (
                caso["saida_esperada"]["soma_maxima"],
                caso["saida_esperada"]["inicio"],
                caso["saida_esperada"]["fim"],
            )
            res_fb = subarranjo_forca_bruta(vetor)
            res_dc = subarranjo_divisao_e_conquista(vetor)
            res_kd = subarranjo_kadane_linear(vetor)

            self.assertEqual(res_fb, esp, f"Falha Força Bruta no caso {caso['id']}")
            self.assertEqual(res_dc, esp, f"Falha Divisão e Conquista no caso {caso['id']}")
            self.assertEqual(res_kd, esp, f"Falha Kadane O(n) no caso {caso['id']}")

    def test_etapa1_consistencia_aleatoria(self):
        """Compara Força Bruta, Divisão e Conquista e Kadane em 50 vetores aleatórios (incluindo negativos e empates)."""
        rng = random.Random(20261028)
        for tam in [1, 2, 3, 5, 10, 25, 50, 100]:
            for _ in range(5):
                vetor = [rng.randint(-15, 15) for _ in range(tam)]
                res_fb = subarranjo_forca_bruta(vetor)
                res_dc = subarranjo_divisao_e_conquista(vetor)
                res_kd = subarranjo_kadane_linear(vetor)
                self.assertEqual(res_fb, res_dc)
                self.assertEqual(res_fb, res_kd)

    def test_etapa2_casos_catalogados(self):
        """Verifica Força Bruta, D&C (limiar=3) e D&C Híbrido (limiar=24) nos casos catalogados."""
        for caso in self.dados["etapa2_par_pontos_mais_proximos"]:
            pontos = [(p[0], p[1]) for p in caso["entrada_pontos"]]
            esp_d = caso["saida_esperada"]["distancia"]
            esp_ids = tuple(caso["saida_esperada"]["indices"])

            d_fb, _, _, ids_fb = par_mais_proximo_forca_bruta(pontos)
            d_dc, _, _, ids_dc = par_mais_proximo_divisao_e_conquista(pontos, limiar_fb=3)
            d_hyb, _, _, ids_hyb = par_mais_proximo_divisao_e_conquista(pontos, limiar_fb=24)

            self.assertAlmostEqual(d_fb, esp_d, places=5, msg=f"Falha distância FB em {caso['id']}")
            self.assertAlmostEqual(d_dc, esp_d, places=5, msg=f"Falha distância D&C em {caso['id']}")
            self.assertAlmostEqual(d_hyb, esp_d, places=5, msg=f"Falha distância Híbrido em {caso['id']}")

            self.assertEqual(ids_fb, esp_ids, f"Falha índices FB em {caso['id']}")
            self.assertEqual(ids_dc, esp_ids, f"Falha índices D&C em {caso['id']}")
            self.assertEqual(ids_hyb, esp_ids, f"Falha índices Híbrido em {caso['id']}")

    def test_etapa2_consistencia_aleatoria(self):
        """Compara Força Bruta e Divisão e Conquista em nuvens de pontos aleatórias."""
        rng = random.Random(20261028)
        for tam in [2, 3, 4, 8, 15, 40, 80, 150]:
            for _ in range(3):
                pontos = [(rng.uniform(-1000.0, 1000.0), rng.uniform(-1000.0, 1000.0)) for _ in range(tam)]
                d_fb, _, _, ids_fb = par_mais_proximo_forca_bruta(pontos)
                d_dc, _, _, ids_dc = par_mais_proximo_divisao_e_conquista(pontos, limiar_fb=3)
                d_hyb, _, _, ids_hyb = par_mais_proximo_divisao_e_conquista(pontos, limiar_fb=24)
                self.assertAlmostEqual(d_fb, d_dc, places=9)
                self.assertAlmostEqual(d_fb, d_hyb, places=9)
                self.assertEqual(ids_fb, ids_dc)
                self.assertEqual(ids_fb, ids_hyb)


if __name__ == "__main__":
    unittest.main(verbosity=2)
