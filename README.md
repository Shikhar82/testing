🗣️ Spoken AI Chatbot with Python, Streamlit & CI/CD Pipeline
This project demonstrates how to build a Spoken English AI Chatbot using Python and Streamlit, integrated with a DevOps CI/CD pipeline using GitHub, Jenkins, SonarQube, OWASP Dependency-Check, and Docker.

🚀 Features
🎙️ AI-powered Spoken English chatbot

🐍 Built with Python and Streamlit

🔁 Automated CI/CD Pipeline

✅ Code Quality Check with SonarQube

🛡️ Security scan with OWASP Dependency-Check

🐳 Dockerized for easy deployment

🛠️ Tech Stack
Frontend: Streamlit

Backend: Python

CI/CD: GitHub + Jenkins

Code Quality: SonarQube

Security: OWASP Dependency-Check

Containerization: Docker

🔄 CI/CD Pipeline Overview
Code Commit: Developer pushes code to GitHub.

Jenkins Trigger: Jenkins pipeline starts automatically.

Dependency Installation: Python packages installed via requirements.txt.

Code Quality Check: SonarQube performs static analysis.

Security Scan: OWASP Dependency-Check scans for known vulnerabilities.

Docker Build: Application is containerized using Docker.

Deployment: Docker container is run with exposed Streamlit app.

📂 Project Structure
bash
Copy
Edit
.
├── app.py                   # Streamlit application
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker configuration
├── Jenkinsfile              # Jenkins pipeline definition
├── sonar-project.properties # SonarQube config
├── README.md
🐳 Run Locally with Docker
bash
Copy
Edit
docker build -t spoken-ai-chatbot .
docker run -p 8501:8501 spoken-ai-chatbot
Then open your browser at http://localhost:8501.

✅ Prerequisites
Python 3.8+

Docker

Jenkins server with required plugins

SonarQube server

OWASP Dependency-Check CLI