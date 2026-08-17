import io
import json
import tempfile
from unittest.mock import Mock, patch

import app as appmod
import requests
from docx import Document
from reportlab.pdfgen import canvas


def resposta_json(dados, status=200):
    resposta = Mock(status_code=status)
    resposta.json.return_value = dados
    resposta.raise_for_status.return_value = None
    return resposta


def main():
    cliente = appmod.app.test_client()
    texto = b"Evento: Conven\xc3\xa7\xc3\xa3o Nexxus. 300 pessoas. Projetor 5000 lumens, 2 unidades."
    arquivo = cliente.post("/api/ia/briefing/arquivo", data={"arquivo": (io.BytesIO(texto), "briefing.txt")}, content_type="multipart/form-data")
    assert arquivo.status_code == 200, arquivo.get_json()
    assert "Convenção Nexxus" in arquivo.get_json()["texto"]
    pdf = io.BytesIO()
    gerador = canvas.Canvas(pdf)
    gerador.drawString(72, 720, "Briefing PDF: evento para 150 pessoas")
    gerador.save()
    pdf.seek(0)
    arquivo_pdf = cliente.post("/api/ia/briefing/arquivo", data={"arquivo": (pdf, "briefing.pdf")}, content_type="multipart/form-data")
    assert arquivo_pdf.status_code == 200, arquivo_pdf.get_json()
    assert "150 pessoas" in arquivo_pdf.get_json()["texto"]
    documento = Document()
    documento.add_paragraph("Briefing DOCX: lançamento de produto para 120 pessoas")
    docx = io.BytesIO()
    documento.save(docx)
    docx.seek(0)
    arquivo_docx = cliente.post("/api/ia/briefing/arquivo", data={"arquivo": (docx, "briefing.docx")}, content_type="multipart/form-data")
    assert arquivo_docx.status_code == 200, arquivo_docx.get_json()
    assert "120 pessoas" in arquivo_docx.get_json()["texto"]
    invalido = cliente.post("/api/ia/briefing/arquivo", data={"arquivo": (io.BytesIO(b"x"), "briefing.exe")}, content_type="multipart/form-data")
    assert invalido.status_code == 400
    grande = cliente.post("/api/ia/briefing/arquivo", data={"arquivo": (io.BytesIO(b"x" * (5 * 1024 * 1024 + 1)), "briefing.txt")}, content_type="multipart/form-data")
    assert grande.status_code == 400
    assert "5 mb" in grande.get_json()["erro"].lower()

    resposta_modelos = resposta_json({"data": [{"id": "gpt-5-mini"}]})
    analise = {"resumo": "Convenção para 300 pessoas.", "campos": {"nome_evento": "Convenção Nexxus", "local_evento": "", "data_evento": "", "qtd_pessoas": "300", "formato_evento": "", "data_montagem": "", "horario_montagem": "", "horario_inicio_evento": "", "horario_fim_evento": "", "data_desmontagem": "", "horario_desmontagem": "", "nome_cliente": ""}, "itens_solicitados": [{"descricao": "Projetor 5000 lumens", "quantidade": 2}], "alertas": ["Confirme local e data."]}
    resposta_ia = resposta_json({"choices": [{"message": {"content": __import__("json").dumps(analise)}}]})
    catalogo = [{"id": 45, "nome": "PROJETOR 5000 LUMENS", "valor": "1050", "id_cat": "196"}]

    with patch.dict(appmod.os.environ, {"BUILT_IN_FORGE_API_URL": "https://ia.exemplo", "BUILT_IN_FORGE_API_KEY": "segredo"}, clear=False), patch.object(appmod.requests, "get", return_value=resposta_modelos), patch.object(appmod.requests, "post", return_value=resposta_ia), patch.object(appmod, "buscar_paginado", return_value=catalogo):
        resposta = cliente.post("/api/ia/briefing", json={"briefing": "Convenção Nexxus com dois projetores."})
    assert resposta.status_code == 200, resposta.get_json()
    corpo = resposta.get_json()
    assert corpo["dados"]["campos"]["qtd_pessoas"] == "300"
    candidato = corpo["dados"]["sugestoes_itens"][0]["candidatos"][0]
    assert candidato["id"] == 45
    assert candidato["valor"] == 1050.0
    assert "nenhum orçamento foi alterado" in corpo["dados"]["aviso"].lower()

    catalogo_relevancia = [
        {"id": 1, "nome": "NOTEBOOK I5", "valor": "250", "id_cat": "196"},
        {"id": 2, "nome": "PASSADOR DE SLIDES LOGITECH", "valor": "80", "id_cat": "196"},
        {"id": 251, "nome": "ASSENTOS PARA ARQUIBANCADA", "valor": "104", "id_cat": "188"},
        {"id": 101, "nome": "TOTEM CARREGADOR", "valor": "190", "id_cat": "242"},
        {"id": 321, "nome": "JARDINEIRA PARA PALCO", "valor": "220", "id_cat": "305"},
        {"id": 256, "nome": "VASO DE VIDRO", "valor": "50", "id_cat": "305"},
        {"id": 23, "nome": "ARRANJO DE FLORES", "valor": "31.5", "id_cat": "305"},
    ]
    sugestoes_relevantes = appmod._sugerir_itens_catalogo([
        {"descricao": "Notebook para apresentação", "quantidade": 1},
        {"descricao": "Passador de slides", "quantidade": 1},
    ], catalogo_relevancia)
    assert [item["id"] for item in sugestoes_relevantes[0]["candidatos"]] == [1]
    assert [item["id"] for item in sugestoes_relevantes[1]["candidatos"]] == [2]

    catalogo_aprendizado = [
        {"id": 1, "nome": "NOTEBOOK I5", "valor": "250", "id_cat": "196"},
        {"id": 2, "nome": "NOTEBOOK I7", "valor": "320", "id_cat": "196"},
        {"id": 3, "nome": "VASO DE VIDRO", "valor": "50", "id_cat": "305"},
    ]
    with tempfile.TemporaryDirectory() as pasta_temporaria:
        arquivo_aprendizado = f"{pasta_temporaria}/aprendizados.json"
        with patch.object(appmod, "ARQUIVO_APRENDIZADOS_CATALOGO", arquivo_aprendizado), patch.object(appmod, "buscar_paginado", return_value=catalogo_aprendizado):
            salvo = cliente.post("/api/ia/aprendizados", json={"pedido": "Notebook para apresentação", "itens": [1, 2]})
            assert salvo.status_code == 200, salvo.get_json()
            assert [item["id"] for item in salvo.get_json()["itens"]] == [1, 2]
            aprendidos = appmod._sugerir_itens_catalogo([{"descricao": "Notebook para apresentação", "quantidade": 1}], catalogo_aprendizado)
            assert [item["id"] for item in aprendidos[0]["candidatos"][:2]] == [1, 2]
            assert all(item["origem"] == "Ensinado pela equipe" for item in aprendidos[0]["candidatos"][:2])
            removido = cliente.post("/api/ia/aprendizados/remover", json={"pedido": "Notebook para apresentação", "item_id": 1})
            assert removido.status_code == 200, removido.get_json()
            apos_remocao = appmod._sugerir_itens_catalogo([{"descricao": "Notebook para apresentação", "quantidade": 1}], catalogo_aprendizado)
            assert apos_remocao[0]["candidatos"][0]["id"] == 2
            assert apos_remocao[0]["candidatos"][0]["origem"] == "Ensinado pela equipe"

    resposta_markdown = '''Aqui está a extração solicitada:
```json
{
  "resumo": "Convenção Nexxus para 80 pessoas.",
  "campos": {"nome_evento": "Convenção Nexxus", "local_evento": "Hotel Laghetto", "data_evento": "2026-09-25"},
  "itens_solicitados": [{"descricao": "projetor", "quantidade": "2"}],
  "alertas": ["Conferir antes de aplicar."]
}
```
'''
    analise_markdown = appmod._normalizar_analise_briefing(appmod._extrair_json_resposta_ia(resposta_markdown))
    assert analise_markdown["campos"]["nome_evento"] == "Convenção Nexxus"
    assert analise_markdown["campos"]["nome_cliente"] == ""
    assert analise_markdown["itens_solicitados"] == [{"descricao": "projetor", "quantidade": 2}]
    assert appmod._extrair_json_resposta_ia(json.dumps(json.dumps(analise))) == analise

    resposta_anthropic = resposta_json({"content": [
        {"type": "thinking", "thinking": "Analisando o briefing."},
        {"type": "text", "text": json.dumps(analise)},
    ]})
    with patch.dict(appmod.os.environ, {"ANTHROPIC_API_KEY": "chave-teste", "ANTHROPIC_MODEL": "claude-haiku-4-5-20251001"}, clear=True), patch.object(appmod.requests, "post", return_value=resposta_anthropic) as post_anthropic:
        resultado_anthropic, modelo_anthropic = appmod._analisar_briefing_com_ia("Convenção Nexxus com dois projetores.")
    corpo_anthropic = post_anthropic.call_args.kwargs["json"]
    assert modelo_anthropic == "claude-haiku-4-5-20251001"
    assert resultado_anthropic["campos"]["nome_evento"] == "Convenção Nexxus"
    assert corpo_anthropic["output_config"]["format"]["type"] == "json_schema"
    assert corpo_anthropic["output_config"]["format"]["schema"]["required"] == ["resumo", "campos", "itens_solicitados", "alertas"]
    try:
        appmod._extrair_json_resposta_ia("Não encontrei dados suficientes para criar uma análise.")
        assert False, "Era esperado erro para resposta sem JSON"
    except ValueError:
        pass

    erro_modelo = requests.HTTPError("Modelo Claude recusado")
    erro_modelo.response = resposta_json({"error": {"message": "model: claude-sonnet indisponível"}}, status=400)
    with patch.object(appmod, "_analisar_briefing_com_ia", side_effect=erro_modelo):
        resposta_erro = cliente.post("/api/ia/briefing", json={"briefing": "Teste de disponibilidade do Claude"})
    assert resposta_erro.status_code == 503, resposta_erro.get_json()
    assert "anthropic_model" in resposta_erro.get_json()["erro"].lower()
    assert "segredo" not in resposta_erro.get_json()["erro"].lower()

    with open("templates/index.html", encoding="utf-8") as arquivo_html:
        pagina = arquivo_html.read()
    assert "Preencher somente os campos que estão vazios" in pagina
    assert "Os valores serão os do catálogo oficial" in pagina
    assert "Ensinar opções corretas para este pedido" in pagina
    assert "/ia/aprendizados/remover" in pagina
    print("OK: briefing, catálogo, filtro de relevância e aprendizado supervisionado validados.")


if __name__ == "__main__":
    main()
