# Referências técnicas — Anexos de projeto em nuvem

## Decisão aprovada

A Soulink aprovou o uso do **Cloudflare R2** para receber automaticamente PDFs de projeto anexados no formulário local. A equipe deve apenas selecionar o arquivo; o backend enviará o PDF para um bucket privado e utilizará um link temporário no PDF comercial.

## Modelo de segurança

O bucket permanecerá privado. O backend local usará credenciais S3 compatíveis do R2, fornecidas por variáveis de ambiente, para enviar o arquivo. O cliente receberá somente uma URL pré-assinada de leitura, válida por até sete dias, sem acesso às credenciais nem à listagem dos demais arquivos.

Os nomes dos arquivos deverão ser gerados pelo sistema com identificador aleatório, e o upload aceitará exclusivamente PDFs dentro do limite que será definido no formulário. As credenciais serão escopadas apenas ao bucket de anexos com a permissão **Object Read & Write**.

## Fontes oficiais consultadas

| Tema | Registro confirmado | Fonte |
|---|---|---|
| URLs pré-assinadas | Concedem acesso temporário a uma operação e objeto específico; validade de 1 segundo a 7 dias; devem ser tratadas como credenciais temporárias. | [Cloudflare R2 — Presigned URLs](https://developers.cloudflare.com/r2/api/s3/presigned-urls/) |
| Preços e faixa gratuita | Standard inclui 10 GB/mês, 1 milhão de operações de escrita e 10 milhões de leituras mensais; tráfego de saída sem cobrança. | [Cloudflare R2 — Pricing](https://developers.cloudflare.com/r2/pricing/) |
| Configuração inicial | É necessário conta Cloudflare com assinatura R2, acesso a Storage & databases > R2, criação de bucket e uso de API S3 compatível. | [Cloudflare R2 — Get started](https://developers.cloudflare.com/r2/get-started/) |
| Credenciais | A criação de token R2 gera Access Key ID e Secret Access Key; a chave secreta é exibida apenas uma vez. A permissão pode ser limitada ao bucket escolhido. | [Cloudflare R2 — Authentication](https://developers.cloudflare.com/r2/api/tokens/) |
