import pathlib
import re
import unittest


RAIZ = pathlib.Path(__file__).resolve().parents[1]
TEMPLATES = RAIZ / "templates"


class CabecalhoSoulinkTest(unittest.TestCase):
    paginas = [
        "index.html",
        "propostas.html",
        "operacional.html",
        "meus_itens.html",
        "financeiro.html",
        "relatorios.html",
    ]

    def test_paginas_principais_usam_cabecalho_compartilhado(self):
        for pagina in self.paginas:
            conteudo = (TEMPLATES / pagina).read_text(encoding="utf-8")
            self.assertIn("soulink-header.css", conteudo, pagina)
            self.assertIn("{% include '_cabecalho_soulink.html' %}", conteudo, pagina)

    def test_menu_horizontal_contem_todas_as_areas(self):
        cabecalho = (TEMPLATES / "_cabecalho_soulink.html").read_text(encoding="utf-8")
        for rotulo in [
            "Nova proposta",
            "Meus orçamentos",
            "Operação",
            "Meus itens",
            "Financeiro",
            "Relatórios",
        ]:
            self.assertIn(rotulo, cabecalho)

    def test_paginas_sem_estilo_generico_que_compete_com_cabecalho(self):
        seletores_proibidos = [
            r"^\s*header\s*\{",
            r"^\s*header\s+h1\b",
            r"^\s*header\s+nav\b",
            r"^\s*header\s+a\b",
        ]
        for pagina in ["financeiro.html", "relatorios.html"]:
            conteudo = (TEMPLATES / pagina).read_text(encoding="utf-8")
            for seletor in seletores_proibidos:
                self.assertIsNone(
                    re.search(seletor, conteudo, flags=re.MULTILINE),
                    f"{pagina}: {seletor}",
                )
