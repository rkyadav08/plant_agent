# 🌿 Modular Plant Doctor AI – 6-Agent Multi-Modal System  
*(Streamlit + Gemini 2.5 Flash Preview)*

[![Streamlit](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit)](#)
[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](#)
[![Gemini](https://img.shields.io/badge/Powered_by-Gemini_2.5_Flash-00A6FF?logo=google)](#)

---

## 🔗 **Live Deployment**
👉 **App Link:** *https://plantagent-9kqusvtm25jpkp2jvswjhu.streamlit.app/*

---

## 🧠 Overview

The **Modular Plant Doctor AI** is a **6-Agent multi-modal pipeline** capable of diagnosing plant diseases using:

- 🌱 Plant Image (mandatory)  
- 🧪 Soil Report PDF (optional)  
- 🌐 Multi-language output (English, Hindi, Marathi)  
- 💬 Follow-up Chat Agent  

Powered by **Gemini 2.5 Flash Preview (2025)** for fast multi-modal reasoning.

---

## ⚙️ Key Features

### 🔹 **6-Agent Architecture**
| Agent | Role |
|-------|------|
| **1. Visual ID Agent** | Identifies plant + detects visual symptoms |
| **2. Soil Analysis Agent** | Extracts & interprets PDF soil reports |
| **3. Diagnostic Agent** | Combines visual + soil findings into final diagnosis |
| **4. Treatment Agent** | Generates step-by-step treatment plan |
| **5. Recovery Agent** | Provides fast recovery & long-term maintenance tips |
| **6. Chat Agent** | Answers follow-up questions using report context only |

---

## 🌐 Multi-Language Output

UI & AI outputs available in:
- English  
- Hindi  
- Marathi  

(Extendable to more Indian languages easily)

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **Streamlit**
- **Google Gemini 2.5 Flash**
- **Requests API**
- **Base64 encoding**
- **Mock Vector DB using Streamlit session state**

---

git clone https://github.com/YOUR-USERNAME/plant-doctor-ai.git
cd plant-doctor-ai
