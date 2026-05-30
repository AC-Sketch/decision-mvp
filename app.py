import random
import streamlit as st

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Missão NR-1: A Jornada da Cultura Segura",
    page_icon="🎲",
    layout="wide"
)

# 2. BANCO DE DADOS DO JOGO (Fases, Personagens com Atributos e Cartas de Evento)
FASES = [
    {
        "nome": "Acampamento Base: Entender o Território",
        "objetivo": "Compreender o escopo da NR-1, seus objetivos e a contextualização dos riscos psicossociais no ambiente de trabalho.",
        "aprendizado": "A NR-1 dita as diretrizes gerais de SST. Entender que o Gerenciamento de Riscos Ocupacionais (GRO) abrange a saúde integral (física e mental) é o passo zero."
    },
    {
        "nome": "Bosque da Percepção: Identificar os Sinais",
        "objetivo": "Reconhecer precocemente os sinais de esgotamento, conflitos latentes e falhas de comunicação interna.",
        "aprendizado": "Riscos psicossociais começam silenciosos. Escuta ativa e mapeamento de clima evitam o agravamento de crises."
    },
    {
        "nome": "Vale do Mapeamento: Análise de Riscos",
        "objetivo": "Classificar os fatores organizacionais e psicossociais que impactam os times.",
        "aprendizado": "Fatores como sobrecarga de trabalho e metas desalinhadas devem ser tratados como riscos reais no inventário da empresa."
    },
    {
        "nome": "Planície da Liderança: O Conselho das Decisões",
        "objetivo": "Tomar decisões gerenciais equilibrando a pressão por entregas e a capacidade humana.",
        "aprendizado": "A liderança desempenha papel central na modulação do estresse e na aplicação prática da cultura preventiva."
    },
    {
        "nome": "Desfiladeiro da Crise: Eventos em Curso",
        "objetivo": "Mitigar e responder a eventos críticos (burnout, assédio ou picos abruptos de absenteísmo).",
        "aprendizado": "A resposta imediata à crise define a maturidade da empresa. Acolhimento e neutralização do dano são prioridades."
    },
    {
        "nome": "Campo da Ação: Construção do Plano",
        "objetivo": "Transformar diagnósticos em ações preventivas estruturadas e mensuráveis.",
        "aprendizado": "Planos de ação eficientes determinam prazos, responsáveis claros e indicadores de eficácia (Ex: canais de escuta, rituais de alinhamento)."
    },
    {
        "nome": "Pântano da Implementação: Execução Prática",
        "objetivo": "Alocar recursos e executar as medidas propostas diante de limitações orçamentárias.",
        "aprendizado": "Sem execução e consistência, os planos viram relatórios gaveta. A prevenção exige constância operacional."
    },
    {
        "nome": "Portal da Auditoria: Verificação de Conformidade",
        "objetivo": "Comprovar a rastreabilidade dos processos e a retenção de evidências documentais.",
        "aprendizado": "A conformidade legal com a NR-1 exige histórico transparente: o que foi identificado, qual foi o plano e como está o monitoramento."
    },
    {
        "nome": "Pico da Cultura Sustentável: Maturidade Organizacional",
        "objetivo": "Avaliar os impactos cumulativos das decisões na saúde, conformidade e resultado final.",
        "aprendizado": "Cultura de segurança não é um projeto com fim, mas um modelo contínuo de tomada de decisão focada em pessoas e sustentabilidade."
    }
]

