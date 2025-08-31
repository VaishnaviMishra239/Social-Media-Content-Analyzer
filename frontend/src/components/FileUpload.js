import React, { useState } from "react";

function FileUpload() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleUpload = async () => {
    if (!file) return;

    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error("Error uploading file:", error);
    }

    setLoading(false);
  };

 
  const formatText = (text) => {
    if (!text) return "No text found";

    return text.split("\n").map((line, i) => (
      <p key={i} style={{ margin: "4px 0" }}>
        {line}
      </p>
    ));
  };

  const getSentimentClass = (sentiment) => {
    if (sentiment === "positive") return "sentiment-positive";
    if (sentiment === "negative") return "sentiment-negative";
    return "sentiment-neutral";
  };

  return (
    <div>
      {/* File Upload Section */}
      <label
        htmlFor="fileUpload"
        style={{ marginLeft: "10px", fontWeight: "bold", fontSize: "1.2rem" }}
      >
        Choose a file to analyze:
      </label>
      <br />
      <input
        style={{ marginLeft: "100px", color: "cadetblue" }}
        id="fileUpload"
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
        aria-label="File upload input"
      />

      <br />
      <button onClick={handleUpload} disabled={!file}>
        {loading ? "Analyzing..." : "Upload & Analyze"}
      </button>

      {/* Results Section */}
      {result && (
        <div
          style={{
            marginTop: "20px",
            textAlign: "left",
            background: "var(--card-bg)",
            padding: "15px",
            borderRadius: "8px",
          }}
        >
          <h3>📄 Extracted Text</h3>
          <div
            style={{
              whiteSpace: "pre-wrap",
              padding: "10px",
              borderRadius: "8px",
              background: "var(--content-bg)",
              color: "var(--text-color)",
            }}
          >
            {formatText(result.content)}
          </div>

          {/* Analysis Section */}
          {result.analysis && (
            <>
              <h3>🔍 Analysis</h3>
              <p>
                <strong>Sentiment: </strong>
                <span className={getSentimentClass(result.analysis.sentiment)}>
                  {result.analysis.sentiment}
                </span>
              </p>
              <p>
                <strong>Polarity:</strong>{" "}
                {result.analysis.polarity.toFixed(2)}
              </p>

              <p>
                <strong>Top Keywords:</strong>
              </p>
              <div>
                {result.analysis.keywords.length > 0 ? (
                  result.analysis.keywords.map((k, i) => (
                    <span
                      key={i}
                      className="keyword-tag"
                      style={{
                        marginRight: "8px",
                        background: "var(--tag-bg)",
                        color: "var(--tag-text)",
                        padding: "3px 6px",
                        borderRadius: "6px",
                        fontSize: "0.9rem",
                      }}
                    >
                      #{k}
                    </span>
                  ))
                ) : (
                  <span>None</span>
                )}
              </div>

              <h3>💡 Suggestions</h3>
              <ul>
                {result.analysis.suggestions.map((s, i) => (
                  <li key={i}>{s}</li>
                ))}
              </ul>
            </>
          )}
        </div>
      )}
    </div>
  );
}

export default FileUpload;
