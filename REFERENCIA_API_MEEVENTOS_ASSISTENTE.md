# Referência de segurança — Assistente de Relatórios

Em 22/08/2026, foi consultada a documentação oficial do Meeventos: <https://docs.meeventos.com.br/>.

A documentação descreve recursos para clientes, orçamentos, financeiro, eventos, produtos e serviços, itens e insumos, pedidos e participantes. Para a assistente local, a integração permanecerá limitada a **consultas de leitura** desses recursos; ela não acionará rotas de criação, edição ou exclusão e não exibirá o token de autenticação.

Fonte: [Visão Geral — Meeventos API](https://docs.meeventos.com.br/).

## Central Financeira — consulta somente leitura

Fonte específica: [Financeiro — Meeventos API](https://docs.meeventos.com.br/endpoints/financeiro).

Para a central local, é permitido exclusivamente `GET /api/v1/financial`, com paginação (`page`, `limit`) e ordenação pelos campos documentados, como `datapagamento`, `datacompetencia`, `valor` e `pago`. A interface poderá exibir os campos devolvidos pelo Meeventos: tipo de cobrança, recebedor/pagador, descrição, valor, juros, multa, desconto, status de pagamento, conta, categoria, centro de custo, modo de pagamento, evento relacionado e parcelas.

Nenhuma rota de criação ou edição financeira será chamada pela plataforma local. O token continuará somente no backend e o resultado será apresentado como consulta, com data/hora de atualização e filtros de período.

## Conciliação bancária assistida — desenho seguro

Os campos retornados em `GET /api/v1/financial` são suficientes para comparar receitas pendentes com um extrato bancário importado. A sugestão local deve combinar, em ordem de relevância, valor líquido, data de pagamento ou competência, nome do pagador/recebedor, descrição, evento relacionado e parcela. O resultado precisa informar a confiança da sugestão e os elementos que levaram à correspondência.

O primeiro estágio da conciliação será estritamente local: importar um extrato em formato estruturado, como OFX ou CSV do banco, listar sugeridos, confirmados, divergentes e sem correspondência, e registrar a decisão em trilha de auditoria local. Nenhuma baixa será enviada ao Meeventos sem uma ação deliberada por lançamento, uma revisão visível dos campos e autorização explícita para habilitar essa etapa.
