import re
import spacy
import json
from flask import Flask, request, jsonify
from transformers import pipeline
from flask import Flask, jsonify, request
from flask_cors import CORS
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import os
import google.generativeai as genai


app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Home Route
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the RiskGPT Backend!"})



### UNSTRUCTURED DATA
# Load NLP Model
nlp = spacy.load("en_core_web_sm")

# Load Financial Sentiment Analysis Model
finbert = pipeline("text-classification", model="yiyanghkust/finbert-tone")

# Example Suspicious Terms (This can be extended)
SUSPICIOUS_TERMS = {
    "money laundering", "offshore", "sanctioned", "embezzlement",
    "tax evasion", "fraud", "shell company", "hawala", "Ponzi scheme",
    "bribery", "kickback", "corruption", "insider trading", "black market",
    "terrorism financing", "narcotics trafficking", "fake invoicing",
    "counterfeit goods", "tax haven", "trade-based money laundering",
    "front company", "ghost company", "smurfing", "structuring",
    "wire fraud", "identity theft", "cybercrime", "phishing",
    "extortion", "racketeering", "conflict of interest", "shell corporation",
    "false accounting", "illicit funds", "illicit transactions",
    "unexplained wealth", "beneficial ownership", "anonymous account",
    "dummy account", "false documentation", "forged documents",
    "politically exposed person (PEP)", "sanctions evasion",
    "unregistered securities", "trade diversion", "arms trafficking",
    "illicit enrichment", "concealment", "money mule", "underground banking",
    "misappropriation", "terrorist financing"
}
# Define Suspicious Terms Categories
HIGH_RISK_TERMS = {
    "terrorism financing", "arms trafficking", "sanctions evasion", "money laundering", "embezzlement",
    "tax evasion", "fraud", "hawala", "Ponzi scheme", "bribery", "kickback", "corruption", "insider trading",
    "black market", "narcotics trafficking", "trade-based money laundering", "wire fraud", "identity theft",
    "cybercrime", "phishing", "extortion", "racketeering", "false accounting", "illicit funds",
    "illicit transactions", "unexplained wealth", "forged documents", "terrorist financing", "unregistered securities",
    "trade diversion", "illicit enrichment", "money mule", "underground banking", "misappropriation"
}

MODERATE_RISK_TERMS = {
    "shell company", "front company", "ghost company", "smurfing", "structuring", "conflict of interest",
    "shell corporation", "beneficial ownership", "anonymous account", "dummy account", "false documentation",
    "concealment", "politically exposed person (PEP)", "sanctions evasion", "fake invoicing", "counterfeit goods"
}

LOW_RISK_TERMS = {
    "offshore", "sanctioned", "tax haven"
}

# Mocked Data from External Watchlists
SEC_EDGAR_COMPANIES = {"Bright Future Nonprofit Inc"}
FATF_COUNTRY = {
    "Algeria",
    "Angola",
    "Bulgaria",
    "Burkina Faso",
    "Cameroon",
    "Côte d'Ivoire",
    "Croatia",
    "Democratic Republic of Congo",
    "Haiti",
    "Kenya",
    "Lao People's Democratic Republic",
    "Lebanon",
    "Mali",
    "Monaco",
    "Mozambique",
    "Namibia",
    "Nepal",
    "Nigeria",
    "South Africa",
    "South Sudan",
    "Syria",
    "Tanzania",
    "Venezuela",
    "Vietnam",
    "Yemen",
    "Democratic People's Republic of Korea",
    "Iran",
    "Myanmar"
}


def load_sdn_list(file_path):
    try:
        df = pd.read_csv(file_path)
        return set(df.iloc[:, 1].dropna().str.strip())  # Taking the second column as SDN list
    except Exception as e:
        print(f"Error loading SDN List: {str(e)}")
        return set()

# SDN_LIST = {"abc"}
SDN_LIST = load_sdn_list("./sdn.csv")

# Function to extract country names from address
def extract_country(address):
    words = address.split()
    return words[-1] if words else "Unknown"

