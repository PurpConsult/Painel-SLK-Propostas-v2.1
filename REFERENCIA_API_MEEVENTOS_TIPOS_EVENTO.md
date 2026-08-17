# Referência da API Meeventos — Tipos de Evento

- **Fonte:** https://docs.meeventos.com.br/
- **Consulta em:** 17/08/2026

A documentação oficial lista **Tipos de Eventos** entre os recursos adicionais da API. A consulta somente leitura ao ambiente da Soulink confirmou que a rota operacional é `GET /eventtype?page=1&limit=200`, retornando objetos com os campos `id` e `nome`, como `{"id":"5","nome":"Corporativo"}`. A integração deve usar o token apenas no backend e aproveitar o recurso para preencher o campo **Formato do evento** com as opções cadastradas no Meeventos.

> A página geral também orienta que cada chamada autenticada use o cabeçalho `Authorization` com o token de acesso. O token não deve ser exibido, enviado ao navegador ou incluído em arquivos versionados.
