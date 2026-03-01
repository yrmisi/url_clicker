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
    const response = await fetch("/api/short_url?html=true", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ long_url: longUrl }),
    });

    if (response.ok) {
      // html=true → всегда HTML фрагмент
      resultDiv.innerHTML = await response.text();
      attachCopyHandler();
    } else {
      // Ошибки → всегда JSON
      const data = await response.json();
      errorDiv.textContent = data.detail || getErrorMessage(response.status);
    }
  } catch (err) {
    errorDiv.textContent = "Network error. Is the server running?";
    console.error(err);
  } finally {
    submitBtn.disabled = false;
  }
});

function attachCopyHandler() {
  const copyBtn = document.getElementById("copyBtn");
  if (copyBtn && !copyBtn.dataset.handlerAttached) {
    copyBtn.dataset.handlerAttached = "true";

    copyBtn.addEventListener("click", async () => {
      const shortUrl = copyBtn.dataset.shortUrl;
      const copiedSuccess = copyBtn.dataset.copiedSuccess || "✓ Copied!";
      const copyError = copyBtn.dataset.copyError || "Failed to copy URL";

      if (!shortUrl) {
        alert(copyError);
        return;
      }

      const success = await copyToClipboard(shortUrl);
      if (success) {
        const originalText = copyBtn.textContent;
        copyBtn.textContent = copiedSuccess;  // ← Из бэкенда!
        copyBtn.style.background = "#218838";
        setTimeout(() => {
          copyBtn.textContent = originalText;
          copyBtn.style.background = "#28a745";
        }, 2000);
      } else {
        alert(copyError);  // ← Из бэкенда!
      }
    });
  }
}

function getErrorMessage(status) {
  return (
    {
      429: "Rate limit exceeded",
      422: "Invalid URL",
    }[status] || "Failed to shorten URL"
  );
}
