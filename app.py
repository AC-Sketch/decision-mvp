import random
import streamlit as st
from dataclasses import dataclass
from typing import List, Dict, Optional

# =========================================================
# MISTER MASTER TRIVIA - JOGO DE PERGUNTAS E RESPOSTAS
# Arquitetura estável por eventos e proteção de estados
# =========================================================

st.set_page_config(page_title="Mister Master Trivia", page_icon="🧠", layout="wide")

# --- ESTILIZAÇÃO VISUAL DE ALTO CONTRASTE ---
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
    
    .panel-question {
        background-color: #ffffff !important;
        border: 2px solid #000000;
        border-radius: 12px; 
        padding: 20px;
        color: #000000 !important;
        box-shadow: 3px 3px 8px rgba(0,0,0,0.4);
        font-size: 18px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 15px;
    }

    .stButton>button {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1.5px solid #000000 !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        padding: 10px !important;
        font-size: 15px !important;
    }
    .stButton>button:hover {
        background-color: #f3f4f6 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- BANCO DE DADOS DE PERGUNTAS (ESTILO MASTER CLÁSSICO) ---
QUESTIONS_DB = [
    {
        "categoria": "História",
        "pergunta": "Em que ano o homem pisou na Lua pela primeira vez?",
        "opcoes": ["1965", "1969", "1972", "1975"],
        "correta": "1969",
        "dica": "Aconteceu no mesmo ano do famoso festival de rock de Woodstock."
    },
    {
        "categoria": "Geografia",
        "pergunta": "Qual é o maior oceano do planeta Terra?",
        "opcoes": ["Oceano Atlântico", "Oceano Índico", "Oceano Pacífico", "Oceano Ártico"],
        "correta": "Oceano Pacífico",
        "dica": "Ele banha a costa oeste das Américas e o leste da Ásia."
    },
    {
        "categoria": "Ciência",
        "pergunta": "Qual elemento químico possui o símbolo 'O' na tabela periódica?",
        "opcoes": ["Ouro", "Oxigênio", "Ozônio", "Osmio"],
        "correta": "Oxigênio",
        "dica": "É o elemento essencial para a nossa respiração."
    },
    {
        "categoria": "Tecnologia",
        "pergunta": "O que significa a sigla 'WWW' no início dos endereços de internet?",
        "opcoes": ["Web Wide Window", "World Wide Web", "Western Wire Web", "World Wide Window"],
        "correta": "World Wide Web",
        "dica": "Traduzido livremente significa 'Rede de Alcance Mundial'."
    },
    {
        "categoria": "Entretenimento",
        "pergunta": "Qual é o nome do criador do icônico personagem Mario nos videogames?",
        "opcoes": ["Hideo Kojima", "Shigeru Miyamoto", "Akira Toriyama", "Masahiro Sakurai"],
        "correta": "Shigeru Miyamoto",
        "dica": "Ele também é o cérebro por trás da franquia The Legend of Zelda."
    }
]

# --- CORE ENGINE (INICIALIZAÇÃO DO ESTADO) ---
def init_master_game():
    # Sorteia a ordem das perguntas para o jogador
    pool = QUESTIONS_DB[:]
    random.shuffle(pool)
    
    st.session_state.master = {
        "questions": pool,
        "current_idx": 0,
        "score": 0,
        "vidas": 3,
        "status": "Jogando", # 'Jogando', 'Vitória', 'Derrota'
        "feedback": "Bem-vindo ao Master! Escolha uma alternativa abaixo.",
        "ajuda_5050": True,
        "ajuda_dica": True,
        "opcoes_visiveis": None, # Controla o corte do 50/50
        "mostrar_dica": False
    }

def process_answer(chosen: str):
    m = st.session_state.master
    q = m["questions"][m["current_idx"]]
    
    if chosen == q["correta"]:
        m["score"] += 10
        m["feedback"] = f"✅ CORRETO! Você ganhou 10 pontos. ('{q['correta']}' era a resposta certa)."
    else:
        m["vidas"] -= 1
        m["feedback"] = f"❌ INCORRETO! Você perdeu 1 vida. A resposta certa era '{q['correta']}'."
        
    if m["vidas"] <= 0:
        m["status"] = "Derrota"
        m["feedback"] = f"💀 FIM DE JOGO! Suas vidas acabaram. Pontuação final: {m['score']} pontos."
        return
        
    # Avança para a próxima pergunta se houver
    m["current_idx"] += 1
    m["opcoes_visiveis"] = None # Reseta ajuda para a próxima questão
    m["mostrar_dica"] = False
    
    if m["current_idx"] >= len(m["questions"]):
        m["status"] = "Vitória"
        m["feedback"] = f"🏆 PARABÉNS! Você respondeu todo o banco de dados! Pontuação máxima: {m['score']} pontos!"

# --- FLUXO DE EXECUÇÃO DA INTERFACE ---
st.markdown("<h2 style='color: white; font-family: monospace; text-align: center; letter-spacing: 2px;'>MISTER MASTER TRIVIA</h2>", unsafe_allow_html=True)
st.markdown("<hr/>", unsafe_allow_html=True)

if "master" not in st.session_state:
    init_master_game()

m = st.session_state.master

# Painel Superior de Status (Placar fixo)
c_sc = st.columns([1.5, 1.5, 1])
with c_sc[0]: st.markdown(f"<div class='status-text'>PONTUAÇÃO: {m['score']} PTS</div>", unsafe_allow_html=True)
with c_sc[1]: st.markdown(f"<div class='status-text'>VIDAS: {'❤️ ' * m['vidas']}</div>", unsafe_allow_html=True)
with c_sc[2]: st.markdown(f"<div class='status-text' style='background-color:#11331c;'>PROGRESSO: {min(m['current_idx'] + 1, len(m['questions']))}/{len(m['questions'])}</div>", unsafe_allow_html=True)

st.markdown("<br/>", unsafe_allow_html=True)

col_game, col_panel = st.columns([2.6, 1.4])

with col_game:
    if m["status"] == "Jogando":
        # Puxa os dados da pergunta atual
        q_atual = m["questions"][m["current_idx"]]
        
        # Define quais opções exibir (tratamento do botão 50/50)
        if m["opcoes_visiveis"] is None:
            m["opcoes_visiveis"] = q_atual["opcoes"][:]
            
        # Caixa da Pergunta Grande
        st.markdown(f"<div class='panel-question'><small style='color:gray;'>CATEGORIA: {q_atual['categoria'].upper()}</small><br/><br/>{q_atual['pergunta']}</div>", unsafe_allow_html=True)
        
        # Renderização das Alternativas em Grid de 2x2
        for r in range(2):
            cols_opt = st.columns(2)
            for c in range(2):
                opt_idx = r * 2 + c
                opt_text = q_atual["opcoes"][opt_idx]
                
                # Oculta se o jogador usou a ajuda 50/50
                is_visible = opt_text in m["opcoes_visiveis"]
                btn_label = opt_text if is_visible else "---"
                
                with cols_opt[c]:
                    if st.button(btn_label, key=f"opt_btn_{opt_idx}", disabled=not is_visible, use_container_width=True):
                        process_answer(opt_text)
                        st.rerun()
                        
    else:
        # Fim de jogo (Vitória ou Derrota)
        st.markdown(f"<div class='panel-question' style='background-color:#0f172a; color:white !important;'>PARTIDA CONCLUÍDA</div>", unsafe_allow_html=True)
        if st.button("Jogar Novamente / Reiniciar Banco", use_container_width=True):
            init_master_game()
            st.rerun()

with col_panel:
    # Balão de Feedback do Juiz
    st.markdown(f"<div class='balloon-retro'><b>💬 Histórico / Juiz:</b><br/><i>\"{m['feedback']}\"</i></div>", unsafe_allow_html=True)
    
    # Linha de Dica Ativa
    if m["status"] == "Jogando" and m["mostrar_dica"]:
        q_atual = m["questions"][m["current_idx"]]
        st.warning(f"💡 Dica: {q_atual['dica']}")
        
    # Painel Lateral de Recursos de Ajuda
    st.markdown("<p style='color: white; font-weight: bold; margin: 5px 0;'>Linhas de Ajuda Disponíveis:</p>", unsafe_allow_html=True)
    
    # Botão Ajuda 1: 50/50
    if st.button("🃏 Eliminar 2 Erradas (50/50)", disabled=not m["ajuda_5050"] or m["status"] != "Jogando", use_container_width=True):
        q_atual = m["questions"][m["current_idx"]]
        erradas = [o for o in q_atual["opcoes"] if o != q_atual["correta"]]
        removidas = random.sample(erradas, 2)
        m["opcoes_visiveis"] = [o for o in q_atual["opcoes"] if o not in removidas]
        m["ajuda_5050"] = False
        m["feedback"] = "Ajuda 50/50 utilizada! Duas alternativas incorretas foram desativadas."
        st.rerun()
        
    # Botão Ajuda 2: Pedir Dica
    if st.button("💡 Revelar uma Dica", disabled=not m["ajuda_dica"] or m["status"] != "Jogando", use_container_width=True):
        m["mostrar_dica"] = True
        m["ajuda_dica"] = False
        m["feedback"] = "Dica revelada! Olhe o painel logo abaixo."
        st.rerun()

if m["status"] == "Vitória":
    st.balloons()
