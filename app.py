import streamlit as st
import random
import html
from statistics import mean

# ==============================================================================
# 1. CONFIGURAÇÃO DA INTERFACE E DESIGN SYSTEM PREMIUM
# ==============================================================================
st.set_page_config(
    page_title="NR-1 GRO/PGR Ultimate Boardgame & Compliance Simulator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Injeção de CSS de alta fidelidade visual (Design Corporativo Moderno)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Inter', sans-serif;
    background-color: #F8FAFC;
    color: #1E293B;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 1.5rem;
    max-width: 1550px;
}

/* Títulos Executivos */
.main-title {
    font-size: 2.3rem;
    font-weight: 800;
    color: #0F172A;
    letter-spacing: -0.04em;
    margin-bottom: 0.2rem;
}

.subtitle {
    font-size: 1.05rem;
    color: #64748B;
    margin-bottom: 1.5rem;
    font-weight: 400;
}

/* Estilização do Tabuleiro Visual */
.board-container {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    margin-bottom: 24px;
}

.board-grid {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 12px;
    margin-top: 15px;
}

.board-tile {
    background: #F1F5F9;
    border: 2px solid #E2E8F0;
    border-radius: 12px;
    padding: 14px;
    min-height: 110px;
    position: relative;
    transition: all 0.2s ease;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.board-tile-special {
    background: #FDF2F8;
    border-color: #F472B6;
}

.tile-number {
    font-size: 11px;
    font-weight: 700;
    color: #94A3B8;
    position: absolute;
    top: 6px;
    left: 8px;
}

.tile-label {
    font-size: 11.5px;
    font-weight: 700;
    color: #1E293B;
    margin-top: 14px;
    line-height: 1.3;
}

.player-token {
    display: inline-block;
    padding: 2px 6px;
    border-radius: 20px;
    font-size: 10px;
    font-weight: 700;
    color: white;
    margin-right: 4px;
    margin-top: 4px;
    box-shadow: 0 1px 2px rgba(0,0,0,0.1);
}

/* Leaderboard Sidebar Cards */
.player-sidebar-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 12px;
    margin-bottom: 10px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.02);
}

/* Modificações nos Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: #E2E8F0;
    padding: 6px;
    border-radius: 12px;
}

.stTabs [data-baseweb="tab"] {
    background-color: transparent;
    border-radius: 8px;
    padding: 8px 16px;
    font-weight: 600;
    color: #475569;
    border: none !important;
}

.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background-color: #FFFFFF;
    color: #0F172A !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

/* Custom Console Logs */
.console-box {
    background: #0F172A;
    color: #94A3B8;
    font-family: 'Courier New', monospace;
    padding: 16px;
    border-radius: 12px;
    max-height: 180px;
    overflow-y: auto;
    font-size: 12px;
    border-left: 4px solid #10B981;
}

