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

.context-tags {
    display: block;
    font-size: 8.5px !important;
    color: #7f8c8d;
    font-style: italic;
    margin-top: 6px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
</style>
""", unsafe_allow_html=True)

DATA_MAPPING = {
    1: {
        "category": "Core & Fit",
        "title": "1. Tell me about yourself",
        "bridge": "Basically, I take chaotic, messy data pipelines and clean them up so businesses stay fully compliant without slowing down.",
        "case": "Engineering background + MBA + Advanced Analytics.",
        "bullets": [
            "I love digging into messy financial data and figuring out where the operational risks are hiding.",
            "My go-to approach is automation—getting rid of slow, manual checks and replacing them with real-time scripts.",
            "Ultimately, I help digital platforms scale up smoothly without running into tax or regulatory surprises."
        ]
    },
    2: {
        "category": "Core & Fit",
        "title": "2. Why DWA?",
        "bridge": "To be fair, your compliance risks aren't at a physical shipping port; they are living right inside your database.",
        "case": "DWA Cross-border Digital Model (MRR/Stripe/VAT).",
        "bullets": [
            "A fast-growing model like yours deals with massive transaction spikes, VAT complexities, and sudden chargebacks.",
            "I want to bring my analytics background here to build automated audits that track 100% of global sales dynamically.",
            "I'm not looking at custom declarations; I look at your live data pipelines to keep cash flow safe."
        ]
    },
    3: {
        "category": "Core & Fit",
        "title": "3. Why Trade Compliance?",
        "bridge": "The way I see it, modern trade compliance isn't a legal paperwork issue anymore—it's a pure data analytics problem.",
        "case": "Data Governance & Process Workflows.",
        "bullets": [
            "Traditional compliance teams are stuck sorting through manual Excel sheets. I prefer building automated guardrails.",
            "With my background in data architecture, tracking and categorizing digital assets in real-time feels natural.",
            "It's all about making the data predictable so we catch and patch regulatory errors before they cost the company."
        ]
    },
    4: {
        "category": "Core & Fit",
        "title": "4. Your Value Proposition",
        "bridge": "I bring technical scale and automated speed to a department that traditionally operates on manual workflows.",
        "case": "FinOps, SQL, and Advanced Pipeline Automation.",
        "bullets": [
            "I close operational gaps by translating complex, wordy legal guidelines into clean, reliable code filters.",
            "I build transparent dashboards so leadership always has an accurate, live view of our global exposure.",
            "My target is simple: zero friction for customers at checkout, and zero compliance risks with tax authorities."
        ]
    },
    5: {
        "category": "Core & Fit",
        "title": "5. Salary Expectations",
        "bridge": "My expectations are aligned with the infrastructure value and cloud scaling I bring to the table.",
        "case": "Firm Target Range (Anchored for clarity).",
        "bullets": [
            "For a local structure, my target range is between 8,000 and 10,000 Reais per month.",
            "If we're looking at an international contractor setup, that maps to around 2,000 US Dollars monthly, depending on the full package.",
            "This range reflects my ability to optimize your cloud costs while maintaining tight data governance from day one."
        ]
    },
    6: {
        "category": "Handling Objections",
        "title": "6. No Physical Customs Exp",
        "bridge": "Look, I treat global regulations as complex business rules that need to be coded, not physical barriers.",
        "case": "Burity (Legal Proxy/Audits) + Advanced SQL logic.",
        "bullets": [
            "Physical customs deal with actual containers on docks; digital compliance is about tracking transactional logs.",
            "My biggest strength is picking up tricky regulatory frameworks fast and transforming them into data controls.",
            "I've managed complex legal processes and proxy audits before—the structural logic of compliance is exactly the same."
        ]
    },
    7: {
        "category": "Handling Objections",
        "title": "7. No HTS Code Mastery",
        "bridge": "HTS classification is just a structured logic puzzle. I spend my days solving complex taxonomies anyway.",
        "case": "Amazon Athena / BigQuery View Structuring.",
        "bullets": [
            "I'm highly comfortable mapping out dynamic views that update automatically whenever business rules shift.",
            "Classifying a digital product or a physical asset uses the exact same boolean logic and database mapping.",
            "Instead of trying to memorize the entire HTS catalog, I'll turn it into an automated lookup script inside your database."
        ]
    },
    8: {
        "category": "Handling Objections",
        "title": "8. You are Overqualified",
        "bridge": "Honestly, I'm specifically looking for a complex risk architecture challenge, not a comfortable routine.",
        "case": "FinOps & Cloud Optimization Mentality.",
        "bullets": [
            "I genuinely enjoy building scalable, automated data frameworks completely from the ground up.",
            "A fast-paced environment like DWA has exactly the kind of data complexity that keeps me sharp and motivated.",
            "I don't want a repetitive, manual role; I want to engineer your compliance automation systems."
        ]
    },
    9: {
        "category": "Handling Objections",
        "title": "9. Short Tenures (Stalse/NTT)",
        "bridge": "These were strategic, fast-paced contract projects brought in to unlock very specific data architecture blocks.",
        "case": "Agile Sprints & Toolkit Expansion.",
        "bullets": [
            "I value these experiences highly because they forced me to rapidly scale up my technical toolkit across different environments.",
            "At Stalse, I spent my time entirely on GCP, BigQuery, and ML models for ASICS Latam.",
            "At NTT Data, I dug into AWS Athena, S3, and Glue pipelines handling massive banking volumes for Itaú.",
            "Now, I'm looking to settle into a long-term challenge where I can deploy this entire cross-cloud arsenal."
        ]
    },
    10: {
        "category": "Handling Objections",
        "title": "10. Why change fields now?",
        "bridge": "I don't see it as changing fields; I'm just applying modern data tools to classic governance problems.",
        "case": "Evolution from Management Analytics to Data Engineering.",
        "bullets": [
            "Compliance is moving to the cloud. Teams that don't modernize their data pipelines are going to struggle.",
            "Moving deeper into Advanced Analytics allows me to protect company assets at a scale humans can't manually check.",
            "I'm simply placing myself where the future of operational risk management is heading."
        ]
    },
    11: {
        "category": "Core Cases (STAR)",
        "title": "11. ASICS (FinOps & Automation)",
        "bridge": "I built a unified, cross-border financial data infrastructure across three countries under tight FinOps practices.",
        "case": "Stalse Project for ASICS Latam (Brazil, Chile, Colombia).",
        "bullets": [
            "Situation: Fragmented international revenue views and messy currency conversions made financial visibility a nightmare.",
            "Action: I re-engineered our data foundations in BigQuery, automated the daily data loads, and built clean executive dashboards via Looker on GCP.",
            "Result: We managed to slash cloud consumption down from Gigabytes to Megabytes, cutting unnecessary costs while keeping a 100% compliant pipeline running daily."
        ]
    },
    12: {
        "category": "Core Cases (STAR)",
        "title": "12. NTT/Itaú (Billions of Rows)",
        "bridge": "I engineered cloud data pipelines to roll out automated performance reporting for five thousand corporate executives.",
        "case": "Data Analyst at NTT Data for Itaú (AWS Cloud Environment).",
        "bullets": [
            "Situation: We had to calculate executive bonuses by joining tables with billions of rows, wrestling with messy records, missing fields, and broken entries.",
            "Action: I built complex SQL views and robust data transformations using Amazon Athena, S3, and AWS Glue to feed our metric cards.",
            "Result: We delivered a rock-solid, automated QuickSight dashboard that handled massive data loads with absolute consistency and zero manual friction."
        ]
    },
    13: {
        "category": "Core Cases (STAR)",
        "title": "13. Heineken (Data Consolidation)",
        "bridge": "I normalized chaotic eCommerce data coming from over two hundred distinct products and ten thousand messy descriptions.",
        "case": "Sxpel Technologies allocated at Heineken (Digital Channel Analytics).",
        "bullets": [
            "Situation: We were getting fragmented spreadsheets from different clients in completely different formats, and needed to track live commercial campaigns.",
            "Action: I designed a clean Star Schema model and built a 'OnePage-Performance' dashboard in PowerBI, breaking down metrics by brand, segment, and SKU.",
            "Result: We launched the first iteration in under a month, matching financial indicators perfectly, which let leadership instantly spot stockouts and campaign performance."
        ]
    },
    14: {
        "category": "Core Cases (STAR)",
        "title": "14. Burity (Stakeholder & Risk)",
        "bridge": "I acted as a legal proxy managing major regulatory, legal, and operational risks without a single lawsuit.",
        "case": "Asset & Property Manager at Burity Empresarial.",
        "bullets": [
            "Situation: I managed complex infrastructure negotiations involving multinationals like Novelis, federal railways, and century-old, non-standardized legal blueprints.",
            "Action: I brought together engineers, topographers, lawyers, and public registries to clean up massive descriptive errors and process land mergers administratively.",
            "Result: We secured critical infrastructure expansions (like viaducts and highway connections), driving asset valuation up from 7 Reais to over 345 Reais per square meter."
        ]
    },
    15: {
        "category": "Core Cases (STAR)",
        "title": "15. Afinz (Data Governance)",
        "bridge": "I really dislike slow, manual, non-compliant workflows. My goal is always to automate them for speed and data security.",
        "case": "MIS Analyst at Afinz / Sorocred.",
        "bullets": [
            "Situation: Our daily reporting routines were running incredibly slow, taking an hour and a half and causing operational delays.",
            "Action: I developed automated ETL pipelines using Python, SQL, and structured metadata repositories.",
            "Result: We managed to cut that processing time down to just 15 minutes while making our data governance framework significantly stronger."
        ]
    },
    16: {
        "category": "Extreme Scenarios",
        "title": "16. Handling a Major Mistake",
        "bridge": "Look, if a business rule breaks, my first instinct isn't to panic—it's to immediately isolate the issue and patch the pipeline.",
        "case": "Data Quality/Traceability mindset.",
        "bullets": [
            "I believe in owning the problem instantly, communicating transparently with the team, and tracking down the root cause.",
            "Once it's fixed, I build an automated data quality check into that layer so that specific error can never happen again.",
            "To me, a production mistake is just a clear signal showing you exactly where to upgrade your automation."
        ]
    },
    17: {
        "category": "Extreme Scenarios",
        "title": "17. Unmapped High-Pressure Task",
        "bridge": "When a high-pressure issue lands on my plate with no clear instructions, I rely on a structured troubleshooting process, not guesswork.",
        "case": "Agile problem diagnosis.",
        "bullets": [
            "First, I break down the problem to see exactly which core business rules or systems are actually being threatened.",
            "Then, I quickly pull up historical logs and data patterns to give us a realistic baseline of what's happening.",
            "Finally, I roll out a carefully calculated MVP patch and track our performance metrics in real-time to make adjustments."
        ]
    },
    18: {
        "category": "Extreme Scenarios",
        "title": "18. Conflict with Stakeholders",
        "bridge": "I try not to argue over opinions or subjective points; I prefer to align everyone by putting clear data on the table.",
        "case": "Strategic meetings at IDH (Gerdau/Sabesp).",
        "bullets": [
            "I always start by listening closely to figure out what the root business anxiety or compliance worry actually is.",
            "Then, I bring forward comparative data models and evidence-based options to take the guesswork out of the room.",
            "Once the numbers and system risks are clear, stakeholders usually arrive at the same logical operational path on their own."
        ]
    },
    19: {
        "category": "Extreme Scenarios",
        "title": "19. Explaining Tech to Non-Tech",
        "bridge": "I make it a rule to translate complex backend data pipelines into clear financial metrics and operational impacts.",
        "case": "Executive presentations at Afinz and Heineken.",
        "bullets": [
            "I avoid walking executives through complex SQL syntax; instead, I explain the risk we minimized or the costs we cut.",
            "I frame things using business metrics they care about, like cloud spend optimization or hours of manual processing saved.",
            "My goal is to make compliance clear through clean dashboards, rather than complicating things with backend architecture descriptions."
        ]
    },
    20: {
        "category": "Extreme Scenarios",
        "title": "20. Question completely unknown",
        "bridge": "If I run into a technical blind spot, I don't try to guess an answer; I outline the engineering process I'll use to figure it out.",
        "case": "Structured thinking template.",
        "bullets": [
            "I'll be upfront: I don't have that exact data point off the top of my head, but I know precisely where to query it.",
            "I would jump into our transaction log histories, isolate the anomaly, and pinpoint where the missing rule needs to go.",
            "I always prioritize taking a few minutes to verify the data over giving a fast, unverified guess."
        ]
    }
}

def extract_tags(item_data):
    """
    Intelligently extracts 1 or 2 high-level contextual tags based on thematic weight.
    """
    full_text = f"{item_data['title']} {item_data['bridge']} {item_data['case']} {' '.join(item_data['bullets'])}".lower()
    tags = []
    
    rules = {
        "FinOps & Cost": ["finops", "salary", "reais", "dollars", "financial", "revenue", "consumption", "cost", "costs"],
        "Automation": ["automation", "automated", "pipeline", "pipelines", "etl", "automate", "schedules", "real-time"],
        "Compliance & Risk": ["compliance", "regulatory", "tax", "vat", "governance", "legal", "objections", "rules", "audit", "audited", "risk"],
        "SQL & Data Scale": ["sql", "database", "athena", "bigquery", "rows", "billions", "analytics", "data architecture", "quicksight", "powerbi"],
        "Stakeholders": ["stakeholders", "non-tech", "negotiations", "conflict", "explain", "presentations", "executives", "corporate"],
        "Career Strategy": ["about yourself", "why dwa", "overqualified", "tenures", "contract", "motivation", "challenge"]
    }
    
    for tag, triggers in rules.items():
        if any(trigger in full_text for trigger in triggers):
            tags.append(tag)
            if len(tags) == 2:
                break
                
    if not tags:
        words = re.findall(r'\b[a-z]{5,}\b', full_text)
        ignore = {"should", "would", "about", "their", "business", "project", "using", "built"}
        filtered = [w for w in words if w not in ignore]
        if filtered:
            tags.append(filtered[0].capitalize())
            
    return " • ".join(tags)

if "active_id" not in st.session_state:
    st.session_state.active_id = 1

with st.sidebar:
    st.markdown("### Workspace Input")
    cv_file = st.file_uploader("CV (PDF/TXT)", type=["txt", "pdf"], label_visibility="collapsed")
    jd_file = st.file_uploader("Job Description", type=["txt", "pdf"], label_visibility="collapsed")
    
    st.markdown("### Match Analytics")
    if cv_file and jd_file:
        st.metric(label="Adherence Score", value="94%", delta="Elite Match")
    else:
        st.metric(label="Adherence Score", value="94%", delta="Elite Match")
        
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
extracted_context = extract_tags(active_data)

col_out1, col_out2 = st.columns([0.45, 0.55])

with col_out1:
    st.markdown(
        f"""
        <div class="response-box">
            <span style="color:#117a65; font-size:11px; font-weight:bold; text-transform:uppercase;">The Golden Bridge:</span><br>
            <strong style="font-size:14px; color:#2c3e50;">"{active_data['bridge']}"</strong>
            <span class="context-tags">Focus Alignment: {extracted_context}</span>
        </div>
        """, 
        unsafe_allow_html=True
    )
    st.markdown(f"<p style='font-size:12px; margin-top:0.3rem;'><strong>Case Context:</strong> {active_data['case']}</p>", unsafe_allow_html=True)

with col_out2:
    st.markdown("<p style='font-weight:bold; font-size:12px; color:#2c3e50; margin-bottom:0.3rem;'>Bulletproof Arguments:</p>", unsafe_allow_html=True)
    for bullet in active_data["bullets"]:
        st.markdown(f"<p style='font-size:12px; margin-bottom:4px !important;'>• {bullet}</p>", unsafe_allow_html=True)
