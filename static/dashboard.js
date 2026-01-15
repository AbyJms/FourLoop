(async function () {
  const res = await fetch("/api/dashboard", { credentials: "include" });
  if (!res.ok) {
    window.location.href = "/";
    return;
  }

  const data = await res.json();

  // Boss / zone
  document.querySelector(".zone-name span").textContent = data.currentZone;
  document.querySelector(".boss-name").textContent = data.boss.name;

  const hpBar = document.querySelector(".hp-bar-inner");
  const hpLabel = document.querySelector(".hp-bar-label span:last-child");

  hpBar.style.width = `${data.boss.hp}%`;
  hpLabel.textContent = `${data.boss.hp}% remaining`;

  // NATIONAL LEADERBOARD (single list)
  const list = document.querySelector(".leaderboard-list");
  list.innerHTML = "";

  data.leaderboard.forEach((u, i) => {
    const li = document.createElement("li");
    li.innerHTML = `
      <span>${i + 1}. ${u.username}</span>
      <span class="score">${u.points} pts</span>
    `;
    list.appendChild(li);
  });

  // Logout
  document.querySelector(".logout").onclick = async () => {
    await fetch("/logout", { method: "POST", credentials: "include" });
    window.location.href = "/";
  };
})();
