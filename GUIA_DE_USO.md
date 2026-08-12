# Guia de Uso — SLK Propostas Pro

## Iniciar a aplicação

Na pasta do projeto, abra o PowerShell e execute:

```powershell
python app.py
```

Em seguida, abra `http://localhost:5000` no navegador. Para encerrar o servidor, volte ao PowerShell e pressione `Ctrl + C`.

## Criar uma proposta

Preencha vendedor, dados do evento e dados do cliente. Os campos de vendedor, local e cliente aceitam busca. Ao selecionar um cliente cadastrado, confira os dados preenchidos automaticamente. Pesquise os itens pelo nome ou pelo ID, ajuste as quantidades e revise a prévia antes de gerar.

Ao gerar uma **nova proposta**, o sistema solicita a criação do orçamento no Meeventos, gera o PDF e salva uma cópia completa dos dados no histórico local. O número do Meeventos passa a ser o número de referência da proposta e do PDF.

## Editar uma proposta existente

Abra **Meus Orçamentos** e clique em **Editar**. O formulário deve reabrir com cliente, evento, vendedor, itens, quantidades e valores da versão escolhida. Ao gerar novamente, o documento mantém o mesmo número original e recebe uma nova versão no histórico.

> A edição preserva o número original no controle interno. Não é criado um novo orçamento no Meeventos para cada versão, evitando duplicidade no ERP.

## Arquivos gerados

| Arquivo ou pasta | Finalidade |
|---|---|
| `propostas.json` | Histórico local das propostas e de suas versões. Não apague este arquivo. |
| `pdfs/` | PDFs das versões geradas. |
| `app.py` | Backend e gerador de PDF. |
| `templates/` | Páginas do formulário, itens e histórico. |

## Atualizar o código com segurança

Antes de usar `git pull`, faça uma cópia de segurança do seu `app.py` caso tenha feito alterações manuais:

```powershell
Copy-Item app.py app_backup_manual.py
```

Depois, você poderá comparar suas alterações com a atualização recebida, sem perder trabalho local.

## Como os testes são conduzidos

Os testes automatizados utilizam dados temporários e simulam exclusivamente a resposta externa do Meeventos. Eles validam que o sistema gera PDF, salva a proposta e monta corretamente a solicitação de orçamento, **sem criar propostas de teste no ERP**.

O envio real ao Meeventos é validado pela operação ao criar uma proposta legítima. Essa escolha evita poluir o ambiente comercial com orçamentos artificiais.
