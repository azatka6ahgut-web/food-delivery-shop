const STATUS_LABELS = {
  pending: "Ожидает оплаты",
  paid: "Оплачен",
  payment_failed: "Оплата не прошла",
  cancelled: "Отменён",
  delivered: "Доставлен",
};

async function loadOrders() {
  const container = document.getElementById("orders-container");
  if (!isLoggedIn()) {
    container.innerHTML = '<p class="empty-state">Войдите, чтобы увидеть заказы</p>';
    return;
  }
  try {
    const orders = await apiRequest("/orders", { auth: true });
    if (orders.length === 0) {
      container.innerHTML = '<p class="empty-state">У вас пока нет заказов</p>';
      return;
    }
    const table = document.createElement("table");
    table.className = "orders-table";
    table.innerHTML = `
      <thead>
        <tr>
          <th>№</th>
          <th>Статус</th>
          <th>Сумма</th>
          <th>Адрес доставки</th>
        </tr>
      </thead>
      <tbody></tbody>
    `;
    const tbody = table.querySelector("tbody");
    orders.forEach((order) => {
      const tr = document.createElement("tr");
      tr.dataset.testid = "order-row";
      tr.dataset.orderId = order.id;
      tr.innerHTML = `
        <td>${order.id}</td>
        <td><span class="status-badge status-${order.status}">${STATUS_LABELS[order.status] || order.status}</span></td>
        <td>${order.total.toFixed(2)} \u20bd</td>
        <td>${order.delivery_address}</td>
      `;
      tbody.appendChild(tr);
    });
    container.innerHTML = "";
    container.appendChild(table);
  } catch (e) {
    container.innerHTML = `<p class="error-message">${e.message}</p>`;
  }
}

document.addEventListener("DOMContentLoaded", loadOrders);
