import random
import streamlit as st

# =========================================================
# SAFETOPOLY: O JOGO DA NR-1 (GERENCIAMENTO DE RISCOS)
# Gamificação Corporativa em Tabuleiro Quadrado 7x7 Nativo
# =========================================================

st.set_page_config(page_title="SafeTopoly NR-1", page_icon="🦺", layout="wide")

# --- ESTILIZAÇÃO VISUAL COMPACTA DE ALTO CONTRASTE ---
st.markdown("""
    <style>
    .stApp { background-color: #0f172a !important; } /* Fundo azul escuro corporativo */
    .block-container { padding: 0.5rem 2rem 0rem 2rem !important; }
    header, footer { visibility: hidden; }
    hr { margin: 0.4rem 0 !important; border-color: rgba(255,255,255,0.2) !important; }

    .status-text {
        color: #ffffff !important;
        font-family: 'Courier New', Courier, monospace;
        font-weight: bold;
        font-size: 15px;
        text-align: center;
        background-color: rgba(30, 41, 59, 0.9);
        padding: 6px 12px;
        border-radius: 6px;
        margin: 0px;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* MALHA QUADRADA DO TABULEIRO (7x7) */
    .banco-grid {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        grid-template-rows: repeat(7, 1fr);
        gap: 6px;
        max-width: 680px;
        margin: 0 auto;
        background-color: #1e293b;
        padding: 12px;
        border-radius: 10px;
        border: 3px solid #f59e0b; /* Borda laranja de segurança */
        box-shadow: 4px 4px 15px rgba(0,0,0,0.5);
    }
    
    .tile-square {
        color: black !important;
        text-align: center;
        padding: 4px 2px;
        border-radius: 4px;
        border: 2px solid #000000;
        font-weight: bold;
        font-size: 10px;
        height: 75px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: inset 0 0 4px rgba(0,0,0,0.2);
    }
    
    /* Centro vazio ocupando as linhas e colunas internas (2 a 6) */
    .board-center {
        grid-column: 2 / 7;
        grid-row: 2 / 7;
        background-color: #0f172a;
        border: 2px dashed rgba(245, 158, 11, 0.3);
        border-radius: 8px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        color: #fbbf24;
        font-family: monospace;
        font-size: 16px;
        text-align: center;
    }
    
    .balloon-retro {
        background-color: #ffffff !important; border: 2px solid #000000; border-radius: 12px; 
        padding: 12px; color: #000000 !important; box-shadow: 3px 3px 6px rgba(0,0,0,0.3);
        font-size: 14px; margin-bottom: 12px;
    }
    .stButton>button {
        background-color: #ffffff !important; color: #000000 !important;
        border: 1.5px solid #000000 !important; font-weight: bold !important; border-radius: 6px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Mapeamento do anel periférico da Grid 7x7 (24 casas)
GRID_POSITIONS = {
    0: (1, 1), 1: (1, 2), 2: (1, 3), 3: (1, 4), 4: (1, 5), 5: (1, 6), 6: (1, 7),
    7: (2, 7), 8: (3, 7), 9: (4, 7), 10: (5, 7), 11: (6, 7),
    12: (7, 7), 13: (7, 6), 14: (7, 5), 15: (7, 4), 16: (7, 3), 17: (7, 2), 
    18: (7, 1), 19: (6, 1), 20: (5, 1), 21: (4, 1), 22: (3, 1), 23: (2, 1)
}

# Banco de Dados temático focado nos pilares essenciais da NR-1 (GRO, PGR, Direitos, Treinamentos)
TILES_NR1 = [
    {"name": "INTEGRAÇÃO 🚀", "type": "GO", "color": "#ffffff"},
    {"name": "Inventário de Riscos", "cost": 150, "fine": 20, "color": "#fb923c"}, # Laranja GRO
    {"name": "Fiscalização 🔎", "type": "Auditoria", "color": "#9ca3af"},
    {"name": "Critérios de Riscos", "cost": 100, "fine": 10, "color": "#fb923c"},
    {"name": "Multa do MTE ⚠️", "type": "Multa", "color": "#f87171"},
    {"name": "Matriz de Severidade", "cost": 120, "fine": 15, "color": "#fb923c"},
    {"name": "CIPA / NEUTRO 🏢", "type": "Neutro", "color": "#ffffff"},
    {"name": "Plano de Emergência", "cost": 200, "fine": 25, "color": "#34d399"}, # Verde PGR
    {"name": "Simulado Incêndio", "cost": 180, "fine": 20, "color": "#34d399"},
    {"name": "Fiscalização 🔎", "type": "Auditoria", "color": "#9ca3af"},
    {"name": "Análise de Acidentes", "cost": 220, "fine": 30, "color": "#34d399"},
    {"name": "Ações Corretivas", "cost": 240, "fine": 35, "color": "#34d399"},
    {"name": "INTERDIÇÃO ⛔", "type": "Embargo", "color": "#ef4444"},
    {"name": "Treinam. Básico NR1", "cost": 280, "fine": 40, "color": "#60a5fa"}, # Azul Capacitação
    {"name": "Treinam. Periódico", "cost": 300, "fine": 45, "color": "#60a5fa"},
    {"name": "Fiscalização 🔎", "type": "Auditoria", "color": "#9ca3af"},
    {"name": "Material Didático", "cost": 150, "fine": 15, "color": "#60a5fa"},
    {"name": "Avaliação Prática", "cost": 160, "fine": 20, "color": "#60a5fa"},
    {"name": "SESMT / SEGURANÇA 🛡️", "type": "Neutro", "color": "#ffffff"},
    {"name": "Direito de Recusa", "cost": 180, "fine": 20, "color": "#c084fc"}, # Roxo Direitos/Deveres
    {"name": "Ordens de Serviço", "cost": 200, "fine": 25, "color": "#c084fc"},
    {"name": "Fiscalização 🔎", "type": "Auditoria", "color": "#9ca3af"},
    {"name": "Comunicação de Riscos", "cost": 220, "fine": 25, "color": "#c084fc"},
    {"name": "Uso Correto de EPI", "cost": 240, "fine": 30, "color": "#c084fc"}
]


def init_game():
    st.session_state.safe = {
        "pos": [0, 0], # [Jogador, CPU]
        "orcamento": [1500, 1500], # Orçamento disponível para gastar em segurança
        "implementations": {}, # tile_idx -> player_idx (quem implementou a melhoria)
        "log": "SafeTopoly NR-1 iniciado! Implemente o PGR e os programas de capacitação para vencer os riscos e proteger os funcionários.",
        "turn": 0,
        "game_over": False
    }


def play_turn(player_idx: int):
    s = st.session_state.safe
    dado = random.randint(1, 6)
    
    old_pos = s["pos"][player_idx]
    s["pos"][player_idx] = (s["pos"][player_idx] + dado) % len(TILES_NR1)
    curr_pos = s["pos"][player_idx]
    
    # Bônus por ciclo completo (renovação anual do PGR/Orçamento)
    if curr_pos < old_pos:
        s["orcamento"][player_idx] += 250
        s["log"] = "O PGR completou seu ciclo anual de revisão! Sua empresa recebeu uma bonificação orçamentária de $250."

    tile = TILES_NR1[curr_pos]
    p_name = "Você" if player_idx == 0 else "O Bot Auditor"
    msg = f"🎲 {p_name} avançou {dado} posições e avaliou o setor: **{tile['name']}**."

    # Lógica de implementação de melhorias
    if "cost" in tile:
        manager = s["implementations"].get(curr_pos)
        if manager is None:
            if s["orcamento"][player_idx] >= tile["cost"]:
                if player_idx == 0:
                    s["log"] = f"{msg}\n\nEste item da NR-1 não está implementado na empresa. Deseja investir **${tile['cost']}** na implementação para evitar prejuízos futuros?"
                    return # Aguarda clique do botão humano
                else:
                    s["implementations"][curr_pos] = 1
                    s["orcamento"][1] -= tile["cost"]
                    msg += f"\n\n💻 O Bot implementou a melhoria corporativa em **{tile['name']}** por ${tile['cost']}."
            else:
                msg += "\n\nSua empresa não possui caixa disponível para este investimento no momento."
        elif manager == player_idx:
            msg += "\n\nSua empresa já está em total conformidade e protegida neste setor."
        else:
            # Paga multa de passivo trabalhista por o oponente ter implementado antes
            s["orcamento"][player_idx] -= tile["fine"]
            s["orcamento"][manager] += tile["fine"]
            msg += f"\n\n🚨 Falha detectada! O oponente documentou essa conformidade primeiro. Sua empresa sofreu perdas de **${tile['fine']}** devido a passivos trabalhistas."
            
    elif tile["type"] == "Auditoria":
        # Sorte ou revés com terminologia da NR-1
        evento = random.choice([
            ("Seus funcionários identificaram um perigo iminente e usaram o Direito de Recusa corretamente! Ganhou bônus de eficiência de +$100.", 100),
            ("Houve falha na comunicação de riscos das ordens de serviço! Custos adicionais de correção: -$100.", -100),
            ("Sua matriz de riscos do PGR foi elogiada em auditoria externa! Premiação de incentivo: +$150.", 150)
        ])
        s["orcamento"][player_idx] += evento[1]
        msg += f"\n\n🔎 **Relatório de Auditoria:** {evento[0]}"
        
    elif tile["type"] == "Multa":
        s["orcamento"][player_idx] -= 150
        msg += "\n\n⚠️ **Notificação do Ministério do Trabalho:** Falha grave na integração de novos colaboradores. Multa administrativa aplicada: -$150."
        
    elif tile["type"] == "Embargo":
        s["pos"][player_idx] = 6 # Joga para a casa 6 (Prisão / Setor Interditado)
        msg += "\n\n⛔ **EMBARGO E INTERDIÇÃO!** Uma área de alto risco não mitigada causou a paralisação das atividades. Seu peão foi levado para o setor de regularização."

    # Valida falência/término do orçamento
    if s["orcamento"][player_idx] <= 0:
        s["game_over"] = True
        s["log"] = f"{msg}\n\n💀 **FALÊNCIA OPERACIONAL!** A empresa gerida por {p_name} faliu por descumprimento em massa da NR-1 e excesso de passivos judiciais."
        return

    s["log"] = msg
    s["turn"] = 1 - player_idx


# --- RENDERIZAÇÃO DA INTERFACE ---
if "safe" not in st.session_state:
    init_game()
sg = st.session_state.safe

# Loop automático da CPU no background
if sg["turn"] == 1 and not sg["game_over"]:
    play_turn(1)
    st.rerun()

# Painel Superior de Orçamento/Saúde da Empresa
c_hdr = st.columns([1.5, 1.5, 1])
with c_hdr[0]: st.markdown(f"<div class='status-text'>SEU ORÇAMENTO: ${sg['orcamento'][0]}</div>", unsafe_allow_html=True)
with c_hdr[1]: st.markdown(f"<div class='status-text'>ORÇAMENTO RIVAL: ${sg['orcamento'][1]}</div>", unsafe_allow_html=True)
with c_hdr[2]: st.markdown(f"<div class='status-text' style='background-color:#1e3a8a;'>TURNO: {'Sua Vez' if sg['turn'] == 0 else 'Auditor jogando...'}</div>", unsafe_allow_html=True)

st.markdown("<br/>", unsafe_allow_html=True)

col_board, col_panel = st.columns([2.2, 1.8])

with col_board:
    # --- CONSTRUÇÃO DO ANEL QUADRADO NR-1 (7x7) ---
    html_tiles = ""
    for idx, t in enumerate(TILES_NR1):
        row, col = GRID_POSITIONS[idx]
        
        # Marcadores visuais dos peões de técnicos de segurança
        peoes = ""
        if sg["pos"][0] == idx: peoes += "🦺" # Humano
        if sg["pos"][1] == idx: peoes += "🤖" # Bot
        
        # Exibe o selo de qual empresa detém a conformidade daquele artigo
        dono = ""
        if idx in sg["implementations"]:
            dono = " [VOCÊ]" if sg["implementations"][idx] == 0 else " [RIVAL]"
            
        html_tiles += f"""
        <div class='tile-square' style='grid-column: {col}; grid-row: {row}; background-color: {t['color']};'>
            <div style='font-size: 7.5px; font-weight:bold; line-height: 1.1;'>{t['name']}{dono}</div>
            <div style='font-size: 14px; margin: 1px 0;'>{peoes}</div>
            <div style='font-size: 8px; color: rgba(0,0,0,0.6);'>
                {f"Custo: ${t['cost']}" if 'cost' in t else 'Diretriz'}
            </div>
        </div>
        """
        
    html_center = """
    <div class='board-center'>
        <b style='letter-spacing:2px; color:#fbbf24; font-size:18px;'>SAFETOPOLY</b><br/>
        <span style='font-size:11px; color:#94a3b8;'>Gestão de Riscos NR-1</span>
    </div>
    """
    
    st.markdown(f"<div class='banco-grid'>{html_tiles}{html_center}</div>", unsafe_allow_html=True)

with col_panel:
    st.markdown(f"<div class='balloon-retro' style='min-height:160px;'><b>📜 Diário de Bordo & Auditorias (NR-1):</b><br/><br/>{sg['log']}</div>", unsafe_allow_html=True)
    
    active_human = (sg["turn"] == 0 and not sg["game_over"])
    pending_decision = "Deseja comprar?" in sg["log"] or "Deseja investir" in sg["log"]
    
    c_btns = st.columns(2)
    with c_btns[0]:
        if st.button("🎲 REALIZAR INSPEÇÃO (DADO)", disabled=not active_human or pending_decision, use_container_width=True):
            play_turn(0)
            st.rerun()
            
    if pending_decision and active_human:
        with c_btns[0]:
            if st.button("👍 Sim, Investir em Conformidade", use_container_width=True):
                curr_p = sg["pos"][0]
                sg["implementations"][curr_p] = 0
                sg["orcamento"][0] -= TILES_NR1[curr_p]["cost"]
                sg["log"] = f"Ótima decisão! Setor **{TILES_NR1[curr_p]['name']}** regularizado com sucesso. Mitigação ativa!"
                sg["turn"] = 1
                st.rerun()
        with c_btns[1]:
            if st.button("👎 Não, Assumir o Risco", use_container_width=True):
                sg["log"] = "Você optou por adiar o investimento de mitigação. Cuidado com as auditorias fiscais!"
                sg["turn"] = 1
                st.rerun()
                
    st.markdown("<br/><br/>", unsafe_allow_html=True)
    if st.button("Reiniciar Treinamento Prático", use_container_width=True):
        init_game()
        st.rerun()

if sg["game_over"] and sg["orcamento"][0] > 0:
    st.balloons()
