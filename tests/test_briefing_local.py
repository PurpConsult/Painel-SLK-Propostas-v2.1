import json
import unittest

from app import _conteudo_estruturado_mensagem_ia, _normalizar_analise_briefing


class BriefingLocalTest(unittest.TestCase):
    def test_prioriza_objeto_estruturado_do_provedor(self):
        conteudo = _conteudo_estruturado_mensagem_ia({
            "content": "Resposta textual que não deve prevalecer.",
            "parsed": {"resumo": "Evento corporativo"},
        })
        self.assertEqual(json.loads(conteudo), {"resumo": "Evento corporativo"})

    def test_aceita_partes_textuais_quando_o_provedor_nao_entrega_parsed(self):
        conteudo = _conteudo_estruturado_mensagem_ia({
            "content": [{"type": "text", "text": "{\"resumo\": \"Teste\"}"}],
        })
        self.assertEqual(json.loads(conteudo), {"resumo": "Teste"})

    def test_normalizacao_nao_cria_dados_ausentes(self):
        analise = _normalizar_analise_briefing({
            "resumo": "Briefing de teste",
            "campos": {"nome_evento": "Reunião"},
            "itens_solicitados": [{"descricao": "Projetor", "quantidade": 2}],
            "alertas": [],
        })
        self.assertEqual(analise["campos"]["nome_evento"], "Reunião")
        self.assertEqual(analise["campos"]["local_evento"], "")
        self.assertEqual(analise["itens_solicitados"], [{"descricao": "Projetor", "quantidade": 2}])
