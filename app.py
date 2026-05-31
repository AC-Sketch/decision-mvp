import streamlit as st
import html
from statistics import mean
import re

st.set_page_config(
    page_title="Collective Decision Engine",
    layout="wide"
)

st.markdown("""
<style>
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 0rem;
    max-width: 1240px;
}

h1 {
    font-size: 2rem !important;
    margin-bottom: 0.6rem !important;
}

h2, h3 {
    margin-top: 0rem !important;
}

/* Controlled vertical spacing between components */
[data-testid="stVerticalBlock"] {
    gap: 0.6rem !important;
}

/* Fine tuning for file uploader alignment */
[data-testid="stFileUploader"] {
    margin-bottom: 0rem;
}

/* Prevents input containers from cutting off bottom padding */
[data-testid="stTextInput"] > div {
    padding-bottom: 2px;
}

[data-testid="stTextArea"] > div {
    padding-bottom: 2px;
}

iframe {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("Collective Decision Engine")

MATRIZ = {
    "Status Quo": [1, 1, 5, 5, 5],
    "100% Virtual": [5, 2, 1, 3, 2],
    "Hybrid Model": [4, 4, 4, 4, 3],
    "Merger / Shared": [4, 2, 4, 1, 1],
}

CRITERIOS = [
    "Economy",
    "Legal Risk",
    "Elderly Care",
    "Complexity",
    "Investment",
]

def extrair_palavras_chave(texto):
    """
    Semantically analyzes text to extract up to two conceptual keywords.
    Matches predefined context rules first, then falls back to a statistical frequency approach.
    """
    if not texto:
        return ""
    
    texto_lower = texto.lower()
    conceitos = []
    
    # Context Rules Mapping for Intelligent Concept Attachment
    regras_contexto = {
        "Finance": ["cost", "economy", "financial", "investment", "expense", "budget", "funds", "reduce", "pressure"],
        "Security": ["concierge", "guard", "surveillance", "safe", "risk", "legal", "breach", "camera", "access"],
        "Social": ["elderly", "residents", "human", "support", "care", "community", "resistance", "adaptation"],
        "Operation": ["complexity", "deployment", "virtual", "hybrid", "merger", "sharing", "transition", "governance", "operational"]
    }
    
    # Match conceptual adherence using smart rules
    for conceito, gatilhos in regras_contexto.items():
        if any(gatilho in texto_lower for gatilho in gatilhos):
            conceitos.append(conceito)
            if len(conceitos) == 2:
                break
                
    # Statistical fallback if explicit conceptual rules are not matched
    if len(conceitos) < 2:
        palavras = re.findall(r'\b[a-z]{4,}\b', texto_lower)
        stop_words = {"with", "from", "this", "that", "more", "everything", "where", "their", "focus", "would", "about"}
        filtradas = [p for p in palavras if p not in stop_words]
        
        contagem = {}
        for p in filtradas:
            contagem[p] = contagem.get(p, 0) + 1
            
        ordenadas = sorted(contagem.items(), key=lambda x: x[1], reverse=True)
        for p, _ in ordenadas:
            palavra_cap = p.capitalize()
            if palavra_cap not in conceitos:
                conceitos.append(palavra_cap)
            if len(conceitos) == 2:
                break

    if not conceitos:
        return ""
    return " • ".join(conceitos[:2])

def gerar_html(titulo, objetivo, contexto):
    medias = {alt: round(mean(notas), 2) for alt, notas in MATRIZ.items()}
    ranking = sorted(medias.items(), key=lambda x: x[1], reverse=True)
    melhor = ranking[0][0]

    header = "".join(f"<th>{html.escape(alt)}</th>" for alt in MATRIZ)

    linhas = ""
    for i, criterio in enumerate(CRITERIOS):
        cells = ""
        for alt, notas in MATRIZ.items():
            nota = notas[i]
            cells += f'<td class="score-{nota}">{nota}</td>'
        linhas += f"<tr><td>{html.escape(criterio)}</td>{cells}</tr>"

    medias_row = "".join(
        f"<td><strong>{nota}</strong></td>"
        for _, nota in medias.items()
    )

    ranking_html = "".join(
        f"<li><strong>{i}st:</strong> {html.escape(alt)} : {nota}</li>"
        for i, (alt, nota) in enumerate(ranking, 1)
    )

    # Dynamic contextual extraction for narrative blocks
    kw_diag = extrair_palavras_chave("Diagnosis: the analyzed scenario demands cost reduction without critical losses in security, support, and governance.")
    kw_b1 = extrair_palavras_chave("Focus: keep everything as it is. Preserves operational comfort, but maintains financial pressure.")
    kw_b2 = extrair_palavras_chave("Focus: radical economy. Reduces cost, but increases risks regarding adaptation and resistance.")
    kw_b3 = extrair_palavras_chave("Focus: balanced transition. Gradual implementation while partially preserving human support.")
    kw_contexto = extrair_palavras_chave(contexto[:1000])

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{html.escape(titulo)}</title>

<style>
@page {{
    size: A4 landscape;
    margin: 7mm;
}}

:root {{
    --primary: #2c3e50;
    --secondary: #18bc9c;
    --background: #f8f9fa;
    --border: #e9ecef;
    --excelente: #2ecc71;
    --bom: #a3e4d7;
    --moderado: #f9e79f;
    --critico: #f5b7b1;
    --pessimo: #e74c3c;
}}

* {{
    box-sizing: border-box;
}}

body {{
    font-family: Segoe UI, Tahoma, sans-serif;
    background: var(--background);
    color: #333;
    margin: 0;
    padding: 32px 6px 6px 6px;
    font-size: 10px;
}}

.container {{
    max-width: 1080px;
    margin: 0 auto;
}}

header {{
    text-align: center;
    border-bottom: 3px solid var(--primary);
    margin-bottom: 7px;
    padding-bottom: 5px;
}}

header h1 {{
    color: var(--primary);
    margin: 0;
    font-size: 20px;
}}

header p {{
    margin: 2px 0 0 0;
    color: #6c757d;
    font-size: 10px;
}}

.grid {{
    display: grid;
    grid-template-columns: 1.28fr 0.9fr;
    gap: 8px;
}}

.card {{
    background: #fff;
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 8px;
    margin-bottom: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.04);
}}

h2 {{
    color: var(--primary);
    font-size: 13px;
    margin: 0 0 5px 0;
    border-left: 5px solid var(--secondary);
    padding-left: 7px;
}}

h3 {{
    margin: 3px 0;
    color: #117a65;
    font-size: 12px;
}}

p {{
    margin: 3px 0;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    text-align: center;
}}

th, td {{
    border: 1px solid var(--border);
    padding: 5px;
    font-size: 9.2px;
}}

th {{
    background: var(--primary);
    color: white;
}}

td:first-child {{
    text-align: left;
    font-weight: bold;
    background: #f1f4f6;
    color: var(--primary);
}}

.score-5 {{ background: var(--excelente); color: white; font-weight: bold; }}
.score-4 {{ background: var(--bom); color: #196f3d; font-weight: bold; }}
.score-3 {{ background: var(--moderado); color: #7d6608; font-weight: bold; }}
.score-2 {{ background: var(--critico); color: #78281f; font-weight: bold; }}
.score-1 {{ background: var(--pessimo); color: white; font-weight: bold; }}

.tree-node {{
    background: #f1f4f6;
    border: 1px solid #d5dbdb;
    border-radius: 6px;
    padding: 7px;
    margin-bottom: 6px;
    position: relative;
}}

.branch {{
    background: white;
    border: 1px dashed #bdc3c7;
    border-radius: 6px;
    padding: 7px;
    margin-bottom: 6px;
    position: relative;
}}

.recommended {{
    border: 2px solid var(--secondary);
    background: #e8f8f5;
}}

.badge {{
    float: right;
    padding: 2px 5px;
    border-radius: 3px;
    font-size: 8px;
    font-weight: bold;
}}

.keywords-tag {{
    display: block;
    text-align: right;
    font-size: 7.5px;
    color: #8c969e;
    font-style: italic;
    margin-top: 4px;
    font-weight: normal;
}}

.success {{
    background: #a3e4d7;
    color: #196f3d;
}}

.danger {{
    background: #f5b7b1;
    color: #78281f;
}}

.conclusion {{
    background: #e8f8f5;
    border-left: 6px solid var(--secondary);
    padding: 8px;
    border-radius: 0 8px 8px 0;
}}

ol {{
    padding-left: 16px;
    margin: 4px 0;
}}

li {{
    margin-bottom: 3px;
}}

.contexto-container {{
    position: relative;
}}

.contexto {{
    max-height: 90px;
    overflow: hidden;
    font-size: 9.2px;
    line-height: 1.3;
    margin-bottom: 2px;
}}

@media print {{
    body {{
        background: white;
    }}

    .card {{
        break-inside: avoid;
    }}
}}
</style>
</head>

<body>
<div class="container">

<header>
    <h1>{html.escape(titulo)}</h1>
    <p>{html.escape(objetivo)}</p>
</header>

<div class="grid">

<div>
    <div class="card">
        <h2>1. Multi-Criteria Decision Matrix</h2>
        <p>Scores from 1 to 5 to compare proposed scenarios.</p>
        <table>
            <thead>
                <tr>
                    <th>Criteria</th>
                    {header}
                </tr>
            </thead>
            <tbody>
                {linhas}
                <tr>
                    <td><strong>Final Average</strong></td>
                    {medias_row}
                </tr>
            </tbody>
        </table>
    </div>

    <div class="card">
        <h2>2. Assessment and Ranking</h2>
        <div class="conclusion">
            <h3>Best suggested alternative: {html.escape(melhor)}</h3>
            <ol>
                {ranking_html}
            </ol>
            <p>
                The recommendation evaluates the equilibrium between economy, legal risk,
                resident support, deployment complexity, and upfront investment.
            </p>
        </div>
    </div>
</div>

<div>
    <div class="card">
        <h2>3. Decision Tree</h2>

        <div class="tree-node">
            <strong>Diagnosis:</strong> the analyzed scenario demands cost reduction
            without critical losses in security, support, and governance.
            <span class="keywords-tag">Adherence: {kw_diag}</span>
        </div>

        <div class="branch">
            <strong>Focus: keep everything as it is</strong>
            <span class="badge danger">Risk</span><br>
            Preserves operational comfort, but maintains financial pressure.
            <span class="keywords-tag">Adherence: {kw_b1}</span>
        </div>

        <div class="branch">
            <strong>Focus: radical economy</strong>
            <span class="badge danger">Sensitive</span><br>
            Reduces cost, but increases risks regarding adaptation and resistance.
            <span class="keywords-tag">Adherence: {kw_b2}</span>
        </div>

        <div class="branch recommended">
            <strong>Focus: balanced transition</strong>
            <span class="badge success">Recommended</span><br>
            Gradual implementation while partially preserving human support.
            <span class="keywords-tag">Adherence: {kw_b3}</span>
        </div>
    </div>

    <div class="card">
        <h2>4. Summary of Context</h2>
        <div class="contexto-container">
            <div class="contexto">
                {html.escape(contexto[:1000])}
            </div>
            <span class="keywords-tag" style="border-top: 1px dotted #e9ecef; padding-top: 2px;">Contextual Focus: {kw_contexto}</span>
        </div>
    </div>
</div>

</div>
</div>
</body>
</html>
"""

col_input, col_preview = st.columns([0.28, 0.72]) 

with col_input:
    st.markdown("### Inputs")

    arquivo = st.file_uploader(
        "TXT",
        type=["txt"],
        label_visibility="collapsed"
    )

    titulo = st.text_input(
        "Title",
        value="Strategic Decision Dashboard"
    )

    objetivo = st.text_input(
        "Objective",
        value="Study of alternatives for target decision-making."
    )

    contexto_manual = st.text_area(
        "Context",
        placeholder="E.g., focus on concierge, costs, safety, elderly care...",
        height=80
    )

    gerar = st.button(
        "Generate report",
        use_container_width=True
    )

with col_preview:
    st.markdown("### Report Preview")

    if gerar:
        texto = ""

        if arquivo:
            texto = arquivo.read().decode("utf-8", errors="ignore")

        contexto = contexto_manual or texto or "No context provided."

        relatorio = gerar_html(
            titulo=titulo,
            objetivo=objetivo,
            contexto=contexto
        )

        st.components.v1.html(
            relatorio,
            height=560,
            scrolling=True
        )

        st.download_button(
            "Download HTML",
            data=relatorio,
            file_name="compact_decision_panel.html",
            mime="text/html",
            use_container_width=True
        )

    else:
        st.info("Upload a TXT file or fill out the context field, then click 'Generate report'.")
