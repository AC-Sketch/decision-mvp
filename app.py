import random
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
import streamlit as st

# =========================================================
# TRUCO STREAMLIT - Versão Customizável
# - Manilha Velha (Fixa) vs Manilha Nova (Variável/Vira)
# - 2 Jogadores (Humano vs Bot) ou 4 Jogadores (Duplas)
# - Sistema de Truco, 6, 9 e 12
# - Regra de empate (Cangada) inclusa
# =========================================================

st.set_page_config(
    page_title="Truco Customizável",
    page_icon="🃏",
    layout="wide",
)

SUITS = ["♦", "♠", "♥", "♣"]  # Ouros, Espadas, Copas, Paus
SUIT_NAMES = {"♦": "Ouros", "♠": "Espadas", "♥": "Copas", "♣": "Paus"}
SUIT_POWER = {"♦": 1, "♠": 2, "♥": 3, "♣": 4}

# Ordem base de força (do mais fraco ao mais forte) para o baralho limpo tradicional
BASE_RANK_ORDER = ["Q", "J", "K", "A", "2", "3"]
# Na manilha velha, 4 e 7 entram no topo da força base antes dos naipes desempatarem
MANILHA_VELHA_ORDER = ["Q", "J", "K", "A", "2", "3", "7", "4"]

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
        return f"{self.rank} de {SUIT_NAMES[self.suit]}"


def get_next_rank(rank: str) -> str:
    """Retorna o rank subsequente para determinar a manilha nova (regra do vira)."""
    order = ["4", "5", "6", "7", "Q", "J", "K", "A", "2", "3"]
    try:
        idx = order.index(rank)
        return order[(idx + 1) % len(order)]
    except ValueError:
        return "4"


def card_power(card: Card, mode: str, vira: Optional[Card] = None) -> Tuple[int, int]:
    """
    Calcula a força da carta. 
    Retorna uma tupla (Força do Rank, Força do Naipe).
    O naipe só desempata se a carta for uma manilha legítima.
    """
    if mode == "Manilha Velha":
        # 4, 7, A, 3, 2, K, J, Q (Paus > Copas > Espadas > Ouros para as manilhas)
        ranks = ["Q", "J", "K", "2", "3", "A", "7", "4"]
        power_idx = ranks.index(card.rank)
        # Se for 4, 7, A ou 3, os naipes desempatam (Manilhas Fixas tradicionais)
        is_manilha = card.rank in ["4", "7", "A", "3"]
        suit_p = SUIT_POWER[card.suit] if is_manilha else 0
        return (power_idx, suit_p)
    else:
        # Manilha Nova (Baseado no Vira)
        manilha_rank = get_next_rank(vira.rank) if vira else ""
        if card.rank == manilha_rank:
            # É manilha! Força máxima e desempatada por naipe
            return (100, SUIT_POWER[card.suit])
        else:
            # Carta comum
            order = ["4", "5", "6", "7", "Q", "J", "K", "A", "2", "3"]
            power_idx = order.index(card.rank) if card.rank in order else 0
            return (power_idx, 0)


def make_deck(mode: str) -> List[Card]:
    # No Truco com manilha nova/vira, costuma-se usar o baralho completo (ou limpo dependendo da região). 
    # Usaremos o baralho tradicional do truco (sem 8, 9, 10).
    ranks = ["4", "5", "6", "7", "Q", "J", "K", "A", "2", "3"] if mode == "Manilha Nova" else ["4", "7", "A", "3", "2", "K", "J", "Q"]
    return [Card(rank, suit) for rank in ranks for suit in SUITS]


def team_of_player(player_idx: int, n_players: int) -> int:
    return player_idx if n_players == 2 else player_idx % 2


def player_name(i: int) -> str:
    return "Você" if i == 0 else f"Bot {i}"


def init_game(n_players: int, mode: str):
    deck = make_deck(mode)
    random.shuffle(deck)

    # Distribui as cartas
    hands = [[] for _ in range(n_players)]
    for _ in range(3):
        for p in range(n_players):
            hands[p].append(deck.pop())

    # Define o vira se for Manilha Nova
    vira = deck.pop() if mode == "Manilha Nova" else None

    st.session_state.game = {
        "n_players": n_players,
        "mode": mode,
        "hands": hands,
        "vira": vira,
        "table": [],
        "turn": 0,
        "dealer": 0,
        "round_no": 1,
        "trick_no": 1,
        "hand_points": 1,
        "score": [0, 0],
        "trick_history": [],  # Guarda quem ganhou cada vaza (0, 1, ou -1 para empate)
        "history": [],
        "finished_hand": False,
        "finished_match": False,
        "message": f"Nova mão iniciada ({mode}). Sua vez!",
        "pending_truco": None,
    }


def reset_match(n_players: int, mode: str):
    init_game(n_players, mode)


