import random
import streamlit as st
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple

# =========================================================
# CENTRAL DE JOGOS RETRÔ - MISTER TRUCO, RPG & MINAS
# Arquitetura modular estável por funções puras
# =========================================================

st.set_page_config(page_title="Coletânea 1000 Jogos Retrô", page_icon="🕹️", layout="wide")

# --- ESTILIZAÇÃO CSS RETRÔ CENTRALIZADA ---
st.markdown("""
    <style>
    .stApp { background-color: #1a4a2b !important; }
    .block-container { padding: 0.5rem 2rem 0rem 2rem !important; }
    header, footer { visibility: hidden; }
    hr { margin: 0.4rem 0 !important; border-color: rgba(255,255,255,0.2) !important; }

    /* Estilo Geral de Status */
    .status-text {
        color: #ffffff !important; font-family: 'Courier New', Courier, monospace; font-weight: bold; font-size: 14px;
        text-align: center; background-color: rgba(0,0,0,0.7); padding: 5px 12px; border-radius: 6px; margin: 0px;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    /* Cartas do Truco */
    .card-back {
        border: 2px solid #ffffff; border-radius: 6px; background-color: #11331c;
        background-image: repeating-linear-gradient(45deg, #1e4a2b 0, #1e4a2b 2px, transparent 0, transparent 50%);
        background-size: 8px 8px; height: 85px; max-width: 62px; margin: 0 auto;
        display: flex; align-items: center; justify-content: center; color: #559966; font-size: 20px; font-weight: bold;
    }
    .card-played {
        border: 2px solid #000000 !important; border-radius: 8px !important; background-color: #ffffff !important;
        color: #000000 !important; height: 100px; max-width: 75px; margin: 0 auto 4px auto;
        display: flex; flex-direction: column; align-items: center; justify-content: center; font-size: 22px; font-weight: bold;
    }
    .card-center {
        border: 2px solid #ffffff !important; border-radius: 8px !important; background-color: #ffffff !important;
        color: #000000 !important; height: 85px; width: 62px; margin: 0 auto;
        display: flex; flex-direction: column; align-items: center; justify-content: center; font-size: 20px; font-weight: bold;
    }
    .red-suit { color: #dc2626 !important; font-size: 28px; line-height: 1; }
    .black-suit { color: #000000 !important; font-size: 28px; line-height: 1; }
    
    /* Caixa de Diálogo / Narrativa */
    .balloon-retro {
        background-color: #ffffff !important; border: 2px solid #000000; border-radius: 8px; 
        padding: 10px; color: #000000 !important; box-shadow: 3px 3px 6px rgba(0,0,0,0.3); font-size: 13px;
    }
    
    /* Botões Globais */
    .stButton>button {
        background-color: #ffffff !important; color: #000000 !important;
        border: 1.5px solid #000000 !important; font-weight: bold !important; border-radius: 6px !important;
    }
    </style>
""", unsafe_allow_html=True)


# =========================================================
# OPERAÇÃO DE VARIÁVEIS DO TRUCO
# =========================================================
SUITS_MAP = {"Ouros": "♦", "Espadas": "♠", "Copas": "♥", "Paus": "♣"}
SUIT_COLORS = {"Ouros": "red-suit", "Espadas": "black-suit", "Copas": "red-suit", "Paus": "black-suit"}
ORDER_MANILHA_NOVA = ["4", "5", "6", "7", "Q", "J", "K", "A", "2", "3"]

@dataclass
class Card:
    rank: str
    suit: str
    @property
    def symbol(self) -> str: return SUITS_MAP[self.suit]
    @property
    def color(self) -> str: return SUIT_COLORS[self.suit]
    @property
    def label(self) -> str: return f"{self.rank}{self.symbol}"

