import random
import streamlit as st

# =========================================================
# CENTRAL DE TABULEIROS RETRÔ: BANCO IMOBILIÁRIO & LUDO
# Lógica estável por eventos e persistência de dados
# =========================================================

st.set_page_config(page_title="Mister Boardgames", page_icon="🎲", layout="wide")

# --- CUSTOMIZAÇÃO VISUAL RETRÔ ---
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
    
    .board-tile {
        color: black !important;
        text-align: center;
        padding: 8px;
        border-radius: 6px;
        border: 2px solid #000000;
        font-weight: bold;
        font-size: 12px;
        min-height: 75px;
        box-shadow: 2px 2px 4px rgba(0,0,0,0.3);
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


# =========================================================
# CORE LOGIC: BANCO IMOBILIÁRIO SIMPLIFICADO
# =========================================================
TILES_BANCO = [
    {"name": "Partida", "type": "GO", "color": "#ffffff"},
    {"name": "Leblon", "price": 100, "rent": 10, "color": "#f87171"},
    {"name": "Sorte ou Revés", "type": "Sorte", "color": "#fbbf24"},
    {"name": "Av. Vieira Souto", "price": 120, "rent": 12, "color": "#f87171"},
    {"name": "Imposto de Renda", "type": "Taxa", "color": "#9ca3af"},
    {"name": "Prisão (Visita)", "type": "Neutro", "color": "#ffffff"},
    {"name": "Av. Paulista", "price": 200, "rent": 20, "color": "#60a5fa"},
    {"name": "Sorte ou Revés", "type": "Sorte", "color": "#fbbf24"},
    {"name": "Av. Brigadeiro", "price": 240, "rent": 24, "color": "#60a5fa"},
    {"name": "Vá para a Prisão", "type": "VáPrisão", "color": "#ef4444"}
]

def init_banco():
    st.session_state.banco = {
        "pos": [0, 0], # [Jogador, CPU]
        "capital": [1500, 1500],
        "properties": {}, # tile_idx -> owner_idx (0 ou 1)
        "log": "O tabuleiro está montado. Cada jogador começa com $1500. Role os dados!",
        "turn": 0, # 0 = Jogador, 1 = CPU
        "game_over": False
    }

def play_banco_turn(player_idx: int):
    b = st.session_state.banco
    dado = random.randint(1, 6)
    
    # Movimentação no tabuleiro circular
    b["pos"][player_idx] = (b["pos"][player_idx] + dado) % len(TILES_BANCO)
    curr_pos = b["pos"][player_idx]
    tile = TILES_BANCO[curr_pos]
    
    p_name = "Você" if player_idx == 0 else "A CPU"
    msg_action = f"🎲 {p_name} rolou {dado} e parou em **{tile['name']}**."

    # Processamento de regras de compra e taxas
    if "price" in tile:
        owner = b["properties"].get(curr_pos)
        if owner is None:
            # Disponível para compra
            if b["capital"][player_idx] >= tile["price"]:
                if player_idx == 0:
                    # Guardamos para decisão manual na interface
                    b["log"] = f"{msg_action}\n\nEsta propriedade está disponível por **${tile['price']}**. Deseja comprar?"
                    return # Para a execução para o humano decidir
                else:
                    # CPU compra agressivamente
                    b["properties"][curr_pos] = 1
                    b["capital"][1] -= tile["price"]
                    msg_action += f"\n\n💻 A CPU comprou esta propriedade por ${tile['price']}!"
            else:
                msg_action += "\n\nSaldo insuficiente para comprar."
        elif owner == player_idx:
            msg_action += "\n\nA propriedade já pertence a você."
        else:
            # Paga aluguel
            b["capital"][player_idx] -= tile["rent"]
            b["capital"][owner] += tile["rent"]
            msg_action += f"\n\n💸 Parou na propriedade do adversário! Pagou **${tile['rent']}** de aluguel."
            
    elif tile["type"] == "Sorte":
        efeito = random.choice([("Ganhou bônus de ações!", 50), ("Perdeu na bolsa!", -50)])
        b["capital"][player_idx] += efeito[1]
        msg_action += f"\n\n🍀 Sorte ou Revés: {efeito[0]} (${efeito[1]})"
    elif tile["type"] == "Taxa":
        b["capital"][player_idx] -= 100
        msg_action += "\n\n⚠️ Pagou $100 de impostos ao banco."
    elif tile["type"] == "VáPrisão":
        b["pos"][player_idx] = 5 # Posição da prisão de visitas
        msg_action += "\n\n👮 Alerta! Foi enviado diretamente para a Prisão!"

    # Verifica falência
    if b["capital"][player_idx] <= 0:
        b["game_over"] = True
        b["log"] = f"{msg_action}\n\n💀 FIM DE JOGO! {p_name} faliu!"
        return

    b["log"] = msg_action
    b["turn"] = 1 - player_idx


# =========================================================
# CORE LOGIC: LUDO SIMPLIFICADO DE CORRIDA
# =========================================================
def init_ludo():
    st.session_state.ludo = {
        "pos": [0, 0], # [Jogador, CPU] - Posição de 0 a 15 (Fim)
        "log": "Peões na linha de largada. Role um 6 para sair ou avance diretamente!",
        "turn": 0,
        "winner": None
    }

def play_ludo_turn(player_idx: int):
    l = st.session_state.ludo
    dado = random.randint(1, 6)
    
    p_name = "Você" if player_idx == 0 else "A CPU"
    msg = f"🎲 {p_name} rolou {dado}."

    # Lógica de movimentação direta baseada em trilha estática
    l["pos"][player_idx] += dado
    
    if l["pos"][player_idx] >= 15:
        l["pos"][player_idx] = 15
        l["winner"] = player_idx
        l["log"] = f"{msg} Chegou na **Casa 15 (Meta Final)**! 🏆 {p_name} venceu a corrida do Ludo!"
        return

    # Regra clássica de Ludo: Cair na mesma casa do adversário "come" o peão
    opp_idx = 1 - player_idx
    if l["pos"][player_idx] == l["pos"][opp_idx] and l["pos"][player_idx] != 0:
        l["pos"][opp_idx] = 0
        msg += f"\n\n💥 PEÃO CAPTURADO! {p_name} caiu na mesma casa e mandou o peão adversário de volta para o Início!"

    l["log"] = f"{msg} Avançou para a **Casa {l['pos'][player_idx]}**."
    l["turn"] = 1 - opp_idx


# --- BARRA SUPERIOR DE CRIAÇÃO DO MENU ---
game_select = st.selectbox("🎮 SELECIONE O JOGO DE TABULEIRO PARA RODAR:", ["🎩 Banco Imobiliário", "🏁 Ludo Corrida Retrô"])
st.markdown("<hr/>", unsafe_allow_html=True)


# ----------------- GAME: BANCO IMOBILIÁRIO -----------------
if game_select == "🎩 Banco Imobiliário":
    if "banco" not in st.session_state: init_banco()
    bg = st.session_state.banco

    # Loop automático do turno da CPU para sincronia estável
    if bg["turn"] == 1 and not bg["game_over"]:
        play_banco_turn(1)
        st.rerun()

    # Indicadores superiores de Dinheiro
    c_bc = st.columns([1.5, 1.5, 1])
    with c_bc[0]: st.markdown(f"<div class='status-text'>SEU CAPITAL: ${bg['capital'][0]}</div>", unsafe_allow_html=True)
    with c_bc[1]: st.markdown(f"<div class='status-text'>CAPITAL CPU: ${bg['capital'][1]}</div>", unsafe_allow_html=True)
    with c_bc[2]: st.markdown(f"<div class='status-text' style='background-color:#11331c;'>TURNO: {'Sua Vez' if bg['turn'] == 0 else 'CPU...'}</div>", unsafe_allow_html=True)
    st.markdown("<br/>", unsafe_allow_html=True)

    col_board, col_panel = st.columns([3, 1])

    with col_board:
        # Renderização visual horizontal das casas do Banco Imobiliário
        st.markdown("<p style='color: white; font-weight: bold; margin: 0;'>Casas do Tabuleiro:</p>", unsafe_allow_html=True)
        cols_tiles = st.columns(len(TILES_BANCO))
        for idx, t in enumerate(TILES_BANCO):
            with cols_tiles[idx]:
                # Monta marcadores textuais de quem está na casa
                peoes = ""
                if bg["pos"][0] == idx: peoes += "🤠"
                if bg["pos"][1] == idx: peoes += "💻"
                
                dono = "Livre"
                if idx in bg["properties"]: dono = "Você" if bg["properties"][idx] == 0 else "CPU"
                info_prop = f"<br/><small>{dono}</small>" if "price" in t else ""
                
                st.markdown(f"""
                    <div class='board-tile' style='background-color: {t['color']};'>
                        <span style='font-size:10px;'>{t['name']}</span><br/>
                        <span style='font-size:14px;'>{peoes}</span>
                        {info_prop}
                    </div>
                """, unsafe_allow_html=True)

        st.markdown("<br/><br/>", unsafe_allow_html=True)

        # Botões de Ação do Humano
        is_human_active = (bg["turn"] == 0 and not bg["game_over"])
        is_decision_pending = "Deseja comprar?" in bg["log"]
        
        c_btns = st.columns([1, 1, 2])
        with c_btns[0]:
            if st.button("🎲 ROLAR DADOS", disabled=not is_human_active or is_decision_pending, use_container_width=True):
                play_banco_turn(0)
                st.rerun()
        
        # Sub-botões caso caia em propriedade livre
        if is_decision_pending and is_human_active:
            with c_btns[0]:
                if st.button("👍 Sim, Comprar", use_container_width=True):
                    curr_p = bg["pos"][0]
                    bg["properties"][curr_p] = 0
                    bg["capital"][0] -= TILES_BANCO[curr_p]["price"]
                    bg["log"] = f"Você comprou {TILES_BANCO[curr_p]['name']}!"
                    bg["turn"] = 1
                    st.rerun()
            with c_btns[1]:
                if st.button("👎 Não, Passar", use_container_width=True):
                    bg["log"] = "Você recusou a compra."
                    bg["turn"] = 1
                    st.rerun()

    with col_panel:
        st.markdown(f"<div class='balloon-retro' style='min-height:120px;'><b>📜 Escrituras & Relatórios:</b><br/>{bg['log']}</div>", unsafe_allow_html=True)
        if st.button("Resetar Banco Imobiliário", use_container_width=True):
            init_banco()
            st.rerun()


# ----------------- GAME: LUDO CORRIDA -----------------
elif game_select == "🏁 Ludo Corrida Retrô":
    if "ludo" not in st.session_state: init_ludo()
    lg = st.session_state.ludo

    # Loop estável da CPU
    if lg["turn"] == 1 and lg["winner"] is None:
        play_ludo_turn(1)
        st.rerun()

    # Placar Fixo
    c_lc = st.columns([1.5, 1.5, 1])
    with c_lc[0]: st.markdown(f"<div class='status-text'>SUA CASA: {lg['pos'][0]} / 15</div>", unsafe_allow_html=True)
    with c_lc[1]: st.markdown(f"<div class='status-text'>CASA CPU: {lg['pos'][1]} / 15</div>", unsafe_allow_html=True)
    with c_lc[2]: st.markdown(f"<div class='status-text' style='background-color:#11331c;'>VEZ: {'Você' if lg['turn'] == 0 else 'CPU...'}</div>", unsafe_allow_html=True)
    st.markdown("<hr/>", unsafe_allow_html=True)

    col_l_board, col_l_panel = st.columns([3, 1])

    with col_l_board:
        # Trilho linear do Ludo de 0 a 15
        st.markdown("<p style='color: white; font-weight: bold; margin: 0;'>Trilha de Corrida (Ludo):</p>", unsafe_allow_html=True)
        cols_track = st.columns(16)
        for step in range(16):
            with cols_track[step]:
                peoes_ludo = ""
                if lg["pos"][0] == step: peoes_ludo += "🤠"
                if lg["pos"][1] == step: peoes_ludo += "💻"
                
                bg_color = "#ffffff"
                if step == 0: bg_color = "#9ca3af" # Início
                if step == 15: bg_color = "#fde047" # Fim
                
                st.markdown(f"""
                    <div class='board-tile' style='background-color: {bg_color}; min-height:60px;'>
                        <span style='font-size:9px;'>C{step}</span><br/>
                        <span style='font-size:16px;'>{peoes_ludo}</span>
                    </div>
                """, unsafe_allow_html=True)

        st.markdown("<br/><br/>", unsafe_allow_html=True)
        if st.button("🎲 JOGAR DADO DO LUDO", disabled=lg["turn"] != 0 or lg["winner"] is not None, use_container_width=True):
            play_ludo_turn(0)
            st.rerun()

    with col_l_panel:
        st.markdown(f"<div class='balloon-retro' style='min-height:120px;'><b>💬 Mural de Corrida:</b><br/>{lg['log']}</div>", unsafe_allow_html=True)
        if st.button("Reiniciar Corrida Ludo", use_container_width=True):
            init_ludo()
            st.rerun()

if ("banco" in st.session_state and st.session_state.banco["game_over"] and st.session_state.banco["capital"][0] > 0) or ("ludo" in st.session_state and st.session_state.ludo["winner"] == 0):
    st.balloons()
