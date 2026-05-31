import streamlit as st
import re

st.set_page_config(
    page_title="War Room - DWA",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Fluid & Non-Overlapping UX Injection
st.markdown("""
<style>
/* Reset main padding limits to prevent overlapping headers */
.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 0.5rem !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
    max-width: 100% !important;
}

/* Global scrollbar behavior control for clean hardware feel */
::-webkit-scrollbar {
    display: none !important;
}

div[data-testid="stVerticalBlock"] {
    gap: 0.25rem !important;
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

/* Force every single column button wrapper to have exact uniform heights and padding */
div.stButton > button {
    width: 100% !important;
    height: 44px !important; /* Uniform button blocks */
    white-space: normal !important; /* Forces multi-line wrap if text is long */
    word-break: keep-all !important;
    overflow: hidden !important;
    font-size: 10px !important;
    line-height: 1.15 !important;
    padding: 0.3rem 0.3rem !important;
    text-align: center !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    border-radius: 5px !important;
    margin-bottom: 4px !important;
}

.category-header {
    font-size: 11px !important;
    font-weight: bold !important;
    color: #2c3e50;
    border-bottom: 2px solid #e9ecef;
    padding-bottom: 3px;
    margin-bottom: 0.4rem !important;
    text-transform: uppercase;
    letter-spacing: 0.3px;
}

/* Output Display Blocks - Engineered for Clear Single-Page Layout Reading */
.response-box {
    background-color: #e8f8f5;
    border-left: 4px solid #18bc9c;
    padding: 8px 10px !important;
    border-radius: 4px;
    margin-bottom: 0.4rem;
    min-height: 65px;
}

.followup-box {
    background-color: #f4f6f7;
    border-left: 4px solid #34495e;
    padding: 8px 10px !important;
    border-radius: 4px;
    margin-bottom: 0.4rem;
    min-height: 65px;
}

.growth-box {
    background-color: #fef9e7;
    border-left: 4px solid #f39c12;
    padding: 6px 10px !important;
    border-radius: 4px;
    margin-bottom: 0.4rem;
    min-height: 55px;
}

.match-box {
    background-color: #ebf5fb;
    border-left: 4px solid #3498db;
    padding: 6px 10px !important;
    border-radius: 4px;
    margin-bottom: 0.4rem;
    min-height: 55px;
}

.bullet-container-box {
    background-color: #ffffff;
    border: 1px solid #e9ecef;
    border-radius: 4px;
    padding: 10px !important;
    min-height: 250px;
}

.qa-container-box {
    background-color: #fdfefe;
    border: 1px solid #d5dbdb;
    border-radius: 4px;
    padding: 10px !important;
    margin-top: 8px;
    min-height: 280px;
}

.qa-item {
    margin-bottom: 8px !important;
    padding-bottom: 6px;
    border-bottom: 1px dashed #eaeded;
}
.qa-item:last-child {
    border-bottom: none;
    margin-bottom: 0px !important;
}
</style>
""", unsafe_allow_html=True)

# 20 Strategic Framework Database Items - Refactored with 60 C-Level Q&A Scenarios
DATA_MAPPING = {
    1: {
        "category": "WHAT - Capabilities & Profile",
        "title": "Tell me about yourself",
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
        ],
        "qa_responses": [
            {"q": "How does an Engineering & MBA background apply to Trade Compliance?", "a": "Compliance in an online business is a process optimization and risk mitigation challenge. Engineering gives me the logic to build automated validation systems, while the MBA provides the financial and strategic overview to ensure these rules protect revenue instead of creating friction."},
            {"q": "Why should we hire a data specialist instead of a traditional customs agent?", "a": "DWA doesn't move heavy physical containers through maritime customs; you move transaction bytes globally via checkout. A traditional agent reviews paperwork post-factum. I build immediate backend filters to audit 100% of logs as they hit your database."},
            {"q": "What is your main professional driver in this domain?", "a": "I am driven by turning high-velocity operational chaos into structured, compliant frameworks. I enjoy setting up systems that give founders and leadership total peace of mind regarding regulatory exposures."}
        ]
    },
    2: {
        "category": "WHY - Intent & Fit",
        "title": "Why DWA?",
        "tag": "STRATEGY",
        "bridge": "Your main compliance risks are not waiting at a physical shipping dock. They are living inside your live checkout database.",
        "followup": "When a digital brand scales cross-border via Stripe, the real bottlenecks are digital tax lines and payment gateway holds.",
        "match": "Proves you understand their exact digital business model (MRR/Infoproducts) better than traditional candidates.",
        "growth": "DWA operates globally with high velocity; they need a data expert who secures cash flow, not a traditional logistics agent.",
        "case": "DWA Cross-border Digital Model (MRR/Stripe/VAT).",
        "bullets": [
            "Operating across multiple regions means managing complex checkout rules and European VAT lines instantly.",
            "I want to apply my SQL toolkit to audit 100% (one hundred percent) of transaction logs automatically.",
            "My focus is protecting your digital checkout funnel from sudden international regulatory blocks."
        ],
        "qa_responses": [
            {"q": "What specific risk do you see in our digital cross-border model?", "a": "With high transaction volumes across multiple borders, your biggest threats are international tax mismatching (like European VAT logic) and sudden payment processor holds due to pattern irregularities. Both stop cash flow instantly."},
            {"q": "How do you plan to help DWA scale?", "a": "By embedding automated validation scripts directly inside the data flow. As volume scales 10x, a manual team fractures. An automated pipeline processes millions of logs with the same processing speed and zero human errors."},
            {"q": "You come from massive brands like Heineken and Itaú. Why join our ecosystem?", "a": "Large corporate environments are great for mastering governance at scale, but their structures move slowly. DWA has the velocity, agility, and modern tech-first mindset where my optimization scripts can generate real impact from week one."}
        ]
    },
    3: {
        "category": "WHY - Intent & Fit",
        "title": "Why Trade Compliance?",
        "tag": "COMPLIANCE",
        "bridge": "Modern trade compliance is no longer a legal paperwork task. It is a pure data analytics problem.",
        "followup": "Digital assets and global checkouts follow logical boolean rules. If your data views are broken, your compliance fails.",
        "match": "Turns a lack of legacy customs experience into a modern technical advantage for a cloud-first company.",
        "case": "Data Governance & Process Workflows.",
        "bullets": [
            "Traditional customs analysts check papers one by one. I build automated codes to audit data in bulk.",
            "My experience with data frameworks allows me to track and categorize digital transactions in real time.",
            "I ensure operational compliance is embedded directly into the code pipeline to prevent penalties."
        ],
        "qa_responses": [
            {"q": "If you are a BI Analyst, why pivot into Compliance?", "a": "I don't see it as a pivot, but as the natural evolution of Data Governance. BI visualizes the business; Compliance protects it. Applying advanced SQL data engineering to isolate regulatory anomalies is the most high-impact way to use analytics today."},
            {"q": "What does compliance mean to you from an operational perspective?", "a": "It means predictability. A compliant company faces no unexpected cross-border holds, no sudden fines, and no platform suspensions. It means the system architecture mirrors local and international tax laws perfectly."},
            {"q": "How do you handle complex, shifting international rules?", "a": "I treat them as dynamic parameter updates inside a database. Instead of hardcoding rules, I build configurable views that allow us to tweak tax or structural parameters instantly when international legal updates occur."}
        ]
    },
    4: {
        "category": "WHAT - Capabilities & Profile",
        "title": "Your Value Proposition",
        "tag": "VALUE",
        "bridge": "I bring technical scale and pipeline automation to a department that traditionally works with manual tools.",
        "followup": "I bridge the gap between complex legal regulations and hard database rules, removing human error completely.",
        "match": "Directly links your analytics expertise to their immediate need for lean, automated operations.",
        "case": "FinOps, SQL, and Advanced Pipeline Automation.",
        "bullets": [
            "I translate wordy regulatory updates into clean automated database filters.",
            "I build transparent dashboards that give leadership a live, 100% (one hundred percent) reliable view of risk.",
            "My target is zero friction at the checkout page and zero compliance risk with international tax authorities."
        ],
        "qa_responses": [
            {"q": "What is your immediate 30-day value add if hired?", "a": "Map out your transactional log streams, identify any manual reporting dependencies (like manual Excel updates), and optimize those workflows into clean SQL automated views to ensure total financial and regulatory data integrity."},
            {"q": "How do you balance compliance restrictions with a growth-focused sales pipeline?", "a": "Compliance shouldn't block the funnel; it must act as an invisible guardrail. By using real-time automated scripts instead of slow human reviews, we ensure legitimate sales go through instantly while high-risk anomalies are isolated behind the scenes."},
            {"q": "What distinguishes your approach to data documentation?", "a": "I follow strict documentation standards using tools like Confluence. I believe a data workflow is only complete when its metadata is fully mapped, allowing any internal stakeholder to audit the operational logic effortlessly."}
        ]
    },
    5: {
        "category": "WHY - Intent & Fit",
        "title": "Salary Expectations",
        "tag": "ANCHOR",
        "bridge": "My financial target is based on the data infrastructure scale and cost savings I can deliver.",
        "case": "Firm Target Range (Clear numbers written out).",
        "followup": "I anchor my rate based on my ability to optimize cloud spend and secure global financial pipelines from day one.",
        "match": "Establishes a transparent, business-driven value alignment without awkward verbal gaps.",
        "growth": "Protects their bottom line. A data-driven approach means your salary is offset by systemic optimization.",
        "bullets": [
            "For a local structure, my target is between 8,000 (eight thousand) and 10,000 (ten thousand) Reais per month.",
            "For an international contractor setup, that maps directly to 2,000 (two thousand) US Dollars per month.",
            "This range reflects a professional who actively implements FinOps and automated data governance layers."
        ],
        "qa_responses": [
            {"q": "Is this number negotiable depending on the benefits package?", "a": "Yes, I am completely open to discussing the overall contract architecture, especially if there is alignment on long-term project growth, remote flexibility, and performance impact metrics."},
            {"q": "Why should we invest this budget in your profile over a junior analyst?", "a": "A junior analyst will maintain your manual routines and spreadsheets. My profile pays for itself by implementing FinOps optimizations that slash processing costs—just like I did at ASICS—and preventing costly revenue blocks from international authorities."},
            {"q": "Are you comfortable with an international B2B contractor arrangement?", "a": "Absolutely. I operate with professional systems and my setup is engineered for seamless cross-border remote integration, which perfectly fits DWA's global operating model."}
        ]
    },
    6: {
        "category": "WHAT - Capabilities & Profile",
        "title": "No Physical Customs Exp",
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
        ],
        "qa_responses": [
            {"q": "The job description emphasizes customs brokerage experience. How do you close that gap?", "a": "Customs brokerage is about verifying if items match legal codes and tax brackets. In the digital space, instead of reading physical manifests, I write SQL routines to check if purchase logs match target international tax regions. The asset changes, the core logic doesn't."},
            {"q": "How can we be sure you understand international regulatory frameworks?", "a": "During my tenure at Burity, I managed complex legal processes, audited corporate property registries, and acted as a legal proxy. I am deeply trained in reading strict legal text and translating it into hard operational workflows."},
            {"q": "What happens if we need to deal with a traditional customs inquiry?", "a": "My engineering approach means that every transaction is documented with clean data traceability. If an international auditor requests a review, we don't scramble through Excel sheets; we pull a flawless, structured database report instantly."}
        ]
    },
    7: {
        "category": "WHAT - Capabilities & Profile",
        "title": "No HTS Code Mastery",
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
        ],
        "qa_responses": [
            {"q": "How would you handle classifying a complex new infoproduct line using HTS?", "a": "I would treat the HTS taxonomy as a relational lookup table. By mapping our internal digital inventory metadata against the official classification matrix via automated scripts, we ensure instantaneous, programmatic categorization instead of manual guessing."},
            {"q": "What is the danger of relying on manual product classification?", "a": "Manual entry introduces human error, which triggers tax mismatches, transaction friction, and compliance audits. Automation guarantees that once a business rule is validated, it applies uniformly across thousands of global daily sales."},
            {"q": "Have you worked with complex taxonomies before?", "a": "Yes. At Heineken, I consolidated and normalized fragmented data across 200 distinct digital products and multiple channels. I am highly accustomed to organizing messy product data into strict, auditable structures."}
        ]
    },
    8: {
        "category": "WHY - Intent & Fit",
        "title": "You are Overqualified",
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
        ],
        "qa_responses": [
            {"q": "Your resume contains Machine Learning and Cloud Engineering. Won't you find this role boring?", "a": "It would only be boring if I performed it manually. Using my advanced toolkit to automate a fast-growing digital compliance engine from scratch is an intellectual challenge that standard, static corporations simply cannot offer."},
            {"q": "What keeps a professional like you loyal to a company?", "a": "Autonomy to optimize processes and systemic complexity. As long as DWA continues expanding its global footprint, new data volumes, cross-border tax hurdles, and system integrations will appear. That technical challenge keeps me highly engaged."},
            {"q": "How does your senior expertise benefit a lean team?", "a": "It prevents tech debt. A junior profile builds short-sighted sheets that break next month. I engineer clean data foundations and documented pipelines that will support DWA's transaction scaling for years without needing a system redesign."}
        ]
    },
    9: {
        "category": "WHAT - Capabilities & Profile",
        "title": "Short Tenures (Stalse/NTT)",
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
        ],
        "qa_responses": [
            {"q": "Why did you stay only 4 months at Stalse and NTT Data?", "a": "Both were structured as high-impact, temporary consulting contracts designed to solve a specific engineering bottleneck. Once the pipelines were automated, the dashboards launched, and documentation completed, the project concluded successfully."},
            {"q": "Are you looking for a long-term home or another short contract?", "a": "I am specifically looking for a permanent, long-term remote opportunity where I can embed myself into the core culture and continuously protect the operation as the brand scales internationally."},
            {"q": "How does jumping across different projects help DWA?", "a": "It has hyper-accelerated my tech adaptability. In under a year, I engineered systems in GCP/BigQuery for ASICS and immediately shifted to AWS/Athena for Itaú. I can adapt to whatever tech stack DWA runs with zero friction."}
        ]
    },
    10: {
        "category": "WHY - Intent & Fit",
        "title": "Why change fields now?",
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
        ],
        "qa_responses": [
            {"q": "Why not stick to classic Business Intelligence roles?", "a": "Classic BI tells you what happened in the past. Modern Risk Compliance uses the exact same data to actively protect the firm's current checkout capability and future expansion. It is a much more strategic, high-stakes application of my skills."},
            {"q": "What part of your analytical mindset applies best to risk tracking?", "a": "Anomaly detection. My background allows me to glance at thousands of log outputs, instantly spot an integration gap or an incorrect country tax calculation, and deploy a permanent programmatic correction before it causes damage."},
            {"q": "How do you view the future of digital trade regulation?", "a": "Governments are becoming highly sophisticated at auditing digital products. The companies that survive are those that treat compliance as a live data pipeline rather than a year-end accounting task. I bring that exact future-proof model to DWA."}
        ]
    },
    11: {
        "category": "HOW - Case Methodology (STAR)",
        "title": "ASICS (2026 - FinOps)",
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
        ],
        "qa_responses": [
            {"q": "How did you handle currency conversions and cross-border data mismatches for ASICS?", "a": "I engineered an automated ETL pipeline inside BigQuery that ingested local transaction streams, applied dynamic currency conversion lookup layers, and standardized regional tax definitions into a single, unified view for management."},
            {"q": "What was the direct business impact of your FinOps optimization at ASICS?", "a": "By optimizing query syntax and refactoring legacy data tables, I reduced processing loads from Gigabytes to Megabytes. This didn't just maximize processing speed; it directly optimized cloud infrastructure spend and prevented system lag."},
            {"q": "How does this ASICS experience help you protect DWA's checkout streams?", "a": "The exact logical engine I used to align Latin American regional revenue rules is what I will use to ingest DWA's cross-border Stripe or processor logs, guaranteeing that our automated dashboard matches regional tax laws perfectly."}
        ]
    },
    12: {
        "category": "HOW - Case Methodology (STAR)",
        "title": "NTT DATA / Itaú (2025)",
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
        ],
        "qa_responses": [
            {"q": "How did you maintain data integrity while handling tables with billions of rows?", "a": "By leveraging partition strategies in Amazon S3, designing optimized schemas, and building highly structured SQL views in Amazon Athena. This ensured that even under massive volume scales, our data transformations never suffered corruption."},
            {"q": "What did you do when the business rules evolved during the project?", "a": "Instead of hardcoding rules into static scripts, I built dynamic, parameter-driven SQL views. When business indicators or rules shifted, we updated the configuration tables, and the entire historical database adapted instantly without downtime."},
            {"q": "Why is your experience with AWS critical for DWA?", "a": "Online platforms process real-time events. My familiarity with backend cloud architectures like S3 and Athena means I can easily interface with your technical data ecosystem to pull, analyze, and secure raw transactional data cleanly."}
        ]
    },
    13: {
        "category": "HOW - Case Methodology (STAR)",
        "title": "Heineken (2023 - 2024)",
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
        ],
        "qa_responses": [
            {"q": "How do you handle messy, unstructured e-commerce data from multiple clients?", "a": "At Heineken, I designed a rigid Star Schema data model that forced all incoming data into a standardized relational mapping. This eliminated anomalies and insured that messy, disparate formats translated into clean, standardized metrics."},
            {"q": "What does 'matching indicators to the exact penny' mean for compliance?", "a": "It means total audirability. If an e-commerce platform has unexplained micro-discrepancies between its checkout logs and bank deposits, it creates immediate financial and compliance risk. I specialize in building data verification loops that eliminate these gaps."},
            {"q": "How does your digital market experience translate to DWA's infoproducts?", "a": "I already speak the language of e-commerce, digital checkouts, funnels, and customer segments. I don't need to be trained on what an online funnel look like; I can dive directly into auditing your product categories and sales data from day one."}
        ]
    },
    14: {
        "category": "HOW - Case Methodology (STAR)",
        "title": "Afinz (2022 - 2023)",
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
        ],
        "qa_responses": [
            {"q": "How did you reduce a reporting workflow from 1.5 hours to 15 minutes?", "a": "By auditing the legacy routine, identifying repetitive human manual tasks, and rewriting the entire ingestion sequence into automated Python and SQL data pipelines. The system handled the heavy lifting, leaving humans to focus purely on anomaly analysis."},
            {"q": "What was your approach to Data Governance at Afinz?", "a": "I structured metadata repositories and clear documentation models inside Confluence and SharePoint. This ensured that all definition metrics and data sources were fully governed, transparent, and aligned with internal process frameworks."},
            {"q": "How will your passion for automation optimize DWA's compliance arm?", "a": "I will target any manual data gathering or Excel compilation inside your compliance routines and replace them with automated data extractions. This minimizes compliance overhead, removes human delay, and provides immediate data feedback loops."}
        ]
    },
    15: {
        "category": "HOW - Case Methodology (STAR)",
        "title": "Burity (Regulatory Base)",
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
        ],
        "qa_responses": [
            {"q": "How does real estate legal proxy experience translate to digital trade compliance?", "a": "The essence of compliance never changes: it is about risk mitigation, textual precision, and strict adherence to institutional rules. Auditing land registries and managing regulatory compliance at Burity trained my eye to ensure everything is aligned with legal frameworks."},
            {"q": "Can you give an example of rectifying an administrative error?", "a": "At Burity, I audited historical technical blueprints and legal agreements to isolate descriptive errors that created major regulatory liabilities. By coordinating legal and operations teams, we rectified those records before any government penalties arose."},
            {"q": "How do you handle interactions with strict government regulatory frameworks?", "a": "With absolute data preparation and zero speculation. My extensive tenure managing property compliance taught me that regulators respond to indisputable, fully documented evidence. I apply that exact precision to digital transaction audits."}
        ]
    },
    16: {
        "category": "WHEN - Extreme Scenarios & Crisis",
        "title": "Handling a Major Mistake",
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
        ],
        "qa_responses": [
            {"q": "What is your immediate reaction when a critical data error is uncovered?", "a": "I immediately suppress emotional noise, isolate the affected transaction range using database logs, and establish a containment filter. Panic solves nothing; data tracing isolates the root breakdown instantly."},
            {"q": "How do you communicate an internal mistake to C-Level stakeholders?", "a": "With complete transparency and an immediate solution. I never present a problem without a documented root-cause breakdown, the quantified impact, and a ready-to-deploy patch that prevents that vulnerability from ever repeating."},
            {"q": "Can you give an example of how you build permanent fixes?", "a": "Every time a processing rule fails, I write a data quality check step directly into the pipeline. If an anomalous transaction payload hits us again, the system automatically routes it to an isolation log for review rather than letting it corrupt our main compliance view."}
        ]
    },
    17: {
        "category": "WHEN - Extreme Scenarios & Crisis",
        "title": "Unmapped High-Pressure Task",
        "tag": "CONTEXT",
        "bridge": "Under extreme pressure with unmapped issues, I rely on structured frameworks, not emotional guessing.",
        "case": "Agile problem diagnosis.",
        "followup": "When a system blind spot appears, you isolate the parameters, review historical logs, and roll out a safe patch.",
        "match": "Demonstrates clear analytical focus and the ability to operate safely inside chaotic environments.",
        "growth": "Global digital sales face sudden updates (like payment gateway changes). You provide a steady, logical filter during high-pressure alerts.",
        "bullets": [
            "Step 1: I isolate the variables to see which core business or compliance rule is being threatened.",
            "Step 2: I pull historical transaction logs to support our decision criteria with evidence.",
            "Step 3: I deploy a calculated MVP solution and monitor the indicators in real-time."
        ],
        "qa_responses": [
            {"q": "How do you start solving a compliance crisis you have never encountered before?", "a": "I break it down into an engineering problem. Step one is isolating the active parameters to understand where the system boundary failed. Step two is parsing recent transaction logs to quantify our exposure. Step three is applying a fast, auditable rule adjustment."},
            {"q": "How do you maintain performance speed under extreme startup pressure?", "a": "By relying on structured agile frameworks. Pressure is mitigated when you work based on data evidence rather than subjective guessing. I let my queries and data tracking establish the path forward."},
            {"q": "What happens if you lack the immediate information to make a critical compliance decision?", "a": "I rapidly extract an exploratory sample from the database via SQL, perform an accelerated pattern analysis, and present a data-backed risk assessment to leadership so we can make an informed, calculated business decision."}
        ]
    },
    18: {
        "category": "WHEN - Extreme Scenarios & Crisis",
        "title": "Conflict with Stakeholders",
        "tag": "CONTEXT",
        "bridge": "I do not fight with subjective opinions. I align conflicting teams by putting hard data criteria on the table.",
        "case": "Strategic performance alignment with cross-functional teams.",
        "followup": "People usually push back because of underlying business anxieties. Once you show them the numbers, the noise stops.",
        "match": "Validates strong, non-combative communication skills, ensuring smooth relations between tech and legal departments.",
        "growth": "As compliance sets tighter rules, sales teams might push back. You use data to prove that compliance protects their bonuses.",
        "bullets": [
            "I start by listening to understand the core operational or financial concern the team is facing.",
            "I present clear, comparative data performance models to take emotional biases out of the conversation.",
            "Once the transactional numbers and compliance risks are visible, teams naturally arrive at the same logical path."
        ],
        "qa_responses": [
            {"q": "How do you handle a growth manager who complains that compliance is slowing down product sales?", "a": "I demonstrate that compliance is actually a revenue protector. I use data to show them how a sudden checkout hold or regulatory penalty from unvalidated logs kills their sales entirely, whereas an automated data filter preserves their pipeline long-term."},
            {"q": "What is your strategy for delivering bad compliance news to cross-functional leaders?", "a": "I remove subjective language. I present a comparative risk model highlighting the exact financial exposure and operational impacts. When leadership views hard transactional numbers, the discussion shifts from an emotional debate to data-driven risk management."},
            {"q": "How do you foster alignment between technical developers and non-technical legal teams?", "a": "By acting as the translator. I understand the business and legal rules from my MBA and corporate background, and I possess the engineering skills to write them into backend code, creating a seamless bridge between both domains."}
        ]
    },
    19: {
        "category": "WHEN - Extreme Scenarios & Crisis",
        "title": "Tech to Non-Tech",
        "tag": "COMMS",
        "bridge": "I translate complex backend data pipelines into clear financial metrics and corporate risk mitigation.",
        "case": "Executive reporting layers at Afinz and Heineken.",
        "followup": "Non-technical stakeholders don't need to hear about SQL query joins; they need to know if the company is legally safe.",
        "match": "Matches DWA's cross-functional requirement. Proves you can speak smoothly to founders, lawyers, and marketing heads.",
        "growth": "Leadership at DWA needs rapid answers to protect the brand. You provide clean, bite-sized executive summaries.",
        "bullets": [
            "I never explain the query syntax. I explain the hour savings or the tax exposure we successfully eliminated.",
            "I use standard corporate metrics that leadership cares about, like cost optimization or processing time saved.",
            "I make compliance visually obvious through clean dashboards rather than talking about backend data engineering."
        ],
        "qa_responses": [
            {"q": "How do you present complex database structures to our non-technical founders?", "a": "I never present code, tables, or database syntax. I present business answers. I use intuitive Power BI or Looker dashboards to visualize risk trends, cost optimization metrics, and system adherence so they can digest operational safety at a glance."},
            {"q": "What standard corporate metrics do you focus on during executive presentations?", "a": "I translate data into financial protection and efficiency gains: hours of manual work eliminated, processing cost reductions (FinOps), and the percentage of transactional data successfully verified against target international tax exposures."},
            {"q": "How did you manage executive communication during your previous data projects?", "a": "At both Afinz and Heineken, I designed strategic management reports and led alignment meetings for diverse corporate audiences. My focus was always on delivering data-driven suggestions to support executive decision-making directly."}
        ]
    },
    20: {
        "category": "WHEN - Extreme Scenarios & Crisis",
        "title": "Investigative Approach & Closing",
        "tag": "INVESTIGATIVE",
        "bridge": "To wrap up, I would love to ask a couple of technical questions to better understand the live challenges you are dealing with right now.",
        "case": "Taking control of the interview context with deep authority.",
        "followup": "What data stack are you running to manage checkouts? Do you have an internal case or data logic test I can solve to prove my execution speed?",
        "match": "Instantly positions you as a senior stakeholder who is auditing them back, guaranteeing an unforgettable close.",
        "growth": "DWA is growing fast. Showing readiness to dive into their live stack proves you are a plug-and-play asset.",
        "bullets": [
            "What is the current platform you use to ingest and query Stripe or payment logs? Is it AWS, GCP, or manual exports?",
            "What is the biggest operational data block your team faces weekly with cross-border tax records?",
            "I am ready to build your automated compliance frameworks so DWA can expand its revenue streams safely."
        ],
        "qa_responses": [
            {"q": "What is the ultimate objective you want to achieve for DWA's trade compliance?", "a": "To turn DWA's compliance arm into a zero-friction, fully automated engine. I want to build data guardrails that process global transactions flawlessly, allowing your online business to scale into any international territory without operational or legal lag."},
            {"q": "Do you have an practical entry test or data problem I can solve right now to prove my execution?", "a": "I am fully prepared to take a sample of your transactional logs or an operational business scenario and build an automated SQL/Python solution to demonstrate my code speed, optimization focus, and risk vision firsthand."},
            {"q": "How soon are you looking for this analyst to start driving impact?", "a": "My cloud toolkit and experience inside online sales funnels mean I have virtually zero learning curve. I am ready to step in as a plug-and-play asset to map, automate, and safeguard your operational data flows immediately."}
        ]
    }
}

