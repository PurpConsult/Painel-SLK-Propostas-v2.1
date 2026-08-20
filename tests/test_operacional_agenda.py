import json

import app as aplicativo


def test_agenda_operacional_consolida_evento_pre_reserva_e_conflito(monkeypatch):
    propostas = [
        {
            "numero": "2201", "versao": 1, "status": "pre_reserva",
            "evento": {"nome_evento": "Pré-reserva técnica", "data_evento_inicio": "2026-08-20", "local_evento": "Lagune"},
            "cliente": {"razao_social": "Cliente teste"},
        }
    ]
    eventos = [{"id": 900, "status": "Confirmado", "dataevento": "2026-08-20", "nomeevento": "Evento confirmado", "nomeCliente": "Hotel", "localevento": "Lagune"}]
    monkeypatch.setattr(aplicativo, "_ler_json", lambda *_: propostas)
    monkeypatch.setattr(aplicativo, "_buscar_paginado_com_parametros", lambda *_args, **_kwargs: eventos)
    cliente = aplicativo.app.test_client()
    resposta = cliente.get("/api/operacional?inicio=2026-08-20&fim=2026-08-20&externos=1")
    dados = resposta.get_json()
    assert resposta.status_code == 200
    assert dados["sucesso"] is True
    assert dados["resumo"]["evento"] == 1
    assert dados["resumo"]["pre_reserva"] == 1
    assert dados["resumo"]["conflitos"] == 1
    proposta = next(item for item in dados["dados"] if item["origem"] == "soulink")
    assert proposta["conflito_confirmado"] is True
    assert "aval da equipe técnica" in proposta["alerta_operacional"]


def test_avaliacao_tecnica_local_e_exibida_no_conflito(monkeypatch, tmp_path):
    propostas = [
        {
            "numero": "2202", "versao": 1, "status": "rascunho",
            "evento": {"nome_evento": "Cotação com conflito", "data_evento_inicio": "2026-08-21", "local_evento": "Lagune"},
            "cliente": {"razao_social": "Cliente teste"},
        }
    ]
    eventos = [{"id": 901, "status": "Confirmado", "dataevento": "2026-08-21", "nomeevento": "Evento confirmado"}]
    arquivo_avaliacoes = tmp_path / "avaliacoes_tecnicas_operacionais.json"
    monkeypatch.setattr(aplicativo, "ARQUIVO_AVALIACOES_TECNICAS", str(arquivo_avaliacoes))

    def ler_json_simulado(arquivo, padrao):
        if arquivo == aplicativo.ARQUIVO_PROPOSTAS:
            return propostas
        if arquivo == str(arquivo_avaliacoes) and arquivo_avaliacoes.exists():
            return json.loads(arquivo_avaliacoes.read_text(encoding="utf-8"))
        return padrao

    monkeypatch.setattr(aplicativo, "_ler_json", ler_json_simulado)
    monkeypatch.setattr(aplicativo, "_buscar_paginado_com_parametros", lambda *_args, **_kwargs: eventos)
    cliente = aplicativo.app.test_client()
    resposta = cliente.post("/api/operacional/avaliacoes-tecnicas", json={"numero": "2202", "versao": 1, "decisao": "aprovada"})
    assert resposta.status_code == 200
    assert resposta.get_json()["sucesso"] is True
    assert arquivo_avaliacoes.exists()
    agenda = cliente.get("/api/operacional?inicio=2026-08-21&fim=2026-08-21&externos=1").get_json()
    proposta = next(item for item in agenda["dados"] if item["origem"] == "soulink")
    assert proposta["aval_tecnico"]["decisao"] == "aprovada"
    assert proposta["conflito_pendente_aval"] is False
