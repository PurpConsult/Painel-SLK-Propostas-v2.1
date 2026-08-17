import os
import tempfile

import app as modulo


catalogo_teste = [{
    "id": 777,
    "nome": "ITEM DE TESTE",
    "id_cat": 1,
    "valor": 100,
}]

arquivo_original = modulo.ARQUIVO_CORRECOES_TIPO_ITENS
buscar_original = modulo.buscar_paginado

with tempfile.TemporaryDirectory() as diretorio:
    try:
        modulo.ARQUIVO_CORRECOES_TIPO_ITENS = os.path.join(diretorio, "correcoes_tipo_itens.json")
        modulo.buscar_paginado = lambda caminho: catalogo_teste if caminho == "/products-services" else []

        with modulo.app.test_client() as cliente:
            resposta = cliente.post("/api/catalogo/tipo-item", json={"item_id": 777, "tipo_item": "Serviço"})

        assert resposta.status_code == 200
        corpo = resposta.get_json()
        assert corpo["sucesso"] is True
        assert corpo["item"]["tipo_item"] == "Serviço"

        item_recarregado = dict(catalogo_teste[0])
        modulo._aplicar_tipo_item_catalogo(item_recarregado)
        assert item_recarregado["tipo_item"] == "Serviço"
        assert item_recarregado["tipo_corrigido_pela_equipe"] is True
    finally:
        modulo.ARQUIVO_CORRECOES_TIPO_ITENS = arquivo_original
        modulo.buscar_paginado = buscar_original

print("OK: a correção de categoria é persistida e reaplicada ao catálogo.")
