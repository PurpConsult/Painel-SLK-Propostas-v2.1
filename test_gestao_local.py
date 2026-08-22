import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

from test_followups_local import _carregar_app, _preparar_usuario


def test_dashboard_e_financeiro_abrem_para_administradora():
    app_local = _carregar_app()
    with tempfile.TemporaryDirectory() as diretorio:
        _preparar_usuario(app_local, diretorio, papel="admin")
        with app_local.app.test_client() as cliente:
            cliente.post("/login", data={"usuario": "teste", "senha": "SenhaTeste!2026"})
            painel = cliente.get("/")
            financeiro = cliente.get("/financeiro")
            assert painel.status_code == 200
            assert financeiro.status_code == 200
            assert "Painel de gestão" in painel.get_data(as_text=True)
            assert "Central Financeira" in financeiro.get_data(as_text=True)


def test_interfaces_de_gestao_tem_controles_solicitados():
    base = Path(__file__).parent / "templates"
    dashboard = (base / "dashboard.html").read_text(encoding="utf-8")
    financeiro = (base / "financeiro.html").read_text(encoding="utf-8")
    propostas = (base / "propostas.html").read_text(encoding="utf-8")
    operacional = (base / "operacional.html").read_text(encoding="utf-8")
    assert "Follow-ups hoje" in dashboard
    assert "Financeiro consultado no Meeventos" in financeiro
    assert "Conciliação bancária por CSV" in financeiro
    assert "arquivoCsv" in financeiro
    assert "Nenhuma baixa será realizada automaticamente" in financeiro
    assert "definirMesVigente" in financeiro
    assert "getMonth()+1" in financeiro
    assert "Agendar follow-up" in propostas
    assert "Vendedor" in operacional
    assert "min-width:1360px" in operacional


def test_financeiro_separa_receitas_pendentes_e_lancamentos_sem_editar_meeventos():
    app_local = _carregar_app()
    resposta_meeventos = Mock()
    resposta_meeventos.raise_for_status.return_value = None
    resposta_meeventos.json.return_value = {"data": [
        {"id": "1", "datacompetencia": "2099-08-12", "vencimento": "2099-08-12", "tipocobranca": "Receita", "valor": "1000,00", "pago": False, "descricao": "Sinal cliente"},
        {"id": "2", "datacompetencia": "2099-08-20", "datapagamento": "2099-08-20", "tipocobranca": "Receita", "valor": "500,00", "pago": True, "descricao": "Recebimento cliente"},
        {"id": "3", "datacompetencia": "2099-08-21", "tipocobranca": "Despesa", "valor": "350,00", "pago": False, "descricao": "Fornecedor"},
    ]}
    with tempfile.TemporaryDirectory() as diretorio:
        _preparar_usuario(app_local, diretorio, papel="admin")
        with app_local.app.test_client() as cliente, patch.object(app_local.requests, "get", return_value=resposta_meeventos):
            cliente.post("/login", data={"usuario": "teste", "senha": "SenhaTeste!2026"})
            central = cliente.get("/api/financeiro/central?inicio=2099-08-01&fim=2099-08-31")
            paginas = [cliente.get(caminho) for caminho in ("/financeiro", "/financeiro/contas-a-receber", "/financeiro/conciliacao", "/financeiro/lancamentos")]
        assert central.status_code == 200
        dados = central.get_json()
        assert dados["sucesso"] is True
        assert dados["resumo"]["recebimentos_em_aberto"] == 1000
        assert dados["resumo"]["recebimentos_pagos"] == 500
        assert dados["resumo"]["despesas_total"] == 350
        assert [registro["natureza"] for registro in dados["dados"]] == ["Receita", "Receita", "Despesa"]
        assert all(pagina.status_code == 200 for pagina in paginas)
