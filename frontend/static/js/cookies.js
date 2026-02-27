// cookies.js - версия для Edge/Chrome + localhost!
(function () {
  "use strict";

  // Функции
  function getCookie(name) {
    const value = "; " + document.cookie;
    const parts = value.split("; " + name + "=");
    return parts.length === 2 ? parts.pop().split(";").shift() : null;
  }

  function generateId(length) {
    const chars =
      "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    let result = "";
    for (let i = 0; i < length; i++) {
      result += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return result;
  }

  // 1. ✅ session_id - создаём ПРИНУДИТЕЛЬНО при каждой загрузке!
  // Убираем Secure для localhost:80 (работает везде!)
  if (!getCookie("session_id")) {
    const newSessionId = generateId(16);
    document.cookie = `session_id=${newSessionId}; path=/; max-age=${24 * 60 * 60}; SameSite=Lax`;
  }

  // 2. Cookie banner - только после DOM
  function initCookieBanner() {
    const cookieBanner = document.getElementById("cookieConsent");
    if (!cookieBanner) return;

    const acceptBtn = document.getElementById("acceptCookies");
    const declineBtn = document.getElementById("declineCookies");

    // Показ баннера только без согласия
    if (!getCookie("cookies_accepted")) {
      setTimeout(() => cookieBanner.classList.add("show"), 1000);
    }

    // Accept - добавляем referrer
    if (acceptBtn) {
      acceptBtn.addEventListener("click", () => {
        document.cookie = `cookies_accepted=true; path=/; max-age=${365 * 24 * 60 * 60}; SameSite=Lax`;
        document.cookie = `user_type=shortener_user; path=/; max-age=${365 * 24 * 60 * 60}; SameSite=Lax`;
        document.cookie = `referrer=${encodeURIComponent(document.referrer || "")}; path=/; max-age=${24 * 60 * 60}; SameSite=Lax`;
        cookieBanner.classList.remove("show");
      });
    }

    // Decline
    if (declineBtn) {
      declineBtn.addEventListener("click", () => {
        document.cookie = `cookies_accepted=false; path=/; max-age=${30 * 24 * 60 * 60}; SameSite=Lax`;
        cookieBanner.classList.remove("show");
      });
    }
  }

  // 3. Запуск banner после DOM (безопасно)
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initCookieBanner);
  } else {
    initCookieBanner(); // DOM уже готов
  }
})();
