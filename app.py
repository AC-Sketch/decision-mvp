import random
import streamlit as st
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple

# =========================================================
# MISTER TRUCO - ENGINE PROFISSIONAL ESTÁVEL
# Resolução de cartas duplicadas, turnos e layout dinâmico
# =========================================================

st.set_page_config(page_title="Mister Truco Pro", page_icon="🃏", layout="wide")

# --- ESTILIZAÇÃO COMPACTA DE ALTO CONTRASTE ---
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
        padding: 5px 12px;
        border-radius: 6px;
        margin: 0px;
        border: 1px solid rgba(255,255,255,0.2);
    }
    .card-back {
        border: 2px solid #ffffff; border-radius: 6px;
        background-color: #11331c;
        background-image: repeating-linear-gradient(45deg, #1e4a2b 0, #1e4a2b 2px, transparent 0, transparent 50%);
        background-size: 8px 8px;
        height: 85px; max-width: 62px; margin: 0 auto;
        display: flex; align-items: center; justify-content: center;
        color: #559966; font-size: 20px; font-weight: bold;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.4);
    }
    .card-played {
        border: 2px solid #000000 !important; border-radius: 8px !important;
        background-color: #ffffff !important; color: #000000 !important; 
        height: 100px; max-width: 75px; margin: 0 auto 4px auto;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        font-size: 22px; font-weight: bold; box-shadow: 3px 3px 8px rgba(0,0,0,0.5);
    }
    .card-center {
        border: 2px solid #ffffff !important; border-radius: 8px !important;
        background-color: #ffffff !important; color: #000000 !important; 
        height: 95px; width: 70px; margin: 0 auto;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        font-size: 22px; font-weight: bold; box-shadow: 3px 3px 10px rgba(0,0,0,0.6);
    }
    .red-suit { color: #dc2626 !important; font-size: 28px; line-height: 1; }
    .black-suit { color: #000000 !important; font-size: 28px; line-height: 1; }
    .balloon-cpu {
        background-color: #ffffff !important; border: 2px solid #000000; border-radius: 12px; 
        padding: 10px; color: #000000 !important; box-shadow: 3px 3px 6px rgba(0,0,0,0.3);
        font-size: 13px; margin-bottom: 12px;
    }
    .challenge-alert {
        color: #fde047 !important; font-weight: bold !important; font-size: 14px !important;
        background-color: rgba(0,0,0,0.5); padding: 6px; border-radius: 6px;
        border: 1px dashed #fde047; margin-bottom: 10px; text-align: center;
    }
    div[data-testid="stRadio"] label, div[data-testid="stRadio"] p {
        color: #ffffff !important; font-size: 13px !important; font-weight: bold !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] { flex-direction: row !important; gap: 15px !important; }
    .stButton>button {
        background-color: #ffffff !important; color: #000000 !important;
        border: 1.5px solid #000000 !important; font-weight: bold !important; border-radius: 6px !important;
    }
    </style>
""", unsafe_allow_html=True)

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

# --- MOTOR DE REGRAS PURAS ---

def get_card_power(card: Card, mode: str, vira: Optional[Card]) -> int:
    if mode == "Manilha Velha":
        if card.rank == "4" and card.suit == "Paus": return 104     # Zap
        if card.rank == "7" and card.suit == "Copas": return 103    # Copilha
        if card.rank == "A" and card.suit == "Espadas": return 102  # Espadilha
        if card.rank == "7" and card.suit == "Ouros": return 101    # Pica-fumo
        order = ["Q", "J", "K", "A", "2", "3"]
        return order.index(card.rank) if card.rank in order else -1
    else:
        if vira is None: return 0
        next_rank = ORDER_MANILHA_NOVA[(ORDER_MANILHA_NOVA.index(vira.rank) + 1) % len(ORDER_MANILHA_NOVA)]
        if card.rank == next_rank:
            suit_pow = {"Ouros": 1, "Espadas": 2, "Copas": 3, "Paus": 4}
            return 100 + suit_pow.get(card.suit, 0)
        return ORDER_MANILHA_NOVA.index(card.rank)

def start_hand(g: dict):
    suits = ["Ouros", "Espadas", "Copas", "Paus"]
    if g["mode"] == "Manilha Velha":
        deck = [Card(r, s) for r in ["3", "2", "A", "K", "J", "Q"] for s in suits]
        deck += [Card("4", "Paus"), Card("7", "Copas"), Card("A", "Espadas"), Card("7", "Ouros")]
    else:
        deck = [Card(r, s) for r in ORDER_MANILHA_NOVA for s in suits]
        
    random.shuffle(deck)
    
    g["hands"] = [[] for _ in range(g["n_players"])]
    for _ in range(3):
        for p in range(g["n_players"]):
            g["hands"][p].append(deck.pop())
            
    g["vira"] = deck.pop() if g["mode"] == "Manilha Nova" else None
    g["table"] = {}  # Mapeamento estrito: player_idx -> Card (Evita sumir a carta)
    g["trick_no"] = 1
    g["hand_points"] = 1
    g["trick_wins"] = []
    g["finished_hand"] = False
    g["pending_truco"] = None
    g["turn"] = (g["dealer"] + 1) % g["n_players"]
    g["message"] = f"Nova rodada! Jogador {g['turn']} começa."

def process_trick_victory(g: dict):
    # Avaliação precisa baseada em chaves estáticas
    players_in_trick = list(g["table"].keys())
    powers = [get_card_power(g["table"][p], g["mode"], g["vira"]) for p in players_in_trick]
    max_pow = max(powers)
    winners = [players_in_trick[i] for i, pow_val in enumerate(powers) if pow_val == max_pow]
    
    is_tie = False
    if len(winners) > 1:
        teams = {w % 2 for w in winners}
        if len(teams) > 1: is_tie = True
        
    if is_tie:
        g["trick_wins"].append(-1)
        next_puller = winners[0]
        g["message"] = "A vaza EMPATOU! Quem amarrou puxa a próxima vaza."
    else:
        next_puller = winners[powers.index(max_pow)]
        g["trick_wins"].append(next_puller % 2)
        g["message"] = f"Jogador {next_puller} ganhou esta vaza!"

    tw = g["trick_wins"]
    hand_winner = None
    
    if tw.count(0) == 2: hand_winner = 0
    elif tw.count(1) == 2: hand_winner = 1
    elif len(tw) == 2 and tw[0] == -1 and tw[1] != -1: hand_winner = tw[1]
    elif len(tw) == 2 and tw[0] != -1 and tw[1] == -1: hand_winner = tw[0]
    elif len(tw) == 3:
        if tw[2] == -1: hand_winner = tw[0] if tw[0] != -1 else 0
        else: hand_winner = tw[2]

    if hand_winner is not None:
        g["score"][hand_winner] += g["hand_points"]
        g["finished_hand"] = True
        g["message"] = f"Fim da mão! Vitória do Time {hand_winner + 1} (+{g['hand_points']} pts)."
        g["dealer"] = (g["dealer"] + 1) % g["n_players"]
        return

    g["turn"] = next_puller

def bot_play(g: dict):
    hand = g["hands"][g["turn"]]
    if not hand: return

    # Bots trucam defensiva ou agressivamente por força média
    avg_p = sum(get_card_power(c, g["mode"], g["vira"]) for c in hand) / len(hand)
    if not g["pending_truco"] and g["hand_points"] < 12 and avg_p > 4.0 and random.random() < 0.08:
        next_val = {1:3, 3:6, 6:9, 9:12}.get(g["hand_points"], 12)
        g["pending_truco"] = {"from_team": g["turn"] % 2, "to_team": 0, "value": next_val}
        g["message"] = f"O Bot {g['turn']} pediu {next_val if next_val > 3 else 'TRUCO'}!"
        return

    hand_powers = [get_card_power(c, g["mode"], g["vira"]) for c in hand]
    if not g["table"]:
        chosen_idx = hand_powers.index(min(hand_powers))
    else:
        table_max = max([get_card_power(c, g["mode"], g["vira"]) for c in g["table"].values()])
        options = [i for i, p in enumerate(hand_powers) if p > table_max]
        chosen_idx = hand_powers.index(min([hand_powers[o] for o in options])) if options else hand_powers.index(min(hand_powers))
        
    card = g["hands"][g["turn"]].pop(chosen_idx)
    g["table"][g["turn"]] = card  # Garante registro permanente na mesa
    
    if len(g["table"]) == g["n_players"]:
        process_trick_victory(g)
    else:
        g["turn"] = (g["turn"] + 1) % g["n_players"]


# --- ÁREA DE CONFIGURAÇÃO ---
c_title, c_players, c_mode, c_reset = st.columns([1, 1.2, 1.2, 0.8])
with c_title:
    st.markdown("<h3 style='color: white; font-family: monospace; margin:0; padding-top:5px;'>MISTER TRUCO</h3>", unsafe_allow_html=True)
with c_players:
    n_players_sel = st.radio("Jogadores", [2, 4], format_func=lambda x: "1v1 (Dois)" if x == 2 else "2v2 (Quatro)", label_visibility="collapsed")
with c_mode:
    mode_sel = st.radio("Regras", ["Manilha Velha", "Manilha Nova"], label_visibility="collapsed")
with c_reset:
    btn_apply = st.button("Aplicar Regras", use_container_width=True)

if "game" not in st.session_state or btn_apply or st.session_state.game["mode"] != mode_sel or st.session_state.game["n_players"] != n_players_sel:
    st.session_state.game = {
        "n_players": n_players_sel,
        "mode": mode_sel,
        "score": [0, 0],
        "dealer": 0,
        "hands": [], "vira": None, "table": {}, "trick_no": 1, "hand_points": 1,
        "trick_wins": [], "finished_hand": False, "pending_truco": None, "turn": 0, "message": ""
    }
    start_hand(st.session_state.game)

g = st.session_state.game

# Processamento de Desafios da CPU
if g["pending_truco"] and g["pending_truco"]["to_team"] == 1:
    if random.random() < 0.55:
        g["hand_points"] = g["pending_truco"]["value"]
        g["pending_truco"] = None
        g["message"] = f"A CPU aceitou! A rodada agora vale {g['hand_points']} tentos."
    else:
        g["score"][0] += g["hand_points"]
        start_hand(g)
        g["message"] = "Eles correram! Os pontos são seus."
    st.rerun()

# Inteligência de disparo de turnos dos Bots
if not g["finished_hand"] and g["turn"] != 0 and not g["pending_truco"]:
    bot_play(g)
    st.rerun()


# --- PLACAR E STATUS ---
c_score = st.columns([2, 1])
with c_score[0]:
    st.markdown(f"<div class='status-text'>CPU (Time 2): {g['score'][1]}   ▏   JOGADOR (Time 1): {g['score'][0]}</div>", unsafe_allow_html=True)
with c_score[1]:
    st.markdown(f"<div class='status-text' style='background-color:#11331c;'>VALENDO: {g['hand_points']} PTS</div>", unsafe_allow_html=True)

st.markdown("<hr/>", unsafe_allow_html=True)


# --- INTERFACE CENTRAL DO TABULEIRO DINÂMICO ---
col_board, col_panel = st.columns([2.8, 1.2])

with col_board:
    # 1. DISPOSIÇÃO ADVERSÁRIA DINÂMICA (Topo)
    if g["n_players"] == 2:
        # Modo 2 Jogadores: Apenas Bot 1 no Topo Centralizado
        c_cpu_pos = st.columns([1.5, 1, 1.5])
        with c_cpu_pos[1]:
            cpu_cards = len(g["hands"][1])
            st.markdown(f"<p style='color: #7ca982; font-size:11px; margin:0; text-align:center;'>BOT 1 ({cpu_cards} cartas)</p>", unsafe_allow_html=True)
            st.markdown("<div class='card-back'>R</div>", unsafe_allow_html=True)
    else:
        # Modo 4 Jogadores: Distribui os Bots na Mesa (Bot 1 Esquerda, Bot 2 Topo, Bot 3 Direita)
        c_cpu_pos = st.columns([1, 1, 1])
        with c_cpu_pos[0]:
            st.markdown(f"<p style='color: #7ca982; font-size:11px; margin:0;'>BOT 1 (Oponente)</p><div class='card-back' style='margin:0;'>R</div>", unsafe_allow_html=True)
        with c_cpu_pos[1]:
            st.markdown(f"<p style='color: #7ca982; font-size:11px; margin:0; text-align:center;'>BOT 2 (Parceiro)</p><div class='card-back'>R</div>", unsafe_allow_html=True)
        with c_cpu_pos[2]:
            st.markdown(f"<p style='color: #7ca982; font-size:11px; margin:0; text-align:right;'>BOT 3 (Oponente)</p><div class='card-back' style='margin:0 0 0 auto;'>R</div>", unsafe_allow_html=True)

    st.markdown("<div style='margin: 15px 0;'></div>", unsafe_allow_html=True)

    # 2. SEÇÃO INFERIOR: Suas Cartas Ativas (Sem Duplicações por ID fixo)
    cols_player = st.columns([1, 1, 1, 1, 1])
    my_turn_active = (g["turn"] == 0 and not g["pending_truco"] and not g["finished_hand"])
    
    for idx, card in enumerate(g["hands"][0]):
        with cols_player[idx + 1]:
            st.markdown(f"""
                <div class='card-played'>
                    <div style='font-size:18px; margin-bottom:-4px;'>{card.rank}</div>
                    <div class='{card.color}'>{card.symbol}</div>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Jogar", key=f"action_card_play_{idx}_{card.rank}_{card.suit}", disabled=not my_turn_active, use_container_width=True):
                # Limpa a mesa antes se uma nova vaza cheia estiver começando após a vitória de alguém
                if len(g["table"]) == g["n_players"]:
                    g["table"] = {}
                g["table"][0] = g["hands"][0].pop(idx)
                
                if len(g["table"]) == g["n_players"]:
                    process_trick_victory(g)
                else:
                    g["turn"] = (g["turn"] + 1) % g["n_players"]
                st.rerun()

    st.markdown("<div style='margin: 15px 0;'></div>", unsafe_allow_html=True)

    # 3. Comandos de Aposta Inferiores
    cols_act = st.columns([1.2, 1, 1, 1.2])
    next_bet = {1:3, 3:6, 6:9, 9:12}.get(g["hand_points"])
    truco_label = "TRUCO" if next_bet == 3 else f"PEDIR {next_bet}" if next_bet else "MÁXIMO"
    
    with cols_act[1]:
        if st.button(truco_label, key="act_truco_p", disabled=not next_bet or not my_turn_active, use_container_width=True):
            g["pending_truco"] = {"from_team": 0, "to_team": 1, "value": next_bet}
            g["message"] = "Você gritou truco! Aguardando o oponente..."
            st.rerun()
    with cols_act[2]:
        if st.button("CORRER", key="act_fold_p", disabled=not my_turn_active, use_container_width=True):
            g["score"][1] += g["hand_points"]
            start_hand(g)
            st.rerun()

with col_panel:
    # Balão de fala e notificações do jogo
    st.markdown(f"<div class='balloon-cpu'><b>💬 Status da Mesa:</b><br/><i>\"{g['message']}\"</i></div>", unsafe_allow_html=True)

    if g["pending_truco"] and g["pending_truco"]["to_team"] == 0:
        st.markdown(f"<div class='challenge-alert'>⚠️ Desafio valendo {g['pending_truco']['value']}!</div>", unsafe_allow_html=True)
        c_ch = st.columns(2)
        if c_ch[0].button("ACEITAR", key="acc_ch_panel", use_container_width=True):
            g["hand_points"] = g["pending_truco"]["value"]
            g["pending_truco"] = None
            g["message"] = f"Aceito! A rodada está valendo {g['hand_points']}."
            st.rerun()
        if c_ch[1].button("CORRER", key="fold_ch_panel", use_container_width=True):
            g["score"][1] += g["hand_points"]
            start_hand(g)
            st.rerun()

    if g["mode"] == "Manilha Nova" and g["vira"]:
        m_rank = ORDER_MANILHA_NOVA[(ORDER_MANILHA_NOVA.index(g["vira"].rank) + 1) % len(ORDER_MANILHA_NOVA)]
        st.markdown(f"<div style='background-color: rgba(0,0,0,0.4); padding: 5px; border-radius: 6px; color: white; text-align: center; font-size:11px; margin-bottom:10px;'>VIRA: <b>{g['vira'].label}</b>   |   MANILHA: <b style='color:#38bdf8;'>{m_rank}</b></div>", unsafe_allow_html=True)

    # EXIBIÇÃO EM TAMPO REAL DAS CARTAS BAIXADAS NA MESA (Centralizado por Player)
    st.markdown("<p style='color: white; font-weight: bold; margin: 0; font-size:13px;'>Cartas Jogadas na Vaza:</p>", unsafe_allow_html=True)
    if not g["table"]:
        st.caption("Nenhuma carta jogada ainda.")
    else:
        # Renderização em grid dos cards jogados na mesa de forma persistente
        for p_idx, c in g["table"].items():
            p_name = "Você" if p_idx == 0 else f"Bot {p_idx}"
            st.markdown(f"""
                <div style="display: flex; align-items: center; gap: 12px; background: rgba(0,0,0,0.4); padding: 4px; border-radius: 8px; margin-bottom: 4px;">
                    <div class='card-center'><div style='font-size:13px;'>{c.rank}</div><div class='{c.color}'>{c.symbol}</div></div>
                    <div style='color: #ffffff; font-size: 13px;'><b>{p_name}</b> jogou</div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='margin: 8px 0;'></div>", unsafe_allow_html=True)
    
    # Se a vaza ou a mão terminar, a mesa permanece congelada até que você clique para avançar
    is_next_hand_ready = g["finished_hand"] or len(g["table"]) == g["n_players"]
    if st.button("Avançar Jogada", key="next_hand_sys_btn", disabled=not is_next_hand_ready, use_container_width=True):
        if g["finished_hand"]:
            start_hand(g)
        else:
            g["table"] = {}  # Limpa o feltro da mesa para a vaza seguinte
        st.rerun()

if g["score"][0] >= 12 or g["score"][1] >= 12:
    st.balloons()
