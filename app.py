import random
import streamlit as st
from dataclasses import dataclass
from typing import List, Dict, Optional

# =========================================================
# SAFETOPOLY: O JOGO DA NR-1 (GERENCIAMENTO DE RISCOS)
# Versão Corporativa Homologada - Layout Nativo Anti-Quebra
# =========================================================

st.set_page_config(page_title="SafeTopoly NR-1", page_icon="🦺", layout="wide")

# --- IDENTIDADE VISUAL CORPORATIVA (CUSTOMIZAÇÃO COMPACTA) ---
st.markdown("""
    <style>
    .stApp { background-color: #0f172a !important; } /* Fundo azul escuro */
    .block-container { padding: 0.5rem 2rem 0rem 2rem !important; }
    header, footer { visibility: hidden; }
    hr { margin: 0.4rem 0 !important; border-color: rgba(255,255,255,0.2) !important; }

    .status-text {
        color: #ffffff !important;
        font-family: 'Courier New', Courier, monospace;
        font-weight: bold;
        font-size: 15px;
        text-align: center;
        background-color: rgba(30, 41, 59, 0.9);
        padding: 6px 12px;
        border-radius: 6px;
        margin: 0px;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .balloon-retro {
        background-color: #ffffff !important; border: 2px solid #000000; border-radius: 12px; 
        padding: 12px; color: #000000 !important; box-shadow: 3px 3px 6px rgba(0,0,0,0.3);
        font-size: 14px; margin-bottom: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# Banco de dados temático contendo 24 etapas estritas da NR-1
TILES_NR1 = [
    {"name": "0. INTEGRAÇÃO 🚀", "type": "GO"},
    {"name": "1. Inventário Riscos 📝", "cost": 100, "fine": 10},
    {"name": "2. Critérios Risco 📊", "cost": 120, "fine": 15},
    {"name": "3. FISCALIZAÇÃO 🔎", "type": "Auditoria"},
    {"name": "4. Matriz Severidade 🧮", "cost": 140, "fine": 15},
    {"name": "5. Avaliação Ergonômica 🪑", "cost": 160, "fine": 20},
    
    {"name": "11. Plano de Ação 📉", "cost": 260, "fine": 30},
    {"name": "10. Análise Acidentes 🚑", "cost": 240, "fine": 25},
    {"name": "9. MULTA MTE ⚠️", "type": "Multa"},
    {"name": "8. Plano Emergência 🚨", "cost": 220, "fine": 25},
    {"name": "7. Simulado Incêndio 🔥", "cost": 200, "fine": 20},
    {"name": "6. CIPA / NEUTRO 🏢", "type": "Neutro"},
    
    {"name": "12. INTERDIÇÃO ⛔", "type": "Embargo"},
    {"name": "13. Treinam. Básico 📘", "cost": 280, "fine": 35},
    {"name": "14. FISCALIZAÇÃO 🔎", "type": "Auditoria"},
    {"name": "15. Treinam. Periódico 🗓️", "cost": 300, "fine": 40},
    {"name": "16. Material Didático 📁", "cost": 150, "fine": 15},
    {"name": "17. Avaliação Prática 🛠️", "cost": 180, "fine": 20},
    
    {"name": "23. Uso de EPIs 🥽", "cost": 240, "fine": 30},
    {"name": "22. Comunicação Risco 📢", "cost": 220, "fine": 25},
    {"name": "21. FISCALIZAÇÃO 🔎", "type": "Auditoria"},
    {"name": "20. Ordens de Serviço 📋", "cost": 200, "fine": 25},
    {"name": "19. Direito de Recusa ✋", "cost": 180, "fine": 20},
    {"name": "18. SESMT / NEUTRO 🛡️", "type": "Neutro"}
]

def init_game():
    st.session_state.safe = {
        "pos": [0, 0], # [Você, CPU]
        "orcamento": [1500, 1500],
        "implementations": {}, # tile_idx -> player_idx
        "log": " SafeTopoly NR-1 Iniciado! Percorra o tabuleiro de 24 setores implementando o PGR e os planos de capacitação corporativos.",
        "turn": 0,
        "game_over": False
    }

def play_turn(player_idx: int):
    s = st.session_state.safe
    dado = random.randint(1, 6)
    
    old_pos = s["pos"][player_idx]
    s["pos"][player_idx] = (s["pos"][player_idx] + dado) % len(TILES_NR1)
    curr_pos = s["pos"][player_idx]
    
    if curr_pos < old_pos:
        s["orcamento"][player_idx] += 250
        s["log"] = "🔄 Ciclo anual do PGR concluído e revisado! Sua empresa recebeu um aporte orçamentário de $250."

    tile = TILES_NR1[curr_pos]
    p_name = "Você" if player_idx == 0 else "O Bot Auditor"
    msg = f"🎲 {p_name} lançou os dados, andou {dado} casas e inspecionou o setor **{tile['name']}**."

    if "cost" in tile:
        manager = s["implementations"].get(curr_pos)
        if manager is None:
            if s["orcamento"][player_idx] >= tile["cost"]:
                if player_idx == 0:
                    s["log"] = f"{msg}\n\nEste item regulatório está sem conformidade. Deseja investir **${tile['cost']}** para adequar o setor?"
                    return # Trava execução para o clique humano
                else:
                    s["implementations"][curr_pos] = 1
                    s["orcamento"][1] -= tile["cost"]
                    msg += f"\n\n💻 O Bot regularizou o setor **{tile['name']}** investindo ${tile['cost']}."
            else:
                msg += "\n\nSua empresa não possui verba em caixa para esta adequação."
        elif manager == player_idx:
            msg += "\n\nEste setor já se encontra com conformidade e auditoria em dia."
        else:
            s["orcamento"][player_idx] -= tile["fine"]
            s["orcamento"][manager] += tile["fine"]
            msg += f"\n\n🚨 Falha na Gestão! O concorrente adequou este processo antes. Sua empresa arcou com **${tile['fine']}** em passivos trabalhistas."
            
    elif tile["type"] == "Auditoria":
        evento = random.choice([
            ("Seus colaboradores identificaram risco iminente e usaram o Direito de Recusa perfeitamente! Eficiência corporativa: +$100.", 100),
            ("Gargalo detectado no mapeamento de perigos físicos das Ordens de Serviço! Gastos extras: -$100.", -100),
            ("Sua estrutura de PGR foi considerada referência regional pelo MTE! Aporte de bônus: +$150.", 150)
        ])
        s["orcamento"][player_idx] += evento[1]
        msg += f"\n\n🔎 **Relatório de Auditoria:** {evento[0]}"
        
    elif tile["type"] == "Multa":
        s["orcamento"][player_idx] -= 150
        msg += "\n\n⚠️ **Autuação Regulatória:** Descumprimento severo na integração inicial de novos operários. Sanção de -$150."
        
    elif tile["type"] == "Embargo":
        s["pos"][player_idx] = 12 # Envia direto para a casa de Interdição
        msg += "\n\n⛔ **EMBARGO FISCAL!** O setor de engenharia paralisou suas operações devido a riscos não mitigados. Desloque-se para a regularização."

    if s["orcamento"][player_idx] <= 0:
        s["game_over"] = True
        s["log"] = f"{msg}\n\n💀 **FALÊNCIA OPERACIONAL!** A empresa liderada por {p_name} quebrou devido ao acúmulo de multas, passivos judiciais e interdições."
        return

    s["log"] = msg
    s["turn"] = 1 - player_idx

# --- MONITORAMENTO DE ESTADO ---
if "safe" not in st.session_state:
    init_game()
sg = st.session_state.safe

if sg["turn"] == 1 and not sg["game_over"]:
    play_turn(1)
    st.rerun()

# Painel Fixo de Métricas
c_hdr = st.columns([1.5, 1.5, 1])
with c_hdr[0]: st.markdown(f"<div class='status-text'>SEU CAIXA DE SEGURANÇA: ${sg['orcamento'][0]}</div>", unsafe_allow_html=True)
with c_hdr[1]: st.markdown(f"<div class='status-text'>CAIXA DE SEGURANÇA RIVAL: ${sg['orcamento'][1]}</div>", unsafe_allow_html=True)
with c_hdr[2]: st.markdown(f"<div class='status-text' style='background-color:#1e3a8a;'>TURNO: {'Sua Vez' if sg['turn'] == 0 else 'Análise do Bot...'}</div>", unsafe_allow_html=True)

st.markdown("<br/>", unsafe_allow_html=True)

col_board, col_panel = st.columns([2.5, 1.5])

with col_board:
    st.markdown("<p style='color:white; font-weight:bold; margin-bottom:5px;'>⚙️ Painel Operacional da Trilha (24 Setores da NR-1):</p>", unsafe_allow_html=True)
    
    # RENDERIZAÇÃO EM ZIGUE-ZAGUE (NATIVA DO STREAMLIT - ANTI-QUEBRA)
    
    # Linha 1 (Casas 0 a 5)
    c_l1 = st.columns(6)
    for i in range(6):
        with c_l1[i]:
            t = TILES_NR1[i]
            p = ""
            if sg["pos"][0] == i: p += "🦺"
            if sg["pos"][1] == i: p += "🤖"
            dono = " [V]" if sg["implementations"].get(i) == 0 else " [R]" if sg["implementations"].get(i) == 1 else ""
            st.info(f"**{t['name']}{dono}**\n\n{p if p else '🔳'}")

    # Linha 2 (Casas 11 a 6 de forma reversa)
    c_l2 = st.columns(6)
    indices_l2 = [11, 10, 9, 8, 7, 6]
    for idx, i in enumerate(indices_l2):
        with c_l2[idx]:
            t = TILES_NR1[i]
            p = ""
            if sg["pos"][0] == i: p += "🦺"
            if sg["pos"][1] == i: p += "🤖"
            dono = " [V]" if sg["implementations"].get(i) == 0 else " [R]" if sg["implementations"].get(i) == 1 else ""
            st.info(f"**{t['name']}{dono}**\n\n{p if p else '🔳'}")

    # Linha 3 (Casas 12 a 17)
    c_l3 = st.columns(6)
    for i in range(12, 18):
        with c_l3[i - 12]:
            t = TILES_NR1[i]
            p = ""
            if sg["pos"][0] == i: p += "🦺"
            if sg["pos"][1] == i: p += "🤖"
            dono = " [V]" if sg["implementations"].get(i) == 0 else " [R]" if sg["implementations"].get(i) == 1 else ""
            st.info(f"**{t['name']}{dono}**\n\n{p if p else '🔳'}")

    # Linha 4 (Casas 23 a 18 de forma reversa)
    c_l4 = st.columns(6)
    indices_l4 = [23, 22, 21, 20, 19, 18]
    for idx, i in enumerate(indices_l4):
        with c_l4[idx]:
            t = TILES_NR1[i]
            p = ""
            if sg["pos"][0] == i: p += "🦺"
            if sg["pos"][1] == i: p += "🤖"
            dono = " [V]" if sg["implementations"].get(i) == 0 else " [R]" if sg["implementations"].get(i) == 1 else ""
            st.info(f"**{t['name']}{dono}**\n\n{p if p else '🔳'}")

with col_panel:
    st.markdown(f"<div class='balloon-retro' style='min-height:160px;'><b>📋 Diário de Bordo Regulatória:</b><br/><br/>{sg['log']}</div>", unsafe_allow_html=True)
    
    active_human = (sg["turn"] == 0 and not sg["game_over"])
    pending_decision = "Deseja investir" in sg["log"] or "Deseja adequar" in sg["log"]
    
    c_btns = st.columns(2)
    with c_btns[0]:
        if st.button("🎲 INSPEÇÃO DE ROTINA (DADO)", disabled=not active_human or pending_decision, use_container_width=True):
            play_turn(0)
            st.rerun()
            
    if pending_decision and active_human:
        with c_btns[0]:
            if st.button("👍 Sim, Alocar Verba", use_container_width=True):
                curr_p = sg["pos"][0]
                sg["implementations"][curr_p] = 0
                sg["orcamento"][0] -= TILES_NR1[curr_p]["cost"]
                sg["log"] = f"Ação Concluída! Setor **{TILES_NR1[curr_p]['name']}** mapeado e com gerenciamento ativo."
                sg["turn"] = 1
                st.rerun()
        with c_btns[1]:
            if st.button("👎 Não, Adiar Mitigação", use_container_width=True):
                sg["log"] = "Risco assumido pela diretoria. Cuidado com auditorias retroativas!"
                sg["turn"] = 1
                st.rerun()
                
    st.markdown("<br/><br/>", unsafe_allow_html=True)
    if st.button("Reiniciar Workshop Prático", use_container_width=True):
        init_game()
        st.rerun()

if sg["game_over"] and sg["orcamento"][0] > 0:
    st.balloons()
