import random
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
import streamlit as st

# =========================================================
# MISTER TRUCO CUSTOM - VERSÃO FINAL AUDITADA
# Regras: Manilha Velha/Nova | 2 ou 4 Jogadores | Truco a 12
# Interface: Estilo Retro "Tapete Verde" com Balão da CPU
# =========================================================

st.set_page_config(
    page_title="Mister Truco Custom",
    page_icon="🃏",
    layout="wide",
)

# --- ESTILIZAÇÃO CSS CUSTOMIZADA (MISTER TRUCO) ---
st.markdown(
    """
    <style>
    .stApp {
        background-color: #1a4a2b; /* Feltro verde clássico */
    }
    .status-text {
        color: #ffffff;
        font-family: 'Courier New', Courier, monospace;
        font-weight: bold;
        font-size: 20px;
        text-align: center;
        background-color: rgba(0,0,0,0.4);
        padding: 5px 15px;
        border-radius: 5px;
    }
    .card-back {
        border: 2px solid #ffffff;
        border-radius: 8px;
        background-color: #1e3a2f;
        background-image: repeating-linear-gradient(45deg, #2d5a44 0, #2d5a44 2px, transparent 0, transparent 50%);
        background-size: 8px 8px;
        height: 110px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #7ca982;
        font-size: 28px;
        font-weight: bold;
        box-shadow: 3px 3px 5px rgba(0,0,0,0.3);
    }
    .card-played {
        border: 2px solid #000000;
        border-radius: 8px;
        background-color: #ffffff;
        color: #000000;
        height: 110px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        font-weight: bold;
        box-shadow: 3px 3px 5px rgba(0,0,0,0.4);
    }
    .red-suit { color: #dc2626; }
    .black-suit { color: #000000; }
    
    /* Balão de fala da CPU */
    .balloon-cpu {
        background-color: #ffffff; 
        border-radius: 15px; 
        padding: 12px; 
        color: #000000; 
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

SUITS = ["♦", "♠", "♥", "♣"]  # Ouros, Espadas, Copas, Paus
SUIT_CLASSES = {"♦": "red-suit", "♠": "black-suit", "♥": "red-suit", "♣": "black-suit"}
SUIT_POWER = {"♦": 1, "♠": 2, "♥": 3, "♣": 4}

BET_SEQUENCE = [1, 3, 6, 9, 12]

@dataclass(frozen=True)
class Card:
    rank: str
    suit: str

    @property
    def label(self) -> str:
        return f"{self.rank}{self.suit}"
    
    @property
    def full_name(self) -> str:
        names = {"♦": "Ouros", "♠": "Espadas", "♥": "Copas", "♣": "Paus"}
        return f"{self.rank} de {names[self.suit]}"


def get_next_rank(rank: str) -> str:
    order = ["4", "5", "6", "7", "Q", "J", "K", "A", "2", "3"]
    try:
        idx = order.index(rank)
        return order[(idx + 1) % len(order)]
    except ValueError:
        return "4"


def card_power(card: Card, mode: str, vira: Optional[Card] = None) -> Tuple[int, int]:
    if mode == "Manilha Velha":
        ranks = ["Q", "J", "K", "2", "3", "A", "7", "4"]
        power_idx = ranks.index(card.rank)
        is_manilha = card.rank in ["4", "7", "A", "3"]
        return (power_idx, SUIT_POWER[card.suit] if is_manilha else 0)
    else:
        manilha_rank = get_next_rank(vira.rank) if vira else ""
        if card.rank == manilha_rank:
            return (100, SUIT_POWER[card.suit])
        order = ["4", "5", "6", "7", "Q", "J", "K", "A", "2", "3"]
        return (order.index(card.rank) if card.rank in order else 0, 0)


def make_deck(mode: str) -> List[Card]:
    ranks = ["4", "5", "6", "7", "Q", "J", "K", "A", "2", "3"] if mode == "Manilha Nova" else ["4", "7", "A", "3", "2", "K", "J", "Q"]
    return [Card(rank, suit) for rank in ranks for suit in SUITS]


def team_of_player(player_idx: int, n_players: int) -> int:
    return player_idx if n_players == 2 else player_idx % 2


def player_name(i: int) -> str:
    return "Você" if i == 0 else f"Bot {i}"


def init_game(n_players: int, mode: str):
    deck = make_deck(mode)
    random.shuffle(deck)

    hands = [[] for _ in range(n_players)]
    for _ in range(3):
        for p in range(n_players):
            hands[p].append(deck.pop())

    vira = deck.pop() if mode == "Manilha Nova" else None

    st.session_state.game = {
        "n_players": n_players,
        "mode": mode,
        "hands": hands,
        "vira": vira,
        "table": [],
        "turn": 0,
        "dealer": 0,
        "trick_no": 1,
        "hand_points": 1,
        "score": [0, 0],
        "trick_history": [],
        "history": [],
        "finished_hand": False,
        "finished_match": False,
        "message": "Pode começar, e se prepare para amargar uma derrota vergonhosa!",
        "pending_truco": None,
    }


def append_history(msg: str):
    st.session_state.game["history"].insert(0, msg)


def next_bet_value(current: int) -> Optional[int]:
    for value in BET_SEQUENCE:
        if value > current:
            return value
    return None


def ask_truco(from_player: int):
    g = st.session_state.game
    from_team = team_of_player(from_player, g["n_players"])
    new_value = next_bet_value(g["hand_points"])

    if new_value is None:
        return

    g["pending_truco"] = {
        "from_team": from_team,
        "to_team": 1 - from_team,
        "value": new_value,
        "from_player": from_player,
    }
    label = "TRUCO!" if new_value == 3 else f"{new_value}!"
    append_history(f"{player_name(from_player)} gritou {label}")
    g["message"] = f"Eu gritei {label}! Vai aceitar ou vai correr pro mato?" if from_player != 0 else f"Você me pediu {label}? Deixa eu pensar..."


def accept_truco():
    g = st.session_state.game
    pending = g["pending_truco"]
    if not pending: return
    g["hand_points"] = pending["value"]
    append_history(f"Pedido aceito! Valendo {g['hand_points']} tentos.")
    g["message"] = f"Aceito! Jogo correndo valendo {g['hand_points']}."
    g["pending_truco"] = None


def refuse_truco():
    g = st.session_state.game
    pending = g["pending_truco"]
    if not pending: return
    winner_team = pending["from_team"]
    g["score"][winner_team] += g["hand_points"]
    append_history(f"Alguém correu! Time {winner_team + 1} leva {g['hand_points']} ponto(s).")
    finish_hand(f"Mão encerrada. O adversário correu!", already_scored=True)


def play_card(player_idx: int, card_idx: int):
    g = st.session_state.game
    if g["finished_hand"] or g["finished_match"] or g["pending_truco"]:
        return

    card = g["hands"][player_idx].pop(card_idx)
    g["table"].append({"player": player_idx, "card": card})
    append_history(f"{player_name(player_idx)} jogou {card.label}")

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
        if len(teams_in_tie) > 1:
            is_empate = True

    if is_empate:
        g["trick_history"].append(-1)
        append_history("A vaza EMPATOU (Cangou)!")
        winner_player = table[highest_indices[0]]["player"]
    else:
        winning_play = table[powers.index(max_power)]
        winner_player = winning_play["player"]
        winner_team = team_of_player(winner_player, g["n_players"])
        g["trick_history"].append(winner_team)
        append_history(f"{player_name(winner_player)} ganhou a vaza com {winning_play['card'].label}.")

    th = g["trick_history"]
    hand_winner = None

    if th.count(0) == 2: hand_winner = 0
    elif th.count(1) == 2: hand_winner = 1
    elif len(th) == 2 and th[0] == -1 and th[1] != -1: hand_winner = th[1]
    elif len(th) == 2 and th[0] != -1 and th[1] == -1: hand_winner = th[0]
    elif len(th) == 3:
        if th[2] == -1:
            hand_winner = th[0] if th[0] != -1 else 0
        else:
            hand_winner = th[2]

    if hand_winner is not None:
        g["score"][hand_winner] += g["hand_points"]
        finish_hand(f"Fim da rodada! Vitória do Time {hand_winner + 1}.", already_scored=True)
        return

    g["table"] = []
    g["trick_no"] += 1
    g["turn"] = winner_player


def finish_hand(msg: str, already_scored: bool = False):
    g = st.session_state.game
    g["finished_hand"] = True
    g["pending_truco"] = None
    g["message"] = msg

    if g["score"][0] >= 12 or g["score"][1] >= 12:
        g["finished_match"] = True
        w = "Você" if g["score"][0] >= 12 else "CPU"
        g["message"] = f"🏆 FIM DA PARTIDA! O grande vencedor foi: {w}!"


def new_hand_keep_score():
    g = st.session_state.game
    n_players, mode, old_score = g["n_players"], g["mode"], g["score"][:]
    init_game(n_players, mode)
    st.session_state.game["score"] = old_score
    st.session_state.game["dealer"] = (g.get("dealer", 0) + 1) % n_players
    st.session_state.game["turn"] = (st.session_state.game["dealer"] + 1) % n_players


def bot_choose_card(player_idx: int) -> int:
    g = st.session_state.game
    hand = g["hands"][player_idx]
    if not hand: return 0
    hand_sorted = sorted(enumerate(hand), key=lambda x: card_power(x[1], g["mode"], g["vira"])[0])
    if not g["table"]: return hand_sorted[0][0]
    best_card = max(g["table"], key=lambda x: card_power(x["card"], g["mode"], g["vira"]))["card"]
    for idx, card in hand_sorted:
        if card_power(card, g["mode"], g["vira"]) > card_power(best_card, g["mode"], g["vira"]):
            return idx
    return hand_sorted[0][0]


def maybe_bot_turns():
    g = st.session_state.game
    safety = 0
    while not g["finished_hand"] and not g["finished_match"] and not g["pending_truco"] and g["turn"] != 0 and safety < 10:
        safety += 1
        player = g["turn"]
        if not g["hands"][player]: continue
        
        # Inteligência Artificial Blefadora do Bot
        avg_p = sum(card_power(c, g["mode"], g["vira"])[0] for c in g["hands"][player]) / len(g["hands"][player])
        if next_bet_value(g["hand_points"]) and avg_p >= 5.0 and random.random() < 0.12:
            ask_truco(player)
            break

        idx = bot_choose_card(player)
        play_card(player, idx)


# --- FLUXO DE EXECUÇÃO PRINCIPAL ---

# 1. Configuração da Barra Lateral (Sidebar)
with st.sidebar:
    st.header("Configurar Jogo")
    n_players = st.radio("Jogadores", [2, 4], format_func=lambda x: "1 vs 1 (Dois)" if x == 2 else "2 vs 2 (Quatro)")
    mode = st.radio("Regra do Baralho", ["Manilha Velha", "Manilha Nova"])
    
    if st.button("Reiniciar com estas Regras", use_container_width=True):
        init_game(n_players, mode)
        st.rerun()

# 2. Proteção contra KeyErrors e Inicialização Segura
if "game" not in st.session_state or "mode" not in st.session_state.game or st.session_state.game["mode"] != mode or st.session_state.game["n_players"] != n_players:
    init_game(n_players, mode)

g = st.session_state.game

# 3. Processa lances automáticos antes de renderizar a tela
if g["pending_truco"] and g["pending_truco"]["to_team"] != team_of_player(0, g["n_players"]):
    # Turno do Bot responder ao Truco do humano
    if random.random() < 0.55: accept_truco()
    else: refuse_truco()
    st.rerun()

maybe_bot_turns()

# --- RENDERIZAÇÃO DA INTERFACE MISTER TRUCO ---

st.markdown("<h1 style='text-align: center; color: white; font-family: monospace; letter-spacing: 4px;'>MISTER TRUCO</h1>", unsafe_allow_html=True)

# Placar Retro Superior
c_sc = st.columns([2, 1, 1, 2])
with c_sc[1]: st.markdown(f"<div class='status-text'>CPU: {g['score'][1]}</div>", unsafe_allow_html=True)
with c_sc[2]: st.markdown(f"<div class='status-text'>MÁRCIO: {g['score'][0]}</div>", unsafe_allow_html=True)

st.divider()

# Divisão do Tabuleiro Verde
col_board, col_panel = st.columns([3, 1])

with col_board:
    # 1. Cartas Ocultas da CPU (Topo)
    cpu_count = len(g["hands"][1]) if g["n_players"] == 2 else len(g["hands"][1]) + len(g["hands"][3])
    cols_cpu = st.columns([1, 1, 1, 1, 1])
    for i in range(min(cpu_count, 3)):
        with cols_cpu[i + 1]:
            st.markdown("<div class='card-back'>R</div>", unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # 2. Centro da Mesa: Placa de "VALENDO X"
    c_val, _ = st.columns([1, 4])
    with c_val:
        st.markdown(f"<div style='text-align: center; color: #7ca982; font-family: monospace; font-size:14px;'>VALENDO<br/><span style='font-size: 50px; font-weight: bold; color: white;'>{g['hand_points']}</span></div>", unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # 3. Suas Cartas Ativas (Baixo)
    cols_player = st.columns([1, 1, 1, 1, 1])
    human_turn = g["turn"] == 0 and not g["pending_truco"] and not g["finished_hand"]
    
    for i, card in enumerate(g["player_hand"] if g["finished_hand"] else g["hands"][0]):
        with cols_player[i + 1]:
            s_class = SUIT_CLASSES[card.suit]
            st.markdown(f"<div class='card-played {s_class}'><div>{card.rank}</div><div style='font-size: 36px;'>{card.suit}</div></div>", unsafe_allow_html=True)
            if st.button("Jogar", key=f"p_btn_{i}", disabled=not human_turn, use_container_width=True):
                play_card(0, i)
                st.rerun()

    st.markdown("<br/><br/>", unsafe_allow_html=True)

    # 4. Botões de Ações de Aumento de Aposta
    cols_act = st.columns([2, 1, 1, 2])
    next_val = next_bet_value(g["hand_points"])
    truco_lbl = "TRUCO" if next_val == 3 else f"PEDIR {next_val}" if next_val else "MÁXIMO"
    
    with cols_act[1]:
        if st.button(truco_lbl, disabled=not next_val or not human_turn, use_container_width=True):
            ask_truco(0)
            st.rerun()
            
    with cols_act[2]:
        if st.button("CORRER", disabled=not human_turn, use_container_width=True):
            g["score"][1] += g["hand_points"]
            finish_hand("Você correu da rodada!", already_scored=True)
            st.rerun()

with col_panel:
    # Balão de Provocação/Fala da Inteligência Artificial
    st.markdown(f"<div class='balloon-cpu'><b>💻 CPU diz:</b><br/><i>\"{g['message']}\"</i></div>", unsafe_allow_html=True)

    # Resposta de Tomada de Decisão do Jogador Humano (Se trucado)
    if g["pending_truco"] and g["pending_truco"]["to_team"] == team_of_player(0, g["n_players"]):
        st.error(f"Adversário pediu {g['pending_truco']['value']}!")
        c_choice = st.columns(2)
        if c_choice[0].button("QUERO!", use_container_width=True):
            accept_truco()
            st.rerun()
        if c_choice[1].button("CORRER", use_container_width=True):
            refuse_truco()
            st.rerun()

    # Bloco Informativo da Regra do Vira (Se Manilha Nova)
    if g["mode"] == "Manilha Nova" and g["vira"]:
        m_rank = get_next_rank(g['vira'].rank)
        st.markdown(f"<div style='background-color: rgba(0,0,0,0.3); padding: 10px; border-radius: 8px; color: white; text-align: center; margin-bottom: 15px;'>VIRA: <b>{g['vira'].label}</b><br/>Manilhas da vez: <b style='color:#38bdf8;'>{m_rank}</b></div>", unsafe_allow_html=True)

    # Cartas jogadas em andamento na mesa
    st.markdown("<p style='color: white; font-weight: bold; margin-bottom: 5px;'>Cartas na Mesa:</p>", unsafe_allow_html=True)
    if not g["table"]:
        st.caption("Nenhuma carta na mesa.")
    else:
        for play in g["table"]:
            c = play["card"]
            s_class = SUIT_CLASSES[c.suit]
            st.markdown(
                f"""
                <div style="display: flex; align-items: center; gap: 12px; background: rgba(0,0,0,0.3); padding: 6px; border-radius: 6px; margin-bottom: 5px;">
                    <div class='card-played {s_class}' style='width: 45px; height: 60px; font-size: 16px; box-shadow:none;'>{c.label}</div>
                    <div style='color: white; font-size: 13px;'><b>{player_name(play['player'])}</b> jogou</div>
                </div>
                """, unsafe_allow_html=True
            )

    st.divider()
    if st.button("Avançar para Próxima Mão", disabled=not g["finished_hand"] or g["finished_match"], use_container_width=True):
        new_hand_keep_score()
        st.rerun()

# Histórico de texto reduzido no rodapé do painel lateral
with st.expander("Histórico de Rodadas"):
    for log in g["history"]:
        st.markdown(f"<small style='color: gray;'>• {log}</small>", unsafe_allow_html=True)

if g["finished_match"]:
    st.balloons()
