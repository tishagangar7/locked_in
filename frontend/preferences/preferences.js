const API_BASE_URL = "http://127.0.0.1:5000";

// -------------------- Redirect to Schedule --------------------
function redirectToSchedule() {
  // Redirect to schedule.html
  window.location.href = "./schedule.html";
}

// -------------------- Load Schedule Data --------------------
async function loadSchedule() {
  const userId = 1; // Replace with the actual user ID
  const scheduleDisplay = document.getElementById("schedule-display");

  try {
    const response = await fetch(`${API_BASE_URL}/preferences/get-schedule?user_id=${userId}`);
    const data = await response.json();

    if (data.success && data.schedule.length > 0) {
      scheduleDisplay.innerHTML = "<h3>Your Schedule Preferences:</h3>";
      data.schedule.forEach((slot, index) => {
        const slotEl = document.createElement("div");
        slotEl.innerHTML = `
          <p><strong>Slot ${index + 1}:</strong> ${slot.date}, ${slot.time} (${slot.category})</p>
        `;
        scheduleDisplay.appendChild(slotEl);
      });
    } else {
      scheduleDisplay.innerHTML = "<p>No schedule preferences set yet.</p>";
    }
  } catch (error) {
    console.error("Error loading schedule:", error);
    scheduleDisplay.innerHTML = "<p>Failed to load schedule preferences.</p>";
  }
}

// -------------------- Submit Medium --------------------
async function submitMedium() {
  const medium = document.getElementById("medium-select").value;
  const messageEl = document.getElementById("medium-message");

  if (!medium) {
    messageEl.textContent = "Please select a medium.";
    return;
  }

  const userId = 1; // Replace with the actual user ID

  try {
    const response = await fetch(`${API_BASE_URL}/preferences/choose-medium`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: userId, medium }),
    });
    const data = await response.json();
    messageEl.textContent = data.message || "Medium updated successfully!";
  } catch (error) {
    console.error("Error updating medium:", error);
    messageEl.textContent = "Failed to update medium.";
  }
}

// -------------------- Upload Syllabus --------------------
async function uploadSyllabus() {
  const fileInput = document.getElementById("syllabus-file");
  const textInput = document.getElementById("syllabus-text");
  const messageEl = document.getElementById("syllabus-message");

  const formData = new FormData();
  if (fileInput.files[0]) {
    formData.append("file", fileInput.files[0]);
  } else if (textInput.value) {
    formData.append("text", textInput.value);
  } else {
    messageEl.textContent = "Please upload a file or enter text.";
    return;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/preferences/upload-syllabus`, {
      method: "POST",
      body: formData,
    });
    const data = await response.json();
    messageEl.textContent = data.success ? "Syllabus uploaded successfully!" : data.error;
  } catch (error) {
    console.error("Error uploading syllabus:", error);
    messageEl.textContent = "Failed to upload syllabus.";
  }
}

// -------------------- Submit Topics --------------------
async function submitTopics() {
  const selectedTopics = Array.from(document.querySelectorAll("#topics-list input:checked")).map(
    (input) => input.value
  );
  const messageEl = document.getElementById("topics-message");

  if (selectedTopics.length === 0) {
    messageEl.textContent = "Please select at least one topic.";
    return;
  }

  const userId = 1; // Replace with the actual user ID

  try {
    const response = await fetch(`${API_BASE_URL}/preferences/select-topics`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: userId, selected_topics: selectedTopics }),
    });
    const data = await response.json();
    messageEl.textContent = data.success ? "Topics submitted successfully!" : data.error;
  } catch (error) {
    console.error("Error submitting topics:", error);
    messageEl.textContent = "Failed to submit topics.";
  }
}

// -------------------- On Page Load --------------------
document.addEventListener("DOMContentLoaded", () => {
  loadSchedule();
});