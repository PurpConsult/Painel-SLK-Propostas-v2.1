# Project TODO - SLK Propostas Pro

## Ajustes identificados em teste de produção — 15/08/2026
- [x] Diagnosticar e corrigir o retorno 503 da API Claude no ambiente local, sem registrar ou expor a chave.
- [x] Manter a prévia revisável sem pré-preenchimento automático, conforme validação da equipe.
- [ ] Implementar opcionalmente o pré-preenchimento do rascunho com sugestões removíveis, se a equipe decidir alterar o fluxo atual no futuro.
- [x] Preencher automaticamente no rascunho os dados estruturados de cliente e evento extraídos do briefing.
- [x] Mostrar somente candidatos de equipamento de alta relevância e resumir itens não localizados na prévia.
- [x] Separar equipamentos e serviços na prévia compacta, exibindo apenas equipamentos na seção prioritária.
- [x] Cobrir em teste que serviços não sejam apresentados como equipamentos prioritários.
- [x] Executar teste comportamental do JavaScript que separa equipamentos prioritários de serviços identificados.
- [x] Permitir que a equipe confirme múltiplos itens válidos do catálogo para um pedido e reaproveitar essas alternativas em prévias futuras.
- [x] Implementar a interface de ensinar associação, com busca no catálogo e remoção das alternativas salvas pela equipe.
- [x] Publicar no GitHub o código do aprendizado supervisionado, sem propostas, PDFs, credenciais ou memória local da equipe.
- [x] Enviar a atualização somente ao repositório existente PurpConsult/Painel-SLK-Propostas-v2.1, sem criar repositório adicional.
- [x] Publicar no repositório existente a prévia compacta validada pela equipe.
- [x] Reorganizar a seleção em blocos visuais distintos de equipamentos e serviços, reduzindo a lista extensa.
- [x] Mover o resumo dos itens escolhidos para antes da prévia assistida.
- [x] Permitir alternar a categoria de um item pela etiqueta e persistir a correção para as próximas propostas.
- [x] Validar em teste a organização visual e a persistência da migração entre equipamentos e serviços.
- [x] Compactar cada item selecionado para exibir somente dados e ações essenciais na visão inicial.
- [x] Manter o valor manual visível e recolher somente a locação externa em ajustes opcionais por item.
- [x] Reorganizar o conteúdo interno de cada cartão para evitar sobreposição entre identidade, quantidade, valor e total.
- [x] Transformar a locação externa em uma caixinha expansível compacta, exibindo os campos adicionais apenas quando aberta.
- [x] Validar visualmente os cartões com nomes longos, quantidade, valor manual e total, corrigindo qualquer sobreposição em tela.
- [x] Verificar no navegador as dimensões renderizadas dos cartões com nome longo, quantidade, valor manual e total, sem colisões entre seus blocos internos.
- [x] Manter a caixa de locação externa aberta ao ativar o item e exibir fornecedor e custo imediatamente.
- [x] Cobrir em teste o fluxo de abrir locação externa, ativá-la e preservar a exibição de seus campos adicionais.
- [x] Remover da tela principal a prévia repetitiva do orçamento, preservando os dados enviados no formulário e no PDF.
- [x] Exibir equipamentos e serviços em uma sequência vertical, com equipamentos acima de serviços.
- [x] Reduzir a locação externa a uma única caixinha compacta por item, sem campos comerciais expostos na seleção.
- [x] Validar seleção de itens, cálculos e criação de proposta após simplificar a tela.
- [x] Executar e registrar um teste ponta a ponta da tela simplificada com seleção, desconto, resposta de geração, PDF e histórico.
- [x] Adicionar um teste de integração do envio simplificado, cobrindo itens, desconto e marcação de locação externa no payload final.
- [x] Executar uma validação real no navegador com itens selecionados, desconto e locação externa, confirmando envio, PDF e histórico em dados isolados de teste.
- [x] Substituir a verificação estrutural por um teste DOM real que preencha os campos, altere valor manual e locação externa, dispare o envio e valide o payload em um backend de teste.
- [x] Executar e registrar a regressão DOM real cobrindo montagem do payload, desconto, valor manual e locação externa.
- [x] Garantir que o total visual e o payload usem o valor manual informado no item, sem manter o valor base no cálculo.
- [x] Restaurar uma composição de duas colunas para impedir que o formulário fique excessivamente longo.
- [x] Organizar a coluna esquerda com briefing por IA, anexo de briefing, dados do evento e dados do cliente.
- [x] Organizar a coluna direita com seleção de itens, equipamentos, serviços, observações gerais e opções comerciais do PDF.
- [x] Atualizar os textos do briefing para "Deixa comigo: Cole aqui o briefing do cliente!" e "Ou anexe o briefing aqui:".
- [x] Executar no navegador com viewport móvel real a tela de orçamento em ambiente isolado, registrando a ordem empilhada dos blocos e ausência de sobreposição visual.
- [x] Realizar um teste interativo real em viewport estreito com seleção, valor manual, locação externa e envio de proposta em ambiente isolado.
- [x] Registrar evidência verificável da validação móvel real antes de concluir a atualização da tela estreita.
- [x] Reduzir o campo de valor manual e posicioná-lo ao lado da identificação do item para tornar o cartão mais limpo.
- [x] Fazer a caixinha Locação externa abrir os campos de fornecedor e valor de custo quando for marcada.
- [x] Separar as datas do evento em Data do Evento | Início e Data do Evento | Final, preservando a opção de evento sem data definida.
- [x] Remover o título "Prévia por IA", manter o brilho e apresentar em seguida "Conte comigo: Cole aqui o briefing do cliente!".
- [x] Mover a explicação sobre conferência humana para um rodapé abaixo da caixa de texto do briefing.
- [x] Exibir diretamente validade, desconto, idioma, link e foto, removendo o recolhimento das opções comerciais e anexos.
- [x] Posicionar o desconto antes do fechamento financeiro da seleção de itens.
- [x] Exibir Valor total da proposta após os subtotais, descontando automaticamente o valor informado.
- [x] Atualizar a regressão DOM para usar Data do Evento | Início e Data do Evento | Final em vez do campo de data único removido.
- [x] Validar a persistência, os cálculos e a geração do PDF com os novos campos e cartões.
- [x] Executar e registrar uma inspeção estrutural que comprove o texto de conferência humana abaixo da caixa de briefing, como rodapé.
- [x] Executar e registrar uma validação de PDF após os ajustes consolidados, confirmando datas de início/final e valor total com desconto.
- [x] Identificar e remover a pré-visualização que ocupa metade da tela do formulário.
- [x] Reorganizar os blocos restantes para que o formulário volte a usar a largura disponível de forma prática.
- [x] Validar a seleção de itens e a geração de proposta após a remoção da pré-visualização.
- [x] Ocultar candidatos de catálogo com baixa aderência ou sem termos técnicos em comum com o pedido do briefing.
- [x] Aceitar blocos de conteúdo e estruturas alternativas retornadas pelo modelo Claude na prévia, mantendo a confirmação humana obrigatória.
- [x] Aceitar de forma segura respostas Claude em JSON puro ou entre blocos de código, sem aplicar sugestões automaticamente.
- [x] Validar e normalizar a estrutura da análise Claude antes de exibir sugestões do catálogo.
- [x] Corrigir a prévia para subtrair o desconto do investimento total.
- [x] Abrir a imagem do item em nova guia, sem substituir a página de orçamento.
- [x] Reservar área segura na segunda página do PDF para impedir texto sobre a logo do papel timbrado.
- [x] Permitir reemitir uma versão já existente do orçamento em Português, Inglês ou Espanhol sem criar nova versão nem alterar dados.
- [x] Corrigir a configuração local da prévia assistida por IA e documentar a variável de ambiente necessária.

