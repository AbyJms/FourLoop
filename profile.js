const API_BASE = "http://127.0.0.1:5000/api";
const token = localStorage.getItem("access_token");

if (!token) {
  window.location.replace("auth.html");
}

fetch(`${API_BASE}/auth/me`, {
  headers: {
    Authorization: `Bearer ${token}`
  }
})
.then(res => {
  if (!res.ok) {
    localStorage.clear();
    window.location.replace("auth.html");
  }
  return res.json();
})
.then(user => {
  document.getElementById("profile-username").textContent = user.username;
  document.getElementById("profile-email").textContent = user.email || "—";
  document.getElementById("profile-type").textContent = user.user_type;
  document.getElementById("profile-points").textContent = user.points;
});
