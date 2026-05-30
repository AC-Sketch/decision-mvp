import random
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
import streamlit as st

# =========================================================
# TRUCO STREAMLIT - INTERFACE VISUAL RETRO (MISTER TRUCO)
# =========================================================

st.set_page_config(
    page_title="Mister Truco Streamlit",
    page_icon="🃏",
    layout="wide",
)

# Estilização global para imitar o "tapete verde" do jogo clássico
st.markdown(
    """
    <style>
    .stApp {
        background-color: #1a4a2b; /* Verde escuro de mesa de cartas */
    }
    .status-text {
        color: #ffffff;
        font-family: 'Courier New', Courier, monospace;
        font-weight: bold;
        text-align: center;
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
        font-size: 24px;
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
    .red-suit {
        color: #dc2626;
    }
    .black-suit {
        color: #000000;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

SUITS = ["♦", "♠", "♥", "♣"]
SUIT_CLASSES = {"♦": "red-suit", "♠": "black-suit", "♥": "red-suit", "♣": "black-suit"}

@dataclass(frozen=True)
class Card:
    rank: str
    suit: str

    @property
    def label(self) -> str:
        return f"{self.rank}{self.suit}"


def init_game():
    # Inicialização simplificada para teste de layout
    st.session_state.game = {
        "score": [0, 0],
        "hand_points": 1,
        "player_hand": [Card("K", "♥"), Card("6", "♠"), Card("Q", "♣")],
        "cpu_cards_count": 3,
        "table": [{"player": "CPU", "card": Card("6", "♣")}],
        "message": "Pode começar, e se prepare para amargar uma derrota vergonhosa!",
    }


if "game" not in st.session_state:
    init_game()

g = st.session_state.game

# --- TOPO: Cabeçalho com Placar (Estilo Mister Truco) ---
st.markdown("<h2 style='text-align: center; color: white; margin-bottom: 0;'>MISTER TRUCO</h2>", unsafe_allow_html=True)
cols_score = st.columns([2, 1, 1, 2])
with cols_score[1]:
    st.markdown(f"<p class='status-text'>CPU: {g['score'][1]}</p>", unsafe_allow_html=True)
with cols_score[2]:
    st.markdown(f"<p class='status-text'>Marcio: {g['score'][0]}</p>", unsafe_allow_html=True)

st.divider()

# --- CORPO PRINCIPAL: Divisão em Mesa (Esquerda) e Painel/Vira (Direita) ---
col_gameplay, col_sidebar = st.columns([3, 1])

with col_gameplay:
    # 1. Cartas do Adversário (CPU) - Sempre viradas para baixo no topo
    cols_cpu = st.columns([1, 1, 1, 1, 1])
    for i in range(g["cpu_cards_count"]):
        with cols_cpu[i + 1]:  # Centralizando levemente
            st.markdown("<div class='card-back'>R</div>", unsafe_allow_html=True)

    # Espaçador central da mesa
    st.markdown("<br/><br/>", unsafe_allow_html=True)
    
    # 2. Indicador de "VALENDO X" no meio da mesa
    c_valendo, _ = st.columns([1, 4])
    with c_valendo:
        st.markdown(
            f"""
            <div style='text-align: center; color: #7ca982; font-family: monospace;'>
                VALENDO<br/><span style='font-size: 42px; font-weight: bold;'>{g['hand_points']}</span>
            </div>
            """, 
            unsafe_allow_html=True
        )

    st.markdown("<br/>", unsafe_allow_html=True)

    # 3. Suas Cartas (Embaixo)
    cols_player = st.columns([1, 1, 1, 1, 1])
    for i, card in enumerate(g["player_hand"]):
        with cols_player[i + 1]:
            suit_class = SUIT_CLASSES[card.suit]
            # Botão estilizado com HTML dentro para simular a carta real do print
            card_html = f"""
            <div class='card-played {suit_class}'>
                <div>{card.rank}</div>
                <div style='font-size: 32px;'>{card.suit}</div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
            if st.button("Jogar", key=f"play_{i}", use_container_width=True):
                # Lógica de jogar a carta entraria aqui
                pass

    # 4. Botões de Ação Inferiores (Truco / Correr)
    st.markdown("<br/>", unsafe_allow_html=True)
    cols_actions = st.columns([2, 1, 1, 2])
    with cols_actions[1]:
        st.button("TRUCO", use_container_width=True)
    with cols_actions[2]:
        st.button("CORRER", use_container_width=True)

with col_sidebar:
    # Caixa de diálogo da IA (Balão de fala do print)
    st.markdown(
        f"""
        <div style="background-color: #ffffff; border-radius: 15px; padding: 12px; color: #000000; position: relative; margin-bottom: 20px; box-shadow: 2px 2px 5px rgba(0,0,0,0.2);">
            <div style="font-size: 13px; font-weight: bold; margin-bottom: 4px;">💻 CPU diz:</div>
            <div style="font-size: 14px; font-style: italic;">"{g['message']}"</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Cartas jogadas na mesa / Vira
    st.markdown("<p style='color: white; font-weight: bold; margin-bottom: 2px;'>MESA / VIRA</p>", unsafe_allow_html=True)
    for play in g["table"]:
        card = play["card"]
        suit_class = SUIT_CLASSES[card.suit]
        
        # Desenha a carta na barra lateral conforme o print
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; gap: 10px; background: rgba(0,0,0,0.2); padding: 10px; border-radius: 8px;">
                <div class='card-played {suit_class}' style='width: 70px; height: 95px; font-size: 20px; flex-shrink: 0;'>
                    <div>{card.rank}</div>
                    <div style='font-size: 24px;'>{card.suit}</div>
                </div>
                <div style='color: white;'>
                    <b>{play['player']}</b><br/><small>Jogou esta carta</small>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