## Function to extract suspicious terms
def extract_suspicious_terms(text):
    detected_terms = set()
    for term in HIGH_RISK_TERMS.union(MODERATE_RISK_TERMS, LOW_RISK_TERMS):
        if term in text.lower():
            detected_terms.add(term)
    return list(detected_terms)

# Function to perform sentiment analysis
def financial_sentiment_analysis(text):
    sentiment = finbert(text)[0]
    label = sentiment['label']
    score = sentiment['score']
    return -1*score if label == "positive" else score


# Function to calculate risk score
# Risk scoring function
def calculate_risk(transaction):
    score = 0
    reasoning = []
    supporting_evidence = []

    transaction_id = transaction.get("Transaction ID", "Unknown")
    sender_name = transaction.get("Sender Name", "Unknown").strip()
    receiver_name = transaction.get("Receiver Name", "Unknown").strip()
    sender_address = transaction.get("Sender Address", "Unknown")
    receiver_address = transaction.get("Receiver Address", "Unknown")
    amount = transaction.get("Amount", 0)
    transaction_type = transaction.get("Transaction Type", "Unknown")
    additional_notes = " ".join(transaction.get("Additional Notes", []))

    # Sentiment Analysis Impact on Risk Score
    sentiment_score = financial_sentiment_analysis(additional_notes)
    score += sentiment_score * 8  # Adjust weight for smoother scaling
    reasoning.append(f"Sentiment analysis adjusted risk by {round(sentiment_score * 8, 2)}")

    # Suspicious Terms Scoring
    detected_terms = extract_suspicious_terms(additional_notes)
    term_score = sum(25 if term in HIGH_RISK_TERMS else 15 if term in MODERATE_RISK_TERMS else 5 for term in detected_terms)
    score += term_score * 0.8  # Apply a smoothing factor
    if detected_terms:
        reasoning.append(f"Suspicious terms detected: {', '.join(detected_terms)}")

    # Country-Based Risk Adjustments
    sender_country = extract_country(sender_address)
    receiver_country = extract_country(receiver_address)
    if sender_country in FATF_COUNTRY and receiver_country in FATF_COUNTRY:
        score += 12
        supporting_evidence.append("Both in FATF Watchlist")
    elif sender_country in FATF_COUNTRY or receiver_country in FATF_COUNTRY:
        score += 6
        supporting_evidence.append("FATF Watchlist")

    # Flagged Entities Risk
    if sender_name in SDN_LIST and receiver_name in SDN_LIST:
        score += 20
        supporting_evidence.append("OFAC SDN List")
    elif sender_name in SDN_LIST or receiver_name in SDN_LIST:
        score += 8
        supporting_evidence.append("OFAC SDN List")

    # Transaction Type Risk
    transaction_type_weights = {
        "Crypto Transfer": 12,
        "SWIFT Transfer": 8,
        "Wire Transfer": 4,
        "ACH Transfer": 0,
    }
    score += transaction_type_weights.get(transaction_type, 0)
    if transaction_type in transaction_type_weights:
        reasoning.append(f"Transaction type risk: {transaction_type}")

    # Transaction Amount Risk
    if amount > 40_000:
        score += 25
        reasoning.append("High transaction amount (>40K USD)")
    elif amount > 25_000:
        score += 18
        reasoning.append("Moderate-high transaction amount (>25K USD)")
    elif amount > 10_000:
        score += 8
        reasoning.append("Transaction amount above 10K USD")

    # Ensure Reasoning Is Not Empty
    if not reasoning:
        reasoning.append("No explicit risk detected.")

    # Cap the Score at 100
    score = min(score, 90)

    # Confidence Score Calculation with smoother scaling
    confidence_score = min(0.4 + (score / 180), 0.9)

    return {
        "Transaction ID": transaction_id,
        "Extracted Entities": {
            "Sender": sender_name,
            "Receiver": receiver_name
        },
        "Risk Score": round(score / 100, 2),
        "Supporting Evidence": supporting_evidence,
        "Confidence Score": round(confidence_score, 3),
        "Reason": " | ".join(reasoning)
    }



import re
import json


