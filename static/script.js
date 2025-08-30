// script.js

// Run after DOM loads
document.addEventListener("DOMContentLoaded", function () {
    // Elements
    const orderForm = document.getElementById("orderForm");
    const vendorOrdersList = document.getElementById("vendorOrdersList");
    const adminOrdersList = document.getElementById("adminOrdersList");

    // Initialize orders in localStorage
    if (!localStorage.getItem("orders")) {
        localStorage.setItem("orders", JSON.stringify([]));
    }

    // Handle user placing an order
    if (orderForm) {
        orderForm.addEventListener("submit", function (e) {
            e.preventDefault();

            const food = document.getElementById("food").value;
            const block = document.getElementById("block").value;

            if (food && block) {
                let orders = JSON.parse(localStorage.getItem("orders"));
                let newOrder = {
                    food: food,
                    block: block,
                    time: new Date().toLocaleTimeString()
                };

                orders.push(newOrder);
                localStorage.setItem("orders", JSON.stringify(orders));

                alert("✅ Order placed successfully!");
                orderForm.reset();
            }
        });
    }

    // Display orders in Vendor/Admin panels
    function displayOrders(listElement) {
        if (!listElement) return;

        listElement.innerHTML = ""; // clear old

        let orders = JSON.parse(localStorage.getItem("orders"));
        orders.forEach((order, index) => {
            let li = document.createElement("li");
            li.textContent = `${index + 1}. ${order.food} → ${order.block} [${order.time}]`;
            listElement.appendChild(li);
        });
    }

    // Update vendor page
    if (vendorOrdersList) {
        setInterval(() => displayOrders(vendorOrdersList), 1000);
    }

    // Update admin page
    if (adminOrdersList) {
        setInterval(() => displayOrders(adminOrdersList), 1000);
    }
});