def get_card_power(card: Card, mode: str, vira: Optional[Card]) -> int:
    if mode == "Manilha Velha":
        if card.rank == "4" and card.suit == "Paus": return 104
        if card.rank == "7" and card.suit == "Copas": return 103
        if card.rank == "A" and card.suit == "Espadas": return 102
        if card.rank == "7" and card.suit == "Ouros": return 101
        order = ["Q", "J", "K", "A", "2", "3"]
        return order.index(card.rank) if card.rank in order else -1
    else:
        if vira is None: return 0
        next_rank = ORDER_MANILHA_NOVA[(ORDER_MANILHA_NOVA.index(vira.rank) + 1) % len(ORDER_MANILHA_NOVA)]
        if card.rank == next_rank:
            suit_pow = {"Ouros": 1, "Espadas": 2, "Copas": 3, "Paus": 4}
            return 100 + suit_pow.get(card.suit, 0)
        return ORDER_MANILHA_NOVA.index(card.rank)

def start_truco_hand(g: dict):
    suits = ["Ouros", "Espadas", "Copas", "Paus"]
    if g["mode"] == "Manilha Velha":
        deck = [Card(r, s) for r in ["3", "2", "A", "K", "J", "Q"] for s in suits]
        deck += [Card("4", "Paus"), Card("7", "Copas"), Card("A", "Espadas"), Card("7", "Ouros")]
    else:
        deck = [Card(r, s) for r in ORDER_MANILHA_NOVA for s in suits]
    random.shuffle(deck)
    g["hands"] = [[] for _ in range(g["n_players"])]
    for _ in range(3):
        for p in range(g["n_players"]): g["hands"][p].append(deck.pop())
    g["vira"] = deck.pop() if g["mode"] == "Manilha Nova" else None
    g["table"] = {}
    g["trick_no"] = 1
    g["hand_points"] = 1
    g["trick_wins"] = []
    g["finished_hand"] = False
    g["pending_truco"] = None
    g["turn"] = (g["dealer"] + 1) % g["n_players"]
    g["message"] = f"Nova rodada! Jogador {g['turn']} começa jogando."

def process_truco_victory(g: dict):
    players_in_trick = list(g["table"].keys())
    powers = [get_card_power(g["table"][p], g["mode"], g["vira"]) for p in players_in_trick]
    max_pow = max(powers)
    winners = [players_in_trick[i] for i, pow_val in enumerate(powers) if pow_val == max_pow]
    is_tie = len(winners) > 1 and len({w % 2 for w in winners}) > 1
    if is_tie:
        g["trick_wins"].append(-1)
        next_puller = winners[0]
        g["message"] = "Empatou! Quem amarrou joga primeiro."
    else:
        next_puller = winners[powers.index(max_pow)]
        g["trick_wins"].append(next_puller % 2)
        g["message"] = f"Jogador {next_puller} ganhou a vaza."
    tw = g["trick_wins"]
    hand_winner = None
    if tw.count(0) == 2: hand_winner = 0
    elif tw.count(1) == 2: hand_winner = 1
    elif len(tw) == 2 and tw[0] == -1 and tw[1] != -1: hand_winner = tw[1]
    elif len(tw) == 2 and tw[0] != -1 and tw[1] == -1: hand_winner = tw[0]
    elif len(tw) == 3: hand_winner = tw[0] if (tw[2] == -1 and tw[0] != -1) else (0 if tw[2] == -1 else tw[2])
    if hand_winner is not None:
        g["score"][hand_winner] += g["hand_points"]
        g["finished_hand"] = True
        g["message"] = f"Fim da rodada! Vitória do Time {hand_winner + 1} (+{g['hand_points']} pts)."
        g["dealer"] = (g["dealer"] + 1) % g["n_players"]
        return
    g["turn"] = next_puller

def bot_truco_play(g: dict):
    hand = g["hands"][g["turn"]]
    if not hand: return
    hand_powers = [get_card_power(c, g["mode"], g["vira"]) for c in hand]
    if not g["table"]: chosen_idx = hand_powers.index(min(hand_powers))
    else:
        table_max = max([get_card_power(c, g["mode"], g["vira"]) for c in g["table"].values()])
        options = [i for i, p in enumerate(hand_powers) if p > table_max]
        chosen_idx = hand_powers.index(min([hand_powers[o] for o in options])) if options else hand_powers.index(min(hand_powers))
    g["table"][g["turn"]] = g["hands"][g["turn"]].pop(chosen_idx)
    if len(g["table"]) == g["n_players"]: process_truco_victory(g)
    else: g["turn"] = (g["turn"] + 1) % g["n_players"]


