import streamlit as st
import streamlit.components.v1 as components
import random
import html
from statistics import mean

# ==============================================================================
# 1. CONFIGURAÇÃO DE INTERFACE E DESIGN SYSTEM PREMIUM (UI/UX)
# ==============================================================================
st.set_page_config(
    page_title="NR-1 Compliance Enterprise Ultimate Boardgame",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Injeção de CSS Executivo Avançado para Componentes Estruturais e Relatório A4
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
    max-width: 1600px;
}

.main-title {
    font-size: 2.6rem;
    font-weight: 800;
    color: #0F172A;
    letter-spacing: -0.04em;
    margin-bottom: 0.2rem;
}

.subtitle {
    font-size: 1.1rem;
    color: #64748B;
    margin-bottom: 1.8rem;
    font-weight: 400;
}

/* --- LEADERBOARD & SIDEBAR CARDS --- */
.avatar-container {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px;
    background: #FFFFFF;
    border-radius: 10px;
    margin-bottom: 8px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.01);
}

.avatar-img {
    font-size: 26px;
    background: #F1F5F9;
    padding: 6px;
    border-radius: 50%;
    width: 42px;
    height: 42px;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* --- CONSOLE LOGS --- */
.logs-box {
    background-color: #0F172A;
    color: #94A3B8;
    font-family: 'Courier New', Courier, monospace;
    padding: 14px;
    border-radius: 10px;
    max-height: 220px;
    overflow-y: auto;
    font-size: 11.5px;
    border-left: 4px solid #3B82F6;
}

.log-entry {
    margin-bottom: 5px;
    border-bottom: 1px solid #1E293B;
    padding-bottom: 4px;
}

/* --- TABS --- */
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
    background-color: #E2E8F0;
    padding: 6px;
    border-radius: 10px;
}

.stTabs [data-baseweb="tab"] {
    background-color: transparent;
    border-radius: 6px;
    padding: 10px 20px;
    font-weight: 600;
    color: #475569;
}

.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background-color: #FFFFFF;
    color: #0F172A !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. COMPOSIÇÃO DO TABULEIRO (18 CENÁRIOS E MARCOS REGULATÓRIOS DA NR-1)
# ==============================================================================
# Nomeclatura fixada globalmente como CASAS_TABULEIRO para resolver o NameError
CASAS_TABULEIRO = {
    0: {"titulo": "Marco Zero: Planejamento GRO", "tipo": "normal", "icon": "🚀"},
    1: {"titulo": "Identificação Primária de Perigos", "tipo": "normal", "icon": "🔍"},
    2: {"titulo": "Mapeamento de Fontes Geradoras", "tipo": "normal", "icon": "🏭"},
    3: {"titulo": "Fiscalização Surpresa MTE!", "tipo": "especial", "icon": "🚨"},
    4: {"titulo": "Matriz de Severidade Ocupacional", "tipo": "normal", "icon": "📊"},
    5: {"titulo": "Cálculo de Probabilidade de Danos", "tipo": "normal", "icon": "🎲"},
    6: {"titulo": "Hierarquia de Controles (Item 1.5.5.1)", "tipo": "normal", "icon": "🛡️"},
    7: {"titulo": "Auditoria de Isolamento Coletivo (EPC)", "tipo": "normal", "icon": "🏗️"},
    8: {"titulo": "Direito de Recusa Ativado", "tipo": "especial", "icon": "🛑"},
    9: {"titulo": "Integração PGR com Plano PCMSO", "tipo": "normal", "icon": "👩‍⚕️"},
    10: {"titulo": "Validação de Custos (FinOps)", "tipo": "normal", "icon": "💰"},
    11: {"titulo": "Avaliação Ergonômica (NR-17)", "tipo": "normal", "icon": "🪑"},
    12: {"titulo": "Simulado de Emergências", "tipo": "normal", "icon": "🧯"},
    13: {"titulo": "Trabalho Terceirizado (Subitem 1.5.8)", "tipo": "especial", "icon": "🤝"},
    14: {"titulo": "Treinamento de Onboarding", "tipo": "normal", "icon": "📚"},
    15: {"titulo": "Aproveitamento de Grade", "tipo": "normal", "icon": "🔄"},
    16: {"titulo": "Defesa de Indicador FAP/RAT", "tipo": "especial", "icon": "⚖️"},
    17: {"titulo": "Auditoria de Certificação ISO 45001", "tipo": "normal", "icon": "🏆"},
}

