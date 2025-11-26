🌿 Modular Plant Doctor AI Agent (6-Agent System)

This is a multi-modal Streamlit application that utilizes a sophisticated 6-Agent architecture based on the Gemini API to provide comprehensive plant health analysis, disease diagnosis, and structured treatment plans. It supports image input, optional PDF soil report analysis, and multilingual output.

✨ Key Features

6-Agent Modular Architecture: Breaks down the diagnosis process into distinct, verifiable steps (parallel and series execution).

Multi-Modal Input: Accepts both a Plant Image (JPEG/PNG) and an Optional PDF Soil Report for comprehensive analysis.

Real-Time Localization: Supports full UI and analysis output in multiple languages, including English, Hindi, and Marathi.

Session Management (Mock VDB): Implements session tracking to save and display analysis history for the current user, simulating persistent storage and access management.

Post-Analysis Chat: Allows users to ask follow-up questions about the generated report using a dedicated Chat Agent (Agent 6).

Deployment Ready: API Key is securely loaded via the GEMINI_API_KEY environment variable.

🚀 Deployment Link

Live Application: [PASTE YOUR DEPLOYMENT LINK HERE]

🏗️ 6-Agent Architecture Overview

The application uses a hybrid parallel and series execution flow to ensure a thorough, cross-referenced diagnosis.

Parallel Execution Path:

Agent 1 (Visual ID Agent): Analyzes the uploaded plant image to identify the plant type and visual symptoms.

Agent 2 (Soil Analysis Agent): Extracts and summarizes data from the optional PDF Soil Report (or provides a placeholder if none is given).

Series Execution Path:

Agent 3 (Diagnostic Agent): Merges the outputs from Agent 1 and Agent 2 to determine the primary disease or nutrient deficiency.

Agent 4 (Treatment Agent): Generates a detailed, step-by-step treatment plan, prioritizing soil corrective actions if imbalances were found by Agent 2.

Agent 5 (Recovery Agent): Provides 3-5 clear tips for fast recovery and long-term preventative care.

Post-Analysis Agent:

Agent 6 (Chat Agent): Activated after the analysis is complete, allowing the user to query the final report for clarification or elaboration.

🛠️ Setup and Installation

Prerequisites

Python: Ensure you have Python 3.8+ installed.

API Key: Obtain a Gemini API Key.

Installation

# Clone or download the plant_agent.py file
# Install required libraries
pip install streamlit requests


Secure Deployment Setup

For deployment (or secure local testing), the application requires the API key to be set as an environment variable:

Variable Name

Value

Description

GEMINI_API_KEY

YOUR_API_KEY_HERE

Your Google AI Studio API Key.

Local Setup (Linux/macOS):

export GEMINI_API_KEY="YOUR_API_KEY_HERE"


Local Setup (Windows - Command Prompt):

set GEMINI_API_KEY="YOUR_API_KEY_HERE"


Running the App Locally

Execute the Streamlit application:

streamlit run plant_agent.py


🧑‍💻 How to Use

Configuration (Sidebar): The application will automatically check for the GEMINI_API_KEY. Select your desired Output Language (e.g., Hindi, Marathi).

Input Data (Section 1):

Upload Plant Image: Drag and drop a clear image showing the affected plant or symptoms. (Mandatory)

Upload Soil Report: Upload a PDF file containing lab results or soil analysis data (Optional).

Start Analysis: Click the 🔬 Start 6-Agent Modular Analysis button.

Review Report (Section 2): The final report will be displayed. Use the Download button to save it as a Markdown file.

Follow-up Chat (Section 3): The chat interface will appear. Ask specific questions about the report.
https://plantagent-9kqusvtm25jpkp2jvswjhu.streamlit.app/
