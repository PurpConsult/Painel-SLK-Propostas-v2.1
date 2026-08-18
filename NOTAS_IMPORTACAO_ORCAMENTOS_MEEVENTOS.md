# Importação de Orçamentos Meeventos — Mapeamento Técnico

## Decisão de produto

A página **Meus Orçamentos** poderá exibir uma segunda origem de dados, identificada visualmente como **Meeventos**. Essa consulta será somente de leitura: os registros externos não serão gravados em `propostas.json`, não gerarão versões Soulink e não poderão ser editados, aprovados, perdidos ou pré-reservados pelo painel.

Essa separação evita a duplicidade entre uma proposta criada no ambiente Soulink e a referência correspondente criada no ERP. Caso o mesmo identificador oficial seja encontrado no histórico local, o painel deve manter a proposta local como registro principal e sinalizar o vínculo, em vez de criar um segundo card externo.

## API confirmada

A documentação oficial do Meeventos informa os seguintes recursos de consulta de orçamentos:

| Operação | Método e rota | Uso previsto no painel |
|---|---|---|
| Listar | `GET /api/v1/budgets` | Trazer uma lista paginada de orçamentos externos. |
| Visualizar | `GET /api/v1/budgets/{id}` | Consultar detalhes de um orçamento externo quando necessário. |
| Busca remota | `search`, `start`, `end`, `page`, `limit`, `field_sort`, `sort` | Filtrar a importação sem carregar registros desnecessários. |

A listagem pode retornar, entre outros, `id`, `nome`, `nomedoevento`, `localevento`, `dataevento`, `vendedor`, `status`, `valorinicial`, `idevento` e dados de follow-up. A documentação informa limite de até 200 registros por página. [1]

>A API documenta criação de orçamento e cadastro de follow-up, mas não lista edição nem exclusão de orçamentos. Portanto, a importação proposta não tentará alterar registros externos. [1]

Em 18/08/2026, foi realizada uma verificação técnica somente de leitura com `GET /budgets?page=1&limit=1` usando a credencial já configurada no ambiente. O endpoint respondeu `HTTP 200` e confirmou a estrutura paginada `data` e `pagination`; nenhum conteúdo de orçamento ou credencial foi registrado nesta validação.

## Regras de apresentação planejadas

1. A busca da página consultará primeiro os cards já carregados e poderá encaminhar o termo ao parâmetro remoto `search` quando a origem Meeventos estiver habilitada.
2. O card externo exibirá apenas os dados disponíveis na API e terá uma etiqueta de origem. Ele não mostrará ações que dependem do histórico Soulink, como editar uma versão ou reemitir um PDF comercial.
3. Quando `numero_oficial` de uma proposta local corresponder ao `id` remoto, o card externo será ocultado para evitar repetição.
4. Falhas de autenticação, indisponibilidade ou limite da API deverão manter o histórico local acessível e mostrar uma mensagem clara, sem expor token, URL interna ou resposta bruta do ERP.

## Visão operacional em calendário

A documentação também disponibiliza consulta somente de leitura de eventos por `GET /api/v1/events` e `GET /api/v1/events/{id}`. A lista aceita busca, paginação, ordenação e intervalo de datas. Os campos úteis para o calendário incluem `dataevento`, `horaevento`, `datasAdicionais`, `nomeevento`, `nomeCliente`, `localevento`, `convidados`, `idorcamento` e `status`. [2]

O calendário operacional deverá compor, em uma mesma visualização, quatro situações sem alterar o ERP: cotações e pré-reservas do histórico Soulink, propostas aprovadas e eventos confirmados trazidos do Meeventos. A Ordem de Serviço será uma saída documental local, gerada apenas por ação humana a partir de uma proposta aprovada ou de um evento confirmado; a primeira entrega não fará inclusão, alteração ou exclusão de eventos no Meeventos.

## Referência

[1] [Meeventos API — Orçamentos](https://docs.meeventos.com.br/endpoints/orcamentos)
[2] [Meeventos API — Eventos](https://docs.meeventos.com.br/endpoints/eventos)
