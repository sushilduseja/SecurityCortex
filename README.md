# AI Governance Dashboard

An AI-powered dashboard for managing AI governance, risk assessment, and compliance workflows.

## Overview

The AI Governance Dashboard provides a comprehensive solution for organizations to manage the governance, risk, and compliance aspects of their AI systems. It leverages AI agents to automate key governance tasks, assess risks, monitor compliance, and generate insightful reports.

![AI Governance Dashboard](assets/logo.svg)

## Key Features

- **AI-Powered Governance**: Automatically generate governance policies and identify governance gaps
- **Risk Assessment**: Assess AI risks using NLP to analyze model documentation
- **Compliance Monitoring**: Track compliance metrics in real-time with anomaly detection
- **Automated Reporting**: Generate comprehensive reports with AI-driven insights
- **Intuitive Interface**: Clean, professional UI with minimal clicks required

## Architecture

The dashboard is built with a modern, modular architecture:

- **Frontend**: Streamlit-based interactive UI
- **Backend**: FastAPI RESTful API
- **AI Agents**: NLP-powered agents for governance, risk, monitoring, and reporting
- **Database**: SQLite for lightweight data storage

## AI Agents

The system uses four specialized AI agents:

1. **Governance Agent**: Automates policy generation and governance gap analysis
2. **Risk Assessment Agent**: Uses NLP to classify AI risks based on documentation
3. **Monitoring Agent**: Continuously tracks compliance metrics and flags anomalies
4. **Reporting Agent**: Generates automated compliance reports with insights

## Getting Started

### Prerequisites

- Python 3.8+
- Required libraries: streamlit, fastapi, huggingface transformers, pandas, plotly, etc.

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-org/ai-governance-dashboard.git
   cd ai-governance-dashboard
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:

   Start the backend API:
   ```
   python -m api.main
   ```

   Start the Streamlit frontend (in a separate terminal):
   ```
   streamlit run app.py
   ```

4. Open your browser and navigate to `http://localhost:5000`

## Usage

### Governance Management

- View and manage governance policies
- Generate new policies using AI
- Identify governance gaps

### Risk Assessment

- Assess AI risks from model documentation
- Analyze risk factors across different categories
- Identify high-risk AI systems

### Compliance Monitoring

- Monitor compliance metrics in real-time
- Set up automated alerts for compliance issues
- Track compliance status across AI systems

### Reporting

- Generate comprehensive governance reports
- Get AI-driven insights and recommendations
- Export reports in various formats

## Project Structure

