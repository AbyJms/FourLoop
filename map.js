console.log("CareerForge loaded");

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

// ================= ZONE MAP FEATURE =================

document.addEventListener("DOMContentLoaded", () => {
  const mapContainer = document.getElementById("zoneMap");
  if (!mapContainer || typeof L === "undefined") return;

  // 🔹 Create map and expose globally (IMPORTANT for tabs)
  window.zoneMapInstance = L.map("zoneMap", {
    zoomControl: false,
    attributionControl: false
  });

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19
  }).addTo(window.zoneMapInstance);

  // Default fallback view
  window.zoneMapInstance.setView([10.5276, 76.2144], 14);

  // Try user location
  navigator.geolocation.getCurrentPosition(
    (pos) => {
      const lat = pos.coords.latitude;
      const lng = pos.coords.longitude;

      window.zoneMapInstance.setView([lat, lng], 15);

      const userIcon = L.icon({
  iconUrl: "you.jpg",
  iconSize: [36, 36],      // size of image
  iconAnchor: [18, 18],   // center the icon
  popupAnchor: [0, -18],  // popup position
  className: "user-map-icon"
});

L.marker([lat, lng], {
  icon: userIcon
})
.addTo(window.zoneMapInstance)
.bindPopup("You are here");

    },
    () => {}
  );

  // Demo quest markers
  L.circleMarker([10.5282, 76.2150], {
    radius: 6,
    color: "#ff4d4d"
  }).addTo(window.zoneMapInstance);

  L.circleMarker([10.5268, 76.2135], {
    radius: 6,
    color: "#ffcc33"
  }).addTo(window.zoneMapInstance);

  L.circleMarker([10.5272, 76.2128], {
    radius: 6,
    color: "#33ff99"
  }).addTo(window.zoneMapInstance);
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
