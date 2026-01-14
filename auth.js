console.log("auth.js loaded");

const API_BASE = "http://127.0.0.1:5000/api";

// ---------------- LOGIN ----------------
document.getElementById("loginBtn").addEventListener("click", async (e) => {
  e.preventDefault();

  const username = document.getElementById("login-username").value.trim();
  const password = document.getElementById("login-password").value.trim();

  if (!username || !password) {
    alert("Enter username and password");
    return;
  }

  const res = await fetch(`${API_BASE}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password })
  });

  const data = await res.json();

  if (!res.ok) {
    alert(data.error || "Login failed");
    return;
  }

  // STORE AUTH
  localStorage.setItem("access_token", data.access_token);
  localStorage.setItem("user", JSON.stringify(data.user));

  // 🔥 ROLE BASED ROUTING
  if (data.user.user_type === "seeker") {
    window.location.replace("seeker-dashboard.html");
  } else {
    window.location.replace("dashboard.html");
  }
});

// ---------------- REGISTER ----------------
document.getElementById("registerBtn").addEventListener("click", async (e) => {
  e.preventDefault();

  const first = document.getElementById("first-name").value.trim();
  const last = document.getElementById("last-name").value.trim();
  const username = document.getElementById("username").value.trim();
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();

  if (!first || !last || !username || !email || !password) {
    alert("Fill all fields");
    return;
  }

  const res = await fetch(`${API_BASE}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      full_name: `${first} ${last}`,
      username,
      email,
      password,
      user_type: "collector" // change to seeker if needed
    })
  });

  const data = await res.json();

  if (!res.ok) {
    alert(data.error || "Registration failed");
    return;
  }

  alert("Registered successfully. Now login.");
});
