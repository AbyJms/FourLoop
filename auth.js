document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("authForm");
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = document.getElementById("loginEmail").value;
    const password = document.getElementById("loginPassword").value;

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
});
