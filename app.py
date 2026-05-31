import streamlit as st

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
    padding-top: 1.0rem !important;
    padding-bottom: 0.1rem !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
    max-width: 100% !important;
}

/* Global scrollbar behavior control for clean hardware feel */
::-webkit-scrollbar {
    display: none !important;
}

div[data-testid="stVerticalBlock"] {
    gap: 0.15rem !important;
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

/* Force column button wrappers to have exact uniform heights */
div.stButton > button {
    width: 100% !important;
    height: 44px !important; 
    white-space: normal !important; 
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

/* Output Display Blocks - Compressed & Symmetrical heights */
.response-box {
    background-color: #e8f8f5;
    border-left: 4px solid #18bc9c;
    padding: 6px 10px !important;
    border-radius: 4px;
    margin-bottom: 0.3rem;
    min-height: 48px;
}

.followup-box {
    background-color: #f4f6f7;
    border-left: 4px solid #34495e;
    padding: 6px 10px !important;
    border-radius: 4px;
    margin-bottom: 0.3rem;
    min-height: 48px;
}

.growth-box {
    background-color: #fef9e7;
    border-left: 4px solid #f39c12;
    padding: 5px 10px !important;
    border-radius: 4px;
    margin-bottom: 0.3rem;
    min-height: 40px;
}

.match-box {
    background-color: #ebf5fb;
    border-left: 4px solid #3498db;
    padding: 5px 10px !important;
    border-radius: 4px;
    margin-bottom: 0.3rem;
    min-height: 40px;
}

.bullet-container-box {
    background-color: #ffffff;
    border: 1px solid #e9ecef;
    border-radius: 4px;
    padding: 6px 10px !important;
    min-height: 120px;
}

.qa-container-box {
    background-color: #f2f4f4;
    border: 1px solid #d5dbdb;
    border-left: 4px solid #1b4f72;
    border-radius: 4px;
    padding: 6px 10px !important;
    margin-top: 3px;
    min-height: 180px;
}

.qa-item {
    margin-bottom: 4px !important;
    padding-bottom: 3px;
    border-bottom: 1px dashed #d5dbdb;
}
.qa-item:last-child {
    border-bottom: none;
    margin-bottom: 0px !important;
}

/* Embedded Document Viewer Styles with Header Protection Gap */
.doc-container {
    background-color: #ffffff;
    border: 1px solid #d5dbdb;
    border-radius: 6px;
    padding: 24px !important;
    padding-top: 25px !important; /* Fixed cutoff issue at the top border */
    box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    max-height: 78vh;
    overflow-y: auto !important;
}
.doc-title {
    color: #1b4f72;
    font-size: 18px;
    font-weight: bold;
    border-bottom: 3px solid #1b4f72;
    padding-bottom: 8px;
    margin-bottom: 18px !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.doc-section {
    font-size: 13px;
    color: #2c3e50;
    margin-bottom: 12px !important;
    line-height: 1.5;
}
.doc-subtitle {
    font-size: 14px;
    color: #154360;
    font-weight: bold;
    margin-top: 16px !important;
    margin-bottom: 6px !important;
    border-bottom: 1px solid #eaeded;
    padding-bottom: 2px;
}
.commentary-box {
    background-color: #ebf5fb;
    border-left: 4px solid #2980b9;
    padding: 10px !important;
    margin-top: 6px !important;
    margin-bottom: 12px !important;
    border-radius: 4px;
    font-size: 12.5px;
}
</style>
""", unsafe_allow_html=True)

# 20 Strategic Framework Database Items - Brands in italics for speaking guardrails
DATA_MAPPING = {
    1: {
        "category": "WHAT - Capabilities & Profile",
        "title": "Tell me about yourself",
        "tag": "PROFILE",
        "bridge": "I am a Production Engineer with an FGV MBA and specialized expertise in Analytics and BI, recognized for transforming raw operational parameters into optimized, data-driven revenue protection models.",
        "followup": "My approach bridges technical architecture with strategic risk management, helping organizations replace fragmented spreadsheet manual processes with robust database single sources of truth.",
        "match": "Establishes institutional authority, linking data-driven decisions directly to global financial security.",
        "growth": "DWA requires infrastructure safety as transaction volume increases; my profile guarantees data predictability without performance bottlenecks.",
        "case": "Engineering + MBA + Corporate Analytics (*Heineken*, *Itaú*, *ASICS*, *NTT DATA*).",
        "bullets": [
            "I leverage structured analytical experience developed across market leaders in highly regulated domains like consumer goods (*Heineken*), banking (*Itaú*), and cross-border retail (*ASICS*).",
            "I isolate data infrastructure friction points, enabling executive teams to align critical decisions with solid database evidence.",
            "My methodology prioritizes infrastructure resource optimization, asset preservation, and structural risk minimization."
        ],
        "qa_responses": [
            {"q": "What is the baseline blueprint of your value proposition?", "a": "I combine process engineering logic with a strategic business overview to maximize infrastructure value. I don't just audit backend query lines; I establish analytical frameworks that proactively secure cross-border revenue and stabilize checkout log funnels."},
            {"q": "How do you drive a scaling team to become truly data-driven?", "a": "By removing subjective guessing and human manual lag from the operational equation. True data-driven execution means translating regulatory and commercial rules into automated validation scripts embedded directly inside the cloud architecture."},
            {"q": "Our data foundations are currently messy. Are you comfortable with manual data cleaning?", "a": "Before any sustainable automation engine can be deployed, a thorough investigation of the raw components is mandatory. I am fully prepared to audit and clean initial data logs manually to completely map out the parameters before structuring long-term architectures."}
        ]
    },
    2: {
        "category": "WHY - Intent & Fit",
        "title": "Why DWA?",
        "tag": "STRATEGY",
        "bridge": "Your main compliance risks are not waiting at a physical shipping dock. They are living inside your live checkout database.",
        "followup": "When a digital brand scales cross-border via *Stripe*, the real bottlenecks are digital tax lines and payment gateway holds.",
        "match": "Proves you understand their exact digital business model (MRR/Infoproducts) better than traditional candidates.",
        "growth": "The organization operates globally with high velocity; they need a data expert who secures cash flow, not a traditional logistics agent.",
        "case": "Cross-border Digital Model (MRR/*Stripe*/VAT).",
        "bullets": [
            "Operating across multiple regions means managing complex checkout rules and European VAT lines instantly.",
            "I want to apply my SQL toolkit to audit 100% of transaction logs automatically.",
            "My focus is protecting your digital checkout funnel from sudden international regulatory blocks."
        ],
        "qa_responses": [
            {"q": "What specific risk do you see in our digital cross-border model?", "a": "With high transaction volumes across multiple borders, your biggest threats are international tax mismatching (like European VAT logic) and sudden payment processor holds due to pattern irregularities. Both stop cash flow instantly."},
            {"q": "How do you plan to help the operation scale?", "a": "By embedding automated validation scripts directly inside the data flow. As volume scales 10x, a manual team fractures. An automated pipeline processes millions of logs with the same processing speed and zero human errors."},
            {"q": "You come from massive corporate brands. Why join our ecosystem?", "a": "Large corporate environments are great for mastering governance at scale, but their structures move slowly. This ecosystem has the velocity, agility, and modern tech-first mindset where my optimization scripts can generate real impact from week one."}
        ]
    },
    3: {
        "category": "WHY - Intent & Fit",
        "title": "Why Trade Compliance?",
        "tag": "COMPLIANCE",
        "bridge": "I view compliance as an optimization and data governance architecture framework designed to ensure absolute process predictability.",
        "followup": "When operational processes mirror international legal parameters flawlessly inside a structured data flow, the business can expand with zero regulatory liabilities.",
        "match": "Positions you as a process-driven governor who treats risk tracking as a systemic engineering discipline.",
        "growth": "Organizations scale safely only when their internal workflows are structured; I provide the operational guardrails needed to secure corporate health.",
        "case": "Data Governance, Quality Control & Process Workflows.",
        "bullets": [
            "My experience with complex metrics and documentation enables me to track data integrity and spot process anomalies cleanly.",
            "I enjoy translating strict business rules into transparent, fully mapped workflows that eliminate operational vulnerabilities.",
            "I believe compliance is the ultimately strategic arm of a global business because it guarantees uninterrupted cash flow."
        ],
        "qa_responses": [
            {"q": "If you are a BI Analyst, why focus on Compliance?", "a": "I don't see it as a shift, but as the highest application of Data Governance. BI visualizes past metrics; Compliance actively safeguards current capabilities. Using advanced data engineering to isolate process vulnerabilities is how I protect corporate assets."},
            {"q": "How do you approach auditing complex, changing international parameters?", "a": "I handle them as dynamic parameter updates rather than hardcoded rules. By structuring configurable views inside the cloud database, the entire historical structure adapts instantly when a legal parameter shifts, preventing system lag."},
            {"q": "How do you ensure data integrity across cross-border financial logs?", "a": "By enforcing strict validation and traceability metrics, similar to what I delivered in past projects (*Afinz*). I ensure all data payloads are fully mapped and verified against master tables to isolate discrepancies before they hit reporting layers."}
        ]
    },
    4: {
        "category": "WHAT - Capabilities & Profile",
        "title": "Your Value Proposition",
        "tag": "VALUE",
        "bridge": "I bring technical scale and pipeline automation to a department that traditionally works with manual tools.",
        "followup": "I bridge the gap between complex legal regulations and hard database rules, removing human error completely.",
        "match": "Directly links your analytics expertise to their immediate need for lean, automated operations.",
        "growth": "Startup environments require proactive solution architecture; my engineering focus eliminates systemic tech debt before it scales.",
        "case": "FinOps, SQL, and Advanced Pipeline Automation.",
        "bullets": [
            "I translate wordy regulatory updates into clean automated database filters.",
            "I build transparent dashboards that give leadership a live, 100% reliable view of risk.",
            "My target is zero friction at the checkout page and zero compliance risk with international tax authorities."
        ],
        "qa_responses": [
            {"q": "What is your immediate 30-day value add if hired?", "a": "Map out your transactional log streams, identify any manual reporting dependencies (like manual Excel updates), and optimize those workflows into clean SQL automated views to ensure total financial and regulatory data integrity."},
            {"q": "How do you balance compliance restrictions with a growth-focused sales pipeline?", "a": "Compliance shouldn't block the funnel; it must act as an invisible guardrail. By using real-time automated scripts instead of slow human reviews, we ensure legitimate sales go through instantly while high-risk anomalies are isolated behind the scenes."},
            {"q": "What distinguishes your approach to data documentation?", "a": "I follow strict documentation standards using tools like *Confluence*. I believe a data workflow is only complete when its metadata is fully mapped, allowing any internal stakeholder to audit the operational logic effortlessly."}
        ]
    },
    5: {
        "category": "WHY - Intent & Fit",
        "title": "Salary Expectations",
        "tag": "ANCHOR",
        "bridge": "My financial target is based on the data infrastructure scale and cost savings I can deliver.",
        "followup": "I anchor my rate based on my ability to optimize cloud spend and secure global financial pipelines from day one.",
        "match": "Establishes a transparent, business-driven value alignment without awkward verbal gaps.",
        "growth": "Protects the bottom line. A data-driven approach means your salary is offset by systemic optimization.",
        "case": "Firm Target Range (Clear numbers written out).",
        "bullets": [
            "For a local structure, my target is between 8,000 (eight thousand) and 10,000 (ten thousand) Reais per month.",
            "For an international contractor setup, that maps directly to 2,000 (two thousand) US Dollars per month.",
            "This range reflects a professional who actively implements FinOps and automated data governance layers."
        ],
        "qa_responses": [
            {"q": "Is this number negotiable depending on the benefits package?", "a": "Yes, I am completely open to discussing the overall contract architecture, especially if there is alignment on long-term project growth, remote flexibility, and performance impact metrics."},
            {"q": "Why should we invest this budget in your profile over a junior analyst?", "a": "A junior analyst will maintain manual routines and spreadsheets. My profile pays for itself by implementing FinOps optimizations that slash processing costs—just like I did in cross-border retail (*ASICS*)—and preventing costly revenue blocks from international authorities."},
            {"q": "Are you comfortable with an international B2B contractor arrangement?", "a": "Absolutely. I operate with professional systems and my setup is engineered for seamless cross-border remote integration, which perfectly fits global operating models."}
        ]
    },
    6: {
        "category": "WHAT - Capabilities & Profile",
        "title": "No Physical Customs Exp",
        "tag": "OBJECTION",
        "bridge": "That is true for physical shipping, but I view international trade regulations as logical database rules.",
        "followup": "A container needs a physical stamp; a global checkout needs a database code validation rule. The logic is identical.",
        "match": "Reframes an apparent skill gap, showing that database auditing is the real solution for digital assets.",
        "growth": "The medium relies on bytes and data logs, not physical freight. My background matches this specific architecture.",
        "case": "*Burity* (Legal Audits) + Advanced SQL logic.",
        "bullets": [
            "Physical customs deal with ocean cargo; digital compliance deals with real-time transactional logs.",
            "My biggest core strength is picking up tricky regulatory rules fast and turning them into automated data controls.",
            "I have spent years verifying legal contracts and blueprints—ensuring data follows rules is my core expertise."
        ],
        "qa_responses": [
            {"q": "The job description emphasizes customs brokerage experience. How do you close that gap?", "a": "Customs brokerage focuses on matching cargo to static tax books. In a digital ecosystem, the logic is identical, but the medium changes. Instead of reviewing paper manifests, I write clean SQL validation scripts to audit digital sales logs against international tax jurisdictions. I automate what a traditional broker does manually."},
            {"q": "How can we be sure you understand international regulatory frameworks?", "a": "During my tenure at *Burity*, I managed complex legal processes, audited corporate property registries, and acted as a legal proxy. I am deeply trained in reading strict legal text and translating it into hard operational workflows."},
            {"q": "What happens if we need to deal with a traditional customs inquiry?", "a": "My engineering approach means that every transaction is documented with clean data traceability. If an international auditor requests a review, we don't scramble through Excel sheets; we pull a flawless, structured database report instantly."}
        ]
    },
    7: {
        "category": "WHAT - Capabilities & Profile",
        "title": "No HTS Code Mastery",
        "tag": "HTS-MAPPING",
        "bridge": "HTS classification is a structured database mapping problem. I process complex taxonomies every day.",
        "followup": "Instead of trying to memorize catalog codes like a human broker, I treat them as structured lookup tables.",
        "match": "Demonstrates technical intelligence—turning static manual processes into scalable automation.",
        "growth": "As the product catalog expands, manual classification will fail. An automated script-based lookup engine scales instantly.",
        "case": "Amazon Athena / BigQuery View Structuring.",
        "bullets": [
            "I am highly comfortable setting up dynamic views that adapt when business parameters shift.",
            "Classifying a digital asset or a physical cargo item follows the exact same relational database logic.",
            "I will translate your product catalog into automated backend lookup scripts for instant validation."
        ],
        "qa_responses": [
            {"q": "How would you handle classifying a complex new product line using HTS?", "a": "I would treat the HTS taxonomy as a relational lookup table. By mapping our internal digital inventory metadata against the official classification matrix via automated scripts, we ensure instantaneous, programmatic categorization instead of manual guessing."},
            {"q": "What is the danger of relying on manual product classification?", "a": "Manual entry introduces human error, which triggers tax mismatches, transaction friction, and compliance audits. Automation guarantees that once a business rule is validated, it applies uniformly across thousands of global daily sales."},
            {"q": "Have you worked with complex taxonomies before?", "a": "Yes. At a *major global beverage brand* (*Heineken*), I consolidated and normalized fragmented data across 200 distinct digital products and multiple channels. I am highly accustomed to organizing messy product data into strict, auditable structures."}
        ]
    },
    8: {
        "category": "WHY - Intent & Fit",
        "title": "You are Overqualified",
        "tag": "RETENTION",
        "bridge": "Honestly, I am specifically looking for a complex risk architecture challenge, not a comfortable routine.",
        "followup": "A repetitive manual data role would be boring. Building automated risk frameworks for a scaling brand keeps me sharp.",
        "match": "Removes the flight-risk anxiety by showing deep intellectual alignment with their core data challenges.",
        "growth": "Startups grow too fast for basic profiles. You provide the advanced toolkit that saves them from rebuilding systems next year.",
        "case": "FinOps & Cloud Optimization Mentality.",
        "bullets": [
            "I am genuinely motivated by engineering scalable, automated compliance guardrails from scratch.",
            "A fast-paced digital model offers the exact data velocity and volume that I enjoy optimizing.",
            "I want to commit long-term to design, code, and secure your cloud compliance infrastructure."
        ],
        "qa_responses": [
            {"q": "Your resume contains Machine Learning and Cloud Engineering. Won't you find this role boring?", "a": "It would only be boring if I performed it manually. Using my advanced toolkit to automate a fast-growing digital compliance engine from scratch is an intellectual challenge that standard, static corporations simply cannot offer."},
            {"q": "What keeps a professional like you loyal to a company?", "a": "Autonomy to optimize processes and systemic complexity. As long as the operation continues expanding its global footprint, new data volumes, cross-border tax hurdles, and system integrations will appear. That technical challenge keeps me highly engaged."},
            {"q": "How does your senior expertise benefit a lean team?", "a": "It prevents tech debt. A junior profile builds short-sighted sheets that break next month. I engineer clean data foundations and documented pipelines that will support transaction scaling for years without needing a system redesign."}
        ]
    },
    9: {
        "category": "WHAT - Capabilities & Profile",
        "title": "Short Tenures (Stalse/NTT)",
        "tag": "PROJECTS",
        "bridge": "These were strategic, fast-paced contract projects brought in to unlock specific data architecture blocks.",
        "followup": "I view these experiences highly positively because they allowed me to rapidly deploy systems across completely different cloud environments.",
        "match": "Frames short projects as intentional, high-impact consulting sprints rather than instability.",
        "growth": "Immediate solution delivery is critical; my experience executing rapid 4-month sprints means I deliver results without a long onboarding lag.",
        "case": "Agile Sprints & Cross-Cloud Toolkit.",
        "bullets": [
            "At a *boutique data agency* (*Stalse*), I focused on GCP pipelines to clean up multi-country revenue views for a *retail leader* (*ASICS*).",
            "At a *global tech consultancy* (*NTT Data*), I engineered data solutions to optimize transactional loads for a *tier-one banking client* (*Itaú*).",
            "Now, I am looking for a long-term challenge to implement this complete cross-cloud arsenal."
        ],
        "qa_responses": [
            {"q": "Why did you stay only 4 months at these specific projects?", "a": "Both were structured as high-impact, temporary consulting contracts designed to solve a specific engineering bottleneck. Once the pipelines were automated, the dashboards launched, and documentation completed, the project concluded successfully."},
            {"q": "Are you looking for a long-term home or another short contract?", "a": "I am specifically looking for a permanent, long-term remote opportunity where I can embed myself into the core culture and continuously protect the operation as the brand scales internationally."},
            {"q": "How does jumping across different projects help the team?", "a": "It has hyper-accelerated my tech adaptability. In under a year, I engineered systems in GCP/BigQuery for a *major consumer brand* and immediately shifted to AWS/Athena for a *banking institution*. I can adapt to whatever tech stack the organization runs with zero friction."}
        ]
    },
    10: {
        "category": "WHY - Intent & Fit",
        "title": "Why change fields now?",
        "tag": "EVOLUTION",
        "bridge": "I don't see it as changing fields. I am simply applying modern tools to classic governance problems.",
        "followup": "Compliance is moving to the cloud. Teams that do not adapt their data pipelines will struggle to survive audits.",
        "match": "Positions you as a forward-thinking Professional who sits where risk management and data science meet.",
        "growth": "Hiring a traditional agent is a step backward; hiring a data-driven risk analyst represents the operational future.",
        "case": "Transition from Management Analytics to Data Engineering.",
        "bullets": [
            "Moving into Advanced Analytics allows me to protect company assets at a scale humans cannot match.",
            "I have spent my career tracking metrics and spotting process anomalies; compliance is the natural next step.",
            "I am positioning my engineering toolkit exactly where the future of risk management is heading."
        ],
        "qa_responses": [
            {"q": "Why not stick to classic Business Intelligence roles?", "a": "Classic BI tells you what happened in the past. Modern Risk Compliance uses the exact same data to actively protect the firm's current checkout capability and future expansion. It is a much more strategic, high-stakes application of my skills."},
            {"q": "What part of your analytical mindset applies best to risk tracking?", "a": "Anomaly detection. My background allows me to glance at thousands of log outputs, instantly spot an integration gap or an incorrect country tax calculation, and deploy a permanent programmatic correction before it causes damage."},
            {"q": "How do you view the future of digital trade regulation?", "a": "Governments are becoming highly sophisticated at auditing digital products. The companies that survive are those that treat compliance as a live data pipeline rather than a year-end accounting task. I bring that exact future-proof model to the operation."}
        ]
    },
    11: {
        "category": "HOW - Case Methodology (STAR)",
        "title": "ASICS (2026 - FinOps)",
        "tag": "CROSS-BORDER",
        "bridge": "I built a unified, cross-border financial data model across 3 (three) countries to secure international revenue tracking.",
        "followup": "We integrated multi-source data platforms into a single architecture, automating currency conversions and tax parameters.",
        "match": "Directly mirrors cross-border operational realities, proving capability to manage complex financial lines across regions.",
        "growth": "The logic used to consolidate international revenue rules for a *cross-border retail leader* (*ASICS*) maps directly to global sales auditing.",
        "case": "Stalse Project for *ASICS* Latam (Brazil, Chile, Colombia).",
        "bullets": [
            "Situation: Fragmented regional data views created massive visibility risks and tracking anomalies for leadership.",
            "Action: I re-engineered the data architecture using BigQuery and automated daily loads using advanced SQL rules.",
            "Result: Slashed cloud data consumption from Gigabytes to Megabytes, optimizing performance and reducing query costs."
        ],
        "qa_responses": [
            {"q": "How did you handle currency conversions and cross-border data mismatches?", "a": "I engineered an automated ETL pipeline inside BigQuery that ingested local transaction streams, applied dynamic currency conversion lookup layers, and standardized regional tax definitions into a single, unified view for management."},
            {"q": "What was the direct business impact of your FinOps optimization?", "a": "By optimizing query syntax and refactoring legacy data tables, I reduced processing loads from Gigabytes to Megabytes. This didn't just maximize processing speed; it directly optimized cloud infrastructure spend and prevented system lag."},
            {"q": "How does this experience help you protect checkout streams?", "a": "The exact logical engine I used to align Latin American regional revenue rules is what I will use to ingest cross-border processor logs, guaranteeing that our automated dashboard matches regional tax laws perfectly."}
        ]
    },
    12: {
        "category": "HOW - Case Methodology (STAR)",
        "title": "NTT DATA / Itaú (2025)",
        "tag": "SCALE-DATA",
        "bridge": "I engineered cloud data pipelines to deliver automated performance reporting for 5,000 (five thousand) executives.",
        "followup": "The project demanded absolute data consistency while handling high-volume tables with complex, evolving business rules.",
        "match": "Proves technical capability to handle massive transaction volumes without system lag or data corruption.",
        "growth": "When high-volume checkout events trigger daily, AWS data experience ensures queries maintain integrity.",
        "case": "Data Analyst at *NTT Data* for *Itaú* (AWS Cloud Environment).",
        "bullets": [
            "Situation: The client needed to calculate executive metrics by joining tables with billions of rows of messy records.",
            "Action: I built complex database views and robust data transformations using Amazon Athena, S3, and AWS Glue.",
            "Result: Delivered an automated dashboard tool that processed massive scales with absolute data consistency."
        ],
        "qa_responses": [
            {"q": "How did you maintain data integrity while handling tables with billions of rows?", "a": "By leveraging partition strategies in Amazon S3, designing optimized schemas, and building highly structured SQL views in Amazon Athena. This ensured that even under massive volume scales, our data transformations never suffered corruption."},
            {"q": "What did you do when the business rules evolved during the project?", "a": "Instead of hardcoding rules into static scripts, I built dynamic, parameter-driven SQL views. When business indicators or rules shifted, we updated the configuration tables, and the entire historical database adapted instantly without downtime."},
            {"q": "Why is your experience with AWS critical?", "a": "Online platforms process real-time events. My familiarity with backend cloud architectures like S3 and Athena means I can easily interface with technical data ecosystems to pull, analyze, and secure raw transactional data cleanly."}
        ]
    },
    14: {
        "category": "HOW - Case Methodology (STAR)",
        "title": "Afinz (2022 - 2023)",
        "tag": "OPTIMIZATION",
        "bridge": "My methodology is engineered to isolate operational friction and optimize resource allocation through automated pipeline systems.",
        "followup": "By mapping metadata structures and establishing strict automated validation layers, we protect data processing speed and prevent transactional lags simultaneously.",
        "match": "Proves an execution-focused mindset. Compliance teams thrive when they eliminate slow manual bottlenecks.",
        "growth": "Startups cannot afford workflows that create operational drag. Technical optimization frees up critical baseline time.",
        "case": "MIS Analyst at *Afinz* / *Sorocred*.",
        "bullets": [
            "Situation: Daily data reporting workflows were entirely manual, taking 1.5 (one and a half) hours and creating operational lags.",
            "Action: Developed automated ETL data pipelines using Python, SQL, and structured repositories.",
            "Result: Slashed processing time down to just 15 (fifteen) minutes while significantly strengthening the data quality framework."
        ],
        "qa_responses": [
            {"q": "How did you reduce a reporting workflow from 1.5 hours to 15 minutes?", "a": "By auditing the legacy routine, identifying repetitive human manual tasks, and rewriting the entire ingestion sequence into automated Python and SQL data pipelines. The system handled the heavy lifting, leaving humans to focus purely on anomaly analysis."},
            {"q": "What was your approach to Data Governance?", "a": "I structured metadata repositories and clear documentation models inside cloud platforms. This ensured that all definition metrics and data sources were fully governed, transparent, and aligned with internal process frameworks."},
            {"q": "How will your focus on automation optimize compliance arms?", "a": "I will target any manual data gathering or Excel compilation inside your compliance routines and replace them with automated data extractions. This minimizes compliance overhead, removes human delay, and provides immediate data feedback loops."}
        ]
    },
    13: {
        "category": "HOW - Case Methodology (STAR)",
        "title": "Heineken (2023 - 2024)",
        "tag": "E-COMMERCE",
        "bridge": "I normalize chaotic e-commerce data streams across 200 distinct online digital products.",
        "followup": "I focus on cleaning up fragmented client inputs to build a transparent, auditable reporting pipeline for leadership.",
        "match": "Gives you zero learning curve regarding digital checkouts, sales funnels, and online platform metrics.",
        "growth": "Operating inside digital infoproduct ecosystems requires familiarity with funnels, online platform checkouts, and transactional data logs.",
        "case": "Allocated at *Heineken* (Digital Channel Analytics).",
        "bullets": [
            "Situation: Received fragmented spreadsheets from multiple clients in different formats, blocking commercial campaign tracking.",
            "Action: Designed a clean Star Schema relational model and built a unified performance dashboard inside Power BI.",
            "Result: Launched the first stable automation in less than 1 (one) month, matching financial indicators to the exact penny."
        ],
        "qa_responses": [
            {"q": "How do you handle messy, unstructured e-commerce data from multiple clients?", "a": "I designed a rigid Star Schema data model that forced all incoming data into a standardized relational mapping. This eliminated anomalies and insured that messy, disparate formats translated into clean, standardized metrics."},
            {"q": "What does 'matching indicators to the exact penny' mean for compliance?", "a": "It means total audirability. If an e-commerce platform has unexplained micro-discrepancies between its checkout logs and bank deposits, it creates immediate financial and compliance risk. I specialize in building data verification loops that eliminate these gaps."},
            {"q": "How does your digital market experience translate to this ecosystem?", "a": "I already speak the language of e-commerce, digital checkouts, funnels, and customer segments. I don't need to be trained on what an online funnel look like; I can dive directly into auditing your product categories and sales data from day one."}
        ]
    },
    15: {
        "category": "HOW - Case Methodology (STAR)",
        "title": "Burity (Regulatory Base)",
        "tag": "LEGAL-AUDIT",
        "bridge": "I acted as a legal proxy managing high-value regulatory, contract, and operational risks with zero liabilities.",
        "followup": "I audited complex legal processes, agreements, and blueprints to rectify historical administrative errors.",
        "match": "Validates your foundational compliance mindset: reading rules, verifying contracts, and protecting corporate assets.",
        "growth": "Even in a digital company, the core philosophy of compliance remains the same: mitigating liability. You have years of proof.",
        "case": "Asset & Property Manager at *Burity Empresarial*.",
        "bullets": [
            "Situation: Managed complex negotiations involving multi-million dollar corporations and strict government registries.",
            "Action: Aligned internal legal and engineering teams to correct descriptive errors and execute land compliance steps.",
            "Result: Secured critical infrastructure expansions administratively, driving asset valuation up with zero lawsuits."
        ],
        "qa_responses": [
            {"q": "How does legal proxy experience translate to digital trade compliance?", "a": "The essence of compliance never changes: it is about risk mitigation, textual precision, and strict adherence to institutional rules. Auditing property registries and managing regulatory compliance trained my eye to ensure everything is aligned with legal frameworks."},
            {"q": "Can you give an example of rectifying an administrative error?", "a": "I audited historical technical blueprints and legal agreements to isolate descriptive errors that created major regulatory liabilities. By coordinating cross-functional teams, we rectified those records before any government penalties arose."},
            {"q": "How do you handle interactions with strict government regulatory frameworks?", "a": "With absolute data preparation and zero speculation. My extensive tenure managing property compliance taught me that regulators respond to indisputable, fully documented evidence. I apply that exact precision to digital transaction audits."}
        ]
    },
    16: {
        "category": "WHEN - Extreme Scenarios & Crisis",
        "title": "Handling a Major Mistake",
        "tag": "MISTAKE-LOG",
        "bridge": "I don't hide behind code execution. If an operational rule or pipeline breaks, my immediate response is instant containment to minimize downside risk.",
        "followup": "I believe in total transparency. I flag the structural bug, present the exact transactional exposure to leadership, and deploy a permanent architectural patch.",
        "match": "Highlights executive maturity under pressure, treating system anomalies as objective engineering problems.",
        "growth": "In a rapid scale startup, bugs appear; an analyst must isolate failure points calmly and deploy permanent fixes.",
        "case": "Data Quality, Containment Layers & Traceability.",
        "bullets": [
            "I suppress emotional noise, pull the raw query logs, and isolate the exact affected transaction range immediately.",
            "I apply a temporary containment filter to stop the leak while diagnosing the root cause breakdown.",
            "I write a new automated verification check directly into the pipeline syntax so that specific vulnerability can never repeat."
        ],
        "qa_responses": [
            {"q": "What is your immediate reaction when a critical data error is uncovered?", "a": "My priority is instant containment, not finger-pointing. I pull the raw query logs, isolate the affected transaction window, and deploy a temporary filter to stop the bleeding. Once the operation is stabilized, I run a root-cause analysis and translate that specific failure into a permanent automated check inside the pipeline."},
            {"q": "How do you communicate an internal pipeline error to C-Level stakeholders?", "a": "With complete data precision. I present a clear summary detailing the root cause, the exact quantified revenue or compliance exposure, and the active resolution patch. Executives value immediate solutions, not open-ended problems."},
            {"q": "How do you ensure data adjustments do not corrupt historical auditable logs?", "a": "By enforcing strict database append-only frameworks. Any corrective adjustments are processed as documented ledger entries with clean metadata traceability, keeping our main historical compliance views fully auditable and compliant with international standards."}
        ]
    },
    17: {
        "category": "WHEN - Extreme Scenarios & Crisis",
        "title": "Unmapped High-Pressure Task",
        "tag": "CONTEXT",
        "bridge": "Under extreme pressure with unmapped issues, I rely on structured frameworks, not emotional guessing.",
        "followup": "When a system blind spot appears, you isolate the parameters, review historical logs, and roll out a safe patch.",
        "match": "Demonstrates clear analytical focus and the ability to operate safely inside chaotic environments.",
        "growth": "Global digital sales face sudden updates (like payment gateway changes). You provide a steady, logical filter during high-pressure alerts.",
        "case": "Agile problem diagnosis.",
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
        "followup": "People usually push back because of underlying business anxieties. Once you show them the numbers, the noise stops.",
        "match": "Validates strong, non-combative communication skills, ensuring smooth relations between tech and legal departments.",
        "growth": "As compliance sets tighter rules, sales teams might push back. You use data to prove that compliance protects their bonuses.",
        "case": "Strategic performance alignment with cross-functional teams.",
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
        "followup": "Non-technical stakeholders don't need to hear about SQL query joins; they need to know if the company is legally safe.",
        "match": "Matches cross-functional requirements, proving the capability to present clear operational updates to diverse teams.",
        "growth": "Leadership requires rapid, digestible structural answers; executive analytical summaries provide immediate clarity.",
        "case": "Executive reporting layers across scale architectures.",
        "bullets": [
            "I never explain the query syntax. I explain the hour savings or the tax exposure we successfully eliminated.",
            "I use standard corporate metrics that leadership cares about, like cost optimization or processing time saved.",
            "I make compliance visually obvious through clean dashboards rather than talking about backend data engineering."
        ],
        "qa_responses": [
            {"q": "How do you present complex database structures to non-technical stakeholders?", "a": "I never present code, tables, or database syntax. I present business answers. I use intuitive dashboards to visualize risk trends, cost optimization metrics, and system adherence so they can digest operational safety at a glance."},
            {"q": "What standard corporate metrics do you focus on during executive presentations?", "a": "I translate data into financial protection and efficiency gains: hours of manual work eliminated, processing cost reductions (FinOps), and the percentage of transactional data successfully verified against target international tax exposures."},
            {"q": "How did you manage executive communication during your previous data projects?", "a": "Across my engineering and analytical tenure, I designed strategic management reports and led alignment meetings for diverse corporate audiences. My focus was always on delivering data-driven suggestions to support executive decision-making directly."}
        ]
    },
    20: {
        "category": "WHEN - Extreme Scenarios & Crisis",
        "title": "Investigative Approach & Closing",
        "tag": "INVESTIGATIVE",
        "bridge": "To wrap up, I would love to align our conversation with a quick strategic assessment of DWA's current architectural state.",
        "followup": "What is the primary platform you leverage to ingest live payment events? Based on that, I am prepared to deliver immediate data-driven value.",
        "match": "Applies a Harvard/McKinsey-level structured ending, shifting the conversation from a pass-fail test to a peer-to-peer strategy alignment.",
        "growth": "A rapid scale model benefits immediately from plug-and-play assets who drive clarity from the final seconds of contact.",
        "case": "Strategic Cross-Functional Integration Techniques.",
        "bullets": [
            "💼 [VALUE CONTRIBUTION CLOSE]: 'I am fully prepared to integrate my cloud toolkit into the operational data pipeline to turn regulatory complexity into automated, highly predictable profit guardrails. I look forward to contributing directly to your team's global scaling.'",
            "⏳ [CONDITIONAL ROADMAP MATCH]: 'Thank you for the strategic overview. It is clear that compliance here is a live data automation problem, which fits my core framework perfectly. I hope to sync again very soon to align on the execution details.'",
            "🌅 [POLISHED WRAP-UP VARIATIONS]: Choose based on timing: 1) 'Have a productive week ahead.' | 2) 'Have an excellent weekend.' | 3) 'It was a real pleasure meeting you today. Let's stay in touch.'"
        ],
        "qa_responses": [
            {"q": "How do you use data to minimize chargebacks without killing checkout conversion?", "a": "By establishing real-time pattern filtering. Instead of broad, generic rules that block legitimate global users, I write precise data models that isolate abnormal fraud markers silently behind the scenes."},
            {"q": "Have you ever audited complex multi-party financial loops or payment splits?", "a": "Yes. In past regional unifications, I aligned fragmented cross-border flows involving dynamic tax rules and regional parameters. Organizing multi-party data taxonomies into clean relational tables is a core strength of my database design."},
            {"q": "Do you have a practical data challenge or case test I can solve right now?", "a": "I would welcome the opportunity. If you can provide a masked extraction of your transactional logs, I am fully prepared to build an automated SQL or Python filter script to demonstrate my code speed, optimization focus, and risk vision firsthand."}
        ]
    }
}

# Navigation State Initialization
if "view_mode" not in st.session_state:
    st.session_state.view_mode = "Main Interview Board"
if "active_id" not in st.session_state:
    st.session_state.active_id = 1

with st.sidebar:
    st.markdown("### Select Workspace View")
    # Native Streamlit navigation buttons inside the sidebar to toggle views seamlessly
    if st.button("📊 Main Interview Board", use_container_width=True):
        st.session_state.view_mode = "Main Interview Board"
        st.rerun()
        
    if st.button("📄 View: André Carvalho ENG_2.pdf", use_container_width=True):
        st.session_state.view_mode = "CV Doc"
        st.rerun()
        
    if st.button("📘 View: Academia de Riqueza Digital_2.pdf", use_container_width=True):
        st.session_state.view_mode = "Guide Doc"
        st.rerun()
    
    st.markdown("---")
    st.markdown("### Strategic Framework")
    st.info("**WHY:** Motivation & Fit\n\n**WHAT:** Scope & Profile\n\n**HOW:** STAR Actions\n\n**WHEN:** Crisis & Investigative Closing")
    
    st.markdown("### Match Analytics")
    st.metric(label="Interview Adherence Score", value="98%", delta="Elite Match")
    st.caption("**Target:** DWA · Trade Compliance Analyst")

# --- VIEW ROUTING ENGINE ---

if st.session_state.view_mode == "CV Doc":
    st.markdown('<div class="doc-container"><div class="doc-title">Document View: André Carvalho — Resume</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="doc-section">
        <strong>ANDRÉ CARVALHO</strong><br>
        Data Analyst | Business Intelligence Analyst 
    </div>
    <div class="doc-subtitle">Professional Summary</div>
    <div class="doc-section">
        Data Analyst and Business Intelligence professional with experience in Analytics, FinOps, Machine Learning, ETL pipelines, Cloud Data Platforms, and Data Governance. Proven track record delivering scalable analytical solutions and strategic insights for companies including Heineken, Itaú, ASICS Latam, Fretebras, and FSB Comunicação. Strong expertise in SQL, Python, AWS, GCP, Power BI, BigQuery, Athena, and dashboard automation.
    </div>
    <div class="doc-subtitle">Professional Experience</div>
    <div class="doc-section">
        <strong>Business Intelligence Analyst :: Stalse (Hybrid Contract) | Jan 2026 - Apr 2026</strong><br>
        • Worked on strategic data projects for clients such as <em>ASICS Latam</em> and <em>Fretebras</em>, focusing on operational efficiency, financial predictability, and value generation.<br>
        • Simplified data architecture, reducing cloud data consumption from Gigabytes to Megabytes, optimizing costs and performance.<br>
        • Created a unified revenue view for Latin American operations (Brazil, Chile, and Colombia) and automated the management dashboard.<br>
        • Conducted strategic SEO analysis, mitigating operational risks and impacts on Customer Acquisition Cost (CAC).
    </div>
    <div class="doc-section">
        <strong>Data Analyst :: NTT DATA (Remote Contract) | Feb 2025 - May 2025</strong><br>
        • Worked within the AWS cloud environment, serving a major enterprise client in the corporate sector (*Itaú*).<br>
        • Focused on Amazon Athena, executing complex SQL queries for data analysis and developing complex view transformations.<br>
        • Collaborated with business units to understand and translate complex requirements into technical solutions under Agile methodologies.
    </div>
    <div class="doc-section">
        <strong>Business Intelligence Analyst :: Sxpel Technologies (Remote) | Nov 2023 - Oct 2024</strong><br>
        • Allocated at <em>Heineken</em>, focused on the Digital Area (eRetail, eCommerce).<br>
        • Consolidated and normalized large customer datasets, designing analytical data models using Star Schema methodologies.<br>
        • Implemented data quality validation and traceability processes increasing reporting reliability for executive decision-making.
    </div>
    <div class="doc-section">
        <strong>MIS (Management Information System) Analyst :: Afinz (Remote) | Sep 2022 - Jun 2023</strong><br>
        • Improved performance of daily data update routines, reducing processing time from 1h30m to just 15 minutes via ETL automation.<br>
        • Structured metadata organization and Data Governance layers using SQL, Python, and AWS tools (Athena, Glue, S3).
    </div>
    <div class="doc-section">
        <strong>Management / T&D Analyst :: Integral Desenvolvimento Humano Ltda | Jan 2005 - Sep 2022</strong><br>
        • Conducted over 2,000 structured analyses, directly supporting corporate strategic decisions for enterprises like Gerdau and Sabesp.<br>
        • Created comparative models for performance evaluation, increasing efficiency in identifying operational gaps.
    </div>
    <div class="doc-section">
        <strong>Asset & Property Manager :: Burity Empresarial | Oct 1996 - Aug 2022</strong><br>
        • Acted as a legal proxy (Procurador). Audited and verified legal processes, agreements, contracts, and technical blueprints to rectify administrative errors and mitigate risks with zero liabilities.
    </div>
    <div class="doc-subtitle">Education & Certifications</div>
    <div class="doc-section">
        • <strong>MBA in Business Administration</strong> — Fundação Getulio Vargas (FGV), Completed in 2006.<br>
        • <strong>Bachelor's Degree in Production Engineering</strong> — CREA-SP, Completed in 2021.<br>
        • Data Analyst & BI Certifications — XPe / IGTI (148 hours each, 2022).<br>
        • <strong>Languages:</strong> Portuguese (Native) | English (Advanced — Academic experience at St Giles International, London).
    </div>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.view_mode == "Guide Doc":
    st.markdown('<div class="doc-container"><div class="doc-title">Document View: Academia de Riqueza Digital — Guia Integral</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="doc-section">
        <strong>4 Blocos Estratégicos de Preparação</strong>
    </div>
    
    <div class="doc-subtitle">Bloco 1: Os Pontos de Convergência</div>
    <div class="doc-section">
        Para vencer esta entrevista, precisas de conectar o modelo de negócio deles à tua capacidade técnica.<br>
        • <strong>Modelo Digital Transfronteiriço:</strong> Venda global de infoprodutos (MRR). O cliente compra de qualquer lugar do mundo através de checkout digital (*Stripe*/PayPal). Milhares de transações diárias.<br>
        • <strong>A Dor Oculta:</strong> Quando uma empresa digital cresce muito rápido internacionalmente, ela enfrenta problemas graves com Impostos Digitais (Regras de IVA/VAT na Europa, onde cada país tem uma taxa para produtos digitais), Bloqueios de Checkout (Processadores de pagamento bloqueiam contas se houver picos de transações sem validação de risco ou compliance de dados) e Auditoria Manual (Eles provavelmente estão a tentar gerir milhares de linhas de vendas em Excel e o processo está a quebrar).<br>
        • <strong>A Visão Real da Vaga (Trade Compliance Analyst):</strong> Embora a descrição pareça tradicional (HTS, importação), no contexto da DWA, eles procuram alguém para garantir a conformidade regulatória e fiscal das vendas globais. Eles não precisam de alguém para lidar com navios; precisam de alguém para classificar os produtos digitais, auditar os dados de vendas e garantir que a operação está blindada contra o fisco internacional.<br>
        • <strong>O Que Podes Entregar (A tua Proposta de Valor):</strong> Em vez de conferir papéis de importação, a tua entrega consiste em centralizar os dados de vendas globais, criar regras automatizadas (via SQL/Python) para detetar anomalias fiscais ou de risco, e gerar dashboards de visibilidade de compliance para a liderança.<br>
        • <strong>Convergência do Teu Perfil:</strong> <em>"O Compliance da DWA não se faz no porto, faz-se no banco de dados. Eu sou o analista que audita e automatiza esse fluxo."</em> Engenharia e Estrutura (MBA) + SQL Avançado / BigQuery / AWS Athena + Automação de Processos e FinOps.
        To win this interview, you need to connect their business model to your technical capabilities.
        • Cross-Border Digital Model: Global sales of digital assets and info-products (MRR). Customers buy from anywhere in the world through digital checkouts (Stripe/PayPal). Thousands of daily transactions.
        • The Hidden Pain Point: When a digital business scales internationally at high velocity, it faces severe bottlenecks with Digital Taxation (European VAT/IVA frameworks, where each country enforces a specific rate for digital assets), Checkout Blocks (Payment processors freeze merchant accounts during transaction volume spikes if there is no real-time risk validation or data compliance), and Manual Auditing (They are likely trying to manage thousands of transaction rows in Excel, and the workflow is collapsing).
        • The Real Job Paradigm (Trade Compliance Analyst): Although the job description sounds traditional (HTS, imports), within the context of DWA, they are looking for an asset to secure the regulatory and fiscal compliance of global sales. They don't need someone to handle cargo ships; they need someone to classify digital products, audit transactional log data, and guarantee the operation is bulletproof against international tax authorities.
        • Your Value Proposition: Instead of cross-checking physical import documentation, your delivery consists of centralizing global sales data streams, engineering automated validation rules (via SQL/Python) to detect fiscal or operational risk anomalies, and building clear compliance visibility dashboards for executive leadership.
        • Profile Convergence: "DWA’s compliance isn't managed at a physical shipping port—it is engineered inside the database. I am the analyst who audits and automates that exact data flow."
    
    </div>
    
    <div class="commentary-box">
        <strong>Mapeamento de Aderência por Experiência Corporativa (Gatilhos de Entrevista):</strong><br>
        • <strong>Stalse (*ASICS*):</strong> A unificação de receita para múltiplos países (Brasil, Chile, Colômbia) prova que você sabe lidar com dados financeiros transfronteiriços (cross-border), que é o núcleo do compliance da DWA. O foco em reduzir custos de dados (FinOps) mostra preocupação com o caixa da empresa. <em>Destaque:</em> A lógica de consolidar regras de receita internacionais e mitigar riscos financeiros para a ASICS é o que você vai aplicar para auditar as vendas globais de infoprodutos deles.<br>
        • <strong>NTT DATA (*Itaú*):</strong> A frase "adjusting them according to evolving business rules" (ajustando de acordo com a mudança das regras de negócio) é ouro para o compliance. As leis de impostos e taxas digitais mudam constantemente no mundo; você prova que sabe adaptar sistemas a regras mutáveis. <em>Destaque:</em> Mostre que você usa a AWS (Athena) para ler grandes volumes de logs de transações e auditar se as regras do negócio estão sendo seguidas à risca no banco de dados.<br>
        • <strong>Heineken:</strong> O foco explícito em Digital Area, eRetail e eCommerce significa que você já entende a dinâmica, as métricas e a estrutura de dados de canais digitais de grandes marcas, o que reduz a sua curva de aprendizado sobre o modelo de negócio deles para quase zero.<br>
        • <strong>Afinz:</strong> Duas palavras fundamentais aqui: Data Governance e Process Workflows. Compliance é, por definição, governança e respeito a processos. Reduzir o tempo de atualização de 1h30 para 15 minutos prova sua capacidade de otimização de tempo e processos. <em>Destaque:</em> Use este exemplo para mostrar que você foca em eficiência operacional. Explique que você gosta de documentar e estruturar processos (via SharePoint/Confluence) para garantir que a equipe siga os padrões regulatórios sem perder agilidade.<br>
        • <strong>Integral Desenvolvimento Humano:</strong> Foco em pensamento estruturado (structured thinking). A realização de mais de 2.000 análises estruturadas e o foco em "identificar gaps operacionais" (erros ou falhas em processos) mostra olhar clínico para auditoria em ambientes regulados (*Gerdau* e *Sabesp*).<br>
        • <strong>Burity:</strong> Termos como "Acted as a legal proxy" (Procurador), "Audited and verified legal processes, agreements, and contracts" são pura gestão de riscos e conformidade legal. <em>Destaque:</em> Se o recrutador for muito apegado ao lado jurídico/normativo, use a Burity para provar que você sabe o que significa ler contratos, seguir leis à risca e lidar com a burocracia governamental para mitigar riscos patrimoniais e legais.
        Corporate Experience Mapping & Alignment (Interview Triggers):
        • Stalse (ASICS): Revenue unification across multiple countries (Brazil, Chile, Colombia) proves your capability in handling cross-border financial data architectures, which is the core baseline of DWA’s compliance framework. Your focus on optimizing data consumption costs (FinOps) demonstrates clear alignment with cash flow protection. Strategic Highlight: The exact structural logic used to consolidate international revenue rules and mitigate financial exposure for ASICS is what you will deploy to audit their global info-product sales logs.  
        • NTT DATA (Itaú): The phrase "adjusting them according to evolving business rules" is pure gold for risk and compliance assessment. International digital tax policies and regulations shift constantly; you prove that your systems adapt seamlessly to fluid business constraints. Strategic Highlight: Emphasize that you leverage AWS (Athena) to ingest massive transactional event log volumes, auditing if complex internal protocols are strictly validated inside the database.  
        • Heineken: Your explicit focus on the Digital Area, eRetail, and eCommerce means you already thoroughly understand the dynamics, performance metrics, and data infrastructure of major digital channels. This effectively reduces your operational learning curve regarding their business model to nearly zero.  
        • Afinz: Two critical keywords apply here: Data Governance and Process Workflows. Compliance is, by definition, governance and process execution predictability. Automating a pipeline load routine from 1h30m down to just 15 minutes provides solid proof of infrastructure optimization capability. Strategic Highlight: Leverage this case to showcase your drive for operational efficiency; explain that you map and structure documentation (via SharePoint/Confluence) to guarantee that technical squads maintain strict regulatory standards without losing velocity.  
        • Integral Desenvolvimento Humano: Focus on structured thinking. Conducting over 2,000 structured analyses with a clear lens on "identifying operational gaps" and process friction demonstrates the sharp clinical eye required for systemic auditing in highly regulated corporate environments such as Gerdau and Sabesp.  
        • Burity: Core pillars such as "Acted as a legal proxy" and "Audited and verified legal processes, agreements, and contracts" translate directly into pure corporate risk management and regulatory compliance. Strategic Highlight: If the interviewer leans heavily on the legal/regulatory spectrum of the role, use this tenure to prove you understand how to evaluate legal clauses, maintain strict normative alignment, and manage corporate liabilities against institutional frameworks.
    </div>
    
    <div class="doc-subtitle">Bloco 2: Roteiro Prático de Entrevista (Curto e Direto)</div>
    <div class="doc-section">
        1. <strong>Tell me about yourself:</strong> <em>"I'm a Data and Business Intelligence professional with an engineering background and an MBA. Throughout my career, I've specialized in centralizing financial data, automating manual reporting, and mitigating operational risks. I help companies turn chaotic data into structured, compliant, and reliable workflows."</em> -> Define imediatamente o teu nível sênior e foca em estrutura e risco.<br>
        2. <strong>Why DWA?:</strong> <em>"DWA is a fast-growing global digital business. Since you operate cross-border with digital products, your biggest compliance challenges aren't at a physical port—they are inside your transactional data. I want to apply my analytics background to help DWA scale its compliance framework smoothly."</em> -> Mostra que compreendes o desafio do modelo digital melhor do que um candidato tradicional.<br>
        3. <strong>Why are you a good fit for Trade Compliance?:</strong> <em>"Because modern compliance is a data problem. I am analytical, process-oriented, and highly detail-oriented. My experience with data governance, financial validation, and advanced SQL allows me to audit 100% of transaction data in real-time, rather than doing manual, slow checks in Excel."</em> -> Transforma a falta de experiência aduaneira tradicional no maior argumento de venda.<br>
        4. <strong>Tell me about a time you solved an operational risk problem (O Case Asics/Stalse):</strong> <em>"At my last project, we had fragmented financial and revenue data across multiple countries, which created huge visibility risks. I re-engineered the data architecture using BigQuery and automated the reporting pipeline. As a result, we eliminated data silos, reduced processing costs, and delivered a 100% reliable view of international revenue to leadership."</em> -> Prova que sabe lidar com o cenário internacional da DWA.<br>
        5. <strong>Objection Handling: 'You don't have experience with Customs/HTS laws.':</strong> <em>"That's true regarding physical customs, but I view international regulations as complex business rules. My core strength is taking complex legal or financial rules, learning them quickly, and translating them into automated data controls to ensure the business is 100% compliant."</em> -> Desarma a objeção focando na adaptabilidade lógica.
    </div>
    
    <div class="doc-subtitle">Bloco 3: Estratégias e Técnicas de Entrevista</div>
    <div class="doc-section">
        • <strong>Técnica do 'Bridging' (Ponte):</strong> Sempre que fizerem uma pergunta sobre comércio exterior tradicional que não domines, responde brevemente e faz a ponte para o teu terreno (dados e processos). Exemplo: <em>"I haven't used HTS for physical shipping, but what I do know deeply is how to classify digital assets for cross-border transactions..."</em><br>
        • <strong>The Power of Silence:</strong> Como a entrevista é em inglês, se não souberes uma palavra, não preenchas o espaço com "uhmmm" ou "ahhh". Para, respira por 2 segundos, organiza a frase curta e responde. Passa uma imagem de alguém analítico e calmo.<br>
        • <strong>Linguagem de Negócio:</strong> Substitui termos puramente técnicos por termos de negócio. Em vez de dizer "eu escrevo scripts em Python", diz "eu crio automações para reduzir riscos operacionais e trabalho manual".
    </div>
    
    <div class="doc-subtitle">Bloco 4: Pontos de Atenção (Onde podes escorregar)</div>
    <div class="doc-section">
        1. <strong>O Alinhamento do Recrutador:</strong> Se a primeira entrevista for com um RH terceirizado ou júnior, eles podem ter apenas um "checklist" de palavras-chave (como HTS, Alfândega, etc.). Atenção: Se sentires que o entrevistador é muito literal, foca nas palavras Auditoria, Processos, Organização e Controlo de Riscos. Não os assustes com termos pesados de Engenharia de Dados se eles não forem da área técnica.<br>
        2. <strong>O 'Overqualification' (Excesso de Qualificação):</strong> O teu currículo tem Heineken, AWS, BigQuery e Machine Learning. O entrevistador pode pensar que vai achar o trabalho uma seca e sair rápido. Mitigação: Deixa claro que gostas da área de Risco e Estrutura e que o teu objetivo na DWA é construir uma infraestrutura eficiente, o que para ti é um desafio intelectual muito interessante.<br>
        3. <strong>Foco no Inglês Prático:</strong> Não uses palavras difíceis ou frases longas. O inglês de negócios internacional valoriza a clareza e a concisão. Frases curtas evitam erros gramaticais e mantêm o tom profissional.
    </div>
    
    <div class="doc-subtitle">About the Job & Qualifications Matrix</div>
    <div class="doc-section">
        • <strong>Company Description:</strong> Dedicated to empowering individuals to build successful online businesses through training programs covering email marketing, content production, and affiliate models.<br>
        • <strong>Role Description:</strong> Full-time remote Trade Compliance Analyst. Responsible for ensuring compliance with international trade regulations, conducting audits, analyzing regulatory changes, and tracking the Harmonized Tariff Schedule (HTS).<br>
        • <strong>Core Qualifications Required:</strong> Proficiency in Trade Compliance; Strong Analytical Skills to assess risks; Knowledge in Import Compliance; Understanding of HTS applications; Excellent attention to detail; Strong communication skills; Bachelor's degree preferred.
    </div>
    </div>
    """, unsafe_allow_html=True)

else:
    # --- DEFAULT MAIN INTERVIEW BOARD VIEW ---
    categories_list = [
        "WHAT - Capabilities & Profile", 
        "WHY - Intent & Fit", 
        "HOW - Case Methodology (STAR)", 
        "WHEN - Extreme Scenarios & Crisis"
    ]

    # Symmetrical 4-Column Layout Grid for Category Navigation
    cols = st.columns(len(categories_list))

    for idx, cat_name in enumerate(categories_list):
        with cols[idx]:
            st.markdown(f'<div class="category-header">{cat_name.split(" - ")[0]}</div>', unsafe_allow_html=True)
            cat_items = {k: v for k, v in DATA_MAPPING.items() if v["category"] == cat_name}
            
            for item_id, item_data in cat_items.items():
                is_active = (st.session_state.active_id == item_id)
                tag_token = f"[{item_data.get('tag', 'CONTEXT')}] "
                clean_title = item_data.get('title', 'Untitled')
                btn_label = f"▸ {tag_token}{clean_title}" if is_active else f"{tag_token}{clean_title}"
                
                if st.button(btn_label, key=f"btn_{item_id}"):
                    st.session_state.active_id = item_id
                    st.rerun()

    st.markdown("<div style='margin-top: 0.15rem; border-top: 1px solid #e9ecef; margin-bottom: 0.25rem;'></div>", unsafe_allow_html=True)

    active_data = DATA_MAPPING.get(st.session_state.active_id, DATA_MAPPING[1])

    # Responsive 50-50 Split View below navigation matrix
    col_out1, col_out2 = st.columns([0.50, 0.50])

    with col_out1:
        st.markdown(
            f"""
            <div class="response-box">
                <span style="color:#117a65; font-size:9.5px; font-weight:bold; text-transform:uppercase;">The Golden Bridge (Natural phrasing):</span><br>
                <strong style="font-size:12.5px; color:#2c3e50; line-height:1.2;">"{active_data.get('bridge', '')}"</strong>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        st.markdown(
            f"""
            <div class="followup-box">
                <span style="color:#2c3e50; font-size:9.5px; font-weight:bold; text-transform:uppercase;">Deep Dive (If asked to elaborate):</span><br>
                <p style="font-size:12px; color:#34495e; line-height:1.25;">{active_data.get('followup', '')}</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        st.markdown(
            f"""
            <div class="growth-box">
                <strong style="color:#d35400; text-transform:uppercase; font-size:9px;">The DWA Growth Link (The Strategic Approach):</strong><br>
                <p style="color:#ba4a00; font-size:11.5px; line-height:1.25; margin-top:1px;">{active_data.get('growth', '')}</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        st.markdown(
            f"""
            <div class="match-box">
                <strong style="color:#2980b9; text-transform:uppercase; font-size:9px;">The Compliance Match Concept:</strong><br>
                <p style="color:#1f618d; font-size:11.5px; line-height:1.25; margin-top:1px;">{active_data.get('match', '')}</p>
            </div>
            """, 
            unsafe_allow_html=True
        )

    with col_out2:
        # ULTRA-COMPACT CONTAINER: Reduced margins, font size and inline layout for the reference text
        bullets_list = active_data.get("bullets", [])
        bullets_html = "".join(f'<p style="font-size:12px; color:#2c3e50; line-height:1.25; margin-bottom:2px !important;">• {b}</p>' for b in bullets_list)
        
        st.markdown(
            f"""
            <div class="bullet-container-box">
                <span style="color:#2c3e50; font-size:10.5px; font-weight:bold; text-transform:uppercase; display:block; margin-bottom:4px;">Bulletproof Supporting Arguments:</span>
                {bullets_html}
                <p style='font-size:10px; color:#7f8c8d; margin-top:2px !important;'><strong>Baseline Case:</strong> {active_data.get('case', '')}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # REFACTORED UX BOX: Dark Blue Accent & Symmetrical layout spacing with fallback control
        qa_list = active_data.get("qa_responses", [])
        qa_html_items = ""
        for qa in qa_list:
            qa_html_items += f"""
            <div class="qa-item">
                <strong style="font-size:11.5px; color:#1b4f72; display:block; line-height:1.2;">Q: {qa.get('q', '')}</strong>
                <p style="font-size:11.5px; color:#154360; line-height:1.25; margin-top:1px !important;"><strong>A:</strong> {qa.get('a', '')}</p>
            </div>
            """
            
        st.markdown(
            f"""
            <div class="qa-container-box">
                <span style="color:#154360; font-size:10.5px; font-weight:bold; text-transform:uppercase; display:block; margin-bottom:4px;">⚡ TOUGHEST C-LEVEL Q&A SIMULATOR:</span>
                {qa_html_items}
            </div>
            """,
            unsafe_allow_html=True
        )