# Personagens com Atributos de RPG (Escala de 1 a 5)
PERSONAGENS_DADOS = {
    "Diretor Executivo": {"Conhecimento": 3, "Prevenção": 2, "Comunicação": 5, "descricao": "Foco em estratégia e performance corporativa. Forte em engajar decisões críticas."},
    "RH (Recursos Humanos)": {"Conhecimento": 4, "Prevenção": 4, "Comunicação": 4, "descricao": "Foco em pessoas, clima e mediação de conflitos organizacionais."},
    "Gestor Operacional": {"Conhecimento": 2, "Prevenção": 3, "Comunicação": 4, "descricao": "Foco em execução e entregas do dia a dia da linha de frente."},
    "Colaborador (Representante)": {"Conhecimento": 3, "Prevenção": 4, "Comunicação": 3, "descricao": "Vivência direta da rotina laboral; termômetro real dos riscos ocultos."},
    "Técnico de Segurança": {"Conhecimento": 5, "Prevenção": 5, "Comunicação": 2, "descricao": "Especialista em normas, inspeção de campo e mitigação técnica."},
    "Psicólogo Organizacional": {"Conhecimento": 4, "Prevenção": 5, "Comunicação": 4, "descricao": "Foco em saúde mental, fatores psicossociais e acolhimento clínico/corporativo."},
    "Compliance": {"Conhecimento": 5, "Prevenção": 3, "Comunicação": 3, "descricao": "Guardião das regras de conduta, ética, canais de denúncia e governança."},
    "Auditor Interno": {"Conhecimento": 5, "Prevenção": 4, "Comunicação": 2, "descricao": "Foco em evidências, métricas frias e aderência legal restrita."},
    "Facilitador / Consultor": {"Conhecimento": 4, "Prevenção": 4, "Comunicação": 5, "descricao": "Elo de ligação que estimula o diálogo e o aprendizado entre as áreas."}
}

EVENTOS = [
    {
        "titulo": "🚀 Meta Impossível",
        "descricao": "A diretoria aumentou as metas do trimestre em 40% sem revisar recursos, prazos ou ferramentas de apoio, gerando sobrecarga imediata.",
        "atributo_chave": "Comunicação",
        "opcoes": {
            "Aceitar e repassar cobrança de forma rígida": {"saude": -20, "conformidade": -10, "resultado": 15, "feedback": "O resultado financeiro sobe no curtíssimo prazo, mas o clima colapsa e gera passivos."},
            "Revisar metas de forma participativa com dados das áreas": {"saude": 15, "conformidade": 12, "resultado": 5, "feedback": "Equilíbrio sustentável. Alinhamento técnico gera previsibilidade e engajamento."},
            "Criar força-tarefa de apoio emocional sem alterar os prazos": {"saude": 5, "conformidade": -5, "resultado": 5, "feedback": "Ação paliativa. Cuidar do sintoma sem mexer na causa raiz (a sobrecarga) não resolve o problema estrutural."}
        }
    },
    {
        "titulo": "⚖️ Denúncia de Assédio",
        "descricao": "Uma denúncia detalhada no canal anônimo aponta comportamento abusivo crônico e gritos por parte de um gerente de alta performance.",
        "atributo_chave": "Conhecimento",
        "opcoes": {
            "Abafar o caso temporariamente para não prejudicar as entregas": {"saude": -25, "conformidade": -25, "resultado": 5, "feedback": "Risco Crítico! A omissão destrói a confiança psicológica e viola frontalmente as diretrizes de compliance e NR-1."},
            "Afastar o denunciado imediatamente para apuração formal rigorosa": {"saude": 15, "conformidade": 20, "resultado": -5, "feedback": "Conformidade exemplar. Demonstra que a integridade física e mental está acima de qualquer indicador financeiro."},
            "Realizar feedback informal com o gestor sem abrir processo": {"saude": -10, "conformidade": -10, "resultado": 0, "feedback": "Ação fraca. Passa a impressão de impunidade e deixa a empresa juridicamente exposta."}
        }
    },
    {
        "titulo": "🌪️ Sinais de Burnout Coletivo",
        "descricao": "Um setor estratégico apresenta picos de absenteísmo, explosões emocionais em reuniões e uma queda acentuada na qualidade das entregas.",
        "atributo_chave": "Prevenção",
        "opcoes": {
            "Exigir relatórios diários de produtividade para conter a queda": {"saude": -25, "conformidade": -10, "resultado": -10, "feedback": "Aumento de controle em momentos de exaustão acelera pedidos de demissão e afastamentos médicos."},
            "Rodar escuta psicossocial estruturada e adequar a divisão de tarefas": {"saude": 20, "conformidade": 15, "resultado": 0, "feedback": "Excelente. Diagnóstico com plano de alívio de carga mental foca diretamente no controle do risco psicossocial."},
            "Contratar uma palestra motivacional de fim de ano": {"saude": -5, "conformidade": -5, "resultado": -5, "feedback": "Incompatível. Tentar tratar exaustão crônica organizacional com automotivantes pontuais gera frustração na equipe."}
        }
    },
    {
        "titulo": "🗣️ Comunicação Ruído",
        "descricao": "Rumores de reestruturação societária estão gerando pânico generalizado e boatos de demissão em massa por falta de posicionamento oficial.",
        "atributo_chave": "Comunicação",
        "opcoes": {
            "Manter silêncio até que tudo esteja 100% assinado": {"saude": -15, "conformidade": -5, "resultado": -10, "feedback": "A rádio peão assume o controle. A ansiedade generalizada paralisa as operações."},
            "Abrir um pronunciamento transparente e espaço para perguntas": {"saude": 15, "conformidade": 10, "resultado": 10, "feedback": "Transparência reduz a ansiedade e foca a energia das equipes em fatos reais, mitigando o estresse."},
            "Emitir um comunicado genérico por e-mail desmentindo os boatos": {"saude": -5, "conformidade": 0, "resultado": 0, "feedback": "Gera desconfiança mútua. Comunicados frios tendem a alimentar mais teorias de conspiração."}
        }
    },
    {
        "titulo": "🏛️ Auditoria de SST de Surpresa",
        "descricao": "Fiscais do trabalho exigem a demonstração imediata de como a empresa integra a identificação de riscos psicossociais e ergonômicos no GRO/PGR.",
        "atributo_chave": "Conhecimento",
        "opcoes": {
            "Improvisar uma planilha de última hora baseada em modelos da internet": {"saude": -10, "conformidade": -20, "resultado": -5, "feedback": "Risco de autuação. Textos genéricos não resistem a uma auditoria aprofundada baseada em evidências reais."},
            "Apresentar as atas de comitês, mapeamentos reais e o plano de ação ativo": {"saude": 5, "conformidade": 25, "resultado": 5, "feedback": "Perfeito! A rastreabilidade prova o cumprimento das exigências do GRO da nova NR-1."},
            "Admitir lacunas técnicas e protocolar um plano formal de correção imediata": {"saude": 10, "conformidade": 12, "resultado": 0, "feedback": "Postura íntegra. Assumir e desenhar uma linha corretiva reduz penalidades de fiscalização ativa."}
        }
    }
]

