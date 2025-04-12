const API_BASE_URL = "http://127.0.0.1:5000";

document.getElementById("signup-form").addEventListener("submit", async (event) => {
  event.preventDefault(); // Prevent form from refreshing the page

  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  const messageEl = document.getElementById("signup-message");

  try {
    const response = await fetch(`${API_BASE_URL}/api/signup`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    const data = await response.json();

    if (data.success) {
      // Redirect to profile.html
      window.location.href = "profile.html";
    } else {
      messageEl.textContent = data.error || "Signup failed. Please try again.";
    }
  } catch (error) {
    console.error("Error during signup:", error);
    messageEl.textContent = "An error occurred. Please try again.";
  }
});