## Fase 1: Configuração do Backend com Proxy Seguro para Meeventos
- [x] Configurar o proxy server-side para todas as chamadas à API do Meeventos.
- [x] Garantir que o token de autenticação da API do Meeventos seja mantido exclusivamente no backend.
- [x] Criar endpoints no backend para buscar `clients` do Meeventos.
- [x] Criar endpoints no backend para buscar `eventlocation` do Meeventos.
- [x] Criar endpoints no backend para buscar `seller` do Meeventos.
- [x] Criar endpoint no backend para enviar `budgets` para o Meeventos.
- [x] Criar endpoint no backend para buscar `products-services` do Meeventos (ou carregar `produtos.txt`).

## Fase 2: Implementação do Frontend com Formulário Estruturado e Busca em Tempo Real
- [x] Criar a estrutura básica do formulário no frontend.
- [x] Implementar campo "Nome do Cliente" com busca e autocomplete consumindo o endpoint `/clients` do backend.
- [x] Implementar campo "Local do Evento" com busca e autocomplete consumindo o endpoint `/eventlocation` do backend.
- [x] Implementar campo "Vendedor" com busca e autocomplete consumindo o endpoint `/seller` do backend.
- [x] Implementar campos "Nome do Evento", "Data" e "Quantidade de Pessoas".

