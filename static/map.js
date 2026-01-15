<<<<<<< HEAD
=======
// ================= LOCATION UTILS =================
>>>>>>> 31502171d08cdc8b8e6e36c7f25152061fa8cd4e
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
<<<<<<< HEAD

      document.getElementById("currentLocation").textContent = place;
    })
    .catch(() => {
      document.getElementById("currentLocation").textContent = "Your Area";
    });
}

=======
>>>>>>> 31502171d08cdc8b8e6e36c7f25152061fa8cd4e

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

<<<<<<< HEAD
  const locationEl = document.getElementById("currentLocation");

  getUserLocationOnce((lat, lng) => {
    // Center map
    window.zoneMapInstance.setView([lat, lng], 15);
=======
  // ================= USER LOCATION =================
  getUserLocationOnce((lat, lng) => {
    window.zoneMap.setView([lat, lng], 15);
>>>>>>> 31502171d08cdc8b8e6e36c7f25152061fa8cd4e

    // User marker
    const userIcon = L.icon({
<<<<<<< HEAD
      iconUrl: "you.jpg",
      iconSize: [36, 36],
      iconAnchor: [18, 18],
      popupAnchor: [0, -18],
=======
      iconUrl: "/static/you.jpg",
      iconSize: [38, 38],
      iconAnchor: [19, 19],
>>>>>>> 31502171d08cdc8b8e6e36c7f25152061fa8cd4e
      className: "user-map-icon"
    });

    L.marker([lat, lng], { icon: userIcon })
<<<<<<< HEAD
      .addTo(window.zoneMapInstance)
      .bindPopup("You are here");

    // 🔥 UPDATE UI TEXT (THIS WAS NEVER RUNNING BEFORE)
    if (locationEl) {
      locationEl.textContent = "Location locked";
    }
  });
=======
      .addTo(window.zoneMap)
      .bindPopup("You are here");
>>>>>>> 31502171d08cdc8b8e6e36c7f25152061fa8cd4e

    updateLocationName(lat, lng);
  });

  // ================= DEMO GARBAGE =================
  const garbageIcon = L.icon({
    iconUrl: "/static/demogarbage.jpeg",
    iconSize: [72, 72],
    iconAnchor: [36, 36],
    className: "demogarbage-icon"
  });

<<<<<<< HEAD
  // Default fallback view
  window.zoneMapInstance.setView([10.5276, 76.2144], 14);



  // Fixed demogarbage spawn locations (preloaded, not user-editable, spread out)

  window.demogarbageHp = 100;
  const demogarbageBosses = [
    {
      id: "demo_1",
      name: "Demo-garbage",
      zone: "Crimson Wastefront",
      cycle: "Nightfall Raid",
      hpPercent: 42,
      timeRemaining: "23:12:55",
      coords: [10.350078, 76.248586],
      contributions: []
    },
    {
      id: "demo_2",
      name: "Demo-garbage (East)",
      zone: "Crimson Wastefront",
      cycle: "Nightfall Raid",
      hpPercent: 68,
      timeRemaining: "18:04:10",
      coords: [10.350078, 76.278586],
      contributions: []
    }
  ];

  window.demogarbageMarkers = demogarbageBosses.map((boss) => {
    // danger radius
    L.circle(boss.coords, {
      radius: 400,
      color: "rgba(255, 80, 80, 0.6)",
      fillColor: "rgba(255, 80, 80, 0.25)",
      fillOpacity: 0.4,
=======
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
>>>>>>> 31502171d08cdc8b8e6e36c7f25152061fa8cd4e
      weight: 2,
      className: "danger-pulse",
      interactive: false
    }).addTo(window.zoneMap);

<<<<<<< HEAD
    const marker = L.marker(boss.coords, { icon: demoGarbageIcon })
      .addTo(window.zoneMapInstance)
      .bindPopup(boss.name);

    // 🔥 click → update UI
    marker.on("click", () => updateBossPanel(boss));

    return marker;
  });



  // Only game logic can change/remove these – e.g., when HP hits 0
  window.setdemogarbageHp = (hp) => {
    window.demogarbageHp = hp;
    if (hp <= 0 && window.demogarbageMarkers) {
      window.demogarbageMarkers.forEach((m) => {
        try {
          window.zoneMapInstance.removeLayer(m);
        } catch (e) {
          // ignore
        }
      });
    }
  };
});

// ================= TAB SWITCHING FIX =================

document.addEventListener("DOMContentLoaded", () => {
  const tabButtons = document.querySelectorAll(".tab-button");
  const tabContents = document.querySelectorAll(".tab-content");

  tabButtons.forEach((btn) => {
    btn.addEventListener("click", function () {
      const target = this.getAttribute("data-tab");
      if (!target) return;

      tabButtons.forEach((b) => b.classList.remove("active"));
      tabContents.forEach((c) => c.classList.remove("active"));

      this.classList.add("active");
      const panel = document.getElementById(target);
      if (panel) panel.classList.add("active");

      // 🔴 REQUIRED: re-render Leaflet AFTER dashboard tab is visible
      if (target === "dashboard" && window.zoneMapInstance) {
        setTimeout(() => {
          window.zoneMapInstance.invalidateSize();
        }, 50);
      }
    });
  });
});

function updateBossPanel(boss) {
  document.querySelector(".boss-name").textContent = boss.name;

  const metaSpans = document.querySelectorAll(".boss-meta span");
  metaSpans[0].textContent = boss.zone;
  metaSpans[1].textContent = boss.cycle;

  document.querySelector(".hp-bar-label span:last-child").textContent =
    `${boss.hpPercent}% remaining`;

  document.querySelector(".hp-bar-inner").style.width =
    `${boss.hpPercent}%`;

  document.querySelector(".cycle-time").textContent =
    boss.timeRemaining;
}


=======
    // Marker
    L.marker(boss.coords, { icon: garbageIcon })
      .addTo(window.zoneMap)
      .bindPopup(boss.name);
  });
});
>>>>>>> 31502171d08cdc8b8e6e36c7f25152061fa8cd4e
