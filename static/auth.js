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
  if (registerForm) {
    registerForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const email = registerForm.querySelector('input[name="registerEmail"]')?.value.trim();
      const password = registerForm.querySelector('input[name="registerPassword"]')?.value;
      if (!email || !password) {
        setMessage("Email and password are required", "error");
        return;
      }
      setMessage("Creating account...", "info");
      try {
        await postJSON("/register", { email, password });
        setMessage("Account created. You can log in now.", "success");
        // switch back to login tab
        tabs.forEach((t) => t.classList.remove("active"));
        loginPanel?.classList.add("active");
        registerPanel?.classList.remove("active");
        const loginTab = document.querySelector('.auth-tab[data-view="login"]');
        loginTab?.classList.add("active");
      } catch (err) {
        setMessage(err.message, "error");
      }
    });
  }
})();
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("authForm");
  if (!form) {
    console.error("authForm not found");
    return;
  }

  form.addEventListener("submit", (e) => {
    e.preventDefault(); // 🔥 critical

    const email = document.getElementById("loginEmail").value;
    const password = document.getElementById("loginPassword").value;

    if (!email || !password) {
      alert("Fill all fields");
      return;
    }

    const user = {
      email,
      username: "NeonVanguard"
    };

    sessionStorage.setItem("authUser", JSON.stringify(user));

    window.location.href = "dashboard.html";
  });
});
