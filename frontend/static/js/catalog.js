let currentCategory = "";

async function loadProducts() {
  const grid = document.getElementById("product-grid");
  grid.innerHTML = "<p>Загрузка...</p>";
  try {
    const path = currentCategory ? `/products?category=${encodeURIComponent(currentCategory)}` : "/products";
    const products = await apiRequest(path);
    if (products.length === 0) {
      grid.innerHTML = '<p class="empty-state">Товары не найдены</p>';
      return;
    }
    grid.innerHTML = "";
    products.forEach((product) => {
      const card = document.createElement("div");
      card.className = "product-card";
      card.dataset.testid = "product-card";
      card.dataset.productId = product.id;
      card.innerHTML = `
        <div class="category">${product.category}</div>
        <div class="name">${product.name}</div>
        <div class="price">${product.price.toFixed(2)} \u20bd</div>
        <button class="primary" data-testid="add-to-cart-btn">В корзину</button>
      `;
      card.querySelector("button").addEventListener("click", () => addToCart(product.id));
      grid.appendChild(card);
    });
  } catch (e) {
    grid.innerHTML = `<p class="error-message">Ошибка загрузки: ${e.message}</p>`;
  }
}

async function addToCart(productId) {
  if (!isLoggedIn()) {
    window.location.href = "/login.html";
    return;
  }
  try {
    await apiRequest("/cart/items", {
      method: "POST",
      auth: true,
      body: { product_id: productId, quantity: 1 },
    });
    await updateCartBadge();
  } catch (e) {
    alert("Не удалось добавить товар: " + e.message);
  }
}

function setupFilters() {
  document.querySelectorAll(".filters button").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".filters button").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      currentCategory = btn.dataset.category || "";
      loadProducts();
    });
  });
}

document.addEventListener("DOMContentLoaded", () => {
  setupFilters();
  loadProducts();
});
