const API_BASE = "";

function getToken() {
  return localStorage.getItem("access_token");
}

function setToken(token) {
  localStorage.setItem("access_token", token);
}

function clearToken() {
  localStorage.removeItem("access_token");
}

function isLoggedIn() {
  return !!getToken();
}

async function apiRequest(path, { method = "GET", body = null, auth = false, form = false } = {}) {
  const headers = {};
  if (!form) headers["Content-Type"] = "application/json";
  if (auth) {
    const token = getToken();
    if (token) headers["Authorization"] = `Bearer ${token}`;
  }

  const response = await fetch(API_BASE + path, {
    method,
    headers,
    body: body ? (form ? body : JSON.stringify(body)) : undefined,
  });

  let data = null;
  try {
    data = await response.json();
  } catch (e) {
    data = null;
  }

  if (!response.ok) {
    const detail = data && data.detail ? data.detail : `HTTP ${response.status}`;
    const err = new Error(typeof detail === "string" ? detail : JSON.stringify(detail));
    err.status = response.status;
    err.data = data;
    throw err;
  }
  return data;
}

async function updateCartBadge() {
  const badge = document.getElementById("cart-count");
  if (!badge) return;
  if (!isLoggedIn()) {
    badge.textContent = "0";
    return;
  }
  try {
    const cart = await apiRequest("/cart", { auth: true });
    const totalQty = cart.items.reduce((sum, item) => sum + item.quantity, 0);
    badge.textContent = totalQty;
  } catch (e) {
    badge.textContent = "0";
  }
}

function renderAuthNav() {
  const authLink = document.getElementById("auth-link");
  if (!authLink) return;
  if (isLoggedIn()) {
    authLink.textContent = "Выйти";
    authLink.onclick = (e) => {
      e.preventDefault();
      clearToken();
      window.location.href = "/";
    };
  } else {
    authLink.textContent = "Войти";
    authLink.href = "/login.html";
  }
}

document.addEventListener("DOMContentLoaded", () => {
  renderAuthNav();
  updateCartBadge();
});
