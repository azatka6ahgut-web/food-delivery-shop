async function loadCart() {
  const container = document.getElementById("cart-items");
  const totalEl = document.getElementById("cart-total");
  const checkoutBtn = document.getElementById("checkout-btn");

  if (!isLoggedIn()) {
    container.innerHTML = '<p class="empty-state">Войдите, чтобы увидеть корзину</p>';
    checkoutBtn.disabled = true;
    return;
  }

  try {
    const cart = await apiRequest("/cart", { auth: true });
    if (cart.items.length === 0) {
      container.innerHTML = '<p class="empty-state">Корзина пуста</p>';
      totalEl.textContent = "";
      checkoutBtn.disabled = true;
      return;
    }
    container.innerHTML = "";
    cart.items.forEach((item) => {
      const row = document.createElement("div");
      row.className = "cart-item";
      row.dataset.testid = "cart-item";
      row.dataset.itemId = item.id;
      row.innerHTML = `
        <div>
          <div class="name">${item.product.name}</div>
          <div class="category">${item.product.price.toFixed(2)} \u20bd за шт.</div>
        </div>
        <div class="qty-controls">
          <button data-action="dec" data-testid="qty-dec">-</button>
          <span data-testid="qty-value">${item.quantity}</span>
          <button data-action="inc" data-testid="qty-inc">+</button>
          <button data-action="remove" data-testid="remove-item">Удалить</button>
        </div>
        <div class="price">${item.line_total.toFixed(2)} \u20bd</div>
      `;
      row.querySelector('[data-action="dec"]').addEventListener("click", () =>
        changeQuantity(item.id, item.quantity - 1)
      );
      row.querySelector('[data-action="inc"]').addEventListener("click", () =>
        changeQuantity(item.id, item.quantity + 1)
      );
      row.querySelector('[data-action="remove"]').addEventListener("click", () =>
        removeItem(item.id)
      );
      container.appendChild(row);
    });
    totalEl.textContent = `Итого: ${cart.total.toFixed(2)} \u20bd`;
    checkoutBtn.disabled = false;
  } catch (e) {
    container.innerHTML = `<p class="error-message">${e.message}</p>`;
  }
}

async function changeQuantity(itemId, newQuantity) {
  if (newQuantity < 1) {
    await removeItem(itemId);
    return;
  }
  try {
    await apiRequest(`/cart/items/${itemId}`, {
      method: "PUT",
      auth: true,
      body: { quantity: newQuantity },
    });
    await loadCart();
    await updateCartBadge();
  } catch (e) {
    alert(e.message);
  }
}

async function removeItem(itemId) {
  try {
    await apiRequest(`/cart/items/${itemId}`, { method: "DELETE", auth: true });
    await loadCart();
    await updateCartBadge();
  } catch (e) {
    alert(e.message);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  loadCart();
  document.getElementById("checkout-btn").addEventListener("click", () => {
    window.location.href = "/checkout.html";
  });
});
