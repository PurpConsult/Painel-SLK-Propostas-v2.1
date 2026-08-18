import json
import os
import tempfile

import app as modulo


buscar_original = modulo.buscar_paginado
arquivo_kits_original = modulo.ARQUIVO_CATALOGO_KITS_LOCAIS


def buscar_teste(_endpoint, max_pages=10):
    return []


with tempfile.TemporaryDirectory() as diretorio:
    arquivo_kits = os.path.join(diretorio, "kits.json")
    with open(arquivo_kits, "w", encoding="utf-8") as arquivo:
        json.dump({
            "kits": [{
                "id": "piloto",
                "nome": "A/V - LAGHETTO - FERNANDO PESSOA I E II",
                "valor": 3665.28,
                "componentes": [
                    {"id_meeventos": "161", "nome": "CAIXA DE SOM", "quantidade": 4},
                    {"id_meeventos": "24", "nome": "DISTRIBUIDOR HDMI 1 X 4", "quantidade": 1},
                ],
            }]
        }, arquivo, ensure_ascii=False)
    try:
        modulo.buscar_paginado = buscar_teste
        modulo.ARQUIVO_CATALOGO_KITS_LOCAIS = arquivo_kits
        catalogo, avisos = modulo._buscar_catalogo_ampliado()
        kit = next(item for item in catalogo if item["id"] == "kit-local:piloto")
        assert avisos == []
        assert kit["nome"] == "KIT A/V - LAGHETTO - FERNANDO PESSOA I E II"
        assert kit["tipo_item"] == "Equipamento"
        assert kit["item_de_composicao"] is True
        assert kit["valor"] == 3665.28
        assert [(item["id_meeventos"], item["quantidade"]) for item in kit["componentes"]] == [("161", 4), ("24", 1)]
        with modulo.app.test_client() as cliente:
            resposta = cliente.get("/api/produtos-catalogo")
            assert resposta.status_code == 200, resposta.get_json()
            retornado = next(item for item in resposta.get_json()["dados"] if item["id"] == "kit-local:piloto")
            assert retornado["nome"] == "KIT A/V - LAGHETTO - FERNANDO PESSOA I E II"
            assert retornado["componentes"][0]["id_meeventos"] == "161"
    finally:
        modulo.buscar_paginado = buscar_original
        modulo.ARQUIVO_CATALOGO_KITS_LOCAIS = arquivo_kits_original


print("OK: kit piloto local entra como equipamento e preserva os componentes associados.")
