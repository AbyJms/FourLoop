// Pull dashboard data from Flask backend and render into the page.
(function () {
  const messageBox = document.getElementById("dashboardMessage");
  const logoutBtn = document.querySelector(".logout");

  const API_BASE = ""; // same-origin; change to "http://127.0.0.1:5000" if serving from file://

  function setMessage(text, type = "info") {
    if (!messageBox) return;
    messageBox.textContent = text;
    messageBox.className = `dashboard-message ${type}`;
  }

  async function fetchDashboard() {
    setMessage("Loading dashboard...", "info");
    const res = await fetch(`${API_BASE}/dashboard`, {
      method: "GET",
      credentials: "include",
    });

    if (res.status === 401) {
      setMessage("Not logged in. Redirecting to login...", "error");
      setTimeout(() => (window.location.href = "auth.html"), 500);
      return null;
    }

    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      setMessage(data.error || "Failed to load dashboard", "error");
      return null;
    }

    setMessage("");
    return data;
  }

  function renderDashboard(data) {
    if (!data) return;
    // Zone name
    const zoneSpan = document.querySelector(".zone-name span");
    if (zoneSpan) zoneSpan.textContent = data.currentZone;

    // Boss info
    const bossName = document.querySelector(".boss-name");
    if (bossName && data.boss?.name) bossName.textContent = data.boss.name;
    const hpLabel = document.querySelector(".hp-bar-label span:last-child");
    const hpBar = document.querySelector(".hp-bar-inner");
    if (hpLabel && typeof data.boss?.hp === "number") {
      hpLabel.textContent = `${data.boss.hp}% remaining`;
    }
    if (hpBar && typeof data.boss?.hp === "number") {
      hpBar.style.width = `${data.boss.hp}%`;
    }

    // Quests (simple text join)
    const mainList = document.querySelector(".main-quests");
    const sideList = document.querySelector(".side-quests");
    if (mainList && Array.isArray(data.mainQuests)) {
      mainList.innerHTML = data.mainQuests.map((q) => `<li>${q}</li>`).join("");
    }
    if (sideList && Array.isArray(data.sideQuests)) {
      sideList.innerHTML = data.sideQuests.map((q) => `<li>${q}</li>`).join("");
    }

    // Party
    const partyList = document.querySelector(".party-list");
    if (partyList && Array.isArray(data.party)) {
      partyList.innerHTML = data.party
        .map(
          (p) => `
          <li>
            <span class="party-name">${p.name}</span>
            <span class="party-role">${p.role}</span>
            <span class="party-status ${p.status?.toLowerCase() || ""}">${p.status}</span>
          </li>`
        )
        .join("");
    }

    // Leaderboards (zonal/national)
    const zonal = document.querySelector(".leaderboard-list.zonal");
    const national = document.querySelector(".leaderboard-list.national");
    if (zonal && Array.isArray(data.leaderboard?.zonal)) {
      zonal.innerHTML = data.leaderboard.zonal
        .map((t) => `<li><span>${t.team}</span><span class="score">${t.score.toLocaleString()} pts</span></li>`)
        .join("");
    }
    if (national && Array.isArray(data.leaderboard?.national)) {
      national.innerHTML = data.leaderboard.national
        .map((t) => `<li><span>${t.team}</span><span class="score">${t.score.toLocaleString()} pts</span></li>`)
        .join("");
    }

    // Rewards
    const rewards = document.querySelector(".rewards");
    if (rewards && data.rewards) {
      rewards.innerHTML = `
        <p>Tier Progress: ${data.rewards.tierProgress}%</p>
        <p>Tokens: ${data.rewards.tokens}</p>
        <p>Redeemed: ${data.rewards.redeemed}</p>
        <p>Next Milestone: ${data.rewards.nextMilestone}</p>
      `;
    }
  }

  async function init() {
    const data = await fetchDashboard();
    renderDashboard(data);
  }

  // Logout button
  if (logoutBtn) {
    logoutBtn.addEventListener("click", async () => {
      try {
        await fetch(`${API_BASE}/logout`, {
          method: "POST",
          credentials: "include",
        });
      } catch (e) {
        /* swallow */
      } finally {
        window.location.href = "auth.html";
      }
    });
  }

  document.addEventListener("DOMContentLoaded", init);
})();
console.log("dashboard.js loaded");

if (!sessionStorage.getItem("authUser")) {
  console.warn("No auth user — redirecting");
  window.location.href = "auth.html";
}
