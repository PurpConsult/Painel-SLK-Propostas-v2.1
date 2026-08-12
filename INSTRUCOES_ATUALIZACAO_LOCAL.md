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

1. Abra **Meus Orçamentos** e clique em **Editar** em uma proposta existente.
2. Confirme que cliente, evento, vendedor, itens e quantidades reaparecem no formulário.
3. Marque **Locação Externa** em um item de teste, informe fornecedor e custo. A margem deve aparecer apenas no controle interno.
4. Gere uma nova versão e confira o histórico. O número original deve ser mantido.
5. Baixe o PDF e confirme que fornecedor, custo e margem **não aparecem** para o cliente.

> Para evitar duplicidade, uma proposta aberta em modo de edição deve gerar uma nova versão interna; o sistema não deve criar um novo orçamento no Meeventos para ela.