.console-line {
    border-bottom: 1px solid #1E293B;
    padding-bottom: 4px;
    margin-bottom: 4px;
}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. MAPEAMENTO DAS CASAS DO TABULEIRO (CONCEITOS E DILEMAS DA NR-1)
# ==============================================================================
CASAS_TABULEIRO = {
    0: {"titulo": "Início da Auditoria", "tipo": "normal", "desc": "Ponto de partida do planejamento do GRO."},
    1: {"titulo": "Identificação de Perigos", "tipo": "normal", "desc": "Mapeamento inicial de fontes geradoras de risco."},
    2: {"titulo": "Análise Causal", "tipo": "normal", "desc": "Investigação de desvios operacionais antigos."},
    3: {"titulo": "Fiscalização Surpresa!", "tipo": "especial", "desc": "Auditor fiscal exige o Inventário de Riscos atualizado."},
    4: {"titulo": "Matriz de Severidade", "tipo": "normal", "desc": "Definição do cruzamento entre lesões e probabilidade."},
    5: {"titulo": "Hierarquia de Controles", "tipo": "normal", "desc": "Aplicação técnica do item 1.5.5.1.2 prioritário."},
    6: {"titulo": "Plano de Ação - CAPEX", "tipo": "normal", "desc": "Aprovação orçamentária das medidas coletivas estruturais."},
    7: {"titulo": "Direito de Recusa", "tipo": "especial", "desc": "Trabalhador identifica risco grave e iminente na caldeira."},
    8: {"titulo": "Integração PCMSO", "tipo": "normal", "desc": "Conexão dos dados médicos com o PGR (Subitem 1.5.5.4.1)."},
    9: {"titulo": "Treinamento de Integração", "tipo": "normal", "desc": "Verificação de aproveitamento de horas de capacitação interna."},
    10: {"titulo": "Gestão de Terceirizados", "tipo": "normal", "desc": "Envio e recepção de riscos de prestadores de serviço."},
    11: {"titulo": "Notificação de Acidente", "tipo": "especial", "desc": "Abertura de Comunicação de Acidente de Trabalho (CAT)."},
    12: {"titulo": "Auditoria de Certificação", "tipo": "normal", "desc": "Preparação dos documentos para extensão do prazo da ISO 45001."},
    13: {"titulo": "Simulado de Emergência", "tipo": "normal", "desc": "Treinamento prático da brigada de incêndio técnica."},
    14: {"titulo": "Análise de Ergonomia", "tipo": "normal", "desc": "Integração do laudo da NR-17 ao plano central do PGR."},
    15: {"titulo": "Ata da CIPA", "tipo": "normal", "desc": "Alinhamento das percepções da comissão interna com o GRO."},
    16: {"titulo": "Nexo Epidemiológico", "tipo": "especial", "desc": "Defesa jurídica contra flutuações sazonais do indicador FAP."},
    17: {"titulo": "Garantia de Compliance", "tipo": "normal", "desc": "Revisão e assinatura digital do Engenheiro e Médico."},
}

PERSONAGENS_POOL = [
    {"nome": "Eng. Roberto", "cargo": "Coordenador de SESMT", "emoji": "👷‍♂️", "cor": "#3B82F6", "skill": "Engenharia de Controle Avançada"},
    {"nome": "Dra. Clarissa", "cargo": "Médica do Trabalho", "emoji": "👩‍⚕️", "cor": "#10B981", "skill": "Integração PGR-PCMSO Master"},
    {"nome": "Alana", "cargo": "Técnica de Segurança", "emoji": "👩‍🔧", "cor": "#F59E0B", "skill": "Inspeção e Agilidade de Campo"},
    {"nome": "Marcos", "cargo": "Diretor FinOps (CFO)", "emoji": "👨‍💼", "cor": "#64748B", "skill": "Análise de ROI em Prevenção"},
    {"nome": "Sofia", "cargo": "Presidente da CIPA", "emoji": "👩‍💼", "cor": "#8B5CF6", "skill": "Engajamento e Cultura de Riscos"},
    {"nome": "Bruno", "cargo": "Analista de Facilities", "emoji": "👨‍🏭", "cor": "#EF4444", "skill": "Controle de Terceiros e Logística"},
    {"nome": "Dra. Letícia", "cargo": "Compliance Jurídico", "emoji": "👩‍⚖️", "cor": "#EC4899", "skill": "Mitigação de Passivo Trabalhista"}
]

