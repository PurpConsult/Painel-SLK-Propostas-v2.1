import assert from 'node:assert/strict';
import fs from 'node:fs';
import { JSDOM } from 'jsdom';

const html = fs.readFileSync('templates/index.html', 'utf8');
const dom = new JSDOM(html, {
  url: 'http://teste.local/',
  runScripts: 'outside-only',
  pretendToBeVisual: true,
});

const { window } = dom;
const { document } = window;
let payloadEnviado = null;

window.alert = () => {};
window.open = () => null;
window.fetch = async (url, options = {}) => {
  if (String(url).endsWith('/gerar-proposta')) {
    payloadEnviado = JSON.parse(options.body);
    return {
      ok: true,
      json: async () => ({
        sucesso: true,
        enviado_meeventos: false,
        numero_proposta: 'TESTE-DOM-01',
        url_pdf: '',
      }),
    };
  }
  if (String(url).endsWith('/tipos-evento')) {
    return { ok: true, json: async () => ({ dados: [{ id: '4', nome: 'Auditório' }, { id: '5', nome: 'Corporativo' }] }) };
  }
  return { ok: true, json: async () => ({ dados: [] }) };
};

window.localStorage.setItem('dados_editar', JSON.stringify({
  evento: { nome_evento: 'Evento DOM', local_evento: 'Local DOM', qtd_pessoas: 25, formato_evento: 'Auditório', id_formato_evento: '4', evento_sem_data: false, nome_vendedor: 'Jairo DOM', id_vendedor: '51' },
  cliente: { nome: 'Cliente DOM', cnpj: '29.649.702/0001-82', email: 'dom@example.com', telefone: '21999999999', contato: 'Contato DOM' },
  itens: [
    { id: '901', nome: 'PROJETOR DOM', valor: 100, valor_padrao: 100, valor_manual: '', quantidade: 2, tipo_item: 'Equipamento', externo: false, fornecedor_externo: '', custo_externo: 0 },
    { id: '902', nome: 'TÉCNICO DOM', valor: 480, valor_padrao: 480, valor_manual: '', quantidade: 1, tipo_item: 'Serviço', externo: false, fornecedor_externo: '', custo_externo: 0 },
  ],
}));

const script = [...document.querySelectorAll('script')].at(-1)?.textContent;
assert.ok(script, 'O script principal do formulário precisa estar presente.');
window.eval(script);

const esperar = () => new Promise(resolve => window.setTimeout(resolve, 0));
await esperar();
await esperar();

const preencher = (id, value) => {
  const campo = document.getElementById(id);
  campo.value = value;
  campo.dispatchEvent(new window.Event('input', { bubbles: true }));
  campo.dispatchEvent(new window.Event('change', { bubbles: true }));
};

preencher('busca_vendedor', 'Jairo DOM');
preencher('nome_evento', 'Evento DOM');
preencher('busca_local', 'Local DOM');
preencher('data_evento_inicio', '2026-09-24');
preencher('data_evento_final', '2026-09-25');
preencher('qtd_pessoas', '25');
preencher('data_montagem', '2026-09-23');
preencher('horario_montagem', '09:00');
preencher('horario_montagem_final', '12:00');
preencher('data_desmontagem', '2026-09-25');
preencher('horario_desmontagem', '18:00');
preencher('horario_desmontagem_final', '20:00');
preencher('formato_evento', '4');
preencher('busca_cliente', 'Cliente DOM');
preencher('cliente_cnpj', '29.649.702/0001-82');
preencher('cliente_email', 'dom@example.com');
preencher('cliente_telefone', '21999999999');
preencher('cliente_contato', 'Contato DOM');
preencher('desconto_proposta', '30');
preencher('observacoes_gerais', 'Teste DOM isolado.');

const semData = document.getElementById('evento_sem_data');
semData.checked = false;
semData.dispatchEvent(new window.Event('change', { bubbles: true }));

const campoManual = document.querySelector('[data-comercial-campo="valor_manual"][data-idx="0"]');
assert.ok(campoManual, 'O cartão deve renderizar o campo de valor manual.');
campoManual.value = '125';
campoManual.dispatchEvent(new window.Event('change', { bubbles: true }));

const locacaoExterna = document.querySelector('[data-externo-campo="externo"][data-idx="0"]');
assert.ok(locacaoExterna, 'O cartão deve renderizar a caixinha de locação externa.');
locacaoExterna.checked = true;
locacaoExterna.dispatchEvent(new window.Event('change', { bubbles: true }));

const form = document.getElementById('form');
form.dispatchEvent(new window.Event('submit', { bubbles: true, cancelable: true }));
await esperar();
await esperar();

assert.ok(payloadEnviado, 'O submit deve enviar o payload ao backend de teste.');
assert.equal(payloadEnviado.nome_evento, 'Evento DOM');
assert.equal(payloadEnviado.desconto_proposta, 30);
assert.equal(payloadEnviado.data_evento_inicio, '2026-09-24');
assert.equal(payloadEnviado.data_evento_final, '2026-09-25');
assert.equal(payloadEnviado.evento_sem_data, false);
assert.equal(payloadEnviado.horario_montagem_final, '12:00');
assert.equal(payloadEnviado.horario_desmontagem_final, '20:00');
assert.equal(payloadEnviado.formato_evento, 'Auditório');
assert.equal(payloadEnviado.id_formato_evento, '4');
assert.equal(payloadEnviado.itens.length, 2);
assert.equal(payloadEnviado.itens[0].valor_manual, '125');
assert.equal(payloadEnviado.itens[0].valor, 125);
assert.equal(payloadEnviado.itens[0].externo, true);
assert.equal(payloadEnviado.total_proposta, 700);
assert.match(document.getElementById('msg_resultado').textContent, /TESTE-DOM-01/);

console.log('OK: o DOM monta e envia o payload simplificado com desconto, valor manual e locação externa.');
