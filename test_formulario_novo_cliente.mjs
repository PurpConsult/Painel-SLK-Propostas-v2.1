import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

const html = readFileSync(new URL("./templates/index.html", import.meta.url), "utf8");

assert.match(html, /id="btn_novo_cliente"/, "O formulário deve exibir a ação Novo cliente.");
assert.match(html, /id="painel_novo_cliente"/, "O painel manual de cliente deve existir.");
assert.match(html, /id="novo_cliente_tipo"/, "O painel deve permitir escolher pessoa física ou jurídica.");
assert.match(html, /id="novo_cliente_documento"/, "O painel deve receber CPF ou CNPJ.");
assert.match(html, /id="btn_salvar_novo_cliente"/, "A criação deve depender de uma ação explícita.");
assert.match(html, /fetch\(`\$\{API_BASE_URL\}\/clientes\/novo`/, "O cadastro deve usar exclusivamente o endpoint local seguro.");
assert.match(html, /mostrarClientesExistentes\(json\.dados\)/, "Duplicidades devem oferecer seleção do cadastro existente.");
assert.match(html, /id="id_cliente"/, "O identificador do cliente deve ser mantido no formulário.");
assert.match(html, /cliente_id: document\.getElementById\("id_cliente"\)\.value/, "A proposta deve carregar o identificador do cliente selecionado.");
assert.match(html, /document\.getElementById\("id_cliente"\)\.value = dados\.id \|\| ""/, "A seleção da lista deve guardar o identificador do cliente.");
assert.match(html, /function limparClienteSelecionadoNoFormulario\(\)/, "Iniciar um cadastro novo deve limpar a seleção anterior.");
assert.match(html, /limparClienteSelecionadoNoFormulario\(\);/, "O painel Novo Cliente deve remover o ID anterior antes do cadastro.");
assert.match(html, /fecharNovoCliente\(true, true\)/, "Cancelar deve restaurar o cliente previamente selecionado.");

console.log("OK: painel Novo Cliente, confirmação manual, duplicidade e ID do cliente validados no formulário.");
