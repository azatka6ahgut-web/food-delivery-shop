function showTab(tab) {
  document.getElementById("login-form").style.display = tab === "login" ? "flex" : "none";
  document.getElementById("register-form").style.display = tab === "register" ? "flex" : "none";
  document.getElementById("tab-login").classList.toggle("active", tab === "login");
  document.getElementById("tab-register").classList.toggle("active", tab === "register");
}

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("tab-login").addEventListener("click", () => showTab("login"));
  document.getElementById("tab-register").addEventListener("click", () => showTab("register"));

  document.getElementById("login-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const errorEl = document.getElementById("login-error");
    errorEl.textContent = "";
    const email = document.getElementById("login-email").value.trim();
    const password = document.getElementById("login-password").value;

    try {
      const formBody = new URLSearchParams();
      formBody.append("username", email);
      formBody.append("password", password);
      const data = await apiRequest("/auth/login", {
        method: "POST",
        form: true,
        body: formBody,
      });
      setToken(data.access_token);
      window.location.href = "/";
    } catch (err) {
      errorEl.textContent = "Неверный email или пароль";
    }
  });

  document.getElementById("register-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const errorEl = document.getElementById("register-error");
    errorEl.textContent = "";
    const email = document.getElementById("register-email").value.trim();
    const password = document.getElementById("register-password").value;

    try {
      await apiRequest("/auth/register", {
        method: "POST",
        body: { email, password },
      });
      // Auto-login after successful registration
      const formBody = new URLSearchParams();
      formBody.append("username", email);
      formBody.append("password", password);
      const data = await apiRequest("/auth/login", {
        method: "POST",
        form: true,
        body: formBody,
      });
      setToken(data.access_token);
      window.location.href = "/";
    } catch (err) {
      errorEl.textContent = err.message || "Не удалось зарегистрироваться";
    }
  });
});
