from flask import Flask, render_template, request, jsonify, send_file
import requests
import json
import os
from datetime import datetime
import io

app = Flask(__name__)

# ============================== #
# CONFIGURAÇÕES DA API EXTERNA   #
# ============================== #
TOKEN = "ix29b-35cym-0urb6-910li-u9uau"
API_BASE = "https://app7.meeventos.com.br/soulinkeventos/api/v1"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

# ============================== #
# MAPEAMENTO DE CATEGORIAS       #
# ============================== #
CAT_ID_TO_NAME = {
    "117": "LOGÍSTICA", "135": "PRODUÇÃO", "176": "CRIAÇÃO",
    "177": "ATRAÇÃO MUSICAL", "187": "FOTO E FILMAGEM", "188": "MOBILIÁRIO",
    "189": "PAISAGISMO", "190": "CENOGRAFIA", "191": "ESPAÇOS INSTAGRAMÁVEIS",
    "192": "GRAVAÇÃO DE ÁUDIO", "193": "UNIFILA", "194": "TRADUÇÃO SIMULTÂNEA",
    "195": "HOUSE MIX", "196": "AUDIOVISUAL", "200": "PALCO",
    "202": "PAINEL DE LED", "203": "GRÁFICA", "205": "LEGALIZAÇÃO",
    "208": "STAFF", "209": "GERADOR", "210": "RÁDIOS COMUNICADORES",
    "242": "ESPAÇO INSTAGRAMÁVEL", "246": "COMISSÃO", "275": "ILUMINAÇÃO",
    "280": "TRADUÇÃO SIMULTÂNEA", "281": "TRANSFORMADORES", "284": "CREDENCIAIS",
    "285": "PRODUÇÃO", "288": "BRINDES", "292": "SONORIZAÇÃO PARA BANDA",
    "299": "CREDENCIAMENTO", "305": "ORNAMENTAÇÃO", "321": "MERCHANDISING",
    "325": "ATIVAÇÃO", "332": "TRANSMISSÃO", "335": "CLIMATIZAÇÃO",
    "345": "ELÉTRICA", "363": "DOCUMENTAÇÃO"
}

# Categorias que são SERVIÇO (o resto é EQUIPAMENTO)
SERVICO_CATS = {"STAFF", "PRODUÇÃO", "ATRAÇÃO MUSICAL", "FOTO E FILMAGEM",
                "LEGALIZAÇÃO", "COMISSÃO", "DOCUMENTAÇÃO", "CREDENCIAMENTO",
                "HOUSE MIX", "TRANSMISSÃO", "TRADUÇÃO SIMULTÂNEA",
                "GRAVAÇÃO DE ÁUDIO", "CRIAÇÃO", "LOGÍSTICA"}