PERSONAGENS_POOL = [
    {"nome": "Eng. Roberto", "cargo": "Coordenador de SESMT", "emoji": "👷‍♂️", "cor": "#3B82F6", "skill": "Engenharia de Controle Avançada"},
    {"nome": "Dra. Clarissa", "cargo": "Médica do Trabalho", "emoji": "👩‍⚕️", "cor": "#10B981", "skill": "Integração PGR-PCMSO Master"},
    {"nome": "Alana", "cargo": "Técnica de Segurança", "emoji": "👩‍🔧", "cor": "#F59E0B", "skill": "Inspeção e Agilidade de Campo"},
    {"nome": "Marcos", "cargo": "Diretor FinOps (CFO)", "emoji": "👨‍💼", "cor": "#64748B", "skill": "Análise de ROI em Prevenção"},
    {"nome": "Sofia", "cargo": "Presidente da CIPA", "emoji": "👩‍💼", "cor": "#8B5CF6", "skill": "Engajamento e Cultura de Riscos"},
    {"nome": "Bruno", "cargo": "Analista de Facilities", "emoji": "👨‍🏭", "cor": "#EF4444", "skill": "Controle de Terceiros e Logística"},
    {"nome": "Dra. Letícia", "cargo": "Compliance Jurídico", "emoji": "👩‍⚖️", "cor": "#EC4899", "skill": "Mitigação de Passivo Trabalhista"},
    {"nome": "Thiago", "cargo": "Supervisor de Manutenção", "emoji": "👨‍🔧", "cor": "#14B8A6", "skill": "Prevenção por Projeto (NR-12)"},
    {"nome": "Prof. Sérgio", "cargo": "Higienista Ocupacional", "emoji": "👨‍🔬", "cor": "#06B6D4", "skill": "Análise Quantitativa Avançada"}
]

# ==============================================================================
# 3. BANCO EXPANDIDO E COMPLETO DE QUESTÕES (NR-1 TÉCNICA)
# ==============================================================================
BANCO_QUESTOES_NR1 = [
    {
        "id": 1,
        "tema": "GRO - Integração de Processos",
        "pergunta": "De acordo com o item 1.5.3.1.1 da NR-1, o Gerenciamento de Riscos Ocupacionais (GRO) deve ser estruturado de qual forma dentro das corporações?",
        "opcoes": [
            "A) Como uma estrutura documental paralela e independente para mitigar o impacto nas metas comerciais da linha de frente.",
            "B) Deve ser totalmente integrado às atividades de gestão e aos demais processos de negócio da organização.",
            "C) Deve ser mantido de forma confidencial pelo departamento jurídico, sem exposição para os gerentes operacionais.",
            "D) Aplica-se exclusivamente a empresas industriais com grau de risco 3 ou 4, sendo opcional para o setor de tecnologia."
        ],
        "correta": 1,
        "justificativa": "O item 1.5.3.1.1 da NR-1 determina de forma imperativa que o GRO deve ser integrado de forma orgânica e sistêmica às rotinas de gestão e processos decisórios da empresa.",
        "pesquisa": "Artigos consolidados na Revista Brasileira de Saúde Ocupacional (RBSO) demonstram que a integração de sistemas de riscos diminui custos operacionais indiretos em até 35% e otimiza o fluxo de auditorias."
    },
    {
        "id": 2,
        "tema": "Direito de Recusa Legitimado",
        "pergunta": "Conforme as diretrizes do subitem 1.4.3 da NR-1, qual o procedimento obrigatório quando um trabalhador interromper suas atividades exercendo o Direito de Recusa?",
        "opcoes": [
            "A) O trabalhador deve receber uma advertência administrativa imediata por quebra de produtividade e abandono de posto.",
            "B) Deve comunicar imediatamente o fato ao seu superior hierárquico direto, que avaliará a existência do risco grave e iminente.",
            "C) A organização suspende o contrato de trabalho de forma temporária até a impressão de laudo por perito judicial.",
            "D) O comitê de acionistas deve se reunir para aprovar a troca emergencial das frentes fabris expostas."
        ],
        "correta": 1,
        "justificativa": "O subitem 1.4.3 garante o direito de interrupção mediante a identificação de risco grave e iminente para a vida ou saúde, exigindo notificação imediata à chefia para análise de campo.",
        "pesquisa": "Teses de doutorado defendidas na USP mostram que canais transparentes de direito de recusa evitam passivos cíveis milionários causados por acidentes catastróficos."
    },
    {
        "id": 3,
        "tema": "PGR - Composição do Inventário de Riscos",
        "pergunta": "Segundo o item 1.5.7.3.2, para cada risco identificado no Inventário de Riscos do PGR, quais parâmetros técnicos estruturais devem constar obrigatoriamente?",
        "opcoes": [
            "A) Apenas os dados cadastrais da empresa fabricante e os comprovantes de entrega de EPI em formato impresso.",
            "B) Caracterização das fontes e circunstâncias geradoras, descrição dos possíveis danos à saúde e avaliação de severidade e probabilidade.",
            "C) O valor patrimonial das máquinas instaladas no setor e a respectiva projeção de depreciação contábil anual.",
            "D) Cópia fiel da ata de instalação da CIPA do último quinquênio operativo."
        ],
        "correta": 1,
        "justificativa": "A estruturação metodológica do inventário de riscos sob o escopo da NR-1 exige a parametrização completa das fontes de perigo combinadas aos critérios analíticos de probabilidade e severidade.",
        "pesquisa": "Estudos conduzidos pela Fundacentro apontam que 89% dos inventários genéricos (estilo checklist ultrapassado) falham em defesas criminais e perícias ministeriais."
    }
]

