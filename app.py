import random
import streamlit as st
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple

# =========================================================
# MISTER TRUCO - ARQUITETURA DE MOTOR DE JOGO PROFISSIONAL
# Baseado nos melhores padrões de motores de cartas do GitHub
# =========================================================

st.set_page_config(page_title="Mister Truco Pro", page_icon="🃏", layout="wide")

# --- INTERFACE DE ALTO CONTRASTE (CSS DETALHADO) ---
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
    .card-back {
        border: 2px solid #ffffff; border-radius: 8px;
        background-color: #11331c;
        background-image: repeating-linear-gradient(45deg, #1e4a2b 0, #1e4a2b 2px, transparent 0, transparent 50%);
        background-size: 8px 8px;
        height: 95px; max-width: 70px; margin: 0 auto;
        display: flex; align-items: center; justify-content: center;
        color: #559966; font-size: 24px; font-weight: bold;
        box-shadow: 3px 3px 6px rgba(0,0,0,0.4);
    }
    .card-played {
        border: 2px solid #000000 !important; border-radius: 8px !important;
        background-color: #ffffff !important; color: #000000 !important; 
        height: 105px; max-width: 80px; margin: 0 auto 4px auto;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        font-size: 24px; font-weight: bold; box-shadow: 3px 3px 8px rgba(0,0,0,0.5);
    }
    .card-mini {
        border: 1.5px solid #000000 !important; border-radius: 5px !important;
        background-color: #ffffff !important; color: #000000 !important; 
        width: 50px; height: 68px;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        font-size: 18px; font-weight: bold; box-shadow: 1px 1px 4px rgba(0,0,0,0.3);
    }
    .red-suit { color: #dc2626 !important; font-size: 30px; line-height: 1; }
    .black-suit { color: #000000 !important; font-size: 30px; line-height: 1; }
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

# --- MODELO DE DADOS ENCAPSULADO ---
SUITS_MAP = {"Ouros": "♦", "Espadas": "♠", "Copas": "♥", "Paus": "♣"}
SUIT_COLORS = {"Ouros": "red-suit", "Espadas": "black-suit", "Copas": "red-suit", "Paus": "black-suit"}

@dataclass
class Card:
    rank: str
    suit: str  # 'Ouros', 'Espadas', 'Copas', 'Paus'

    @property
    def symbol(self) -> str: return SUITS_MAP[self.suit]
    @property
    def color(self) -> str: return SUIT_COLORS[self.suit]
    @property
    def label(self) -> str: return f"{self.rank}{self.symbol}"

# --- ENGINE LOGIC (MÁQUINA DE ESTADOS DO TRUCO) ---
class TrucoMatch:
    def __init__(self, n_players: int, mode: str):
        self.n_players = n_players
        self.mode = mode
        self.score = [0, 0] # [Humano/Dupla, CPU]
        self.dealer = 0
        self.start_new_hand()

    def get_deck(self) -> List[Card]:
        suits = ["Ouros", "Espadas", "Copas", "Paus"]
        if self.mode == "Manilha Velha":
            # Apenas manilhas fixas e cartas limpas tradicionais
            cards = [Card(r, s) for r in ["3", "2", "A", "K", "J", "Q"] for s in suits]
            cards += [Card("4", "Paus"), Card("7", "Copas"), Card("A", "Espadas"), Card("7", "Ouros")]
            return cards
        else:
            return [Card(r, s) for r in ["4", "5", "6", "7", "Q", "J", "K", "A", "2", "3"] for s in suits]

    def get_card_power(self, card: Card) -> int:
        if self.mode == "Manilha Velha":
            if card.rank == "4" and card.suit == "Paus": return 104     # Zap
            if card.rank == "7" and card.suit == "Copas": return 103    # Copilha
            if card.rank == "A" and card.suit == "Espadas": return 102  # Espadilha
            if card.rank == "7" and card.suit == "Ouros": return 101    # Pica-fumo
            order = ["Q", "J", "K", "A", "2", "3"]
            return order.index(card.rank) if card.rank in order else -1
        else:
            # Manilha Nova baseada no Vira
            order = ["4", "5", "6", "7", "Q", "J", "K", "A", "2", "3"]
            next_rank = order[(order.index(self.vira.rank) + 1) % len(order)]
            if card.rank == next_rank:
                suit_pow = {"Ouros": 1, "Espadas": 2, "Copas": 3, "Paus": 4}
                return 100 + suit_pow[card.suit]
            return order.index(card.rank)

    def start_new_hand(self):
        deck = self.get_deck()
        random.shuffle(deck)
        
        self.hands = [[] for _ in range(self.n_players)]
        for _ in range(3):
            for p in range(self.n_players):
                self.hands[p].append(deck.pop())
                
        self.vira = deck.pop() if self.mode == "Manilha Nova" else None
        self.table = []
        self.trick_no = 1
        self.hand_points = 1
        self.trick_wins = [] # Histórico de quem ganhou cada vaza (0=Humano, 1=CPU, -1=Empate)
        self.finished_hand = False
        self.pending_truco = None
        
        # O "Mão" (quem começa) é o jogador após o distribuidor (Dealer)
        self.hand_starter = (self.dealer + 1) % self.n_players
        self.turn = self.hand_starter
        self.message = f"Nova mão! {self.get_player_name(self.turn)} começa jogando."

    def get_player_name(self, idx: int) -> str:
        return "Você" if idx == 0 else f"Bot {idx}"

    def play_card(self, player_idx: int, card_idx: int):
        if self.finished_hand or self.pending_truco or self.turn != player_idx:
            return
        
        card = self.hands[player_idx].pop(card_idx)
        self.table.append({"player": player_idx, "card": card})
        
        # Próximo turno
        if len(self.table) < self.n_players:
            self.turn = (self.turn + 1) % self.n_players
        else:
            self.resolve_trick()

    def resolve_trick(self):
        # Avaliação técnica de força das cartas na mesa
        powers = [self.get_card_power(p["card"]) for p in self.table]
        max_pow = max(powers)
        winners = [i for i, pow_val in enumerate(powers) if pow_val == max_pow]
        
        # Avalia se jogadores de equipes distintas empataram (Cangada)
        is_tie = False
        if len(winners) > 1:
            teams = {w_idx % 2 for w_idx in winners}
            if len(teams) > 1: is_tie = True
            
        if is_tie:
            vaza_winner_team = -1
            self.trick_wins.append(-1)
            # Em caso de empate, quem puxa a próxima é o jogador da vaza que amarrou
            next_puller = self.table[winners[0]]["player"]
            self.message = "A vaza empatou! Quem amarrou joga primeiro."
        else:
            winning_play = self.table[powers.index(max_pow)]
            next_puller = winning_play["player"]
            vaza_winner_team = next_puller % 2
            self.trick_wins.append(vaza_winner_team)
            self.message = f"{self.get_player_name(next_puller)} ganhou a vaza."

        # Processamento das regras de Melhor de 3 do Truco
        tw = self.trick_wins
        hand_winner_team = None
        
        if tw.count(0) == 2: hand_winner_team = 0
        elif tw.count(1) == 2: hand_winner_team = 1
        elif len(tw) == 2 and tw[0] == -1 and tw[1] != -1: hand_winner_team = tw[1]
        elif len(tw) == 2 and tw[0] != -1 and tw[1] == -1: hand_winner_team = tw[0]
        elif len(tw) == 3:
            if tw[2] == -1: hand_winner_team = tw[0] if tw[0] != -1 else 0
            else: hand_winner_team = tw[2]

        if hand_winner_team is not None:
            self.score[hand_winner_team] += self.hand_points
            self.finished_hand = True
            self.message = f"Fim da mão! Time {hand_winner_team + 1} ganhou {self.hand_points} ponto(s)."
            self.dealer = (self.dealer + 1) % self.n_players
            return

        # Limpa mesa e passa o turno para quem ganhou a vaza
        self.table = []
        self.trick_no += 1
        self.turn = next_puller

    def bot_play_logic(self):
        # AI básica baseada em busca heurística da melhor carta disponível
        hand = self.hands[self.turn]
        if not hand: return
        
        # Inteligência de blefe randômico e Truco automático
        if not self.pending_truco and self.hand_points < 12 and random.random() < 0.08:
            self.cpu_ask_truco()
            return
            
        hand_powers = [self.get_card_power(c) for c in hand]
        if not self.table:
            chosen_idx = hand_powers.index(min(hand_powers)) # Se for o primeiro, sai por baixo
        else:
            table_max = max([self.get_card_power(p["card"]) for p in self.table])
            # Tenta matar a mesa com o menor recurso possível
            options = [i for i, p in enumerate(hand_powers) if p > table_max]
            chosen_idx = hand_powers.index(min([hand_powers[o] for o in options])) if options else hand_powers.index(min(hand_powers))
            
        self.play_card(self.turn, chosen_idx)

    def cpu_ask_truco(self):
        next_val = {1:3, 3:6, 6:9, 9:12}.get(self.hand_points)
        if next_val:
            self.pending_truco = {"from_team": 1, "to_team": 0, "value": next_val}
            self.message = f"A CPU gritou {next_val if next_val > 3 else 'TRUCO'}! Vai correr ou vai aceitar?"

    def human_ask_truco(self):
        next_val = {1:3, 3:6, 6:9, 9:12}.get(self.hand_points)
        if next_val:
            self.pending_truco = {"from_team": 0, "to_team": 1, "value": next_val}
            self.message = f"Você pediu {next_val if next_val > 3 else 'TRUCO'}! Aguardando a CPU responder..."


# --- CONTROLADOR DE SESSÃO DO STREAMLIT ---
c_top_title, c_top_players, c_top_mode, c_top_reset = st.columns([1, 1.2, 1.2, 0.8])

with c_top_title:
    st.markdown("<h3 style='color: white; font-family: monospace; margin:0; padding-top:5px;'>MISTER TRUCO</h3>", unsafe_allow_html=True)
with c_top_players:
    n_players = st.radio("Jogadores", [2, 4], format_func=lambda x: "1v1 (Dois)" if x == 2 else "2v2 (Quatro)", label_visibility="collapsed")
with c_top_mode:
    mode = st.radio("Regras", ["Manilha Velha", "Manilha Nova"], label_visibility="collapsed")
with c_top_reset:
    apply_rules = st.button("Aplicar Regras", use_container_width=True)

# Reinicialização segura da máquina de estados do Engine
if "engine" not in st.session_state or apply_rules or st.session_state.engine.mode != mode or st.session_state.engine.n_players != n_players:
    st.session_state.engine = TrucoMatch(n_players, mode)

eng = st.session_state.engine

# --- SISTEMA DE RESPOSTA AUTOMÁTICA DA CPU ---
if eng.pending_truco and eng.pending_truco["to_team"] == 1:
    if random.random() < 0.6:  # Decisão randômica estável do bot
        eng.accept_truco()
    else:
        eng.score[0] += eng.hand_points
        eng.start_new_hand()
        eng.message = "A CPU correu do seu desafio! Você ganhou os pontos."
    st.rerun()

# Processamento de turnos automáticos dos Bots em cascata
if not eng.finished_hand and eng.turn != 0 and not eng.pending_truco:
    eng.bot_play_logic()
    st.rerun()

# --- INTERFACE GRÁFICA ATUALIZADA ---
c_score = st.columns([2, 1])
with c_score[0]:
    st.markdown(f"<div class='status-text'>CPU: {eng.score[1]}   ▏   VOCÊ: {eng.score[0]}</div>", unsafe_allow_html=True)
with c_score[1]:
    st.markdown(f"<div class='status-text' style='background-color:#11331c;'>VALENDO: {eng.hand_points} PTS</div>", unsafe_allow_html=True)

st.markdown("<hr/>", unsafe_allow_html=True)

col_board, col_panel = st.columns([2.8, 1.2])

with col_board:
    # 1. Zona Superior: Cartas Ocultas da CPU
    cpu_cards_left = len(eng.hands[1]) if eng.n_players == 2 else len(eng.hands[1]) + len(eng.hands[3])
    cols_cpu = st.columns([1, 1, 1, 1, 1])
    for i in range(min(cpu_cards_left, 3)):
        with cols_cpu[i + 1]:
            st.markdown("<div class='card-back'>R</div>", unsafe_allow_html=True)

    st.markdown("<div style='margin: 15px 0;'></div>", unsafe_allow_html=True)

    # 2. Zona Inferior: Suas Cartas Ativas (Fundo Branco Isolado)
    cols_player = st.columns([1, 1, 1, 1, 1])
    is_my_turn = (eng.turn == 0 and not eng.pending_truco and not eng.finished_hand)
    
    for idx, card in enumerate(eng.hands[0]):
        with cols_player[idx + 1]:
            st.markdown(f"""
                <div class='card-played'>
                    <div style='font-size:18px; margin-bottom:-4px;'>{card.rank}</div>
                    <div class='{card.color}'>{card.symbol}</div>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Jogar", key=f"btn_{idx}_{card.label}", disabled=not is_my_turn, use_container_width=True):
                eng.play_card(0, idx)
                st.rerun()

    st.markdown("<div style='margin: 15px 0;'></div>", unsafe_allow_html=True)

    # 3. Comandos de Aposta da Mesa
    cols_act = st.columns([1.2, 1, 1, 1.2])
    next_bet = {1:3, 3:6, 6:9, 9:12}.get(eng.hand_points)
    btn_label = "TRUCO" if next_bet == 3 else f"PEDIR {next_bet}" if next_bet else "MÁXIMO"
    
    with cols_act[1]:
        if st.button(btn_label, key="action_truco_main", disabled=not next_bet or not is_my_turn, use_container_width=True):
            eng.human_ask_truco()
            st.rerun()
    with cols_act[2]:
        if st.button("CORRER", key="action_fold_main", disabled=not is_my_turn, use_container_width=True):
            eng.score[1] += eng.hand_points
            eng.start_new_hand()
            eng.message = "Você correu da mão."
            st.rerun()

with col_panel:
    # Caixa de Diálogo do Bot
    st.markdown(f"<div class='balloon-cpu'><b>💻 CPU diz:</b><br/><i>\"{eng.message}\"</i></div>", unsafe_allow_html=True)

    # Interface de Desafio (Se trucado pela CPU)
    if eng.pending_truco and eng.pending_truco["to_team"] == 0:
        st.markdown(f"<div class='challenge-alert'>⚠️ Desafio valendo {eng.pending_truco['value']}!</div>", unsafe_allow_html=True)
        c_ch = st.columns(2)
        if c_ch[0].button("ACEITAR", key="accept_challenge_btn", use_container_width=True):
            eng.accept_truco()
            st.rerun()
        if c_ch[1].button("CORRER", key="fold_challenge_btn", use_container_width=True):
            eng.score[1] += eng.hand_points
            eng.start_new_hand()
            st.rerun()

    # Informações da Manilha de Vira
    if eng.mode == "Manilha Nova" and eng.vira:
        order = ["4", "5", "6", "7", "Q", "J", "K", "A", "2", "3"]
        m_rank = order[(order.index(eng.vira.rank) + 1) % len(order)]
        st.markdown(f"<div style='background-color: rgba(0,0,0,0.4); padding: 5px; border-radius: 6px; color: white; text-align: center; font-size:11px; margin-bottom:10px;'>VIRA: <b>{eng.vira.label}</b>   |   MANILHA: <b style='color:#38bdf8;'>{m_rank}</b></div>", unsafe_allow_html=True)

    # EXIBIÇÃO EM TEMPO REAL DAS CARTAS JOGADAS NA MESA
    st.markdown("<p style='color: white; font-weight: bold; margin: 0; font-size:13px;'>Cartas na Mesa:</p>", unsafe_allow_html=True)
    if not eng.table:
        st.caption("A mesa está limpa.")
    else:
        for play in eng.table:
            c = play["card"]
            st.markdown(f"""
                <div style="display: flex; align-items: center; gap: 12px; background: rgba(0,0,0,0.4); padding: 5px; border-radius: 8px; margin-bottom: 4px;">
                    <div class='card-mini'><div style='font-size:11px;'>{c.rank}</div><div class='{c.color}' style='font-size:18px;'>{c.symbol}</div></div>
                    <div style='color: #ffffff; font-size: 13px;'><b>{eng.get_player_name(play['player'])}</b> jogou</div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='margin: 8px 0;'></div>", unsafe_allow_html=True)
    if st.button("Avançar Próxima Mão", key="system_next_hand", disabled=not eng.finished_hand, use_container_width=True):
        eng.start_new_hand()
        st.rerun()

if eng.score[0] >= 12 or eng.score[1] >= 12:
    st.balloons()