def append_history(msg: str):
    st.session_state.game["history"].insert(0, msg)
    st.session_state.game["history"] = st.session_state.game["history"][:20]


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
        g["message"] = "A mão já está valendo 12!"
        return

    g["pending_truco"] = {
        "from_team": from_team,
        "to_team": 1 - from_team,
        "value": new_value,
        "from_player": from_player,
    }

    label = "TRUCO!" if new_value == 3 else f"{new_value}!"
    append_history(f"{player_name(from_player)} gritou {label}")
    g["message"] = f"{player_name(from_player)} pediu {label}. Aguardando resposta do oponente."


def accept_truco():
    g = st.session_state.game
    pending = g["pending_truco"]
    if not pending:
        return

    g["hand_points"] = pending["value"]
    append_history(f"Time {pending['to_team'] + 1} aceitou! A rodada agora vale {g['hand_points']} pontos.")
    g["message"] = f"Pedido aceito! O jogo continuará valendo {g['hand_points']}."
    g["pending_truco"] = None


def refuse_truco():
    g = st.session_state.game
    pending = g["pending_truco"]
    if not pending:
        return

    winner_team = pending["from_team"]
    previous_value = g["hand_points"]
    g["score"][winner_team] += previous_value
    append_history(f"Time {pending['to_team'] + 1} correu. Time {winner_team + 1} faturou {previous_value} ponto(s).")
    finish_hand(f"Time {winner_team + 1} venceu a mão porque o adversário correu.", already_scored=True)


def bot_accepts_truco() -> bool:
    g = st.session_state.game
    to_team = g["pending_truco"]["to_team"]
    bot_cards = []
    for p, hand in enumerate(g["hands"]):
        if team_of_player(p, g["n_players"]) == to_team and p != 0:
            bot_cards.extend(hand)

    if not bot_cards:
        return random.random() < 0.5
    
    avg_power = sum(card_power(c, g["mode"], g["vira"])[0] for c in bot_cards) / len(bot_cards)
    return random.random() < min(0.85, max(0.2, avg_power / 10 if g["mode"] == "Manilha Nova" else avg_power / 7))


def maybe_bot_respond_truco():
    g = st.session_state.game
    pending = g.get("pending_truco")
    if not pending or pending["to_team"] == team_of_player(0, g["n_players"]):
        return

    if bot_accepts_truco():
        accept_truco()
    else:
        refuse_truco()


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
        g["message"] = f"Vez de {player_name(g['turn'])}."


def resolve_trick():
    g = st.session_state.game
    table = g["table"]

    # Calcula o poder de todas as cartas na mesa
    powers = [card_power(play["card"], g["mode"], g["vira"]) for play in table]
    max_power = max(powers, key=lambda x: (x[0], x[1]))
    
    # Verifica se houve empate na maior força da mesa (cangada)
    highest_indices = [i for i, p in enumerate(powers) if p[0] == max_power[0] and p[1] == max_power[1]]
    
    is_empate = False
    if len(highest_indices) > 1:
        # Se os jogadores que empataram são de times opostos, é uma cangada (empate)
        teams_in_tie = {team_of_player(table[i]["player"], g["n_players"]) for i in highest_indices}
        if len(teams_in_tie) > 1:
            is_empate = True

    if is_empate:
        g["trick_history"].append(-1)
        append_history(f"Vaza {g['trick_no']} EMPATOU (Cangou)!")
        # Em caso de empate, quem joga primeiro na próxima é quem amarrou a vaza (ou mantém o turno anterior)
        winner_player = table[highest_indices[0]]["player"]
    else:
        winning_play = table[powers.index(max_power)]
        winner_player = winning_play["player"]
        winner_team = team_of_player(winner_player, g["n_players"])
        g["trick_history"].append(winner_team)
        append_history(f"Vaza {g['trick_no']}: {player_name(winner_player)} ganhou com {winning_play['card'].label}.")

    # Verificação das regras de Melhor de 3 com empates
    th = g["trick_history"]
    hand_winner = None

    # Caso 1: Alguém fez duas vazas directas
    if th.count(0) == 2: hand_winner = 0
    elif th.count(1) == 2: hand_winner = 1
    # Caso 2: Houve empate na primeira vaza -> Quem ganhar a segunda ganha a mão
    elif len(th) == 2 and th[0] == -1 and th[1] != -1:
        hand_winner = th[1]
    # Caso 3: Primeira vaza teve dono, segunda empatou -> O dono da primeira ganha
    elif len(th) == 2 and th[0] != -1 and th[1] == -1:
        hand_winner = th[0]
    # Caso 4: Todas empataram ou empatou na terceira -> Quem ganhou a primeira leva
    elif len(th) == 3:
        if th[2] == -1:  # Terceira empatou
            hand_winner = th[0] if th[0] != -1 else 0 # Se todas empatarem, ponto do Dealer (Mão de Ferro simplificada pro Time 1)
        else:
            hand_winner = th[2]

    if hand_winner is not None and hand_winner != -1:
        g["score"][hand_winner] += g["hand_points"]
        finish_hand(f"Time {hand_winner + 1} venceu a rodada e marcou {g['hand_points']} ponto(s)!", already_scored=True)
        return

    g["table"] = []
    g["trick_no"] += 1
    g["turn"] = winner_player
    g["message"] = f"Vaza finalizada. {player_name(winner_player)} puxa a próxima rodada."