if "active_id" not in st.session_state:
    st.session_state.active_id = 1

with st.sidebar:
    st.markdown("### Workspace Reference")
    st.caption("• André Carvalho ENG.pdf")
    st.caption("• Academia de Riqueza Digital.pdf")
    
    st.markdown("### Strategic Framework")
    st.info("**WHY:** Motivation & Fit\n\n**WHAT:** Scope & Profile\n\n**HOW:** STAR Actions\n\n**WHEN:** Crisis & Investigative Closing")
    
    st.markdown("### Match Analytics")
    st.metric(label="Interview Adherence Score", value="98%", delta="Elite Match")
    st.caption("**Target:** DWA · Trade Compliance Analyst")

# Layout Category Configuration - perfectly divided into exactly 4 uniform columns
categories_list = [
    "WHAT - Capabilities & Profile", 
    "WHY - Intent & Fit", 
    "HOW - Case Methodology (STAR)", 
    "WHEN - Extreme Scenarios & Crisis"
]

# Generate native 4 columns map to maintain symmetrical distribution
cols = st.columns(len(categories_list))

for idx, cat_name in enumerate(categories_list):
    with cols[idx]:
        st.markdown(f'<div class="category-header">{cat_name.split(" - ")[0]}</div>', unsafe_allow_html=True)
        cat_items = {k: v for k, v in DATA_MAPPING.items() if v["category"] == cat_name}
        
        for item_id, item_data in cat_items.items():
            is_active = (st.session_state.active_id == item_id)
            tag_token = f"[{item_data.get('tag', 'CONTEXT')}] "
            clean_title = item_data['title']
            btn_label = f"▸ {tag_token}{clean_title}" if is_active else f"{tag_token}{clean_title}"
            
            if st.button(btn_label, key=f"btn_{item_id}"):
                st.session_state.active_id = item_id
                st.rerun()

