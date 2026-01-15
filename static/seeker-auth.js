const API_BASE = "http://127.0.0.1:5000/api";
const token = localStorage.getItem("access_token");

if (!token) {
  window.location.href = "auth.html";
}

fetch(`${API_BASE}/auth/me`, {
  headers: {
    "Authorization": `Bearer ${token}`
  }
})
.then(res => res.json())
.then(user => {
  if (user.user_type !== "seeker") {
    window.location.href = "dashboard.html";
  }
})
.catch(() => {
  localStorage.clear();
  window.location.href = "auth.html";
});
