import random
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
import streamlit as st

# =========================================================
# MISTER TRUCO - VERSÃO PREMIUM CORRIGIDA E AUDITADA
# Regras tradicionais de turno, baralho limpo e correção de bugs
# =========================================================

st.set_page_config(
    page_title="Mister Truco",
    page_icon="🃏",
    layout="wide",
)

# --- INJEÇÃO DE CSS DE ALTO CONTRASTE ---
st.markdown(
    """
    <style>
    .stApp { background-color: #1a4a2b !important; }
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    header, footer {visibility: hidden;}
    hr {margin: 0.4rem 0 !important; border-color: rgba(255,255,255,0.2) !important;}

    .status-text {
        color: #ffffff !important;
        font-family: 'Courier New', Courier, monospace;
        font-weight: bold;
        font-size: 15px;
        text-align: center;
        background-color: rgba(0,0,0,0.6);
        padding: 4px 12px;
        border-radius: 6px;
        margin: 0px;
        border: 1px solid rgba(255,255,255,0.2);
    }

    /* Verso da carta da CPU */
    .card-back {
        border: 2px solid #ffffff;
        border-radius: 8px;
        background-color: #11331c;
        background-image: repeating-linear-gradient(45deg, #1e4a2b 0, #1e4a2b 2px, transparent 0, transparent 50%);
        background-size: 8px 8px;
        height: 95px;
        max-width: 70px;
        margin: 0 auto;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #559966;
        font-size: 24px;
        font-weight: bold;
        box-shadow: 3px 3px 6px rgba(0,0,0,0.4);
    }

    /* Carta Física com Máximo Contraste */
    .card-played {
        border: 2px solid #000000 !important;
        border-radius: 8px !important;
        background-color: #ffffff !important; 
        color: #000000 !important; 
        height: 105px;
        max-width: 80px;
        margin: 0 auto 4px auto;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        font-weight: bold;
        box-shadow: 3px 3px 8px rgba(0,0,0,0.5);
    }
    
    .card-mini {
        border: 1.5px solid #000000 !important;
        border-radius: 5px !important;
        background-color: #ffffff !important; 
        color: #000000 !important; 
        width: 50px;
        height: 70px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        font-weight: bold;
        box-shadow: 1px 1px 4px rgba(0,0,0,0.3);
    }
    
    .red-suit { color: #dc2626 !important; font-size: 30px; line-height: 1; }
    .black-suit { color: #000000 !important; font-size: 30px; line-height: 1; }
    .red-suit-mini { color: #dc2626 !important; font-size: 22px; line-height: 1; }
    .black-suit-mini { color: #000000 !important; font-size: 22px; line-height: 1; }
    
    .balloon-cpu {
        background-color: #ffffff !important; 
        border: 2px solid #000000;
        border-radius: 12px; 
        padding: 10px; 
        color: #000000 !important; 
        box-shadow: 3px 3px 6px rgba(0,0,0,0.3);
        font-size: 13px;
        margin-bottom: 12px;
    }
    
    div[data-testid="stRadio"] label, div[data-testid="stRadio"] p {
        color: #ffffff !important;
        font-size: 13px !important;
        font-weight: bold !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] {
        flex-direction: row !important;
        gap: 15px !important;
    }

    .stButton>button {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1.5px solid #000000 !important;
        font-weight: bold !important;
        border-radius: 6px !important;
        padding: 2px 8px !important;
    }
    
    .challenge-alert {
        color: #fde047 !important;
        font-weight: bold !important;
        font-size: 15px !important;
        background-color: rgba(0,0,0,0.4);
        padding: 6px;
        border-radius: 6px;
        border: 1px dashed #fde047;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

SUITS = ["♦", "♠", "♥", "♣"]
SUIT_CLASSES = {"♦": "red-suit", "♠": "black-suit", "♥": "red-suit", "♣": "black-suit"}
SUIT_MINI_CLASSES = {"♦": "red-suit-mini", "♠": "black-suit-mini", "♥": "red-suit-mini", "♣": "black-suit-mini"}
SUIT_POWER = {"♦": 1, "♠": 2, "♥": 3, "♣": 4}
BET_SEQUENCE = [1, 3, 6, 9, 12]

@dataclass(frozen=True)
class Card:
    rank: str
    suit: str

    @property
    def label(self) -> str:
        return f"{self.rank}{self.suit}"


def get_next_rank(rank: str) -> str:
    order = ["4", "5", "6", "7", "Q", "J", "K", "A", "2", "3"]
    try:
        return order[(order.index(rank) + 1) % len(order)]
    except ValueError:
        return "4"


def card_power(card: Card, mode: str, vira: Optional[Card] = None) -> Tuple[int, int]:
    if mode == "Manilha Velha":
        # Ordem tradicional do baralho limpo de manilha fixa
        # Manilhas: 4♣ (Zap) > 7♥ (Copilha) > A♠ (Espadilha) > 7♦ (Pica-fumo)
        # Cartas comuns: 3 > 2 > A (de outros naipes) > K > J > Q
        if card.rank == "4" and card.suit == "♣": return (104, 4)
        if card.rank == "7" and card.suit == "♥": return (103, 3)
        if card.rank == "A" and card.suit == "♠": return (102, 2)
        if card.rank == "7" and card.suit == "♦": return (101, 1)
        
        order = ["Q", "J", "K", "A", "2", "3"]
        return (order.index(card.rank) if card.rank in order else -1, 0)
    else:
        # Manilha Nova (Baseada no Vira)
        manilha_rank = get_next_rank(vira.rank) if vira else ""
        if card.rank == manilha_rank:
            return (100, SUIT_POWER[card.suit])
        order = ["4", "5", "6", "7", "Q", "J", "K", "A", "2", "3"]
        return (order.index(card.rank) if card.rank in order else 0, 0)


def make_deck(mode: str) -> List[Card]:
    if mode == "Manilha Velha":
        # BARALHO LIMPO ESTRITO: Apenas as cartas válidas na regra clássica paulista/mineira
        valid_ranks = ["3", "2", "A", "K", "J", "Q"]
        deck = [Card(rank, suit) for rank in valid_ranks for suit in SUITS]
        # Adiciona cirurgicamente apenas as 4 manilhas fixas reais
        deck.append(Card("4", "♣"))
        deck.append(Card("7", "♥"))
        deck.append(Card("A", "♠"))
        deck.append(Card("7", "♦"))
        return deck
    else:
        # Manilha Nova usa o esqueleto completo sem 8, 9, 10
        ranks = ["4", "5", "6", "7", "Q", "J", "K", "A", "2", "3"]
        return [Card(rank, suit) for rank in ranks for suit in SUITS]


def team_of_player(player_idx: int, n_players: int) -> int:
    return player_idx if n_players == 2 else player_idx % 2


def player_name(i: int) -> str:
    return "Você" if i == 0 else f"Bot {i}"


def init_game(n_players: int, mode: str, structural_reset: bool = False):
    deck = make_deck(mode)
    random.shuffle(deck)

    hands = [[] for _ in range(n_players)]
    for _ in range(3):
        for p in range(n_players):
            hands[p].append(deck.pop())

    vira = deck.pop() if mode == "Manilha Nova" else None
    
    # Preserva o placar se for apenas uma virada de mão comum
    old_score = [0, 0]
    old_dealer = 0
    if "game" in st.session_state and not structural_reset:
        old_score = st.session_state.game["score"]
        old_dealer = st.session_state.game["dealer"]
        next_dealer = (old_dealer + 1) % n_players
    else:
        next_dealer = 0

    st.session_state.game = {
        "n_players": n_players,
        "mode": mode,
        "hands": hands,
        "vira": vira,
        "table": [],
        "dealer": next_dealer,
        "turn": (next_dealer + 1) % n_players, # O jogador seguinte ao distribuidor inicia a primeira vaza (Mão)
        "trick_no": 1,
        "hand_points": 1,
        "score": old_score,
        "trick_history": [],
        "history": [],
        "finished_hand": False,
        "finished_match": False,
        "message": f"Nova mão distribuída! Vez de {player_name((next_dealer + 1) % n_players)} começar.",
        "pending_truco": None,
    }


def next_bet_value(current: int) -> Optional[int]:
    for value in BET_SEQUENCE:
        if value > current: return value
    return None


def ask_truco(from_player: int):
    g = st.session_state.game
    from_team = team_of_player(from_player, g["n_players"])
    new_value = next_bet_value(g["hand_points"])
    if new_value is None: return

    g["pending_truco"] = {
        "from_team": from_team,
        "to_team": 1 - from_team,
        "value": new_value,
        "from_player": from_player,
    }
    label = "TRUCO!" if new_value == 3 else f"{new_value}!"
    g["history"].insert(0, f"{player_name(from_player)} gritou {label}")
    g["message"] = f"Eu gritei {label}! Aceita ou corre?" if from_player != 0 else f"Você pediu {label}? Deixa eu pensar..."


def accept_truco():
    g = st.session_state.game
    pending = g["pending_truco"]
    if not pending: return
    g["hand_points"] = pending["value"]
    g["history"].insert(0, f"Desafio aceito! Valendo {g['hand_points']}.")
    g["message"] = f"Aceito! A rodada agora está valendo {g['hand_points']} tentos."
    g["pending_truco"] = None


def refuse_truco():
    g = st.session_state.game
    pending = g["pending_truco"]
    if not pending: return
    winner_team = pending["from_team"]
    g["score"][winner_team] += g["hand_points"]
    g["history"].insert(0, f"Correram! O Time {winner_team + 1} faturou os pontos.")
    finish_hand(f"Mão encerrada porque o adversário correu do desafio.", already_scored=True)


def play_card(player_idx: int, card_idx: int):
    g = st.session_state.game
    if g["finished_hand"] or g["finished_match"] or g["pending_truco"]:
        return

    card = g["hands"][player_idx].pop(card_idx)
    g["table"].append({"player": player_idx, "card": card})
    g["history"].insert(0, f"{player_name(player_idx)} jogou {card.label}")

    if len(g["table"]) == g["n_players"]:
        resolve_trick()
    else:
        g["turn"] = (g["turn"] + 1) % g["n_players"]


def resolve_trick():
    g = st.session_state.game
    table = g["table"]

    powers = [card_power(play["card"], g["mode"], g["vira"]) for play in table]
    max_power = max(powers, key=lambda x: (x[0], x[1]))
    highest_indices = [i for i, p in enumerate(powers) if p[0] == max_power[0] and p[1] == max_power[1]]
    
    is_empate = False
    if len(highest_indices) > 1:
        teams_in_tie = {team_of_player(table[i]["player"], g["n_players"]) for i in highest_indices}
        if len(teams_in_tie) > 1: is_empate = True

    if is_empate:
        g["trick_history"].append(-1)
        g["history"].insert(0, f"Vaza {g['trick_no']} empatou!")
        # Em caso de empate, o jogador que "amarrou" (fez o empate) ou o último a jogar mantém a vez de puxar
        winner_player = table[highest_indices[0]]["player"]
    else:
        winning_play = table[powers.index(max_power)]
        winner_player = winning_play["player"]
        winner_team = team_of_player(winner_player, g["n_players"])
        g["trick_history"].append(winner_team)
        g["history"].insert(0, f"{player_name(winner_player)} ganhou a vaza com {winning_play['card'].label}.")

    th = g["trick_history"]
    hand_winner = None

    # Lógica estruturada de melhor de 3 vazas (com regras de empate/cangada)
    if th.count(0) == 2: hand_winner = 0
    elif th.count(1) == 2: hand_winner = 1
    elif len(th) == 2 and th[0] == -1 and th[1] != -1: hand_winner = th[1]
    elif len(th) == 2 and th[0] != -1 and th[1] == -1: hand_winner = th[0]
    elif len(th) == 3:
        if th[2] == -1: hand_winner = th[0] if th[0] != -1 else 0
        else: hand_winner = th[2]

    if hand_winner is not None:
        g["score"][hand_winner] += g["hand_points"]
        finish_hand(f"Fim da rodada! Vitória do Time {hand_winner + 1}.", already_scored=True)
        return

    # Se a mão não acabou, o vencedor da vaza anterior TEM que jogar primeiro (Puxar a vaza)
    g["table"] = []
    g["trick_no"] += 1
    g["turn"] = winner_player
    g["message"] = f"Vaza resolvida. {player_name(winner_player)} ganhou e joga primeiro agora."


def finish_hand(msg: str, already_scored: bool = False):
    g = st.session_state.game
    g["finished_hand"] = True
    g["pending_truco"] = None
    g["message"] = msg

    if g["score"][0] >= 12 or g["score"][1] >= 12:
        g["finished_match"] = True
        w = "Você" if g["score"][0] >= 12 else "CPU"
        g["message"] = f"🏆 FIM DE JOGO! {w} atingiu os 12 pontos e venceu a partida!"


def bot_choose_card(player_idx: int) -> int:
    g = st.session_state.game
    hand = g["hands"][player_idx]
    if not hand: return 0
    hand_sorted = sorted(enumerate(hand), key=lambda x: card_power(x[1], g["mode"], g["vira"])[0])
    if not g["table"]: return hand_sorted[0][0]
    best_card = max(g["table"], key=lambda x: card_power(x["card"], g["mode"], g["vira"]))["card"]
    for idx, card in hand_sorted:
        if card_power(card, g["mode"], g["vira"]) > card_power(best_card, g["mode"], g["vira"]): return idx
    return hand_sorted[0][0]


def maybe_bot_turns():
    g = st.session_state.game
    safety = 0
    while not g["finished_hand"] and not g["finished_match"] and not g["pending_truco"] and g["turn"] != 0 and safety < 10:
        safety += 1
        player = g["turn"]
        if not g["hands"][player]: continue
        
        avg_p = sum(card_power(c, g["mode"], g["vira"])[0] for c in g["hands"][player]) / len(g["hands"][player])
        if next_bet_value(g["hand_points"]) and avg_p >= 5.0 and random.random() < 0.12:
            ask_truco(player)
            break

        idx = bot_choose_card(player)
        play_card(player, idx)


# --- ÁREA DE SELEÇÃO CONFIGURÁVEL DO TOPO ---
c_top_title, c_top_players, c_top_mode, c_top_reset = st.columns([1, 1.2, 1.2, 0.8])

with c_top_title:
    st.markdown("<h3 style='color: white; font-family: monospace; margin:0; padding-top:5px;'>MISTER TRUCO</h3>", unsafe_allow_html=True)

with c_top_players:
    n_players = st.radio("Jogadores:", [2, 4], format_func=lambda x: "1v1 (Dois)" if x == 2 else "2v2 (Quatro)", label_visibility="collapsed")

with c_top_mode:
    mode = st.radio("Manilha:", ["Manilha Velha", "Manilha Nova"], label_visibility="collapsed")

with c_top_reset:
    apply_btn = st.button("Aplicar Regras", use_container_width=True)

# Inicialização com barreira anti-bug de estado
if "game" not in st.session_state or st.session_state.game["mode"] != mode or st.session_state.game["n_players"] != n_players or apply_btn:
    init_game(n_players, mode, structural_reset=True)

g = st.session_state.game

if g["pending_truco"] and g["pending_truco"]["to_team"] != team_of_player(0, g["n_players"]):
    if random.random() < 0.55: accept_truco()
    else: refuse_truco()
    st.rerun()

maybe_bot_turns()

# --- TABULEIRO E EXIBIÇÃO ---
c_header = st.columns([2, 1])
with c_header[0]:
    st.markdown(f"<div class='status-text'>CPU: {g['score'][1]}   ▏   VOCÊ: {g['score'][0]}</div>", unsafe_allow_html=True)
with c_header[1]:
    st.markdown(f"<div class='status-text' style='background-color:#11331c;'>VALENDO: {g['hand_points']} PTS</div>", unsafe_allow_html=True)

st.markdown("<hr/>", unsafe_allow_html=True)

col_board, col_panel = st.columns([2.8, 1.2])

with col_board:
    # 1. Cartas Ocultas do Adversário
    cpu_count = len(g["hands"][1]) if g["n_players"] == 2 else len(g["hands"][1]) + len(g["hands"][3])
    cols_cpu = st.columns([1, 1, 1, 1, 1])
    for i in range(min(cpu_count, 3)):
        with cols_cpu[i + 1]:
            st.markdown("<div class='card-back'>R</div>", unsafe_allow_html=True)

    st.markdown("<div style='margin: 12px 0;'></div>", unsafe_allow_html=True)

    # 2. Suas Cartas Ativas (Correção definitiva do KeyError)
    cols_player = st.columns([1, 1, 1, 1, 1])
    human_turn = g["turn"] == 0 and not g["pending_truco"] and not g["finished_hand"]
    
    # Puxa sempre da mão real guardada, evitando quebras estruturais
    my_cards = g["hands"][0]
    for i, card in enumerate(my_cards):
        with cols_player[i + 1]:
            s_class = SUIT_CLASSES[card.suit]
            st.markdown(
                f"""
                <div class='card-played'>
                    <div style='font-size:18px; margin-bottom:-4px;'>{card.rank}</div>
                    <div class='{s_class}'>{card.suit}</div>
                </div>
                """, 
                unsafe_allow_html=True
            )
            if st.button("Jogar", key=f"p_btn_{i}", disabled=not human_turn, use_container_width=True):
                play_card(0, i)
                st.rerun()

    st.markdown("<div style='margin: 12px 0;'></div>", unsafe_allow_html=True)

    # 3. Comandos de Aposta da Mesa
    cols_act = st.columns([1.2, 1, 1, 1.2])
    next_val = next_bet_value(g["hand_points"])
    truco_lbl = "TRUCO" if next_val == 3 else f"PEDIR {next_val}" if next_val else "MÁXIMO"
    
    with cols_act[1]:
        if st.button(truco_lbl, key="mesa_truco_btn", disabled=not next_val or not human_turn or g["finished_hand"], use_container_width=True):
            ask_truco(0)
            st.rerun()
            
    with cols_act[2]:
        if st.button("CORRER", key="mesa_correr_btn", disabled=not human_turn or g["finished_hand"], use_container_width=True):
            g["score"][1] += g["hand_points"]
            finish_hand("Você correu e deu os pontos para a CPU!", already_scored=True)
            st.rerun()

with col_panel:
    # Caixa de comunicação da CPU
    st.markdown(f"<div class='balloon-cpu'><b>💻 CPU diz:</b><br/><i>\"{g['message']}\"</i></div>", unsafe_allow_html=True)

    # Modais de desafio (Truco/6/9/12)
    if g["pending_truco"] and g["pending_truco"]["to_team"] == team_of_player(0, g["n_players"]):
        st.markdown(f"<div class='challenge-alert'>⚠️ Desafio: Aceita valer {g['pending_truco']['value']}?</div>", unsafe_allow_html=True)
        c_choice = st.columns(2)
        if c_choice[0].button("ACEITAR", key="challenge_accept_unique", use_container_width=True):
            accept_truco()
            st.rerun()
        if c_choice[1].button("CORRER", key="challenge_refuse_unique", use_container_width=True):
            refuse_truco()
            st.rerun()

    # Informações do Vira (Manilha Nova)
    if g["mode"] == "Manilha Nova" and g["vira"]:
        st.markdown(f"<div style='background-color: rgba(0,0,0,0.4); padding: 5px; border-radius: 6px; color: white; text-align: center; font-size:11px; margin-bottom:10px; border: 1px solid rgba(255,255,255,0.1);'>VIRA: <b>{g['vira'].label}</b>   |   MANILHA: <b style='color:#38bdf8;'>{get_next_rank(g['vira'].rank)}</b></div>", unsafe_allow_html=True)

    # REVISÃO VISUAL DA MESA (Ver as cartas jogadas na rodada)
    st.markdown("<p style='color: white; font-weight: bold; margin: 0; font-size:13px;'>Cartas na Mesa:</p>", unsafe_allow_html=True)
    if not g["table"]:
        st.caption("A mesa está limpa.")
    else:
        for play in g["table"]:
            c = play["card"]
            mini_s_class = SUIT_MINI_CLASSES[c.suit]
            st.markdown(
                f"""
                <div style="display: flex; align-items: center; gap: 12px; background: rgba(0,0,0,0.4); padding: 6px; border-radius: 8px; margin-bottom: 6px; border: 1px solid rgba(255,255,255,0.1);">
                    <div class='card-mini'>
                        <div style='font-size:12px; margin-bottom:-4px;'>{c.rank}</div>
                        <div class='{mini_s_class}'>{c.suit}</div>
                    </div>
                    <div style='color: #ffffff; font-size: 13px;'>
                        <b>{player_name(play['player'])}</b> jogou esta carta.
                    </div>
                </div>
                """, 
                unsafe_allow_html=True
            )

    st.markdown("<div style='margin: 8px 0;'></div>", unsafe_allow_html=True)
    if st.button("Próxima Mão", key="next_hand_btn", disabled=not g["finished_hand"] or g["finished_match"], use_container_width=True):
        new_hand_keep_score()
        st.rerun()

if g["finished_match"]:
    st.balloons()