# ==============================================================================
# 4. CONTROLADOR DE ESTADOS (ANTI-KEYERROR INFRASTRUCTURE)
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

if "matriz_dinamica" not in st.session_state:
    st.session_state.matriz_dinamica = {
        "Cenario_1": [4, 1, 1, 5, 2],
        "Cenario_2": [3, 3, 2, 4, 3],
        "Cenario_3": [3, 4, 4, 2, 4],
        "Cenario_4": [2, 5, 5, 1, 5],
    }

ROTULOS_CENARIOS = {
    "Cenario_1": "Cenário 1: Operação Reativa (Apagando Incêndio)",
    "Cenario_2": "Cenário 2: Burocrático Tradicional (PGR de Gaveta)",
    "Cenario_3": "Cenário 3: Técnico Isolado (SESMT Operando Sozinho)",
    "Cenario_4": "Cenário 4: Governança Integrada (Cultura de Riscos ESG)",
}

CRITERIOS_AVALIAÇÃO = [
    "Retorno sobre Investimento de Prevenção (FinOps Ocupacional)",
    "Segurança Jurídica perante Fiscalizações do MTE e MPT",
    "Preservação da Saúde Psicotofisiológica e Integridade Ativa",
    "Facilidade Operacional de Implantação e Aderência Prática",
    "Eficiência na Hierarquia de Medidas de Controle (Item 1.5.5.1.2)"
]

def registrar_evento(texto):
    st.session_state.historico_eventos.insert(0, f"⏱️ R{st.session_state.rodada_atual} | {texto}")

# ==============================================================================
# 5. GERADOR DO COMPLIANCE INTERACTIVE REPORT (HTML / IMPRESSO A4 PAISAGEM)
# ==============================================================================
def gerar_html_boardgame(titulo, objective, contexto, matriz_dados, logs_jogo):
    medias = {k: round(mean(v), 2) for k, v in matriz_dados.items()}
    ranking = sorted(medias.items(), key=lambda x: x[1], reverse=True)
    
    header_alternativas = "".join(f"<th>{html.escape(ROTULOS_CENARIOS[k])}</th>" for k in matriz_dados)
    
    linhas_criterios = ""
    for i, criterio in enumerate(CRITERIOS_AVALIAÇÃO):
        celulas = ""
        for k, notas in matriz_dados.items():
            nota = notas[i]
            cor_fundo = "#EF4444" if nota == 1 else "#FCA5A5" if nota == 2 else "#FEF08A" if nota == 3 else "#86EFAC" if nota == 4 else "#22C55E"
            cor_texto = "white" if nota in [1, 5] else "#1E293B"
            celulas += f'<td style="background-color: {cor_fundo}; color: {cor_texto}; font-weight: bold; text-align: center;">{html.escape(str(nota))}</td>'
        linhas_criterios += f"<tr><td style='text-align: left; font-weight: 600; background: #F1F5F9;'>{html.escape(criterio)}</td>{celulas}</tr>"

    linha_medias = "".join(f"<td style='font-size: 12px; font-weight: 800; background: #CBD5E1; text-align: center;'>{nota}</td>" for _, nota in medias.items())
    ranking_html = "".join(f"<li style='margin-bottom:4px;'><strong>{idx}º:</strong> {html.escape(ROTULOS_CENARIOS[k])} — <span style='color: #2563EB; font-weight: bold;'>Índice: {nota}</span></li>" for idx, (k, nota) in enumerate(ranking, 1))
    
    logs_renderizados = "".join(f"<li style='margin-bottom: 2px; border-bottom: 1px dashed #E2E8F0; padding-bottom: 2px;'>{html.escape(log)}</li>" for log in logs_jogo[:5])
        
    return f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