# =========================================================
# MOTOR DO CAMPO MINADO (RETRO MINESWEEPER)
# =========================================================
def init_mines():
    grid_size = 5
    num_mines = 4
    board = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
    revealed = [[False for _ in range(grid_size)] for _ in range(grid_size)]
    mines_placed = 0
    while mines_placed < num_mines:
        r, c = random.randint(0, grid_size-1), random.randint(0, grid_size-1)
        if board[r][c] != -1:
            board[r][c] = -1
            mines_placed += 1
    for r in range(grid_size):
        for c in range(grid_size):
            if board[r][c] == -1: continue
            count = 0
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if 0 <= r+dr < grid_size and 0 <= c+dc < grid_size:
                        if board[r+dr][c+dc] == -1: count += 1
            board[r][c] = count
    st.session_state.mines = {"board": board, "revealed": revealed, "status": "Jogando", "safe_clicks": 0}


# =========================================================
# MOTOR DO RPG DE TEXTO (MASMORRA RETRÔ)
# =========================================================
def init_rpg():
    st.session_state.rpg = {
        "vida": 20, "ataque": 4, "ouro": 10, "fase": 1,
        "log": "Você acorda nos portões de uma masmorra escura... Prepare sua espada!",
        "inimigo_vida": 0, "inimigo_nome": "", "status": "Explorando"
    }

def process_rpg_action(action: str):
    r = st.session_state.rpg
    if action == "Explorar":
        evento = random.choice(["Vazio", "Tesouro", "Monstro"])
        if evento == "Vazio":
            r["log"] = "Você caminha por um corredor úmido e silencioso. Nada aqui."
            r["fase"] += 1
        elif evento == "Tesouro":
            ganho = random.randint(5, 15)
            r["ouro"] += ganho
            r["log"] = f"Baú encontrado! Você ganhou {ganho} moedas de ouro."
            r["fase"] += 1
        elif evento == "Monstro":
            monstros = [("Morcego", 6), ("Esqueleto", 10), ("Orc Brutal", 14)]
            nome, m_vida = random.choice(monstros)
            r["inimigo_nome"] = nome
            r["inimigo_vida"] = m_vida
            r["status"] = "Combate"
            r["log"] = f"Um {nome} pulou das sombras! Vida do inimigo: {m_vida}."
    elif action == "Atacar":
        dano_jogador = random.randint(2, r["ataque"])
        dano_inimigo = random.randint(1, 4)
        r["inimigo_vida"] -= dano_jogador
        r["vida"] -= dano_inimigo
        r["log"] = f"Você atacou o {r['inimigo_nome']} causando {dano_jogador} de dano! O monstro te contra-atacou causando {dano_inimigo} de dano."
        if r["inimigo_vida"] <= 0:
            r["status"] = "Explorando"
            r["ouro"] += 5
            r["fase"] += 1
            r["log"] = f"Vitória! Você derrotou o {r['inimigo_nome']} e pilhou 5 moedas de ouro."
        elif r["vida"] <= 0:
            r["status"] = "Game Over"
            r["log"] = f"Você sucumbiu aos ferimentos causados pelo {r['inimigo_nome']}... Fim da sua jornada."


# =========================================================
# FLUXO DE SELEÇÃO DO JOGO (INTERAÇÃO PRINCIPAL)
# =========================================================
game_choice = st.selectbox("💿 SELECIONE O JOGO DO SEU CD-ROM:", ["🃏 Mister Truco", "💣 Campo Minado Retrô", "⚔️ RPG Masmorra de Texto"])
st.markdown("<hr/>", unsafe_allow_html=True)

