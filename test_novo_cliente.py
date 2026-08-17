import importlib.util
import os
from unittest.mock import Mock, patch


CAMINHO = os.path.join(os.path.dirname(__file__), "app.py")
ESPEC = importlib.util.spec_from_file_location("soulink_app_novo_cliente", CAMINHO)
appmod = importlib.util.module_from_spec(ESPEC)
ESPEC.loader.exec_module(appmod)


def resposta_json(dados):
    resposta = Mock()
    resposta.json.return_value = dados
    resposta.raise_for_status.return_value = None
    return resposta


def payload_pj():
    return {
        "tipo_cadastro": "pj",
        "razao_social": "Empresa Teste LTDA",
        "nome_fantasia": "Empresa Teste",
        "documento": "12.345.678/0001-90",
        "email": "contato@empresateste.com.br",
        "telefone": "(21) 3333-2222",
        "responsavel": "Ana Responsável",
        "cidade": "Rio de Janeiro",
        "estado": "rj",
    }


def testar_criacao_com_sucesso():
    cliente_http = appmod.app.test_client()
    buscas_sem_resultado = [resposta_json({"data": []}) for _ in range(3)]
    retorno_criacao = resposta_json({"status": "success", "data": [{"id": "9001", "cliente": "Empresa Teste LTDA"}]})
    with patch.object(appmod, "TOKEN", "token-de-teste"), patch.object(appmod.requests, "get", side_effect=buscas_sem_resultado) as busca, patch.object(appmod.requests, "post", return_value=retorno_criacao) as criar:
        resposta = cliente_http.post("/api/clientes/novo", json=payload_pj())
    assert resposta.status_code == 201, resposta.get_data(as_text=True)
    corpo = resposta.get_json()
    assert corpo["sucesso"] is True
    assert corpo["cliente"]["id"] == "9001"
    assert corpo["cliente"]["cnpjpj"] == "12345678000190"
    assert corpo["cliente"]["estado"] if "estado" in corpo["cliente"] else True
    assert busca.call_count == 3
    enviado = criar.call_args.kwargs["json"]
    assert isinstance(enviado, list) and len(enviado) == 1
    assert enviado[0]["tipocadastro"] == 1
    assert enviado[0]["cnpjpj"] == "12345678000190"
    assert enviado[0]["razaosocial"] == "Empresa Teste LTDA"


def testar_duplicidade_bloqueia_criacao():
    cliente_http = appmod.app.test_client()
    existente = {"id": "48", "nome": "Empresa Teste LTDA", "cnpjpj": "12345678000190", "email": "contato@empresateste.com.br"}
    respostas_busca = [resposta_json({"data": [existente]}) for _ in range(3)]
    with patch.object(appmod, "TOKEN", "token-de-teste"), patch.object(appmod.requests, "get", side_effect=respostas_busca), patch.object(appmod.requests, "post") as criar:
        resposta = cliente_http.post("/api/clientes/novo", json=payload_pj())
    assert resposta.status_code == 409
    corpo = resposta.get_json()
    assert corpo["duplicado"] is True
    assert corpo["dados"][0]["id"] == "48"
    criar.assert_not_called()


def testar_dados_invalidos_nao_consultam_api():
    cliente_http = appmod.app.test_client()
    with patch.object(appmod, "TOKEN", "token-de-teste"), patch.object(appmod.requests, "get") as busca, patch.object(appmod.requests, "post") as criar:
        resposta = cliente_http.post("/api/clientes/novo", json={"tipo_cadastro": "pj", "razao_social": "AB", "email": "invalido"})
    assert resposta.status_code == 400
    assert "razão social" in resposta.get_json()["erro"]
    busca.assert_not_called()
    criar.assert_not_called()


def testar_id_cliente_e_preservado_na_proposta():
    dados = appmod.normalizar_dados_proposta({"cliente_id": "9001", "cliente_nome": "Empresa Teste LTDA"})
    assert dados["cliente"]["id"] == "9001"


if __name__ == "__main__":
    testar_criacao_com_sucesso()
    testar_duplicidade_bloqueia_criacao()
    testar_dados_invalidos_nao_consultam_api()
    testar_id_cliente_e_preservado_na_proposta()
    print("OK: criação manual, duplicidade, validação e identificação de novo cliente validadas.")