def  parse_transactions(text):
    transactions = text.strip().split("\n---\n")  # Split transactions
    parsed_transactions = []

    for transaction in transactions:
        try:
            data = {}

            # Extract fields using regex (with error handling)
            data["Transaction ID"] = re.search(r"Transaction ID:\s*(.+)", transaction)

            # Extract Sender Name (Fixing the regex)
            sender_match = re.search(r"Sender:\s*\n?\s*- Name:\s*([^\n]+)", transaction)
            data["Sender Name"] = sender_match.group(1).strip() if sender_match else "Unknown"


            # data["Sender Name"] = re.search(r"Sender:\s*- Name:\s*\"(.+)\"", transaction)
            data["Sender Account"] = re.search(r"- Account:\s*([\w\d\s]+)", transaction)
            data["Sender Address"] = re.search(r"- Address:\s*(.+)", transaction)

            receiver_match = re.search(r"Receiver:\s*\n?\s*- Name:\s*([^\n]+)", transaction)
            data["Receiver Name"] = receiver_match.group(1).strip() if receiver_match else "Unknown"

            # data["Receiver Name"] = re.search(r"Receiver:\s*- Name:\s*\"(.+)\"", transaction)
            data["Receiver Account"] = re.search(r"- Account:\s*([\w\d\s]+)", transaction)
            data["Receiver Address"] = re.search(r"- Address:\s*(.+)", transaction)
            data["Amount"] = re.search(r"Amount:\s*\$?([\d,]+)", transaction)

            # Convert extracted values (handle None cases)
            data["Transaction ID"] = data["Transaction ID"].group(1) if data["Transaction ID"] else "Unknown"
            # data["Sender Name"] = data["Sender Name"].group(1) if data["Sender Name"] else "Unknown"
            data["Sender Account"] = data["Sender Account"].group(1) if data["Sender Account"] else "Unknown"
            data["Sender Address"] = data["Sender Address"].group(1) if data["Sender Address"] else "Unknown"
            # data["Receiver Name"] = data["Receiver Name"].group(1) if data["Receiver Name"] else "Unknown"
            data["Receiver Account"] = data["Receiver Account"].group(1) if data["Receiver Account"] else "Unknown"
            data["Receiver Address"] = data["Receiver Address"].group(1) if data["Receiver Address"] else "Unknown"
            data["Amount"] = float(data["Amount"].group(1).replace(",", "")) if data["Amount"] else 0.0

            # Extract additional notes as a list
            additional_notes = re.findall(r"- \"(.+)\"", transaction)
            data["Additional Notes"] = additional_notes if additional_notes else []

            parsed_transactions.append(data)

            print(data)

        except Exception as e:
            print(f"⚠ Error parsing transaction: {e}\nTransaction Content:\n{transaction}\n")

    return parsed_transactions

