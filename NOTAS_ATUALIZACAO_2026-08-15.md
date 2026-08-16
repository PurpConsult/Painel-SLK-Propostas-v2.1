# Notas da Atualização — 15 de agosto de 2026

Esta atualização reúne os recursos comerciais implementados após a versão de 12 de agosto. A instalação deve preservar obrigatoriamente o arquivo `propostas.json` e a pasta `pdfs/`, pois eles concentram o histórico e os documentos comerciais já emitidos.

| Recurso | Resultado entregue |
|---|---|
| Imagens de itens | Revisão humana por aprovação/rejeição; somente imagens aprovadas entram no PDF com link clicável. |
| Status comercial | Pré-reserva, aprovada e perdida registrados por versão, sem alteração do orçamento aceito. |
| Financeiro | Página apenas de consulta das versões aprovadas e de seus PDFs. |
| Briefing assistido | Leitura de texto, PDF e DOCX de até 5 MB; sugestões revisáveis que não aplicam dados automaticamente. |
| Catálogo e valores | Itens sugeridos sempre vêm do catálogo oficial; a IA não inventa preços. |
| Idiomas | Cópia comercial do PDF em Português, Inglês ou Espanhol, com 377 nomes de itens traduzidos por ID. |

## Atualização segura

1. Faça uma cópia da pasta atual da ferramenta.
2. Feche a aplicação, se ela estiver em execução no PowerShell.
3. Extraia o conteúdo do pacote por cima da pasta da ferramenta.
4. Quando o Windows perguntar se deseja substituir arquivos, confirme para os arquivos de aplicação, **mas não substitua** `propostas.json` nem a pasta `pdfs/`.
5. No PowerShell, dentro da pasta da ferramenta, execute `pip install -r requirements.txt` e depois `python app.py`.

> O pacote não inclui propostas, PDFs de clientes, token de API ou qualquer dado comercial pré-existente.
