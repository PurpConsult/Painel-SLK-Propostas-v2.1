import os
import tempfile
from unittest.mock import patch

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


def executar():
    with tempfile.TemporaryDirectory() as pasta_temporaria:
        pasta_original = sistema.PASTA_RELATORIOS
        sistema.PASTA_RELATORIOS = pasta_temporaria
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

                pdf = cliente.get(f"/api/relatorio/comissao/{identificador}/pdf")
                assert pdf.status_code == 200
                assert pdf.data[:4] == b"%PDF"

                planilha = cliente.get(f"/api/relatorio/comissao/{identificador}/planilha")
                assert planilha.status_code == 200
                assert planilha.data[:2] == b"PK"
        finally:
            sistema.PASTA_RELATORIOS = pasta_original

    print("OK: rotas, persistência temporária, PDF e planilha de relatórios validados.")


if __name__ == "__main__":
    executar()
