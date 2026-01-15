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
