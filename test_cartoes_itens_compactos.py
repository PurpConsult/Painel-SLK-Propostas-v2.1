from pathlib import Path


html = Path(__file__).with_name("templates").joinpath("index.html").read_text(encoding="utf-8")

# A visão desktop deve manter os controles essenciais na mesma linha do card.
assert 'grid-template-areas:"identidade quantidade manual total remover"' in html

# A quantidade não pode voltar a ficar em uma faixa exclusiva abaixo do item.
assert 'grid-area:quantidade;display:flex;align-items:center' in html
assert 'grid-template-areas:"identidade remover" "operacao operacao"' not in html

# O HTML deve manter os cinco blocos na sequência comercial desejada.
inicio_renderizacao = html.index('const linha = `<div class="item-com-locacao"><div class="item-cartao">')
fim_renderizacao = html.index('</div>${renderizarComposicaoKit(item, idx)}${renderizarLocacaoExterna(item, idx)}</div>`;', inicio_renderizacao)
card = html[inicio_renderizacao:fim_renderizacao]

assert card.index('class="item-identidade"') < card.index('class="item-quantidade"')
assert card.index('class="item-quantidade"') < card.index('class="item-valor-manual"')
assert card.index('class="item-valor-manual"') < card.index('class="item-total"')
assert card.index('class="item-total"') < card.index('class="remover"')

# Os kits preservam um painel próprio de componentes depois do card principal.
assert 'function renderizarComposicaoKit(item, idx)' in html
assert 'data-comp-action="minus"' in html
assert 'data-comp-action="plus"' in html
assert 'data-comp-action="remover"' in html
assert html.count('componentes: Array.isArray(item.componentes) ? item.componentes.map(componente => ({...componente})) : [],') == 2
assert 'const botaoComponente = e.target.closest("[data-comp-action]");' in html
assert 'kit.componentes.splice(componenteIdx, 1);' in html
assert 'kit.valor = Math.round(novoValor * 100) / 100;' in html
assert 'kit.valor_padrao = kit.valor;' in html

# No celular, a segunda linha deve ser uma adaptação responsiva, não um retorno
# ao card alto anterior.
assert '@media(max-width:1100px) and (min-width:769px){.item-cartao{grid-template-columns:minmax(0,1fr) auto 24px;grid-template-areas:"identidade quantidade remover" "manual total total"' in html
assert '@media(max-width:560px){.item-cartao{grid-template-columns:minmax(0,1fr) auto 24px;grid-template-areas:"identidade quantidade remover" "manual total total"' in html

print("OK: cards de itens preservam nome, quantidade, valor manual, total e remoção no layout compacto.")
