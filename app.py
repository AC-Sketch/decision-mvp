import random
import streamlit as st

# =========================================================
# BANCO IMOBILIÁRIO RETRÔ - TABULEIRO QUADRADO REAL (7x7)
# Circuito expandido para 24 casas (6 por linha/coluna)
# =========================================================

st.set_page_config(page_title="Mister Boardgames", page_icon="🎲", layout="wide")

# --- INTERFACE DE ALTO CONTRASTE E CONFIGURAÇÃO DA GRID 7x7 ---
st.markdown("""
    <style>
    .stApp { background-color: #1a4a2b !important; }
    .block-container { padding: 0.5rem 2rem 0rem 2rem !important; }
    header, footer { visibility: hidden; }
    hr { margin: 0.4rem 0 !important; border-color: rgba(255,255,255,0.2) !important; }

    .status-text {
        color: #ffffff !important;
        font-family: 'Courier New', Courier, monospace;
        font-weight: bold;
        font-size: 15px;
        text-align: center;
        background-color: rgba(0,0,0,0.7);
        padding: 6px 12px;
        border-radius: 6px;
        margin: 0px;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    /* MALHA DO TABULEIRO EXPANDIDA PARA 7 COLUNAS X 7 LINHAS */
    .banco-grid {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        grid-template-rows: repeat(7, 1fr);
        gap: 6px;
        max-width: 680px;
        margin: 0 auto;
        background-color: #11331c;
        padding: 12px;
        border-radius: 10px;
        border: 3px solid #000000;
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
    
    /* Centro vazio gigante ocupando da coluna 2 à 6 e linha 2 à 6 */
    .board-center {
        grid-column: 2 / 7;
        grid-row: 2 / 7;
        background-color: #1a4a2b;
        border: 2px dashed rgba(255,255,255,0.15);
        border-radius: 8px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        color: #7ca982;
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

# Mapeamento do anel de 24 casas ao redor da Grid 7x7 (6 casas reais em cada lado limpando as quinas)
GRID_POSITIONS = {
    0: (1, 1), 1: (1, 2), 2: (1, 3), 3: (1, 4), 4: (1, 5), 5: (1, 6), 6: (1, 7),  # Linha Superior (0 a 6)
    7: (2, 7), 8: (3, 7), 9: (4, 7), 10: (5, 7), 11: (6, 7), 12: (4, 7),          # Ajuste lateral direito
    12: (7, 7), 13: (7, 6), 14: (7, 5), 15: (7, 4), 16: (7, 3), 17: (7, 2), 18: (7, 1), # Linha Inferior
    19: (6, 1), 20: (5, 1), 21: (4, 1), 22: (3, 1), 23: (2, 1)                    # Lateral Esquerda subindo
}

# Consertando os índices remanescentes da descida e subida da matriz 7x7
GRID_POSITIONS = {
    0: (1, 1), 1: (1, 2), 2: (1, 3), 3: (1, 4), 4: (1, 5), 5: (1, 6), 6: (1, 7),
    7: (2, 7), 8: (3, 7), 9: (4, 7), 10: (5, 7), 11: (6, 7),
    12: (7, 7), 13: (7, 6), 14: (7, 5), 15: (7, 4), 16: (7, 3), 17: (7, 2), 18: (4, 1),
    18: (7, 1), 19: (6, 1), 20: (5, 1), 21: (4, 1), 22: (3, 1), 23: (2, 1)
}

TILES_BANCO = [
    {"name": "PARTIDA", "type": "GO", "color": "#ffffff"},
    {"name": "LEBLON", "price": 100, "rent": 10, "color": "#f87171"},
    {"name": "SORTE/REVÉS", "type": "Sorte", "color": "#fbbf24"},
    {"name": "VIEIRA SOUTO", "price": 120, "rent": 12, "color": "#f87171"},
    {"name": "IMPOSTO", "type": "Taxa", "color": "#9ca3af"},
    {"name": "NOSSA SRA", "price": 140, "rent": 15, "color": "#f87171"},
    {"name": "PRISÃO", "type": "Neutro", "color": "#ffffff"},
    {"name": "AV. PAULISTA", "price": 200, "rent": 20, "color": "#60a5fa"},
    {"name": "SORTE/REVÉS", "type": "Sorte", "color": "#fbbf24"},
    {"name": "AV. BRIGADEIRO", "price": 240, "rent": 24, "color": "#60a5fa"},
    {"name": "COMP. FORÇA", "price": 150, "rent": 30, "color": "#e9d5ff"},
    {"name": "AV. REBOUÇAS", "price": 260, "rent": 26, "color": "#60a5fa"},
    {"name": "VÁ P/ PRISÃO", "type": "VáPrisão", "color": "#ef4444"},
    {"name": "MORUMBI", "price": 300, "rent": 32, "color": "#34d399"},
    {"name": "SORTE/REVÉS", "type": "Sorte", "color": "#fbbf24"},
    {"name": "INTERLAGOS", "price": 320, "rent": 36, "color": "#34d399"},
    {"name": "TAXA LUCROS", "type": "Taxa", "color": "#9ca3af"},
    {"name": "IBIRAPUERA", "price": 350, "rent": 40, "color": "#34d399"},
    {"name": "PARADA LIVRE", "type": "Neutro", "color": "#ffffff"},
    {"name": "MINAS GERAIS", "price": 180, "rent": 18, "color": "#fb923c"},
    {"name": "SORTE/REVÉS", "type": "Sorte", "color": "#fbbf24"},
    {"name": "AV. PARANÁ", "price": 200, "rent": 20, "color": "#fb923c"},
    {"name": "COMP. ÁGUA", "price": 150, "rent": 30, "color": "#e9d5ff"},
    {"name": "REPUBLICA", "price": 220, "rent": 22, "color": "#fb923c"}
]


def init_banco():
    st.session_state.banco = {
        "pos": [0, 0], 
        "capital": [1500, 1500],
        "properties": {}, 
        "log": "Tabuleiro expandido profissional (24 casas)! Cada linha e coluna possui 6 casas reais. Role os dados!",
        "turn": 0, 
        "game_over": False
    }


def play_banco_turn(player_idx: int):
    b = st.session_state.banco
    dado = random.randint(1, 6)
    
    old_pos = b["pos"][player_idx]
    b["pos"][player_idx] = (b["pos"][player_idx] + dado) % len(TILES_BANCO)
    curr_pos = b["pos"][player_idx]
    
    if curr_pos < old_pos:
        b["capital"][player_idx] += 200
        b["log"] = "Passou pela linha de partida e faturou um dividendo de $200!"

    tile = TILES_BANCO[curr_pos]
    p_name = "Você" if player_idx == 0 else "A CPU"
    msg_action = f"🎲 {p_name} mandou o peão avançar {dado} casas e parou em **{tile['name']}**."

    if "price" in tile:
        owner = b["properties"].get(curr_pos)
        if owner is None:
            if b["capital"][player_idx] >= tile["price"]:
                if player_idx == 0:
                    b["log"] = f"{msg_action}\n\nTítulo imobiliário livre por **${tile['price']}**. Deseja comprar?"
                    return 
                else:
                    b["properties"][curr_pos] = 1
                    b["capital"][1] -= tile["price"]
                    msg_action += f"\n\n💻 A CPU investiu e comprou {tile['name']} por ${tile['price']}!"
            else:
                msg_action += "\n\nSaldo em caixa insuficiente para essa aquisição."
        elif owner == player_idx:
            msg_action += "\n\nVocê já detém as ações desta localidade."
        else:
            b["capital"][player_idx] -= tile["rent"]
            b["capital"][owner] += tile["rent"]
            msg_action += f"\n\n💸 Parada com custo! Pagou **${tile['rent']}** de aluguel ao proprietário."
            
    elif tile["type"] == "Sorte":
        efeito = random.choice([
            ("Retorno de dividendos de fundos!", 150),
            ("Cobrança de seguro automotivo!", -100),
            ("Prêmio de loteria regional!", 200),
            ("Reparos urgentes de encanamento!", -50)
        ])
        b["capital"][player_idx] += efeito[1]
        msg_action += f"\n\n🍀 CARTÃO DE SORTE OU REVÉS: {efeito[0]} (${efeito[1]})"
    elif tile["type"] == "Taxa":
        b["capital"][player_idx] -= 150
        msg_action += "\n\n⚠️ Imposto sobre Propriedade Territorial Urbana! Recolhido -$150."
    elif tile["type"] == "VáPrisão":
        b["pos"][player_idx] = 6  # Casa número 6 é a prisão de visitas
        msg_action += "\n\n👮 Mandado de prisão! O peão foi recolhido imediatamente."

    if b["capital"][player_idx] <= 0:
        b["game_over"] = True
        b["log"] = f"{msg_action}\n\n💀 FALÊNCIA GERAL! O mercado engoliu as economias de {p_name}!"
        return

    b["log"] = msg_action
    b["turn"] = 1 - player_idx


# --- COMPONENTES DE INTERFACE ---
st.markdown("<h2 style='text-align: center; color: white; font-family: monospace; letter-spacing: 2px;'>🎩 MISTER MONOPOLY PRO</h2>", unsafe_allow_html=True)
st.markdown("<hr/>", unsafe_allow_html=True)

if "banco" not in st.session_state: 
    init_banco()
bg = st.session_state.banco

if bg["turn"] == 1 and not bg["game_over"]:
    play_banco_turn(1)
    st.rerun()

# Painel de Status
c_bc = st.columns([1.5, 1.5, 1])
with c_bc[0]: st.markdown(f"<div class='status-text'>SEU PATRIMÔNIO: ${bg['capital'][0]}</div>", unsafe_allow_html=True)
with c_bc[1]: st.markdown(f"<div class='status-text'>PATRIMÔNIO CPU: ${bg['capital'][1]}</div>", unsafe_allow_html=True)
with c_bc[2]: st.markdown(f"<div class='status-text' style='background-color:#11331c;'>RODADA: {'Seu Turno' if bg['turn'] == 0 else 'CPU operando...'}</div>", unsafe_allow_html=True)

st.markdown("<br/>", unsafe_allow_html=True)

col_board, col_panel = st.columns([2.2, 1.8])

with col_board:
    # --- CONSTRUÇÃO DO ANEL QUADRADO REAL 7x7 ---
    html_tiles = ""
    for idx, t in enumerate(TILES_BANCO):
        row, col = GRID_POSITIONS[idx]
        
        peoes = ""
        if bg["pos"][0] == idx: peoes += "🤠"
        if bg["pos"][1] == idx: peoes += "💻"
        
        dono_lbl = ""
        if idx in bg["properties"]:
            dono_lbl = " [M]" if bg["properties"][idx] == 0 else " [C]"
            
        html_tiles += f"""
        <div class='tile-square' style='grid-column: {col}; grid-row: {row}; background-color: {t['color']};'>
            <div style='font-size: 8px; font-weight:bold; line-height: 1.1;'>{t['name']}{dono_lbl}</div>
            <div style='font-size: 15px; margin: 1px 0;'>{peoes}</div>
            <div style='font-size: 8px; color: rgba(0,0,0,0.6);'>
                {f"${t['price']}" if 'price' in t else 'Ação'}
            </div>
        </div>
        """
        
    html_center = """
    <div class='board-center'>
        <b style='letter-spacing:3px; color:white; font-size:20px;'>MONOPOLY</b><br/>
        <span style='font-size:11px; color:#a7f3d0;'>Circuito Real 24 Casas</span>
    </div>
    """
    
    st.markdown(f"<div class='banco-grid'>{html_tiles}{html_center}</div>", unsafe_allow_html=True)

with col_panel:
    st.markdown(f"<div class='balloon-retro' style='min-height:160px;'><b>📜 Relatório da Bolsa de Valores:</b><br/><br/>{bg['log']}</div>", unsafe_allow_html=True)
    
    is_human_active = (bg["turn"] == 0 and not bg["game_over"])
    is_decision_pending = "Deseja comprar?" in bg["log"]
    
    c_btns = st.columns(2)
    with c_btns[0]:
        if st.button("🎲 LANÇAR DADOS", disabled=not is_human_active or is_decision_pending, use_container_width=True):
            play_banco_turn(0)
            st.rerun()
            
    if is_decision_pending and is_human_active:
        with c_btns[0]:
            if st.button("👍 Sim, Adquirir Título", use_container_width=True):
                curr_p = bg["pos"][0]
                bg["properties"][curr_p] = 0
                bg["capital"][0] -= TILES_BANCO[curr_p]["price"]
                bg["log"] = f"Parabéns! Você assinou as escrituras e comprou {TILES_BANCO[curr_p]['name']}."
                bg["turn"] = 1
                st.rerun()
        with c_btns[1]:
            if st.button("👎 Não, Rejeitar Oferta", use_container_width=True):
                bg["log"] = "Você rejeitou a proposta para reter liquidez em caixa."
                bg["turn"] = 1
                st.rerun()
                
    st.markdown("<br/><br/>", unsafe_allow_html=True)
    if st.button("Reiniciar Toda a Mesa", use_container_width=True):
        init_banco()
        st.rerun()

if bg["game_over"] and bg["capital"][0] > 0:
    st.balloons()
