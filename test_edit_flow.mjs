import assert from "node:assert/strict";
import fs from "node:fs";
import vm from "node:vm";

const root = new URL(".", import.meta.url).pathname;
const propostaCompleta = {
  numero: "TESTE-1720",
  versao: 2,
  cliente: {
    razao_social: "Nexxus Engenharia",
    documento: "12.345.678/0001-90",
    email: "contato@nexxus.com.br",
    telefone: "(21) 99999-9999",
    contato: "Raquel Santos",
  },
  evento: {
    nome_evento: "Reunião Nexxus",
    data_evento: "2026-09-24",
    data_evento_inicio: "2026-09-24",
    horario_inicio_evento: "14:00",
    data_evento_final: "2026-09-24",
    horario_fim_evento: "18:00",
    data_montagem: "2026-09-24",
    horario_montagem: "09:00",
    horario_montagem_final: "12:00",
    data_desmontagem: "2026-09-24",
    horario_desmontagem: "18:00",
    horario_desmontagem_final: "20:00",
    formato_evento: "Auditório",
    id_formato_evento: "4",
    local_evento: "Laghetto Stilo Barra",
    qtd_pessoas: "300",
    nome_vendedor: "Jairo",
    id_vendedor: "62",
  },
  itens: [
    { id: 2, nome: "TÉCNICO AUDIOVISUAL", valor: 480, quantidade: 1, tipo_item: "Serviço" },
    { id: 45, nome: "PROJETOR 5000 LUMENS", valor: 1050, quantidade: 2, tipo_item: "Equipamento" },
    { id: 77, nome: "CADEIRA", valor: 30, quantidade: 20, tipo_item: "Equipamento" },
  ],
};

function extrairScript(arquivo) {
  const conteudo = fs.readFileSync(arquivo, "utf8");
  const scripts = [...conteudo.matchAll(/<script>([\s\S]*?)<\/script>/g)];
  return scripts.at(-1)?.[1] || "";
}

function criarContexto(armazenamento, fetchFn) {
  const elementos = new Map();
  const novoElemento = () => ({
    value: "", innerText: "", innerHTML: "", textContent: "", disabled: false, files: [],
    style: {}, dataset: {}, className: "", children: [],
    listeners: {},
    addEventListener(tipo, manipulador) { this.listeners[tipo] = manipulador; },
    appendChild(filho) { this.children.push(filho); },
    closest() { return null; },
    classList: { contains() { return false; }, add() {}, remove() {}, toggle() {} },
  });
  const document = {
    getElementById(id) {
      if (!elementos.has(id)) elementos.set(id, novoElemento());
      return elementos.get(id);
    },
    addEventListener() {},
    querySelectorAll() { return []; },
    createElement() { return novoElemento(); },
  };
  const localStorage = {
    getItem: chave => armazenamento.has(chave) ? armazenamento.get(chave) : null,
    setItem: (chave, valor) => armazenamento.set(chave, String(valor)),
    removeItem: chave => armazenamento.delete(chave),
  };
  const window = { location: { href: "" }, open() {} };
  const contexto = { console, document, localStorage, fetch: fetchFn, window, alert() {}, setTimeout, clearTimeout, Promise, Number, String, parseFloat, JSON, encodeURIComponent };
  contexto.globalThis = contexto;
  return { contexto: vm.createContext(contexto), elementos, window, document };
}

const aguardarMicrotarefas = () => new Promise(resolve => setTimeout(resolve, 0));

async function main() {
  const armazenamento = new Map();
  const propostasScript = extrairScript(`${root}templates/propostas.html`);
  const lista = criarContexto(armazenamento, async () => ({ ok: true, json: async () => ({ sucesso: true, dados: propostaCompleta }) }));
  vm.runInContext(propostasScript, lista.contexto);
  vm.runInContext("irEditar('TESTE-1720', 2)", lista.contexto);
  await aguardarMicrotarefas();
  await aguardarMicrotarefas();

  assert.equal(lista.window.location.href, "/");
  assert.equal(armazenamento.get("editar_numero"), "TESTE-1720");
  assert.equal(armazenamento.get("editar_versao"), "2");

  const indexScript = extrairScript(`${root}templates/index.html`);
  const formulario = criarContexto(armazenamento, async url => {
    if (String(url).includes("/gerar-proposta")) {
      return {
        ok: true,
        json: async () => ({ sucesso: true, enviado_meeventos: false, numero_proposta: "TESTE-1720", url_pdf: null }),
      };
    }
    if (String(url).includes("/tipos-evento")) {
      return { ok: true, json: async () => ({ sucesso: true, dados: [{ id: "4", nome: "Auditório" }] }) };
    }
    return { ok: true, json: async () => ({ dados: [] }) };
  });
  vm.runInContext(indexScript, formulario.contexto);
  await aguardarMicrotarefas();
  await aguardarMicrotarefas();

  const el = formulario.elementos;
  assert.equal(el.get("busca_vendedor").value, "Jairo");
  assert.equal(el.get("id_vendedor").value, "62");
  assert.equal(el.get("nome_evento").value, "Reunião Nexxus");
  assert.equal(el.get("busca_local").value, "Laghetto Stilo Barra");
  assert.equal(el.get("data_evento_inicio").value, "2026-09-24");
  assert.equal(el.get("horario_inicio_evento").value, "14:00");
  assert.equal(el.get("data_evento_final").value, "2026-09-24");
  assert.equal(el.get("horario_fim_evento").value, "18:00");
  assert.equal(el.get("data_montagem").value, "2026-09-24");
  assert.equal(el.get("horario_montagem").value, "09:00");
  assert.equal(el.get("horario_montagem_final").value, "12:00");
  assert.equal(el.get("data_desmontagem").value, "2026-09-24");
  assert.equal(el.get("horario_desmontagem").value, "18:00");
  assert.equal(el.get("horario_desmontagem_final").value, "20:00");
  assert.equal(el.get("formato_evento").value, "4");
  assert.equal(el.get("qtd_pessoas").value, "300");
  assert.equal(el.get("busca_cliente").value, "Nexxus Engenharia");
  assert.equal(el.get("cliente_cnpj").value, "12.345.678/0001-90");
  assert.equal(el.get("cliente_email").value, "contato@nexxus.com.br");
  assert.equal(el.get("cliente_telefone").value, "(21) 99999-9999");
  assert.equal(el.get("cliente_contato").value, "Raquel Santos");
  const itensCarregados = JSON.parse(vm.runInContext("JSON.stringify(selecionados)", formulario.contexto));
  assert.equal(itensCarregados.length, propostaCompleta.itens.length);
  assert.deepEqual(
    itensCarregados.map(({ id, nome, valor, quantidade, tipo_item }) => ({ id, nome, valor, quantidade, tipo_item })),
    propostaCompleta.itens,
  );
  assert.equal(el.get("btnSubmit").textContent, "💾 Salvar nova versão da proposta");
  assert.equal(el.get("tituloPagina").textContent, "EDITAR: Proposta TESTE-1720");
  assert.equal(formulario.document.title, "EDITAR: Proposta TESTE-1720 | SOULINK");

  await el.get("form").listeners.submit({ preventDefault() {} });
  assert.equal(el.get("tituloPagina").textContent, "SOULINK | Orçamentos");
  assert.equal(formulario.document.title, "SOULINK | Orçamentos");
  assert.equal(armazenamento.get("editar_numero"), undefined);
  console.log("OK: ação Editar preenche o formulário, contextualiza o cabeçalho e restaura a marca após salvar.");
}

main().catch(erro => {
  console.error(erro);
  process.exitCode = 1;
});
