# Atualização local — formulário, cronograma e formatos

Esta atualização reorganiza a área **Dados do Evento**, adiciona horários de montagem, início, final e desmontagem, mantém a opção **Evento sem data definida** e transforma **Formato do Evento** em uma seleção abastecida pelos tipos cadastrados no Meeventos. A chave do Meeventos continua somente no computador, como variável de ambiente; ela não acompanha este pacote.

| Item preservado | O que fazer |
|---|---|
| `propostas.json` | **Não apagar nem substituir.** Ele guarda o histórico e as versões já criadas. |
| Pasta `pdfs` | **Não apagar nem substituir.** Ela guarda os PDFs comerciais existentes. |
| `MEEVENTOS_TOKEN` e `ANTHROPIC_API_KEY` | **Não editar.** As chaves permanecem configuradas no Windows, fora do código. |

## Passo a passo no Windows

Primeiro, baixe o arquivo ZIP desta entrega e extraia-o, por exemplo, em `C:\Users\Anyaht\Downloads\SLK_Ajustes_Evento`. Depois, abra o **PowerShell** e execute os comandos abaixo um por um. Se a sua pasta estiver em outro local, altere somente o trecho `C:\Users\Anyaht\Painel-SLK-Propostas-v2.1-main`.

```powershell
$pastaSistema = "C:\Users\Anyaht\Painel-SLK-Propostas-v2.1-main"
$pastaAtualizacao = "C:\Users\Anyaht\Downloads\SLK_Ajustes_Evento"

Copy-Item "$pastaSistema\app.py" "$pastaSistema\app_backup_antes_ajuste_evento.py"
Copy-Item "$pastaSistema\templates\index.html" "$pastaSistema\templates\index_backup_antes_ajuste_evento.html"

Copy-Item "$pastaAtualizacao\app.py" "$pastaSistema\app.py" -Force
Copy-Item "$pastaAtualizacao\templates\index.html" "$pastaSistema\templates\index.html" -Force

Set-Location $pastaSistema
py app.py
```

> Mantenha a janela do PowerShell aberta enquanto a equipe utiliza o painel. Quando aparecer `Running on http://127.0.0.1:5000`, abra esse endereço no navegador.

## Conferência recomendada

No formulário, confira se a frase do briefing aparece como um cabeçalho azul, se **Local** e **Quantidade de Pessoas** estão na mesma linha e se as datas de montagem, evento e desmontagem têm os horários nos locais previstos. Em **Formato do Evento**, aguarde alguns segundos e confirme que aparecem os formatos cadastrados no Meeventos, como Corporativo, Congresso e Workshop.

Faça uma proposta de teste marcada como **Evento sem data definida**. Ela deve ser salva apenas localmente, com PDF e histórico, sem criar um orçamento comercial no Meeventos. Depois, se desejar, clique em **Meus Orçamentos**, abra a edição da proposta e confirme que os dados de data, horário e formato retornam ao formulário.

## Em caso de retorno à versão anterior

Pare a aplicação com `Ctrl + C` no PowerShell. Em seguida, execute os dois comandos abaixo e inicie novamente com `py app.py`.

```powershell
Copy-Item "$pastaSistema\app_backup_antes_ajuste_evento.py" "$pastaSistema\app.py" -Force
Copy-Item "$pastaSistema\templates\index_backup_antes_ajuste_evento.html" "$pastaSistema\templates\index.html" -Force
```

## Referência técnica

O seletor é carregado pelo backend da aplicação, que consulta o recurso **Tipos de Evento** do Meeventos. O navegador recebe apenas a lista de opções, nunca a credencial de integração. [1]

## Referências

[1] [Meeventos — Tipos de Evento](https://docs.meeventos.com.br/endpoints/tipodeevento)
