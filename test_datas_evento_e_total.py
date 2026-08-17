import os
import tempfile

from pypdf import PdfReader

import app as modulo


payload = {
    "evento": {
        "nome_evento": "Reunião de validação",
        "data_evento_inicio": "2026-09-24",
        "data_evento_final": "2026-09-25",
        "evento_sem_data": False,
    },
    "desconto_proposta": 30,
    "itens": [
        {
            "id": 9101,
            "nome": "PROJETOR DE 5000 LUMES",
            "tipo_item": "Equipamento",
            "quantidade": 2,
            "valor": 1050,
            "valor_manual": "125",
            "externo": True,
            "fornecedor_externo": "Fornecedor de teste",
            "custo_externo": 80,
        },
        {
            "id": 9102,
            "nome": "TÉCNICO AUDIOVISUAL",
            "tipo_item": "Serviço",
            "quantidade": 1,
            "valor": 480,
        },
    ],
}

dados = modulo.normalizar_dados_proposta(payload)
blocos = modulo.aplicar_desconto_blocos(
    modulo.calcular_blocos(dados["itens"]), dados["desconto_proposta"]
)

assert dados["evento"]["data_evento_inicio"] == "2026-09-24"
assert dados["evento"]["data_evento_final"] == "2026-09-25"
assert dados["evento"]["data_evento"] == "2026-09-24"
assert dados["controle_locacao_externa"]["quantidade_itens"] == 1
assert dados["controle_locacao_externa"]["custo"] == 160.0
assert blocos["locacao"]["subtotal"] == 250.0
assert blocos["servicos"]["subtotal"] == 480.0
assert blocos["desconto"] == 30.0
assert blocos["total_geral"] == 700.0

dados["blocos"] = blocos
pdf = modulo.gerar_pdf_buffer(dados, "TESTE-DATAS")
with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as arquivo_temporario:
    arquivo_temporario.write(pdf.getvalue())
    caminho_pdf = arquivo_temporario.name

try:
    texto_pdf = "\n".join(pagina.extract_text() or "" for pagina in PdfReader(caminho_pdf).pages)
    assert "24/09/2026" in texto_pdf
    assert "25/09/2026" in texto_pdf
    assert "700,00" in texto_pdf
finally:
    os.unlink(caminho_pdf)

print("OK: datas de início/final, locação externa e total com desconto estão preservados no PDF.")