BANCO_QUESTOES_NR1 = [
    {
        "id": 1,
        "tema": "GRO - Integração de Processos",
        "pergunta": "De acordo com o item 1.5.3.1.1 da NR-1, o Gerenciamento de Riscos Ocupacionais (GRO) deve ser estruturado de qual forma?",
        "opcoes": [
            "A) Deve ser uma estrutura paralela e independente para não interferir nas metas comerciais.",
            "B) Deve ser integrado às atividades de gestão e aos demais processos da organização.",
            "C) É restrito ao arquivamento eletrônico sem comunicação com as gerências de operação.",
            "D) Aplica-se exclusivamente a trabalhadores temporários do setor logístico primário."
        ],
        "correta": 1,
        "justificativa": "O item 1.5.3.1.1 determina explicitamente a integração nativa aos processos de negócio da corporação.",
    },
    {
        "id": 2,
        "tema": "Direito de Recusa Legitimado",
        "pergunta": "Conforme o subitem 1.4.3 da NR-1, quando o trabalhador exercer o Direito de Recusa por risco grave e iminente, qual a ação compulsória imediata?",
        "opcoes": [
            "A) Sofrer advertência administrativa por interrupção de produtividade.",
            "B) Comunicar imediatamente o fato ao seu superior hierárquico direto.",
            "C) Abandonar o estabelecimento sem prestar esclarecimentos à engenharia.",
            "D) Aguardar nova convocação anual via correio eletrônico ou memorando."
        ],
        "correta": 1,
        "justificativa": "O fluxo regulamentar exige comunicação imediata da situação para avaliação das lideranças técnicas.",
    },
    {
        "id": 3,
        "tema": "Inventário de Riscos",
        "pergunta": "Segundo o item 1.5.7.3.2, o Inventário de Riscos do PGR precisa contemplar obrigatoriamente:",
        "opcoes": [
            "A) Apenas a lista de presença nos treinamentos institucionais de integração.",
            "B) Caracterização das fontes, descrição de possíveis danos, avaliação de severidade e probabilidade.",
            "C) O balanço financeiro trimestral e a depreciação de ativos de proteção coletiva.",
            "D) O registro de marcas e patentes de equipamentos importados."
        ],
        "correta": 1,
        "justificativa": "A composição técnica estrutural do inventário exige a matriz de perigos detalhada combinada com severidade e probabilidade.",
    }
]

# ==============================================================================
# 3. CONTROLADOR ESTÁVEL DE ESTADO (SESSION STATE INFRASTRUCTURE)
# ==============================================================================
if "jogo_iniciado" not in st.session_state:
    st.session_state.jogo_iniciado = False
if "jogadores" not in st.session_state:
    st.session_state.jogadores = []
if "num_jogadores" not in st.session_state:
    st.session_state.num_jogadores = 3
if "rodada_atual" not in st.session_state:
    st.session_state.rodada_atual = 1
if "pergunta_atual_index" not in st.session_state:
    st.session_state.pergunta_atual_index = 0
if "dado_resultado" not in st.session_state:
    st.session_state.dado_resultado = "-"
if "historico_eventos" not in st.session_state:
    st.session_state.historico_eventos = []
if "resposta_enviada" not in st.session_state:
    st.session_state.resposta_enviada = False

# CORREÇÃO INTEGRAL DOS DIALETOS E CHAVES DO DICIONÁRIO PARA EVITAR ERROS DE DIGITAÇÃO:
if "matriz_dinamica" not in st.session_state:
    st.session_state.matriz_dinamica = {
        "Cenario_1": [4, 1, 1, 5, 2],
        "Cenario_2": [3, 3, 2, 4, 3],
        "Cenario_3": [3, 4, 4, 2, 4],
        "Cenario_4": [2, 5, 5, 1, 5],
    }

ROTULOS_CENARIOS = {
    "Cenario_1": "Cenário 1: Reativo",
    "Cenario_2": "Cenário 2: Burocrático",
    "Cenario_3": "Cenário 3: Técnico",
    "Cenario_4": "Cenário 4: Integrado",
}

def registrar_evento(texto):
    st.session_state.historico_eventos.insert(0, f"⚡ R{st.session_state.rodada_atual} | {texto}")

