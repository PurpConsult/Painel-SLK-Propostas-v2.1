import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';

const pagina = fs.readFileSync('templates/index.html', 'utf8');
const inicio = pagina.indexOf('function renderizarLocacaoExterna');
const fim = pagina.indexOf('function atualizarResumoLocacaoExterna');

assert.ok(inicio >= 0 && fim > inicio, 'A função de renderização da locação externa deve existir.');

const contexto = {
  escaparHtml: valor => String(valor ?? '').replace(/[&<>"']/g, caractere => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  })[caractere]),
};

vm.runInNewContext(`${pagina.slice(inicio, fim)}; this.renderizarLocacaoExterna = renderizarLocacaoExterna;`, contexto);

const itemInterno = { externo: false };
const caixinhaDesmarcada = contexto.renderizarLocacaoExterna(itemInterno, 3);
assert.ok(caixinhaDesmarcada.includes('class="locacao-caixinha"'), 'A locação externa deve usar uma caixinha compacta.');
assert.ok(caixinhaDesmarcada.includes('Locação externa'), 'A caixinha deve ter a identificação clara de locação externa.');
assert.ok(caixinhaDesmarcada.includes('data-externo-campo="externo"'), 'A caixinha deve manter o campo de locação externa por item.');
assert.ok(!caixinhaDesmarcada.includes('Fornecedor') && !caixinhaDesmarcada.includes('Custo unitário'), 'Fornecedor e custo devem permanecer ocultos até a ativação da locação externa.');

const itemExterno = { externo: true };
const caixinhaMarcada = contexto.renderizarLocacaoExterna(itemExterno, 4);
assert.ok(caixinhaMarcada.includes('checked'), 'A caixinha deve manter a marcação quando o item for locação externa.');
assert.ok(/<details[^>]*\bopen\b/.test(caixinhaMarcada), 'Ao ativar a locação externa, a caixinha deve abrir os campos complementares.');
assert.ok(caixinhaMarcada.includes('Fornecedor') && caixinhaMarcada.includes('Valor do custo'), 'A ativação deve revelar fornecedor e custo da locação externa.');
assert.ok(caixinhaMarcada.includes('data-externo-campo="fornecedor_externo"') && caixinhaMarcada.includes('data-externo-campo="custo_externo"'), 'Fornecedor e custo devem atualizar o item selecionado.');

console.log('OK: a locação externa abre fornecedor e custo depois de ser marcada.');