# ============================== #
# FUNÇÕES AUXILIARES             #
# ============================== #
def buscar_paginado(endpoint, max_pages=10):
    """Busca todos os registros de um endpoint paginado."""
    todos = []
    page = 1
    while page <= max_pages:
        try:
            resp = requests.get(f"{API_BASE}{endpoint}?page={page}&limit=200", headers=HEADERS, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            items = data.get("data", data if isinstance(data, list) else [])
            todos.extend(items)
            pagination = data.get("pagination", {})
            total_pages = int(pagination.get("total_page", 1))
            if page >= total_pages:
                break
            page += 1
        except Exception as e:
            print(f"Erro ao buscar {endpoint} página {page}: {e}")
            break
    return todos

def calcular_blocos(itens):
    loc, svc = [], []
    for it in itens or []:
        qtd = max(1, int(float(it.get("quantidade", 1))))
        val = float(it.get("valor") or 0)
        tipo = str(it.get("tipo") or it.get("tipo_item") or "equipamento").lower()
        item_novo = {**it, "quantidade": qtd, "valor": val, "subtotal": round(qtd * val, 2)}
        if "serv" in tipo:
            svc.append(item_novo)
        else:
            loc.append(item_novo)
    return {
        "locacao": {"itens": loc, "subtotal": round(sum(i["subtotal"] for i in loc), 2)},
        "servicos": {"itens": svc, "subtotal": round(sum(i["subtotal"] for i in svc), 2)},
        "total_geral": round(sum(i["subtotal"] for i in loc) + sum(i["subtotal"] for i in svc), 2),
    }

# ============================== #
# ROTAS DA API (PROXY)           #
# ============================== #
@app.route("/api/vendedores")
def api_vendedores():
    try:
        resp = requests.get(f"{API_BASE}/seller", headers=HEADERS, timeout=10)
        dados = resp.json()
        return jsonify(sucesso=True, dados=dados)
    except Exception as e:
        return jsonify(sucesso=False, erro=str(e)), 500

@app.route("/api/locais")
def api_locais():
    try:
        resp = requests.get(f"{API_BASE}/eventlocation", headers=HEADERS, timeout=10)
        dados = resp.json()
        return jsonify(sucesso=True, dados=dados)
    except Exception as e:
        return jsonify(sucesso=False, erro=str(e)), 500

@app.route("/api/clientes")
def api_clientes():
    """Busca TODOS os clientes (745+) com paginação automática."""
    try:
        clientes = buscar_paginado("/clients")
        return jsonify(sucesso=True, dados=clientes)
    except Exception as e:
        return jsonify(sucesso=False, erro=str(e)), 500

@app.route("/api/produtos-catalogo")
def api_produtos_catalogo():
    """Busca TODOS os 375 produtos/serviços da API com categorias."""
    try:
        produtos = buscar_paginado("/products-services")
        # Enriquecer com nome da categoria e tipo (Equipamento/Serviço)
        for p in produtos:
            cat_id = p.get("id_cat", "")
            cat_nome = CAT_ID_TO_NAME.get(str(cat_id), "OUTROS")
            p["categoria"] = cat_nome
            p["tipo_item"] = "Serviço" if cat_nome in SERVICO_CATS else "Equipamento"
        return jsonify(sucesso=True, dados=produtos)
    except Exception as e:
        return jsonify(sucesso=False, erro=str(e)), 500

# ============================== #
# PDF ENGINE                     #
# ============================== #
def gerar_pdf_buffer(dados_proposta, num_orcamento=""):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
    )
   
    buffer = io.BytesIO()
    numero = num_orcamento or dados_proposta.get("numero", "RASCUNHO")

    # ✅ LOGO
    CAMINHO_LOGO = "soulink_logo.png"
    if not os.path.exists(CAMINHO_LOGO):
        CAMINHO_LOGO = "soulink_logo_white.png"

    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        leftMargin=1.5*cm, rightMargin=1.5*cm,
        topMargin=1.5*cm, bottomMargin=1.5*cm,
        title=f"Proposta {numero}", author="SLK Eventos"
    )
    styles = getSampleStyleSheet()
    NE = ParagraphStyle('NE', parent=styles['Normal'], fontSize=10, leading=14, spaceAfter=3)
    ROT = ParagraphStyle('ROT', parent=styles['Normal'], fontSize=9, textColor=colors.HexColor("#666"))
    H2  = ParagraphStyle('H2',  parent=styles['Heading2'], fontSize=13, textColor=colors.HexColor("#0056b3"), spaceBefore=10, spaceAfter=6)
    TIT = ParagraphStyle('TIT', parent=styles['Heading1'], fontSize=17, alignment=1, textColor=colors.HexColor("#111"))
    SUB = ParagraphStyle('SUB', parent=styles['Normal'], fontSize=10, alignment=1, textColor=colors.HexColor("#666"), spaceAfter=12)
    NEG = ParagraphStyle('NEG', parent=NE, fontName='Helvetica-Bold')

    def fmt(v): return f"R$ {float(v):,.2f}".replace(",","X").replace(".",",").replace("X",".")

    # ✅ FUNÇÃO PEGAR CORRIGIDA, COMPLETA, ANTES DE USAR
    def pegar(*chaves):
        for c in chaves:
            # Nível raiz
            v = dados_proposta.get(c)
            if v not in (None, "", "-"):
                return str(v).strip()
            # Grupo evento
            if isinstance(dados_proposta.get("evento"), dict):
                v = dados_proposta["evento"].get(c)
                if v not in (None, "", "-"): return str(v).strip()
                if c == "local": v = dados_proposta["evento"].get("local_evento")
                if c == "vendedor": v = dados_proposta["evento"].get("nome_vendedor") or dados_proposta["evento"].get("vendedor")
                if v not in (None, "", "-"): return str(v).strip()
            # Grupo cliente
            if isinstance(dados_proposta.get("cliente"), dict):
                v = dados_proposta["cliente"].get(c)
                if v not in (None, "", "-"): return str(v).strip()
                if c in ("razao_social", "nome"):
                    v = dados_proposta["cliente"].get("nome_cliente") or dados_proposta["cliente"].get("razaosocial") or dados_proposta["cliente"].get("razao_social")
                if c == "documento":
                    v = dados_proposta["cliente"].get("cnpj") or dados_proposta["cliente"].get("cpf") or dados_proposta["cliente"].get("documento")
                if c == "telefone":
                    v = dados_proposta["cliente"].get("telefone_cliente") or dados_proposta["cliente"].get("celular") or dados_proposta["cliente"].get("telefone")
                if v not in (None, "", "-"): return str(v).strip()
        return "-"

    # ✅ ÚNICA VEZ: INICIA LISTA DE ELEMENTOS (SEM DUPLICAR!)
    elementos = []

    # Cabeçalho
    try:
        logo = Image(CAMINHO_LOGO, width=4*cm, height=2.5*cm) if os.path.exists(CAMINHO_LOGO) else Paragraph("<b>SOULINK EVENTOS</b>", TIT)
    except:
        logo = Paragraph("<b>SOULINK EVENTOS</b>", TIT)
    cab = Table([[logo, Paragraph(f"<b>ORÇAMENTO</b><br/>Nº {numero}", TIT)]], colWidths=[5*cm,12*cm])
    cab.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'MIDDLE'),('ALIGN',(1,0),(1,0),'CENTER'),('BOTTOMPADDING',(0,0),(-1,-1),10)]))
    elementos.append(cab)
    elementos.append(Paragraph(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", SUB))
    elementos.append(Spacer(1,0.3*cm))

    # 📌 DADOS DO EVENTO
    elementos.append(Paragraph("<b>📌 DADOS DO EVENTO</b>", H2))
    tev = Table([
        [Paragraph("<b>Evento:</b>",ROT), Paragraph(pegar("nome_evento","nome"),NE),
         Paragraph("<b>Data:</b>",ROT),   Paragraph(pegar("data_evento","data"),NE)],
        [Paragraph("<b>Local:</b>",ROT),  Paragraph(pegar("local_evento","local"),NE),
         Paragraph("<b>Pessoas:</b>",ROT),Paragraph(pegar("qtd_pessoas","quantidade_pessoas"),NE)],
        [Paragraph("<b>Vendedor:</b>",ROT),Paragraph(pegar("vendedor","nome_vendedor"),NE),"",""],
    ], colWidths=[2.2*cm,6.3*cm,2.2*cm,6.3*cm])
    tev.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,-1),colors.HexColor("#f8f9fa")),
        ('BOX',(0,0),(-1,-1),.5,colors.HexColor("#dee2e6")),('INNERGRID',(0,0),(-1,-1),.3,colors.HexColor("#e9ecef")),
        ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
    elementos.append(tev); elementos.append(Spacer(1,0.4*cm))

    # 👤 DADOS DO CLIENTE
    elementos.append(Paragraph("<b>👤 DADOS DO CLIENTE</b>", H2))
    tcl = Table([
        [Paragraph("<b>Razão Social / Nome:</b>",ROT), Paragraph(pegar("razao_social","nome","nome_cliente"), NE)],
        [Paragraph("<b>CNPJ / CPF:</b>",ROT), Paragraph(pegar("documento","doc","cnpj","cpf","cnpjpj","cpfcnpj"), NE),
         Paragraph("<b>Contato:</b>",ROT),     Paragraph(pegar("contato","responsavel","nome_contato","cliente_contato"), NE)],
        [Paragraph("<b>Telefone:</b>",ROT),    Paragraph(pegar("telefone","celular","telefone2","whatsapp","telefone_cliente"), NE),
         Paragraph("<b>Email:</b>",ROT),       Paragraph(pegar("email","email2","email_cliente"), NE)],
    ], colWidths=[2.8*cm,5.7*cm,2.2*cm,6.3*cm])
    tcl.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,-1),colors.HexColor("#fff8e1")),
        ('BOX',(0,0),(-1,-1),.5,colors.HexColor("#ffecb3")),('INNERGRID',(0,0),(-1,-1),.3,colors.HexColor("#ffe082")),
        ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
    elementos.append(tcl); elementos.append(Spacer(1,0.5*cm))

    # ✅ CÁLCULO DOS BLOCOS ANTES DE USAR
    blocos = dados_proposta.get("blocos") or {}
    if not blocos:
        blocos = calcular_blocos(dados_proposta.get("itens", []))
    loc = blocos.get("locacao",  {"itens":[],"subtotal":0})
    svc = blocos.get("servicos", {"itens":[],"subtotal":0})
    total = blocos.get("total_geral", loc["subtotal"]+svc["subtotal"])

    CAB = [["ITEM","DESCRIÇÃO","QTD","UNITÁRIO","SUBTOTAL"]]
    LARG = [2.5*cm,7.5*cm,1.5*cm,3*cm,3*cm]
    EST_BASE = [
        ('ALIGN',(2,0),(-1,-1),'RIGHT'),('ALIGN',(0,0),(0,-1),'CENTER'),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),('GRID',(0,0),(-1,-1),.4,colors.HexColor("#dee2e6")),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor("#f8f9fa")]),
        ('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),
        ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,0),9),
    ]

    # 📦 EQUIPAMENTOS
    elementos.append(Paragraph("<b>📦 EQUIPAMENTOS / LOCAÇÃO</b>", H2))
    dloc = [[Paragraph(str(i.get("codigo","-")),NE), Paragraph(str(i.get("nome","-")),NE), str(i.get("quantidade",1)), fmt(i.get("valor",0)), fmt(i.get("subtotal",0))] for i in loc["itens"]]
    if not dloc: dloc = [["",Paragraph("<i>Nenhum equipamento</i>",NE),"","",""]]
    t1 = Table(CAB+dloc, colWidths=LARG)
    e1 = list(EST_BASE) + [('BACKGROUND',(0,0),(-1,0),colors.HexColor("#0056b3")),('TEXTCOLOR',(0,0),(-1,0),colors.white)]
    t1.setStyle(e1); elementos.append(t1)
    s1 = Table([["","","",Paragraph("SUBTOTAL EQUIPAMENTOS:",NEG),Paragraph(fmt(loc['subtotal']),NEG)]], colWidths=LARG)
    s1.setStyle(TableStyle([('ALIGN',(3,0),(-1,-1),'RIGHT'),
        ('BACKGROUND',(3,0),(-1,-1),colors.HexColor("#e3f2fd")),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('GRID',(0,0),(-1,-1),.4,colors.HexColor("#bbdefb"))]))
    elementos.append(s1); elementos.append(Spacer(1,0.6*cm))

    # 🛠 SERVIÇOS
    elementos.append(Paragraph("<b>🛠 SERVIÇOS / MÃO DE OBRA</b>", H2))
    dsv = [[Paragraph(str(i.get("codigo","-")),NE), Paragraph(str(i.get("nome","-")),NE), str(i.get("quantidade",1)), fmt(i.get("valor",0)), fmt(i.get("subtotal",0))] for i in svc["itens"]]
    if not dsv: dsv = [["",Paragraph("<i>Nenhum serviço</i>",NE),"","",""]]
    t2 = Table(CAB+dsv, colWidths=LARG)
    e2 = list(EST_BASE) + [('BACKGROUND',(0,0),(-1,0),colors.HexColor("#28a745")),('TEXTCOLOR',(0,0),(-1,0),colors.white)]
    t2.setStyle(e2); elementos.append(t2)
    s2 = Table([["","","",Paragraph("SUBTOTAL SERVIÇOS:",NEG),Paragraph(fmt(svc['subtotal']),NEG)]], colWidths=LARG)
    s2.setStyle(TableStyle([('ALIGN',(3,0),(-1,-1),'RIGHT'),
        ('BACKGROUND',(3,0),(-1,-1),colors.HexColor("#e8f5e9")),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('GRID',(0,0),(-1,-1),.4,colors.HexColor("#a5d6a7"))]))
    elementos.append(s2); elementos.append(Spacer(1,0.7*cm))

    # 💰 TOTAL
    TT = ParagraphStyle('TT',parent=NEG,fontSize=12,textColor=colors.HexColor("#e65100"))
    TTV = ParagraphStyle('TTV',parent=NEG,fontSize=14,textColor=colors.HexColor("#e65100"))
    tt = Table([["","","",Paragraph("INVESTIMENTO TOTAL:",TT),Paragraph(fmt(total),TTV)]], colWidths=LARG)
    tt.setStyle(TableStyle([('ALIGN',(3,0),(-1,-1),'RIGHT'),
        ('BACKGROUND',(3,0),(-1,-1),colors.HexColor("#fff3e0")),
        ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),
        ('BOX',(3,0),(-1,-1),1,colors.HexColor("#ffb74d"))]))
    elementos.append(tt); elementos.append(Spacer(1,0.8*cm))

    # Observações
    obs = str(pegar("observacoes","observacao")).strip()
    if obs and obs != "-":
        elementos.append(Paragraph("<b>📝 OBSERVAÇÕES:</b>", H2))
        elementos.append(Paragraph(obs.replace("\n","<br/>"), NE))
        elementos.append(Spacer(1,0.5*cm))

    # Condições
    elementos.append(Paragraph("<b>✅ CONDIÇÕES GERAIS:</b>", H2))
    for c in [
        "• Validade: 15 dias corridos.",
        "• Pagamento: 50% entrada + 50% até 2 dias úteis antes do evento.",
        "• Confirmação mediante assinatura de contrato e pagamento.",
        "• Não incluso: alimentação, transporte, impostos e taxas de terceiros não mencionados.",
        "• Alterações de escopo por escrito e com reajuste.",
    ]: elementos.append(Paragraph(c, NE))

    doc.build(elementos)
    buffer.seek(0)
    return buffer

