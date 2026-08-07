# SLK Propostas Pro

Sistema de geração de propostas comerciais integrado ao **ME Eventos**.

## Funcionalidades

- 375 produtos/serviços carregados direto da API Meeventos
- 747+ clientes com busca e autocomplete
- 10 vendedores e 121 locais de evento
- Geração de PDF profissional com logo SouLink
- Envio automático ao Meeventos (cria orçamento e retorna ID)
- Número do orçamento do Meeventos usado no PDF e controle interno
- Página "Meus Itens" com todos os produtos/serviços e suas categorias
- Distinção entre Equipamentos e Serviços

## Instalação

```bash
pip install -r requirements.txt
python app.py
```

Acesse: http://localhost:5000

## Arquivos

| Arquivo | Descrição |
|---------|-----------|
| `app.py` | Backend Flask com proxy para API Meeventos |
| `templates/index.html` | Frontend principal - formulário de propostas |
| `templates/meus_itens.html` | Página de visualização de todos os itens |
| `soulink_logo.png` | Logo SouLink para o PDF |
| `logo_vendai.png` | Logo VendAI para o rodapé |
| `requirements.txt` | Dependências Python |

## API Meeventos

O sistema se conecta à API do Meeventos usando o token configurado em `app.py`.

Endpoints utilizados:
- GET `/products-services` - Catálogo completo (375 itens)
- GET `/customers` - Clientes (747+)
- GET `/users` - Vendedores
- GET `/locations` - Locais de evento
- POST `/budgets` - Criar orçamento

## Desenvolvido por

**VendAI** - Inteligência Artificial para Vendas
