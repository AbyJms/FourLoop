(async function () {
  const res = await fetch("/api/profile", { credentials: "include" });
  if (!res.ok) {
    window.location.href = "/";
    return;
  }

  const u = await res.json();

  document.querySelector(".profile-username").textContent = u.username;
  document.querySelector(".current-title span").textContent = u.title || "—";

  document.getElementById("stat-username").textContent = u.username;
  document.getElementById("stat-credits").textContent = u.credits;
  document.getElementById("stat-points").textContent = u.points;
  document.getElementById("stat-total-points").textContent = u.total_points;
  document.getElementById("stat-rank").textContent = u.rank;
  document.getElementById("stat-best-rank").textContent = u.best_rank;
})();
