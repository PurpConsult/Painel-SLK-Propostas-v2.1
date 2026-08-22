import os
import tempfile
from unittest.mock import Mock, patch

import requests

import app as sistema


EVENTOS = [{
    "id": "9001",
    "nome": "Convenção Lagune",
    "dataevento": "2026-08-10",
    "localevento": "Lagune Barra Hotel",
    "status": "Eventos Anteriores",
    "idorcamento": "1057",
    "valor_total": 1000,
}]

ITENS = [{
    "id": "E-1", "nome": "Painel de LED", "tipo": 7, "valor": 600,
}, {
    "id": "S-1", "nome": "Técnico", "tipo": 2, "valor": 400,
}]


def test_assistente_consulta_eventos_quando_ia_indisponivel():
    """Um pedido explícito continua consultável em modo leitura, mesmo sem resposta do modelo."""
    configuracao_testing_original = sistema.app.config.get("TESTING")
    login_ativo_original = sistema.app.config.get("LOGIN_LOCAL_ATIVO")
    sistema.app.config["TESTING"] = True
    sistema.app.config["LOGIN_LOCAL_ATIVO"] = False
    resposta_meeventos = Mock()
    resposta_meeventos.raise_for_status.return_value = None
    resposta_meeventos.json.return_value = {"data": EVENTOS}
    try:
        with sistema.app.test_client() as cliente, patch.object(sistema, "_planejar_relatorio_com_ia", side_effect=RuntimeError("IA indisponível")), patch.object(sistema.requests, "get", return_value=resposta_meeventos):
            resposta = cliente.post("/api/relatorios/assistente", json={"mensagem": "Quero os eventos de junho, julho e agosto de 2026"})
        assert resposta.status_code == 200, resposta.get_data(as_text=True)
        dados = resposta.get_json()
        assert dados["sucesso"] is True
        assert dados["plano"]["acao"] == "consultar_meeventos"
        assert dados["plano"]["recurso"] == "events"
        assert dados["plano"]["data_inicio"] == "2026-06-01"
        assert dados["plano"]["data_fim"] == "2026-08-31"
        assert dados["dados_consultados"]["quantidade"] == 1
    finally:
        sistema.app.config["TESTING"] = configuracao_testing_original
        sistema.app.config["LOGIN_LOCAL_ATIVO"] = login_ativo_original


def executar():
    with tempfile.TemporaryDirectory() as pasta_temporaria:
        pasta_original = sistema.PASTA_RELATORIOS
        testing_original = sistema.app.config.get("TESTING")
        login_ativo_original = sistema.app.config.get("LOGIN_LOCAL_ATIVO")
        sistema.PASTA_RELATORIOS = pasta_temporaria
        sistema.app.config["TESTING"] = True
        sistema.app.config["LOGIN_LOCAL_ATIVO"] = False
        cliente = sistema.app.test_client()
        try:
            with patch.object(sistema, "consultar_eventos_relatorio", return_value=EVENTOS), patch.object(sistema, "consultar_itens_evento_relatorio", return_value=ITENS):
                resposta = cliente.post("/api/relatorio/comissao", json={
                    "hotel_id": "lagune_barra_hotel",
                    "data_inicio": "2026-08-01",
                    "data_fim": "2026-08-31",
                })
                assert resposta.status_code == 200, resposta.get_data(as_text=True)
                dados = resposta.get_json()
                assert dados["sucesso"] is True
                assert dados["quantidade_eventos"] == 1
                assert dados["totais"]["comissao"] == 75.24
                identificador = dados["id_relatorio"]

                reavaliacao = cliente.post("/api/relatorio/comissao", json={
                    "hotel_id": "lagune_barra_hotel",
                    "data_inicio": "2026-08-01",
                    "data_fim": "2026-08-31",
                    "itens_excluidos": ["9001:E-1"],
                })
                assert reavaliacao.status_code == 200, reavaliacao.get_data(as_text=True)
                dados_reavaliados = reavaliacao.get_json()
                assert dados_reavaliados["totais"]["comissao"] == 0

                pagina = cliente.get("/relatorios")
                assert pagina.status_code == 200
                assert b"Revis\xc3\xa3o humana obrigat\xc3\xb3ria" in pagina.data
                assert b"Continue a conversa" in pagina.data
                assert b"Enviar mensagem" in pagina.data
                assert b"Consulta segura" in pagina.data

                pdf = cliente.get(f"/api/relatorio/comissao/{identificador}/pdf")
                assert pdf.status_code == 200
                assert pdf.data[:4] == b"%PDF"

                planilha = cliente.get(f"/api/relatorio/comissao/{identificador}/planilha")
                assert planilha.status_code == 200
                assert planilha.data[:2] == b"PK"

            resposta_http = Mock(status_code=401)
            erro_http = requests.exceptions.HTTPError(response=resposta_http)
            with patch.object(sistema, "consultar_eventos_relatorio", side_effect=erro_http):
                falha = cliente.post("/api/relatorio/comissao", json={
                    "hotel_id": "lagune_barra_hotel",
                    "data_inicio": "2026-08-01",
                    "data_fim": "2026-08-31",
                })
            assert falha.status_code == 502
            assert "MEEVENTOS_TOKEN" in falha.get_json()["detalhes"]
        finally:
            sistema.PASTA_RELATORIOS = pasta_original
            sistema.app.config["TESTING"] = testing_original
            sistema.app.config["LOGIN_LOCAL_ATIVO"] = login_ativo_original

    print("OK: rotas, persistência temporária, PDF e planilha de relatórios validados.")


if __name__ == "__main__":
    executar()
