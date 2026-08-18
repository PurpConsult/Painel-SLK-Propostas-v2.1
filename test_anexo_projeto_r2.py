import io
import json
import os
import tempfile
from unittest.mock import patch

import app as modulo


class ClienteR2Falso:
    def __init__(self):
        self.envios = []

    def put_object(self, **kwargs):
        self.envios.append(kwargs)

    def generate_presigned_url(self, operacao, Params, ExpiresIn):
        assert operacao == "get_object"
        assert Params["Bucket"] == "soulink-projetos"
        assert ExpiresIn == 604800
        return f"https://link-seguro.exemplo/{Params['Key']}"


def main():
    configuracao_original = {
        "R2_ACCOUNT_ID": modulo.R2_ACCOUNT_ID,
        "R2_ACCESS_KEY_ID": modulo.R2_ACCESS_KEY_ID,
        "R2_SECRET_ACCESS_KEY": modulo.R2_SECRET_ACCESS_KEY,
        "R2_BUCKET_NAME": modulo.R2_BUCKET_NAME,
        "R2_LINK_TTL_SECONDS": modulo.R2_LINK_TTL_SECONDS,
    }
    try:
        modulo.R2_ACCOUNT_ID = "conta-teste"
        modulo.R2_ACCESS_KEY_ID = "chave-teste"
        modulo.R2_SECRET_ACCESS_KEY = "segredo-teste"
        modulo.R2_BUCKET_NAME = "soulink-projetos"
        modulo.R2_LINK_TTL_SECONDS = 604800
        cliente_r2 = ClienteR2Falso()
        cliente = modulo.app.test_client()

        with patch.object(modulo, "_criar_cliente_r2", return_value=cliente_r2):
            resposta = cliente.post(
                "/api/upload-anexo-projeto",
                data={"arquivo": (io.BytesIO(b"%PDF-1.7\nPDF de teste"), "projeto do cliente.pdf")},
                content_type="multipart/form-data",
            )

        assert resposta.status_code == 200, resposta.get_data(as_text=True)
        corpo = resposta.get_json()
        assert corpo["sucesso"] is True
        assert corpo["anexo_projeto_nome"] == "projeto_do_cliente.pdf"
        assert corpo["link_projeto"].startswith("https://link-seguro.exemplo/")
        assert cliente_r2.envios[0]["ContentType"] == "application/pdf"
        assert cliente_r2.envios[0]["Body"].startswith(b"%PDF-")

        resposta_invalida = cliente.post(
            "/api/upload-anexo-projeto",
            data={"arquivo": (io.BytesIO(b"arquivo invalido"), "projeto.txt")},
            content_type="multipart/form-data",
        )
        assert resposta_invalida.status_code == 400
        assert "PDF" in resposta_invalida.get_json()["erro"]

        with tempfile.TemporaryDirectory() as pasta_teste:
            arquivo_propostas = os.path.join(pasta_teste, "propostas.json")
            pasta_pdfs = os.path.join(pasta_teste, "pdfs")
            proposta = {
                "nome_evento": "Evento de teste",
                "evento_sem_data": True,
                "cliente_nome": "Cliente teste",
                "cliente_email": "cliente@exemplo.com",
                "cliente_telefone": "21999999999",
                "cliente_contato": "Contato teste",
                "itens": [{"codigo": "1", "nome": "Tela", "quantidade": 1, "valor": 1000, "tipo": "equipamento"}],
                "anexo_projeto_chave": "projetos/teste/projeto.pdf",
                "anexo_projeto_nome": "projeto.pdf",
            }
            with patch.object(modulo, "ARQUIVO_PROPOSTAS", arquivo_propostas), \
                 patch.object(modulo, "PASTA_PDFS", pasta_pdfs), \
                 patch.object(modulo, "_gerar_link_assinado_r2", return_value="https://link-seguro.exemplo/renovado") as renovar_link:
                criada = cliente.post("/api/gerar-proposta", json=proposta)
                assert criada.status_code == 200, criada.get_data(as_text=True)
                with open(arquivo_propostas, encoding="utf-8") as arquivo:
                    historico = json.load(arquivo)
                assert historico[0]["anexo_projeto_chave"] == "projetos/teste/projeto.pdf"
                assert historico[0]["link_projeto"] == "https://link-seguro.exemplo/renovado"
                numero = criada.get_json()["numero_proposta"]
                reemitida = cliente.post(f"/api/propostas/{numero}/versoes/1/reemitir-pdf", json={"idioma": "en"})
                assert reemitida.status_code == 200, reemitida.get_data(as_text=True)
                assert renovar_link.call_count >= 2

        print("OK: upload de PDF para R2, link seguro, histórico e reemissão validados.")
    finally:
        for chave, valor in configuracao_original.items():
            setattr(modulo, chave, valor)


if __name__ == "__main__":
    main()
