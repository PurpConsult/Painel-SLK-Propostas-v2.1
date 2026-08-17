import assert from 'node:assert/strict';
import fs from 'node:fs';
import puppeteer from 'puppeteer-core';

const url = 'http://127.0.0.1:5001/';
const screenshot = '/home/ubuntu/entregas/validacao_movel_interativa.png';
let payloadEnviado = null;

const browser = await puppeteer.launch({
  executablePath: '/usr/bin/chromium',
  headless: true,
  args: ['--no-sandbox', '--disable-setuid-sandbox'],
});

try {
  const page = await browser.newPage();
  await page.setViewport({ width: 375, height: 812, isMobile: true, deviceScaleFactor: 1 });
  page.on('request', request => {
    if (request.url().endsWith('/api/gerar-proposta') && request.method() === 'POST') {
      payloadEnviado = JSON.parse(request.postData() || '{}');
    }
  });

  await page.goto(url, { waitUntil: 'networkidle0' });
  await page.evaluate(() => {
    localStorage.setItem('dados_editar', JSON.stringify({
      evento: { nome_evento: 'Evento Mobile Real', local_evento: 'Local Mobile Real', qtd_pessoas: 12, formato_evento: 'Auditório', evento_sem_data: true, nome_vendedor: 'Jairo Mobile', id_vendedor: '62' },
      cliente: { nome: 'Cliente Mobile Real', cnpj: '', email: '', telefone: '', contato: '' },
      itens: [
        { id: '701', nome: 'PROJETOR MOBILE REAL', valor: 100, valor_padrao: 100, valor_manual: '', quantidade: 2, tipo_item: 'Equipamento', externo: false, fornecedor_externo: '', custo_externo: 0 },
        { id: '702', nome: 'TÉCNICO MOBILE REAL', valor: 480, valor_padrao: 480, valor_manual: '', quantidade: 1, tipo_item: 'Serviço', externo: false, fornecedor_externo: '', custo_externo: 0 },
      ],
    }));
  });
  await page.reload({ waitUntil: 'networkidle0' });
  await page.waitForSelector('[data-comercial-campo="valor_manual"][data-idx="0"]');

  const layout = await page.evaluate(() => {
    const grade = document.querySelector('.formulario-duas-colunas');
    const esquerda = document.querySelector('.coluna-esquerda').getBoundingClientRect();
    const direita = document.querySelector('.coluna-direita').getBoundingClientRect();
    return {
      colunas: getComputedStyle(grade).gridTemplateColumns,
      esquerda: { x: esquerda.x, top: esquerda.top, width: esquerda.width },
      direita: { x: direita.x, top: direita.top, width: direita.width },
      overflowHorizontal: document.documentElement.scrollWidth > window.innerWidth,
    };
  });
  assert.equal(layout.overflowHorizontal, false, 'A tela móvel não pode gerar rolagem horizontal.');
  assert.equal(layout.esquerda.x, layout.direita.x, 'Em largura móvel, as colunas devem ocupar a mesma faixa horizontal.');
  assert.ok(layout.direita.top > layout.esquerda.top, 'A seleção deve aparecer depois de briefing e dados em tela móvel.');

  await page.locator('#busca_vendedor').fill('Jairo Mobile');
  await page.locator('#nome_evento').fill('Evento Mobile Real');
  await page.locator('#busca_local').fill('Local Mobile Real');
  await page.locator('#qtd_pessoas').fill('12');
  await page.locator('#formato_evento').fill('Auditório');
  await page.locator('#busca_cliente').fill('Cliente Mobile Real');
  await page.locator('[data-comercial-campo="valor_manual"][data-idx="0"]').fill('125');
  await page.keyboard.press('Tab');
  await page.locator('[data-externo-campo="externo"][data-idx="0"]').click();
  await page.locator('.comercial-extra summary').click();
  await page.locator('#desconto_proposta').fill('30');
  const semDataMarcado = await page.$eval('#evento_sem_data', campo => campo.checked);
  if (!semDataMarcado) await page.locator('#evento_sem_data').click();
  const respostaEnvio = page.waitForResponse(resposta => resposta.url().endsWith('/api/gerar-proposta') && resposta.request().method() === 'POST');
  await page.locator('#btnSubmit').click();
  const resposta = await respostaEnvio;
  assert.equal(resposta.status(), 200, 'O envio isolado deve retornar sucesso.');
  await page.waitForFunction(() => document.getElementById('msg_resultado')?.textContent?.includes('salva localmente'));

  assert.ok(payloadEnviado, 'O envio precisa alcançar o backend isolado pelo navegador real.');
  assert.equal(payloadEnviado.itens.length, 2);
  assert.equal(payloadEnviado.itens[0].valor, 125);
  assert.equal(payloadEnviado.itens[0].valor_manual, '125');
  assert.equal(payloadEnviado.itens[0].externo, true);
  assert.equal(payloadEnviado.desconto_proposta, 30);
  assert.equal(payloadEnviado.total_proposta, 700);

  await page.screenshot({ path: screenshot, fullPage: true });
  assert.ok(fs.existsSync(screenshot), 'A captura de validação móvel precisa ser gerada.');
  console.log('OK: navegador móvel real validou layout empilhado, item, valor manual, locação externa e envio isolado.');
} finally {
  await browser.close();
}