# 3. FUNÇÕES DO SISTEMA
def inicializar_jogo():
    st.session_state.fase = 0
    st.session_state.saude = 60
    st.session_state.conformidade = 60
    st.session_state.resultado = 60
    st.session_state.personagens_escolhidos = []
    st.session_state.iniciado = False
    st.session_state.historico = []
    st.session_state.evento_atual = None
    st.session_state.ultimo_feedback = ""

def limitar_valores(valor):
    return max(0, min(100, valor))

def renderizar_tabuleiro(fase_atual):
    icones = ["🚩", "🌳", "🔍", "⚖️", "🌪️", "🛠️", "📦", "🏛️", "🏆"]
    barras = []
    for idx, icone in enumerate(icones):
        if idx == fase_atual:
            barras.append(f"**[{icone} F{idx+1}]**")
        elif idx < fase_atual:
            barras.append("✅")
        else:
            barras.append(icone)
    return " ── ".join(barras)

def calcular_classificacao(s, c, r):
    pior_indicador = min(s, c, r)
    media = (s + c + r) / 3
    
    if pior_indicador < 35:
        return "⚠️ Empresa em Risco Crítico (Risco iminente de autuações, Burnout massivo ou Processos Judiciais)"
    if media >= 80 and pior_indicador >= 65:
        return "🌟 Referência em Cultura Segura (Sustentabilidade humana, legal e alto rendimento comercial)"
    if media >= 65 and pior_indicador >= 50:
        return "📈 Empresa Segura em Evolução (Bons caminhos tomados, necessita de ajustes contínuos)"
    return "🩹 Empresa Vulnerável (Ações reativas que apagam incêndios, mas não tratam a raiz estrutural)"

