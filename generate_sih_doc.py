import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def create_exact_template_doc(output_path="Honeywell_Idea_Submission_BehaviorIQ.docx"):
    doc = docx.Document()
    
    # Page Margins
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)
        
    def add_page_title(text):
        p = doc.add_heading(text, level=1)
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run = p.runs[0]
        run.font.size = Pt(20)
        run.font.bold = True
        run.font.color.rgb = RGBColor(15, 23, 42) # Dark Slate
        return p

    def add_bullet(bold_prefix, text=""):
        p = doc.add_paragraph(style='List Bullet')
        if bold_prefix:
            r1 = p.add_run(bold_prefix)
            r1.bold = True
            r1.font.size = Pt(11)
        if text:
            r2 = p.add_run(" " + text if bold_prefix else text)
            r2.font.size = Pt(11)
        return p

    def add_sub_bullet(bold_prefix, text=""):
        p = doc.add_paragraph(style='List Bullet 2')
        if bold_prefix:
            r1 = p.add_run(bold_prefix)
            r1.bold = True
            r1.font.size = Pt(10.5)
        if text:
            r2 = p.add_run(" " + text if bold_prefix else text)
            r2.font.size = Pt(10.5)
        return p

    # PAGE 1: IMPORTANT INSTRUCTIONS
    add_page_title("IMPORTANT INSTRUCTIONS")
    p1 = doc.add_paragraph("Please ensure below pointers are met while submitting the Idea PPT:")
    p1.runs[0].font.bold = True
    add_bullet("1. Kindly keep the maximum slides limit up to six (6). (Including the title slide)")
    add_bullet("2. Try to avoid paragraphs and post your idea in points / diagrams / Infographics / pictures")
    add_bullet("3. Keep your explanation precise and easy to understand")
    add_bullet("4. Idea should be unique and novel.")
    add_bullet("5. You can only use provided template for making the PPT without changing the idea details pointers (mentioned in previous slides).")
    add_bullet("6. You need to save the file in PDF and upload the same on portal. No PPT, Word Doc or any other format will be supported.")
    
    p_note = doc.add_paragraph()
    r_note = p_note.add_run("Note - You can delete this slide (Important Pointers) when you upload the details of your idea portal.")
    r_note.font.bold = True
    r_note.font.color.rgb = RGBColor(220, 38, 38) # Red

    doc.add_page_break()

    # PAGE 2: TITLE PAGE
    add_page_title("TITLE PAGE")
    add_bullet("Problem Statement ID –", "[Insert Your PS ID e.g., SIH1234 / HW_SEC_01]")
    add_bullet("Problem Statement Title-", "Autonomous Behavioral Anomaly Detection & Threat SOC Engine for Enterprise IT & Industrial OT")
    add_bullet("Theme-", "Cybersecurity / AI & ML / Smart Industrial Automation")
    add_bullet("PS Category-", "Software")
    add_bullet("Student Name (Registered on portal)-", "Yash Singh")
    add_bullet("Student ID-", "[Insert Your Registered Portal Student ID]")

    doc.add_page_break()

    # PAGE 3: IDEA TITLE
    add_page_title("IDEA TITLE: BehaviorIQ")
    
    p_sub = doc.add_paragraph()
    r_sub = p_sub.add_run("Proposed Solution (Describe your Idea/Solution/Prototype)")
    r_sub.font.bold = True
    r_sub.font.size = Pt(14)
    r_sub.font.underline = True

    add_bullet("Detailed explanation of the proposed solution:")
    add_sub_bullet("• Autonomous Behavioral SOC Engine:", "Replaces static SIEM alert rules with dynamic, per-entity machine learning baselines to detect novel zero-day intrusions.")
    add_sub_bullet("• Dual-Stage ML Architecture:", "Combines an Unsupervised Isolation Forest Profiler (5,000 decision trees) for anomaly scoring [0-100] with a Multi-Class LightGBM Classifier for threat taxonomy assignment.")
    add_sub_bullet("• Explainable AI (SHAP XAI):", "Provides SHAP feature attribution leaderboards and natural-language forensic narratives for every flagged alert.")

    add_bullet("How it addresses the problem:")
    add_sub_bullet("• Eliminates SOC Alert Fatigue:", "Enforces a strict Top 1% Alert Budget (>= 75.0 Risk Score), filtering out 99% of benign false positive noise.")
    add_sub_bullet("• Sub-Second Mitigation Response:", "Executes autonomous playbooks (Cloudflare WAF IP quarantine, OAuth2 token revocation, mandatory MFA) in < 0.38 seconds.")
    add_sub_bullet("• Solves Edge Cases:", "Employs Hierarchical Bayesian Blending for Cold-Start entities (N < 20 events) and Exponential Moving Average (EMA alpha = 0.05) for Concept Drift adaptation.")

    add_bullet("Innovation and uniqueness of the solution:")
    add_sub_bullet("• Real-Time Geo-Velocity Tracking:", "Calculates physical travel speed (> 840 km/h) between consecutive access tokens to stop impossible travel intrusions.")
    add_sub_bullet("• Dark Web Intelligence Integration:", "Live cross-referencing of entity session tokens against active dark web credential dumps and breach databases.")

    doc.add_page_break()

    # PAGE 4: TECHNICAL APPROACH
    add_page_title("TECHNICAL APPROACH")

    add_bullet("Technologies to be used (e.g. programming languages, frameworks, hardware):")
    add_sub_bullet("• Languages & Backend Frameworks:", "Python 3.11, FastAPI REST Framework, Uvicorn, Gunicorn WSGI.")
    add_sub_bullet("• Machine Learning & Explainability:", "Scikit-Learn (Isolation Forest), LightGBM (Multi-Class Gradient Boosting), SHAP (SHapley Additive exPlanations), NumPy, Pandas.")
    add_sub_bullet("• Distributed Streaming & Storage:", "Apache Kafka Event Broker (1,420+ eps), Redis Feature Store Cache (<0.2ms latency).")
    add_sub_bullet("• Frontend Interface:", "Glassmorphism HTML5 Canvas, Tailwind CSS v3, Chart.js, Web Audio API.")
    add_sub_bullet("• Cloud & Orchestration:", "Docker, Docker Compose, Kubernetes HPA (Autoscaling), Vercel (Frontend), Render (Backend).")

    add_bullet("Methodology and process for implementation (Flow Charts/Images/ working prototype):")
    add_sub_bullet("• Ingestion & Feature Engineering Pipeline:", "Access Stream Logs ➔ Extract Geo-Velocity, Failed Login Bursts, Device Hash ➔ Stateful Feature Matrix.")
    add_sub_bullet("• Unsupervised Profiling & Scoring:", "Feature Matrix ➔ Isolation Forest (5,000 Trees) ➔ Normalized Anomaly Score [0-100].")
    add_sub_bullet("• Top 1% Alert Budget Filter:", "Score >= 75.0 ? Flag Threat : Update EMA Baseline Profile (alpha = 0.05).")
    add_sub_bullet("• Classification & Explainability:", "Flagged Anomaly ➔ LightGBM Classifier ➔ SHAP Feature Importance Attribution ➔ Analyst Triage Desk.")
    add_sub_bullet("• Autonomous SOAR Playbook:", "High Confidence Threat ➔ Execute Cloudflare WAF IP Block & OAuth Token Revocation (<0.38s).")

    doc.add_page_break()

    # PAGE 5: FEASIBILITY AND VIABILITY
    add_page_title("FEASIBILITY AND VIABILITY")

    add_bullet("Analysis of the feasibility of the idea:")
    add_sub_bullet("• Empirical ML Benchmark Scores:", "Binary Anomaly F1-Score = 0.961, Precision = 0.972, Recall = 0.951.")
    add_sub_bullet("• Real-Time Latency Benchmark:", "Model inference completes in < 0.8ms per event, handling > 12,000 events/sec throughput.")
    add_sub_bullet("• False Positive Rate Target:", "Top 1% Alert Budget enforcement maintains FPR < 0.32%, well below the industry standard limit.")

    add_bullet("Potential challenges and risks:")
    add_sub_bullet("• Cold-Start Challenge:", "Newly onboarded users or IoT devices (N < 20 events) lack behavioral history, risking false positive storms.")
    add_sub_bullet("• Concept Drift Risk:", "Legitimate evolving employee behavior (e.g. shift change) causing false baseline drift over time.")

    add_bullet("Strategies for overcoming these challenges:")
    add_sub_bullet("• Hierarchical Bayesian Blending:", "Blends population priors (user vs service_account vs edge_device) with empirical stats, reducing cold-start FPR to 0.85%.")
    add_sub_bullet("• EMA Baseline Adaptation (alpha = 0.05):", "Continuously updates non-anomalous baseline centroids without requiring expensive full-model retraining.")

    doc.add_page_break()

    # PAGE 6: ARTIFACTS
    add_page_title("ARTIFACTS")

    add_bullet("Relevant artifacts, such as :")

    add_bullet("Copy of the Code Embedded:")
    add_sub_bullet("• GitHub Repository:", "https://github.com/Yash-Singh607/Behavior-IQ")
    add_sub_bullet("• Containerization:", "Dockerfile (512MB RAM optimized), docker-compose.yml (API, Redis, Kafka).")
    add_sub_bullet("• Kubernetes Manifests:", "deploy/k8s/deployment.yaml (Deployment, LoadBalancer Service, Horizontal Pod Autoscaler).")

    add_bullet("Snaps of the solution proposal & Live Cloud Links:")
    add_sub_bullet("• Live Vercel Frontend UI:", "https://behavior-iq-jade.vercel.app")
    add_sub_bullet("• Live Render FastAPI Backend:", "https://behavior-iq.onrender.com")
    add_sub_bullet("• Interactive Swagger API Docs:", "https://behavior-iq.onrender.com/docs")
    add_sub_bullet("• Live Analyst Testing Credentials:", "Email: admin@behavioriq.ai | Password: admin123")

    add_bullet("Dashboard snaps:")
    add_sub_bullet("• Real-Time Incident Triage Desk:", "Interactive triage stream table with SHAP feature attributions.")
    add_sub_bullet("• Stage Threat Injection Simulator:", "⚡ Launch Attack Scenario trigger (APT29 Cozy Bear, FIN7 Ransomware, Insider Data Theft).")
    add_sub_bullet("• Security Gate Authentication:", "Glassmorphism login gate modal with user profile dropdown.")

    doc.add_page_break()

    # PAGE 7: RESEARCH AND REFERENCES
    add_page_title("RESEARCH AND REFERENCES")

    add_bullet("Details / Links of the reference and research work:")
    add_sub_bullet("• Isolation Forest Anomaly Detection:", "Liu, F. T., Ting, K. M., & Zhou, Z. H. (2008). Isolation Forest. IEEE International Conference on Data Mining (ICDM).")
    add_sub_bullet("• LightGBM Gradient Boosting Framework:", "Ke, G., et al. (2017). LightGBM: A Highly Efficient Gradient Boosting Decision Tree. Advances in Neural Information Processing Systems (NeurIPS).")
    add_sub_bullet("• SHAP Explainable AI Framework:", "Lundberg, S. M., & Lee, S. I. (2017). A Unified Approach to Interpreting Model Predictions. NeurIPS.")
    add_sub_bullet("• MITRE ATT&CK Framework:", "MITRE ATT&CK Matrix for Enterprise & Industrial Control Systems (ICS).")
    add_sub_bullet("• Security & Compliance Standards:", "ISO/IEC 27001:2022, SOC 2 Type II, and GDPR Privacy Regulations.")

    doc.save(output_path)
    print(f"Document successfully created at {output_path}")

if __name__ == "__main__":
    create_exact_template_doc()

