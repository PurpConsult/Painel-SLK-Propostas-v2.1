from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
)
from datetime import datetime
import os

PASTA_PDFS = "pdfs"
if not os.path.exists(PASTA_PDFS):
    os.makedirs(PASTA_PDFS)

# ✅ LOGO CERTA (usa o arquivo que está na sua pasta)
CAMINHO_LOGO = "soulink_logo.png"
# Se a logo acima não existir, tenta a outra:
if not os.path.exists(CAMINHO_LOGO):
    CAMINHO_LOGO = "soulink_logo_white.png"

LARGURA_PAGINA, ALTURA_PAGINA = A4
MARGEM = 1.5 * cm

def _formatar_real(valor):
    return f"R$ {float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def gerar_pdf_proposta(proposta):
    numero = proposta.get("numero", "SEM-NUMERO")
    nome_arquivo = f"proposta_{numero.replace('/', '-')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    caminho_completo = os.path.join(PASTA_PDFS, nome_arquivo)

    doc = SimpleDocTemplate(
        caminho_completo,
        pagesize=A4,
        leftMargin=MARGEM,
        rightMargin=MARGEM,
        topMargin=MARGEM,
        bottomMargin=MARGEM,
        title=f"Proposta {numero}",
        author="SLK Eventos"
    )

    styles = getSampleStyleSheet()
    estilo_titulo = ParagraphStyle(
        'Titulo', parent=styles['Heading1'],
        fontSize=18, textColor=colors.HexColor("#1a1a1a"),
        spaceAfter=6, alignment=1
    )
    estilo_subtitulo = ParagraphStyle(
        'Subtitulo', parent=styles['Normal'],
        fontSize=10, textColor=colors.HexColor("#666666"),
        spaceAfter=14, alignment=1
    )
    estilo_h2 = ParagraphStyle(
        'H2', parent=styles['Heading2'],
        fontSize=13, textColor=colors.HexColor("#0056b3"),
        spaceBefore=10, spaceAfter=6
    )
    estilo_normal = ParagraphStyle(
        'Normal', parent=styles['Normal'],
        fontSize=10, leading=14, spaceAfter=4
    )
    estilo_rotulo = ParagraphStyle(
        'Rotulo', parent=styles['Normal'],
        fontSize=9, textColor=colors.HexColor("#666666")
    )

    elementos = []

    # ==============================================
    # ✅ CABEÇALHO COM LOGO + TÍTULO
    # ==============================================
    dados_cabecalho = []
    try:
        if os.path.exists(CAMINHO_LOGO):
            logo = Image(CAMINHO_LOGO, width=4*cm, height=2.5*cm)
            logo.hAlign = 'LEFT'
        else:
            logo = Paragraph("<b>SLK EVENTOS</b>", estilo_titulo)
    except:
        logo = Paragraph("<b>SLK EVENTOS</b>", estilo_titulo)

    bloco_titulo = [
        [logo, Paragraph(f"<b>PROPOSTA COMERCIAL</b><br/>Nº {numero}", estilo_titulo)]
    ]
    tabela_cabecalho = Table(bloco_titulo, colWidths=[5*cm, 12*cm])
    tabela_cabecalho.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (1,0), (1,0), 'CENTER'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    elementos.append(tabela_cabecalho)
    elementos.append(Paragraph(f"Gerada em: {proposta.get('data_criacao', datetime.now().strftime('%d/%m/%Y %H:%M'))}", estilo_subtitulo))
    elementos.append(Spacer(1, 0.3*cm))

    # ==============================================
    # 📌 DADOS DO EVENTO
    # ==============================================
    ev = proposta.get("evento", {})
    elementos.append(Paragraph("<b>📌 DADOS DO EVENTO</b>", estilo_h2))
    tabela_evento = Table([
        [Paragraph("<b>Evento:</b>", estilo_rotulo), Paragraph(ev.get("nome_evento", "-"), estilo_normal),
         Paragraph("<b>Data:</b>", estilo_rotulo), Paragraph(ev.get("data_evento", "-"), estilo_normal)],
        [Paragraph("<b>Local:</b>", estilo_rotulo), Paragraph(ev.get("local_evento", "-"), estilo_normal),
         Paragraph("<b>Pessoas:</b>", estilo_rotulo), Paragraph(str(ev.get("qtd_pessoas", "-")), estilo_normal)],
        [Paragraph("<b>Vendedor:</b>", estilo_rotulo), Paragraph(ev.get("vendedor", "-"), estilo_normal), "", ""],
    ], colWidths=[2.2*cm, 6.3*cm, 2.2*cm, 6.3*cm])
    tabela_evento.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8f9fa")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#dee2e6")),
        ('INNERGRID', (0,0), (-1,-1), 0.3, colors.HexColor("#e9ecef")),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    elementos.append(tabela_evento)
    elementos.append(Spacer(1, 0.4*cm))

    # ==============================================
    # 👤 DADOS DO CLIENTE
    # ==============================================
    cl = proposta.get("cliente", {})
    elementos.append(Paragraph("<b>👤 DADOS DO CLIENTE</b>", estilo_h2))
    tabela_cliente = Table([
        [Paragraph("<b>Razão Social / Nome:</b>", estilo_rotulo), Paragraph(cl.get("razao_social") or cl.get("nome") or "-", estilo_normal)],
        [Paragraph("<b>CNPJ / CPF:</b>", estilo_rotulo), Paragraph(cl.get("documento") or cl.get("cnpj") or cl.get("cpf") or "-", estilo_normal),
         Paragraph("<b>Contato:</b>", estilo_rotulo), Paragraph(cl.get("contato") or cl.get("responsavel") or "-", estilo_normal)],
        [Paragraph("<b>Telefone:</b>", estilo_rotulo), Paragraph(cl.get("telefone") or cl.get("celular") or "-", estilo_normal),
         Paragraph("<b>Email:</b>", estilo_rotulo), Paragraph(cl.get("email") or "-", estilo_normal)],
    ], colWidths=[2.8*cm, 5.7*cm, 2.2*cm, 6.3*cm])
    tabela_cliente.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#fff8e1")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#ffecb3")),
        ('INNERGRID', (0,0), (-1,-1), 0.3, colors.HexColor("#ffe082")),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    elementos.append(tabela_cliente)
    elementos.append(Spacer(1, 0.5*cm))

    # ==============================================
    # 📦 BLOCO 1: EQUIPAMENTOS / LOCAÇÃO
    # ==============================================
    blocos = proposta.get("blocos", {})
    loc = blocos.get("locacao", {"itens": [], "subtotal": 0})
    itens_loc = loc.get("itens", [])

    elementos.append(Paragraph("<b>📦 EQUIPAMENTOS / LOCAÇÃO</b>", estilo_h2))

    cabecalho = [["ITEM", "DESCRIÇÃO", "QTD", "UNITÁRIO", "SUBTOTAL"]]
    dados_loc = []
    for it in itens_loc:
        dados_loc.append([
            Paragraph(str(it.get("codigo", "-")), estilo_normal),
            Paragraph(str(it.get("nome", "-")), estilo_normal),
            str(it.get("quantidade", 1)),
            _formatar_real(it.get("valor", 0)),
            _formatar_real(it.get("subtotal", 0)),
        ])

    if not dados_loc:
        dados_loc = [["", Paragraph("<i>Nenhum equipamento adicionado</i>", estilo_normal), "", "", ""]]

    tabela_loc = Table(cabecalho + dados_loc, colWidths=[2.5*cm, 7.5*cm, 1.5*cm, 3*cm, 3*cm])
    estilo_tabela = [
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0056b3")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 9),
        ('ALIGN', (2,0), (-1,-1), 'RIGHT'),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.4, colors.HexColor("#dee2e6")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8f9fa")]),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]
    tabela_loc.setStyle(estilo_tabela)
    elementos.append(tabela_loc)

    subtotal_loc = [
        ["", "", "", "<b>SUBTOTAL EQUIPAMENTOS:</b>", f"<b>{_formatar_real(loc.get('subtotal', 0))}</b>"]
    ]
    t_sub_loc = Table(subtotal_loc, colWidths=[2.5*cm, 7.5*cm, 1.5*cm, 3*cm, 3*cm])
    t_sub_loc.setStyle(TableStyle([
        ('ALIGN', (3,0), (-1,-1), 'RIGHT'),
        ('FONTNAME', (3,0), (-1,-1), 'Helvetica-Bold'),
        ('BACKGROUND', (3,0), (-1,-1), colors.HexColor("#e3f2fd")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.4, colors.HexColor("#bbdefb")),
    ]))
    elementos.append(t_sub_loc)
    elementos.append(Spacer(1, 0.6*cm))

    # ==============================================
    # 🛠 BLOCO 2: SERVIÇOS
    # ==============================================
    svc = blocos.get("servicos", {"itens": [], "subtotal": 0})
    itens_svc = svc.get("itens", [])

    elementos.append(Paragraph("<b>🛠 SERVIÇOS / MÃO DE OBRA</b>", estilo_h2))

    dados_svc = []
    for it in itens_svc:
        dados_svc.append([
            Paragraph(str(it.get("codigo", "-")), estilo_normal),
            Paragraph(str(it.get("nome", "-")), estilo_normal),
            str(it.get("quantidade", 1)),
            _formatar_real(it.get("valor", 0)),
            _formatar_real(it.get("subtotal", 0)),
        ])

    if not dados_svc:
        dados_svc = [["", Paragraph("<i>Nenhum serviço adicionado</i>", estilo_normal), "", "", ""]]

    tabela_svc = Table(cabecalho + dados_svc, colWidths=[2.5*cm, 7.5*cm, 1.5*cm, 3*cm, 3*cm])
    estilo_tabela_svc = list(estilo_tabela)
    estilo_tabela_svc[0] = ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#28a745"))
    estilo_tabela_svc[1] = ('TEXTCOLOR', (0,0), (-1,0), colors.white)
    tabela_svc.setStyle(estilo_tabela_svc)
    elementos.append(tabela_svc)

    subtotal_svc = [
        ["", "", "", "<b>SUBTOTAL SERVIÇOS:</b>", f"<b>{_formatar_real(svc.get('subtotal', 0))}</b>"]
    ]
    t_sub_svc = Table(subtotal_svc, colWidths=[2.5*cm, 7.5*cm, 1.5*cm, 3*cm, 3*cm])
    t_sub_svc.setStyle(TableStyle([
        ('ALIGN', (3,0), (-1,-1), 'RIGHT'),
        ('FONTNAME', (3,0), (-1,-1), 'Helvetica-Bold'),
        ('BACKGROUND', (3,0), (-1,-1), colors.HexColor("#e8f5e9")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.4, colors.HexColor("#a5d6a7")),
    ]))
    elementos.append(t_sub_svc)
    elementos.append(Spacer(1, 0.7*cm))

    # ==============================================
    # 💰 TOTAL GERAL
    # ==============================================
    total = blocos.get("total_geral", loc.get("subtotal",0) + svc.get("subtotal",0))
    tabela_total = Table([
        ["", "", "", "", ""],
        ["", "", "", "<b>INVESTIMENTO TOTAL:</b>", f"<b><font size='14'>{_formatar_real(total)}</font></b>"]
    ], colWidths=[2.5*cm, 7.5*cm, 1.5*cm, 3*cm, 3*cm])
    tabela_total.setStyle(TableStyle([
        ('ALIGN', (3,1), (-1,-1), 'RIGHT'),
        ('FONTNAME', (3,1), (-1,-1), 'Helvetica-Bold'),
        ('BACKGROUND', (3,1), (-1,-1), colors.HexColor("#fff3e0")),
        ('TEXTCOLOR', (3,1), (-1,-1), colors.HexColor("#e65100")),
        ('TOPPADDING', (0,1), (-1,-1), 8),
        ('BOTTOMPADDING', (0,1), (-1,-1), 8),
        ('BOX', (3,1), (-1,-1), 1, colors.HexColor("#ffb74d")),
    ]))
    elementos.append(tabela_total)
    elementos.append(Spacer(1, 0.8*cm))

    # ==============================================
    # 📝 OBSERVAÇÕES
    # ==============================================
    obs = proposta.get("observacoes", "").strip()
    if obs:
        elementos.append(Paragraph("<b>📝 OBSERVAÇÕES:</b>", estilo_h2))
        elementos.append(Paragraph(obs.replace("\n", "<br/>"), estilo_normal))
        elementos.append(Spacer(1, 0.5*cm))

    # ==============================================
    # ✅ CONDIÇÕES GERAIS
    # ==============================================
    elementos.append(Paragraph("<b>✅ CONDIÇÕES GERAIS:</b>", estilo_h2))
    condicoes = [
        "• Validade da proposta: 15 (quinze) dias corridos a partir da data de emissão.",
        "• Forma de pagamento: 50% de entrada na confirmação e 50% até 2 dias úteis antes do evento.",
        "• A confirmação do evento se dará mediante a assinatura do contrato e pagamento da entrada.",
        "• Não incluso: alimentação, transporte, materiais de consumo, impostos municipais/estaduais e taxas de terceiros não mencionados explicitamente.",
        "• Qualquer alteração no escopo deverá ser formalizada por escrito e implicará em reajuste de valores.",
    ]
    for c in condicoes:
        elementos.append(Paragraph(c, estilo_normal))

    doc.build(elementos)
    return caminho_completo