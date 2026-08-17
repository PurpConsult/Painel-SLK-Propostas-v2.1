import assert from 'node:assert/strict';
import fs from 'node:fs';
import { JSDOM } from 'jsdom';

const html = fs.readFileSync('templates/index.html', 'utf8');
const dom = new JSDOM(html, {
  url: 'http://teste-mobile.local/',
  runScripts: 'outside-only',
  pretendToBeVisual: true,
});

const { window } = dom;
const { document } = window;
Object.defineProperty(window, 'innerWidth', { value: 375, configurable: true });
window.matchMedia = query => ({
  matches: query.includes('max-width') && query.includes('768px'),
  media: query,
  addEventListener: () => {},
  removeEventListener: () => {},
});

let payloadEnviado = null;
window.alert = () => {};
window.open = () => null;
window.fetch = async (url, options = {}) => {
  if (String(url).endsWith('/gerar-proposta')) {
    payloadEnviado = JSON.parse(options.body);
    return { ok: true, json: async () => ({ sucesso: true, numero_proposta: 'MOBILE-01', url_pdf: '' }) };
  }
  return { ok: true, json: async () => ({ dados: [] }) };
};

window.localStorage.setItem('dados_editar', JSON.stringify({
  evento: { nome_evento: 'Evento Mobile', local_evento: 'Local Mobile', qtd_pessoas: 12, formato_evento: 'Auditório', evento_sem_data: true, nome_vendedor: 'Jairo Mobile', id_vendedor: '62' },
  cliente: { nome: 'Cliente Mobile', cnpj: '', email: '', telefone: '', contato: '' },
  itens: [
    { id: '801', nome: 'PROJETOR MOBILE', valor: 100, valor_padrao: 100, valor_manual: '', quantidade: 2, tipo_item: 'Equipamento', externo: false, fornecedor_externo: '', custo_externo: 0 },
    { id: '802', nome: 'TÉCNICO MOBILE', valor: 480, valor_padrao: 480, valor_manual: '', quantidade: 1, tipo_item: 'Serviço', externo: false, fornecedor_externo: '', custo_externo: 0 },
  ],
}));

const script = [...document.querySelectorAll('script')].at(-1)?.textContent;
assert.ok(script, 'O script do formulário precisa estar presente.');
window.eval(script);

const esperar = () => new Promise(resolve => window.setTimeout(resolve, 0));
await esperar();
await esperar();

assert.equal(window.innerWidth, 375, 'O cenário deve executar em largura de celular.');
assert.equal(window.matchMedia('(max-width:768px)').matches, true, 'A regra de tela estreita precisa estar ativa no cenário.');
assert.ok(document.querySelector('.coluna-esquerda') && document.querySelector('.coluna-direita'), 'As duas colunas devem continuar disponíveis para empilhamento móvel.');
assert.ok(document.querySelector('.coluna-esquerda').compareDocumentPosition(document.querySelector('.coluna-direita')) & window.Node.DOCUMENT_POSITION_FOLLOWING, 'A coluna de briefing e dados deve vir antes da seleção em tela estreita.');

const preencher = (id, value) => {
  const campo = document.getElementById(id);
  campo.value = value;
  campo.dispatchEvent(new window.Event('input', { bubbles: true }));
  campo.dispatchEvent(new window.Event('change', { bubbles: true }));
};

preencher('busca_vendedor', 'Jairo Mobile');
preencher('nome_evento', 'Evento Mobile');
preencher('busca_local', 'Local Mobile');
preencher('qtd_pessoas', '12');
preencher('formato_evento', 'Auditório');
preencher('busca_cliente', 'Cliente Mobile');
preencher('desconto_proposta', '30');
preencher('observacoes_gerais', 'Cenário mobile de validação.');

const campoManual = document.querySelector('[data-comercial-campo="valor_manual"][data-idx="0"]');
campoManual.value = '125';
campoManual.dispatchEvent(new window.Event('change', { bubbles: true }));

const locacao = document.querySelector('[data-externo-campo="externo"][data-idx="0"]');
locacao.checked = true;
locacao.dispatchEvent(new window.Event('change', { bubbles: true }));

document.getElementById('evento_sem_data').checked = true;
document.getElementById('form').dispatchEvent(new window.Event('submit', { bubbles: true, cancelable: true }));
await esperar();
await esperar();

assert.ok(payloadEnviado, 'O envio da proposta deve funcionar no cenário de tela estreita.');
assert.equal(payloadEnviado.itens.length, 2);
assert.equal(payloadEnviado.itens[0].valor, 125);
assert.equal(payloadEnviado.itens[0].valor_manual, '125');
assert.equal(payloadEnviado.itens[0].externo, true);
assert.equal(payloadEnviado.desconto_proposta, 30);
assert.equal(payloadEnviado.total_proposta, 700);

console.log('OK: a tela estreita preserva ordem, seleção, valor manual, locação externa e envio.');
