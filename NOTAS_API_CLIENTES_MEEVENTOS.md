# Integração de Novo Cliente — Meeventos

Fonte consultada em 17/08/2026: [documentação oficial de Clientes](https://docs.meeventos.com.br/endpoints/clientes).

## Contrato utilizado

O cadastro é feito por `POST /api/v1/clients`. A documentação informa que o corpo deve ser um **array**, mesmo quando houver somente um cliente. A resposta de sucesso retorna `status`, `message` e uma lista `data` com o novo `id` e o nome do cliente.

O único campo obrigatório é `nome`. Para a operação comercial da Soulink, a tela solicitará também o tipo de cadastro, documento, e-mail, telefone/celular e contato responsável, quando disponíveis. Pessoas jurídicas serão enviadas com `tipocadastro: 1`, razão social, nome fantasia e `cnpjpj`; pessoas físicas usarão `tipocadastro: 0`, nome e `cpf`.

## Proteção contra duplicidade

Antes de criar um registro, o backend deve consultar `/api/v1/clients` com `search` e `type=3` quando houver CPF/CNPJ e com `type=1` quando houver e-mail. A documentação também permite busca padrão por nome, razão social ou nome fantasia. O fluxo local nunca deve criar o cliente quando a pesquisa encontrar um documento ou e-mail correspondente; em vez disso, deve devolver o cadastro existente para a equipe selecionar.

## Segurança

O token continua exclusivo no backend, na variável de ambiente `MEEVENTOS_TOKEN`. O navegador só envia os campos permitidos do formulário para a rota local, que valida, consulta duplicidade e então encaminha o cadastro ao Meeventos.