# ==============================================================================
# 4. GERADOR DE COMPLIANCE REPORT EM HTML (PADRÃO A4 PAISAGEM)
# ==============================================================================
def gerar_html_boardgame(titulo, objetivo, contexto, matriz_dados, logs_jogo):
    medias = {k: round(mean(v), 2) for k, v in matriz_dados.items()}
    ranking = sorted(medias.items(), key=lambda x: x[1], reverse=True)
    
    header_alternativas = "".join(f"<th>{html.escape(ROTULOS_CENARIOS[k])}</th>" for k in matriz_dados)
    
    linhas_criterios = ""
    criterios_labels = [
        "Retorno sobre Investimento (FinOps)",
        "Segurança Jurídica perante MTE/MPT",
        "Preservação da Saúde e Integridade",
        "Facilidade Prática de Implantação",
        "Hierarquia de Controles"
    ]
    for i, criterio in enumerate(criterios_labels):
        celulas = ""
        for k, notas in matriz_dados.items():
            nota = notas[i]
            cor_fundo = "#EF4444" if nota == 1 else "#FCA5A5" if nota == 2 else "#FEF08A" if nota == 3 else "#86EFAC" if nota == 4 else "#22C55E"
            cor_texto = "white" if nota in [1, 5] else "#1E293B"
            celulas += f'<td style="background-color: {cor_fundo}; color: {cor_texto}; font-weight: bold; text-align: center;">{nota}</td>'
        linhas_criterios += f"<tr><td style='text-align: left; font-weight: 600; background: #F1F5F9;'>{html.escape(criterio)}</td>{celulas}</tr>"

    linha_medias = "".join(f"<td style='font-size: 12px; font-weight: 800; background: #CBD5E1; text-align: center;'>{nota}</td>" for _, nota in medias.items())
    ranking_html = "".join(f"<li><strong>{idx}º Lugar:</strong> {html.escape(ROTULOS_CENARIOS[k])} — <span style='color: #2563EB; font-weight: bold;'>Média: {nota}</span></li>" for idx, (k, nota) in enumerate(ranking, 1))
    
    logs_renderizados = "".join(f"<li style='margin-bottom: 2px; border-bottom: 1px dashed #E2E8F0;'>{html.escape(log)}</li>" for log in logs_jogo[:4])
        
    return f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