## Fase 3: Tabela de Itens com Cálculos Automáticos e Gerenciamento de Fornecedores Externos
- [x] Implementar busca em tempo real no catálogo de produtos (via backend) com adição de itens à proposta por clique.
- [x] Criar tabela de itens da proposta no frontend.
- [x] Adicionar funcionalidade de ajuste de quantidade por item na tabela.
- [x] Adicionar funcionalidade de remoção de itens da tabela.
- [x] Implementar cálculo automático de subtotal e total no frontend.
- [x] Adicionar checkbox "Locação Externa?" por item.
- [x] Adicionar campos "Nome do fornecedor" e "Valor de custo" para itens externos.
- [x] Exibir a margem de lucro calculada em tempo real para itens externos.

## Fase 4: Geração de PDF Profissional com Download
- [x] Implementar a lógica de geração de PDF no backend (ou no frontend, se for mais viável com bibliotecas JS).
- [x] Incluir logo da SLK no PDF.
- [x] Incluir dados do cliente, evento e vendedor no PDF.
- [x] Incluir tabela de itens no PDF.
- [x] Incluir total no PDF.
- [x] Incluir condições gerais no PDF.
- [x] Disponibilizar o PDF para download direto no navegador.

## Fase 5: Integração Completa, Testes e Entrega
- [x] Integrar o formulário com o envio do orçamento ao Meeventos via API POST `/budgets` (backend).
- [x] Realizar validação integrada simulada de autocomplete, itens, prévia e envio do orçamento, sem criar dados no Meeventos.
- [x] Executar validação integrada real do endpoint de geração, comprovando persistência, PDF e retorno de `url_pdf`.
- [x] Documentar a validação do envio real ao Meeventos ou a razão para mantê-la protegida contra criação de dados de teste.
- [x] Garantir que a prévia em tempo real da proposta funcione corretamente.

## Fase 6: Documentação e Instruções de Uso
- [x] Criar documentação para o usuário final sobre como usar a aplicação.

## Ajustes de Layout do PDF — Solicitação de Thayná
- [x] Centralizar "ORÇAMENTO Nº [número]" em uma única linha no cabeçalho.
- [x] Posicionar a data de geração centralizada logo abaixo do número do orçamento.
- [x] Manter os subtotais de equipamentos e serviços em linhas únicas logo abaixo de cada tabela.
- [x] Manter o investimento total em uma única linha, com alinhamento comercial e sem quebra indevida.

## Correção de Propostas Salvas e Edição
- [x] Normalizar cliente, evento, vendedor e itens antes de salvar cada proposta.
- [x] Salvar todos os campos necessários para reabrir uma proposta no formulário sem perdas.
- [x] Preservar o número original ao editar e criar uma nova versão no histórico.
- [x] Testar criação, listagem e reabertura de proposta com todos os dados preenchidos.
- [x] Validar a listagem agrupada pelo número original e a indicação da última versão.
- [x] Validar a preparação dos dados completos para reabrir a proposta no formulário.
- [x] Executar teste ponta a ponta da ação Editar, confirmando todos os campos e itens preenchidos no formulário.
- [x] Executar teste real no navegador contra a aplicação Flask, confirmando a ação Editar com dados persistidos.

## Entrega Consolidada para Instalação Local
- [x] Montar pacote com backend, páginas e instruções de atualização segura.
- [x] Validar a estrutura do pacote antes da entrega.
- [x] Entregar o pacote e o procedimento de instalação e teste.
- [x] Reconstruir o pacote local com os módulos de imagens aprovadas, status, briefing seguro e PDFs multilíngues.

## Ajustes de Identidade Visual e Conteúdo Comercial
- [x] Alterar o título e o cabeçalho principal para "SOULINK | Orçamentos".
- [x] Aplicar o mesmo degradê azul do formulário na página "Minhas Propostas".
- [x] Exibir no formulário o número da proposta em edição, com texto contextual no cabeçalho.
- [x] Exibir no PDF a validade calculada em 48 horas a partir da geração.
- [x] Atualizar os dados bancários e as condições gerais conforme o texto aprovado.
- [x] Inserir no PDF a assinatura com o nome do vendedor responsável.
- [x] Aplicar a marca SOULINK no título e no cabeçalho visível da página "Meus Itens".
- [x] Restaurar o título padrão do formulário após salvar uma edição com sucesso.
- [x] Gerar e revisar a nova prévia visual do PDF.
- [x] Preparar um novo pacote consolidado de instalação local.

