let points = 8000;
const owned = {
  "free-bus": 0,
  "bus-discount": 0,
  "train-discount": 0,
  "electricity": 0,
  "ration": 0
};

document.querySelectorAll(".redeem-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    const card = btn.closest(".store-card");
    const id = card.dataset.id;
    const cost = Number(card.dataset.cost);

    if (points < cost) return;
    if (owned[id] >= 2) return;

    points -= cost;
    owned[id]++;

    document.getElementById("storePoints").textContent = points;
    document.getElementById(`${id}-owned`).textContent = owned[id];
  });
});