# ----------------- FLUXO: MISTER TRUCO -----------------
if game_choice == "🃏 Mister Truco":
    c_t1, c_t2, c_t3, c_t4 = st.columns([1, 1.2, 1.2, 0.8])
    with c_top_title: st.markdown("<h4 style='color:white; margin:0;'>MISTER TRUCO</h4>", unsafe_allow_html=True)
    with c_top_players: n_players = st.radio("Jogadores", [2, 4], format_func=lambda x: "1v1 (Dois)" if x == 2 else "2v2 (Quatro)", label_visibility="collapsed")
    with c_top_mode: mode = st.radio("Manilha", ["Manilha Velha", "Manilha Nova"], label_visibility="collapsed")
    with c_top_reset: apply_btn = st.button("Aplicar Regras", use_container_width=True)

    if "truco_state" not in st.session_state or apply_btn or st.session_state.truco_state["mode"] != mode or st.session_state.truco_state["n_players"] != n_players:
        st.session_state.truco_state = {"n_players": n_players, "mode": mode, "score": [0, 0], "dealer": 0, "hands": [], "vira": None, "table": {}, "trick_no": 1, "hand_points": 1, "trick_wins": [], "finished_hand": False, "pending_truco": None, "turn": 0, "message": ""}
        start_truco_hand(st.session_state.truco_state)

    tg = st.session_state.truco_state
    if not tg["finished_hand"] and tg["turn"] != 0:
        bot_truco_play(tg)
        st.rerun()

    # Renderização da Tela do Truco
    st.markdown(f"<div class='status-text'>CPU: {tg['score'][1]}   ▏   JOGADOR: {tg['score'][0]}   ▏   VALENDO: {tg['hand_points']} PTS</div>", unsafe_allow_html=True)
    st.markdown("<div style='margin:10px 0;'></div>", unsafe_allow_html=True)
    
    col_b, col_p = st.columns([2.8, 1.2])
    with col_b:
        # Cartas da CPU
        c_cpu = st.columns([1,1,1,1,1])
        for x in range(min(len(tg["hands"][1]) if tg["n_players"]==2 else len(tg["hands"][1])+len(tg["hands"][3]), 3)):
            with c_cpu[x+1]: st.markdown("<div class='card-back'>R</div>", unsafe_allow_html=True)
        st.markdown("<br/>", unsafe_allow_html=True)
        # Suas Cartas
        c_ply = st.columns([1,1,1,1,1])
        my_turn = (tg["turn"] == 0 and not tg["finished_hand"])
        for idx, card in enumerate(tg["hands"][0]):
            with c_ply[idx+1]:
                st.markdown(f"<div class='card-played'><div style='font-size:16px;'>{card.rank}</div><div class='{card.color}'>{card.symbol}</div></div>", unsafe_allow_html=True)
                if st.button("Jogar", key=f"t_play_{idx}_{card.label}", disabled=not my_turn, use_container_width=True):
                    if len(tg["table"]) == tg["n_players"]: tg["table"] = {}
                    tg["table"][0] = tg["hands"][0].pop(idx)
                    if len(tg["table"]) == tg["n_players"]: process_truco_victory(tg)
                    else: tg["turn"] = (tg["turn"] + 1) % tg["n_players"]
                    st.rerun()
        # Botões de Aposta
        st.markdown("<br/>", unsafe_allow_html=True)
        c_act = st.columns([1, 1, 1, 1])
        if c_act[1].button("TRUCO", disabled=not my_turn or tg["hand_points"]>1, use_container_width=True):
            tg["hand_points"] = 3
            tg["message"] = "Você gritou Truco! A CPU aceitou timidamente."
            st.rerun()
        if c_act[2].button("CORRER", disabled=not my_turn, use_container_width=True):
            tg["score"][1] += tg["hand_points"]
            start_truco_hand(tg)
            st.rerun()
    with col_p:
        st.markdown(f"<div class='balloon-retro'><b>💬 Tabuleiro:</b><br/>{tg['message']}</div>", unsafe_allow_html=True)
        if tg["mode"] == "Manilha Nova" and tg["vira"]:
            st.markdown(f"<div style='color:white; font-size:12px; text-align:center; background:rgba(0,0,0,0.3); padding:4px; border-radius:4px;'>VIRA: {tg['vira'].label}</div>", unsafe_allow_html=True)
        st.markdown("<p style='color:white; font-size:13px; font-weight:bold; margin:5px 0 0 0;'>Mesa:</p>", unsafe_allow_html=True)
        for p, c in tg["table"].items():
            st.markdown(f"<div style='color:white; font-size:13px;'>• Pl{p} jogou: <b>{c.label}</b></div>", unsafe_allow_html=True)
        st.markdown("<br/>", unsafe_allow_html=True)
        if st.button("Avançar Rodada", disabled=not tg["finished_hand"] and len(tg["table"]) != tg["n_players"], use_container_width=True):
            if tg["finished_hand"]: start_truco_hand(tg)
            else: tg["table"] = {}
            st.rerun()

