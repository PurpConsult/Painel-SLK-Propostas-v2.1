import json
import os
import tempfile

import app as modulo


payload_simplificado = {
    "vendedor_nome": "Jairo",
    "id_vendedor": "62",
    "nome_evento": "Evento de validação simplificada",
    "local_nome": "Local de teste",
    "data_evento": "",
    "evento_sem_data": True,
    "qtd_pessoas": "50",
    "cliente_nome": "Cliente de validação",
    "cliente_cnpj": "12.345.678/0001-00",
    "cliente_email": "cliente@example.com",
    "cliente_telefone": "21999999999",
    "cliente_contato": "Responsável de teste",
    "validade_proposta": "2026-08-24",
    "desconto_proposta": 25,
    "observacoes_gerais": "Validação sem envio ao Meeventos.",
    "itens": [
        {
            "id": 901,
            "nome": "PROJETOR DE TESTE",
            "tipo_item": "Equipamento",
            "quantidade": 2,
            "valor": 100,
            "valor_manual": 125,
            "externo": True,
        },
        {
            "id": 902,
            "nome": "TÉCNICO DE TESTE",
            "tipo_item": "Serviço",
            "quantidade": 1,
            "valor": 480,
            "externo": False,
        },
    ],
}


arquivo_propostas_original = modulo.ARQUIVO_PROPOSTAS
pasta_pdfs_original = modulo.PASTA_PDFS

with tempfile.TemporaryDirectory() as diretorio:
    try:
        modulo.ARQUIVO_PROPOSTAS = os.path.join(diretorio, "propostas.json")
        modulo.PASTA_PDFS = os.path.join(diretorio, "pdfs")

        with modulo.app.test_client() as cliente:
            resposta = cliente.post("/api/gerar-proposta", json=payload_simplificado)
            assert resposta.status_code == 200
            corpo = resposta.get_json()
            assert corpo["sucesso"] is True
            assert corpo["enviado_meeventos"] is False
            assert corpo["blocos"]["total_bruto"] == 730.0
            assert corpo["blocos"]["desconto"] == 25.0
            assert corpo["blocos"]["total_geral"] == 705.0

            resposta_pdf = cliente.get(corpo["url_pdf"])
            assert resposta_pdf.status_code == 200
            assert resposta_pdf.mimetype == "application/pdf"
            assert len(resposta_pdf.data) > 1000

        with open(modulo.ARQUIVO_PROPOSTAS, "r", encoding="utf-8") as arquivo:
            historico = json.load(arquivo)

        assert len(historico) == 1
        proposta = historico[0]
        assert proposta["arquivo_pdf"] == corpo["arquivo_pdf"]
        assert proposta["controle_locacao_externa"]["quantidade_itens"] == 1
        assert proposta["itens"][0]["externo"] is True
        assert proposta["desconto_proposta"] == 25.0
        assert os.path.exists(os.path.join(modulo.PASTA_PDFS, corpo["arquivo_pdf"]))
    finally:
        modulo.ARQUIVO_PROPOSTAS = arquivo_propostas_original
        modulo.PASTA_PDFS = pasta_pdfs_original

print("OK: envio simplificado gera PDF, registra histórico, desconto e locação externa sem criar orçamento no Meeventos.")