## Ajuste de Logo para PDF — Solicitação de Thayná
- [x] Criar uma versão limpa da logo Soulink, com fundo branco, para uso no cabeçalho do PDF.
- [x] Substituir a logo no gerador de PDF e validar a nova prévia comercial.
- [x] Atualizar o pacote de instalação local com a nova logo.
- [x] Confirmar o salvamento recuperável do projeto após otimizar a logo branca.

## Revisão de Logo — Bloco Azul Lateral
- [x] Preparar e entregar a logo Soulink com o bloco azul lateral preservado e fundo branco.
- [x] Aplicar a logo com bloco azul lateral ao cabeçalho do PDF.
- [x] Validar o PDF e reconstruir o pacote de instalação com a logo aprovada.
- [x] Publicar as alterações consolidadas no repositório GitHub da Soulink.
- [x] Publicar no GitHub os ajustes consolidados de cartões, briefing, datas de evento, opções comerciais e fechamento financeiro.
- [x] Reforçar a exclusão de propostas, PDFs, chaves e arquivos de memória operacional antes da publicação no GitHub.

## Logo Padrão da Soulink
- [x] Substituir o arquivo padrão soulink_logo.png pela versão aprovada com bloco azul lateral.

## Apresentação Comercial Soulink
- [x] Criar uma apresentação comercial sobre a plataforma de propostas e a estratégia de integração com o Meeventos.

## Acesso Diário Simplificado
- [ ] Definir a alternativa de acesso diário mais simples para a equipe, sem execução manual de arquivo BAT.

## Ajustes Visuais Pendentes — Formulário de Proposta
- [x] Aplicar à frase "Conte comigo: Cole aqui o briefing do cliente!" a mesma identidade visual do cabeçalho Dados do Evento.
- [x] Reorganizar Dados do Evento com Local ao lado de Quantidade de pessoas.
- [x] Inserir Data de Montagem com horários de e até abaixo de Local.
- [x] Organizar Data de início do evento e Data final do evento com seus respectivos horários.
- [x] Inserir a caixinha solicitada abaixo das datas do evento.
- [x] Inserir Data de Desmontagem com horários de e até abaixo da caixinha.
- [x] Substituir o campo livre Formato do evento por uma seleção carregada de Tipos de Evento cadastrados no Meeventos, sem expor o token.
- [x] Preservar datas e horários de montagem, evento e desmontagem no payload, histórico e PDF.
- [x] Validar o layout e a preservação dos dados comerciais após os ajustes visuais.

## Correções de Conferência de Proposta e Briefing
- [x] Substituir a prévia fixa por um botão Visualizar proposta que abre um PDF temporário em nova aba, sem salvar histórico ou enviar ao Meeventos.
- [x] Garantir que a criação definitiva permaneça em uma ação separada, após a conferência do PDF.
- [x] Retornar JSON legível quando a leitura de um anexo de briefing falhar inesperadamente, evitando o erro Failed to fetch.
- [x] Validar por teste automatizado o PDF provisório, a ausência de persistência e o retorno seguro da leitura de anexo.

## Versão Online da Plataforma Soulink
- [ ] Manter a publicação, a importação do histórico e o uso diário da versão online em pausa até a aprovação final explícita da versão local.
- [ ] Definir o acesso da equipe e a preservação do histórico atual para a versão online.
- [ ] Estruturar uma versão online segura com integração Meeventos protegida no servidor.
- [ ] Migrar proposta, PDF, histórico e edição versionada para a versão online.
- [ ] Validar a aplicação online e preparar o link de uso diário da equipe.
- [x] Criar o modelo de dados online para propostas, versões, itens, status, aprovações de imagem e arquivos em armazenamento seguro.
- [x] Implementar procedimentos protegidos para catálogo Meeventos e gestão versionada de propostas no servidor online.
- [x] Construir a interface Soulink online de Proposta, Orçamentos, Itens e Financeiro usando o novo backend.
- [ ] Importar o histórico local somente por ação controlada, preservando os números e versões existentes.
- [x] Adicionar testes automatizados dos procedimentos online de criação, versão, status, financeiro e revisão de imagens.
- [ ] Validar a interface online contra os procedimentos reais, cobrindo carregamento, vazio, erro e ações comerciais.
- [ ] Concluir a criação e edição versionada pela interface online, não apenas a consulta e a alteração de status.
- [ ] Executar e registrar validação ponta a ponta: criar proposta, editar nova versão, alterar status e revisar imagem, confirmando a persistência no banco.
- [ ] Adicionar teste de integração ou interface para criação, edição versionada, estados de carregamento/vazio/erro e ações comerciais reais.