st.markdown("<div style='margin-top: 0.3rem; border-top: 1px solid #e9ecef; margin-bottom: 0.4rem;'></div>", unsafe_allow_html=True)

active_data = DATA_MAPPING[st.session_state.active_id]

# Responsive 50-50 Split View below buttons matrix
col_out1, col_out2 = st.columns([0.50, 0.50])

with col_out1:
    st.markdown(
        f"""
        <div class="response-box">
            <span style="color:#117a65; font-size:9.5px; font-weight:bold; text-transform:uppercase;">The Golden Bridge (Natural phrasing):</span><br>
            <strong style="font-size:12.5px; color:#2c3e50; line-height:1.2;">"{active_data['bridge']}"</strong>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    st.markdown(
        f"""
        <div class="followup-box">
            <span style="color:#2c3e50; font-size:9.5px; font-weight:bold; text-transform:uppercase;">Deep Dive (If asked to elaborate):</span><br>
            <p style="font-size:12px; color:#34495e; line-height:1.25;">{active_data['followup']}</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    st.markdown(
        f"""
        <div class="growth-box">
            <strong style="color:#d35400; text-transform:uppercase; font-size:9px;">The DWA Growth Link (The Strategic Approach):</strong><br>
            <p style="color:#ba4a00; font-size:11.5px; line-height:1.25; margin-top:1px;">{active_data['growth']}</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    st.markdown(
        f"""
        <div class="match-box">
            <strong style="color:#2980b9; text-transform:uppercase; font-size:9px;">The Compliance Match Concept:</strong><br>
            <p style="color:#1f618d; font-size:11.5px; line-height:1.25; margin-top:1px;">{active_data['match']}</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

with col_out2:
    st.markdown(
        f"""
        <div class="bullet-container-box">
            <span style="color:#2c3e50; font-size:10.5px; font-weight:bold; text-transform:uppercase; display:block; margin-bottom:4px;">Bulletproof Supporting Arguments:</span>
            {"".join(f'<p style="font-size:12px; color:#2c3e50; line-height:1.3; margin-bottom:4px !important;">• {bullet}</p>' for bullet in active_data["bullets"])}
            <p style='font-size:11px; color:#7f8c8d; margin-top:8px; border-top: 1px solid #e9ecef; padding-top:4px;'><strong>Baseline Case Reference:</strong> {active_data['case']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # NEW UX INJECTION: Dynamic C-Level Predictor Q&A Box taking over the empty bottom right space
    qa_html_items = ""
    for qa in active_data["qa_responses"]:
        qa_html_items += f"""
        <div class="qa-item">
            <strong style="font-size:11.5px; color:#c0392b; display:block; line-height:1.2;">Q: {qa['q']}</strong>
            <p style="font-size:11.5px; color:#232b2b; line-height:1.25; margin-top:2px !important;"><strong>A:</strong> {qa['a']}</p>
        </div>
        """
        
    st.markdown(
        f"""
        <div class="qa-container-box">
            <span style="color:#78281f; font-size:10.5px; font-weight:bold; text-transform:uppercase; display:block; margin-bottom:6px;">⚡ TOUGHEST C-LEVEL Q&A SIMULATOR:</span>
            {qa_html_items}
        </div>
        """,
        unsafe_allow_html=True
    )