# 4. CONTROLE DE ESTADO INICIAL
if "iniciado" not in st.session_state:
    inicializar_jogo()

# 5. RENDERIZAÇÃO DA INTERFACE STREAMLIT
st.title("🎲 Missão NR-1: A Jornada da Cultura Segura")
st.caption("A simulação de tomada de decisão que conecta Riscos Psicossociais, Gestão Ocupacional e Performance do Negócio.")

# Carregamento do Banner Visual
try:
    st.image("assets/cenario.png", use_container_width=True)
except Exception:
    pass

# TELA 1: SETUP E CONFIGURAÇÃO DA PARTIDA
if not st.session_state.iniciado:
    st.markdown("""
    ### 🎯 A Missão Organizacional
    A sua empresa está passando por um período crítico de transição operacional. O desafio do comitê de liderança 
    é atravessar as **9 etapas da jornada**, gerenciando incidentes reais. Suas escolhas moldarão a integridade 
    da cultura e ditarão se a empresa prosperará ou entrará em colapso.
    """)
    
    st.warning("🗣️ **Grito de Guerra Corporativo:** *Perceber os riscos, prevenir os danos, proteger as pessoas!*")
    
    st.markdown("---")
    st.subheader("⚙️ Configuração da Partida")
    
    versao = st.radio("Selecione o tamanho do Comitê de Crise:", ["Modo Reduzido (2 a 5 Jogadores)", "Modo Expandido (6 a 9 Jogadores)"], horizontal=True)
    
    limite_max = 5 if "Reduzido" in versao else 9
    
    personagens_selecionados = st.multiselect(
        f"Selecione de 2 a {limite_max} membros para compor o seu time de tomadores de decisão:",
        list(PERSONAGENS_DADOS.keys()),
        max_selections=limite_max
    )
    
    if personagens_selecionados:
        st.markdown("**Atributos da Equipe Selecionada:**")
        cols = st.columns(len(personagens_selecionados))
        for idx, p in enumerate(personagens_selecionados):
            with cols[idx]:
                st.markdown(f"**{p}**")
                st.caption(PERSONAGENS_DADOS[p]["descricao"])
                st.text(f"🧠 Conhec.: {PERSONAGENS_DADOS[p]['Conhecimento']}")
                st.text(f"🛡️ Preven.: {PERSONAGENS_DADOS[p]['Prevenção']}")
                st.text(f"💬 Comun.: {PERSONAGENS_DADOS[p]['Comunicação']}")

    st.markdown("---")
    with st.expander("📚 Alinhamento Inicial: O que dita a Nova NR-1?"):
        st.markdown("""
        A **NR-1 (Disposições Gerais e Gerenciamento de Riscos Ocupacionais)** exige que as organizações estruturem o 
        **PGR (Programa de Gerenciamento de Riscos)** focado em identificar perigos, avaliar o nível dos riscos e implantar 
        medidas de prevenção com monitoramento contínuo. 
        
        No ambiente moderno, os **fatores psicossociais** (assédio, sobrecarga mental, liderança abusiva) integraram-se a essa 
        matriz de perigos, impactando diretamente a conformidade legal e a produtividade da empresa.
        """)

    if st.button("▶️ Iniciar Expedição", type="primary"):
        if len(personagens_selecionados) < 2:
            st.error("Selecione pelo menos 2 personagens para viabilizar as dinâmicas de debate e votação do comitê.")
        else:
            st.session_state.personagens_escolhidos = personagens_selecionados
            st.session_state.iniciado = True
            st.session_state.evento_atual = random.choice(EVENTOS)
            st.rerun()

