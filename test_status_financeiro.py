import json
import os
import shutil
import tempfile
from unittest.mock import Mock, patch

import app as appmod


def payload(evento_sem_data=False):
    return {
        "evento": {
            "nome_evento": "Convenção Comercial",
            "data_evento": "" if evento_sem_data else "2026-09-25",
            "evento_sem_data": evento_sem_data,
        },
        "cliente": {"razao_social": "Cliente Financeiro"},
        "itens": [{"id": 1, "nome": "MONTAGEM E DESMONTAGEM", "valor": 1250, "quantidade": 1, "tipo_item": "Equipamento"}],
    }


def main():
    pasta_teste = tempfile.mkdtemp(prefix="slk_status_teste_")
    arquivo_propostas_original = appmod.ARQUIVO_PROPOSTAS
    pasta_pdfs_original = appmod.PASTA_PDFS
    try:
        appmod.ARQUIVO_PROPOSTAS = os.path.join(pasta_teste, "propostas.json")
        appmod.PASTA_PDFS = os.path.join(pasta_teste, "pdfs")
        os.makedirs(appmod.PASTA_PDFS, exist_ok=True)
        cliente = appmod.app.test_client()
        resposta_meeventos = Mock(status_code=201)
        resposta_meeventos.json.return_value = {"data": {"id": "TESTE-STATUS"}}

        with patch.object(appmod.requests, "post", return_value=resposta_meeventos):
            criada = cliente.post("/api/gerar-proposta", json=payload())
            assert criada.status_code == 200, criada.get_data(as_text=True)
            assert criada.get_json()["numero_proposta"] == "TESTE-STATUS"

            sem_data = cliente.post("/api/gerar-proposta", json=payload(evento_sem_data=True))
            assert sem_data.status_code == 200
            numero_sem_data = sem_data.get_json()["numero_proposta"]

        listagem = cliente.get("/api/propostas").get_json()["dados"]
        proposta = next(item for item in listagem if item["numero"] == "TESTE-STATUS")
        assert proposta["status"] == "rascunho"
        assert proposta["versoes"][0]["status"] == "rascunho"

        pre = cliente.post("/api/propostas/TESTE-STATUS/versoes/1/status", json={"status": "pre_reserva"})
        assert pre.status_code == 200, pre.get_json()
        assert pre.get_json()["status"] == "pre_reserva"

        aprovada = cliente.post("/api/propostas/TESTE-STATUS/versoes/1/status", json={"status": "aprovada"})
        assert aprovada.status_code == 200, aprovada.get_json()
        assert aprovada.get_json()["status"] == "aprovada"

        bloqueada = cliente.post("/api/propostas/TESTE-STATUS/versoes/1/status", json={"status": "perdida"})
        assert bloqueada.status_code == 409

        bloqueio_data = cliente.post(f"/api/propostas/{numero_sem_data}/versoes/1/status", json={"status": "pre_reserva"})
        assert bloqueio_data.status_code == 409

        financeiro = cliente.get("/api/financeiro")
        assert financeiro.status_code == 200
        dados_financeiro = financeiro.get_json()
        assert dados_financeiro["quantidade"] == 1
        # O item foi classificado como equipamento e inclui 5% de impostos.
        assert dados_financeiro["total_aprovado"] == 1312.5
        assert dados_financeiro["dados"][0]["numero"] == "TESTE-STATUS"

        with open(appmod.ARQUIVO_PROPOSTAS, encoding="utf-8") as arquivo:
            persistidas = json.load(arquivo)
        principal = next(item for item in persistidas if item["numero"] == "TESTE-STATUS")
        assert principal["status"] == "aprovada"
        assert principal["aprovada_em"]

        with open(os.path.join(os.path.dirname(__file__), "templates", "propostas.html"), encoding="utf-8") as arquivo:
            propostas_html = arquivo.read()
        with open(os.path.join(os.path.dirname(__file__), "templates", "financeiro.html"), encoding="utf-8") as arquivo:
            financeiro_html = arquivo.read()
        assert "data-status=\"pre_reserva\"" in propostas_html
        assert "/api/financeiro" in financeiro_html
        print("OK: pré-reserva, aprovação, bloqueio de cópia fechada e financeiro somente leitura validados.")
    finally:
        appmod.ARQUIVO_PROPOSTAS = arquivo_propostas_original
        appmod.PASTA_PDFS = pasta_pdfs_original
        shutil.rmtree(pasta_teste, ignore_errors=True)


if __name__ == "__main__":
    main()
