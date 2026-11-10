// 1. Arrays and Objects (For Technical Design)
let orderItems = []; 
let customerInfo = { name: "", email: "" };

// 2. Function to handle adding items
function addToOrder(itemName, price) {
    // Add to array
    orderItems.push({ name: itemName, price: price });
    
    // Update the page dynamically (Feature Purpose)
    let orderList = document.getElementById("order-list");
    let orderTotal = document.getElementById("order-total");
    
    if (orderList && orderTotal) {
        orderList.innerHTML = ""; // Clear current list
        let total = 0;
        
        for (let i = 0; i < orderItems.length; i++) {
            let li = document.createElement("li");
            li.innerText = orderItems[i].name + " - $" + orderItems[i].price;
            orderList.appendChild(li);
            total = total + orderItems[i].price;
        }
        orderTotal.innerText = "Total: $" + total;
    }
    
    // Save to localStorage
    localStorage.setItem("myBakeryOrder", JSON.stringify(orderItems));
}

// 3. Function to load saved data when page opens
function loadOrder() {
    let savedOrder = localStorage.getItem("myBakeryOrder");
    if (savedOrder) {
        orderItems = JSON.parse(savedOrder);
        
        let orderList = document.getElementById("order-list");
        let orderTotal = document.getElementById("order-total");
        
        if (orderList && orderTotal) {
            let total = 0;
            for (let i = 0; i < orderItems.length; i++) {
                let li = document.createElement("li");
                li.innerText = orderItems[i].name + " - $" + orderItems[i].price;
                orderList.appendChild(li);
                total = total + orderItems[i].price;
            }
            orderTotal.innerText = "Total: $" + total;
        }
    }
}

// 4. Form Validation Function (For contact.html)
function validateForm(event) {
    event.preventDefault(); // Stop page from refreshing
    
    let nameInput = document.getElementById("name").value;
    let emailInput = document.getElementById("email").value;
    let errorMsg = document.getElementById("error-message");
    
    errorMsg.innerHTML = ""; // Clear previous errors
    
    // Check 1: Name cannot be empty
    if (nameInput.trim() === "") {
        errorMsg.innerHTML = "Error: Name cannot be empty.";
        return false;
    }
    
    // Check 2: Email must contain @
    if (!emailInput.includes("@")) {
        errorMsg.innerHTML = "Error: Please enter a valid email address (must include @).";
        return false;
    }
    
    errorMsg.style.color = "green";
    errorMsg.innerHTML = "Success! Form submitted.";
    return true;
}

// Run loadOrder when page loads
window.onload = loadOrder;