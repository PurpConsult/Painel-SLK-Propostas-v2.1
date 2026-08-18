from pypdf import PdfReader

import app as modulo


itens = [
    {"codigo": "1", "nome": "PROJETOR FULL HD", "tipo_item": "Equipamento", "quantidade": 1, "valor": 1000},
    {"codigo": "2", "nome": "COORDENADOR TÉCNICO", "tipo_item": "Serviço", "quantidade": 1, "valor": 550},
]
blocos = modulo.aplicar_desconto_blocos(modulo.calcular_blocos(itens), 0)
dados = {
    "numero": "TESTE-IMPOSTOS",
    "versao": 1,
    "evento": {"nome_evento": "Conferência de validação", "evento_sem_data": True},
    "cliente": {"nome": "Cliente de validação"},
    "itens": itens,
    "blocos": blocos,
    "opcoes_pdf": {"idioma": "pt"},
}

pdf = modulo.gerar_pdf_buffer(dados, "TESTE-IMPOSTOS")
leitor = PdfReader(pdf)
texto = "\n".join(pagina.extract_text() or "" for pagina in leitor.pages)

assert "TOTAL EQUIPAMENTOS (+ 5% DE IMPOSTOS)" in texto
assert "TOTAL SERVIÇOS (+ 5% + 12% DE IMPOSTOS)" in texto
assert "Impostos incluídos: os totais de equipamentos e serviços já contemplam os acréscimos aplicáveis." in texto
assert "R$ 1.050,00" in texto
assert "R$ 580,80" in texto
assert "R$ 1.630,80" in texto
print("OK: PDF comercial informa os impostos incluídos e preserva os valores finais.")
