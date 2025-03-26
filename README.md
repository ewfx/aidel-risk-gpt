# 🚀 RiskGPT

## 📌 Table of Contents
- [Introduction](#introduction)
- [Demo](#demo)
- [Inspiration](#inspiration)
- [What It Does](#what-it-does)
- [How We Built It](#how-we-built-it)
- [Challenges We Faced](#challenges-we-faced)
- [How to Run](#how-to-run)
- [Tech Stack](#tech-stack)
- [Team](#team)

---

## 🎯 Introduction
Our project focuses on transaction risk analysis, aiming to detect fraudulent or high-risk transactions in financial data. We utilize data preprocessing, statistical analysis, and AI techniques to identify suspicious patterns and anomalies.

## 🎥 Demo
🔗 [Live Demo](#) (if applicable)  
📹 [Video Demo](#) (if applicable)  
🖼️ Screenshots:

<img width="1432" alt="image" src="https://github.com/user-attachments/assets/09292ef2-3ff5-4c7c-b4fb-9f3da8a3b095" />
<img width="1438" alt="image" src="https://github.com/user-attachments/assets/c4bba139-1e4f-445d-adec-52dfdefcfed7"/>
<img width="1429" alt="image" src="https://github.com/user-attachments/assets/44b03f0a-cb40-4012-bb30-991de6c9a7e0"/>
<img width="1424" alt="image" src="https://github.com/user-attachments/assets/967d5411-08a6-4490-a6e0-c4d78c3dab34" />
<img width="1432" alt="image" src="https://github.com/user-attachments/assets/cfb916e8-ac1e-4ceb-98a0-00c7d7d81371" />

## 💡 Inspiration
Traditional fraud detection methods rely on static rules, making them ineffective against evolving fraud patterns. This project leverages AI to provide a dynamic, intelligent fraud detection system that adapts to new threats in real-time. 

## ⚙️ What It Does
1. Natural Language Processing (NLP) for Anomaly Detection
	•	Implements spaCy and Hugging Face Transformers for advanced NLP-based fraud analysis.
	•	Identifies suspicious descriptions and unusual transaction behaviors.
2. Real-time API Integration
	•	Built using Flask, providing a RESTful API for easy integration with financial systems.
	•	Supports Flask-CORS for secure cross-origin communication.
3.	Automated Data Processing & Cleaning
	•	Handles missing values intelligently by replacing them with meaningful estimates.
	•	Uses Pandas for efficient data transformation and processing.
4.	AI-Powered Insights
	•	Utilizes Google Generative AI for enhanced predictive analysis.
	•	Offers adaptive fraud detection that evolves with new data patterns.

## 🛠️ How We Built It
This project leverages a combination of machine learning, natural language processing (NLP), and web technologies to detect fraud in financial transactions. The key technologies and frameworks used include:
	•	Programming Languages: Python
	•	Machine Learning & NLP: Scikit-learn, Transformers (Hugging Face), spaCy
	•	Web Framework: Flask (for building APIs)
	•	Frontend Support: Flask-CORS (for handling cross-origin requests)
	•	Data Processing: Pandas, MinMaxScaler (for normalization)

## 🚧 Challenges We Faced
We thought of calling a proper LLM to summarise the risk reasoning. We had to choose which one could process the transactions based on the input and output cost. In web scraping, Google has restricted automated web-scraping calls, hence we ultimately used Google Gemini to further analyse the company's Wikipedia information. Processing the text as an input also took a lot of time for debugging. 

## 🏃 How to Run
1. Clone the repository  
   ```sh
   git clone https://github.com/samyakbakliwal7/RiskGPT.git
   ```
2. Install dependencies  
   ```sh
   npm install
   pip install re spacy flask transformers flask-cors scikit-learn pandas google-generativeai
   
   ```
3. Run the project  
   ```sh
   npm run build
   npm start

   python RiskAnalysisBackend.py
   ```

## 🏗️ Tech Stack
- 🔹 Frontend: React
- 🔹 Backend: Flask
- 🔹 Database: N/A
- 🔹 Other: Google Gemini API: gemini-1.5-flash-8b

## 👥 Team
- **Samyak Bakliwal** - [[GitHub](https://github.com/samyakbakliwal7)](#) | [LinkedIn](#)
- **Aakriti Saraogi** - [[GitHub](#)](https://github.com/aakritisaraogi) | [LinkedIn](#)
- **Atharva Marathe** - [[GitHub](#)](https://github.com/atharvamarathe) | [LinkedIn](#)
- **Wandari Blah** - [GitHub](#) | [LinkedIn](#)
