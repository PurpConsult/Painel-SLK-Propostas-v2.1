# Validação do Fluxo de Novo Cliente

## Revisão visual inicial

Em 17/08/2026, a página local `http://127.0.0.1:5000/` foi revisada após abrir o botão **Novo cliente**. O painel ficou inserido diretamente no bloco **Dados do Cliente**, sem deslocar as colunas principais do formulário. A experiência apresenta seleção entre pessoa jurídica e pessoa física, campos de documento, identificação, contatos e uma seção recolhível de endereço e observações.

O painel informa explicitamente que o registro só é criado após a ação manual **Cadastrar no Meeventos**, e que há conferência de duplicidade antes da criação. A busca existente de clientes permanece disponível logo abaixo do painel.

## Interações simuladas no navegador

O retorno de sucesso do endpoint local foi simulado sem nenhuma escrita externa. A tela enviou os dados ao endpoint local `/api/clientes/novo`, selecionou o cliente retornado, copiou seu identificador para o formulário e exibiu a confirmação de vínculo com a proposta.

Também foi simulado um retorno de duplicidade. Nesse cenário, a interface permaneceu aberta, não criou cadastro e apresentou uma ação explícita para a equipe escolher o cliente existente. Por fim, foi validado que abrir o painel remove temporariamente o identificador de um cliente previamente selecionado; ao cancelar, os dados anteriores são restaurados integralmente.
