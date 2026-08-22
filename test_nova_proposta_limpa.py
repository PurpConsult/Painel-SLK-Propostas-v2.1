import unittest
from pathlib import Path


class NovaPropostaLimpaTest(unittest.TestCase):
    def setUp(self):
        self.template = Path(__file__).with_name("templates").joinpath("index.html").read_text(encoding="utf-8")
        self.header = Path(__file__).with_name("templates").joinpath("_cabecalho_soulink.html").read_text(encoding="utf-8")

    def test_nova_proposta_descarta_rascunho_e_oferece_limpeza_completa(self):
        self.assertIn('id="btnLimparFormulario"', self.template)
        self.assertIn('function limparFormularioCompleto()', self.template)
        self.assertIn('parametrosPagina.get("nova") === "1"', self.template)
        self.assertIn('limparRascunhoDeEdicao();', self.template)
        self.assertIn('href="/nova-proposta"', self.header)
        self.assertIn('Comercial', self.header)

    def test_logo_vendai_usa_arquivo_local_com_estilo_visivel(self):
        self.assertIn("logo_vendai.png", self.template)
        self.assertIn('class="logo-vendai"', self.template)
        self.assertIn("opacity:1", self.template)


if __name__ == "__main__":
    unittest.main()