## Relatório de Comissão — Lagune Hotel
- [x] Receber a fonte dos eventos realizados no Lagune Hotel entre 01/01/2026 e 17/08/2026.
- [x] Consolidar apenas os equipamentos por evento, excluindo serviços, montagem, desmontagem, mobiliário, técnicos e afins.
- [x] Calcular base líquida após dedução de 5% e 12% e aplicar comissão de 15%.
- [x] Entregar relatório com memória de cálculo, total comissionável e total de comissão a pagar.

## Evolução Comercial da Plataforma — Solicitações Pós-Apresentação
- [x] Incluir datas de montagem, desmontagem, evento, horários, formato e opção de evento sem data definida.
- [x] Permitir validade editável por calendário, com padrão de sete dias.
- [x] Permitir preço unitário manual por item, desconto destacado e opções de exibição de valores no PDF.
- [x] Permitir observações gerais, foto da proposta e link clicável de projeto.
- [x] Validar que o link de projeto é incorporado como hyperlink clicável no PDF comercial.
- [x] Permitir imagens de itens e serviços no PDF, com versão comercial que permita ampliação pelo cliente.
- [x] Atualizar identidade visual do PDF com papel timbrado e tons de azul da marca Soulink.
- [x] Criar botão de pré-reserva, status da proposta e página financeira de versões aprovadas.
- [x] Registrar status por versão, preservando uma versão aprovada como cópia fechada para o financeiro.
- [x] Exibir badges de status e ações de pré-reserva, aprovação e perda em Meus Orçamentos.
- [x] Criar uma página Financeiro somente leitura com PDFs das versões aprovadas.
- [x] Criar prévia assistida por IA a partir de briefing livre e de arquivo enviado.
- [x] Garantir que a IA apenas sugira dados e itens, sem sobrescrever campos ou alterar a proposta sem confirmação humana.
- [x] Limitar a leitura de briefing a arquivos TXT, PDF e DOCX, com validação de extensão, tamanho e conteúdo.
- [x] Usar exclusivamente o catálogo Meeventos para os itens sugeridos e seus valores, sem preços inventados pela IA.
- [x] Adicionar teste automatizado de extração de texto em arquivo DOCX.
- [x] Adicionar teste automatizado de rejeição para arquivo acima de 5 MB.
- [x] Criar versões do PDF em inglês e espanhol.
- [x] Preservar os nomes e IDs originais do catálogo internamente, traduzindo somente a cópia comercial do PDF.
- [x] Permitir selecionar Português, Inglês ou Espanhol ao gerar a cópia comercial do PDF.
- [x] Traduzir cabeçalhos, condições comerciais e nomes técnicos dos itens na cópia em inglês e espanhol.
- [x] Validar que o histórico e a integração Meeventos conservam os dados originais em português e os mesmos IDs.
- [x] Mapear traduções por ID para 100% dos itens do catálogo em inglês e espanhol, sem depender apenas de substituições heurísticas por trecho de texto.
- [x] Adicionar teste automatizado que verifica cobertura de tradução dos nomes de todos os itens do catálogo para inglês e espanhol.
- [x] Usar o papel timbrado Soulink enviado como base do novo PDF comercial.
- [x] Consultar imagens disponíveis no catálogo Meeventos antes de criar um cadastro manual complementar de fotos.
- [x] Pesquisar online imagens correspondentes aos descritivos do catálogo, com revisão antes da associação ao item.
- [x] Pesquisar online imagens correspondentes aos descritivos do catálogo, com revisão antes da associação ao item.
- [x] Permitir aprovação ou rejeição humana das imagens candidatas na página Meus Itens.
- [x] Usar somente imagens aprovadas na cópia comercial do PDF, com miniatura e link clicável para ampliação.

