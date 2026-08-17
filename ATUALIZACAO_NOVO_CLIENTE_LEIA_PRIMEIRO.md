# Atualização local — Cadastro de Novo Cliente

Este pacote acrescenta ao formulário de propostas o fluxo **Novo cliente**. Ele não inclui propostas, PDFs, credenciais, imagens particulares ou arquivos de backup.

## O que muda

No bloco **Dados do Cliente**, o botão **+ Novo cliente** abre um painel de cadastro manual. A equipe escolhe pessoa jurídica ou pessoa física, informa o nome, o contato e os demais dados disponíveis. Ao confirmar, o sistema consulta cadastros semelhantes antes de enviar o novo registro ao Meeventos.

Se for encontrado um possível cadastro repetido, a tela não cria outro cliente. Ela apresenta o cliente já existente para a equipe escolher manualmente. Em uma criação aprovada pelo Meeventos, o cliente novo é selecionado automaticamente no orçamento e seu identificador fica associado à proposta.

## Antes de atualizar

1. Feche a aplicação local com `Ctrl + C` no PowerShell que estiver executando o `app.py`.
2. Faça o backup solicitado no comando de atualização.
3. Nunca copie ou substitua manualmente `propostas.json`, a pasta `pdfs`, arquivos `.env` ou arquivos de backup.
4. Mantenha `MEEVENTOS_TOKEN` configurado no Windows. A credencial continua fora do código e é usada somente pelo backend local.

## Como aplicar

Extraia o arquivo ZIP em uma pasta temporária, copie o conteúdo para a pasta da aplicação e permita substituir somente o `app.py` e o `templates/index.html`. O comando fornecido junto com o pacote já realiza o backup e a cópia dos arquivos necessários.

Depois, inicie normalmente a aplicação:

```powershell
py app.py
```

## Teste recomendado

1. Abra `http://127.0.0.1:5000/` e pesquise primeiro pelo cliente já existente.
2. Se não encontrar, clique em **+ Novo cliente**.
3. Informe nome e ao menos e-mail, celular ou telefone. O CNPJ/CPF não é obrigatório, mas ajuda a evitar duplicidade.
4. Clique em **Cadastrar no Meeventos**.
5. Confirme que a mensagem informa que o cliente foi cadastrado e selecionado no orçamento.
6. Em uma situação de possível duplicidade, use o botão do cadastro existente. Não crie um cliente novo enquanto houver dúvida.

> O cadastro só é enviado ao Meeventos depois da ação manual da equipe. Cancelar o painel não cria registros e restaura o cliente que já estava selecionado no orçamento.
