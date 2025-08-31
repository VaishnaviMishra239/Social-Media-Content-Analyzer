import React, { useEffect, useState } from "react";
import FileUpload from "./components/FileUpload";
import "./App.css";

function App() {
  const [theme, setTheme] = useState("light");

 
  useEffect(() => {
    const saved = localStorage.getItem("theme");
    const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
    const initial = saved || (prefersDark ? "dark" : "light");
    setTheme(initial);
    document.documentElement.setAttribute("data-theme", initial);
  }, []);


  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme((t) => (t === "light" ? "dark" : "light"));
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>📊 Social Media Content Analyzer</h1>
          <button onClick={toggleTheme} style={{ fontSize: "12px", width: "130px",height: "35px",  position: 'absolute', top: 20, right: 20}}>
          {theme === "light" ? "🌙 Dark Mode" : "☀️ Light Mode"}
        </button>
        <p className="subtitle">Upload your post & get instant insights</p>

      </header>

      <main>
        <div className="card">
          <FileUpload />
        </div>
      </main>

      <footer className="app-footer">
        <p>Made with ❤️ for the Technical Assessment</p>
      </footer>
    </div>
  );
}

export default App;
