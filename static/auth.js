// Frontend auth wiring: handles login/register form submissions to Flask backend.
(function () {
  const loginForm = document.getElementById("authForm");
  const registerForm = document.getElementById("registerForm");
  const messageBox = document.getElementById("authMessage");
  const tabs = document.querySelectorAll(".auth-tab");
  const loginPanel = document.getElementById("loginPanel");
  const registerPanel = document.getElementById("registerPanel");

  const API_BASE = ""; // same-origin; change to "http://127.0.0.1:5000" if serving HTML from file://

  function setMessage(text, type = "info") {
    if (!messageBox) return;
    messageBox.textContent = text;
    messageBox.className = `auth-message ${type}`;
  }

  async function postJSON(path, body) {
    const res = await fetch(`${API_BASE}${path}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include", // keep session cookie
      body: JSON.stringify(body),
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      throw new Error(data.error || "Request failed");
    }
    return data;
  }

  // Login submit
  if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const email = document.getElementById("loginEmail")?.value.trim();
      const password = document.getElementById("loginPassword")?.value;
      if (!email || !password) {
        setMessage("Email and password are required", "error");
        return;
      }
      setMessage("Logging in...", "info");
      try {
        await postJSON("/login", { email, password });
        setMessage("Login successful. Redirecting to dashboard...", "success");
        setTimeout(() => (window.location.href = "dashboard.html"), 500);
      } catch (err) {
        setMessage(err.message, "error");
      }
    });
  }

  // Register submit
  <!-- HTML -->
<div class="auth-tabs">
  <button class="auth-tab active" data-view="login">Login</button>
  <button class="auth-tab" data-view="register">Register</button>
</div>

<div id="loginPanel" class="auth-panel active">
  <form id="loginForm">
    <input type="email" id="loginEmail" placeholder="Email" required>
    <input type="password" id="loginPassword" placeholder="Password" required>
    <button type="submit">Login</button>
  </form>
</div>

<div id="registerPanel" class="auth-panel">
  <form id="registerForm">
    <input type="email" name="registerEmail" placeholder="Email" required>
    <input type="password" name="registerPassword" placeholder="Password" required>
    <button type="submit">Register</button>
  </form>
</div>
