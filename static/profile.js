(async function () {
  const res = await fetch("/api/profile", { credentials: "include" });
  if (!res.ok) {
    window.location.href = "/";
    return;
  }

  const u = await res.json();

  document.querySelector(".profile-username").textContent = u.username;
  document.querySelector(".current-title span").textContent = u.title || "—";

  document.querySelector(".title-badge").innerHTML =
    `Credits: ${u.credits}<br>` +
    `Points: ${u.points}<br>` +
    `Lifetime Points: ${u.total_points}<br>` +
    `Rank: ${u.rank}<br>` +
    `Best Rank: ${u.best_rank}`;
})();