def finish_hand(msg: str, already_scored: bool = False):
    g = st.session_state.game
    g["finished_hand"] = True
    g["pending_truco"] = None
    g["message"] = msg

    if g["score"][0] >= 12 or g["score"][1] >= 12:
        g["finished_match"] = True
        winner = 0 if g["score"][0] >= 12 else 1
        g["message"] = f"🏆 FIM DE JOGO! Time {winner + 1} venceu a partida por {g['score'][0]} x {g['score'][1]}!"


def new_hand_keep_score():
    g = st.session_state.game
    n_players = g["n_players"]
    mode = g["mode"]
    old_score = g["score"][:]
    
    init_game(n_players, mode)
    st.session_state.game["score"] = old_score
    st.session_state.game["dealer"] = (g.get("dealer", 0) + 1) % n_players
    st.session_state.game["turn"] = (st.session_state.game["dealer"] + 1) % n_players
    st.session_state.game["message"] = f"Nova mão distribuída. Vez de {player_name(st.session_state.game['turn'])}."


def bot_choose_card(player_idx: int) -> int:
    g = st.session_state.game
    hand = g["hands"][player_idx]
    hand_sorted = sorted(enumerate(hand), key=lambda x: card_power(x[1], g["mode"], g["vira"])[0])
    
    if not g["table"]:
        return hand_sorted[0][0] # Joga a mais baixa se for o primeiro

    best_table_card = max(g["table"], key=lambda x: card_power(x["card"], g["mode"], g["vira"]))["card"]
    best_table_pow = card_power(best_table_card, g["mode"], g["vira"])

    # Tenta matar com a menor carta possível que vença a mesa
    for idx, card in hand_sorted:
        if card_power(card, g["mode"], g["vira"]) > best_table_pow:
            return idx
            
    return hand_sorted[0][0]


def maybe_bot_turns():
    g = st.session_state.game
    safety = 0
    while (
        not g["finished_hand"]
        and not g["finished_match"]
        and not g["pending_truco"]
        and g["turn"] != 0
        and safety < 12
    ):
        safety += 1
        player = g["turn"]
        hand = g["hands"][player]
        
        if not hand:
            continue

        # Inteligência artificial de blefe/truco randômico para os bots
        avg_power = sum(card_power(c, g["mode"], g["vira"])[0] for c in hand) / len(hand)
        if next_bet_value(g["hand_points"]) and avg_power >= 5 and random.random() < 0.15:
            ask_truco(player)
            break

        idx = bot_choose_card(player)
        play_card(player, idx)


# --- INTERFACE GRÁFICA (RENDERERS) ---

