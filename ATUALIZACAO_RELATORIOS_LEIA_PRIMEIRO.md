# Atualização local — Área de Relatórios Soulink

Este pacote acrescenta a página **Relatórios** ao ambiente local da Soulink. Ele não contém propostas, PDFs, credenciais ou qualquer dado da operação.

## O que foi incluído

A nova aba permite selecionar o Lagune Barra Hotel, informar um período, consultar eventos em modo somente leitura, revisar os equipamentos, confirmar exclusões de itens terceirizados ou sublocados e baixar o relatório em PDF ou a planilha de apoio.

Os cálculos seguem o padrão aprovado: somente equipamentos, desconto geral rateado, dedução de 5%, dedução de 12% sobre o saldo e comissão de 15% para o Lagune.

## Antes de atualizar

1. Feche a aplicação local, se ela estiver aberta.
2. Faça uma cópia da sua pasta atual para uma pasta de backup com a data do dia.
3. Não copie nem substitua `propostas.json`, a pasta `pdfs` ou qualquer arquivo `.env` existente.
4. Confira se a variável `MEEVENTOS_TOKEN` já está configurada no Windows, pois ela continua sendo necessária para a consulta de eventos.

## Aplicação com o pacote ZIP

1. Extraia o pacote em uma pasta temporária, como a pasta Downloads.
2. Copie os arquivos extraídos para dentro da pasta da aplicação Soulink, permitindo substituir apenas os arquivos de código e de `templates`.
3. Preserve os seus arquivos operacionais e credenciais conforme a seção anterior.
4. Inicie a aplicação normalmente e abra `http://127.0.0.1:5000/relatorios`.

## Teste recomendado

Use inicialmente um período de poucos dias. Clique em **Gerar apuração**, confira os equipamentos listados, marque somente o que for confirmado como terceirizado ou sublocado e use **Recalcular com exclusões confirmadas** antes de baixar o PDF ou a planilha.

> A integração de relatórios somente consulta o Meeventos. Ela não cria, edita ou exclui eventos, pedidos ou propostas no sistema externo.

## Se aparecer uma mensagem de falha da API Meeventos

Reinicie a aplicação e verifique a conexão. Se a mensagem informar que a credencial foi recusada, confira a variável `MEEVENTOS_TOKEN` no Windows e reinicie novamente. Nunca cole o token dentro do arquivo `app.py`.