## Correção do Relatório de Comissão — Lagune Hotel
- [x] Aplicar primeiro a dedução de 5% e, sobre o saldo, a dedução de 12% por evento.
- [x] Recalcular a comissão de 15% sobre a base final após as duas deduções sequenciais.
- [x] Identificar os indicadores disponíveis de terceirização e manter todos os equipamentos até confirmação humana de exclusão.
- [x] Listar os eventos do Lagune Hotel com itens de palco para confirmação humana de terceirização.
- [x] Ratear o desconto geral de cada proposta entre todos os itens e reduzir proporcionalmente a base de equipamentos.
- [x] Atualizar, validar e reenviar a planilha, o demonstrativo e o pacote de comissão corrigidos.

## PDF Comercial — Comissão Lagune Hotel
- [x] Consolidar a memória de cálculo revisada e a comissão mensal para apresentação ao hotel.
- [x] Gerar gráfico mensal da comissão com valores precisos e identidade visual Soulink.
- [x] Produzir, validar e entregar o relatório em PDF com comunicação visual comercial da Soulink.

## Revisão de Apresentação — PDF Lagune Hotel
- [x] Substituir as equações tributárias por explicações objetivas das porcentagens aplicadas.
- [x] Inserir tabela geral com totais dos eventos, equipamentos após desconto, impostos, valor comissionável e comissão a pagar.
- [x] Aplicar a comunicação visual do arquivo de referência após o reenvio bem-sucedido do anexo.
- [x] Recompilar, validar e reenviar o PDF comercial revisado.

## Logo Oficial da Soulink — PDF Lagune Hotel
- [x] Extrair a logo oficial da Soulink contida no PDF de referência enviado.
- [x] Substituir a marca do relatório pela logo oficial sem alterar dados ou cálculos.
- [x] Recompilar, validar e entregar a versão atualizada do PDF.

## Assinatura VendAI — PDF Lagune Hotel
- [x] Localizar e validar a logo oficial da VendAI.
- [x] Adicionar “Desenvolvido por VendAI - AI & Sales Consulting” e a logo ao encerramento comercial do relatório.
- [x] Recompilar, validar e reenviar o PDF atualizado.

## Refinamento da Marca VendAI — PDF Lagune Hotel
- [x] Remover o fundo branco da logo VendAI para uso sobre o fundo escuro do relatório.
- [x] Reduzir a logo e mantê-la opaca, sem efeito de marca-d’água, no encerramento.
- [x] Recompilar, validar e entregar o PDF refinado.

## Assinatura Textual VendAI — PDF Lagune Hotel
- [x] Remover a logo VendAI do encerramento do relatório.
- [x] Manter somente a frase “Desenvolvido por VendAI - AI & Sales Consulting”.
- [x] Recompilar, validar e entregar a versão simplificada do PDF.

## Área de Relatórios — Lagune Hotel
- [x] Criar uma aba Relatórios no ambiente Soulink com geração por período.
- [x] Registrar as regras do Lagune: equipamentos elegíveis, desconto geral rateado, deduções sequenciais de 5% e 12% e comissão de 15%.
- [x] Manter exclusão de terceirizados e sublocados sob confirmação humana.
- [x] Gerar exportações revisáveis em PDF e planilha para apresentação ao hotel.
- [x] Preparar a estrutura para configuração futura de outros hotéis e suas próprias regras de comissão.

## Métricas Padrão — Todos os Relatórios
- [x] Aplicar somente equipamentos como base de qualquer relatório de comissão.
- [x] Ratear descontos gerais da proposta proporcionalmente aos equipamentos.
- [x] Aplicar dedução de 5% e, em seguida, de 12% sobre o saldo antes da comissão.
- [x] Permitir que cada hotel configure apenas os parâmetros comerciais próprios, como percentual de comissão e exceções aprovadas.

## Cadastro Manual de Novo Cliente
- [x] Confirmar os campos obrigatórios e o formato aceito pelo endpoint de clientes do Meeventos.
- [x] Adicionar ao backend uma criação segura de cliente com validação e prevenção de duplicidade.
- [x] Incluir no formulário a ação Novo Cliente e os campos manuais necessários.
- [x] Preencher e selecionar automaticamente o cliente recém-criado após confirmação do Meeventos.
- [x] Validar em testes os cenários de sucesso, campos inválidos, duplicidade e falha externa.
- [x] Preparar atualização local sem incluir propostas, PDFs, credenciais ou backups.

## Publicação solicitada — Novo Cliente
- [x] Publicar o commit validado de Novo Cliente no repositório oficial PurpConsult/Painel-SLK-Propostas-v2.1.

