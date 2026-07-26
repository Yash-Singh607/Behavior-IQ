import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

def create_sih_submission_doc(output_path="Honeywell_Idea_Submission_BehaviorIQ.docx"):
    doc = docx.Document()
    
    # Page Margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)
        
    # Title
    title = doc.add_heading("HONEYWELL IDEA SUBMISSION", level=0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_run = title.runs[0]
    title_run.font.size = Pt(22)
    title_run.font.bold = True
    title_run.font.color.rgb = RGBColor(220, 38, 38) # Honeywell Red
    
    sub = doc.add_paragraph("BehaviorIQ: Autonomous Behavioral Anomaly Detection & Threat SOC Engine")
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub.runs[0].font.bold = True
    sub.runs[0].font.size = Pt(13)
    
    doc.add_paragraph() # Spacer
    
    def add_slide_heading(text):
        p = doc.add_heading(text, level=1)
        p.runs[0].font.size = Pt(16)
        p.runs[0].font.bold = True
        p.runs[0].font.color.rgb = RGBColor(15, 23, 42) # Slate Dark
        return p

    def add_bullet(p_or_text, bold_prefix="", text=""):
        p = doc.add_paragraph(style='List Bullet')
        if bold_prefix:
            r1 = p.add_run(bold_prefix + ": ")
            r1.bold = True
            r1.font.size = Pt(11)
        r2 = p.add_run(text)
        r2.font.size = Pt(11)
        return p

    # SLIDE 1
    add_slide_heading("SLIDE 1: TITLE PAGE")
    add_bullet(None, "Organization / Host", "Honeywell Hackathon Idea Submission")
    add_bullet(None, "Problem Statement Title", "Autonomous Behavioral Anomaly Detection & Threat SOC Engine for Enterprise IT & Industrial OT")
    add_bullet(None, "Theme", "Cybersecurity / Industrial OT Protection / AI & ML")
    add_bullet(None, "Category", "Software")
    add_bullet(None, "Student / Presenter Name", "Yash Singh")
    add_bullet(None, "Participant ID", "[Insert Your Registered ID Here]")
    
    doc.add_page_break()

    # SLIDE 2
    add_slide_heading("SLIDE 2: IDEA TITLE & PROPOSED SOLUTION")
    p2 = doc.add_paragraph()
    r = p2.add_run("Idea Title: BehaviorIQ — Autonomous AI-Powered Behavioral Threat Engine")
    r.bold = True; r.font.size = Pt(12)
    
    doc.add_heading("Proposed Solution (Describe your Idea/Solution/Prototype)", level=2)
    add_bullet(None, "Detailed Explanation", "BehaviorIQ is an autonomous AI-powered Security Operations Center (SOC) engine that replaces static SIEM alert rules with dynamic, per-entity machine learning baselines. It analyzes real-time stream logs (1,420+ events/sec) across users, service accounts, and Honeywell edge devices to detect novel zero-day intrusions.")
    add_bullet(None, "Addressing Alert Fatigue", "Enforces a strict Top 1% Alert Budget (>= 75.0 Risk Score), filtering out 99% of benign noise to eliminate analyst alert fatigue.")
    add_bullet(None, "Sub-Second Response", "Executes autonomous mitigation playbooks (Cloudflare WAF IP quarantine, OAuth2 token revocation, mandatory MFA) in <0.38 seconds.")
    add_bullet(None, "Innovation & Uniqueness", "Explainable AI (SHAP XAI) provides feature attributions and natural-language narratives for every alert. Integrated dark web breach intelligence cross-references compromised credentials.")

    doc.add_page_break()

    # SLIDE 3
    add_slide_heading("SLIDE 3: TECHNICAL APPROACH")
    doc.add_heading("Technologies to be used", level=2)
    add_bullet(None, "Machine Learning Core", "Scikit-Learn (Isolation Forest - 5,000 decision trees) + LightGBM Multi-Class Classifier + SHAP Explainability.")
    add_bullet(None, "Backend REST Infrastructure", "Python 3.11, FastAPI REST Framework, Uvicorn, Gunicorn, Apache Kafka Stream Broker, Redis Feature Store Cache.")
    add_bullet(None, "Frontend & Data Viz", "Glassmorphism HTML5 Canvas, Tailwind CSS v3, Chart.js, Web Audio API.")
    add_bullet(None, "Cloud Orchestration", "Docker, Docker Compose, Kubernetes HPA, Vercel (Frontend), Render (Backend).")

    doc.add_heading("Methodology and Implementation Pipeline", level=2)
    pipeline_p = doc.add_paragraph()
    pipeline_p.add_run("Real-Time Log Stream (1,420 eps) ➔ Feature Engineering (Geo-Velocity >840 km/h, Failed Logins/5m) ➔ Isolation Forest Profiler (5,000 Trees -> 0-100 Risk Score) ➔ Top 1% Alert Budget Filter (FPR 0.32%) ➔ LightGBM Classifier ➔ SHAP Attribution Narrative ➔ Autonomous WAF Block (<0.38s)").font.size = Pt(10)

    doc.add_page_break()

    # SLIDE 4
    add_slide_heading("SLIDE 4: FEASIBILITY AND VIABILITY")
    doc.add_heading("Feasibility Analysis", level=2)
    add_bullet(None, "Proven Model Accuracy", "Binary Anomaly F1-Score = 0.961, Precision = 0.972, Recall = 0.951.")
    add_bullet(None, "Ultra-Low Latency", "Machine learning inference completes in < 0.8ms per event, guaranteeing real-time streaming feasibility.")

    doc.add_heading("Potential Challenges & Risks", level=2)
    add_bullet(None, "Cold-Start Problem", "Newly onboarded users/devices (N < 20 events) triggering false positive storms.")
    add_bullet(None, "Concept Drift", "Legitimate evolving behavior over time causing baseline drift.")

    doc.add_heading("Overcoming Strategies", level=2)
    add_bullet(None, "Hierarchical Bayesian Blending", "Smoothly interpolates population priors (user vs service_account vs edge_device) and empirical stats, keeping cold-start FPR at 0.85%.")
    add_bullet(None, "EMA Concept Drift (alpha = 0.05)", "Dynamically adapts non-anomalous entity centroids over time without re-training models.")

    doc.add_page_break()

    # SLIDE 5
    add_slide_heading("SLIDE 5: ARTIFACTS & LIVE CLOUD DEPLOYMENT EVIDENCE")
    doc.add_heading("1. Live Cloud Production Deployments (Clickable Links)", level=2)
    add_bullet(None, "Live Vercel Frontend UI", "https://behavior-iq-jade.vercel.app")
    add_bullet(None, "Live Render FastAPI Backend", "https://behavior-iq.onrender.com")
    add_bullet(None, "Interactive Swagger API Docs", "https://behavior-iq.onrender.com/docs")
    add_bullet(None, "Open-Source GitHub Repository", "https://github.com/Yash-Singh607/Behavior-IQ")

    doc.add_heading("2. Live Analyst Login Credentials (For Evaluator Testing)", level=2)
    add_bullet(None, "Analyst Login Email", "admin@behavioriq.ai")
    add_bullet(None, "Analyst Password", "admin123")
    add_bullet(None, "Role & Access", "SOC Administrator & Lead Behavioral Security Analyst")

    doc.add_heading("3. Code & Production Microservice Artifacts", level=2)
    add_bullet(None, "Containerization", "Dockerfile (512MB memory-optimized), docker-compose.yml (Orchestrating API, Redis Feature Store, and Apache Kafka Broker).")
    add_bullet(None, "Kubernetes Manifests", "Full production Kubernetes deployment, Service LoadBalancer, and Horizontal Pod Autoscaler (HPA) manifests (deploy/k8s/deployment.yaml).")

    doc.add_heading("4. Interactive SOC Dashboard Features", level=2)
    add_bullet(None, "Real-Time Triage Desk", "Live incident queue table with SHAP feature attributions.")
    add_bullet(None, "Stage Threat Injector", "Interactive threat scenario simulator (Launch Attack Scenario).")
    add_bullet(None, "Real Security Gate", "Glassmorphism authentication gate modal with user profile dropdown.")

    doc.add_page_break()

    # SLIDE 6
    add_slide_heading("SLIDE 6: RESEARCH AND REFERENCES")
    add_bullet(None, "Isolation Forest Anomaly Detection", "Liu, F. T., Ting, K. M., & Zhou, Z. H. (2008). Isolation Forest. IEEE International Conference on Data Mining (ICDM).")
    add_bullet(None, "LightGBM Gradient Boosting", "Ke, G., et al. (2017). LightGBM: A Highly Efficient Gradient Boosting Decision Tree. Advances in Neural Information Processing Systems (NeurIPS).")
    add_bullet(None, "SHAP Explainability", "Lundberg, S. M., & Lee, S. I. (2017). A Unified Approach to Interpreting Model Predictions. NeurIPS.")
    add_bullet(None, "Cybersecurity Frameworks", "MITRE ATT&CK Matrix for Enterprise & ICS.")
    add_bullet(None, "Compliance Standards", "ISO/IEC 27001:2022, SOC 2 Type II, and GDPR Privacy Regulations.")

    doc.save(output_path)
    print(f"Document successfully created at {output_path}")

if __name__ == "__main__":
    create_sih_submission_doc()
