import json
import os
import shutil
import tempfile
from unittest.mock import Mock, patch

import app as appmod


def payload_com_desconto():
    return {
        "evento": {"nome_evento": "Convenção de Teste", "data_evento": "2026-09-25"},
        "cliente": {"razao_social": "Cliente de Teste"},
        "desconto_proposta": 120,
        "opcoes_pdf": {"idioma": "pt"},
        "itens": [{"id": 2, "nome": "PROJETOR 5000 LUMENS", "valor": 4500, "quantidade": 1, "tipo_item": "Equipamento"}],
    }


def main():
    pasta_teste = tempfile.mkdtemp(prefix="slk_correcoes_teste_")
    arquivo_original, pasta_original = appmod.ARQUIVO_PROPOSTAS, appmod.PASTA_PDFS
    ambiente_original = {chave: os.environ.get(chave) for chave in ("BUILT_IN_FORGE_API_URL", "BUILT_IN_FORGE_API_KEY", "ANTHROPIC_API_KEY", "ANTHROPIC_MODEL")}
    try:
        appmod.ARQUIVO_PROPOSTAS = os.path.join(pasta_teste, "propostas.json")
        appmod.PASTA_PDFS = os.path.join(pasta_teste, "pdfs")
        cliente = appmod.app.test_client()
        resposta_meeventos = Mock(status_code=201)
        resposta_meeventos.json.return_value = {"data": {"id": "TESTE-IDIOMA"}}
        with patch.object(appmod.requests, "post", return_value=resposta_meeventos):
            criada = cliente.post("/api/gerar-proposta", json=payload_com_desconto())
        assert criada.status_code == 200, criada.get_data(as_text=True)
        assert criada.get_json()["blocos"]["desconto"] == 120.0
        assert criada.get_json()["blocos"]["total_geral"] == 4605.0

        antes = json.load(open(appmod.ARQUIVO_PROPOSTAS, encoding="utf-8"))
        reemitida = cliente.post("/api/propostas/TESTE-IDIOMA/versoes/1/reemitir-pdf", json={"idioma": "en"})
        assert reemitida.status_code == 200, reemitida.get_data(as_text=True)
        dados = reemitida.get_json()
        assert dados["arquivo_pdf"].endswith("_en.pdf")
        assert os.path.exists(os.path.join(appmod.PASTA_PDFS, dados["arquivo_pdf"]))
        depois = json.load(open(appmod.ARQUIVO_PROPOSTAS, encoding="utf-8"))
        assert len(antes) == len(depois) == 1
        assert depois[0]["opcoes_pdf"]["idioma"] == "pt"
        assert cliente.post("/api/propostas/TESTE-IDIOMA/versoes/1/reemitir-pdf", json={"idioma": "fr"}).status_code == 400

        for chave in ("BUILT_IN_FORGE_API_URL", "BUILT_IN_FORGE_API_KEY"):
            os.environ.pop(chave, None)
        os.environ["ANTHROPIC_API_KEY"] = "chave-de-teste"
        os.environ["ANTHROPIC_MODEL"] = "modelo-de-teste"
        provedor, modelo, url, chave = appmod._modelo_ia_disponivel()
        assert (provedor, modelo, url, chave) == ("anthropic", "modelo-de-teste", "https://api.anthropic.com", "chave-de-teste")

        raiz = os.path.dirname(__file__)
        app_texto = open(os.path.join(raiz, "app.py"), encoding="utf-8").read()
        index_texto = open(os.path.join(raiz, "templates", "index.html"), encoding="utf-8").read()
        propostas_texto = open(os.path.join(raiz, "templates", "propostas.html"), encoding="utf-8").read()
        assert "NewWindow=True" in app_texto
        assert "topMargin=4.4*cm" in app_texto
        assert "subtotal_geral" in index_texto and "totalBruto - desconto" in index_texto
        assert "function issue(language)" in propostas_texto and "reemitir-pdf" in propostas_texto
        print("OK: desconto, nova guia, área segura, reemissão multilíngue e IA Claude local validados.")
    finally:
        appmod.ARQUIVO_PROPOSTAS, appmod.PASTA_PDFS = arquivo_original, pasta_original
        for chave, valor in ambiente_original.items():
            if valor is None:
                os.environ.pop(chave, None)
            else:
                os.environ[chave] = valor
        shutil.rmtree(pasta_teste, ignore_errors=True)


if __name__ == "__main__":
    main()
