// Функция копирования в буфер обмена
async function copyToClipboard(text) {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch (err) {
    // fallback для старых браузеров
    const textArea = document.createElement("textarea");
    textArea.value = text;
    textArea.style.position = "fixed"; // невидимый
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    try {
      const success = document.execCommand("copy");
      document.body.removeChild(textArea);
      return success;
    } catch (fallbackErr) {
      document.body.removeChild(textArea);
      return false;
    }
  }
}