@page {{ size: A4 landscape; margin: 10mm; }}
body {{ font-family: 'Segoe UI', Arial, sans-serif; color: #1E293B; background: #FFF; margin: 0; padding: 0; font-size: 12px; }}
.wrapper {{ width: 100%; max-width: 1100px; margin: 0 auto; border: 2px solid #0F172A; padding: 20px; border-radius: 8px; }}
header {{ border-bottom: 3px solid #0F172A; padding-bottom: 10px; margin-bottom: 15px; }}
.title {{ font-size: 22px; font-weight: 800; color: #0F172A; text-transform: uppercase; }}
.grid {{ display: grid; grid-template-columns: 1.3fr 1fr; gap: 20px; }}
.box {{ border: 1px solid #E2E8F0; border-radius: 6px; padding: 12px; margin-bottom: 12px; }}
.box-title {{ font-size: 13px; font-weight: 700; color: #1E3A8A; margin-top: 0; margin-bottom: 8px; border-left: 4px solid #2563EB; padding-left: 6px; }}
table {{ width: 100%; border-collapse: collapse; font-size: 11px; }}
th {{ background: #0F172A; color: white; padding: 8px; text-transform: uppercase; font-size: 9px; border: 1px solid #0F172A; }}
td {{ padding: 6px; border: 1px solid #E2E8F0; }}
</style>
</head>
<body>
<div class="wrapper">
    <header>
        <div class="title">{html.escape(titulo)}</div>
        <div style="color: #64748B;">Objetivo: {html.escape(objetivo)}</div>
    </header>
    <div class="grid">
        <div>
            <div class="box">
                <div class="box-title">Matriz de Desempenho Operacional GRO</div>
                <table>
                    <thead><tr><th>Critérios Avaliados</th>{header_alternativas}</tr></thead>
                    <tbody>{linhas_criterios}<tr style="background: #E2E8F0; font-weight: bold;"><td style="background: #CBD5E1;">ÍNDICE DE CONFORMIDADE</td>{linha_medias}</tr></tbody>
                </table>
            </div>
            <div class="box">
                <div class="box-title">Estratégia Recomendada</div>
                <div style="background: #EFF6FF; padding: 10px; border-radius: 4px; font-weight: bold; margin-bottom: 8px;">
                    Diretriz Campeã: {html.escape(ROTULOS_CENARIOS[ranking[0][0]])}
                </div>
                <ol style="margin: 0; padding-left: 20px;">{ranking_html}</ol>
            </div>
        </div>
        <div>
            <div class="box">
                <div class="box-title">Evidências e Fatos Levantados</div>
                <p style="text-align: justify; margin: 0 0 10px 0;">{html.escape(contexto)}</p>
                <div style="background: #F8FAFC; padding: 8px; border-radius: 4px; font-size: 10.5px;">
                    <strong>Histórico Recente de Campo:</strong>
                    <ul style="margin: 5px 0 0 0; padding-left: 15px;">{logs_renderizados}</ul>
                </div>
            </div>
        </div>
    </div>
</div>
</body>
</html>
"""

# ==============================================================================
# 5. SIDEBAR: MONITORAMENTO E ENTRADA DE DADOS
# ==============================================================================
with st.sidebar:
    st.markdown("### ⚙️ Painel de Setup do Jogo")
    
    if not st.session_state.jogo_iniciado:
        st.session_state.num_jogadores = st.slider("Selecione a quantidade de Auditores (1 a 7):", min_value=1, max_value=7, value=st.session_state.num_jogadores)
        
        jogadores_temp = []
        for i in range(st.session_state.num_jogadores):
            pool_item = PERSONAGENS_POOL[i % len(PERSONAGENS_POOL)]
            nome_j = st.text_input(f"Nome do Jogador {i+1}", value=f"Auditor {i+1}", key=f"nome_j_{i}")
            
            jogadores_temp.append({
                "id": i + 1,
                "nome": nome_j,
                "char": pool_item["nome"],
                "cargo": pool_item["cargo"],
                "emoji": pool_item["emoji"],
                "cor": pool_item["cor"],
                "skill": pool_item["skill"],
                "score": 0,
                "posicao": 0
            })
            
        if st.button("🚀 Iniciar Partida de Tabuleiro", type="primary", use_container_width=True):
            st.session_state.jogadores = jogadores_temp
            st.session_state.jogo_iniciado = True
            st.session_state.rodada_atual = 1
            st.session_state.pergunta_atual_index = 0
            st.session_state.historico_eventos = []
            registrar_evento("O Tabuleiro do GRO foi montado com sucesso.")
            st.rerun()
    else:
        st.subheader("🏆 Leaderboard Ativo")
        for p in st.session_state.jogadores:
            st.markdown(f"""
            <div class="player-sidebar-card" style="border-left: 4px solid {p['cor']};">
                <div style="font-weight:700; color:#0F172A; font-size:13px;">{p['emoji']} {p['nome']}</div>
                <div style="font-size:11px; color:#64748B;">{p['char']} ({p['cargo']})</div>
                <div style="display:flex; justify-content:space-between; margin-top:5px; font-weight:700; font-size:12px; color:#2563EB;">
                    <span>Casa Atual: {p['posicao']}</span>
                    <span>{p['score']} pts</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        st.divider()
        if st.button("🔄 Reiniciar Jogo", type="secondary", use_container_width=True):
            st.session_state.jogo_iniciado = False
            st.rerun()

# ==============================================================================
# 6. LAYOUT CENTRAL - TITULOS E ABAS DE RECURSOS EXPANDIDOS
# ==============================================================================
st.markdown("<div class='main-title'>Simulador e Tabuleiro Interativo NR-1 / GRO</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Mecanismo Gamificado de Auditoria Operacional e Tomada de Decisão Multicritério</div>", unsafe_allow_html=True)

tab_jogo, tab_legislacao, tab_teses = st.tabs([
    "🎲 Tabuleiro de Jogo Dinâmico",
    "📜 Legislações e Links Oficiais MTE",
    "🔬 Artigos Técnicos e Acerco Científico"
])

# ------------------------------------------------------------------------------
# TAB 1: O TABULEIRO COMPLETO EM BLOCOS VISUAIS
# ------------------------------------------------------------------------------
with tab_jogo:
    if not st.session_state.jogo_iniciado:
        st.info("💡 Escolha a quantidade de jogadores e preencha os nomes na barra lateral para ativar o tabuleiro interativo.")
    else:
        st.markdown("### 🗺️ Mapa de Progresso do Tabuleiro GRO")
        
        html_tiles = ""
        for n_casa in range(18):
            casa_info = CASAS_TABULEIRO[n_casa]
            is_special = "board-tile-special" if casa_info["tipo"] == "especial" else ""
            
            tokens_jogadores = ""
            for p in st.session_state.jogadores:
                if p["posicao"] % 18 == n_casa:
                    tokens_jogadores += f'<span class="player-token" style="background-color:{p["cor"]};">{p["emoji"]} {p["nome"]}</span>'
            
            html_tiles += f"""
            <div class="board-tile {is_special}">
                <div class="tile-number">#{n_casa}</div>
                <div class="tile-label">{casa_info['titulo']}</div>
                <div style="margin-top: auto;">{tokens_jogadores}</div>
            </div>
            """
            
        st.markdown(f'<div class="board-grid">{html_tiles}</div>', unsafe_allow_html=True)
        st.divider()
        
        idx_vez = st.session_state.pergunta_atual_index % len(st.session_state.jogadores)
        j_vez = st.session_state.jogadores[idx_vez]
        
        c_mecanica, c_auditoria = st.columns([0.45, 0.55])
        
        with c_mecanica:
            st.markdown(f"#### 🎯 Vez de Jogar: **{j_vez['nome']}**")
            st.caption(f"Função Ativa: {j_vez['char']} | Habilidade Especial: {j_vez['skill']}")
            
            cc1, cc2 = st.columns([0.5, 0.5])
            with cc1:
                if st.button("🎲 Rolar Dado Corporativo", use_container_width=True, type="primary"):
                    st.session_state.dado_resultado = random.randint(1, 6)
                    j_vez["posicao"] += st.session_state.dado_resultado
                    registrar_evento(f"{j_vez['nome']} rolou {st.session_state.dado_resultado} e avançou para a Casa {j_vez['posicao'] % 18}.")
                    st.session_state.resposta_enviada = False
                    st.rerun()
            with cc2:
                st.markdown(f"<div style='font-size:16px; font-weight:bold; text-align:center; background:#F1F5F9; border:1px solid #CBD5E1; padding:8px; border-radius:8px; color:#1E3A8A;'>Dado: {st.session_state.dado_resultado}</div>", unsafe_allow_html=True)
                
            st.divider()
            
            q_idx = st.session_state.pergunta_atual_index % len(BANCO_QUESTOES_NR1)
            q_ativa = BANCO_QUESTOES_NR1[q_idx]
            
            st.markdown(f"##### 📑 Desafio Técnico: {q_ativa['tema']}")
            st.markdown(f"<div style='background:white; padding:12px; border:1px solid #E2E8F0; border-radius:8px; margin-bottom:12px;'>{q_ativa['pergunta']}</div>", unsafe_allow_html=True)
            
            resp_sel = st.radio("Selecione sua resposta fundamentada na norma:", q_ativa["opcoes"], key=f"r_{st.session_state.pergunta_atual_index}")
            
            if st.button("Submeter Resposta para Análise", use_container_width=True):
                st.session_state.resposta_enviada = True
                idx_sel = q_ativa["opcoes"].index(resp_sel)
                
                if idx_sel == q_ativa["correta"]:
                    j_vez["score"] += 20
                    # Correção das chaves internas para evitar KeyError
                    st.session_state.matriz_dinamica["Cenario_4"][1] = min(5, st.session_state.matriz_dinamica["Cenario_4"][1] + 1)
                    registrar_evento(f"✅ {j_vez['nome']} ACERTOU! Score subiu na Matriz GRO.")
                else:
                    j_vez["score"] = max(0, j_vez["score"] - 10)
                    st.session_state.matriz_dinamica["Cenario_1"][1] = max(1, st.session_state.matriz_dinamica["Cenario_1"][1] - 1)
                    registrar_evento(f"❌ {j_vez['nome']} ERROU. Risco legal alterado.")
                    
                st.session_state.pergunta_atual_index += 1
                if st.session_state.pergunta_atual_index % len(st.session_state.jogadores) == 0:
                    st.session_state.rodada_atual += 1
                st.rerun()
                
            st.markdown("##### 📟 Histórico em Tempo Real (Logs do Painel)")
            log_str = "".join(f"<div class='console-line'>{l}</div>" for l in st.session_state.historico_eventos)
            st.markdown(f"<div class='console-box'>{log_str}</div>", unsafe_allow_html=True)
            
        with c_auditoria:
            st.markdown("#### 📋 Relatório de Auditoria A4 em Tempo Real")
            tx_tit = st.text_input("Título Executivo do Relatório", value="Parecer Técnico Consolidador de Riscos Ocupacionais (NR-1)")
            tx_obj = st.text_input("Objetivo Estratégico", value="Adequação e mitigação de contingências corporativas de SST.")
            tx_ctx = st.text_area("Evidências Narrativas", value="Identificou-se conformidade nos processos de treinamento continuado de terceiros conforme NR-1.", height=80)
            
            html_a4 = gerar_html_boardgame(tx_tit, tx_obj, tx_ctx, st.session_state.matriz_dinamica, st.session_state.historico_eventos)
            st.components.v1.html(html_a4, height=450, scrolling=True)
            
            st.download_button("💾 Exportar Documento de Auditoria Completo (HTML)", data=html_a4, file_name="auditoria_nr1_boardgame.html", mime="text/html", use_container_width=True)

# ------------------------------------------------------------------------------
# TAB 2: ACERVO COMPLETO DE LEGISLAÇÃO E DOCUMENTOS OFICIAIS
# ------------------------------------------------------------------------------
with tab_legislacao:
    st.markdown("### 🏛️ Central de Ativos Regulatórios e Fontes Oficiais Primárias")
    st.markdown("* **[Texto Oficial Integral da NR-1 (SST/MTE)](https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/inspecao-do-trabalho/seguranca-e-saude-no-trabalho/sst-portarias/normas-regulamentadoras/nr-01-atualizada-2022.pdf)**")
    st.markdown("* **[Guia Técnico Prático de Implementação do PGR](https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/inspecao-do-trabalho/seguranca-e-saude-no-trabalho/pgr/guia_pratico_pgr.pdf)**")

# ------------------------------------------------------------------------------
# TAB 3: EVIDÊNCIAS CIENTÍFICAS, TESES E ARTIGOS REVISADOS POR PARES
# ------------------------------------------------------------------------------
with tab_teses:
    st.markdown("### 🔬 Repositório Científico Avançado e Teses Acadêmicas")
    st.markdown("* **[Revista Brasileira de Saúde Ocupacional (RBSO) - SciELO](https://www.scielo.br/j/rbso/)**")
    st.markdown("* **[Portal de Publicações Técnicas da Fundacentro](https://www.fundacentro.gov.br/)**")
