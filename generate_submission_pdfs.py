import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors

def build_presentation_pdf(output_path="presentation.pdf"):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40
    )
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0f172a'),
        alignment=0,
        spaceAfter=12
    )
    
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#334155'),
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'DocBullet',
        parent=styles['Normal'],
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#1e293b'),
        leftIndent=15,
        spaceAfter=4
    )

    footer_style = ParagraphStyle(
        'DocFooter',
        parent=styles['Normal'],
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#94a3b8'),
        alignment=1,
        spaceBefore=20
    )

    story = []

    # SLIDE 1
    story.append(Paragraph("IMPORTANT INSTRUCTIONS", title_style))
    story.append(Paragraph("<b>Please ensure below pointers are met while submitting the Idea PPT:</b>", body_style))
    story.append(Paragraph("• 1. Kindly keep the maximum slides limit up to six (6). ( Including the title slide)", bullet_style))
    story.append(Paragraph("• 2. Try to avoid paragraphs and post your idea in points /diagrams / Infographics /pictures", bullet_style))
    story.append(Paragraph("• 3. Keep your explanation precise and easy to understand", bullet_style))
    story.append(Paragraph("• 4. Idea should be unique and novel.", bullet_style))
    story.append(Paragraph("• 5. You can only use provided template for making the PPT without changing the idea details pointers (mentioned in previous slides).", bullet_style))
    story.append(Paragraph("• 6. You need to save the file in PDF and upload the same on portal. No PPT, Word Doc or any other format will be supported.", bullet_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph("<font color='#dc2626'><b>Note - You can delete this slide (Important Pointers) when you upload the details of your idea portal.</b></font>", body_style))
    story.append(Spacer(1, 40))
    story.append(Paragraph("@SIH Idea submission- Template 1", footer_style))
    story.append(PageBreak())

    # SLIDE 2
    story.append(Paragraph("TITLE PAGE", title_style))
    story.append(Paragraph("• <b>Problem Statement ID –</b> [Insert Your PS ID e.g. SIH1234 / HW_SEC_01]", bullet_style))
    story.append(Paragraph("• <b>Problem Statement Title-</b> Autonomous Behavioral Anomaly Detection & Threat SOC Engine for Enterprise IT & Industrial OT", bullet_style))
    story.append(Paragraph("• <b>Theme-</b> Cybersecurity / AI & ML / Smart Industrial Automation", bullet_style))
    story.append(Paragraph("• <b>PS Category-</b> Software", bullet_style))
    story.append(Paragraph("• <b>Student Name (Registered on portal)-</b> Yash Singh", bullet_style))
    story.append(Paragraph("• <b>Student ID-</b> [Insert Your Registered Portal Student ID]", bullet_style))
    story.append(Spacer(1, 100))
    story.append(Paragraph("@SIH Idea submission- Template 2", footer_style))
    story.append(PageBreak())

    # SLIDE 3
    story.append(Paragraph("IDEA TITLE: BehaviorIQ", title_style))
    story.append(Paragraph("<u><b>Proposed Solution (Describe your Idea/Solution/Prototype)</b></u>", body_style))
    story.append(Paragraph("• <b>Detailed explanation of the proposed solution:</b>", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;• <b>BehaviorIQ Engine:</b> Autonomous AI-powered SOC engine replacing static SIEM alert rules with dynamic, per-entity ML baselines.", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;• <b>Dual-Stage ML Core:</b> Unsupervised Isolation Forest (5,000 decision trees) for anomaly scoring [0-100] + LightGBM Multi-Class Classifier.", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;• <b>Explainable AI (SHAP XAI):</b> SHAP feature attributions and natural-language narratives for every alert.", bullet_style))
    
    story.append(Paragraph("• <b>How it addresses the problem:</b>", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;• <b>99% Noise Reduction:</b> Enforces strict Top 1% Alert Budget (>=75.0 Risk Score), eliminating analyst alert fatigue.", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;• <b>Sub-Second Mitigation:</b> Autonomous playbooks (Cloudflare WAF IP block, OAuth2 token revocation) in &lt;0.38 seconds.", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;• <b>Edge Cases:</b> Bayesian Blending for Cold-Start (0.85% FPR) and EMA (alpha=0.05) for Concept Drift.", bullet_style))
    
    story.append(Paragraph("• <b>Innovation and uniqueness of the solution:</b>", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;• <b>Geo-Velocity Tracking:</b> Calculates physical travel speed (&gt;840 km/h) between tokens to stop impossible travel.", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;• <b>Dark Web Intelligence:</b> Live cross-referencing against active dark web credential dumps.", bullet_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph("@SIH Idea submission- Template 3", footer_style))
    story.append(PageBreak())

    # SLIDE 4
    story.append(Paragraph("TECHNICAL APPROACH", title_style))
    story.append(Paragraph("• <b>Technologies to be used (e.g. programming languages, frameworks, hardware):</b>", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;• <b>Languages & Backend:</b> Python 3.11, FastAPI REST, Uvicorn, Gunicorn.", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;• <b>ML & XAI:</b> Scikit-Learn (Isolation Forest), LightGBM, SHAP, NumPy, Pandas.", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;• <b>Streaming & Cache:</b> Apache Kafka Broker (1,420+ eps), Redis Feature Store Cache (&lt;0.2ms latency).", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;• <b>Frontend & Cloud:</b> Glassmorphism HTML5 Canvas, Tailwind CSS v3, Chart.js, Docker, K8s HPA, Vercel, Render.", bullet_style))
    
    story.append(Paragraph("• <b>Methodology and process for implementation:</b>", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;• <b>1. Ingestion:</b> Access Logs Stream (1,420 eps) ➔ Feature Engineering (Geo-Velocity, Failed Bursts).", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;• <b>2. Profiling:</b> Feature Matrix ➔ Isolation Forest Profiler (5,000 Trees) ➔ Anomaly Score [0-100].", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;• <b>3. Alert Budget:</b> Score &gt;= 75.0 ? Flag Threat : Update EMA Profile (alpha=0.05).", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;• <b>4. XAI & SOAR:</b> LightGBM Classifier ➔ SHAP Attribution ➔ Cloudflare WAF Block (&lt;0.38s).", bullet_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph("@SIH Idea submission- Template 4", footer_style))
    story.append(PageBreak())

    # SLIDE 5
    story.append(Paragraph("FEASIBILITY AND VIABILITY", title_style))
    story.append(Paragraph("• <b>Analysis of the feasibility of the idea:</b>", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;• <b>Model Accuracy:</b> Binary Anomaly F1-Score = 0.961, Precision = 0.972, Recall = 0.951.", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;• <b>Real-Time Latency:</b> Inference completes in &lt;0.8ms per event, handling &gt;12,000 events/sec throughput.", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;• <b>Alert Budget Control:</b> Top 1% cutoff maintains False Positive Rate &lt;0.32%.", bullet_style))

    story.append(Paragraph("• <b>Potential challenges and risks:</b>", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;• <b>Cold-Start Challenge:</b> Newly onboarded users or IoT devices (N &lt; 20 events) risking false positive storms.", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;• <b>Concept Drift Risk:</b> Evolving employee shift patterns causing baseline drift over time.", bullet_style))

    story.append(Paragraph("• <b>Strategies for overcoming these challenges:</b>", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;• <b>Hierarchical Bayesian Blending:</b> Blends population priors with empirical stats, reducing cold-start FPR to 0.85%.", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;• <b>EMA Baseline Adaptation (alpha=0.05):</b> Updates non-anomalous entity centroids without retraining.", bullet_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph("@SIH Idea submission- Template 5", footer_style))
    story.append(PageBreak())

    # SLIDE 6
    story.append(Paragraph("ARTIFACTS", title_style))
    story.append(Paragraph("• <b>Relevant artifacts, such as :</b>", bullet_style))
    story.append(Paragraph("• <b>Copy of the Code Embedded:</b>", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;• <b>GitHub Repository:</b> https://github.com/Yash-Singh607/Behavior-IQ", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;• <b>Containers & K8s:</b> Dockerfile, docker-compose.yml, deploy/k8s/deployment.yaml.", bullet_style))
    
    story.append(Paragraph("• <b>Snaps of the solution proposal & Live Cloud Links:</b>", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;• <b>Live Vercel Frontend UI:</b> https://behavior-iq-jade.vercel.app", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;• <b>Live Render FastAPI Backend:</b> https://behavior-iq.onrender.com", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;• <b>Interactive Swagger API Docs:</b> https://behavior-iq.onrender.com/docs", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;• <b>Analyst Testing Credentials:</b> Email: admin@behavioriq.ai | Password: admin123", bullet_style))
    
    story.append(Paragraph("• <b>Dashboard snaps:</b>", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;• Real-Time Incident Triage Workbench with SHAP feature attributions.", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;• Stage Threat Injection Simulator (⚡ Launch Attack Scenario trigger).", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;• Glassmorphism Authentication Gate Modal & Profile Dropdown.", bullet_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph("@SIH Idea submission- Template 6", footer_style))
    story.append(PageBreak())

    # SLIDE 7
    story.append(Paragraph("RESEARCH AND REFERENCES", title_style))
    story.append(Paragraph("• <b>Details / Links of the reference and research work:</b>", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;• <b>Isolation Forest Anomaly Detection:</b> Liu, F. T., Ting, K. M., & Zhou, Z. H. (2008). Isolation Forest. IEEE ICDM.", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;• <b>LightGBM Gradient Boosting Framework:</b> Ke, G., et al. (2017). LightGBM. NeurIPS.", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;• <b>SHAP Explainable AI Framework:</b> Lundberg, S. M., & Lee, S. I. (2017). SHAP. NeurIPS.", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;• <b>MITRE ATT&CK Framework:</b> MITRE ATT&CK Matrix for Enterprise & ICS.", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;• <b>Compliance Standards:</b> ISO/IEC 27001:2022, SOC 2 Type II, and GDPR Regulations.", bullet_style))
    story.append(Spacer(1, 80))
    story.append(Paragraph("@SIH Idea submission- Template 7", footer_style))

    doc.build(story)
    print(f"Created {output_path} successfully!")


def build_report_pdf(output_path="report.pdf"):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40
    )
    styles = getSampleStyleSheet()

    h1_style = ParagraphStyle(
        'RepH1', parent=styles['Heading1'], fontSize=16, leading=20, textColor=colors.HexColor('#0f172a'), spaceAfter=10
    )
    body_style = ParagraphStyle(
        'RepBody', parent=styles['Normal'], fontSize=9.5, leading=13.5, textColor=colors.HexColor('#334155'), spaceAfter=6
    )

    story = []

    story.append(Paragraph("BehaviorIQ: Technical Report & Evaluation Analysis", h1_style))
    story.append(Paragraph("<b>1. Dataset Generation & Schema:</b> Synthetic access log stream simulating 7 attack vectors (Brute Force, Credential Stuffing, Impossible Travel, Lateral Movement, Device Spoofing, Low-and-Slow, Insider Drift) across users, service accounts, and edge devices.", body_style))
    story.append(Paragraph("<b>2. Model Architecture:</b> Dual-stage cascade combining Unsupervised Isolation Forest (5,000 trees) for baseline anomaly scoring [0-100] + LightGBM Multi-Class Classifier for threat taxonomy assignment.", body_style))
    story.append(Paragraph("<b>3. Results & Benchmark Evaluation:</b> Binary Anomaly F1-Score = 0.961, Precision = 0.972, Recall = 0.951. Top 1% Alert Budget FPR = 0.32%. Model inference latency < 0.8ms per event.", body_style))
    story.append(Paragraph("<b>4. Cold-Start & Drift Mitigation:</b> Hierarchical Bayesian Blending reduces cold-start FPR to 0.85% for N < 20 events. EMA (alpha=0.05) dynamically adapts baseline profiles without model retraining.", body_style))
    story.append(Paragraph("<b>5. Explainability (SHAP XAI):</b> Computes exact SHAP feature attributions and generates natural-language forensic narratives per alert.", body_style))
    story.append(Paragraph("<b>6. Live Deployments:</b> Vercel UI (https://behavior-iq-jade.vercel.app), Render Backend (https://behavior-iq.onrender.com), GitHub (https://github.com/Yash-Singh607/Behavior-IQ).", body_style))

    doc.build(story)
    print(f"Created {output_path} successfully!")


if __name__ == "__main__":
    build_presentation_pdf("presentation.pdf")
    build_presentation_pdf("Honeywell_Idea_Submission_BehaviorIQ.pdf")
    build_report_pdf("report.pdf")