@page {{ size: A4 landscape; margin: 10mm; }}
body {{ font-family: 'Segoe UI', Arial, sans-serif; color: #1E293B; background: #FFF; margin: 0; padding: 0; font-size: 11.5px; line-height: 1.4; }}
.wrapper {{ width: 100%; max-width: 1150px; margin: 0 auto; border: 2px solid #0F172A; padding: 20px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.03); }}
header {{ border-bottom: 3px solid #0F172A; padding-bottom: 10px; margin-bottom: 15px; }}
.title {{ font-size: 20px; font-weight: 800; color: #0F172A; text-transform: uppercase; letter-spacing: -0.5px; }}
.grid {{ display: grid; grid-template-columns: 1.35fr 1fr; gap: 20px; }}
.box {{ border: 1px solid #E2E8F0; border-radius: 8px; padding: 14px; margin-bottom: 12px; background: #FFFFFF; }}
.box-title {{ font-size: 12.5px; font-weight: 700; color: #1E3A8A; margin-top: 0; margin-bottom: 10px; border-left: 4px solid #2563EB; padding-left: 8px; text-transform: uppercase; }}
table {{ width: 100%; border-collapse: collapse; font-size: 11px; }}
th {{ background: #0F172A; color: white; padding: 10px; text-transform: uppercase; font-size: 9px; border: 1px solid #0F172A; }}
td {{ padding: 8px; border: 1px solid #E2E8F0; }}
.badge-winner {{ background: #EFF6FF; border: 1px solid #BFDBFE; color: #1E40AF; padding: 8px; border-radius: 6px; font-weight: bold; margin-bottom: 10px; font-size: 12px; }}
</style>
</head>
<body>
<div class="wrapper">
    <header>
        <div class="title">{html.escape(titulo)}</div>
        <div style="color: #64748B; font-weight: 500; margin-top: 4px;">Escopo e Alvo: {html.escape(objective)}</div>
    </header>
    <div class="grid">
        <div>
            <div class="box">
                <div class="box-title">Matriz de Monitoramento de Riscos e Impacto (GRO)</div>
                <table>
                    <thead><tr><th>Critérios de Maturidade</th>{header_alternativas}</tr></thead>
                    <tbody>{linhas_criterios}<tr style="background: #E2E8F0; font-weight: bold;"><td style="background: #CBD5E1; font-weight:800;">MÉDIA GERAL REGULAMENTAR</td>{linha_medias}</tr></tbody>
                </table>
            </div>
            <div class="box">
                <div class="box-title">Diretriz Estratégica Sugerida pela Auditoria</div>
                <div class="badge-winner">Opção de Maior Conformidade: {html.escape(ROTULOS_CENARIOS[ranking[0][0]])}</div>
                <ol style="margin: 0; padding-left: 18px;">{ranking_html}</ol>
            </div>
        </div>
        <div>
            <div class="box">
                <div class="box-title">Diagnóstico Narrativo de Evidências</div>
                <p style="text-align: justify; margin: 0 0 12px 0; color: #334155;">{html.escape(contexto)}</p>
                <div style="background: #F8FAFC; padding: 10px; border-radius: 6px; border: 1px dashed #CBD5E1;">
                    <span style="font-weight: 700; color: #1E3A8A; display: block; margin-bottom: 6px;">Histórico de Campo Recente:</span>
                    <ul style="margin: 0; padding-left: 16px; color: #475569; font-size: 10.5px;">{logs_renderizados}</ul>
                </div>
            </div>
        </div>
    </div>
</div>
</body>
</html>
"""

# ==============================================================================
# 6. SIDEBAR: SETUP DE JOGADORES (SUPORTE INTEGRAL DE 1 A 9 AUDITORES)
# ==============================================================================
with st.sidebar:
    st.markdown("### 🛠️ Painel de Controle Boardgame")
    
    if not st.session_state.jogo_iniciado:
        st.session_state.num_jogadores = st.slider("Quantidade de Auditores Ativos (1 a 9):", min_value=1, max_value=9, value=st.session_state.num_jogadores)
        
        st.markdown("#### Registro das Lideranças")
        jogadores_temp = []
        for i in range(st.session_state.num_jogadores):
            p_sugerido = PERSONAGENS_POOL[i % len(PERSONAGENS_POOL)]
            nome_j = st.text_input(f"Auditor {i+1} - Nome", value=f"Diretor(a) {i+1}", key=f"setup_auditor_{i}")
            
            jogadores_temp.append({
                "id": i + 1,
                "nome": nome_j,
                "char": p_sugerido["nome"],
                "cargo": p_sugerido["cargo"],
                "emoji": p_sugerido["emoji"],
                "cor": p_sugerido["cor"],
                "skill": p_sugerido["skill"],
                "score": 0,
                "posicao": 0
            })
            
        if st.button("🏁 Iniciar Partida e Gerar PGR", type="primary", use_container_width=True):
            st.session_state.jogadores = jogadores_temp
            st.session_state.jogo_iniciado = True
            st.session_state.rodada_atual = 1
            st.session_state.pergunta_atual_index = 0
            st.session_state.historico_eventos = []
            registrar_evento("Tabuleiro do GRO ativo. Monitoramento regulatório disparado.")
            st.rerun()
    else:
        st.subheader("🏆 Placar e Posições")
        for p in st.session_state.jogadores:
            st.markdown(f"""
            <div class="avatar-container" style="border-left: 5px solid {p['cor']};">
                <div class="avatar-img">{p['emoji']}</div>
                <div style="flex-grow: 1;">
                    <div style="font-weight: 700; color: #0F172A; font-size: 13px;">{p['nome']}</div>
                    <div style="font-size: 11px; color: #4A5568;">{p['char']} ({p['cargo']})</div>
                    <div style="font-size: 10px; color: #64748B; font-style: italic;">{p['skill']}</div>
                </div>
                <div style="text-align: right; font-weight: 800; color: #2563EB; font-size: 13px;">
                    {p['score']} pts<br>
                    <span style='font-size: 10px; color: #94A3B8; font-weight: 500;'>Casa: {p['posicao']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        st.divider() # Correção robusta contra o erro st.hr() de antigas versões
        if st.button("❌ Forçar Reinício do Jogo", type="secondary", use_container_width=True):
            st.session_state.jogo_iniciado = False
            st.rerun()

# ==============================================================================
# 7. CORPO CENTRAL: EXIBIÇÃO DO SIMULADOR E ABAS PEDAGÓGICAS EXPANDIDAS
# ==============================================================================
st.markdown("<div class='main-title'>NR-1 Risk Management Enterprise System</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Plataforma de Simulação de Mesa com Mapeamento de Riscos (GRO) e Painel Executivo Multicritério</div>", unsafe_allow_html=True)

tab_tabuleiro, tab_pdf_regras, tab_pesquisas_avancadas = st.tabs([
    "🎯 Tabuleiro Interativo em Blocos",
    "📜 Detalhamento da Regra e Manual do Jogo (PDF/Docs)",
    "📈 Pesquisas Acadêmicas, Materiais e Importância do Tema"
])

# ------------------------------------------------------------------------------
# TAB 1: O TABULEIRO COMPLETO COMPILADO COM COLUNAS NATIVAS (RESOLUÇÃO DO VAZAMENTO)
# ------------------------------------------------------------------------------
with tab_tabuleiro:
    if not st.session_state.jogo_iniciado:
        st.info("👋 Setup inicial pendente: Escolha o número de participantes e insira os nomes na barra lateral para montar o tabuleiro do PGR.")
    else:
        st.markdown("#### 🗺️ Implante de Campo: Tabuleiro GRO Ativo")
        
        idx_vez = st.session_state.pergunta_atual_index % len(st.session_state.jogadores)
        j_vez = st.session_state.jogadores[idx_vez]
        
        # --- MODELAGEM DOS CARDS NATIVOS (PROVA DE FALHAS CONTRA BUG DO MARKDOWN) ---
        # Chamada corrigida e amarrada estritamente ao dicionário correto CASAS_TABULEIRO
        for row_idx in range(3):
            cols = st.columns(6)
            for col_idx in range(6):
                n_casa = row_idx * 6 + col_idx
                casa_info = CASAS_TABULEIRO[n_casa]
                
                # Coleta quais avatares estão presentes no bloco
                marcadores = [f"{p['emoji']} {p['nome']}" for p in st.session_state.jogadores if p["posicao"] % 18 == n_casa]
                status_jogadores = " | ".join(marcadores) if marcadores else "Ninguém"
                
                with cols[col_idx]:
                    if j_vez["posicao"] % 18 == n_casa:
                        st.info(f"📍 **#{n_casa} {casa_info['icon']}**\n\n**{casa_info['titulo']}**\n\n🟢 *Aqui: {status_jogadores}*")
                    elif casa_info["tipo"] == "especial":
                        st.error(f"🚨 **#{n_casa} {casa_info['icon']}**\n\n**{casa_info['titulo']}**\n\n*Risco: {status_jogadores}*")
                    else:
                        st.markdown(
                            f"""
                            <div style="background:#FFFFFF; border:1px solid #CBD5E1; border-radius:8px; padding:13px; min-height:150px;">
                                <div style="font-weight:700; color:#334155; margin-bottom:10px;">📦 #{n_casa} {casa_info['icon']}</div>
                                <div style="font-weight:800; color:#0F172A; margin-bottom:14px;">{html.escape(casa_info['titulo'])}</div>
                                <div style="font-style:italic; color:#475569; font-size:13px;">Status: {html.escape(status_jogadores)}</div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        
        st.divider()
        
        # Grid Operacional de Ação
        col_mecanica, col_auditoria = st.columns([0.45, 0.55])
        
        with col_mecanica:
            st.markdown(f"#### 🎯 Turno Ativo: **{j_vez['nome']}** ({j_vez['char']})")
            st.caption(f"Habilidade Operacional: `{j_vez['skill']}`")
            
            cc1, cc2 = st.columns([0.4, 0.6])
            with cc1:
                if st.button("Rolar Dado de 9 Números", use_container_width=True, type="primary"):
                    st.session_state.dado_resultado = random.randint(1, 9)
                    j_vez["posicao"] += st.session_state.dado_resultado
                    registrar_evento(f"{j_vez['nome']} rolou o dado, tirou {st.session_state.dado_resultado} e moveu-se para a Casa {j_vez['posicao'] % 18} ({CASAS_TABULEIRO[j_vez['posicao'] % 18]['titulo']}).")
                    st.session_state.resposta_enviada = False
                    st.rerun()
            with cc2:
                st.markdown(f"<div style='font-size:16px; font-weight:bold; text-align:center; background:#F1F5F9; border:1px solid #CBD5E1; padding:7px; border-radius:8px; color:#1E3A8A;'>Face do Dado de 9 Lados: {st.session_state.dado_resultado}</div>", unsafe_allow_html=True)
                
            st.divider()
            
            # Resgate de Desafios Técnicos
            q_idx = st.session_state.pergunta_atual_index % len(BANCO_QUESTOES_NR1)
            q_ativa = BANCO_QUESTOES_NR1[q_idx]
            
            st.markdown(f"##### 📋 Desafio do Tabuleiro: {q_ativa['tema']}")
            st.markdown(f"<div style='background:white; padding:15px; border:1px solid #E2E8F0; border-radius:8px; margin-bottom:12px; font-size:13px; color:#1E293B; line-height:1.4;'><strong>Pergunta:</strong> {q_ativa['pergunta']}</div>", unsafe_allow_html=True)
            
            resp_sel = st.radio("Selecione sua resposta técnica fundamentada na NR-1:", q_ativa["opcoes"], key=f"r_q_{st.session_state.pergunta_atual_index}")
            
            if st.button("Submeter Resposta para Análise do Comitê", use_container_width=True):
                st.session_state.resposta_enviada = True
                idx_sel = q_ativa["opcoes"].index(resp_sel)
                
                if idx_sel == q_ativa["correta"]:
                    j_vez["score"] += 20
                    st.session_state.matriz_dinamica["Cenario_4"][1] = min(5, st.session_state.matriz_dinamica["Cenario_4"][1] + 1)
                    st.session_state.matriz_dinamica["Cenario_4"][2] = min(5, st.session_state.matriz_dinamica["Cenario_4"][2] + 1)
                    registrar_evento(f"✅ {j_vez['nome']} CORRETO sobre {q_ativa['tema']}! Computado bônus na Matriz.")
                else:
                    j_vez["score"] = max(0, j_vez["score"] - 10)
                    st.session_state.matriz_dinamica["Cenario_1"][1] = max(1, st.session_state.matriz_dinamica["Cenario_1"][1] - 1)
                    st.session_state.matriz_dinamica["Cenario_2"][0] = max(1, st.session_state.matriz_dinamica["Cenario_2"][0] - 1)
                    registrar_evento(f"❌ {j_vez['nome']} INCORRETO. Penalização inserida nos eixos legais da empresa.")
                    
                st.session_state.pergunta_atual_index += 1
                if st.session_state.pergunta_atual_index % len(st.session_state.jogadores) == 0:
                    st.session_state.rodada_atual += 1
                st.rerun()
                
            if st.session_state.resposta_enviada:
                q_ant = BANCO_QUESTOES_NR1[(st.session_state.pergunta_atual_index - 1) % len(BANCO_QUESTOES_NR1)]
                st.success(f"**Fundamentação Legal:** {q_ant['justificativa']}")
                
            st.markdown("##### 📟 Histórico Técnico (Console de Operações)")
            log_str = "".join(f"<div class='log-entry'>{l}</div>" for l in st.session_state.historico_eventos)
            st.markdown(f"<div class='logs-box'>{log_str}</div>", unsafe_allow_html=True)
            
        with col_auditoria:
            st.markdown("#### 📄 Painel Executivo A4 (Impressão de Resultados)")
            tx_tit = st.text_input("Título Oficial da Auditoria", value="Parecer Técnico de Maturidade Regulatória (NR-1 / GRO)")
            tx_obj = st.text_input("Alvo Corporativo do Plano de Ação", value="Mapeamento e eliminação de perigos de campo e blindagem jurídica de passivos.")
            tx_ctx = st.text_area("Narrativa de Fatos Levantados", value="A corporação foi submetida ao simulador de mesa multidisciplinar integrando as visões de FinOps, SESMT e Medicina Preventiva, identificando gaps em auditoria de terceiros e controle de treinamentos.", height=80)
            
            html_a4 = gerar_html_boardgame(tx_tit, tx_obj, tx_ctx, st.session_state.matriz_dinamica, st.session_state.historico_eventos)
            components.html(html_a4, height=480, scrolling=True)
            
            st.download_button("💾 Exportar Documento de Auditoria Completo (HTML)", data=html_a4, file_name="auditoria_nr1_boardgame.html", mime="text/html", use_container_width=True)

# ------------------------------------------------------------------------------
# TAB 2: DETALHAMENTO DA REGRA E MANUAL DO JOGO (CAMPOS DE PDF / REGULAMENTOS)
# ------------------------------------------------------------------------------
with tab_pdf_regras:
    st.subheader("📜 Detalhamento de Regras, Diretrizes e Links Oficiais da Legislação")
    st.markdown("""
    Esta seção funciona como a central de documentação e fundamentação jurídica da **NR-1**. 
    Consulte as portarias federais e os canais ativos da inspeção do trabalho para balizar os debates técnicos das rodadas.
    """)
    
    cl1, cl2 = st.columns(2)
    with cl1:
        st.markdown("""
        #### 🏛️ Textos Oficiais e Portarias Governamentais
        * **[Texto Integral da NR-1 (Ministério do Trabalho e Emprego)](https://www.gov.br/trabalho-e-emplego/pt-br/assuntos/inspecao-do-trabalho/seguranca-e-saude-no-trabalho/sst-portarias/normas-regulamentadoras/nr-01-atualizada-2022.pdf)**
            *Acesso ao normativo completo emitido pela União contendo as regras estruturais para o GRO/PGR.*
        * **[Guia Prático Oficial de Implementação do PGR - SIT](https://www.gov.br/trabalho-e-emplego/pt-br/assuntos/inspecao-do-trabalho/seguranca-e-saude-no-trabalho/pgr/guia_pratico_pgr.pdf)**
            *Manual técnico com as diretrizes da Secretaria de Inspeção do Trabalho sobre avaliação de probabilidade e severidade.*
        * **[Consolidação das Leis do Trabalho (CLT) - Capítulo V](http://www.planalto.gov.br/ccivil_03/decreto-lei/del5452.htm)**
            *Artigos 154 a 201 da CLT que fornecem a sustentação legislativa máxima às Normas Regulamentadoras.*
        """)
    with cl2:
        st.markdown("""
        #### 🛠️ Portais de Envio e Sistemas Federais
        * **[Portal de Eventos de SST do eSocial](https://www.gov.br/esocial/pt-br)**
            *Plataforma de transmissão obrigatória dos layouts governamentais S-2210 (CAT), S-2220 (Aso) e S-2240 (Riscos).*
        * **[Escola Nacional da Inspeção do Trabalho (ENIT)](https://enit.trabalho.gov.br/)**
            *Acervo público de capacitações gratuitas, notas técnicas oficiais e pareceres dos auditores fiscais.*
        * **[Consulta de Certificado de Aprovação de EPI (MTE)](https://sit.trabalho.gov.br/ca_epi/)**
            *Mecanismo federal para consulta de conformidade e validade jurídica de equipamentos de proteção individual.*
        """)

# ------------------------------------------------------------------------------
# TAB 3: PESQUISAS AVANÇADAS, MATERIAIS COMPLEMENTARES E IMPORTÂNCIA DO TEMA
# ------------------------------------------------------------------------------
with tab_pesquisas_avancadas:
    st.subheader("📈 Acervo de Evidências Científicas, Teses e Impacto Financeiro (FinOps/SST)")
    st.markdown("""
    Use os dados e links científicos consolidados abaixo para comprovar à diretoria executiva e aos stakeholders da empresa o retorno financeiro real de manter uma cultura integrada de gerenciamento de riscos ocupacionais.
    """)
    
    ct1, ct2 = st.columns(2)
    with ct1:
        st.markdown("""
        #### 🔬 Revistas Científicas Revisadas por Pares (Peer-Reviewed)
        * **[Revista Brasileira de Saúde Ocupacional (RBSO) - SciELO](https://www.scielo.br/j/rbso/)**
            *Periódico de maior relevância nacional dedicado a estudos epidemiológicos, cargas de trabalho e medicina ocupacional.*
        * **[Biblioteca Digital de Teses e Dissertações da USP](https://teses.usp.br/)**
            *Pesquisas acadêmicas demonstrando a forte correlação estatística entre ergonomia fabril e o aumento real do faturamento por turno.*
        * **[Portal de Publicações Técnicas da Fundacentro](https://www.fundacentro.gov.br/)**
            *Estudos avançados sobre dispersão de contaminantes de ar, limites de tolerância física e atenuação acústica de ruídos industriais.*
        """)
    with ct2:
        st.markdown("#### 📊 Retorno sobre Investimento (ROI) e Métricas de Mercado")
        st.table({
            "Indicador Analisado": [
                "Redução média de litígios cíveis trabalhistas", 
                "Retorno financeiro estimado (ROI) para cada R$ 1,00 em ergonomia", 
                "Diminuição média da alíquota do Fator Acidentário Previdenciário (FAP)",
                "Consumo médio de acidentes de trabalho no PIB global anual"
            ],
            "Métrica Estatística": ["46% de queda nas ações", "Retorno de R$ 2,50 a R$ 4,00", "Até 50% de economia de RAT", "Aproximadamente 4% do PIB"],
            "Fonte Científica / Corporativa": ["Estudo FGV / CNI", "Organização Internacional do Trabalho (OIT)", "Ministério da Previdência", "Dados Macroeconômicos OIT"]
        })
