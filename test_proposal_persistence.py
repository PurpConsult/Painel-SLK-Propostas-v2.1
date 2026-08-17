import json
import os
import shutil
import tempfile
from unittest.mock import Mock, patch

import app as appmod


def main():
    pasta_teste = tempfile.mkdtemp(prefix="slk_propostas_teste_")
    try:
        appmod.ARQUIVO_PROPOSTAS = os.path.join(pasta_teste, "propostas.json")
        appmod.PASTA_PDFS = os.path.join(pasta_teste, "pdfs")
        os.makedirs(appmod.PASTA_PDFS, exist_ok=True)
        cliente = appmod.app.test_client()

        payload_novo = {
            "evento": {
                "nome_evento": "Reunião Nexxus",
                "data_evento": "2026-09-24",
                "local_evento": "Laghetto Stilo Barra",
                "qtd_pessoas": "300",
                "nome_vendedor": "Jairo",
                "id_vendedor": "62",
            },
            "cliente": {
                "razao_social": "Nexxus Engenharia",
                "documento": "12.345.678/0001-90",
                "email": "contato@nexxus.com.br",
                "telefone": "(21) 99999-9999",
                "contato": "Raquel Santos",
            },
            "itens": [
                {"id": 2, "nome": "TÉCNICO AUDIOVISUAL", "valor": 480, "quantidade": 1, "tipo_item": "Serviço"},
                {
                    "id": 45,
                    "nome": "PROJETOR 5000 LUMENS",
                    "valor": 1050,
                    "quantidade": 2,
                    "tipo_item": "Equipamento",
                    "imagem_url": "https://example.com/projetor-aprovado.png",
                    "imagem_fonte": "Imagem aprovada",
                    "externo": True,
                    "fornecedor_externo": "Locadora Alfa",
                    "custo_externo": 700,
                },
            ],
            "observacoes": "Teste automatizado",
            "opcoes_pdf": {
                "mostrar_valor_unitario": True,
                "mostrar_condicoes_gerais": True,
                "idioma": "en",
            },
        }
        resposta_meeventos = Mock(status_code=201)
        resposta_meeventos.json.return_value = {"data": {"id": "TESTE-1720"}}

        with patch.object(appmod.requests, "post", return_value=resposta_meeventos) as post_mock:
            resposta = cliente.post("/api/gerar-proposta", json=payload_novo)
            assert resposta.status_code == 200, resposta.get_data(as_text=True)
            criado = resposta.get_json()
            assert criado["sucesso"] is True
            assert criado["numero_proposta"] == "TESTE-1720"
            assert criado["versao"] == 1
            assert post_mock.call_count == 1

            payload_edicao = dict(payload_novo)
            payload_edicao["numero_original"] = "TESTE-1720"
            payload_edicao["itens"] = payload_novo["itens"] + [
                {"id": 77, "nome": "CADEIRA", "valor": 30, "quantidade": 20, "tipo_item": "Equipamento"}
            ]
            resposta_edicao = cliente.post("/api/gerar-proposta", json=payload_edicao)
            assert resposta_edicao.status_code == 200, resposta_edicao.get_data(as_text=True)
            editado = resposta_edicao.get_json()
            assert editado["numero_proposta"] == "TESTE-1720"
            assert editado["versao"] == 2
            assert post_mock.call_count == 1, "Uma edição não deve duplicar o orçamento no Meeventos"

        with open(appmod.ARQUIVO_PROPOSTAS, encoding="utf-8") as arquivo:
            salvas = json.load(arquivo)
        assert len(salvas) == 2
        assert salvas[0]["cliente"]["email"] == "contato@nexxus.com.br"
        assert salvas[0]["evento"]["id_vendedor"] == "62"
        assert salvas[0]["itens"][1]["externo"] is True
        assert salvas[0]["itens"][1]["fornecedor_externo"] == "Locadora Alfa"
        assert salvas[0]["itens"][1]["custo_externo"] == 700.0
        assert salvas[0]["itens"][1]["imagem_url"] == "https://example.com/projetor-aprovado.png"
        assert salvas[0]["itens"][1]["nome"] == "PROJETOR 5000 LUMENS"
        assert salvas[0]["itens"][1]["id"] == 45
        assert salvas[0]["opcoes_pdf"]["idioma"] == "en"
        assert salvas[0]["controle_locacao_externa"]["custo"] == 1400.0
        assert salvas[0]["controle_locacao_externa"]["margem_bruta"] == 700.0
        assert len(salvas[1]["itens"]) == 3

        detalhes = cliente.get("/api/propostas/TESTE-1720/versoes/2")
        assert detalhes.status_code == 200
        dados_edicao = detalhes.get_json()["dados"]
        assert dados_edicao["cliente"]["telefone"] == "(21) 99999-9999"
        assert dados_edicao["evento"]["local_evento"] == "Laghetto Stilo Barra"
        assert len(dados_edicao["itens"]) == 3
        assert dados_edicao["itens"][1]["fornecedor_externo"] == "Locadora Alfa"
        assert dados_edicao["itens"][1]["imagem_url"] == "https://example.com/projetor-aprovado.png"
        assert dados_edicao["opcoes_pdf"]["idioma"] == "en"

        listagem = cliente.get("/api/propostas")
        assert listagem.status_code == 200
        agrupadas = listagem.get_json()["dados"]
        assert len(agrupadas) == 1
        assert agrupadas[0]["numero"] == "TESTE-1720"
        assert agrupadas[0]["ultima_versao"] == 2
        assert agrupadas[0]["cliente"] == "Nexxus Engenharia"
        assert agrupadas[0]["evento"] == "Reunião Nexxus"
        assert len(agrupadas[0]["versoes"]) == 2

        with open(os.path.join(os.path.dirname(__file__), "templates", "index.html"), encoding="utf-8") as arquivo:
            index_html = arquivo.read()
        with open(os.path.join(os.path.dirname(__file__), "templates", "propostas.html"), encoding="utf-8") as arquivo:
            propostas_html = arquivo.read()
        assert "function preencherFormularioDeEdicao()" in index_html
        assert "selecionados = (dados.itens || []).map" in index_html
        assert "Locação externa" in index_html
        assert "Margem bruta" in index_html
        assert "imagem_url: item.imagem_aprovada?.image_url" in index_html
        assert 'id="idioma_pdf"' in index_html
        assert 'idioma: document.getElementById("idioma_pdf").value' in index_html
        assert "localStorage.setItem('dados_editar', dadosOrganizados);" in propostas_html
        assert "/api/propostas/${encodeURIComponent(numProposta)}/versoes/${versao}" in propostas_html
        print("OK: criação, listagem, versionamento e recuperação completa para edição validados.")
    finally:
        shutil.rmtree(pasta_teste, ignore_errors=True)


if __name__ == "__main__":
    main()
