console.log("dashboard.js loaded");

if (!sessionStorage.getItem("authUser")) {
  console.warn("No auth user — redirecting");
  window.location.href = "auth.html";
}
