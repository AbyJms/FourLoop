(function () {
  const loginBtn = document.getElementById("loginBtn");
  const registerBtn = document.getElementById("registerBtn");
  const messageBox = document.getElementById("authMessage");

  function setMessage(text, type = "info") {
    if (!messageBox) return;
    messageBox.textContent = text;
    messageBox.className = `auth-message ${type}`;
  }

  async function postJSON(path, body) {
    const res = await fetch(path, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify(body),
    });

    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(data.error || "Request failed");
    return data;
  }

  // LOGIN
  if (loginBtn) {
    loginBtn.addEventListener("click", async (e) => {
      e.preventDefault();

      const username = document.getElementById("login-username")?.value.trim();
      const password = document.getElementById("login-password")?.value;

      if (!username || !password) {
        setMessage("Username and password required", "error");
        return;
      }

      setMessage("Logging in...");

      try {
        await postJSON("/login", { username, password });
        window.location.href = "/dashboard";
      } catch (err) {
        setMessage(err.message, "error");
      }
    });
  }

  // REGISTER
  if (registerBtn) {
    registerBtn.addEventListener("click", async (e) => {
      e.preventDefault();

      const username = document.getElementById("username")?.value.trim();
      const email = document.getElementById("email")?.value.trim();
      const password = document.getElementById("password")?.value;

      if (!username || !email || !password) {
        setMessage("All fields are required", "error");
        return;
      }

      setMessage("Registering...");

      try {
        await postJSON("/register", { username, email, password });
        setMessage("Registered successfully. You can now log in.", "success");
        document.querySelector('[data-view="login"]')?.click();
      } catch (err) {
        setMessage(err.message, "error");
      }
    });
  }
})();
