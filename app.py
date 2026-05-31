import streamlit as st
import re

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

.followup-box {
    background-color: #f4f6f7;
    border-left: 4px solid #34495e;
    padding: 10px !important;
    border-radius: 4px;
    margin-top: 0.4rem;
    margin-bottom: 0.4rem;
}

.match-box {
    background-color: #ebf5fb;
    border-left: 4px solid #3498db;
    padding: 8px !important;
    border-radius: 4px;
    margin-top: 0.3rem;
    margin-bottom: 0.3rem;
    font-size: 11.5px;
}

.trigger-btn button {
    width: 100% !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    font-size: 10px !important;
    padding: 0.2rem 0.4rem !important;
    height: 32px !important;
    margin-bottom: 4px !important;
    text-align: left !important;
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

# DATA_MAPPING ordered structurally and chronologically (Newest experiences first)
DATA_MAPPING = {
    1: {
        "category": "Core & Fit",
        "title": "1. Tell me about yourself",
        "tag": "FIT",
        "bridge": "I take messy, broken data pipelines and structure them so global businesses can scale without risk.",
        "followup": "With my engineering background and MBA, I don't just write code; I design systems that secure revenue workflows.",
        "match": "Connects André's technical engineering rigor directly to DWA's need for stable, scalable transaction auditing.",
        "case": "Engineering background + MBA + Advanced Analytics.",
        "bullets": [
            "I focus on automated data governance, replacing slow manual checks with clean, programmatic controls.",
            "I turn complex data structures into clear dashboards that help executive teams see risk instantly.",
            "My target is to help digital companies secure their money and keep data clean across borders."
        ]
    },
    2: {
        "category": "Core & Fit",
        "title": "2. Why DWA?",
        "tag": "STRATEGY",
        "bridge": "Your main compliance risks are not at a physical shipping dock. They live right inside your checkout database.",
        "followup": "When an online business scales this fast, managing thousands of lines of cross-border data manually in Excel is where things break.",
        "match": "Proves deep knowledge of the digital infoproduct model (MRR/Stripe) over traditional customs brokers.",
        "case": "DWA Cross-border Digital Model (MRR/Stripe/VAT).",
        "bullets": [
            "Operating globally means dealing with dynamic transaction spikes, chargebacks, and complex European VAT lines.",
            "I want to use my SQL skills to build automated lookup scripts that track 100% (one hundred percent) of sales logs.",
            "I focus on securing your transactional pipelines and protecting your cash flow from international tax blocks."
        ]
    },
    3: {
        "category": "Core & Fit",
        "title": "3. Why Trade Compliance?",
        "tag": "COMPLIANCE",
        "bridge": "Modern trade compliance is no longer a legal paperwork task. It is a pure data analytics problem.",
        "followup": "Digital products require precise logical classification rules. If your database views are wrong, your tax reporting fails.",
        "match": "Transforms the lack of traditional maritime customs background into a massive technical competitive advantage.",
        "case": "Data Governance & Process Workflows.",
        "bullets": [
            "Traditional customs analysts check papers one by one. I build automated code filters to check data in bulk.",
            "My experience in data governance allows me to categorize and track global digital assets in real time.",
            "I make compliance data predictable so we patch regulatory errors before they cost the company money."
        ]
    },
    4: {
        "category": "Core & Fit",
        "title": "4. Your Value Proposition",
        "tag": "VALUE",
        "bridge": "I bring technical scale and automation to a department that traditionally works with manual tools.",
        "followup": "I translate long, wordy tax rules into clean code logic, removing human error from the operational workflow.",
        "match": "Directly targets DWA's hidden pain point: scaling operations efficiently without multiplying manual headcount.",
        "case": "FinOps, SQL, and Advanced Pipeline Automation.",
        "bullets": [
            "I eliminate operational blind spots by embedding compliance rules right inside the data pipeline.",
            "I build transparent dashboards that give leadership a fully reliable view of global tax and risk exposure.",
            "My goal is simple: zero friction at the checkout page and zero compliance risk with international authorities."
        ]
    },
    5: {
        "category": "Core & Fit",
        "title": "5. Salary Expectations",
        "tag": "ANCHOR",
        "bridge": "My financial target is based on the data infrastructure scale and cost savings I can deliver.",
        "case": "Firm Target Range (Clear numbers written out).",
        "followup": "I am fully aligned with market rates for an analyst who actively implements cost controls and data governance.",
        "match": "Establishes a firm professional anchor, linking compensation directly to ROI and database optimization.",
        "bullets": [
            "For a local Brazilian structure, my target is between 8,000 (eight thousand) and 10,000 (ten thousand) Reais per month.",
            "For an international contract setup, that maps to 2,000 (two thousand) US Dollars monthly.",
            "This cost is justified by my ability to optimize cloud data spend and protect global business revenue streams."
        ]
    },
    11: {
        "category": "Core Cases (STAR)",
        "title": "11. ASICS (2026 - FinOps)",
        "tag": "FINOPS",
        "bridge": "I built a unified, cross-border financial data model across 3 (three) countries to secure revenue tracking.",
        "case": "Stalse Project for ASICS Latam (Brazil, Chile, Colombia).",
        "followup": "We merged multi-source data from GA4 and marketing platforms, integrating dynamic currency conversion formulas.",
        "match": "Directly mirrors DWA's cross-border reality. Proves capacity to consolidate fragmented international financial rows.",
        "bullets": [
            "Situation: Fragmented revenue views across multiple regions created massive visibility and financial forecasting risks.",
            "Action: I re-engineered the data foundations using BigQuery and automated daily pipeline loads via advanced SQL.",
            "Result: I slashed cloud data consumption down from Gigabytes to Megabytes, cutting database query costs significantly."
        ]
    },
    12: {
        "category": "Core Cases (STAR)",
        "title": "12. NTT DATA / Itaú (2025)",
        "tag": "BIG DATA",
        "bridge": "I engineered cloud data pipelines to roll out automated metrics for 5,000 (five thousand) business executives.",
        "case": "Data Analyst at NTT Data for Itaú (AWS Cloud Environment).",
        "followup": "The core challenge was cleansing dirty database records and mapping complex structural business rules at scale.",
        "match": "Proves ability to process millions of transactions without breaking, mapping perfectly to DWA's high sales volumes.",
        "bullets": [
            "Situation: The client needed to process tables with billions of rows, fighting duplicate entries and broken customer data strings.",
            "Action: I built complex database views and data transformations using Amazon Athena, S3, and AWS Glue pipelines.",
            "Result: Delivered a reliable, automated dashboard with absolute data consistency and zero manual processing lag."
        ]
    },
    13: {
        "category": "Core Cases (STAR)",
        "title": "13. Heineken (2023 - 2024)",
        "tag": "E-COMMERCE",
        "bridge": "I normalized chaotic e-commerce data lines across 200 (two hundred) distinct online digital products.",
        "case": "Sxpel Technologies allocated at Heineken (Digital Channel Analytics).",
        "followup": "I mapped out clean relational database structures to ensure the data was fully auditable by business teams.",
        "match": "Leverages direct expertise in e-commerce workflows and checkout structures, matching DWA's pure digital model.",
        "bullets": [
            "Situation: Received messy spreadsheets from multiple external clients, all in different formats, blocking performance tracking.",
            "Action: Designed a scalable Star Schema data model and built a unified dashboard tool using Power BI.",
            "Result: Launched the first stable automation in less than 1 (one) month, matching financial metrics to the exact penny."
        ]
    },
    15: {
        "category": "Core Cases (STAR)",
        "title": "15. Afinz (2022 - 2023)",
        "tag": "GOVERNANCE",
        "bridge": "I hate slow, manual, non-compliant workflows, so I build automated pipelines to enforce governance.",
        "case": "MIS Analyst at Afinz / Sorocred.",
        "followup": "I also documented our metadata rules and processes inside Confluence to ensure the team followed strict audit standards.",
        "match": "Proves an obsession with efficiency. Compliance teams love analysts who proactively eliminate slow processes.",
        "bullets": [
            "Situation: Daily business reporting routines were completely manual, taking 1.5 (one and a half) hours and creating operational delays.",
            "Action: Developed automated ETL data pipelines using Python, SQL, and structured metadata repositories.",
            "Result: Slashed processing time down to just 15 (fifteen) minutes while significantly strengthening data quality layers."
        ]
    },
    14: {
        "category": "Core Cases (STAR)",
        "title": "14. Burity (Long Tenure)",
        "tag": "RISK-AUDIT",
        "bridge": "I acted as a legal proxy managing high-value regulatory, legal, and operational compliance risks.",
        "case": "Asset & Property Manager at Burity Empresarial.",
        "followup": "I sat at the table with lawyers, engineers, and public registries to clean up massive descriptive and structural errors.",
        "match": "Highlights core regulatory mindset: reading legal files, auditing contracts, and mitigating corporate liability.",
        "bullets": [
            "Situation: Managed complex land and infrastructure compliance rules involving multi-million dollar corporations and federal registries.",
            "Action: Audited and verified legal processes, agreements, property contracts, and complex government blueprints.",
            "Result: Fixed major historical compliance errors administratively, securing expansions with zero lawsuits or penalties."
        ]
    },
    6: {
        "category": "Handling Objections",
        "title": "6. No Physical Customs Exp",
        "tag": "OBJECTION",
        "bridge": "That is true for physical shipping, but I view international trade regulations as logical database rules.",
        "case": "Burity (Legal Audits) + Advanced SQL logic.",
        "followup": "A physical container needs a customs seal; a digital product needs a database code validation rule. The operational logic is identical.",
        "match": "Reconceptualizes a potential skill gap, framing database auditing as the modern solution to digital compliance.",
        "bullets": [
            "Physical customs deal with ocean freight; digital trade compliance deals with real-time transaction logs.",
            "My biggest core strength is taking complex regulatory rules rapidly and transforming them into data filters.",
            "I have spent years auditing high-risk contracts and processes—ensuring data follows rules is what I do best."
        ]
    },
    7: {
        "category": "Handling Objections",
        "title": "7. No HTS Code Mastery",
        "tag": "HTS-PUZZLE",
        "bridge": "HTS classification is a structured database mapping problem. I process complex taxonomies every single day.",
        "case": "Amazon Athena / BigQuery View Structuring.",
        "followup": "Instead of trying to memorize catalog codes like a human broker, I treat them as relational data tables.",
        "match": "Demonstrates technical intelligence—turning static manual lookups into a scalable database automation system.",
        "bullets": [
            "I am highly skilled at setting up dynamic views that adjust instantly when global business rules change.",
            "Classifying a digital asset or a physical cargo item follows the exact same boolean and relational database logic.",
            "I will translate your HTS regulatory catalogs into automated database lookup scripts for instant validation."
        ]
    },
    8: {
        "category": "Handling Objections",
        "title": "8. You are Overqualified",
        "tag": "RETENTION",
        "bridge": "Honestly, I am specifically looking for a complex risk architecture challenge, not a comfortable routine.",
        "case": "FinOps & Cloud Optimization Mentality.",
        "followup": "A quiet, manual data role would be boring. Building automated risk pipelines for a growing brand is what keeps me engaged.",
        "match": "Completely removes the flight-risk anxiety by showing a deep intellectual interest in compliance engineering.",
        "bullets": [
            "I am deeply motivated by engineering scalable, automated compliance guardrails completely from scratch.",
            "A fast-paced digital model like DWA offers the exact data velocity and volume that I enjoy optimizing.",
            "I want to commit long-term to design, code, and secure your cloud compliance infrastructure."
        ]
    },
    16: {
        "category": "Extreme Scenarios",
        "title": "16. Handling a Major Mistake",
        "bridge": "If a pipeline or business rule breaks, my immediate step is to isolate the anomaly and patch the system.",
        "case": "Data Quality and Traceability mindset.",
        "followup": "I believe in absolute transparency—I flag the issue immediately, communicate the impact, and present the patch.",
        "match": "Highlights executive maturity, transparency, and a structural focus on building permanent automated preventative solutions.",
        "bullets": [
            "I take full ownership of the problem, run root-cause analysis, and pull the logs to see exactly what failed.",
            "I immediately deploy an automated data quality layer to ensure that specific business failure can never happen again.",
            "In my framework, a production error is simply an urgent signal showing us where to upgrade our system rules."
        ]
    },
    18: {
        "category": "Extreme Scenarios",
        "title": "18. Conflict with Stakeholders",
        "bridge": "I do not argue with subjective opinions. I align conflicting teams by putting hard data criteria on the table.",
        "case": "Strategic performance meetings with diverse teams.",
        "followup": "People usually argue because of underlying business anxieties. Once you map the actual system risk with data, the argument stops.",
        "match": "Showcases strong, non-combative interpersonal skills, using objective metrics to create corporate alignment.",
        "bullets": [
            "I always start by listening closely to understand the core compliance or financial concern the team is facing.",
            "I present clear, comparative data performance models to take emotional biases out of the workspace.",
            "Once the transactional numbers and risks are visible, stakeholders naturally align on the best operational path."
        ]
    },
    19: {
        "category": "Extreme Scenarios",
        "title": "19. Tech to Non-Tech",
        "tag": "COMMUNICATION",
        "bridge": "I translate complex backend data pipelines into clear financial impacts and business risk mitigation.",
        "case": "Executive reporting layers at Afinz and Heineken.",
        "followup": "Non-technical leaders don't need to know the database query syntax; they need to know if the company is safe.",
        "match": "Matches DWA's cross-functional requirement. Proves ability to interact smoothly with legal and business heads.",
        "bullets": [
            "I never explain the backend SQL query logic. I explain the hour savings or the tax exposure we eliminated.",
            "I use standard corporate metrics that leadership cares about, like cost reduction, cloud optimization, or time saved.",
            "I make compliance visually obvious through clean dashboards rather than talking about complex engineering pipelines."
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
    st.metric(label="Adherence Score", value="96%", delta="Elite Match")
        
    st.caption("**Target:** DWA · Trade Compliance Analyst")

categories_list = ["Core & Fit", "Core Cases (STAR)", "Handling Objections", "Extreme Scenarios"]
cols = st.columns(4)

for idx, cat_name in enumerate(categories_list):
    with cols[idx]:
        st.markdown(f'<div class="category-header">{cat_name}</div>', unsafe_allow_html=True)
        
        cat_items = {k: v for k, v in DATA_MAPPING.items() if v["category"] == cat_name}
        
        for item_id, item_data in cat_items.items():
            is_active = (st.session_state.active_id == item_id)
            
            # Button Label with implicit core tag token
            tag_token = f"[{item_data.get('tag', 'CONTEXT')}] "
            clean_title = item_data['title'].split(". ")[1] if ". " in item_data['title'] else item_data['title']
            btn_label = f"▸ {tag_token}{clean_title}" if is_active else f"{tag_token}{clean_title}"
            
            st.markdown('<div class="trigger-btn">', unsafe_allow_html=True)
            if st.button(btn_label, key=f"btn_{item_id}"):
                st.session_state.active_id = item_id
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='margin-top: 0.6rem; border-top: 1px solid #e9ecef; margin-bottom: 0.4rem;'></div>", unsafe_allow_html=True)

active_data = DATA_MAPPING[st.session_state.active_id]

col_out1, col_out2 = st.columns([0.48, 0.52])

with col_out1:
    st.markdown(
        f"""
        <div class="response-box">
            <span style="color:#117a65; font-size:11px; font-weight:bold; text-transform:uppercase;">The Golden Bridge (Simple phrasing):</span><br>
            <strong style="font-size:13.5px; color:#2c3e50;">"{active_data['bridge']}"</strong>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    st.markdown(
        f"""
        <div class="followup-box">
            <span style="color:#2c3e50; font-size:11px; font-weight:bold; text-transform:uppercase;">Deep Dive (If asked to elaborate):</span><br>
            <p style="font-size:12.5px; color:#34495e; margin-top:2px;">{active_data['followup']}</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    st.markdown(
        f"""
        <div class="match-box">
            <strong style="color:#2980b9; text-transform:uppercase; font-size:10px;">The Compliance Match Concept:</strong><br>
            {active_data['match']}
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    st.markdown(f"<p style='font-size:12px; margin-top:0.4rem;'><strong>Case Context Reference:</strong> {active_data['case']}</p>", unsafe_allow_html=True)

with col_out2:
    st.markdown("<p style='font-weight:bold; font-size:12px; color:#2c3e50; margin-bottom:0.3rem;'>Bulletproof Supporting Arguments:</p>", unsafe_allow_html=True)
    for bullet in active_data["bullets"]:
        st.markdown(f"<p style='font-size:12.5px; margin-bottom:5px !important;'>• {bullet}</p>", unsafe_allow_html=True)
