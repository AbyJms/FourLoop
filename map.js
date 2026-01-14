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

      document.getElementById("currentLocation").textContent = place;
    })
    .catch(() => {
      document.getElementById("currentLocation").textContent = "Your Area";
    });
}


// ================= FORM VALIDATION =================

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("studentRegisterForm");
  if (!form) return;

  const firstNameInput = document.getElementById("firstName");
  const lastNameInput = document.getElementById("lastName");
  const usernameInput = document.getElementById("username");
  const emailInput = document.getElementById("email");
  const passwordInput = document.getElementById("password");
  const formMessage = document.getElementById("formMessage");

  const setError = (fieldName, message) => {
    const el = document.querySelector(`.field-error[data-for="${fieldName}"]`);
    if (el) el.textContent = message || "";
  };

  const clearAllErrors = () => {
    document.querySelectorAll(".field-error").forEach((el) => {
      el.textContent = "";
    });
    if (formMessage) {
      formMessage.textContent = "";
      formMessage.classList.remove("error");
    }
  };

  const isValidGmail = (value) =>
    /^[a-zA-Z0-9._%+-]+@gmail\.com$/.test(value);

  const isValidPassword = (value) =>
    /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$/.test(value);

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    clearAllErrors();

    let hasError = false;

    if (!firstNameInput.value.trim()) {
      setError("firstName", "First name is required.");
      hasError = true;
    }

    if (!lastNameInput.value.trim()) {
      setError("lastName", "Last name is required.");
      hasError = true;
    }

    if (!usernameInput.value.trim()) {
      setError("username", "Username is required.");
      hasError = true;
    }

    const emailValue = emailInput.value.trim();
    if (!emailValue) {
      setError("email", "Gmail address is required.");
      hasError = true;
    } else if (!isValidGmail(emailValue)) {
      setError(
        "email",
        "Please enter a valid Gmail address (ends with @gmail.com)."
      );
      hasError = true;
    }

    const passwordValue = passwordInput.value;
    if (!passwordValue) {
      setError("password", "Password is required.");
      hasError = true;
    } else if (!isValidPassword(passwordValue)) {
      setError(
        "password",
        "Password must be at least 8 characters and include 1 uppercase, 1 lowercase, 1 number, and 1 symbol."
      );
      hasError = true;
    }

    if (hasError) {
      if (formMessage) {
        formMessage.textContent =
          "Please fix the errors above and try again.";
        formMessage.classList.add("error");
      }
      return;
    }

    if (formMessage) {
      formMessage.textContent =
        "Registration details look good! (Demo only, not submitted.)";
      formMessage.classList.remove("error");
    }
  });
});

function getUserLocationOnce(callback) {
  const cached = sessionStorage.getItem("zoneMapUserLocation");

  // 1️⃣ If we already have coords → use them, DO NOTHING ELSE
  if (cached) {
    try {
      const { lat, lng } = JSON.parse(cached);
      if (typeof lat === "number" && typeof lng === "number") {
        callback(lat, lng);
        return; // 🔥 stops everything
      }
    } catch (e) { }
  }

  // 2️⃣ If no cache, check permission state FIRST
  if (!navigator.permissions || !navigator.geolocation) return;

  navigator.permissions.query({ name: "geolocation" }).then((status) => {
    if (status.state === "granted") {
      // permission already granted → safe to ask ONCE
      navigator.geolocation.getCurrentPosition((pos) => {
        const lat = pos.coords.latitude;
        const lng = pos.coords.longitude;

        sessionStorage.setItem(
          "zoneMapUserLocation",
          JSON.stringify({ lat, lng })
        );

        callback(lat, lng);
      });
    } else if (status.state === "prompt") {
      // first ever ask
      navigator.geolocation.getCurrentPosition((pos) => {
        const lat = pos.coords.latitude;
        const lng = pos.coords.longitude;

        sessionStorage.setItem(
          "zoneMapUserLocation",
          JSON.stringify({ lat, lng })
        );

        callback(lat, lng);
      });
    } else {
      console.warn("Location denied");
    }
  });
}

// ================= ZONE MAP FEATURE =================

document.addEventListener("DOMContentLoaded", () => {
  const mapContainer = document.getElementById("zoneMap");
  if (!mapContainer || typeof L === "undefined") return;

  // 🔹 Create map and expose globally (IMPORTANT for tabs)
  window.zoneMapInstance = L.map("zoneMap", {
    zoomControl: false,
    attributionControl: false
  });

  // 🔹 Default OpenStreetMap tiles (normal light map)
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: '&copy; OpenStreetMap contributors',
    maxZoom: 19
  }).addTo(window.zoneMapInstance);

  // 🔹 Fullscreen toggle
  const mapWrapper = mapContainer.closest(".map-wrapper");
  const fullscreenBtn = mapWrapper?.querySelector(".map-fullscreen-btn");

  const applySizeFix = () => {
    if (window.zoneMapInstance) {
      setTimeout(() => window.zoneMapInstance.invalidateSize(), 150);
    }
  };

  const toggleFullscreen = () => {
    if (!mapWrapper) return;
    const isActive = mapWrapper.classList.toggle("is-fullscreen");
    if (fullscreenBtn) {
      fullscreenBtn.textContent = isActive ? "Exit Fullscreen" : "Fullscreen";
    }
    applySizeFix();
  };

  if (fullscreenBtn) {
    fullscreenBtn.addEventListener("click", toggleFullscreen);
  }

  const locationEl = document.getElementById("currentLocation");

  getUserLocationOnce((lat, lng) => {
    // Center map
    window.zoneMapInstance.setView([lat, lng], 15);

    // User marker
    const userIcon = L.icon({
      iconUrl: "you.jpg",
      iconSize: [36, 36],
      iconAnchor: [18, 18],
      popupAnchor: [0, -18],
      className: "user-map-icon"
    });

    L.marker([lat, lng], { icon: userIcon })
      .addTo(window.zoneMapInstance)
      .bindPopup("You are here");

    // 🔥 UPDATE UI TEXT (THIS WAS NEVER RUNNING BEFORE)
    if (locationEl) {
      locationEl.textContent = "Location locked";
    }
  });

  // Fixed demogarbage icon (large, no outline, cannot be moved by players)
  const demoGarbageIcon = L.icon({
    iconUrl: "demogarbage.jpeg",
    iconSize: [72, 72],
    iconAnchor: [36, 36],
    popupAnchor: [0, -36],
    className: "demogarbage-icon"
  });

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
      weight: 2,
      interactive: false,
      className: "danger-pulse"
    }).addTo(window.zoneMapInstance);

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


getUserLocationOnce((lat, lng) => {
  // center the map
  window.zoneMapInstance.setView([lat, lng], 15);

  // add user marker
  const userIcon = L.icon({
    iconUrl: "you.jpg",
    iconSize: [36, 36],
    iconAnchor: [18, 18],
    popupAnchor: [0, -18],
    className: "user-map-icon"
  });

  L.marker([lat, lng], { icon: userIcon })
    .addTo(window.zoneMapInstance)
    .bindPopup("You are here");

  // update text
  const el = document.getElementById("currentLocation");
  if (el) {
    el.textContent = "Location locked";
  }
});

