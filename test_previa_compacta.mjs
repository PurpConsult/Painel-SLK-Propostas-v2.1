import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';

const pagina = fs.readFileSync('templates/index.html', 'utf8');
const blocoScript = pagina.match(/<script>([\s\S]*?)<\/script>/)?.[1] || '';
const inicio = blocoScript.indexOf('function escaparHtmlIA');
const fim = blocoScript.indexOf('async function lerArquivoBriefing');

assert.ok(inicio >= 0 && fim > inicio, 'Não foi possível extrair a prévia compacta do formulário.');

const elementos = { resultado_ia: { className: '', innerHTML: '' } };
const contexto = vm.createContext({
  document: { getElementById: (id) => elementos[id] || (elementos[id] = {}) },
  console,
});

vm.runInContext(blocoScript.slice(inicio, fim), contexto);

contexto.renderizarAnaliseIA({
  resumo: 'Teste de separação.',
  sugestoes_itens: [
    { pedido: 'Projetor', quantidade_sugerida: 1, candidatos: [{ id: 10, nome: 'PROJETOR 5000 LUMENS', tipo_item: 'Equipamento', valor: 1050 }] },
    { pedido: 'Operação', quantidade_sugerida: 1, candidatos: [{ id: 20, nome: 'TÉCNICO AUDIOVISUAL', tipo_item: 'Serviço', valor: 480 }] },
  ],
  itens_nao_localizados: [{ pedido: 'Cabo de rede', quantidade_sugerida: 2 }],
  alertas: [],
});

const html = elementos.resultado_ia.innerHTML;
const inicioEquipamentos = html.indexOf('<h4>Equipamentos prioritários</h4>');
const inicioServicos = html.indexOf('Ver 1 serviço(s) identificado(s) e já incluído(s)');
const equipamento = html.indexOf('PROJETOR 5000 LUMENS');
const servico = html.indexOf('TÉCNICO AUDIOVISUAL');

assert.ok(inicioEquipamentos >= 0, 'A seção de equipamentos prioritários deve existir.');
assert.ok(inicioServicos > inicioEquipamentos, 'A seção de serviços deve existir após equipamentos.');
assert.ok(equipamento > inicioEquipamentos && equipamento < inicioServicos, 'O equipamento deve ficar somente na seção prioritária.');
assert.ok(servico > inicioServicos, 'O serviço não pode aparecer na seção de equipamentos prioritários.');
assert.ok(html.includes('Não localizamos no catálogo'), 'Os itens não localizados devem continuar resumidos.');

console.log('OK: equipamentos e serviços estão separados na prévia compacta.');
