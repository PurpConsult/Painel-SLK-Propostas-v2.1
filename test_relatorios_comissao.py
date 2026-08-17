import importlib.util
import os
import tempfile
from unittest.mock import Mock, patch


def carregar_app():
    caminho = os.path.join(os.path.dirname(__file__), "app.py")
    spec = importlib.util.spec_from_file_location("soulink_relatorios", caminho)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def main():
    app = carregar_app()
    configuracao = {
        "nome": "Lagune Barra Hotel",
        "percentual_comissao": 0.15,
        "deducao_1": 0.05,
        "deducao_2": 0.12,
        "tipo_equipamento": "7",
        "tipo_desconto_geral": "5",
    }
    eventos = [{
        "id": "100",
        "dataevento": "2026-08-01",
        "nomeevento": "Evento de teste",
        "localevento": "Lagune Barra Hotel",
        "idorcamento": "900",
        "status": "Eventos Anteriores",
    }]
    itens = {"100": [
        {"id": "1", "tipo": "2", "nome": "Serviço", "valor": "2000"},
        {"id": "2", "tipo": "7", "nome": "LED próprio", "valor": "8000"},
        {"id": "3", "tipo": "7", "nome": "Palco sublocado", "valor": "2000"},
        {"id": "4", "tipo": "5", "nome": "Desconto geral", "valor": "-1200"},
    ]}
    apuracao = app.calcular_apuracao_comissao(configuracao, eventos, itens, ["100:3"])
    evento = apuracao["eventos"][0]
    assert float(evento["bruto_itens"]) == 12000.0
    assert float(evento["equipamentos_bruto"]) == 8000.0
    assert float(evento["equipamentos_excluidos"]) == 2000.0
    assert float(evento["desconto_rateado_equipamentos"]) == 800.0
    assert float(evento["equipamentos_apos_desconto"]) == 7200.0
    assert float(evento["deducao_1"]) == 360.0
    assert float(evento["deducao_2"]) == 820.8
    assert float(evento["base_comissionavel"]) == 6019.2
    assert float(evento["comissao"]) == 902.88
    assert evento["itens_excluidos"][0]["nome"] == "Palco sublocado"

    registro = {
        "id_relatorio": "apuracao_teste",
        "gerado_em": "17/08/2026 12:00",
        "periodo": {"inicio": "2026-08-01", "fim": "2026-08-31"},
        "apuracao": app._serializar_relatorio(apuracao),
    }
    pdf = app.gerar_pdf_relatorio_comissao(registro).getvalue()
    planilha = app.gerar_planilha_relatorio_comissao(registro).getvalue()
    assert pdf.startswith(b"%PDF") and len(pdf) > 3000
    assert planilha.startswith(b"PK") and len(planilha) > 3000

    primeira = Mock()
    primeira.json.return_value = {"data": [{"id": "1"}], "pagination": {"total_page": 2}}
    primeira.raise_for_status.return_value = None
    try:
        with patch.object(app, "TOKEN", "teste"), patch.object(app.requests, "get", return_value=primeira):
            app._buscar_paginado_com_parametros("/events", {"start": "2026-08-01", "end": "2026-08-31"}, max_paginas=1)
    except ValueError:
        pass
    else:
        raise AssertionError("A paginação parcial deveria produzir erro explícito.")

    segunda = Mock()
    segunda.json.return_value = {"data": [{"id": "2"}], "pagination": {"total_page": 2}}
    segunda.raise_for_status.return_value = None
    with patch.object(app, "TOKEN", "teste"), patch.object(app.requests, "get", side_effect=[primeira, segunda]):
        itens_paginados = app._buscar_paginado_com_parametros("/events", {"start": "2026-08-01", "end": "2026-08-31"}, max_paginas=2)
    assert [item["id"] for item in itens_paginados] == ["1", "2"]
    print("OK: cálculo sequencial, exclusão humana e exportações de relatório validados.")


if __name__ == "__main__":
    main()
