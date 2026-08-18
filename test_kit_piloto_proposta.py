import json
import json
import os
import tempfile

import app as modulo


arquivo_propostas_original = modulo.ARQUIVO_PROPOSTAS
pasta_pdfs_original = modulo.PASTA_PDFS

payload = {
    "vendedor_nome": "Jairo",
    "id_vendedor": "62",
    "nome_evento": "Validação do kit piloto",
    "local_nome": "Local de teste",
    "evento_sem_data": True,
    "cliente_nome": "Cliente de validação",
    "validade_proposta": "2026-08-24",
    "itens": [{
        "id": "kit-local:av-laghetto-fernando-pessoa-i-e-ii",
        "id_kit_local": "av-laghetto-fernando-pessoa-i-e-ii",
        "nome": "KIT A/V - LAGHETTO - FERNANDO PESSOA I E II",
        "tipo_item": "Equipamento",
        "origem_catalogo": "Kits cadastrados localmente",
        "quantidade": 1,
        "valor": 1196.00,
        "valor_padrao": 1196.00,
        "componentes": [
            {"id_meeventos": "161", "nome": "CAIXA DE SOM", "quantidade": 5, "valor_unitario": 239.20},
        ],
    }],
}


with tempfile.TemporaryDirectory() as diretorio:
    try:
        modulo.ARQUIVO_PROPOSTAS = os.path.join(diretorio, "propostas.json")
        modulo.PASTA_PDFS = os.path.join(diretorio, "pdfs")
        with modulo.app.test_client() as cliente:
            resposta = cliente.post("/api/gerar-proposta", json=payload)
            assert resposta.status_code == 200, resposta.get_json()
            corpo = resposta.get_json()
            assert corpo["sucesso"] is True
            assert corpo["blocos"]["locacao"]["subtotal"] == 1196.00
            assert corpo["blocos"]["locacao"]["total"] == 1255.80

        with open(modulo.ARQUIVO_PROPOSTAS, "r", encoding="utf-8") as arquivo:
            proposta = json.load(arquivo)[0]
        kit = proposta["itens"][0]
        assert kit["id_kit_local"] == "av-laghetto-fernando-pessoa-i-e-ii"
        assert kit["origem_catalogo"] == "Kits cadastrados localmente"
        assert kit["componentes"][0]["id_meeventos"] == "161"
        assert kit["valor"] == 1196.00
        assert kit["valor_padrao"] == 1196.00
        assert kit["componentes"][0]["quantidade"] == 5
        assert kit["componentes"][0]["valor_unitario"] == 239.20
        assert all(componente["id_meeventos"] != "24" for componente in kit["componentes"])
        assert os.path.exists(os.path.join(modulo.PASTA_PDFS, corpo["arquivo_pdf"]))
    finally:
        modulo.ARQUIVO_PROPOSTAS = arquivo_propostas_original
        modulo.PASTA_PDFS = pasta_pdfs_original


print("OK: kit piloto preserva a composição editada, o valor recalculado e a remoção de componentes no histórico.")
