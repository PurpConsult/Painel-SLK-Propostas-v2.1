# Atualização Local — SLK Propostas Pro

Este pacote atualiza apenas o sistema: `app.py`, páginas em `templates/`, documentação e dependências. Ele **não contém** nem substitui `propostas.json` ou a pasta `pdfs`, portanto o histórico e os PDFs existentes permanecem preservados.

## 1. Pare o sistema

No PowerShell em que o sistema estiver executando, pressione:

```text
Ctrl + C
```

## 2. Faça uma cópia de segurança local

Abra o PowerShell na pasta do projeto e execute:

```powershell
Copy-Item app.py app_backup_antes_atualizacao.py
Copy-Item templates templates_backup_antes_atualizacao -Recurse
Copy-Item propostas.json propostas_backup_antes_atualizacao.json -ErrorAction SilentlyContinue
```

## 3. Instale a atualização

1. Extraia o arquivo ZIP recebido **dentro da pasta do projeto**.
2. Quando o Windows perguntar se deseja substituir arquivos, escolha **Substituir os arquivos no destino**.
3. Não apague `propostas.json` e não apague a pasta `pdfs`.

## 4. Inicie novamente

No PowerShell, execute:

```powershell
python app.py
```

Depois, abra `http://localhost:5000` e pressione `Ctrl + F5` no navegador para atualizar a página sem cache.

## 5. Teste seguro recomendado

1. Confirme que o título do navegador e o cabeçalho principal mostram **SOULINK | Orçamentos**.
2. Abra **Meus Orçamentos** e confirme que o cabeçalho está em degradê azul. Clique em **Editar** em uma proposta existente.
3. Confirme que o cabeçalho do formulário informa **EDITAR: Proposta [número]** e que cliente, evento, vendedor, itens e quantidades reaparecem no formulário.
4. Marque **Locação Externa** em um item de teste, informe fornecedor e custo. A margem deve aparecer apenas no controle interno.
5. Gere uma nova versão e confira o histórico. O número original deve ser mantido e o título deve voltar a **SOULINK | Orçamentos**.
6. Baixe o PDF e confirme que fornecedor, custo e margem **não aparecem** para o cliente.
7. No PDF, confirme a validade de 48 horas, os dados bancários, as condições gerais e o nome do vendedor na assinatura.

> Para evitar duplicidade, uma proposta aberta em modo de edição deve gerar uma nova versão interna; o sistema não deve criar um novo orçamento no Meeventos para ela.