# TELA 2: FASE DO JOGO EM CURSO
else:
    # SE JÁ PASSOU DAS 9 FASES - EXIBIR DASHBOARD FINAL
    if st.session_state.fase >= len(FASES):
        st.header("🏁 Destino Alcançado: Relatório de Maturidade")
        st.markdown(renderizar_tabuleiro(8))
        st.markdown("---")
        
        # Painel de Métricas Finais
        c1, c2, c3 = st.columns(3)
        c1.metric("❤️ Saúde Organizacional final", f"{st.session_state.saude}/100")
        c2.metric("📋 Conformidade Geral NR-1", f"{st.session_state.conformidade}/100")
        c3.metric("📈 Desempenho & Resultado", f"{st.session_state.resultado}/100")
        
        status_final = calcular_classificacao(st.session_state.saude, st.session_state.conformidade, st.session_state.resultado)
        st.success(f"### **Classificação de Mercado:**\n{status_final}")
        
        # Recomendações Dinâmicas da Consultoria
        st.markdown("### 📋 Plano de Ação Estrutural Recomendado")
        recs_geradas = 0
        if st.session_state.saude < 60:
            st.error("🚨 **Ação Corretiva em Saúde Mental:** Priorizar a criação de canais de denúncia criptografados, rituais de alinhamento de carga de trabalho e facilitação de treinamentos contra lideranças autocráticas.")
            recs_geradas += 1
        if st.session_state.conformidade < 60:
            st.error("🚨 **Ação Corretiva em SST Legal:** Revisar imediatamente os parâmetros do seu PGR. Garantir que as avaliações de riscos ergonômicos e organizacionais possuam dados empíricos e evidências físicas auditáveis.")
            recs_geradas += 1
        if st.session_state.resultado < 60:
            st.warning("⚠️ **Ação de Produtividade Sustentável:** Alinhar os fluxos de trabalho operacionais. A baixa eficiência aponta que a exaustão ou os retrabalhos gerados pela desorganização interna estão corroendo as margens financeiras.")
            recs_geradas += 1
        if recs_geradas == 0:
            st.balloons()
            st.info("🏅 **Plano de Manutenção Avançado:** A governança integrada é excelente. Recomenda-se realizar auditorias simuladas anuais e workshops de reciclagem de multiplicadores da cultura de segurança para blindar o modelo atual.")

        # Histórico da Partida
        with st.expander("📜 Ver Diário de Bordo da Jornada"):
            for h in st.session_state.historico:
                st.markdown(f"""
                **Etapa {h['etapa']}**: {h['evento']}
                * **Líder da Rodada:** {h['lider']} | **Ação Tomada:** *{h['decisao']}*
                * **Modificadores Aplicados:** Saúde ({h['impacto']['saude']}), Conformidade ({h['impacto']['conformidade']}), Resultado ({h['impacto']['resultado']})
                * **Resultado nos Dados:** {h['dado_info']}
                """)
                st.caption(f"↳ *Diagnóstico Técnico:* {h['feedback']}")
                st.markdown("---")

        if st.button("🔄 Jogar Novamente / Reiniciar"):
            inicializar_jogo()
            st.rerun()

    # RENDERIZAÇÃO DO LOOP DE ETAPAS ATIVAS
    else:
        dados_fase = FASES[st.session_state.fase]
        
        # Barra visual de Progresso do Tabuleiro
        st.markdown(renderizar_tabuleiro(st.session_state.fase))
        st.markdown("---")
        
        # Painel Informativo da Fase
        st.subheader(f"📍 Etapa {st.session_state.fase + 1}: {dados_fase['nome']}")
        st.markdown(f"🎯 **Objetivo Estratégico:** {dados_fase['objetivo']}")
        
        # Exibição dos Scores Atuais do Negócio
        m1, m2, m3 = st.columns(3)
        m1.metric("❤️ Saúde Organizacional", f"{st.session_state.saude}/100")
        m2.metric("📋 Conformidade NR-1", f"{st.session_state.conformidade}/100")
        m3.metric("📈 Resultado do Negócio", f"{st.session_state.resultado}/100")
        
        # Caixa de Orientação da Fase
        st.info(f"💡 **Fundamento Técnico da Etapa:** {dados_fase['aprendizado']}")
        
        st.markdown("### 🎴 Evento de Campo Sorteado")
        if st.session_state.evento_atual is None:
            st.session_state.evento_atual = random.choice(EVENTOS)
            
        evt = st.session_state.evento_atual
        
        st.error(f"##### **{evt['titulo']}**")
        st.markdown(f"*{evt['descricao']}*")
        st.caption(f"⚙️ Atributo Organizacional exigido para Mitigação: **{evt['atributo_chave']}**")
        
        # Mecânica de Decisão Coletiva
        escolha_opcao = st.radio("Entre em consenso com a equipe. Qual rota de decisão o comitê adotará?", list(evt["opcoes"].keys()))
        
        # Mecânica RPG: Escolha do Líder
        st.markdown("### 🎲 Alocação de Competência (RPG)")
        lider_rodada = st.selectbox(
            "Escolha qual membro do comitê liderará as tratativas deste caso. (O nível de Atributo dele impactará o sucesso do dado):",
            st.session_state.personagens_escolhidos
        )
        
        valor_atributo = PERSONAGENS_DADOS[lider_rodada][evt["atributo_chave"]]
        st.caption(f"ℹ️ {lider_rodada} possui Nível **{valor_atributo}/5** em **{evt['atributo_chave']}**.")
        
        # Exibição do último feedback de rodada se disponível
        if st.session_state.ultimo_feedback:
            st.markdown("---")
            st.success(st.session_state.ultimo_feedback)
            st.session_state.ultimo_feedback = "" # Limpa para o próximo ciclo

        # Botão de Aplicação e Lógica Interna
        if st.button("⚖️ Consolidar e Rolar Dados", type="primary"):
            impacto_base = evt["opcoes"][escolha_opcao].copy()
            feedback_tecnico = evt["opcoes"][escolha_opcao]["feedback"]
            
            # Rolagem do Dado Virtual (D6) + Modificadores do RPG
            rolagem_dado = random.randint(1, 6)
            total_teste = rolagem_dado + valor_atributo
            
            # Cálculo de Bônus de Atributo Organizacional
            texto_dados = ""
            if total_teste >= 8:
                # Sucesso Crítico: Ameniza perdas ou maximiza bônus
                impacto_base["saude"] = impacto_base["saude"] + 4 if impacto_base["saude"] < 0 else impacto_base["saude"] + 6
                impacto_base["conformidade"] = impacto_base["conformidade"] + 4 if impacto_base["conformidade"] < 0 else impacto_base["conformidade"] + 6
                impacto_base["resultado"] = impacto_base["resultado"] + 4 if impacto_base["resultado"] < 0 else impacto_base["resultado"] + 6
                texto_dados = f"✨ Sucesso Crítico no Teste! Rolagem: {rolagem_dado} + Atributo: {valor_atributo} = {total_teste}. A competência do líder minimizou danos e amplificou os retornos da escolha!"
            elif total_teste <= 4:
                # Complicação de Execução por falta de competência focada
                impacto_base["saude"] -= 6
                impacto_base["conformidade"] -= 6
                impacto_base["resultado"] -= 6
                texto_dados = f"❌ Falha de Execução Operacional! Rolagem: {rolagem_dado} + Atributo: {valor_atributo} = {total_teste}. A falta de força técnica na condução gerou gargalos adicionais de atrito."
            else:
                texto_dados = f"⚖️ Execução Regular. Rolagem: {rolagem_dado} + Atributo: {valor_atributo} = {total_teste}. A ação ocorreu exatamente sob as projeções padrão."

            # Atualização de Estados Gerais
            st.session_state.saude = limitar_valores(st.session_state.saude + impacto_base["saude"])
            st.session_state.conformidade = limitar_valores(st.session_state.conformidade + impacto_base["conformidade"])
            st.session_state.resultado = limitar_valores(st.session_state.resultado + impacto_base["resultado"])
            
            # Salvamento no Histórico
            st.session_state.historico.append({
                "etapa": st.session_state.fase + 1,
                "evento": evt["titulo"],
                "decisao": escolha_opcao,
                "lider": lider_rodada,
                "impacto": impacto_base,
                "dado_info": texto_dados,
                "feedback": feedback_tecnico
            })
            
            # Passagem de Turno / Avanço de Etapa
            st.session_state.ultimo_feedback = f"🎯 Consequência Aplicada:\n\n* {texto_dados}\n\n* Análise: {feedback_tecnico}"
            st.session_state.fase += 1
            st.session_state.evento_atual = random.choice(EVENTOS)
            st.rerun()
