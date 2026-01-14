console.log("CareerForge loaded");

// Basic validation for the Student / Employee registration form
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("studentRegisterForm");
  if (!form) return; // Only run on the student register page

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

  const isValidGmail = (value) => {
    const gmailRegex = /^[a-zA-Z0-9._%+-]+@gmail\.com$/;
    return gmailRegex.test(value);
  };

  const isValidPassword = (value) => {
    // At least 8 chars, 1 uppercase, 1 lowercase, 1 number, 1 symbol
    const passwordRegex =
      /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$/;
    return passwordRegex.test(value);
  };

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
      setError("email", "Please enter a valid Gmail address (ends with @gmail.com).");
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
        formMessage.textContent = "Please fix the errors above and try again.";
        formMessage.classList.add("error");
      }
      return;
    }

    // For now just show a success message – this is where you'd send data to a backend.
    if (formMessage) {
      formMessage.textContent = "Registration details look good! (Demo only, not submitted.)";
      formMessage.classList.remove("error");
    }

    // Optionally clear the form
    // form.reset();
  });
});

// ================= ZONE MAP FEATURE =================

// Make sure map exists on page
document.addEventListener("DOMContentLoaded", () => {
  const mapContainer = document.getElementById("zoneMap");
  if (!mapContainer) return;

  // Initialize map
  const map = L.map("zoneMap", {
    zoomControl: false,
    attributionControl: false
  });

  // OpenStreetMap tiles
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19
  }).addTo(map);

  // Try to get user location
  navigator.geolocation.getCurrentPosition(
    (pos) => {
      const lat = pos.coords.latitude;
      const lng = pos.coords.longitude;

      map.setView([lat, lng], 15);

      // User marker
      L.circleMarker([lat, lng], {
        radius: 6,
        color: "#ff0000",
        fillColor: "#ff0000",
        fillOpacity: 0.9
      })
      .addTo(map)
      .bindPopup("You are here");
    },
    () => {
      // Fallback location (demo)
      map.setView([10.5276, 76.2144], 14);
    }
  );

  // Example quest markers (demo)
  L.circleMarker([10.5282, 76.2150], {
    radius: 6,
    color: "#ff4d4d"
  }).addTo(map);

  L.circleMarker([10.5268, 76.2135], {
    radius: 6,
    color: "#ffcc33"
  }).addTo(map);

  L.circleMarker([10.5272, 76.2128], {
    radius: 6,
    color: "#33ff99"
  }).addTo(map);
});