## Formato de Montagem, Imagem Padrão e Prévia de Proposta
- [x] Substituir o tipo de evento incorreto por um campo livre de observação de montagem, como Auditório, Coquetel, Escolar e ATC.
- [x] Preservar a observação de montagem no histórico e no PDF da proposta.
- [x] Aplicar a imagem enviada como referência padrão quando nenhuma imagem específica for adicionada à proposta.
- [x] Criar uma prévia visual compacta da proposta, atualizada durante o preenchimento sem duplicar o formulário.
- [x] Validar a prévia, os dados persistidos e o PDF gerado com formato e imagem padrão.
- [x] Preparar atualização local segura sem propostas, PDFs, credenciais ou backups.

## Visualização Antes do Envio e Briefing por PDF
- [x] Remover a prévia fixa do formulário para evitar repetição de informações.
- [x] Criar a ação Visualizar proposta, abrindo o PDF provisório em uma nova aba sem enviar dados ao Meeventos.
- [x] Manter Criar proposta como ação final, que gera e envia a proposta confirmada ao Meeventos.
- [x] Diagnosticar e corrigir o erro Failed to fetch ao anexar um briefing em PDF à prévia por IA.
- [ ] Validar visualização em nova aba e leitura de briefing PDF antes de preparar a atualização local.
- [x] Preparar atualização local segura sem propostas, PDFs, credenciais ou backups.
- [ ] Confirmar a aplicação dos arquivos atualizados e o reinício correto da aplicação no computador local após o erro persistente de briefing.

## Anexo Automático de Projeto
- [x] Definir o uso de armazenamento em nuvem próprio, com envio automático após a equipe anexar o PDF no formulário.
- [x] Selecionar Cloudflare R2 como provedor de armazenamento, com links protegidos e temporários para os PDFs de projeto.
- [x] Avaliar o campo de anexo integrado à proposta e o controle de acesso, tamanho e prazo de disponibilidade dos PDFs.
- [x] Configurar o provedor de nuvem e as credenciais de upload exclusivamente no backend local.
- [x] Integrar o upload automático, a geração de link controlado e o PDF comercial ao fluxo de proposta.
- [x] Validar o acesso externo ao anexo e preparar a atualização local sem expor credenciais.
- [x] Corrigir a variável R2_ACCOUNT_ID no computador local com o identificador de conta correto, sem alterar nem expor as chaves de acesso.

## Ajustes Comerciais e Inteligência de Catálogo
- [x] Publicar no GitHub o estado validado do upload automático de PDF antes das novas alterações.
- [x] Remover o campo manual Link do Projeto / Referência, mantendo somente o upload automático de PDF na nuvem.
- [x] Aplicar imposto de 5% sobre o total de equipamentos e exibir o valor separadamente.
- [x] Aplicar aos serviços o imposto de 5% sobre a base e, sobre o valor desse primeiro imposto, uma segunda incidência de 12%; somar ambos ao total de serviços, sem tratar o cálculo como uma alíquota única de 17%.
- [x] Reorganizar o fechamento comercial em subtotal geral, desconto e investimento total, preservando os totais de equipamentos e serviços.
- [x] Aprimorar a interpretação do briefing e a busca no catálogo para aumentar a aderência das sugestões de itens.
- [x] Cobrir em testes os cálculos sequenciais, o novo fechamento comercial e a correspondência ampliada de itens.
- [x] Preparar pacote local e roteiro de validação dos ajustes comerciais, sem arquivos operacionais ou credenciais.
- [ ] Validar localmente a leitura dos impostos, o fechamento comercial e as sugestões de catálogo antes de publicar esta atualização no GitHub.

## Simplificação Visual dos Impostos
- [x] Remover da tela e do PDF as fórmulas e memórias de cálculo exibidas ao lado dos totais de equipamentos e serviços.
- [x] Exibir somente rótulos comerciais objetivos para total de equipamentos, total de serviços, subtotal geral, desconto e investimento total.
- [x] Preservar os cálculos de impostos confirmados apenas no backend e validar que os valores finais não foram alterados.
- [x] Preparar uma atualização local simples após a validação visual e de cálculo.
- [ ] Validar no computador local a leitura comercial simplificada antes de publicar este refinamento no GitHub.

