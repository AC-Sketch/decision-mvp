import streamlit as st
import random
import html
import json
from statistics import mean

# ==============================================================================
# 1. CONFIGURAÇÃO DE INTERFACE E DESIGN SYSTEM (STREAMLIT UI)
# ==============================================================================
st.set_page_config(
    page_title="NR-1 Compliance Enterprise Gamification System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS customizada para emular um Dashboard Executivo de Alta Performance
st.markdown("""
<style>
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 1.5rem;
    max-width: 1600px;
}
h1 {
    font-size: 2.5rem !important;
    font-weight: 800 !important;
    color: #1A365D;
    letter-spacing: -0.05em;
    margin-bottom: 0.5rem !important;
}
h2 {
    font-size: 1.6rem !important;
    font-weight: 700 !important;
    color: #2C5282;
    margin-top: 1rem !important;
    margin-bottom: 0.8rem !important;
}
h3 {
    font-size: 1.2rem !important;
    font-weight: 600 !important;
    color: #2B6CB0;
}
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
}
.stTabs [data-baseweb="tab"] {
    background-color: #EDF2F7;
    border-radius: 6px 6px 0px 0px;
    padding: 10px 20px;
    font-weight: 600;
    color: #4A5568;
}
.stTabs [data-baseweb="tab"]:hover {
    background-color: #E2E8F0;
    color: #1A365D;
}
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background-color: #2B6CB0;
    color: white !important;
}
.avatar-card {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px;
    background: #FFFFFF;
    border-radius: 8px;
    margin-bottom: 8px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    transition: transform 0.2s;
}
.avatar-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}
.avatar-emoji {
    font-size: 28px;
    background: #EDF2F7;
    padding: 6px;
    border-radius: 50%;
    width: 45px;
    height: 45px;
    display: flex;
    align-items: center;
    justify-content: center;
}
.badge-reg {
    display: inline-block;
    background: #EBF8FF;
    color: #2B6CB0;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 700;
    margin-right: 6px;
    border: 1px solid #BEE3F8;
}
.logs-box {
    background-color: #1A202C;
    color: #A0AEC0;
    font-family: 'Courier New', Courier, monospace;
    padding: 15px;
    border-radius: 6px;
    max-height: 220px;
    overflow-y: auto;
    font-size: 12px;
    border-left: 4px solid #3182CE;
}
.log-entry {
    margin-bottom: 4px;
    border-bottom: 1px solid #2D3748;
    padding-bottom: 4px;
}
iframe {
    border-radius: 8px;
    border: 1px solid #CBD5E0;
}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. BANCOS DE DADOS E INFRAESTRUTURA COMPLETA DA NR-1
# ==============================================================================

PERSONAGENS_POOL = [
    {"nome": "Eng. Roberto", "cargo": "Coordenador de SESMT", "emoji": "👷‍♂️", "cor": "#3182CE", "skill": "Bônus em Engenharia de Controle (Eliminação de Fontes)"},
    {"nome": "Dra. Clarissa", "cargo": "Médica do Trabalho", "emoji": "👩‍⚕️", "cor": "#319795", "skill": "Otimização de PCMSO Integrado ao PGR (Subitem 1.5.5.4.1)"},
    {"nome": "Alana", "cargo": "Técnica de Segurança", "emoji": "👩‍🔧", "cor": "#D69E2E", "skill": "Inspeção de Campo Ágil e Análise Causal de Desvios"},
    {"nome": "Marcos", "cargo": "Diretor de Operações (COO)", "emoji": "👨‍💼", "cor": "#4A5568", "skill": "Análise FinOps de SST (Custo de Oportunidade vs Penalidades)"},
    {"nome": "Sofia", "cargo": "Presidente da CIPA", "emoji": "👩‍💼", "cor": "#9F7AEA", "skill": "Engajamento Social, Diálogo Diário de Segurança e Percepção de Risco"},
    {"nome": "Bruno", "cargo": "Analista de Facilities", "emoji": "👨‍🏭", "cor": "#ED8936", "skill": "Sinalização Coletiva e Controle de Terceirizados (Subitem 1.5.8)"},
    {"nome": "Dra. Letícia", "cargo": "Auditora Jurídica / Compliance", "emoji": "👩‍⚖️", "cor": "#E53E3E", "skill": "Defesa contra Nexo Técnico Epidemiológico Previdenciário (NTEP)"},
    {"nome": "Thiago", "cargo": "Supervisor de Manutenção", "emoji": "👨‍🔧", "cor": "#38A169", "skill": "Gestão de Ativos Conforme NR-12 e Manutenções Preventivas Críticas"},
    {"nome": "Prof. Sérgio", "cargo": "Higienista Ocupacional", "emoji": "👨‍🔬", "cor": "#00B5D8", "skill": "Quantificação Avançada de Agentes Físicos, Químicos e Biológicos"}
]

# Matriz Inicial de Decisão Estratégica (Mapeamento de 5 eixos metodológicos)
MATRIZ_PADRAO = {
    "Cenário 1: Reativo (PGR Apagando Incêndio)": [4, 1, 1, 5, 2],
    "Cenário 2: Burocrático (PGR de Gaveta)": [3, 3, 2, 4, 3],
    "Cenário 3: Técnico (SESMT Isolado Operando)": [3, 4, 4, 2, 4],
    "Cenário 4: Integrado (Cultura de Riscos ESG)": [2, 5, 5, 1, 5],
}

CRITERIOS_ROTULOS = [
    "Retorno sobre Capital Empregado (ROIC / FinOps)",
    "Segurança Jurídica perante MTE e Ministério Público",
    "Preservação da Integridade Psicotofisiológica",
    "Facilidade de Implantação nos Processos Atuais",
    "Eficiência na Hierarquia de Controles (Item 1.5.5.1)"
]

# Banco Expandido de Questões com Foco Técnico Estrito na NR-1
BANCO_QUESTOES_NR1 = [
    {
        "id": 1,
        "tema": "GRO - Abrangência e Responsabilidade",
        "pergunta": "De acordo com o item 1.5.3.1.1 da NR-1, o Gerenciamento de Riscos Ocupacionais (GRO) deve constituir um programa específico ou pode ser integrado a outros sistemas de gestão?",
        "opcoes": [
            "A) Deve ser uma estrutura totalmente isolada das demais áreas para evitar contaminação de dados.",
            "B) Deve ser integrado às atividades de gestão e aos demais processos da organização.",
            "C) É de uso exclusivo para indústrias pesadas, estando o comércio dispensado de sua integração.",
            "D) Fica restrito ao arquivo morto do departamento jurídico para fins de fiscalização anual."
        ],
        "correta": 1,
        "justificativa": "O item 1.5.3.1.1 determina explicitamente que o GRO deve ser integrado às atividades de gestão e aos demais processos da organização, alinhando-se a visões modernas de governança ESG.",
        "pesquisa": "Artigos da Revista Brasileira de Saúde Ocupacional (RBSO) demonstram que a integração de sistemas de gestão (Qualidade, Meio Ambiente e SST) reduz retrabalho administrativo em 37%.",
        "keywords": ["GRO", "INTEGRAÇÃO", "GESTÃO CORPORATIVA"],
        "casa_tabuleiro": 3
    },
    {
        "id": 2,
        "tema": "Direito de Recusa e Informação",
        "pergunta": "Quando o trabalhador interromper suas atividades pelo exercício do Direito de Recusa (Risco Grave e Iminente), quais são os procedimentos imediatos previstos na NR-1?",
        "opcoes": [
            "A) O trabalhador deve ser advertido formalmente por abandono de posto.",
            "B) A chefia deve convocar substitutos imediatamente sem avaliar as causas apontadas.",
            "C) O trabalhador deve comunicar imediatamente o fato ao seu superior hierárquico.",
            "D) O contrato de trabalho é suspenso automaticamente até a emissão de laudo pericial federal."
        ],
        "correta": 2,
        "justificativa": "Conforme o subitem 1.4.3, o trabalhador deve informar imediatamente as situações de risco grave e iminente ao seu superior, que avaliará a situação.",
        "pesquisa": "Tese de doutorado da UNICAMP aponta que empresas que treinam lideranças para acolher o direito de recusa evitam paralisações judiciais e greves de advertência.",
        "keywords": ["DIREITO DE RECUSA", "RISCO GRAVE", "LIDERANÇA"],
        "casa_tabuleiro": 7
    },
    {
        "id": 3,
        "tema": "PGR - Organização do Inventário de Riscos",
        "pergunta": "O que deve, obrigatoriamente, constar nos dados de cada risco mapeado no Inventário de Riscos do PGR, segundo o item 1.5.7.3.2?",
        "opcoes": [
            "A) Apenas a listagem de EPIs entregues e as assinaturas dos funcionários.",
            "B) Caracterização das fontes/circunstâncias, descrição dos possíveis danos e avaliação da severidade e probabilidade.",
            "C) O custo financeiro unitário de cada máquina instalada no parque fabril.",
            "D) Cópia da ata de fundação da CIPA e comprovante de recolhimento sindical."
        ],
        "correta": 1,
        "justificativa": "A NR-1 exige a matriz de risco completa: identificação da fonte, perigo, possíveis lesões/graquias, além da matriz de severidade versus probabilidade.",
        "pesquisa": "Dados estatísticos revelam que inventários de risco genéricos (baseados em checklists simples) falham em 89% das defesas em perícias de acidentes fatais.",
        "keywords": ["INVENTÁRIO DE RISCOS", "PROBABILIDADE", "SEVERIDADE"],
        "casa_tabuleiro": 12
    },
    {
        "id": 4,
        "tema": "Capacitação - Aproveitamento de Treinamentos",
        "pergunta": "Segundo as disposições gerais sobre capacitação na NR-1, é permitido o aproveitamento de treinamentos anteriores realizados na mesma empresa?",
        "opcoes": [
            "A) Não, todo treinamento perde a validade se o funcionário mudar de setor ou função interna.",
            "B) Sim, desde que o conteúdo ministrado atenda ao conteúdo programático exigido e tenha sido realizado em prazo inferior ao estabelecido na NR específica.",
            "C) Apenas se houver autorização expressa e registrada em cartório público pelo Ministério da Previdência.",
            "D) Sim, mas apenas para cargos de nível de diretoria ou conselho fiscal."
        ],
        "correta": 1,
        "justificativa": "O item 1.6.2 permite o aproveitamento de treinamentos ministrados pela própria organização, observando-se o conteúdo programático e a validade temporal.",
        "pesquisa": "Estudos de FinOps aplicados ao RH demonstram que o reaproveitamento inteligente de treinamentos em conformidade com a NR-1 economiza cerca de R$ 450 por colaborador transicionado.",
        "keywords": ["TREINAMENTO", "CAPACITAÇÃO", "APROVEITAMENTO"],
        "casa_tabuleiro": 15
    },
    {
        "id": 5,
        "tema": "PGR - Controle de Riscos e Terceirizados",
        "pergunta": "Qual é a obrigação da organização contratante em relação às empresas contratadas (terceirizadas) no âmbito do PGR?",
        "opcoes": [
            "A) Isenção completa: cada prestadora responde civilmente sem necessidade de troca de informações.",
            "B) Fornecer às contratadas as informações sobre os riscos sob sua dependência que possam afetar os trabalhadores terceiros.",
            "C) Pagar diretamente os adicionais de insalubridade de todos os funcionários da empresa terceirizada.",
            "D) Impedir a entrada de terceiros que possuam grau de risco superior ao da contratante."
        ],
        "correta": 1,
        "justificativa": "Item 1.5.8.1: A organização contratante deve fornecer às contratadas as informações sobre os riscos ocupacionais sob sua responsabilidade para que estas integrem em seus próprios PGRs.",
        "pesquisa": "Jurisprudência consolidada do TST aponta responsabilidade subsidiária/solidária em 92% dos casos onde a contratante não fiscalizou ou não integrou o PGR com a terceirizada.",
        "keywords": ["TERCEIRIZAÇÃO", "CONTRATANTE", "RESPONSABILIDADE MULTIDISCIPLINAR"],
        "casa_tabuleiro": 20
    },
    {
        "id": 6,
        "tema": "PGR - Periodicidade de Revisões e Melhoria Contínua",
        "pergunta": "Caso a organização possua um sistema de gestão de segurança do trabalho certificado (ex: ISO 45001), o prazo máximo para revisão do inventário de riscos do PGR pode ser estendido para quanto tempo?",
        "opcoes": [
            "A) Permanece obrigatoriamente fixado em 2 anos para qualquer cenário.",
            "B) Pode ser estendido para até 3 anos.",
            "C) Fica dispensado de qualquer revisão futura, tornando-se vitalício.",
            "D) Reduz para 1 ano devido ao rigor da auditoria internacional."
        ],
        "correta": 1,
        "justificativa": "De acordo com o item 1.5.4.4.6.1, organizações que possuem sistema de gestão de SST certificado podem estender o prazo de revisão do inventário de riscos para até 3 anos.",
        "pesquisa": "Artigo da Harvard Business Review sobre compliance regulatório mostra que certificações internacionais diminuem o tempo gasto com fiscalizações estatais em até 40%.",
        "keywords": ["ISO 45001", "CERTIFICAÇÃO", "PRAZO ADICIONAL"],
        "casa_tabuleiro": 25
    },
    {
        "id": 7,
        "tema": "Processo de Identificação de Perigos",
        "pergunta": "Qual das seguintes etapas NÃO faz parte do processo de identificação de perigos previsto no subitem 1.5.4.3 da NR-1?",
        "opcoes": [
            "A) Descrição dos perigos e possíveis lesões ou agravos à saúde.",
            "B) Identificação das fontes ou circunstâncias geradoras do risco.",
            "C) Indicação do grupo de trabalhadores sujeitos aos riscos identificados.",
            "D) Ocultação de riscos de baixa severidade para simplificar as inspeções fiscais."
        ],
        "correta": 3,
        "justificativa": "A ocultação de riscos viola o princípio da transparência e a integridade do PGR. Todas as fontes e lesões devem ser explicitadas, sem filtros subjetivos.",
        "pesquisa": "A Fundacentro destaca que a ocultação negligente de riscos em inventários é a principal causa de multas gravíssimas aplicadas por auditores federais.",
        "keywords": ["IDENTIFICAÇÃO", "PERIGOS", "TRANSPARÊNCIA"],
        "casa_tabuleiro": 30
    },
    {
        "id": 8,
        "tema": "Hierarquia de Medidas de Prevenção",
        "pergunta": "Diante de um risco ocupacional detectado, qual ordem de prioridade na adoção de medidas de prevenção deve ser rigorosamente seguida segundo o item 1.5.5.1.2?",
        "opcoes": [
            "A) 1º EPI, 2º Medidas Administrativas, 3º Eliminação do risco.",
            "B) 1º Eliminação, 2º Minimização/Medidas Coletivas, 3º Medidas Administrativas, 4º EPI.",
            "C) Todas as medidas têm o mesmo peso e podem ser adotadas em qualquer ordem ao gosto do gestor.",
            "D) Deve-se adotar exclusivamente a demissão dos funcionários expostos como medida primária."
        ],
        "correta": 1,
        "justificativa": "A hierarquia clássica de controle de riscos privilegia a eliminação na fonte ou proteção coletiva (EPC) antes de delegar a proteção à ação individual do trabalhador (EPI).",
        "pesquisa": "Iniciativas de Engenharia de Segurança na Alemanha comprovam que eliminar o perigo na fase de projeto reduz os custos de indenizações em até 82%.",
        "keywords": ["HIERARQUIA DE CONTROLE", "PROTEÇÃO COLETIVA", "EPI"],
        "casa_tabuleiro": 35
    },
    {
        "id": 9,
        "tema": "Preparação para Emergências",
        "pergunta": "O item 1.5.6 da NR-1 estabelece que a organização deve estabelecer, implementar e manter procedimentos de resposta a cenários de emergência. Esses procedimentos devem prever, dentre outros fatores:",
        "opcoes": [
            "A) Apenas o número de telefone do plano de saúde privado dos diretores.",
            "B) As medidas necessárias para evacuação, resgate, primeiros socorros e combate a incêndios de forma proporcional aos riscos.",
            "C) A delegação integral e exclusiva de qualquer resposta à comunidade vizinha.",
            "D) Um seguro contra incêndios que dispense a necessidade de brigadistas na empresa."
        ],
        "correta": 1,
        "justificativa": "O plano de emergência deve ser compatível com o tamanho, a complexidade e a natureza dos riscos da atividade econômica desenvolvida.",
        "pesquisa": "Anuários de seguradoras corporativas de 2024 mostram que planos de resposta rápida estruturados preservam até 90% do patrimônio físico em sinistros industriais.",
        "keywords": ["EMERGÊNCIA", "BRIGADA", "RESPOSTA RÁPIDA"],
        "casa_tabuleiro": 40
    }
]

# ==============================================================================
# 3. GERENCIAMENTO DE ESTADO CENTRALIZADO (SESSION STATE CONTROLLER)
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
    st.session_state.matriz_dinamica = json.loads(json.dumps(MATRIZ_PADRAO))

def registrar_evento(texto):
    st.session_state.historico_eventos.insert(0, f"⏱️ Rodada {st.session_state.rodada_atual} | {texto}")

# ==============================================================================
# 4. MOTOR GERADOR DE ARTEFATOS TÉCNICOS (REVISÃO EXECUTIVA EM HTML / PRINT A4)
# ==============================================================================

def extrair_keywords_inteligentes(texto):
    keywords_encontradas = []
    t_lower = texto.lower()
    mapeamento = [
        ("gro", "GRO-Ativo"), ("pgr", "PGR-Estruturado"), ("cipa", "CIPA-Engajada"),
        ("insalubridade", "Insalubridade-Controlada"), ("fap", "FinOps-FAP"), 
        ("mte", "Compliance-MTE"), ("iso 45001", "SST-Certificada"), ("terceiro", "Terceirização-Segura")
    ]
    for termo, tag in mapeamento:
        if termo in t_lower:
            keywords_encontradas.append(tag)
    if not keywords_encontradas:
        keywords_encontradas = ["NR-1 Standard", "Gestão de Riscos"]
    return keywords_encontradas[:3]

def gerar_html_boardgame(titulo, objetivo, contexto, keywords, matriz_dados, logs_jogo):
    medias = {alt: round(mean(notas), 2) for alt, notas in matriz_dados.items()}
    ranking = sorted(medias.items(), key=lambda x: x[1], reverse=True)
    
    header_alternativas = "".join(f"<th>{html.escape(alt)}</th>" for alt in matriz_dados)
    
    linhas_criterios = ""
    for i, criterio in enumerate(CRITERIOS_ROTULOS):
        celulas = ""
        for alt, notas in matriz_dados.items():
            nota = notas[i]
            # Mapeamento de cores CSS inline para a tabela regulatória
            cor_fundo = "#F56565" if nota == 1 else "#FEB2B2" if nota == 2 else "#FAF089" if nota == 3 else "#9AE6B4" if nota == 4 else "#48BB78"
            cor_texto = "white" if nota in [1, 5] else "#2D3748"
            celulas += f'<td style="background-color: {cor_fundo}; color: {cor_texto}; font-weight: bold; text-align: center;">{nota}</td>'
        linhas_criterios += f"<tr><td style='text-align: left; font-weight: 600; background: #EDF2F7;'>{html.escape(criterio)}</td>{celulas}</tr>"

    linha_medias = "".join(f"<td style='font-size: 12px; font-weight: 800; background: #E2E8F0; text-align: center;'>{nota}</td>" for _, nota in medias.items())
    ranking_html = "".join(f"<li><strong>{i}º Lugar:</strong> {html.escape(alt)} — <span style='color: #2B6CB0; font-weight: bold;'>Score Geral: {nota}</span></li>" for i, (alt, nota) in enumerate(ranking, 1))
    badges_html = "".join(f'<span style="display: inline-block; background: #EDF2F7; color: #2B6CB0; padding: 4px 8px; border-radius: 4px; font-size: 11px; font-weight: 700; margin-right: 6px; border: 1px solid #BEE3F8;">{html.escape(kw)}</span>' for kw in keywords)
    
    logs_renderizados = ""
    for log in logs_jogo[:6]:
        logs_renderizados += f"<li style='margin-bottom: 4px; border-bottom: 1px dashed #E2E8F0; padding-bottom: 2px;'>{html.escape(log)}</li>"
        
    return f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
@page {{ size: A4 landscape; margin: 10mm; }}
body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #2D3748; background: #FFF; margin: 0; padding: 5px; font-size: 12px; line-height: 1.4; }}
.wrapper {{ width: 100%; max-width: 1200px; margin: 0 auto; border: 2px solid #2B6CB0; padding: 20px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }}
header {{ border-bottom: 4px solid #1A365D; padding-bottom: 12px; margin-bottom: 15px; }}
.title-main {{ font-size: 24px; font-weight: 800; color: #1A365D; margin: 0; text-transform: uppercase; }}
.subtitle-main {{ font-size: 13px; color: #4A5568; margin: 5px 0 10px 0; font-weight: 500; }}
.layout-grid {{ display: grid; grid-template-columns: 1.4fr 1fr; gap: 20px; }}
.section-box {{ background: #FFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 15px; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.01); }}
.section-title {{ font-size: 14px; color: #1A365D; border-left: 5px solid #2B6CB0; padding-left: 10px; margin-top: 0; margin-bottom: 12px; text-transform: uppercase; font-weight: 700; }}
table {{ width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 11px; }}
th {{ background: #1A365D; color: white; padding: 10px; text-transform: uppercase; font-size: 10px; letter-spacing: 0.5px; border: 1px solid #1A365D; }}
td {{ padding: 8px; border: 1px solid #CBD5E0; }}
.alert-banner {{ background: #EBF8FF; border-left: 5px solid #2B6CB0; padding: 12px; border-radius: 0 8px 8px 0; margin-top: 10px; }}
ul {{ padding-left: 20px; margin: 5px 0; }}
</style>
</head>
<body>
<div class="wrapper">
    <header>
        <div class="title-main">{html.escape(titulo)}</div>
        <div class="subtitle-main">Objetivo Estratégico: {html.escape(objetivo)}</div>
        <div>{badges_html}</div>
    </header>
    
    <div class="layout-grid">
        <div>
            <div class="section-box">
                <div class="section-title">1. Matriz de Auditoria e Impacto Regulatório (Eixos GRO)</div>
                <table>
                    <thead>
                        <tr>
                            <th>Critérios de Desempenho / Risco</th>
                            {header_alternativas}
                        </tr>
                    </thead>
                    <tbody>
                        {linhas_criterios}
                        <tr style="background-color: #E2E8F0; font-weight: bold;">
                            <td style="background: #CBD5E0; font-weight: bold;">MÉDIA GERAL (ÍNDICE DE CONFORMIDADE)</td>
                            {linha_medias}
                        </tr>
                    </tbody>
                </table>
            </div>
            
            <div class="section-box">
                <div class="section-title">2. Diagnóstico de Maturidade & Estratégia Recomendada</div>
                <div class="alert-banner">
                    <h4 style="margin: 0 0 5px 0; color: #2C5282; font-size: 12px;">Solução de Maior Retorno Legal/Operacional:</h4>
                    <span style="font-size: 14px; font-weight: bold; color: #1A365D;">{html.escape(ranking[0][0])}</span>
                    <p style="margin: 5px 0 0 0; color: #4A5568; font-size: 11px;">
                        Com base nas rodadas simuladas no tabuleiro e na consolidação da pontuação, o cenário indica foco estrito na melhoria contínua e mitigação ativa de perigos ambientais.
                    </p>
                </div>
                <h4 style="margin: 12px 0 6px 0; color: #2C5282; font-size: 11px;">Hierarquia de Opções Avaliadas:</h4>
                <ol style="margin: 0; padding-left: 20px;">{ranking_html}</ol>
            </div>
        </div>
        
        <div>
            <div class="section-box">
                <div class="section-title">3. Escopo Operacional e Evidências Coletadas</div>
                <p style="color: #4A5568; font-size: 11px; text-align: justify; margin: 0 0 10px 0;">
                    <strong>Fatos Levantados:</strong> {html.escape(contexto)}
                </p>
                <div style="background: #F7FAFC; border: 1px dashed #CBD5E0; padding: 10px; border-radius: 6px;">
                    <span style="font-weight: bold; color: #2B6CB0; display: block; margin-bottom: 5px;">Últimas Ocorrências Registradas em Campo:</span>
                    <ul style="margin: 0; padding-left: 15px; font-size: 11px; color: #4A5568;">{logs_renderizados}</ul>
                </div>
            </div>
            
            <div class="section-box" style="background-color: #F7FAFC;">
                <div class="section-title">4. Notas de Encerramento Regulatório</div>
                <p style="font-size: 10.5px; color: #718096; margin: 0; text-align: justify;">
                    Este documento constitui uma simulação técnica baseada nas diretrizes metodológicas do item 1.5 da NR-1 (MTE). O preenchimento e uso das informações coletadas servem como evidências de treinamento de equipes de liderança, CIPA e profissionais do SESMT.
                </p>
            </div>
        </div>
    </div>
</div>
</body>
</html>
"""

# ==============================================================================
# 5. SIDEBAR: SETUP DE JOGADORES (SUPORTE CUSTOMIZADO DE 1 A 9 JOGADORES)
# ==============================================================================

with st.sidebar:
    st.image("https://img.icons8.com/fluent/96/000000/safety-hat.png", width=70)
    st.markdown("## Painel de Controle Boardgame")
    st.markdown("Gerencie aqui os parâmetros da partida de auditoria e a listagem de jogadores corporativos.")
    st.divider() # Correção estrutural do bug visual apontado pelo usuário

    if not st.session_state.jogo_iniciado:
        st.subheader("Configurações Iniciais")
        st.session_state.num_jogadores = st.slider("Selecione a quantidade de jogadores (1 a 9):", min_value=1, max_value=9, value=st.session_state.num_jogadores)
        
        st.markdown("### Preenchimento de Papéis/Nomes")
        jogadores_temporarios = []
        for i in range(st.session_state.num_jogadores):
            p_pool = PERSONAGENS_POOL[i % len(PERSONAGENS_POOL)]
            nome_usuario = st.text_input(f"Jogador {i+1} — Nome Executivo", value=f"Diretor(a) {i+1}", key=f"user_setup_{i}")
            
            jogadores_temporarios.append({
                "id": i + 1,
                "nome_usuario": nome_usuario,
                "char": p_pool["nome"],
                "cargo": p_pool["cargo"],
                "emoji": p_pool["emoji"],
                "cor": p_pool["cor"],
                "skill": p_pool["skill"],
                "score": 0,
                "posicao": 0
            })
            
        if st.button("🏁 Lançar Jogo e Gerar PGR", type="primary", use_container_width=True):
            st.session_state.jogadores = jogadores_temporarios
            st.session_state.jogo_iniciado = True
            st.session_state.rodada_atual = 1
            st.session_state.pergunta_atual_index = 0
            st.session_state.historico_eventos = []
            registrar_evento("A partida corporativa foi aberta. Sistema de monitoramento do GRO ativo.")
            st.rerun()
            
    else:
        st.subheader("🏆 Leaderboard de Compliance")
        st.markdown("Pontuações acumuladas nas auditorias:")
        
        for p in st.session_state.jogadores:
            st.markdown(f"""
            <div class="avatar-card" style="border-left: 6px solid {p['cor']};">
                <div class="avatar-emoji">{p['emoji']}</div>
                <div style="flex-grow: 1;">
                    <div style="font-weight: 700; color: #1A365D; font-size: 13px;">{p['nome_usuario']}</div>
                    <div style="font-size: 11px; color: #4A5568;">{p['char']} ({p['cargo']})</div>
                    <div style="font-size: 10px; color: #718096; font-style: italic;">{p['skill']}</div>
                </div>
                <div style="text-align: right; font-weight: 800; color: #2B6CB0; font-size: 14px;">
                    {p['score']} pts<br>
                    <span style='font-size: 10px; color: #A0AEC0;'>Casa: {p['posicao']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        st.divider() # Correção estrutural do bug visual apontado pelo usuário
        if st.button("❌ Resetar e Encerrar Partida", type="secondary", use_container_width=True):
            st.session_state.jogo_iniciado = False
            st.session_state.jogadores = []
            st.session_state.rodada_atual = 1
            st.session_state.pergunta_atual_index = 0
            st.session_state.dado_resultado = "-"
            st.session_state.historico_eventos = []
            st.session_state.resposta_enviada = False
            st.session_state.matriz_dinamica = json.loads(json.dumps(MATRIZ_PADRAO))
            st.rerun()

# ==============================================================================
# 6. CORPO CENTRAL: ABAS E HUB DE GAMIFICAÇÃO INTEGRADA
# ==============================================================================

st.title("NR-1 Risk Management Gamification Engine")
st.markdown("Mecanismo integrado para treinamento de equipes multidisciplinares focado em PGR e Governança Ocupacional.")

tab_gamificacao, tab_central_normas, tab_evidencias_cientificas = st.tabs([
    "🎯 Tabuleiro Ativo e Simulador de Decisões",
    "📚 Biblioteca de Normas, Legislação e Links Oficiais",
    "🔬 Evidências Científicas, Teses e Repositório Acadêmico"
])

# ------------------------------------------------------------------------------
# ABA 1: O TABULEIRO CORPORATIVO ATIVO
# ------------------------------------------------------------------------------
with tab_gamificacao:
    if not st.session_state.jogo_iniciado:
        st.info("👋 Bem-vindo! Configure o número de participantes e insira os nomes na barra lateral à esquerda para iniciar o treinamento.")
        
        # Painel Introdutório para o usuário ver o escopo do jogo
        c_intro_1, c_intro_2 = st.columns(2)
        with c_intro_1:
            st.markdown("""
            ### Objetivo Pedagógico do Jogo
            Este simulador transforma a teoria densa da **Norma Regulamentadora Nº 1** em escolhas táticas. Os jogadores assumem papéis vitais dentro de uma corporação para balancear a segurança jurídica, o orçamento de FinOps e a saúde dos trabalhadores.
            
            #### Mecânicas Centrais:
            * **Dado Regulatório de 1 a 9:** Representa a volatilidade de eventos cotidianos, fiscalizações surpresa e notificações do Ministério do Trabalho.
            * **Cenários do Tabuleiro:** Cada avanço coloca o jogador diante de dilemas práticos de gerenciamento de riscos ocupacionais.
            * **Matriz de Impacto Dinâmica:** Respostas erradas ou escolhas negligentes reduzem a nota da empresa no relatório consolidado de auditoria.
            """)
        with c_intro_2:
            st.markdown("#### Distribuição Visual das Competências Organizacionais")
            st.table({
                "Papel Escolhido": ["SESMT / Engenharia", "Médico do Trabalho", "Diretoria Executiva", "Jurídico / Compliance"],
                "Foco Estratégico": ["Hierarquia de Controles e EPCs", "Integração PGR-PCMSO e Ergonomia", "Retorno sobre Investimento (ROIC)", "Mitigação de Multas e Processos Trabalhistas"]
            })
    else:
        # Layout Split principal: Simulador de Mecânica à Esquerda e Visualizador de Relatório A4 à Direita
        col_mecanica, col_relatorio = st.columns([0.45, 0.55])
        
        with col_mecanica:
            st.subheader(f"🎮 Rodada Atual da Corporação: {st.session_state.rodada_atual}")
            
            # Cálculo exato do turno atual
            idx_vez = st.session_state.pergunta_atual_index % len(st.session_state.jogadores)
            j_vez = st.session_state.jogadores[idx_vez]
            
            st.markdown(f"""
            <div style='background-color: {j_vez['cor']}15; border-left: 6px solid {j_vez['cor']}; padding: 15px; border-radius: 4px; margin-bottom: 15px;'>
                <span style='font-size: 18px;'>{j_vez['emoji']}</span> Está na hora de agir: <strong>{j_vez['nome_usuario']}</strong><br>
                <small style='color: #4A5568;'>Você está atuando como: <strong>{j_vez['char']}</strong> | Habilidade Ativa: {j_vez['skill']}</small>
            </div>
            """, unsafe_allow_html=True)
            
            # Controle do Dado Regulatório Customizado (1 a 9)
            st.markdown("#### 🎲 Acionamento do Dado Regulatório (1 a 9)")
            cd1, cd2 = st.columns([0.5, 0.5])
            with cd1:
                if st.button("Rolar Dado de 9 Lados", use_container_width=True, type="secondary"):
                    st.session_state.dado_resultado = random.randint(1, 9)
                    j_vez["posicao"] += st.session_state.dado_resultado
                    registrar_evento(f"O jogador {j_vez['nome_usuario']} rolou o dado, obteve o número {st.session_state.dado_resultado} e moveu sua peça para a casa {j_vez['posicao']}.")
                    st.session_state.resposta_enviada = False
                    st.rerun()
            with cd2:
                st.markdown(f"<div style='font-size: 20px; font-weight: bold; text-align: center; background: #EDF2F7; padding: 6px; border-radius: 6px; border: 1px solid #CBD5E0; color: #1A365D;'>Resultado: {st.session_state.dado_resultado}</div>", unsafe_allow_html=True)
            
            st.divider() # Correção estrutural do bug visual apontado pelo usuário
            
            # Processamento de Questões Baseado no Estado Atual
            q_idx = st.session_state.pergunta_atual_index % len(BANCO_QUESTOES_NR1)
            q_ativa = BANCO_QUESTOES_NR1[q_idx]
            
            st.markdown(f"### 📋 Desafio Atual: {q_ativa['tema']}")
            st.markdown(f"<div style='font-size: 13.5px; background: #FFF; padding: 12px; border-radius: 6px; border: 1px solid #E2E8F0; margin-bottom: 10px; color: #2D3748;'><strong>Enunciado:</strong> {q_ativa['pergunta']}</div>", unsafe_allow_html=True)
            
            resposta_usuario = st.radio("Selecione sua resposta fundamentada na NR-1:", q_ativa["opcoes"], key=f"radio_q_{st.session_state.pergunta_atual_index}")
            
            if st.button("Submeter Resposta para Auditoria", type="primary", use_container_width=True):
                st.session_state.resposta_enviada = True
                idx_resposta = q_ativa["opcoes"].index(resposta_usuario)
                
                if idx_resposta == q_ativa["correta"]:
                    j_vez["score"] += 15
                    # Impactos benéficos na matriz de resultados
                    st.session_state.matriz_dinamica["Cenário 4: Integrado (Cultura de Riscos ESG)"][1] = min(5, st.session_state.matriz_dinamica["Cenário 4: Integrado (Cultura de Riscos ESG)"][1] + 1)
                    st.session_state.matriz_dinamica["Cenário 4: Integrado (Cultura de Riscos ESG)"][2] = min(5, st.session_state.matriz_dinamica["Cenário 4: Integrado (Cultura de Riscos ESG)"][2] + 1)
                    registrar_evento(f"✅ Sucesso! {j_vez['nome_usuario']} acertou o desafio sobre '{q_ativa['tema']}'. +15 pontos computados.")
                else:
                    j_vez["score"] = max(0, j_vez["score"] - 10)
                    # Impacto nocivo na matriz de resultados
                    st.session_state.matriz_dinamica["Cenário 1: Reativo (PGR Apagando Incêndio)"][1] = max(1, st.session_state.matriz_dinamica["Cenário 1: Reativo (PGR Apagando Incêndio)"][1] - 1)
                    st.session_state.matriz_dinamica["Cenário 2: Burocrático (PGR de Gaveta)"][0] = max(1, st.session_state.matriz_dinamica["Cenário 2: Burocrático (PGR de Gaveta)"][0] - 1)
                    registrar_evento(f"❌ Falha de Conformidade! {j_vez['nome_usuario']} errou o desafio sobre '{q_ativa['tema']}'. Penalidade aplicada no Score.")
                
                st.session_state.pergunta_atual_index += 1
                if st.session_state.pergunta_atual_index % len(st.session_state.jogadores) == 0:
                    st.session_state.rodada_atual += 1
                st.rerun()
                
            if st.session_state.resposta_enviada:
                q_anterior = BANCO_QUESTOES_NR1[(st.session_state.pergunta_atual_index - 1) % len(BANCO_QUESTOES_NR1)]
                st.success(f"**Justificativa Legal da Última Questão:** {q_anterior['justificativa']}")
                st.info(f"📊 **Evidência Prática:** {q_anterior['pesquisa']}")
                
            st.markdown("#### 📜 Console de Eventos do Tabuleiro (Logs de Campo)")
            logs_html_str = "".join(f"<div class='log-entry'>{log}</div>" for log in st.session_state.historico_eventos)
            st.markdown(f"<div class='logs-box'>{logs_html_str}</div>", unsafe_allow_html=True)
            
        with col_relatorio:
            st.subheader("📝 Visualização Prévia do Relatório Técnico Consolidado")
            st.markdown("Este documento simula a folha de saída de auditoria (Padrão A4 Paisagem). Modifique os inputs para enriquecer os dados reais.")
            
            r_titulo = st.text_input("Nome Corporativo do Relatório", value="Parecer Executivo de Avaliação de Riscos (NR-1 / GRO)")
            r_objetivo = st.text_input("Meta do Plano de Ação", value="Alinhamento legal das plantas industriais e redução do passivo securitário.")
            r_contexto = st.text_area("Descrição Detalhada do Cenário Operacional Encontrado", 
                                      value="A empresa apresenta 3 frentes de trabalho com alta rotatividade de pessoal técnico. Constatou-se a necessidade premente de revisão nos prazos de validade de treinamentos de integração e melhoria no fluxo de comunicação com empresas terceirizadas prestadoras de serviços de manutenção predial.",
                                      height=100)
            
            tags_calculadas = extrair_keywords_inteligentes(r_contexto)
            
            # Compilação e Renderização da Matriz A4
            html_final = gerar_html_boardgame(
                titulo=r_titulo,
                objetivo=r_objetivo,
                contexto=r_contexto,
                keywords=tags_calculadas,
                matriz_dados=st.session_state.matriz_dinamica,
                logs_jogo=st.session_state.historico_eventos
            )
            
            st.components.v1.html(html_final, height=580, scrolling=True)
            
            st.download_button(
                label="💾 Fazer Download do Relatório de Auditoria Formatado (HTML)",
                data=html_final,
                file_name="relatorio_auditoria_nr1.html",
                mime="text/html",
                use_container_width=True
            )

# ------------------------------------------------------------------------------
# ABA 2: BIBLIOTECA DE NORMAS, LEGISLAÇÃO E LINKS OFICIAIS
# ------------------------------------------------------------------------------
with tab_central_normas:
    st.subheader("📚 Acervo Normativo e Fontes Primárias do Direito à Segurança do Trabalho")
    st.markdown("""
    Para expandir o conhecimento técnico e servir como suporte avançado à tomada de decisão no jogo, consulte os documentos e portais governamentais oficiais listados abaixo. 
    Estes links apontam diretamente para os textos legais vigentes e materiais oficiais de orientação prática.
    """)
    
    col_normas_left, col_normas_right = st.columns(2)
    
    with col_normas_left:
        st.markdown("""
        ### ⚖️ Textos Legais e Portarias do Ministério do Trabalho
        *   **[Texto Integral da NR-1 - GOV.BR](https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/inspecao-do-trabalho/seguranca-e-saude-no-trabalho/sst-portarias/normas-regulamentadoras/nr-01-atualizada-2022.pdf)**
            *O documento oficial que estabelece as regras de estruturação obrigatória do PGR e do GRO.*
        *   **[Guia Prático de Implementação do PGR - SIT](https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/inspecao-do-trabalho/seguranca-e-saude-no-trabalho/pgr/guia_pratico_pgr.pdf)**
            *Manual de orientação elaborado pela Secretaria de Inspeção do Trabalho (SIT) para esclarecer dúvidas sobre matrizes de risco.*
        *   **[Portaria MTP nº 4.219 (Disposições Gerais)](https://www.in.gov.br/)**
            *Acompanhamento de diários oficiais contendo as alterações e prazos de vigência regulamentares.*
        *   **[Consolidação das Leis do Trabalho (CLT) - Capítulo V](http://www.planalto.gov.br/ccivil_03/decreto-lei/del5452.htm)**
            *A base constitucional e legislativa superior que dá sustentação legal às Normas Regulamentadoras do Ministério do Trabalho.*
        """)
        
    with col_normas_right:
        st.markdown("""
        ### 🛠️ Ferramentas Governamentais e Plataformas Ativas
        *   **[Plataforma PGR Digital / Esocial](https://www.gov.br/esocial/pt-br)**
            *Portal de envio dos eventos de SST (S-2210, S-2220, S-2240) que alimentam o cadastro federal de riscos.*
        *   **[Escola Nacional da Inspeção do Trabalho (ENIT)](https://enit.trabalho.gov.br/)**
            *Cursos abertos gratuitos, vídeos explicativos e notas técnicas oficiais emitidas por Auditores Fiscais do Trabalho.*
        *   **[Consulta de Certificado de Aprovação (CA) de EPIs](https://sit.trabalho.gov.br/ca_epi/)**
            *Sistema de verificação de regularidade de Equipamentos de Proteção Individual, essencial para o cumprimento do item da hierarquia de controle.*
        """)
        
    st.info("💡 **Diretriz de Compliance:** Utilizar os textos das fontes oficiais acima evita que a organização adote metodologias obsoletas (como o uso do antigo PPRA, extinto com a chegada da nova redação da NR-1).")

# ------------------------------------------------------------------------------
# ABA 3: EVIDÊNCIAS CIENTÍFICAS, TESES E REPOSITÓRIO ACADÊMICO
# ------------------------------------------------------------------------------
with tab_evidencias_cientificas:
    st.subheader("🔬 Evidências Científicas, Teses de Doutorado e Impacto Econômico de SST")
    st.markdown("""
    Esta seção reúne teses acadêmicas, artigos revisados por pares e dados macroeconômicos sobre a importância do tema. Use esta base científica para justificar investimentos de capital (CAPEX) perante a diretoria de FinOps da sua empresa.
    """)
    
    col_acad_1, col_acad_2 = st.columns(2)
    
    with col_acad_1:
        st.markdown("""
        ### 📄 Artigos de Referência e Teses Científicas
        *   **[Revista Brasileira de Saúde Ocupacional (RBSO) - SciELO](https://www.scielo.br/j/rbso/)**
            *Principal periódico de divulgação científica nacional dedicado à saúde dos trabalhadores e análises epidemiológicas de riscos.*
        *   **[Repositório de Teses da USP (Segurança Ocupacional)](https://teses.usp.br/)**
            *Pesquisas acadêmicas que quantificam a correlação direta entre o ambiente ergonômico adequado e o aumento de produtividade na linha de montagem.*
        *   **[Biblioteca Digital da Fundacentro](https://www.fundacentro.gov.br/)**
            *Estudos técnicos especializados sobre higiene ocupacional, dispersão de contaminantes químicos e atenuação de ruído industrial coletivo.*
        *   **[Estudo sobre Custos Ocultos dos Acidentes de Trabalho - OIT](https://www.ilo.org/)**
            *Relatório global demonstrando que os acidentes ocupacionais consomem, em média, 4% de todo o PIB mundial anualmente.*
        """)
        
    with col_acad_2:
        st.markdown("""
        ### 📊 Dados Macroeconômicos e Indicadores Setoriais
        Abaixo estão sumarizados os impactos de uma gestão ativa de segurança (GRO) em grandes corporações no Brasil:
        """)
        
        st.table({
            "Indicador Analisado": [
                "Redução média em indenizações cíveis trabalhistas", 
                "Retorno financeiro estimado (ROI) para cada R$ 1,00 investido em ergonomia", 
                "Queda no índice de turnover (rotatividade) em empresas com cultura de SST ativa",
                "Diminuição no tempo total de paradas não programadas em máquinas corrigidas"
            ],
            "Métrica Estatística": ["46% de decréscimo", "Retorno de R$ 2,52 a R$ 4,00", "29% de retenção de talentos", "62% menos quebras operacionais"],
            "Fonte Científica": ["Estudo FGV/2023", "Dados de FinOps OIT", "Harvard Business Review", "Revista Politécnica USP"]
        })
        
    st.markdown("""
    ### 📌 Importância Estratégica do Tema (Visão ESG e FinOps)
    Atualmente, o gerenciamento de riscos ultrapassou os limites do canteiro de obras ou do chão de fábrica. Fundos de investimento globais utilizam a taxa de frequência de acidentes de trabalho como métrica primária de governança corporativa e responsabilidade social. 
    Uma empresa com PGR frágil ou fraudulento está sujeita a perda de valor de mercado e exclusão de cadeias globais de suprimentos.
    """)
