import React, { useState } from "react";
import axios from "axios";
import "./RiskAnalysis.css";
import loadingGif from "./loading.gif";

function RiskAnalysis() {
  const [file, setFile] = useState(null);
  const [fileType, setFileType] = useState("csv");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [summaryData, setSummaryData] = useState({});
  const [activeSummary, setActiveSummary] = useState(null);
  const [loadingSummary, setLoadingSummary] = useState(false);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleFileTypeChange = (event) => {
    setFileType(event.target.value);
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a file to upload.");
      return;
    }

    setLoading(true);
    setError("");

    const formData = new FormData();
    formData.append("file", file);

    const endpoint =
      fileType === "csv"
        ? "http://127.0.0.1:8080/upload_transactions_structured"
        : "http://127.0.0.1:8080/upload_transactions_unstructured";

    try {
      const response = await axios.post(endpoint, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResults(response.data.transactions || response.data);
    } catch (error) {
      setError("Failed to process the file. Please try again.");
    }

    setLoading(false);
  };

  const generateTransactionSummary = async (transactionId) => {
    if (!transactionId || !results.length) {
      setError("Invalid transaction selected.");
      return;
    }

    setLoadingSummary(true);
    setSummaryData((prev) => ({ ...prev, [transactionId]: "Generating..." }));

    setTimeout(async () => {
      try {
        const response = await axios.post("http://127.0.0.1:8080/generate_summary", {
          transaction: results.find((txn) => txn["Transaction ID"] === transactionId),
        });
        setSummaryData((prev) => ({ ...prev, [transactionId]: response.data.summary }));
      } catch (error) {
        setSummaryData((prev) => ({ ...prev, [transactionId]: "Failed to generate summary." }));
      }

      setLoadingSummary(false);
      setActiveSummary(transactionId);
    }, 1500);
  };

  return (
    <div className="risk-analysis-container">
      <h2>Risk Assessment Evaluation</h2>

      <div className="input-group">
        <label>Select File Type:</label>
        <select value={fileType} onChange={handleFileTypeChange}>
          <option value="csv">CSV (Structured Data)</option>
          <option value="txt">TXT (Unstructured Data)</option>
        </select>
      </div>

      <div className="file-upload">
        <input type="file" accept={fileType === "csv" ? ".csv" : ".txt"} onChange={handleFileChange} />
        <button onClick={handleUpload} disabled={loading}>
          {loading ? "Uploading..." : "Upload & Process"}
        </button>
      </div>

      {error && <p className="error-message">{error}</p>}

      {results.length > 0 && (
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Transaction ID</th>
                <th>Sender</th>
                <th>Receiver</th>
                <th>Risk Score</th>
                <th>Confidence Score</th>
                <th>Source</th>
                <th>Reason</th>
              </tr>
            </thead>
            <tbody>
              {results.map((result) => (
                <tr key={result["Transaction ID"]}>
                  <td>{result["Transaction ID"]}</td>
                  <td>{result["Extracted Entities"]?.Sender || "N/A"}</td>
                  <td>{result["Extracted Entities"]?.Receiver || "N/A"}</td>
                  <td>{result["Risk Score"]}</td>
                  <td>{result["Confidence Score"]}</td>
                  <td>{result["Supporting Evidence"]?.join(", ") || "N/A"}</td>
                  <td>
                    <button onClick={() => generateTransactionSummary(result["Transaction ID"]) }>
                      View Details
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {loadingSummary && (
        <div className="loading-overlay">
          <img src={loadingGif} alt="Loading..." className="loading-gif" />
        </div>
      )}

      {activeSummary && (
        <div className="popup-overlay">
          <div className="popup-box" style={{ textAlign: "left" }}>
            <h3>Reason for {activeSummary}</h3>
            <div>
              {summaryData[activeSummary]?.split("\n").map((point, index) => (
                <p key={index}>{point}</p>
              ))}
            </div>
            <button className="close-button" onClick={() => setActiveSummary(null)}>
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default RiskAnalysis;