## Rótulos Resumidos de Impostos
- [x] Exibir em Total equipamentos apenas a indicação “(+ 5% de impostos)”, sem valores intermediários ou fórmulas.
- [x] Exibir em Total serviços apenas a indicação “(+ 5% + 12% de impostos)”, sem valores intermediários ou fórmulas.
- [x] Aplicar os mesmos rótulos resumidos no PDF comercial, preservando os valores já validados.
- [x] Preparar o pacote local auditado sem alterar as credenciais ou os dados operacionais.
- [ ] Validar no computador local os rótulos resumidos no formulário e no PDF antes de publicar este refinamento no GitHub.

## Explicitação Comercial dos Impostos no PDF
- [x] Informar no fechamento do PDF que os impostos aplicáveis já estão incluídos nos totais de equipamentos e serviços.
- [x] Preservar os percentuais e os valores finais aprovados, sem apresentar fórmulas ou valores intermediários.
- [x] Validar o texto comercial e a composição visual do PDF antes de preparar a atualização local.

## Catálogo Ampliado e Imagens Comerciais
- [x] Incluir na seleção de equipamentos os itens, insumos e kits disponíveis no Meeventos, mantendo a origem e os dados de cada registro.
- [x] Fazer a foto de referência da proposta abrir em uma nova aba quando clicada no PDF.
- [ ] Definir e validar o modelo de planilha para associação em lote de fotos de itens, sem etapa individual de validação quando a associação vier da equipe.
- [ ] Importar somente associações explícitas fornecidas pela equipe, preservando itens sem foto quando não houver correspondência confiável.
- [ ] Validar catálogo ampliado, links de imagem no PDF e importação de fotos antes de preparar a atualização local.
- [ ] Aguardar a planilha de fotos da equipe antes de iniciar a importação em lote.

## Correção da Busca de Kits
- [ ] Inspecionar o retorno e os recursos de catálogo do Meeventos para identificar a origem real dos kits que não apareceram na busca.
- [ ] Corrigir a consulta ou a normalização dos kits sem remover itens, insumos, aprendizado ou correção de categoria existentes.
- [ ] Validar a pesquisa por um kit real informado pela equipe antes de preparar a correção local.
- [ ] Consultar explicitamente a visão de Kits indicada pela equipe no Meeventos, separada da listagem padrão de Itens e Insumos.

## Catálogo Local de Kits por Capturas
- [ ] Registrar, a partir das capturas fornecidas pela equipe, o nome comercial, os itens associados, quantidades e identificadores disponíveis de cada kit.
- [x] Criar um catálogo local separado de kits, sem sobrescrever dados oficiais de Itens e Insumos ou Produtos e Serviços do Meeventos.
- [x] Permitir a busca e a seleção de cada kit como equipamento, preservando a composição associada no histórico da proposta.
- [ ] Validar cada kit somente depois de receber as capturas de sua listagem e de seus componentes.
- [x] Cadastrar e aprovar um único kit piloto antes de inserir os demais kits do catálogo local.
- [x] Cadastrar como piloto o “KIT A/V - LAGHETTO - FERNANDO PESSOA I E II” com os oito componentes e quantidades exibidos pela equipe.
- [x] Exibir o prefixo comercial “KIT” antes do nome de todos os registros do catálogo local de kits.

## Edição Local da Composição de Kits
- [x] Exibir os componentes e quantidades quando um kit for selecionado na proposta.
- [x] Permitir excluir um componente somente da composição daquela proposta, sem alterar o catálogo-base do kit.
- [x] Permitir alterar a quantidade de um componente somente na proposta atual e recalcular o valor do kit.
- [x] Preservar a composição editada em cálculos, PDF, prévia e histórico da proposta.
- [ ] Na integração aplicável com o Meeventos, desmembrar o kit e enviar somente os componentes finais, com IDs oficiais e quantidades editadas.
- [x] Validar o fluxo de expansão e edição usando o kit piloto antes de disponibilizar a atualização local.

## Compactação dos Cards de Itens
- [x] Posicionar o controle de quantidade ao lado do nome de cada equipamento ou serviço.
- [x] Posicionar o campo de valor manual ao lado da descrição do item, evitando uma linha exclusiva para esse dado.
- [x] Reduzir a altura dos cards sem alterar remoção, locação externa, troca de categoria, cálculo ou valor manual.
- [x] Validar o layout compacto em equipamentos e serviços antes de preparar a atualização local.

## Publicação da Edição de Kits
- [x] Publicar no repositório oficial o código, os testes e o registro de tarefas da composição editável de kits, sem dados operacionais ou credenciais.
