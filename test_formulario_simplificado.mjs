import assert from 'node:assert/strict';
import fs from 'node:fs';

const pagina = fs.readFileSync('templates/index.html', 'utf8');

assert.ok(!pagina.includes('id="prev_vendedor"'), 'A prévia repetitiva não deve retornar ao formulário.');
assert.ok(pagina.includes('itens: selecionados,'), 'Os itens selecionados devem continuar sendo enviados ao backend.');
assert.ok(
  pagina.includes('total_proposta: Math.max(0, selecionados.reduce') && pagina.includes('valor_manual') && pagina.includes('desconto_proposta'),
  'O total da proposta deve considerar os itens selecionados, o valor manual e o desconto.'
);
assert.ok(pagina.includes('desconto_proposta:'), 'O desconto deve continuar sendo enviado ao backend.');
assert.ok(pagina.includes('nome_evento: document.getElementById("nome_evento").value'), 'Os dados do evento devem continuar sendo enviados ao backend.');
assert.ok(pagina.includes('cliente_nome: document.getElementById("busca_cliente").value'), 'Os dados do cliente devem continuar sendo enviados ao backend.');
assert.ok(pagina.includes('data-externo-campo="externo"'), 'A marcação simples de locação externa deve continuar sendo enviada junto ao item.');

console.log('OK: o formulário simplificado preserva itens, total, desconto e dados comerciais para envio.');
