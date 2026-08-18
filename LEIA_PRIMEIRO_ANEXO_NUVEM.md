# Atualização Soulink — Anexo Automático de Projeto na Nuvem

Este pacote acrescenta o campo **PDF do Projeto / Referência** ao formulário da proposta. A equipe apenas seleciona o arquivo PDF: ao clicar em **Criar proposta**, o sistema o envia automaticamente para o bucket privado `soulink-projetos` no Cloudflare R2 e inclui um link clicável no PDF comercial.

> A ação **Visualizar proposta** continua sem enviar arquivos, sem salvar histórico e sem integrar com o Meeventos. O envio do anexo acontece apenas na criação definitiva.

## Proteção e disponibilidade

Os arquivos não são públicos. O sistema gera um link seguro temporário, válido por **7 dias**, alinhado ao prazo padrão de validade da proposta. Quando uma cópia da proposta for reemitida, o sistema gera um novo link para o mesmo PDF de projeto. O envio aceita somente PDFs de até **20 MB**.

Nenhuma chave do Cloudflare está dentro deste pacote. As credenciais devem ficar apenas nas variáveis de ambiente do Windows, conforme o procedimento abaixo.

## Arquivos atualizados

| Arquivo | Finalidade |
|---|---|
| `app.py` | Envio seguro ao R2, geração de link temporário e preservação no histórico. |
| `templates/index.html` | Campo para anexar o PDF no formulário. |
| `requirements.txt` | Inclui a biblioteca compatível com R2. |
| `static/imagem_referencia_padrao.jpeg` | Mantém a imagem padrão aprovada para as propostas. |

## Aplicação local

1. Baixe o ZIP e feche a aplicação Soulink, se ela estiver aberta.
2. Abra o **PowerShell** pelo menu Iniciar.
3. Cole o bloco abaixo inteiro. Ele cria um backup completo, atualiza somente os arquivos necessários e instala a dependência nova.

```powershell
$pastaSistema = "$env:USERPROFILE\Painel-SLK-Propostas-v2.1-main"
$arquivoZip = "$env:USERPROFILE\Downloads\SLK_ANEXO_AUTOMATICO_NUVEM_2026-08-18.zip"
$pastaExtracao = "$env:USERPROFILE\Downloads\SLK_TEMP_ANEXO_NUVEM"
$dataBackup = Get-Date -Format "yyyy-MM-dd_HH-mm"
$pastaBackup = "$env:USERPROFILE\Backup_Soulink_$dataBackup"

if (!(Test-Path $pastaSistema)) { Write-Host "Pasta não encontrada: $pastaSistema" -ForegroundColor Red; exit }
if (!(Test-Path $arquivoZip)) { Write-Host "ZIP não encontrado: $arquivoZip" -ForegroundColor Red; exit }

Copy-Item $pastaSistema $pastaBackup -Recurse
if (Test-Path $pastaExtracao) { Remove-Item $pastaExtracao -Recurse -Force }
Expand-Archive -Path $arquivoZip -DestinationPath $pastaExtracao -Force
$pastaAtualizacao = Get-ChildItem $pastaExtracao -Directory | Select-Object -First 1
if ($null -eq $pastaAtualizacao) { throw "Não encontrei os arquivos dentro do ZIP." }

Copy-Item "$($pastaAtualizacao.FullName)\app.py" "$pastaSistema\app.py" -Force
Copy-Item "$($pastaAtualizacao.FullName)\requirements.txt" "$pastaSistema\requirements.txt" -Force
Copy-Item "$($pastaAtualizacao.FullName)\templates\index.html" "$pastaSistema\templates\index.html" -Force
Copy-Item "$($pastaAtualizacao.FullName)\static\imagem_referencia_padrao.jpeg" "$pastaSistema\static\imagem_referencia_padrao.jpeg" -Force

Set-Location $pastaSistema
py -m pip install -r requirements.txt
Write-Host "Atualização instalada. Agora configure as chaves R2 no próximo bloco." -ForegroundColor Green
```

## Configuração das chaves R2 no Windows

Ainda no PowerShell, cole o bloco abaixo. Quando o PowerShell perguntar, cole os três dados que você anotou no Cloudflare: **Account ID**, **Access Key ID** e **Secret Access Key**. A chave secreta não será exibida enquanto for digitada.

```powershell
$r2AccountId = Read-Host "Cole o R2 Account ID"
$r2AccessKey = Read-Host "Cole o R2 Access Key ID"
$r2SecretSeguro = Read-Host "Cole o R2 Secret Access Key" -AsSecureString
$ponteiro = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($r2SecretSeguro)

try {
    $r2Secret = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($ponteiro)
    [Environment]::SetEnvironmentVariable("R2_ACCOUNT_ID", $r2AccountId, "User")
    [Environment]::SetEnvironmentVariable("R2_ACCESS_KEY_ID", $r2AccessKey, "User")
    [Environment]::SetEnvironmentVariable("R2_SECRET_ACCESS_KEY", $r2Secret, "User")
    [Environment]::SetEnvironmentVariable("R2_BUCKET_NAME", "soulink-projetos", "User")
    [Environment]::SetEnvironmentVariable("R2_LINK_TTL_SECONDS", "604800", "User")

    $env:R2_ACCOUNT_ID = $r2AccountId
    $env:R2_ACCESS_KEY_ID = $r2AccessKey
    $env:R2_SECRET_ACCESS_KEY = $r2Secret
    $env:R2_BUCKET_NAME = "soulink-projetos"
    $env:R2_LINK_TTL_SECONDS = "604800"
    Write-Host "Credenciais protegidas neste computador." -ForegroundColor Green
}
finally {
    if ($ponteiro -ne [IntPtr]::Zero) { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ponteiro) }
    Remove-Variable r2Secret -ErrorAction SilentlyContinue
}
```

## Início e teste

No mesmo PowerShell, execute:

```powershell
Set-Location "$env:USERPROFILE\Painel-SLK-Propostas-v2.1-main"
py app.py
```

Abra `http://127.0.0.1:5000` e faça um teste com uma proposta que tenha pelo menos um item:

1. Na área comercial, selecione um PDF no campo **PDF do Projeto / Referência**.
2. Clique em **Visualizar proposta** para confirmar que a prévia continua sem enviar o arquivo.
3. Clique em **Criar proposta**.
4. Abra o PDF gerado e clique no link do projeto. Ele deve abrir o PDF selecionado em uma nova aba.

Se houver uma mensagem de erro, mantenha o PowerShell aberto e registre a mensagem exibida após o clique em **Criar proposta**. Não envie chaves, tokens ou capturas que mostrem informações sensíveis.
