// Современная функция копирования (Clipboard API + fallback)
async function copyToClipboard(text) {
  // 1. Современный Clipboard API (Chrome 66+, Firefox 63+, Safari 13.1+)
  if (navigator.clipboard && window.isSecureContext) {
    try {
      await navigator.clipboard.writeText(text);
      return true;
    } catch (err) {
      console.warn("Clipboard API failed:", err);
    }
  }

  // 2. Fallback execCommand (устаревший, но работает везде)
  return execCommandFallback(text);
}

// Вспомогательная функция для execCommand
function execCommandFallback(text) {
  const textArea = document.createElement("textarea");
  Object.assign(textArea.style, {
    position: "fixed",
    left: "-9999px",
    top: "-9999px",
    opacity: 0,
    pointerEvents: "none",
  });

  textArea.value = text;
  document.body.appendChild(textArea);
  textArea.focus();
  textArea.select();

  const success = document.execCommand("copy");
  document.body.removeChild(textArea);

  return success;
}
