# Referência técnica — Área de Relatórios

Esta funcionalidade usa exclusivamente consultas de leitura ao Meeventos. A listagem de eventos utiliza `GET /api/v1/events`, com os parâmetros `start`, `end`, `page` e `limit`; os eventos elegíveis são filtrados localmente por status **Eventos Anteriores** e pelo local configurado para cada hotel. A consulta de itens utiliza `GET /api/v1/orders?idevento={id}`, que retorna, entre outros, os campos `id`, `nome`, `valor` e `tipo`.

| Critério local | Campo de origem | Aplicação |
|---|---|---|
| Evento realizado | `status` | Considerar apenas `Eventos Anteriores`. |
| Hotel | `localevento` | Filtrar pelos termos configurados para cada hotel. |
| Equipamento elegível | `tipo = 7` | Compor a base de comissão. |
| Desconto geral | Lançamento negativo de `tipo = 5` | Ratear pela participação dos equipamentos no valor bruto dos itens. |
| Terceirização/sublocação | Não disponível de forma confiável | Excluir somente após confirmação humana da equipe. |

> A documentação oficial indica que as consultas de eventos e pedidos suportam paginação, filtros e parâmetros de período. Nenhuma rota de criação, edição ou exclusão é utilizada pela área de relatórios.

## Fontes

[1] [Meeventos API — Eventos](https://docs.meeventos.com.br/endpoints/eventos)

[2] [Meeventos API — Pedidos](https://docs.meeventos.com.br/endpoints/pedidos)
