// api.js — central backend connector

const API_BASE = "http://localhost:5000/api";

// --------------------
// TOKEN HELPERS
// --------------------
function getToken() {
  return localStorage.getItem("access_token");
}

function setToken(token) {
  localStorage.setItem("access_token", token);
}

function logout() {
  localStorage.removeItem("access_token");
  window.location.href = "login.html";
}

// --------------------
// AUTH
// --------------------
async function login(email, password) {
  const res = await fetch(`${API_BASE}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  });

  const data = await res.json();

  if (!res.ok) {
    throw new Error(data.error || "Login failed");
  }

  setToken(data.access_token);
  return data;
}

// --------------------
// USER
// --------------------
async function getUserStats() {
  const res = await fetch(`${API_BASE}/users/stats`, {
    headers: {
      "Authorization": `Bearer ${getToken()}`
    }
  });

  if (res.status === 401) logout();
  return res.json();
}

// --------------------
// REPORTS / QUESTS
// --------------------
async function getReports() {
  const res = await fetch(`${API_BASE}/reports?status=pending`, {
    headers: {
      "Authorization": `Bearer ${getToken()}`
    }
  });

  if (res.status === 401) logout();
  return res.json();
}

async function createReport(payload) {
  const res = await fetch(`${API_BASE}/reports`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${getToken()}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  });

  if (res.status === 401) logout();
  return res.json();
}

async function assignReport(id) {
  return fetch(`${API_BASE}/reports/${id}/assign`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${getToken()}`
    }
  });
}

async function completeReport(id) {
  return fetch(`${API_BASE}/reports/${id}/complete`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${getToken()}`
    }
  });
}
