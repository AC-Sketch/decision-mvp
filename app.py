import streamlit as st

st.set_page_config(
    page_title="War Room",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 0.5rem !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
    max-width: 100% !important;
}

div[data-testid="stVerticalBlock"] {
    gap: 0.3rem !important;
}

[data-testid="stSidebarUserContent"] {
    padding-top: 1rem !important;
}

h3, p, div {
    margin-top: 0rem !important;
    margin-bottom: 0rem !important;
}

div[data-testid="stMetric"] {
    background-color: #f8f9fa;
    padding: 6px !important;
    border-radius: 4px;
    border: 1px solid #e9ecef;
    text-align: center;
}

.response-box {
    background-color: #e8f8f5;
    border-left: 4px solid #18bc9c;
    padding: 10px !important;
    border-radius: 4px;
    margin-top: 0.4rem;
    margin-bottom: 0.4rem;
}

.trigger-btn button {
    width: 100% !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    font-size: 11px !important;
    padding: 0.2rem 0.4rem !important;
    height: 28px !important;
    margin-bottom: 4px !important;
}

.category-header {
    font-size: 11px !important;
    font-weight: bold !important;
    color: #2c3e50;
    border-bottom: 1px solid #e9ecef;
    padding-bottom: 2px;
    margin-top: 0.1rem !important;
    margin-bottom: 0.4rem !important;
}
</style>
""", unsafe_allow_html=True)

DATA_MAPPING = {
    1: {
        "category": "Core & Fit",
        "title": "1. Tell me about yourself",
        "bridge": "I turn chaotic, cross-border data into structured, compliant workflows.",
        "case": "Engineering background + MBA + Advanced Analytics.",
        "bullets": [
            "I specialize in centralizing financial data and mitigating operational risks.",
            "My focus is automation, replacing slow manual checks with real-time data governance.",
            "I help fast-growing digital businesses scale without breaking regulatory compliance."
        ]
    },
    2: {
        "category": "Core & Fit",
        "title": "2. Why DWA?",
        "bridge": "Your compliance challenges aren't at a physical port; they are inside your database.",
        "case": "DWA Cross-border Digital Model (MRR/Stripe/VAT).",
        "bullets": [
            "As a fast-growing business, you face extreme risks with VAT, transaction spikes, and chargebacks.",
            "I want to apply my analytics background to audit 100% of global sales data dynamically.",
            "I don't look at shipping papers; I look at transaction pipelines to secure cash flow."
        ]
    },
    3: {
        "category": "Core & Fit",
        "title": "3. Why Trade Compliance?",
        "bridge": "Modern trade compliance is fundamentally a data analytics problem.",
        "case": "Data Governance & Process Workflows.",
        "bullets": [
            "Traditional compliance relies on manual Excel checks. I build automated controls.",
            "My experience with data architecture allows me to track and categorize digital assets in real-time.",
            "I ensure data predictability and mitigate regulatory penalties before they happen."
        ]
    },
    4: {
        "category": "Core & Fit",
        "title": "4. Your Value Proposition",
        "bridge": "I bring technical scale to a department that traditionally works manually.",
        "case": "FinOps, SQL, and Advanced Pipeline Automation.",
        "bullets": [
            "I reduce operational gaps by translating complex legal rules into hard code filters.",
            "I build executive dashboards that give leadership a 100% reliable view of global compliance.",
            "My goal is zero friction at the checkout and zero compliance risk with international tax authorities."
        ]
    },
    5: {
        "category": "Core & Fit",
        "title": "5. Salary Expectations",
        "bridge": "My financial requirement is structured based on the value and infrastructure scale I deliver.",
        "case": "Clear Range (Written Out to Avoid Any Verbal Misunderstanding).",
        "bullets": [
            "My target salary is between five thousand and ten thousand Brazilian Reais per month.",
            "For international contracts, this translates to one thousand to two thousand US Dollars per month.",
            "I am fully aligned with standard market rates for a professional maximizing FinOps and data governance."
        ]
    },
    6: {
        "category": "Handling Objections",
        "title": "6. No Physical Customs Exp",
        "bridge": "I view international regulations as complex business rules, not physical barriers.",
        "case": "Burity (Legal Proxy/Audits) + Advanced SQL logic.",
        "bullets": [
            "Physical customs deal with containers; digital compliance deals with transactional logs.",
            "My core strength is learning complex regulatory rules rapidly and turning them into data controls.",
            "I have audited contracts and legal processes as a proxy; the logic of compliance is identical."
        ]
    },
    7: {
        "category": "Handling Objections",
        "title": "7. No HTS Code Mastery",
        "bridge": "HTS classification is a structured logic problem. I process complex taxonomies for breakfast.",
        "case": "Amazon Athena / BigQuery View Structuring.",
        "bullets": [
            "I am highly skilled at setting up dynamic views that adjust according to evolving business taxonomies.",
            "Classifying a digital product or a physical asset follows the same boolean and mathematical logic.",
            "I will translate the HTS catalog into automated lookup scripts inside your database."
        ]
    },
    8: {
        "category": "Handling Objections",
        "title": "8. You are Overqualified",
        "bridge": "I am looking for an intellectual challenge in risk architecture, not a comfortable routine.",
        "case": "FinOps & Cloud Optimization Mentality.",
        "bullets": [
            "I am deeply motivated by building scalable, automated frameworks from scratch.",
            "A fast-paced digital business like DWA offers the exact data complexity that keeps me engaged.",
            "I don't want a boring manual job; I want to engineer your compliance automation."
        ]
    },
    9: {
        "category": "Handling Objections",
        "title": "9. Short Tenures (Stalse/NTT)",
        "bridge": "These were strategic, short-term contract projects targeted to solve hyper-specific architecture blocks.",
        "case": "Agile Sprints & Toolkit Expansion.",
        "bullets": [
            "I look at these projects highly positively because they allowed me to rapidly expand my technical arsenal.",
            "At Stalse, I focused entirely on GCP, BigQuery, and Machine Learning models for ASICS Latam.",
            "At NTT Data, I mastered AWS Athena, S3, and Glue pipelines for high-volume banking systems.",
            "I am now looking for a long-term challenge to implement this complete cross-cloud arsenal."
        ]
    },
    10: {
        "category": "Handling Objections",
        "title": "10. Why change fields now?",
        "bridge": "I am not changing fields; I am applying modern tools to classic governance problems.",
        "case": "Evolution from Management Analytics to Data Engineering.",
        "bullets": [
            "Compliance is moving to the cloud. Companies that don't adapt their data pipelines will fail.",
            "My shift to Advanced Analytics allows me to protect company assets at a scale humans cannot match.",
            "I am positioning myself where the future of operational risk management is."
        ]
    },
    11: {
        "category": "Core Cases (STAR)",
        "title": "11. ASICS (FinOps & Automation)",
        "bridge": "I built a unified, cross-border financial data infrastructure across three countries under FinOps practices.",
        "case": "Stalse Project for ASICS Latam (Brazil, Chile, Colombia).",
        "bullets": [
            "Situation: Fragmented international revenue views and complex currency conversions created extreme visibility and predictability risks.",
            "Action: Re-engineered data foundations using BigQuery, automated daily loads, and designed executive dashboards via Looker on GCP.",
            "Result: Slashed cloud consumption from Gigabytes to Megabytes, optimizing costs while ensuring a 100% compliant and daily updated cross-border financial pipeline."
        ]
    },
    12: {
        "category": "Core Cases (STAR)",
        "title": "12. NTT/Itaú (Billions of Rows)",
        "bridge": "I engineered cloud data pipelines to deliver automated performance reporting to five thousand corporate executives.",
        "case": "Data Analyst at NTT Data for Itaú (AWS Cloud Environment).",
        "bullets": [
            "Situation: The client needed to calculate executive bonuses by joining tables with billions of rows, battling dirty data like missing keywords and mixed CPF/CNPJ records.",
            "Action: Built complex SQL views and robust data transformations inside Amazon Athena, utilizing S3 and AWS Glue to populate online metric cards.",
            "Result: Delivered a reliable, automated QuickSight dashboard that processed massive data loads with absolute data consistency and zero operational friction."
        ]
    },
    13: {
        "category": "Core Cases (STAR)",
        "title": "13. Heineken (Data Consolidation)",
        "bridge": "I normalized chaotic eRetail and eCommerce data from over two hundred distinct products and ten thousand messy product descriptions.",
        "case": "Sxpel Technologies allocated at Heineken (Digital Channel Analytics).",
        "bullets": [
            "Situation: Received fragmented spreadsheets from multiple clients, all in different formats, needing urgent commercial campaign tracking.",
            "Action: Designed a scalable Star Schema model and built a 'OnePage-Performance' dashboard in PowerBI, delivering a complete breakdown by segment, brand, and SKU.",
            "Result: Delivered the first automated iteration in under a month, matching financial indicators to the penny, enabling leadership to immediately spot product stockouts and evaluate campaign performance."
        ]
    },
    14: {
        "category": "Core Cases (STAR)",
        "title": "14. Burity (Stakeholder & Risk)",
        "bridge": "I acted as a legal proxy managing billion-dollar regulatory, legal, and operational risks without a single lawsuit.",
        "case": "Asset & Property Manager at Burity Empresarial.",
        "bullets": [
            "Situation: Managed complex land and infrastructure negotiations involving multinational corporations (Novelis), federal railways (MRS Logistics), land cartels, and centuries-old non-standardized legal blueprints.",
            "Action: Aligned engineers, topographers, lawyers, and public registries to rectify major descriptive errors and process complex land mergers administratively.",
            "Result: Secured critical infrastructure expansions (viaducts and highway connections), driving asset valuation from seven Reais per square meter to over three hundred and forty-five Reais per square meter, with a projected path to one thousand Reais."
        ]
    },
    15: {
        "category": "Core Cases (STAR)",
        "title": "15. Afinz (Data Governance)",
        "bridge": "I hate slow, manual, non-compliant processes. I automate them for speed and security.",
        "case": "MIS Analyst at Afinz / Sorocred.",
        "bullets": [
            "Situation: Daily reporting routines were slow, taking 1.5 hours, creating operational lags.",
            "Action: Developed automated ETL pipelines using Python, SQL, and structured metadata repositories.",
            "Result: Slashed processing time to just 15 minutes and strengthened the data governance framework."
        ]
    },
    16: {
        "category": "Extreme Scenarios",
        "title": "16. Handling a Major Mistake",
        "bridge": "When a rule breaks, my immediate step is not to panic, but to isolate and patch the pipeline.",
        "case": "Data Quality/Traceability mindset.",
        "bullets": [
            "I acknowledge the issue immediately, communicate transparently, and find the root cause.",
            "I implement an automated data quality layer to ensure that specific failure can never happen again.",
            "In my framework, a mistake is a signal to upgrade the automation system."
        ]
    },
    17: {
        "category": "Extreme Scenarios",
        "title": "17. Unmapped High-Pressure Task",
        "bridge": "Under extreme pressure, I rely on structured frameworks, not emotional improvisation.",
        "case": "Agile problem diagnosis.",
        "bullets": [
            "Step 1: I isolate the variables to understand what is threatening the business rule.",
            "Step 2: I gather historical data patterns to support the decision criteria.",
            "Step 3: I deploy a calculated MVP solution and monitor the indicators in real-time."
        ]
    },
    18: {
        "category": "Extreme Scenarios",
        "title": "18. Conflict with Stakeholders",
        "bridge": "I don't argue with opinions; I align expectations using hard data criteria.",
        "case": "Strategic meetings at IDH (Gerdau/Sabesp).",
        "bullets": [
            "I listen to understand the underlying business anxiety or compliance concern.",
            "I present comparative performance models and evidence-based solutions to remove subjectivity.",
            "Once the data is clear, stakeholders naturally align on the best operational path."
        ]
    },
    19: {
        "category": "Extreme Scenarios",
        "title": "19. Explaining Tech to Non-Tech",
        "bridge": "I translate complex data pipelines into clear financial and operational impacts.",
        "case": "Executive presentations at Afinz and Heineken.",
        "bullets": [
            "I never explain the SQL syntax; I explain the risk mitigation or the cost reduction.",
            "I use clear metrics like CAC reduction, cloud optimization, or processing time saved.",
            "I make compliance visible through clean dashboards, not complicated architecture descriptions."
        ]
    },
    20: {
        "category": "Extreme Scenarios",
        "title": "20. Question completely unknown",
        "bridge": "I don't guess unmapped parameters; I outline the engineering process to discover them.",
        "case": "Structured thinking template.",
        "bullets": [
            "I don't have that specific data point right now, but I know exactly how to query it.",
            "I would check the transaction log history, isolate the anomaly, and define the missing rule.",
            "I prioritize process accuracy over fast, unverified guesses."
        ]
    }
}

if "active_id" not in st.session_state:
    st.session_state.active_id = 1

with st.sidebar:
    st.markdown("### Workspace Input")
    cv_file = st.file_uploader("CV (PDF/TXT)", type=["txt", "pdf"], label_visibility="collapsed")
    jd_file = st.file_uploader("Job Description", type=["txt", "pdf"], label_visibility="collapsed")
    
    st.markdown("### Match Analytics")
    if cv_file and jd_file:
        st.metric(label="Adherence Score", value="87%", delta="High Match")
    else:
        st.metric(label="Adherence Score", value="87%", delta="High Match")
        
    st.caption("**Target:** DWA · Trade Compliance Analyst")

categories_list = ["Core & Fit", "Handling Objections", "Core Cases (STAR)", "Extreme Scenarios"]
cols = st.columns(4)

for idx, cat_name in enumerate(categories_list):
    with cols[idx]:
        st.markdown(f'<div class="category-header">{cat_name}</div>', unsafe_allow_html=True)
        
        cat_items = {k: v for k, v in DATA_MAPPING.items() if v["category"] == cat_name}
        
        for item_id, item_data in cat_items.items():
            is_active = (st.session_state.active_id == item_id)
            btn_label = f"▸ {item_data['title']}" if is_active else item_data['title']
            
            st.markdown('<div class="trigger-btn">', unsafe_allow_html=True)
            if st.button(btn_label, key=f"btn_{item_id}"):
                st.session_state.active_id = item_id
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='margin-top: 0.6rem; border-top: 1px solid #e9ecef; margin-bottom: 0.4rem;'></div>", unsafe_allow_html=True)

active_data = DATA_MAPPING[st.session_state.active_id]

col_out1, col_out2 = st.columns([0.45, 0.55])

with col_out1:
    st.markdown(
        f"""
        <div class="response-box">
            <span style="color:#117a65; font-size:11px; font-weight:bold; text-transform:uppercase;">The Golden Bridge:</span><br>
            <strong style="font-size:14px; color:#2c3e50;">"{active_data['bridge']}"</strong>
        </div>
        """, 
        unsafe_allow_html=True
    )
    st.markdown(f"<p style='font-size:12px; margin-top:0.3rem;'><strong>Case Context:</strong> {active_data['case']}</p>", unsafe_allow_html=True)

with col_out2:
    st.markdown("<p style='font-weight:bold; font-size:12px; color:#2c3e50; margin-bottom:0.3rem;'>Bulletproof Arguments:</p>", unsafe_allow_html=True)
    for bullet in active_data["bullets"]:
        st.markdown(f"<p style='font-size:12px; margin-bottom:4px !important;'>• {bullet}</p>", unsafe_allow_html=True)