@app.route("/api/gerar-pdf", methods=["POST"])
def api_gerar_pdf():
    dados_proposta = request.json
    num_orcamento = dados_proposta.get("num_orcamento", "")
    pdf_buffer = gerar_pdf_buffer(dados_proposta, num_orcamento)
    filename = f"proposta_SLK_{num_orcamento}_{datetime.now().strftime('%d%m%Y')}.pdf"
    return send_file(pdf_buffer, download_name=filename, mimetype="application/pdf")

# ============================== #
# ENVIO PARA O MEEVENTOS         #
# ============================== #
@app.route("/api/enviar-orcamento", methods=["POST"])
def api_enviar_orcamento():
    dados = request.json
    try:
        payload = {
            "nome": dados.get("cliente_nome", "Cliente") or "Cliente",
            "nomedoevento": dados.get("nome_evento", "Evento SLK") or "Evento SLK",
            "dataevento": dados.get("data_evento", "") or "",
            "idvendedor": str(dados.get("id_vendedor", "51")) or "51",
            "numeroconvidados": str(dados.get("qtd_pessoas", "")) or "",
            "nomeresponsavel": dados.get("cliente_contato", "") or "",
            "observacao": f"Proposta gerada via SLK Propostas Pro | Total: R$ {dados.get('total_proposta', 0):.2f}"
        }
        # ✅ CORRIGIDO: Adicionar Accept header obrigatório
        post_headers = {
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        res = requests.post(f"{API_BASE}/budgets", headers=post_headers, json=payload, timeout=15)
        res.raise_for_status()
        resposta = res.json()
        # Retorna o ID do orçamento criado no Meeventos
        id_orcamento = resposta.get("id", "")
        return jsonify(sucesso=True, id_orcamento=id_orcamento)
    except requests.exceptions.RequestException as e:
        erro_detalhe = ""
        if hasattr(e, 'response') and e.response is not None:
            erro_detalhe = e.response.text
        return jsonify(sucesso=False, erro=str(e), detalhes=erro_detalhe), 500

# ============================== #
# SALVAR / LISTAR PROPOSTAS      #
# ============================== #
ARQUIVO_PROPOSTAS = "propostas.json"

def _salvar_json(arquivo, dados):
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

def _ler_json(arquivo, padrao):
    if not os.path.exists(arquivo): return padrao
    try:
        with open(arquivo, "r", encoding="utf-8") as f: return json.load(f)
    except:
        return padrao

@app.route("/api/calcular", methods=["POST"])
def api_calcular():
    return jsonify({"sucesso": True, "blocos": calcular_blocos(request.get_json(force=True).get("itens", []))})

@app.route("/api/gerar-proposta", methods=["POST"])
def api_gerar_proposta():
    # Recebe os dados enviados do formulário
    dados = request.get_json(force=True) or {}

    # Calcula blocos de locação e serviços com valores
    blocos = calcular_blocos(dados.get("itens", []))
    dados["blocos"] = blocos

    # Garante estrutura organizada dos dados do evento
    if "evento" not in dados:
        dados["evento"] = {
            "nome_evento": dados.get("nome_evento", "-"),
            "data_evento": dados.get("data_evento", "-"),
            "local_evento": dados.get("local_evento", "-"),
            "qtd_pessoas": dados.get("qtd_pessoas", "-"),
            "vendedor": dados.get("vendedor", "-"),
            "id_vendedor": dados.get("id_vendedor", "51")
        }

    # Garante estrutura organizada dos dados do cliente
    if "cliente" not in dados:
        dados["cliente"] = {
            "razao_social": dados.get("razao_social") or dados.get("nome_cliente", "-"),
            "documento": dados.get("cnpj") or dados.get("cpf") or "-",
            "contato": dados.get("contato_cliente", "-"),
            "telefone": dados.get("telefone_cliente", "-"),
            "email": dados.get("email_cliente", "-")
        }

    # Envia proposta para o Meeventos e captura número oficial
    numero_meeventos = ""
    try:
        payload_envio = {
            "nome": dados["cliente"]["razao_social"],
            "nomedoevento": dados["evento"]["nome_evento"],
            "dataevento": dados["evento"]["data_evento"],
            "idvendedor": str(dados["evento"]["id_vendedor"]),
            "numeroconvidados": str(dados["evento"]["qtd_pessoas"]),
            "nomeresponsavel": dados["cliente"]["contato"],
            "observacao": f"SOULINK | Novos Orçamentos | Total R$ {blocos['total_geral']:.2f}"
        }
        # ✅ CORRIGIDO: Usar headers com Accept
        post_headers = {
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        r = requests.post(f"{API_BASE}/budgets", headers=post_headers, json=payload_envio, timeout=15)
        if r.status_code < 300:
            resp = r.json() or {}
            numero_meeventos = str(resp.get("id") or resp.get("numero") or resp.get("idorcamento") or "")
            print(f"✅ Orçamento enviado ao Meeventos: {numero_meeventos}")
        else:
            print(f"⚠️ Meeventos retornou {r.status_code}: {r.text[:200]}")
    except Exception as e:
        print(f"[Meeventos] Aviso: não enviado -> {e}")

    # ===== 📂 CRIAÇÃO AUTOMÁTICA DA PASTA PDFS =====
    pdf_buf = gerar_pdf_buffer(dados, numero_meeventos)
    nome_pdf = f"orcamento_{(numero_meeventos or ('PROV-'+str(int(datetime.now().timestamp())))).replace('/','-')}.pdf"
    pasta_pdf = "pdfs"
    os.makedirs(pasta_pdf, exist_ok=True)  # ✅ CRIA SE NÃO EXISTIR
    caminho_completo_pdf = os.path.join(pasta_pdf, nome_pdf)

    # Salva o arquivo PDF na pasta
    try:
        with open(caminho_completo_pdf, "wb") as f:
            f.write(pdf_buf.getvalue())
        print(f"✅ PDF salvo com sucesso: {caminho_completo_pdf}")
    except Exception as e:
        print(f"❌ Erro ao salvar PDF: {e}")
        return jsonify({"sucesso": False, "erro": f"Falha ao salvar PDF: {str(e)}"}), 500

    # ✅ CORRIGIDO: Salva a proposta no histórico (propostas.json) para aparecer em "Meus Orçamentos"
    todas_propostas = _ler_json(ARQUIVO_PROPOSTAS, [])
    
    # Gera ID único para a proposta (usa número do Meeventos se disponível)
    numero_proposta = numero_meeventos or f"PROV-{len(todas_propostas)+1:04d}"
    
    proposta_salva = {
        "numero": numero_proposta,
        "versao": 1,
        "data_criacao": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "numero_oficial": numero_meeventos or None,
        "cliente": dados.get("cliente", {}),
        "evento": dados.get("evento", {}),
        "blocos": blocos,
        "observacoes": dados.get("observacoes", "") or "",
        "arquivo_pdf": nome_pdf,
        "itens": dados.get("itens", [])  # ✅ Salva itens para edição futura
    }
    
    todas_propostas.append(proposta_salva)
    _salvar_json(ARQUIVO_PROPOSTAS, todas_propostas)
    
    print(f"✅ Proposta salva no histórico: {numero_proposta}")

    # Retorna dados para o frontend (com link para abrir o PDF)
    return jsonify({
        "sucesso": True,
        "numero_proposta": numero_proposta,
        "arquivo_pdf": nome_pdf,
        "url_pdf": f"/pdfs/{nome_pdf}",  # ✅ Link para abrir automaticamente
        "blocos": blocos,
        "enviado_meeventos": bool(numero_meeventos)
    })

@app.route("/api/propostas")
def api_listar_propostas():
    """Lista todas as propostas agrupadas por número (com histórico de versões)."""
    todas = _ler_json(ARQUIVO_PROPOSTAS, [])
    agrupado = {}
    
    for p in todas:
        n = p.get("numero", "SEM_NUMERO")
        
        if n not in agrupado:
            agrupado[n] = {
                "numero": n,
                "cliente": p.get("cliente",{}).get("razao_social") or p.get("cliente",{}).get("nome") or "-",
                "evento": p.get("evento",{}).get("nome_evento") or "-",
                "total": p.get("blocos",{}).get("total_geral",0),
                "ultima_versao": 1,
                "ultima_data": p.get("data_criacao",""),
                "numero_oficial": p.get("numero_oficial", ""),
                "versoes": [],
            }
        
        agrupado[n]["versoes"].append({
            "versao": p.get("versao",1),
            "data": p.get("data_criacao",""),
            "total": p.get("blocos",{}).get("total_geral",0),
            "arquivo_pdf": p.get("arquivo_pdf",""),
            "numero_oficial": p.get("numero_oficial", "")
        })
        
        # Atualiza última versão e data
        agrupado[n]["ultima_versao"] = max(agrupado[n]["ultima_versao"], p.get("versao",1))
        agrupado[n]["ultima_data"] = p.get("data_criacao","")
    
    return jsonify({"quantidade": len(agrupado), "dados": list(agrupado.values())})

@app.route("/pdfs/<nome>")
def download_pdf(nome):
    """Serve PDFs da pasta pdfs."""
    return send_file(os.path.join("pdfs", nome), mimetype="application/pdf")

# ============================== #
# ROTAS DO FRONTEND              #
# ============================== #
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/produtos")
def pagina_produtos():
    return render_template("produtos.html") if os.path.exists("templates/produtos.html") else render_template("index.html")

@app.route("/propostas")
def pagina_propostas():
    caminho = "templates/propostas.html"
    # 1º: verifica se o arquivo existe no lugar certo
    if not os.path.exists(caminho):
        return f"""
        <h1 style="color:red">❌ Arquivo não encontrado!</h1>
        <p>Esperava encontrar em: <code>{caminho}</code></p>
        <p>✅ Verifique se:</p>
        <ul>
            <li>O arquivo se chama <b>exatamente</b> <code>propostas.html</code></li>
            <li>Ele está <b>DENTRO</b> da pasta <code>templates</code> (ao lado do <code>index.html</code>)</li>
            <li>Não tem espaço, acento ou letra maiúscula errada no nome</li>
        </ul>
        """
    # 2º: tenta abrir, se der erro mostra qual é
    try:
        return render_template("propostas.html")
    except Exception as e:
        import traceback
        return f"""
        <h1 style="color:red">❌ Erro ao carregar a página</h1>
        <h3>Motivo:</h3>
        <pre style="background:#f8f8f8;padding:15px">{str(e)}</pre>
        <h3>Detalhe completo:</h3>
        <pre style="background:#f0f0f0;padding:15px;font-size:11px">{traceback.format_exc()}</pre>
        """

@app.route("/meus-itens")
def meus_itens():
    return render_template("meus_itens.html") if os.path.exists("templates/meus_itens.html") else render_template("index.html")

# ============================== #
# INICIALIZAÇÃO                  #
# ============================== #
if __name__ == "__main__":
    print("="*60)
    print("  SOULINK — INTEGRAÇÃO MEEVENTOS")
    print("="*60)
    print(f"  🏠 Painel          : http://localhost:5000")
    print(f"  📋 Minhas Propostas: http://localhost:5000/propostas")
    print(f"  📦 Meus Itens      : http://localhost:5000/meus-itens")
    print("="*60)
    app.run(debug=True, host="0.0.0.0", port=5000)