def main():
    st.title("🃏 Truco Streamlit Pro")
    st.caption("Altere os modos de jogo na barra lateral e divirta-se!")

    with st.sidebar:
        st.header("Configurações da Partida")
        n_players = st.radio(
            "Quantidade de Jogadores",
            [2, 4],
            format_func=lambda x: "1 vs 1 (Dois Jogadores)" if x == 2 else "2 vs 2 (Quatro Jogadores / Duplas)"
        )
        
        mode = st.radio(
            "Regra da Manilha",
            ["Manilha Velha", "Manilha Nova"],
            help="Velha: Manilhas fixas (4, 7, A, 3). Nova: Manilha definida pelo Vira (+1 acima)."
        )

        if "game" not in st.session_state:
            init_game(n_players, mode)

        if st.button("Reiniciar Partida com Configurações", use_container_width=True):
            reset_match(n_players, mode)
            st.rerun()

        st.divider()
        st.markdown(
            f"""
            **Regras Ativas:**
            * Modo: {n_players} Jogadores.
            * Tipo: {mode}.
            * Pontuação máxima: 12 Tentos.
            """
        )

    g = st.session_state.game

    # Se o usuário mudou configurações no rádio sem clicar no botão, reseta preventivamente
    if g["n_players"] != n_players or g["mode"] != mode:
        init_game(n_players, mode)
        g = st.session_state.game

    maybe_bot_respond_truco()
    maybe_bot_turns()

    # --- PLACAR ---
    st.markdown("### Placar")
    c1, c2, c3 = st.columns(3)
    c1.metric("Sua Dupla / Você" if g["n_players"] == 4 else "Você (Time 1)", g["score"][0])
    c2.metric("Bots Adversários" if g["n_players"] == 4 else "Bot (Time 2)", g["score"][1])
    c3.metric("Esta Mão Vale:", f"{g['hand_points']} ponto(s)")
    st.progress(min(max(g["score"][0], g["score"][1]) / 12, 1.0))

    st.info(f"💬 {g['message']}")

    # --- ZONA DE VIRA (Se aplicável) ---
    if g["mode"] == "Manilha Nova" and g["vira"]:
        manilha_da_vez = get_next_rank(g["vira"].rank)
        st.markdown(
            f"""
            <div style="background-color:#1e293b; padding:15px; border-radius:10px; text-align:center; margin-bottom:15px;">
                <span style="color:gray; font-size:14px;">CARTA VIRA</span><br/>
                <b style="font-size:24px; color:#38bdf8;">{g['vira'].label}</b> ({g['vira'].full_name})<br/>
                <span style="font-size:14px;">As manilhas da rodada são as cartas de rank: <b>{manilha_da_vez}</b></span>
            </div>
            """, unsafe_allow_html=True
        )

    left, right = st.columns([2, 1])

    with left:
        # --- MESA ---
        st.markdown("#### Mesa")
        if not g["table"]:
            st.caption("A mesa está limpa. Aguardando jogadas.")
        else:
            cols_table = st.columns(len(g["table"]))
            for col, play in zip(cols_table, g["table"]):
                with col:
                    st.markdown(
                        f"""
                        <div style="border:2px solid #4b5563; border-radius:10px; padding:12px; text-align:center; background-color:#0f172a;">
                            <div style="font-size:28px; font-weight:bold;">{play['card'].label}</div>
                            <div style="color:#9ca3af; font-size:12px;">{player_name(play['player'])}</div>
                        </div>
                        """, unsafe_allow_html=True
                    )

        st.divider()

        # --- MÃO DO JOGADOR HUMANO ---
        st.markdown("#### Suas Cartas")
        human_turn = g["turn"] == 0 and not g["pending_truco"] and not g["finished_hand"]
        
        if not g["hands"][0]:
            st.caption("Você não tem cartas restantes nesta mão.")
        else:
            cols_hand = st.columns(3)
            for i, card in enumerate(g["hands"][0]):
                with cols_hand[i]:
                    lbl = f"🂠 {card.label}\n\n({card.rank})"
                    if st.button(lbl, key=f"c_{i}_{card.label}", disabled=not human_turn, use_container_width=True):
                        play_card(0, i)
                        st.rerun()

        st.divider()

        # --- AÇÕES DE CLIQUE ---
        st.markdown("#### Comandos de Jogo")
        b_cols = st.columns(3)
        
        # Botão de Aumentar Aposta
        next_val = next_bet_value(g["hand_points"])
        btn_label = "Pedir Truco" if next_val == 3 else f"Pedir {next_val}" if next_val else "Limite de 12 atingido"
        
        if b_cols[0].button(btn_label, disabled=not next_val or g["finished_hand"] or g["finished_match"] or g["turn"] != 0, use_container_width=True):
            ask_truco(0)
            st.rerun()

        # Botão de Passar para Próxima Mão
        if b_cols[1].button("Avançar para Nova Mão", disabled=not g["finished_hand"] or g["finished_match"], use_container_width=True):
            new_hand_keep_score()
            st.rerun()

        # Resposta caso o Bot tenha trucado o Humano
        pending = g.get("pending_truco")
        if pending and pending["to_team"] == team_of_player(0, g["n_players"]):
            st.warning(f"⚠️ O adversário pediu {pending['value']}! O que deseja fazer?")
            r_cols = st.columns(2)
            if r_cols[0].button("👍 Aceitar", key="acc"):
                accept_truco()
                st.rerun()
            if r_cols[1].button("🏃‍♂️ Correr (Ir pro baralho)", key="ref"):
                refuse_truco()
                st.rerun()

    with right:
        # --- HISTÓRICO ---
        st.markdown("#### Histórico de Lances")
        if not g["history"]:
            st.caption("Nenhum lance efetuado.")
        else:
            for item in g["history"]:
                st.markdown(f"<small>• {item}</small>", unsafe_allow_html=True)

    # Modo Debug / Ver cartas dos Bots ocultos
    with st.expander("🕵️‍♂️ Espiar cartas dos Bots (Modo Debug)"):
        for p in range(1, g["n_players"]):
            c_lines = " | ".join(c.label for c in g["hands"][p]) if g["hands"][p] else "Sem cartas"
            st.write(f"**{player_name(p)}:** {c_lines}")

    if g["finished_match"]:
        st.balloons()


if __name__ == "__main__":
    main()
