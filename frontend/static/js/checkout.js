document.addEventListener("DOMContentLoaded", () => {
  if (!isLoggedIn()) {
    window.location.href = "/login.html";
    return;
  }

  const form = document.getElementById("checkout-form");
  const errorEl = document.getElementById("error-message");
  const successEl = document.getElementById("success-message");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    errorEl.textContent = "";
    successEl.textContent = "";

    const address = document.getElementById("address").value.trim();
    const cardNumber = document.getElementById("card-number").value.trim();
    const cardExpiry = document.getElementById("card-expiry").value.trim();
    const cardCvv = document.getElementById("card-cvv").value.trim();

    try {
      const order = await apiRequest("/orders", {
        method: "POST",
        auth: true,
        body: { delivery_address: address },
      });

      try {
        await apiRequest(`/payment/${order.id}`, {
          method: "POST",
          auth: true,
          body: {
            card_number: cardNumber,
            card_expiry: cardExpiry,
            card_cvv: cardCvv,
          },
        });
        successEl.textContent = `Заказ #${order.id} оплачен! Спасибо за покупку.`;
        await updateCartBadge();
        setTimeout(() => (window.location.href = "/orders.html"), 1500);
      } catch (payErr) {
        errorEl.textContent = `Заказ #${order.id} создан, но оплата отклонена: ${payErr.message}`;
      }
    } catch (err) {
      errorEl.textContent = err.message;
    }
  });
});
