import random
import streamlit as st
from dataclasses import dataclass
from typing import List, Dict, Optional

# =========================================================
# COLETÂNEA RETRÔ: JOGO DE TABULEIRO & RPG DE DADOS
# Arquitetura de Funções Puras e Estados Blindados
# =========================================================

st.set_page_config(page_title="Mister Boardgames", page_icon="🎲", layout="wide")

# --- ESTILIZAÇÃO VISUAL DE ALTO CONTRASTE (ESTILO RETRÔ) ---
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
    
    /* Casas do Tabuleiro */
    .board-cell {
        background-color: #ffffff !important;
        color: #000000 !important;
        font-size: 36px !important;
        font-weight: bold !important;
        height: 90px !important;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 2px solid #000000 !important;
        border-radius: 8px !important;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
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
# LÓGICA CORE: TABULEIRO JOGO DA VELHA (BOT INTELIGENTE)
# =========================================================
def init_tic_tac_toe():
    st.session_state.ttt = {
        "board": [" "] * 9,
        "status": "Sua Vez",
        "winner": None,
        "score": st.session_state.get("ttt", {}).get("score", [0, 0]) # [Jogador, CPU]
    }

def check_ttt_winner(board: List[str]) -> Optional[str]:
    lines = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
    for a, b, c in lines:
        if board[a] == board[b] == board[c] and board[a] != " ":
            return board[a]
    if " " not in board:
        return "Empate"
    return None

def bot_ttt_move(board: List[str]) -> int:
    # 1. Se puder ganhar nesta jogada, ganha
    for i in range(9):
        if board[i] == " ":
            test = board[:]
            test[i] = "O"
            if check_ttt_winner(test) == "O": return i
    # 2. Se o jogador for ganhar, bloqueia
    for i in range(9):
        if board[i] == " ":
            test = board[:]
            test[i] = "X"
            if check_ttt_winner(test) == "X": return i
    # 3. Joga em posição randômica livre
    empty = [i for i, v in enumerate(board) if v == " "]
    return random.choice(empty) if empty else 0


# =========================================================
# LÓGICA CORE: RPG DE TABULEIRO E DADOS (MASMORRA)
# =========================================================
def init_rpg_board():
    st.session_state.rpg = {
        "posicao": 0, # Casa atual no tabuleiro de 0 a 10
        "vida": 15,
        "ouro": 5,
        "log": "Você colocou seu peão na linha de partida do Tabuleiro da Masmorra. Role o dado!",
        "status": "Jogando"
    }

def play_rpg_turn():
    r = st.session_state.rpg
    dado = random.randint(1, 6)
    r["posicao"] += dado
    
    if r["posicao"] >= 10:
        r["posicao"] = 10
        r["status"] = "Vitória"
        r["log"] = f"🎲 Você rolou {dado} e avançou para a Casa 10! 🏆 PARABÉNS! Você cruzou o tabuleiro vivo e escapou da masmorra com {r['ouro']} moedas de ouro!"
        return

    # Eventos de casas do tabuleiro
    eventos = {
        1: ("Armadilha de Espinhos", -3, 0, "💥 Casa 1: Você pisou em um falso piso! Perdeu 3 de Vida."),
        2: ("Baú de Moedas", 0, 5, "💰 Casa 2: Um baú antigo trancado. Você achou 5 moedas de ouro!"),
        3: ("Encontro com Goblin", -2, 2, "⚔️ Casa 3: Um Goblin sorrateiro te atacou! Você o derrotou, perdeu 2 de vida mas pilhou 2 moedas."),
        4: ("Fonte Escura", 4, 0, "🧪 Casa 4: Você bebeu de uma fonte mística e recuperou 4 de Vida!"),
        5: ("Corredor Vazio", 0, 0, "🚶 Casa 5: Uma área silenciosa do tabuleiro. Nada aconteceu."),
        6: ("Ninho de Morcegos", -1, 0, "🦇 Casa 6: Morcegos famintos te morderam! Perdeu 1 de Vida."),
        7: ("Estátua de Ouro", 0, 8, "✨ Casa 7: Você arrancou pedras preciosas dos olhos de uma estátua! +8 de Ouro."),
        8: ("Névoa Venenosa", -4, 0, "☠️ Casa 8: Uma fumaça tóxica cobriu a sala! Você perdeu 4 de Vida."),
        9: ("Mercador Retrô", 2, -3, "🛒 Casa 9: Você encontrou um mercador, pagou 3 de ouro por uma poção e recuperou 2 de vida.")
    }
    
    nome, vida_alt, ouro_alt, msg = eventos.get(r["posicao"], ("Sala Vazia", 0, 0, "🚶 Você avançou sem problemas."))
    
    r["vida"] += vida_alt
    r["ouro"] += ouro_alt
    if r["ouro"] < 0: r["ouro"] = 0
    
    r["log"] = f"🎲 Você rolou o dado e tirou {dado}. Avançou para a **Casa {r['posicao']}**.\n\n{msg}"
    
    if r["vida"] <= 0:
        r["status"] = "Derrota"
        r["log"] = f"🎲 Você avançou para a Casa {r['posicao']} após rolar {dado}, mas seus pontos de Vida chegaram a 0... Seu peão foi removido do tabuleiro. Fim de jogo."


# --- MENU DE SELEÇÃO GLOBAL DO TOPO ---
game_mode = st.selectbox("🎮 SELECIONE O JOGO DE TABULEIRO:", ["⭕ Jogo da Velha (Tabuleiro)", "🎲 RPG de Dados e Tabuleiro"])
st.markdown("<hr/>", unsafe_allow_html=True)


# ----------------- COLO: JOGO DA VELHA -----------------
if game_mode == "⭕ Jogo da Velha (Tabuleiro)":
    if "ttt" not in st.session_state:
        init_tic_tac_toe()
        
    t = st.session_state.ttt
    
    # Placar Superior Fixo
    c_sc = st.columns([2, 1])
    with c_sc[0]: st.markdown(f"<div class='status-text'>PLACARES   ▏   VOCÊ: {t['score'][0]}   |   CPU: {t['score'][1]}</div>", unsafe_allow_html=True)
    with c_sc[1]: st.markdown(f"<div class='status-text' style='background-color:#11331c;'>STATUS: {t['status'].upper()}</div>", unsafe_allow_html=True)
    st.markdown("<br/>", unsafe_allow_html=True)
    
    col_board, col_panel = st.columns([2.5, 1.5])
    
    with col_board:
        # Renderização da grade 3x3 perfeita usando botões Streamlit nativos
        for row in range(3):
            cols_grid = st.columns([1, 1, 1, 3])
            for col in range(3):
                idx = row * 3 + col
                cell_value = t["board"][idx]
                
                with cols_grid[col]:
                    # Botão estilizado atua como a casa do tabuleiro
                    if st.button(f"{cell_value} ", key=f"ttt_cell_{idx}", disabled=cell_value != " " or t["winner"] is not None):
                        t["board"][idx] = "X"
                        winner = check_ttt_winner(t["board"])
                        
                        if winner:
                            t["winner"] = winner
                        else:
                            # Vez do Bot jogar de forma imediata na mesma rodada
                            cpu_move = bot_ttt_move(t["board"])
                            t["board"][cpu_move] = "O"
                            winner = check_ttt_winner(t["board"])
                            if winner: t["winner"] = winner
                            
                        # Processa fim de jogo e pontuação
                        if t["winner"]:
                            if t["winner"] == "X":
                                t["score"][0] += 1
                                t["status"] = "Você Ganhou!"
                            elif t["winner"] == "O":
                                t["score"][1] += 1
                                t["status"] = "CPU Ganhou!"
                            else:
                                t["status"] = "Empatou!"
                        st.rerun()
                        
    with col_panel:
        st.markdown(f"<div class='balloon-retro'><b>💬 Painel do Juiz:</b><br/>{t['status'] if not t['winner'] else 'Partida encerrada.'}</div>", unsafe_allow_html=True)
        if st.button("Reiniciar Tabuleiro", use_container_width=True):
            init_tic_tac_toe()
            st.rerun()


# ----------------- COLO: RPG DE TABULEIRO -----------------
elif game_mode == "🎲 RPG de Dados e Tabuleiro":
    if "rpg" not in st.session_state:
        init_rpg_board()
        
    r = st.session_state.rpg
    
    # Placar Superior Fixo dos Status do Herói
    c_r_sc = st.columns([1.5, 1.5, 1])
    with c_r_sc[0]: st.markdown(f"<div class='status-text'>HERÓI: {r['vida']} HP (Vida)</div>", unsafe_allow_html=True)
    with c_r_sc[1]: st.markdown(f"<div class='status-text'>BOLSA: {r['ouro']} 💰 (Ouro)</div>", unsafe_allow_html=True)
    with c_r_sc[2]: st.markdown(f"<div class='status-text' style='background-color:#11331c;'>CASA ATUAL: {r['posicao']}/10</div>", unsafe_allow_html=True)
    st.markdown("<br/>", unsafe_allow_html=True)
    
    col_r_board, col_r_panel = st.columns([2.5, 1.5])
    
    with col_r_board:
        # Desenho linear do trilho do tabuleiro (0 a 10)
        st.markdown("<p style='color:white; font-weight:bold; margin:0;'>Trilho do Tabuleiro:</p>", unsafe_allow_html=True)
        cols_track = st.columns(11)
        for step in range(11):
            with cols_track[step]:
                if r["posicao"] == step:
                    # Indica onde está o peão do jogador
                    st.markdown(f"<div style='background-color:#fde047; color:black; font-weight:bold; text-align:center; padding:10px; border-radius:5px; border:2px solid black;'>🤠 <br/>C{step}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div style='background-color:white; color:black; text-align:center; padding:10px; border-radius:5px; border:1px solid #ccc;'>🔳<br/>C{step}</div>", unsafe_allow_html=True)
                    
        st.markdown("<br/><br/>", unsafe_allow_html=True)
        # Botão de ação para rolar dados
        if st.button("🎲 ROLAR DADO (AVANÇAR)", disabled=r["status"] != "Jogando", use_container_width=True):
            play_rpg_turn()
            st.rerun()
            
    with col_r_panel:
        st.markdown(f"<div class='balloon-retro' style='min-height:120px;'><b>📜 Crônicas da Masmorra:</b><br/>{r['log']}</div>", unsafe_allow_html=True)
        if st.button("Nova Jornada RPG", use_container_width=True):
            init_rpg_board()
            st.rerun()