# Flask Route for Processing Uploaded Text File
@app.route("/upload_transactions_unstructured", methods=["POST"])
def upload_transactions_unstructured():
    try:
        # Check if file is present in request
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]
        file_content = file.read().decode("utf-8")  # Read and decode file

        transactions = parse_transactions(file_content)
        results = [calculate_risk(txn) for txn in transactions]  # Process risk analysis

        return jsonify({"transactions": results}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


### STRUCTURED DATA
import pandas as pd
import re
import spacy
import json
from flask import Flask, request, jsonify
from sklearn.preprocessing import MinMaxScaler

nlp = spacy.load('en_core_web_sm')


# Function to extract risk keywords from transactions
def extract_risk_keywords(transactions):
    risk_keywords = set()
    for details in transactions:
        if pd.notna(details):
            doc = nlp(details.lower())
            risk_keywords.update([token.text for token in doc if token.pos_ in ['NOUN', 'VERB']])
    return risk_keywords

# Function to assess risk
def assess_risk(transaction, risk_keywords):
    details = str(transaction.get('Transaction Details', '')).lower()
    country = transaction.get('Receiver Country', '')
    amount = float(transaction.get('Amount', 0))
    receiver_country = float(transaction.get('Amount', 0))
    sender_name = str(transaction.get("Payer Name"))
    receiver_name = str(transaction.get("Receiver Name"))
    supporting_evidence = []
    score = 0

    # Risk Scoring Components
    keyword_risk = sum(kw in details for kw in risk_keywords) * 15
    offshore_risk = 25 if country in FATF_COUNTRY else 0
    amount_risk = min((amount / 1_000_000) * 10, 20)

    if receiver_country in FATF_COUNTRY:
        score += 12
        supporting_evidence.append("FATF Watchlist")

    # Flagged Entities Risk
    if sender_name in SDN_LIST and receiver_name in SDN_LIST:
        score += 20
        supporting_evidence.append("OFAC SDN List")
    elif sender_name in SDN_LIST or receiver_name in SDN_LIST:
        score += 8
        supporting_evidence.append("OFAC SDN List")

    risk_score = 0.4 * keyword_risk + 0.3 * offshore_risk + 0.3 * amount_risk

    # Confidence Score Calculation
    confidence_score = 0.6
    if keyword_risk > 0:
        confidence_score += 0.1
    if offshore_risk > 0:
        confidence_score += 0.1
    if amount > 100_000:
        confidence_score += 0.1

    confidence_score = min(0.3 + (risk_score / 180), 0.9)

    return risk_score, confidence_score, supporting_evidence

# Flask Route to Handle CSV Upload and Risk Assessment
@app.route('/upload_transactions_structured', methods=['POST'])
def upload_transactions_structured():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if not file.filename.endswith('.csv'):
        return jsonify({"error": "Invalid file format. Please upload a CSV file."}), 400

    # Read CSV File
    try:
        data = pd.read_csv(file)
    except Exception as e:
        return jsonify({"error": f"Failed to read CSV file: {str(e)}"}), 400

    # Extract Risk Keywords
    risk_keywords = extract_risk_keywords(data['Transaction Details'])

    # Apply Risk Assessment
    results = []
    for _, row in data.iterrows():
        risk_score, confidence_score, supporting_evidence = assess_risk(row, risk_keywords)

        results.append({
            "Transaction ID": row.get('Transaction ID', 'Unknown'),
            "Extracted Entities": {  # ✅ Ensure this matches the frontend
                "Sender": row.get('Payer Name', 'Unknown'),
                "Receiver": row.get('Receiver Name', 'Unknown')
            },
            "Risk Score": round(risk_score / 100, 2),
            "Supporting Evidence": supporting_evidence,
            "Confidence Score": round(confidence_score, 2),
            "Reason": f"{row.get('Receiver Name', 'Unknown')} may have offshore transactions."
        })

    return jsonify({"transactions": results}), 200


# 🔹 Configure Gemini API Key
GENAI_API_KEY = "AIzaSyAp1m8kAbPPrCiXzCHN-aYk9SlPKkX4UnA"  # 🔴 Replace with your actual Gemini API key
genai.configure(api_key=GENAI_API_KEY)

# 🔹 Load Gemini Model

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-8b",
    generation_config=generation_config,
)

@app.route("/generate_summary", methods=["POST"])
def generate_summary():
    try:
        transaction = request.json.get("transaction", {})
        transaction_id = transaction.get("Transaction ID", "Unknown")

        if not transaction:
            return jsonify({"error": "No transaction data provided"}), 400

        # Construct input prompt for Gemini AI
        prompt = f"""
        Summarize the risk assessment for the following transaction:

        Transaction ID: {transaction_id}
        Sender: {transaction.get('Extracted Entities', {}).get('Sender', 'Unknown')}
        Receiver: {transaction.get('Extracted Entities', {}).get('Receiver', 'Unknown')}
        Risk Score: {transaction.get('Risk Score', 'N/A')}
        Confidence Score: {transaction.get('Confidence Score', 'N/A')}
        Supporting Evidence: {', '.join(transaction.get('Supporting Evidence', []))}
        Reason: {transaction.get('Reason', 'N/A')}

        Provide a brief summary that highlights potential concerns. Also search Wikipedia for possible concerns regarding both the companies. Answer in bullet points and plain text and don't write "**" anywhere and limit it to 60 words. 
        """

        response = model.generate_content(prompt)
        summary = response.text.strip()

        return jsonify({"summary": summary})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Run Flask App
if __name__ == "__main__":
    app.run(debug=True, port=8080)