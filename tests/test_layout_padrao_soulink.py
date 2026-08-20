import pathlib
import unittest


RAIZ = pathlib.Path(__file__).resolve().parents[1]


class LayoutPadraoSoulinkTest(unittest.TestCase):
    def test_nova_proposta_usa_casca_visual_compartilhada(self):
        conteudo = (RAIZ / "templates" / "index.html").read_text(encoding="utf-8")

        self.assertIn("soulink-pages.css", conteudo)
        self.assertIn("<main class=\"wrap\">", conteudo)
        self.assertIn("<h1>Nova Proposta</h1>", conteudo)
        self.assertIn("id=\"form\"", conteudo)
        self.assertIn("id=\"btn_analisar_ia\"", conteudo)

    def test_relatorios_mantem_assistente_e_padrao_compartilhado(self):
        conteudo = (RAIZ / "templates" / "relatorios.html").read_text(encoding="utf-8")

        self.assertIn("soulink-pages.css", conteudo)
        self.assertIn("class=\"intro page-intro\"", conteudo)
        self.assertIn("id=\"assistente-pedido\"", conteudo)
        self.assertIn("id=\"btn-assistente\"", conteudo)
        self.assertIn("Nenhum PDF é gerado sem sua confirmação", conteudo)

    def test_folha_compartilhada_reflete_o_padrao_de_meus_orcamentos(self):
        conteudo = (RAIZ / "static" / "soulink-pages.css").read_text(encoding="utf-8")

        self.assertIn("--blue: #005f78", conteudo)
        self.assertIn("max-width: 1220px", conteudo)
        self.assertIn("box-shadow: 0 4px 15px #073f4c08", conteudo)


if __name__ == "__main__":
    unittest.main()
