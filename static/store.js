let credits = 0;

async function loadCredits() {
  const res = await fetch("/api/store", { credentials: "include" });
  if (!res.ok) return;

  const data = await res.json();
  credits = data.credits;
  document.getElementById("storePoints").textContent = credits;
}

async function redeem(cost) {
  const res = await fetch("/api/redeem", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify({ cost })
  });

  const data = await res.json();

  if (!res.ok) {
    alert(data.error);
    return;
  }

  credits = data.credits;
  document.getElementById("storePoints").textContent = credits;
}

document.querySelectorAll(".redeem-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    const card = btn.closest(".store-card");
    const cost = Number(card.dataset.cost);
    redeem(cost);
  });
});

loadCredits();
