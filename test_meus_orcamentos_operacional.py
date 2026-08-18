"""Regressões da página comercial e da agenda operacional, executável com `python test_meus_orcamentos_operacional.py`."""
import json
import os
import tempfile

import app as sistema


RAIZ = os.path.dirname(os.path.abspath(__file__))


def executar():
    with open(os.path.join(RAIZ, "templates", "propostas.html"), encoding="utf-8") as arquivo:
        propostas_html = arquivo.read()
    with open(os.path.join(RAIZ, "templates", "operacional.html"), encoding="utf-8") as arquivo:
        operacional_html = arquivo.read()
    with open(os.path.join(RAIZ, "app.py"), encoding="utf-8") as arquivo:
        backend = arquivo.read()

    assert 'id="search"' in propostas_html
    assert "Buscar por número, cliente, evento ou local" in propostas_html
    assert "Versões anteriores" in propostas_html
    assert 'data-language="pt"' in propostas_html
    assert 'data-language="en"' in propostas_html
    assert 'data-language="es"' in propostas_html
    assert "Incluir orçamentos Meeventos" in propostas_html
    assert "Consulta somente leitura" in propostas_html
    assert "Visão Operacional" in operacional_html
    assert "Gerar OS" in operacional_html
    assert "Todos os status" in operacional_html
    assert 'id="filtroLocal"' in operacional_html
    assert 'id="filtroResponsavel"' in operacional_html
    assert "Todos os locais" in operacional_html
    assert "Todos os responsáveis" in operacional_html
    assert "def api_listar_orcamentos_meeventos" in backend
    assert "def api_operacional" in backend
    assert "def api_ordem_servico_proposta" in backend
    assert "def api_ordem_servico_evento" in backend
    assert 'request.args.get("externos", "1")' in backend
    assert "externos=${externos?'1':'0'}" in operacional_html
    assert 'methods=["POST"]' not in backend[backend.index("def api_listar_orcamentos_meeventos"):backend.index("def _data_operacional")]

    dados = [{
        "numero": "1057", "versao": 2, "status": "aprovada", "numero_oficial": "",
        "cliente": {"razao_social": "Cliente Exemplo"},
        "evento": {"nome_evento": "Convenção Comercial", "local_evento": "Lagune Hotel", "data_evento_inicio": "2026-08-20", "horario_inicio_evento": "09:00"},
        "blocos": {"total_geral": 2500.00},
        "itens": [{"nome": "Projetor", "quantidade": 1, "valor": 400}],
    }]
    arquivo_temporario = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8")
    try:
        json.dump(dados, arquivo_temporario)
        arquivo_temporario.close()
        arquivo_original = sistema.ARQUIVO_PROPOSTAS
        sistema.ARQUIVO_PROPOSTAS = arquivo_temporario.name
        try:
            cliente = sistema.app.test_client()
            resposta = cliente.get("/api/propostas")
            corpo = resposta.get_json()
            assert resposta.status_code == 200 and corpo["dados"][0]["local"] == "Lagune Hotel"

            agenda = cliente.get("/api/operacional?inicio=2026-08-01&fim=2026-08-31&externos=0")
            agenda_corpo = agenda.get_json()
            assert agenda.status_code == 200 and agenda_corpo["sucesso"] is True
            item = next(registro for registro in agenda_corpo["dados"] if registro["origem"] == "soulink")
            assert item["tipo"] == "aprovada" and item["pode_gerar_os"] is True

            os_pdf = cliente.get("/api/operacional/os/proposta/1057/2")
            assert os_pdf.status_code == 200
            assert os_pdf.mimetype == "application/pdf"
        finally:
            sistema.ARQUIVO_PROPOSTAS = arquivo_original
    finally:
        try:
            os.unlink(arquivo_temporario.name)
        except FileNotFoundError:
            pass

    print("OK — Meus Orçamentos e a visão operacional foram validados.")


if __name__ == "__main__":
    executar()
