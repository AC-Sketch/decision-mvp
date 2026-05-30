# app.py
import streamlit as st
import random

st.set_page_config(page_title="Missão NR-1", layout="wide")

if "fase" not in st.session_state:
    st.session_state.fase = 0
    st.session_state.saude = 50
    st.session_state.conformidade = 50
    st.session_state.resultado = 50
    st.session_state.jogadores = []
    st.session_state.iniciado = False

fases = [
    "Entender o Território NR-1",
    "Identificar os Sinais",
    "Mapeamento dos Riscos",
    "Conselho da Liderança",
    "Crise em Curso",
    "Construção do Plano de Ação",
    "Implementação",
    "Auditoria NR-1",
    "Cultura Sustentável"
]

personagens = [
    "Diretor Executivo",
    "RH",
    "Gestor Operacional",
    "Colaborador",
    "Técnico de Segurança",
    "Psicólogo Organizacional",
    "Compliance",
    "Auditor",
    "Representante dos Trabalhadores"
]

eventos = [
    {
        "titulo": "Meta Impossível",
        "descricao": "A empresa aumentou as metas sem revisar recursos e carga de trabalho.",
        "opcoes": {
            "Manter a meta e cobrar resultado": (-15, -10, 15),
            "Revisar a meta com as lideranças": (10, 10, 5),
            "Criar plano de apoio às equipes": (15, 5, 0)
        }
    },
    {
        "titulo": "Denúncia de Assédio",
        "descricao": "Uma denúncia anônima indica comportamento abusivo de uma liderança.",
        "opcoes": {
            "Ignorar até aparecerem provas": (-20, -20, 0),
            "Abrir apuração formal": (10, 20, -5),
            "Afastar preventivamente e acolher envolvidos": (15, 15, -10)
        }
    },
    {
        "titulo": "Sinais de Burnout",
        "descricao": "Uma equipe apresenta absenteísmo, irritabilidade e queda de desempenho.",
        "opcoes": {
            "Cobrar mais produtividade": (-20, -10, 5),
            "Realizar escuta estruturada": (20, 10, 0),
            "Redistribuir carga de trabalho": (15, 10, -5)
        }
    },
    {
        "titulo": "Falha de Comunicação",
        "descricao": "Mudanças internas foram comunicadas de forma confusa, gerando insegurança.",
        "opcoes": {
            "Deixar cada gestor explicar como quiser": (-10, -5, 0),
            "Criar comunicação oficial e espaço para dúvidas": (10, 10, 5),
            "Fazer reuniões por área com RH e liderança": (15, 5, 0)
        }
    }
]

st.title("🎲 Missão NR-1: A Jornada da Cultura Segura")

if not st.session_state.iniciado:
    st.subheader("Contexto do Jogo")

    st.write("""
    A empresa enfrenta desafios relacionados à saúde mental, pressão por resultados,
    comunicação, liderança e riscos psicossociais.

    A missão dos jogadores é conduzir a organização por 9 etapas,
    tomando decisões que equilibrem:

    - Saúde Organizacional
    - Conformidade NR-1
    - Resultado do Negócio
    """)

    st.markdown("### Grito de Guerra")
    st.info("Perceber, prevenir, proteger!")

    qtd = st.slider("Número de jogadores", 1, 9, 4)

    escolhidos = st.multiselect(
        "Escolha os personagens",
        personagens,
        max_selections=qtd
    )

    if st.button("Iniciar Jornada"):
        if len(escolhidos) == qtd:
            st.session_state.jogadores = escolhidos
            st.session_state.iniciado = True
            st.rerun()
        else:
            st.warning("Escolha exatamente o número de personagens definido.")

else:
    fase_atual = fases[st.session_state.fase]

    st.header(f"Etapa {st.session_state.fase + 1}: {fase_atual}")

    col1, col2, col3 = st.columns(3)

    col1.metric("❤️ Saúde Organizacional", st.session_state.saude)
    col2.metric("📋 Conformidade NR-1", st.session_state.conformidade)
    col3.metric("📈 Resultado do Negócio", st.session_state.resultado)

    st.markdown("### Personagens em jogo")
    st.write(", ".join(st.session_state.jogadores))

    evento = random.choice(eventos)

    st.markdown("### Carta de Evento")
    st.warning(f"**{evento['titulo']}**")
    st.write(evento["descricao"])

    escolha = st.radio(
        "Qual decisão o grupo toma?",
        list(evento["opcoes"].keys())
    )

    if st.button("Aplicar decisão"):
        impacto = evento["opcoes"][escolha]

        st.session_state.saude += impacto[0]
        st.session_state.conformidade += impacto[1]
        st.session_state.resultado += impacto[2]

        st.session_state.saude = max(0, min(100, st.session_state.saude))
        st.session_state.conformidade = max(0, min(100, st.session_state.conformidade))
        st.session_state.resultado = max(0, min(100, st.session_state.resultado))

        if st.session_state.fase < 8:
            st.session_state.fase += 1
            st.rerun()
        else:
            st.session_state.fase += 1
            st.rerun()

    if st.session_state.fase >= 9:
        st.header("Resultado Final")

        media = (
            st.session_state.saude +
            st.session_state.conformidade +
            st.session_state.resultado
        ) / 3

        if media >= 80:
            classificacao = "Referência em Saúde Organizacional"
        elif media >= 60:
            classificacao = "Empresa Segura"
        elif media >= 40:
            classificacao = "Empresa em Desenvolvimento"
        else:
            classificacao = "Empresa em Situação Crítica"

        st.success(f"Classificação final: {classificacao}")

        st.write("### Recomendações")
        if st.session_state.saude < 60:
            st.write("- Reforçar ações de escuta, prevenção ao assédio e equilíbrio de carga de trabalho.")
        if st.session_state.conformidade < 60:
            st.write("- Revisar documentação, PGR, fluxo de riscos psicossociais e evidências.")
        if st.session_state.resultado < 60:
            st.write("- Conectar as ações de saúde organizacional aos indicadores de negócio.")

        if st.button("Reiniciar jogo"):
            st.session_state.clear()
            st.rerun()
