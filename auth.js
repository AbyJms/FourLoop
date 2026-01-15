document.addEventListener("DOMContentLoaded", () => {
<<<<<<< HEAD
  const form = document.getElementById("authForm");
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
=======
  const API_BASE = "http://localhost:5000/api";

  const authForm = document.getElementById("authForm");
  const registerForm = document.getElementById("registerForm");

  /* -------------------------
     LOGIN
  ------------------------- */
  if (authForm) {
    authForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      const email = document.getElementById("loginEmail").value.trim();
      const password = document.getElementById("loginPassword").value.trim();

      if (!email || !password) {
        alert("Fill all fields");
        return;
      }

      try {
        const res = await fetch(`${API_BASE}/auth/login`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, password })
        });

        const data = await res.json();

        if (!res.ok) {
          alert(data.error || "Login failed");
          return;
        }

        // SAVE JWT
        localStorage.setItem("access_token", data.access_token);

        // redirect
        window.location.href = "dashboard.html";
      } catch (err) {
        alert("Backend not reachable. Is Flask running?");
      }
    });
  }

  /* -------------------------
     REGISTER
  ------------------------- */
  if (registerForm) {
    registerForm.addEventListener("submit", async (e) => {
      e.preventDefault();
>>>>>>> 04da2d01ffe9acadffbb6189fda4a30b9b647ac9

      const email = registerForm.registerEmail.value.trim();
      const username = registerForm.username.value.trim();
      const password = registerForm.registerPassword.value.trim();

<<<<<<< HEAD
    try {
      const res = await fetch("http://127.0.0.1:5000/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
      });

      const data = await res.json();

      if (!res.ok) {
        alert(data.error || "Login failed");
        return;
      }

      // save auth
      sessionStorage.setItem("authUser", JSON.stringify(data.user));
      sessionStorage.setItem("token", data.access_token);

      window.location.href = "dashboard.html";

    } catch (err) {
      console.error(err);
      alert("Server error");
    }
  });
=======
      if (!email || !username || !password) {
        alert("Fill all fields");
        return;
      }

      const payload = {
        email,
        username,
        password,
        user_type: "collector" // can change later
      };

      try {
        const res = await fetch(`${API_BASE}/auth/register`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });

        const data = await res.json();

        if (!res.ok) {
          alert(data.error || "Registration failed");
          return;
        }

        alert("Registration successful. Please log in.");

        // switch to login view
        document.querySelector('[data-view="login"]').click();
      } catch (err) {
        alert("Backend not reachable. Is Flask running?");
      }
    });
  }
>>>>>>> 04da2d01ffe9acadffbb6189fda4a30b9b647ac9
});
