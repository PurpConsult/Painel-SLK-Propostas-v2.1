import unittest

from app import _normalizar_plano_assistente_relatorios


class AssistenteRelatoriosTest(unittest.TestCase):
    def setUp(self):
        self.configuracoes = {"lagune": {"nome": "Lagune Hotel"}}

    def test_restringe_acao_e_hotel_ao_escopo_configurado(self):
        plano = _normalizar_plano_assistente_relatorios({
            "resposta": "Vamos conferir.", "perguntas": ["Qual período?"],
            "acao": "apagar_eventos", "hotel_id": "externo", "data_inicio": "2026/01/01",
            "data_fim": "2026-12-31", "matematica": ["Base"], "confirmacao_necessaria": False,
        }, self.configuracoes)
        self.assertEqual(plano["acao"], "esclarecer")
        self.assertEqual(plano["hotel_id"], "")
        self.assertEqual(plano["data_inicio"], "")
        self.assertEqual(plano["data_fim"], "2026-12-31")
        self.assertTrue(plano["confirmacao_necessaria"])

    def test_preserva_consulta_permitida_com_datas_iso(self):
        plano = _normalizar_plano_assistente_relatorios({
            "resposta": "Posso consultar.", "perguntas": [], "acao": "consultar_comissao",
            "hotel_id": "lagune", "data_inicio": "2026-01-01", "data_fim": "2026-08-19",
            "matematica": ["Somente equipamentos."], "confirmacao_necessaria": True,
        }, self.configuracoes)
        self.assertEqual(plano["acao"], "consultar_comissao")
        self.assertEqual(plano["hotel_id"], "lagune")
        self.assertEqual(plano["data_inicio"], "2026-01-01")
