import os
import zipfile

def zip_submission_files(zip_filename="AI_Behavioral_Anomaly_Detection.zip"):
    # Target files & folders to include
    include_files = [
        "requirements.txt",
        "README.md",
        "report.pdf",
        "presentation.pdf",
        "Honeywell_Idea_Submission_BehaviorIQ.pdf",
        "Honeywell_Idea_Submission_BehaviorIQ.docx",
        "Dockerfile",
        "docker-compose.yml",
        "render.yaml",
        "vercel.json",
        "run_demo.py"
    ]

    include_dirs = ["src", "data", "models", "app", "deploy", "presentation"]

    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in include_files:
            if os.path.exists(file):
                zipf.write(file, arcname=file)

        for folder in include_dirs:
            if os.path.exists(folder):
                for root, dirs, files in os.walk(folder):
                    if "__pycache__" in root:
                        continue
                    for f in files:
                        if f.endswith(".pyc"):
                            continue
                        file_path = os.path.join(root, f)
                        arcname = os.path.relpath(file_path, ".")
                        zipf.write(file_path, arcname=arcname)

    print(f"Submission ZIP created successfully at {zip_filename}")

if __name__ == "__main__":
    zip_submission_files("AI_Behavioral_Anomaly_Detection.zip")
    zip_submission_files("BehaviorIQ_Submission.zip")
