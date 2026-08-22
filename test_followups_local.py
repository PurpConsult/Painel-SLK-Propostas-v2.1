import importlib.util
import tempfile
from datetime import datetime, timedelta
from pathlib import Path


def _carregar_app():
    caminho = Path(__file__).with_name("app.py")
    especificacao = importlib.util.spec_from_file_location("soulink_app_teste_followups", caminho)
    modulo = importlib.util.module_from_spec(especificacao)
    assert especificacao.loader is not None
    especificacao.loader.exec_module(modulo)
    modulo.app.config.update(TESTING=True, LOGIN_LOCAL_ATIVO=True)
    return modulo


def _preparar_usuario(modulo, diretorio, papel="comercial"):
    base = Path(diretorio)
    modulo.ARQUIVO_USUARIOS_LOCAL = str(base / "usuarios.json")
    modulo.ARQUIVO_AUDITORIA_LOCAL = str(base / "auditoria.json")
    modulo.ARQUIVO_FOLLOWUPS_COMERCIAIS = str(base / "followups.json")
    modulo.ARQUIVO_PROPOSTAS = str(base / "propostas.json")
    modulo._salvar_usuarios_locais([{
        "id": "usuario", "nome": "Equipe de Teste", "usuario": "teste",
        "senha_hash": modulo.generate_password_hash("SenhaTeste!2026"), "papel": papel, "ativo": True,
    }])


def test_comercial_agenda_conclui_e_reagenda_followup_local():
    app_local = _carregar_app()
    with tempfile.TemporaryDirectory() as diretorio:
        _preparar_usuario(app_local, diretorio)
        hoje = datetime.now().date()
        with app_local.app.test_client() as cliente:
            cliente.post("/login", data={"usuario": "teste", "senha": "SenhaTeste!2026"})
            pagina = cliente.get("/followups")
            assert pagina.status_code == 200
            assert "Agenda comercial dos próximos sete dias" in pagina.get_data(as_text=True)
            resposta = cliente.post("/api/followups", json={
                "data_followup": hoje.isoformat(), "tipo_referencia": "proposta", "acao": "ligar",
                "referencia": "PROV-100 · V1", "titulo": "Convenção Comercial", "cliente": "Cliente Teste",
                "observacao": "Confirmar a aprovação do orçamento.",
            })
            assert resposta.status_code == 201
            identificador = resposta.get_json()["followup"]["id"]
            agenda = cliente.get(f"/api/followups?inicio={hoje.isoformat()}&fim={hoje.isoformat()}").get_json()
            assert agenda["sucesso"] is True
            assert len(agenda["dados"]) == 1
            assert agenda["resumo"]["hoje"] == 1

            concluido = cliente.post(f"/api/followups/{identificador}/concluir")
            assert concluido.status_code == 200
            agenda_pendente = cliente.get(f"/api/followups?inicio={hoje.isoformat()}&fim={hoje.isoformat()}").get_json()
            assert agenda_pendente["dados"] == []

            nova_data = (hoje + timedelta(days=2)).isoformat()
            reagendado = cliente.post(f"/api/followups/{identificador}/adiar", json={"data_followup": nova_data})
            assert reagendado.status_code == 200
            agenda_nova = cliente.get(f"/api/followups?inicio={nova_data}&fim={nova_data}").get_json()
            assert agenda_nova["dados"][0]["status"] == "pendente"


def test_perfil_tecnico_nao_altera_followup_comercial():
    app_local = _carregar_app()
    with tempfile.TemporaryDirectory() as diretorio:
        _preparar_usuario(app_local, diretorio, papel="tecnica")
        with app_local.app.test_client() as cliente:
            cliente.post("/login", data={"usuario": "teste", "senha": "SenhaTeste!2026"})
            resposta = cliente.post("/api/followups", json={
                "data_followup": "2026-08-21", "tipo_referencia": "evento", "acao": "ligar",
                "referencia": "EV-123", "titulo": "Evento Teste",
            })
            assert resposta.status_code == 403
            assert "Somente os perfis" in resposta.get_json()["erro"]
            pagina = cliente.get("/followups")
            assert pagina.status_code == 403


def test_interfaces_comercial_e_resposta_de_relatorios_estao_presentes():
    base = Path(__file__).parent
    cabecalho = (base / "templates" / "_cabecalho_soulink.html").read_text(encoding="utf-8")
    followups = (base / "templates" / "followups.html").read_text(encoding="utf-8")
    relatorios = (base / "templates" / "relatorios.html").read_text(encoding="utf-8")
    nova_proposta = (base / "templates" / "index.html").read_text(encoding="utf-8")
    propostas = (base / "templates" / "propostas.html").read_text(encoding="utf-8")
    assert "Comercial" in cabecalho and "/followups" in cabecalho
    assert "Agenda comercial dos próximos sete dias" in followups
    assert "assistente-resposta-usuario" in relatorios
    assert "pedidoOriginalAssistente" in relatorios
    assert "resumo comercial" in nova_proposta.lower()
    assert "resumo_total_equipamentos" in nova_proposta
    assert "resumo_total_servicos" in nova_proposta
    assert "Agendar follow-up" in propostas
    assert "followupForm" in propostas
