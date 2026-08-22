# Guia de Uso — SLK Propostas Pro

# SOULINK | Orçamentos — Guia de Uso

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

Enquanto a proposta estiver aberta para edição, o cabeçalho exibirá **EDITAR: Proposta [número]**. Após salvar a nova versão, o título volta para **SOULINK | Orçamentos**.

## Construir uma proposta a partir de briefing

No bloco **Prévia assistida por IA**, descreva o briefing ou envie um arquivo `TXT`, `PDF` ou `DOCX` de até 5 MB. A análise apresenta somente uma sugestão para revisão: ela não preenche o formulário, não adiciona itens e não envia informações ao Meeventos automaticamente. Revise os dados encontrados e clique em **Aplicar sugestões** apenas se desejar copiar a sugestão para o formulário.

> Os preços e os itens sugeridos vêm exclusivamente do catálogo oficial carregado do Meeventos. A IA não define valores nem cria itens fora desse catálogo.

Para ativar essa função no computador local, configure a chave Claude como variável de ambiente do Windows. Siga o arquivo `INSTRUCOES_IA_CLAUDE_LOCAL.md`; a chave não deve ser inserida em `app.py`, no GitHub ou em arquivos do projeto.

## Usar imagens de itens no PDF

Abra **Meus Itens** e revise as imagens candidatas. Use **Aprovar** somente quando a foto representar corretamente o item. Apenas fotos aprovadas podem aparecer no PDF comercial, em miniatura clicável; ao clicar, o cliente pode abrir a imagem em tamanho maior. Uma imagem rejeitada não será inserida nas próximas propostas.

## Controlar pré-reserva, aprovação e financeiro

Em **Meus Orçamentos**, os botões da última versão permitem marcar a proposta como **Pré-reserva**, **Aprovada** ou **Perdida**. Quando aprovada, a versão fica protegida como uma cópia fechada; novas edições continuam como nova versão de trabalho, sem alterar o registro aprovado. A página **Financeiro** exibe exclusivamente versões aprovadas, em modo de consulta e com acesso ao PDF.

## Usar a Central Financeira

A área **Financeiro** está dividida em quatro rotinas: **Visão geral**, **Contas a receber**, **Conciliação CSV** e **Lançamentos**. A Visão geral mostra os recebimentos em aberto, vencidos e pagos; Contas a receber separa receitas; e Lançamentos permite consultar receitas e despesas retornadas pelo Meeventos.

> A Central Financeira funciona somente em modo de leitura. Ela não cria cobranças, não altera registros e não realiza baixas no Meeventos.

Na Conciliação CSV, o extrato é lido apenas no navegador para gerar uma prévia. Nenhum arquivo é enviado ou gravado, e nenhuma correspondência será confirmada automaticamente. Quando houver um CSV de exemplo sem dados sensíveis, os cabeçalhos reais poderão ser mapeados para a etapa de sugestões e conferência humana.

## Consultar dados com a assistente de Relatórios

Na tela **Relatórios**, descreva a necessidade em linguagem natural. Quando o pedido trouxer uma consulta clara, como “quero os eventos de junho, julho e agosto de 2026”, a assistente consulta apenas os dados permitidos do Meeventos e apresenta uma amostra para refinamento. Caso o serviço de IA esteja indisponível, o sistema ainda consegue reconhecer pedidos diretos de eventos, orçamentos, clientes ou lançamentos financeiros, sempre em modo somente leitura.

Nenhuma consulta cria, edita ou exclui dados no Meeventos. A criação de PDF e quaisquer decisões comerciais continuam sujeitas à revisão humana.

## Conferir o PDF comercial e escolher o idioma

No formulário, em **Opções da cópia comercial**, escolha **Português**, **Inglês** ou **Espanhol** antes de gerar. O PDF traduz cabeçalhos, condições e nomes de todos os itens do catálogo, preservando internamente o nome original em português e o mesmo ID para histórico e Meeventos. O PDF também apresenta a forma de pagamento, a validade escolhida, os dados bancários da SLK Eventos e as condições gerais aprovadas. Ao final, a assinatura usa automaticamente o nome do vendedor selecionado na proposta.

## Arquivos gerados

| Arquivo ou pasta | Finalidade |
|---|---|
| `propostas.json` | Histórico local das propostas e de suas versões. Não apague este arquivo. |
| `pdfs/` | PDFs das versões geradas. |
| `app.py` | Backend e gerador de PDF. |
| `templates/` | Páginas do formulário, itens e histórico. |
| `catalogo_traducoes_por_id.json` | Traduções comerciais em inglês e espanhol ligadas aos IDs do catálogo. Não altere os IDs. |
| `catalogo_imagens_sugeridas.json` | Candidatas de imagem pesquisadas para revisão humana. |

## Atualizar o código com segurança

Antes de usar `git pull`, faça uma cópia de segurança do seu `app.py` caso tenha feito alterações manuais:

```powershell
Copy-Item app.py app_backup_manual.py
```

Depois, você poderá comparar suas alterações com a atualização recebida, sem perder trabalho local.

## Como os testes são conduzidos

Os testes automatizados utilizam dados temporários e simulam exclusivamente a resposta externa do Meeventos. Eles validam que o sistema gera PDF, salva a proposta e monta corretamente a solicitação de orçamento, **sem criar propostas de teste no ERP**.

O envio real ao Meeventos é validado pela operação ao criar uma proposta legítima. Essa escolha evita poluir o ambiente comercial com orçamentos artificiais.
