import { useState, useEffect } from "react";
import { motion } from "framer-motion";

const Homepage = () => {
  const [backendStatus, setBackendStatus] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8080/")
      .then((response) => {
        if (response.ok) {
          setBackendStatus(true);
        } else {
          setBackendStatus(false);
        }
      })
      .catch(() => setBackendStatus(false));
  }, []);

  return (
    <div style={{ minHeight: "100vh", backgroundColor: "#f5f5f5", color: "#000", textAlign: "center", padding: "20px", position: "relative" }}>
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
      >
        <h1 style={{ fontSize: "2rem", fontWeight: "bold" }}>Welcome to RiskGPT</h1>
        <p style={{ marginTop: "10px", fontSize: "1.2rem", color: "#555" }}>
          AI-Driven Entity Intelligence and Risk Analysis
        </p>
        <img src="/Icons/analytics.gif" alt="App Icon" style={{ height: "75px", width: "75px" }} />

        {/* Main Content */}
        <p style={{ marginTop: "20px", fontSize: "1.2rem", color: "#444" }}>
          RiskGPT is an AI-driven platform designed to analyze entity risk using advanced machine learning and AI algorithms.
          <h2 style={{ fontSize: "1.5rem", fontWeight: "bold", marginTop: "20px" }}>
            Key Benefits of RiskGPT
          </h2>
          <ul style={{ listStyle: "none", padding: "0", marginTop: "10px" }}>
            <li style={{ display: "flex", alignItems: "center", gap: "10px" }}>
              ✅ <strong>Faster Analysis</strong> – Finds risk factors in minutes instead of days.
              <img src="/Icons/fasterAnalysis.png" alt="Faster Analysis" style={{ height: "50px", width: "50px" }} />
            </li>
            <li style={{ display: "flex", alignItems: "center", gap: "10px" }}>
              ✅ <strong>More Accurate</strong> – Reduces human errors in verifying companies.
              <img src="/Icons/Accurate.png" alt="More Accurate" style={{ height: "50px", width: "50px" }} />
            </li>
            <li style={{ display: "flex", alignItems: "center", gap: "10px" }}>
              ✅ <strong>Real-time Updates</strong> – Keeps track of changing risk factors.
              <img src="/Icons/updates.png" alt="Real-time Updates" style={{ height: "50px", width: "50px" }} />
            </li>
            <li style={{ display: "flex", alignItems: "center", gap: "10px" }}>
              ✅ <strong>Automated Decision Support</strong> – Helps analysts take quick action.
              <img src="/Icons/quickAction.png" alt="Automated Decision Support" style={{ height: "50px", width: "50px" }} />
            </li>
          </ul>
        </p>
      </motion.div>

      {/* Backend Status Box in Bottom-Right */}
      <motion.div
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.8 }}
        style={{
          position: "fixed",
          bottom: "20px",
          right: "20px",
          backgroundColor: "#222",
          color: "#fff",
          padding: "10px 15px",
          borderRadius: "8px",
          boxShadow: "0px 4px 10px rgba(0, 0, 0, 0.2)",
          fontSize: "14px",
        }}
      >
        Backend status:{" "}
        {backendStatus === null ? (
          <span style={{ color: "#f1c40f" }}>Checking...</span>
        ) : backendStatus ? (
          <span style={{ color: "#2ecc71" }}>✅ Up and running</span>
        ) : (
          <span style={{ color: "#e74c3c" }}>❌ Down</span>
        )}
      </motion.div>
    </div>
  );
};

export default Homepage;
