// ================= LOCATION UTILS =================
function updateLocationName(lat, lng) {
  fetch(
    `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}`
  )
    .then(res => res.json())
    .then(data => {
      const place =
        data.address.suburb ||
        data.address.neighbourhood ||
        data.address.city ||
        data.address.town ||
        "Your Area";

      const el = document.getElementById("currentLocation");
      if (el) el.textContent = place;
    })
    .catch(() => {
      const el = document.getElementById("currentLocation");
      if (el) el.textContent = "Location locked";
    });
}

// ================= GEOLOCATION (SAFE) =================
function getUserLocationOnce(callback) {
  const cached = sessionStorage.getItem("zoneMapUserLocation");
  if (cached) {
    try {
      const { lat, lng } = JSON.parse(cached);
      callback(lat, lng);
      return;
    } catch {}
  }

  if (!navigator.geolocation) {
    console.warn("Geolocation not supported");
    return;
  }

  navigator.geolocation.getCurrentPosition(
    pos => {
      const lat = pos.coords.latitude;
      const lng = pos.coords.longitude;

      sessionStorage.setItem(
        "zoneMapUserLocation",
        JSON.stringify({ lat, lng })
      );

      callback(lat, lng);
    },
    () => {
      console.warn("Location denied");
    },
    { enableHighAccuracy: true }
  );
}

// ================= ZONE MAP =================
document.addEventListener("DOMContentLoaded", () => {
  const mapEl = document.getElementById("zoneMap");
  if (!mapEl || typeof L === "undefined") return;

  // Create map
  window.zoneMap = L.map("zoneMap", {
    zoomControl: false,
    attributionControl: false
  });

  // Tiles
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19
  }).addTo(window.zoneMap);

  // Fallback view (before GPS)
  window.zoneMap.setView([10.5276, 76.2144], 14);

  // ================= FULLSCREEN =================
  const wrapper = mapEl.closest(".map-wrapper");
  const fsBtn = wrapper?.querySelector(".map-fullscreen-btn");

  fsBtn?.addEventListener("click", () => {
    wrapper.classList.toggle("is-fullscreen");
    fsBtn.textContent = wrapper.classList.contains("is-fullscreen")
      ? "Exit Fullscreen"
      : "Fullscreen";

    setTimeout(() => window.zoneMap.invalidateSize(), 200);
  });

  // ================= USER LOCATION =================
  getUserLocationOnce((lat, lng) => {
    window.zoneMap.setView([lat, lng], 15);

    const userIcon = L.icon({
      iconUrl: "/static/you.jpg",
      iconSize: [38, 38],
      iconAnchor: [19, 19],
      className: "user-map-icon"
    });

    L.marker([lat, lng], { icon: userIcon })
      .addTo(window.zoneMap)
      .bindPopup("You are here");

    updateLocationName(lat, lng);
  });

  // ================= DEMO GARBAGE =================
  const garbageIcon = L.icon({
    iconUrl: "/static/demogarbage.jpeg",
    iconSize: [72, 72],
    iconAnchor: [36, 36],
    className: "demogarbage-icon"
  });

  const bosses = [
    { name: "Demo-garbage", coords: [10.350078, 76.248586] },
    { name: "Demo-garbage (East)", coords: [10.350078, 76.278586] }
  ];

  bosses.forEach(boss => {
    // Danger pulse
    L.circle(boss.coords, {
      radius: 420,
      color: "rgba(255,80,80,0.6)",
      fillColor: "rgba(255,80,80,0.25)",
      weight: 2,
      className: "danger-pulse",
      interactive: false
    }).addTo(window.zoneMap);

    // Marker
    L.marker(boss.coords, { icon: garbageIcon })
      .addTo(window.zoneMap)
      .bindPopup(boss.name);
  });
});