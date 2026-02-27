const form = document.getElementById("urlForm");
const resultDiv = document.getElementById("result");
const errorDiv = document.getElementById("error");
const submitBtn = document.getElementById("submitBtn");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const longUrl = document.getElementById("longUrl").value.trim();

  errorDiv.textContent = "";
  resultDiv.innerHTML = "";
  submitBtn.disabled = true;

  try {
    const response = await fetch("/api/short_url", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ long_url: longUrl }),
    });

    const data = await response.json();

    if (response.ok) {
      const shortUrl = data.link;
      const creationCount = data.creation_count; // ← получаем link и creation_count из ручки
      resultDiv.innerHTML = `
        <strong>Short URL:</strong>
        <div style="display: flex; align-items: center; gap: 10px; margin-top: 5px; flex-wrap: wrap;">
            <a href="${shortUrl}" target="_blank" style="flex-grow: 1; word-break: break-all;">${shortUrl}</a>
            <button id="copyBtn">📋 Copy</button>
        </div>
        <div style="margin-top: 10px; font-size: 0.9em; color: #555;">
            This link has been generated <strong>${creationCount}</strong> time(s).
        </div>
        `;
      document.getElementById("copyBtn").addEventListener("click", async () => {
        const success = await copyToClipboard(shortUrl);
        if (success) {
          const btn = document.getElementById("copyBtn");
          btn.textContent = "✓ Copied!";
          btn.style.background = "#218838";
          setTimeout(() => {
            btn.textContent = "📋 Copy";
            btn.style.background = "#28a745";
          }, 2000);
        } else {
          alert("Failed to copy URL");
        }
      });
    } else if (response.status === 429) {
      errorDiv.textContent =
        data.detail ||
        "You have exceeded your request limit. Please try again later.";
    } else if (response.status === 422) {
      errorDiv.textContent = data.detail || "Invalid URL.";
    } else {
      errorDiv.textContent = data.detail || "Failed to shorten URL.";
    }
  } catch (err) {
    errorDiv.textContent = "Network error. Is the server running?";
    console.error(err);
  } finally {
    submitBtn.disabled = false;
  }
});
