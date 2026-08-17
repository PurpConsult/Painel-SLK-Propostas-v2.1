# Validação — Área de Relatórios

## Revisão inicial

Em 17/08/2026, a página local `/relatorios` foi aberta no navegador. A interface carregou a configuração **Lagune Barra Hotel — comissão de 15%**, os campos de período e os controles de geração, recálculo e exportação.

| Item validado | Resultado |
|---|---|
| Rota `/relatorios` | Carregada corretamente. |
| Navegação principal | Painel, Meus Orçamentos, Financeiro e Meus Itens visíveis. |
| Configuração comercial | Hotel e comissão apresentados a partir da configuração local. |
| Aviso de revisão humana | Visível antes de qualquer exclusão. |
| Consulta real | Iniciada em modo somente leitura para o período de 01/01/2026 a 17/08/2026; a resposta ainda estava em processamento na observação inicial. |

## Regras de validação

Os testes automatizados cobrem o cálculo sequencial, a exclusão humana, a persistência temporária, as rotas de apuração e as exportações em PDF e XLSX. No navegador, os botões permaneceram bloqueados enquanto a requisição estava aberta, confirmando que a tela impede duplicidade de apuração. A consulta real deve finalizar antes de se validar o volume de eventos retornado pelo Meeventos para o período selecionado.