# ----------------- FLUXO: CAMPO MINADO -----------------
elif game_choice == "💣 Campo Minado Retrô":
    if "mines" not in st.session_state: init_mines()
    m = st.session_state.mines
    
    st.markdown(f"<div class='status-text'>STATUS: {m['status'].upper()} ▏ Cuidado onde clica!</div>", unsafe_allow_html=True)
    st.markdown("<br/>", unsafe_allow_html=True)
    
    # Renderização da grade 5x5
    for r in range(5):
        cols_m = st.columns([1, 1, 1, 1, 1, 5])
        for c in range(5):
            with cols_m[c]:
                if m["revealed"][r][c]:
                    val = m["board"][r][c]
                    lbl = "💥" if val == -1 else "🟩" if val == 0 else f"{val}"
                    st.button(lbl, key=f"mine_{r}_{c}", disabled=True, use_container_width=True)
                else:
                    if st.button("❓", key=f"mine_{r}_{c}", disabled=m["status"] != "Jogando", use_container_width=True):
                        m["revealed"][r][c] = True
                        if m["board"][r][c] == -1:
                            m["status"] = "Explodiu! Game Over."
                        else:
                            m["safe_clicks"] += 1
                            if m["safe_clicks"] == 21: m["status"] = "Vitória Total! Você limpou a área."
                        st.rerun()
    st.markdown("<br/>", unsafe_allow_html=True)
    if st.button("Reiniciar Campo Minado"):
        init_mines()
        st.rerun()

# ----------------- FLUXO: RPG DE TEXTO -----------------
elif game_choice == "⚔️ RPG Masmorra de Texto":
    if "rpg" not in st.session_state: init_rpg()
    r = st.session_state.rpg
    
    st.markdown(f"<div class='status-text'>SALA: {r['fase']} ▏ VIDA: {r['vida']} HP ▏ OURO: {r['ouro']} 💰</div>", unsafe_allow_html=True)
    st.markdown("<br/>", unsafe_allow_html=True)
    
    col_r_left, col_r_right = st.columns([2, 1])
    with col_r_left:
        st.markdown(f"<div class='balloon-retro' style='height:120px;'><b>📜 Diário da Masmorra:</b><br/><i>{r['log']}</i></div>", unsafe_allow_html=True)
        st.markdown("<br/>", unsafe_allow_html=True)
        
        # Gerenciamento de ações baseado no estado do RPG
        c_r_btn = st.columns(3)
        if r["status"] == "Explorando":
            if c_r_btn[0].button("Avançar e Explorar", use_container_width=True):
                process_rpg_action("Explorar")
                st.rerun()
        elif r["status"] == "Combate":
            if c_r_btn[0].button("⚔️ Atacar Monstro", use_container_width=True):
                process_rpg_action("Atacar")
                st.rerun()
    with col_r_right:
        if r["status"] == "Combate":
            st.warning(f"⚔️ EM COMBATTE!\nInimigo: {r['inimigo_name']}\nVida Restante: {r['inimigo_vida']}")
        if st.button("Reiniciar Aventura RPG"):
            init_rpg()
            st.rerun()
