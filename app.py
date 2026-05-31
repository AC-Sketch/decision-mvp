import streamlit as st
import re

st.set_page_config(
    page_title="War Room - DWA",
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

.growth-box {
    background-color: #fef9e7;
    border-left: 4px solid #f39c12;
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

# Complete DATA_MAPPING with exactly 20 blocks renumerated and aligned to business rules
DATA_MAPPING = {
    1: {
        "category": "Core & Fit",
        "title": "1. Tell me about yourself",
        "tag": "PROFILE",
        "bridge": "I take messy, unmapped data pipelines and structure them so global digital businesses can scale without risk.",
        "followup": "With my engineering background and MBA, I don't just look at code syntax—I design systems that secure operational and revenue workflows.",
        "match": "Connects your structural engineering rigor directly to DWA's fast-moving transaction pipeline.",
        "growth": "DWA is scaling rapidly with thousands of daily transactions; you provide the architectural safety engine they need right now.",
        "case": "Engineering background + MBA + Advanced Analytics.",
        "bullets": [
            "I focus on data governance, replacing slow manual work with automated backend filters.",
            "I help teams transition away from chaotic spreadsheets into single sources of truth.",
            "My primary goal is to ensure data predictability and mitigate compliance risks dynamically."
        ]
    },
    2: {
        "category": "Core & Fit",
        "title": "2. Why DWA?",
        "tag": "STRATEGY",
        "bridge": "Your compliance risks are not waiting at a physical shipping dock. They are living inside your live checkout database.",
        "followup": "When a digital brand scales cross-border via Stripe, the real bottlenecks are digital tax lines and payment gateway holds.",
        "match": "Proves you understand their exact digital business model (MRR/Infoproducts) better than traditional candidates.",
        "growth": "DWA operates globally with high velocity; they need a data expert who secures cash flow, not a traditional logistics agent.",
        "case": "DWA Cross-border Digital Model (MRR/Stripe/VAT).",
        "bullets": [
            "Operating across multiple regions means managing complex checkout rules and European VAT lines instantly.",
            "I want to apply my SQL toolkit to audit 100% (one hundred percent) of transaction logs automatically.",
            "My focus is protecting your digital checkout funnel from sudden international regulatory blocks."
        ]
    },
    3: {
        "category": "Core & Fit",
        "title": "3. Why Trade Compliance?",
        "tag": "COMPLIANCE",
        "bridge": "Modern trade compliance is no longer a legal paperwork task. It is a pure data analytics problem.",
        "followup": "Digital assets and global checkouts follow logical boolean rules. If your data views are broken, your compliance fails.",
        "match": "Turns a lack of legacy customs experience into a modern technical advantage for a cloud-first company.",
        "case": "Data Governance & Process Workflows.",
        "bullets": [
            "Traditional compliance relies on slow Excel lookups. I build automated scripts to audit data in bulk.",
            "My experience with data frameworks allows me to track and categorize digital transactions in real time.",
            "I ensure operational compliance is embedded directly into the code pipeline to prevent penalties."
        ]
    },
    4: {
        "category": "Core & Fit",
        "title": "4. Your Value Proposition",
        "tag": "VALUE",
        "bridge": "I bring technical scale and pipeline automation to a department that traditionally works with manual tools.",
        "followup": "I bridge the gap between complex legal regulations and hard database rules, removing human error completely.",
        "match": "Directly links your analytics expertise to their immediate need for lean, automated operations.",
        "case": "FinOps, SQL, and Advanced Pipeline Automation.",
        "bullets": [
            "I translate wordy regulatory updates into clean automated database filters.",
            "I build transparent dashboards that give leadership a live, 100% (one hundred percent) reliable view of risk.",
            "My target is zero friction at the checkout page and zero compliance risk with international tax authorities."
        ]
    },
    5: {
        "category": "Core & Fit",
        "title": "5. Salary Expectations",
        "tag": "ANCHOR",
        "bridge": "My financial target is structured based on the infrastructure value and cloud savings I deliver.",
        "case": "Firm Target Range (Clear numbers written out).",
        "followup": "I anchor my rate based on my ability to optimize cloud spend and secure global financial pipelines from day one.",
        "match": "Establishes a transparent, business-driven value alignment without awkward verbal gaps.",
        "growth": "Protects their bottom line. A data-driven approach means your salary is offset by systemic optimization.",
        "bullets": [
            "For a local corporate structure, my target is between 8,000 (eight thousand) and 10,000 (ten thousand) Reais per month.",
            "For an international contractor setup, that maps directly to 2,000 (two thousand) US Dollars per month.",
            "This range reflects a professional who actively implements FinOps and automated data governance layers."
        ]
    },
    6: {
        "category": "Handling Objections",
        "title": "6. No Physical Customs Exp",
        "tag": "OBJECTION",
        "bridge": "That is true for physical shipping, but I view international trade regulations as logical database rules.",
        "case": "Burity (Legal Audits) + Advanced SQL logic.",
        "followup": "A container needs a physical stamp; a global checkout needs a database code validation rule. The logic is identical.",
        "match": "Reframes an apparent skill gap, showing that database auditing is the real solution for digital assets.",
        "growth": "DWA does not ship heavy physical freight. They ship bytes and data logs. Your background matches their true medium.",
        "bullets": [
            "Physical customs deal with ocean cargo; digital compliance deals with real-time transactional logs.",
            "My biggest core strength is picking up tricky regulatory rules fast and turning them into automated data controls.",
            "I have spent years verifying legal contracts and blueprints—ensuring data follows rules is my core expertise."
        ]
    },
    7: {
        "category": "Handling Objections",
        "title": "7. No HTS Code Mastery",
        "tag": "HTS-MAPPING",
        "bridge": "HTS classification is a structured database mapping problem. I process complex taxonomies every day.",
        "case": "Amazon Athena / BigQuery View Structuring.",
        "followup": "Instead of trying to memorize catalog codes like a human broker, I treat them as structured lookup tables.",
        "match": "Demonstrates technical intelligence—turning static manual processes into scalable automation.",
        "growth": "As DWA expands its product lines, manual classification will fail. You offer a script-based lookup engine that scales instantly.",
        "bullets": [
            "I am highly comfortable setting up dynamic views that adapt when business parameters shift.",
            "Classifying a digital asset or a physical cargo item follows the exact same relational database logic.",
            "I will translate your product catalog into automated backend lookup scripts for instant validation."
        ]
    },
    8: {
        "category": "Handling Objections",
        "title": "8. You are Overqualified",
        "tag": "RETENTION",
        "bridge": "Honestly, I am specifically looking for a complex risk architecture challenge, not a comfortable routine.",
        "case": "FinOps & Cloud Optimization Mentality.",
        "followup": "A repetitive manual data role would be boring. Building automated risk frameworks for a scaling brand keeps me sharp.",
        "match": "Removes the flight-risk anxiety by showing deep intellectual alignment with their core data challenges.",
        "growth": "Startups grow too fast for basic profiles. You provide the advanced toolkit that saves them from rebuilding systems next year.",
        "bullets": [
            "I am genuinely motivated by engineering scalable, automated compliance guardrails from scratch.",
            "A fast-paced digital model like DWA offers the exact data velocity and volume that I enjoy optimizing.",
            "I want to commit long-term to design, code, and secure your cloud compliance infrastructure."
        ]
    },
    9: {
        "category": "Handling Objections",
        "title": "9. Short Tenures (Stalse/NTT)",
        "tag": "PROJECTS",
        "bridge": "These were strategic, fast-paced contract projects brought in to unlock specific data architecture blocks.",
        "case": "Agile Sprints & Cross-Cloud Toolkit.",
        "followup": "I view these experiences highly positively because they allowed me to rapidly deploy systems across completely different cloud environments.",
        "match": "Frames short projects as intentional, high-impact consulting sprints rather than instability.",
        "growth": "DWA needs immediate solutions. Your experience executing rapid 4-month sprints means you deliver results without a long onboarding lag.",
        "bullets": [
            "At Stalse, I focused on GCP and BigQuery pipelines to clean up multi-country revenue data for ASICS.",
            "At NTT Data, I mastered AWS Athena and Glue pipelines to process banking loads for Itaú.",
            "Now, I am looking for a long-term challenge to implement this complete cross-cloud arsenal."
        ]
    },
    10: {
        "category": "Handling Objections",
        "title": "10. Why change fields now?",
        "tag": "EVOLUTION",
        "bridge": "I don't see it as changing fields. I am simply applying modern tools to classic governance problems.",
        "case": "Transition from Management Analytics to Data Engineering.",
        "followup": "Compliance is moving to the cloud. Teams that do not adapt their data pipelines will struggle to survive audits.",
        "match": "Positions you as a forward-thinking Professional who sits where risk management and data science meet.",
        "growth": "DWA is a modern tech brand. Hiring a traditional agent is a step backward; hiring a data-driven risk analyst is the future.",
        "bullets": [
            "Moving into Advanced Analytics allows me to protect company assets at a scale humans cannot match.",
            "I have spent my career tracking metrics and spotting process anomalies; compliance is the natural next step.",
            "I am positioning my engineering toolkit exactly where the future of risk management is heading."
        ]
    },
    11: {
        "category": "Core Cases (STAR)",
        "title": "11. ASICS (2026 - FinOps)",
        "tag": "CROSS-BORDER",
        "bridge": "I built a unified, cross-border financial data model across 3 (three) countries to secure international revenue tracking.",
        "case": "Stalse Project for ASICS Latam (Brazil, Chile, Colombia).",
        "followup": "We integrated multi-source data platforms into a single architecture, automating currency conversions and tax parameters.",
        "match": "Directly mirrors DWA's cross-border reality. Proves you can manage complex financial lines across regions.",
        "growth": "DWA sells globally. The logic I used to consolidate international revenue rules for ASICS is exactly what I will use to audit your sales.",
        "bullets": [
            "Situation: Fragmented regional data views created massive visibility risks and tracking anomalies for leadership.",
            "Action: I re-engineered the data architecture using BigQuery and automated daily loads using advanced SQL rules.",
            "Result: Slashed cloud data consumption from Gigabytes to Megabytes, optimizing performance and reducing query costs."
        ]
    },
    12: {
        "category": "Core Cases (STAR)",
        "title": "12. NTT DATA / Itaú (2025)",
        "tag": "SCALE-DATA",
        "bridge": "I engineered cloud data pipelines to deliver automated performance reporting for 5,000 (five thousand) executives.",
        "case": "Data Analyst at NTT Data for Itaú (AWS Cloud Environment).",
        "followup": "The project demanded absolute data consistency while handling high-volume tables with complex, evolving business rules.",
        "match": "Proves your technical capability to handle massive transaction volumes without system lag or data corruption.",
        "growth": "When DWA triggers thousands of daily checkout logs, you have the AWS background to ensure your audit queries don't break.",
        "bullets": [
            "Situation: The client needed to calculate executive metrics by joining tables with billions of rows of messy records.",
            "Action: I built complex database views and robust data transformations using Amazon Athena, S3, and AWS Glue.",
            "Result: Delivered an automated dashboard tool that processed massive scales with absolute data consistency."
        ]
    },
    13: {
        "category": "Core Cases (STAR)",
        "title": "13. Heineken (2023 - 2024)",
        "tag": "E-COMMERCE",
        "bridge": "I normalized chaotic e-commerce data streams across 200 (two hundred) distinct online digital products.",
        "case": "Sxpel Technologies allocated at Heineken (Digital Channel Analytics).",
        "followup": "I focused on cleaning up fragmented client inputs to build a transparent, auditable reporting pipeline for leadership.",
        "match": "Gives you zero learning curve regarding digital checkouts, sales funnels, and online platform metrics.",
        "growth": "DWA is an online infoproduct ecosystem. I already speak the language of checkouts, funnels, and digital accounts.",
        "bullets": [
            "Situation: Received fragmented spreadsheets from multiple clients in different formats, blocking commercial campaign tracking.",
            "Action: Designed a clean Star Schema relational model and built a unified performance dashboard inside Power BI.",
            "Result: Launched the first stable automation in less than 1 (one) month, matching financial indicators to the exact penny."
        ]
    },
    14: {
        "category": "Core Cases (STAR)",
        "title": "14. Afinz (2022 - 2023)",
        "tag": "OPTIMIZATION",
        "bridge": "I hate slow, manual, non-compliant workflows, so I build automated pipelines to protect speed and security.",
        "case": "MIS Analyst at Afinz / Sorocred.",
        "followup": "I also structured our metadata repositories and led governance meetings to ensure strict process adherence.",
        "match": "Proves an execution-focused mindset. Compliance teams thrive when they eliminate slow manual bottlenecks.",
        "growth": "DWA cannot afford an analyst who wastes hours on manual entries. You free up team time through technical optimization.",
        "bullets": [
            "Situation: Daily data reporting workflows were entirely manual, taking 1.5 (one and a half) hours and creating operational lags.",
            "Action: Developed automated ETL data pipelines using Python, SQL, and structured repositories.",
            "Result: Slashed processing time down to just 15 (fifteen) minutes while significantly strengthening the data quality framework."
        ]
    },
    15: {
        "category": "Core Cases (STAR)",
        "title": "15. Burity (Regulatory Base)",
        "tag": "LEGAL-AUDIT",
        "bridge": "I acted as a legal proxy managing high-value regulatory, contract, and operational risks with zero liabilities.",
        "case": "Asset & Property Manager at Burity Empresarial.",
        "followup": "I audited complex legal processes, agreements, and blueprints to rectify historical administrative errors.",
        "match": "Validates your foundational compliance mindset: reading rules, verifying contracts, and protecting corporate assets.",
        "growth": "Even in a digital company, the core philosophy of compliance remains the same: mitigating liability. You have years of proof.",
        "bullets": [
            "Situation: Managed complex negotiations involving multi-million dollar corporations and strict government registries.",
            "Action: Aligned internal legal and engineering teams to correct descriptive errors and execute land compliance steps.",
            "Result: Secured critical infrastructure expansions administratively, driving asset valuation up with zero lawsuits."
        ]
    },
    16: {
        "category": "Extreme Scenarios",
        "title": "16. Handling a Major Mistake",
        "tag": "MISTAKE-LOG",
        "bridge": "If a pipeline or business rule breaks, my immediate step is to isolate the anomaly and patch the system.",
        "case": "Data Quality and Traceability mindset.",
        "followup": "I believe in total transparency. I flag the issue, show the operational impact, and deploy the fix immediately.",
        "match": "Highlights executive maturity. You treat errors as structural engineering data points, not personal crises.",
        "growth": "In a fast startup, things will break. DWA needs an analyst who isolates bugs calmly and builds permanent code fixes.",
        "bullets": [
            "I take full ownership, check the transaction logs, and isolate exactly where the validation rule failed.",
            "I implement an automated data quality check layer to ensure that specific failure can never happen again.",
            "In my workflow, a production mistake is simply an clear indicator showing us where to upgrade our backend logic."
        ]
    },
    17: {
        "category": "Extreme Scenarios",
        "title": "17. Unmapped High-Pressure Task",
        "bridge": "Under extreme pressure with unmapped issues, I rely on structured frameworks, not emotional guessing.",
        "case": "Agile problem diagnosis.",
        "followup": "When a system blind spot appears, you isolate the parameters, review historical logs, and roll out a safe patch.",
        "match": "Demonstrates clear analytical focus and the ability to operate safely inside chaotic environments.",
        "growth": "Global digital sales face sudden updates (like payment gateway changes). You provide a steady, logical filter during high-pressure alerts.",
        "bullets": [
            "Step 1: I isolate the variables to see which core business or compliance rule is being threatened.",
            "Step 2: I pull historical transaction logs to support our decision criteria with evidence.",
            "Step 3: I deploy a calculated MVP solution and monitor the indicators in real-time."
        ]
    },
    18: {
        "category": "Extreme Scenarios",
        "title": "18. Conflict with Stakeholders",
        "bridge": "I do not fight with subjective opinions. I align conflicting teams by putting clear data on the table.",
        "case": "Strategic performance alignment with cross-functional teams.",
        "followup": "People usually push back because of underlying business anxieties. Once you show them the numbers, the noise stops.",
        "match": "Validates strong, non-combative communication skills, ensuring smooth relations between tech and legal departments.",
        "growth": "As compliance sets tighter rules, sales teams might push back. You use data to prove that compliance protects their bonuses.",
        "bullets": [
            "I start by listening to understand the core operational or financial concern the team is facing.",
            "I present clear, comparative data performance models to take emotional biases out of the conversation.",
            "Once the transactional numbers and compliance risks are visible, teams naturally arrive at the same logical path."
        ]
    },
    19: {
        "category": "Extreme Scenarios",
        "title": "19. Tech to Non-Tech",
        "bridge": "I translate complex backend data pipelines into clear financial metrics and corporate risk mitigation.",
        "case": "Executive reporting layers at Afinz and Heineken.",
        "followup": "Non-technical stakeholders don't need to hear about SQL query joins; they need to know if the company is legally safe.",
        "match": "Matches DWA's cross-functional reality. Proves you can speak smoothly to founders, lawyers, and marketing heads.",
        "growth": "Leadership at DWA needs rapid answers to protect the brand. You provide clean, bite-sized executive summaries.",
        "bullets": [
            "I never explain the query syntax. I explain the hour savings or the tax exposure we successfully eliminated.",
            "I use standard corporate metrics that leadership cares about, like cost optimization or processing time saved.",
            "I make compliance visually obvious through clean dashboards rather than talking about backend data engineering."
        ]
    },
    20: {
        "category": "Extreme Scenarios",
        "title": "20. Closing Statement / Final Approach",
        "tag": "CLOSING",
        "bridge": "To wrap up, I am not looking for a traditional, comfortable routine. I am here to build your automated compliance engine.",
        "case": "Perfect Elo Between André's Background & DWA's Moment.",
        "followup": "My goal is to combine my Engineering structure, my MBA business vision, and my Advanced SQL toolkit to protect your growth.",
        "match": "The ultimate strategic pitch. Ties your entire professional summary directly to DWA's core digital scaling needs.",
        "growth": "DWA is at a turning point: continuing with slow manual checkouts or automating data governance. I am the analyst for that automation.",
        "bullets": [
            "I bring cross-cloud experience (AWS/GCP) to a department that traditionally operates manually in Excel.",
            "I will ensure your checkout funnels experience zero friction, and your global sales face zero compliance risk.",
            "I am ready to secure your transaction pipelines long-term so DWA can focus on scaling its revenue safely."
        ]
    }
}

if "active_id" not in st.session_state:
    st.session_state.active_id = 1

with st.sidebar:
    st.markdown("### Workspace Reference")
    st.caption("• André Carvalho ENG.pdf")
    st.caption("• Academia de Riqueza Digital.pdf")
    
    st.markdown("### Match Analytics")
    st.metric(label="Interview Adherence Score", value="98%", delta="Elite Match")
    st.caption("**Target:** DWA · Trade Compliance Analyst")

categories_list = ["Core & Fit", "Handling Objections", "Core Cases (STAR)", "Extreme Scenarios"]
cols = st.columns(4)

for idx, cat_name in enumerate(categories_list):
    with cols[idx]:
        st.markdown(f'<div class="category-header">{cat_name}</div>', unsafe_allow_html=True)
        cat_items = {k: v for k, v in DATA_MAPPING.items() if v["category"] == cat_name}
        
        for item_id, item_data in cat_items.items():
            is_active = (st.session_state.active_id == item_id)
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
            <span style="color:#117a65; font-size:11px; font-weight:bold; text-transform:uppercase;">The Golden Bridge (Natural phrasing):</span><br>
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
        <div class="growth-box">
            <strong style="color:#d35400; text-transform:uppercase; font-size:10px;">The DWA Growth Link (The Strategic Approach):</strong><br>
            <p style="color:#ba4a00; margin-top:2px;">{active_data['growth']}</p>
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
    
    st.markdown(f"<p style='font-size:11.5px; margin-top:0.4rem; color:#7f8c8d;'><strong>Baseline Reference:</strong> {active_data['case']}</p>", unsafe_allow_html=True)

with col_out2:
    st.markdown("<p style='font-weight:bold; font-size:12px; color:#2c3e50; margin-bottom:0.3rem;'>Bulletproof Supporting Arguments:</p>", unsafe_allow_html=True)
    for bullet in active_data["bullets"]:
        st.markdown(f"<p style='font-size:12.5px; margin-bottom:5px !important;'>• {bullet}</p>", unsafe_allow_html=True)
