const API_BASE_URL = "http://127.0.0.1:5000";

// -------------------- Redirect to Schedule --------------------
function redirectToSchedule() {
  window.location.href = "./schedule.html";
}

// -------------------- Submit Medium --------------------
async function submitMedium() {
  const medium = document.getElementById("medium-select").value;
  const messageEl = document.getElementById("medium-message");

  if (!medium) {
    messageEl.textContent = "Please select a medium.";
    messageEl.className = "message error";
    return;
  }

  const userId = localStorage.getItem("user_id");

  try {
    const response = await fetch(`${API_BASE_URL}/preferences/choose-medium`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: userId, medium }),
    });
    const data = await response.json();
    messageEl.textContent = data.message || "Medium updated successfully!";
    messageEl.className = "message success";
  } catch (error) {
    console.error("Error updating medium:", error);
    messageEl.textContent = "Failed to update medium.";
    messageEl.className = "message error";
  }
}

// -------------------- Upload Syllabus --------------------
async function uploadSyllabus() {
    const fileInput = document.getElementById("syllabus-file");
    const textInput = document.getElementById("syllabus-text");
    const messageEl = document.getElementById("syllabus-message");
    const topicsList = document.getElementById("topics-list");
  
    const formData = new FormData();
    if (fileInput.files[0]) {
      formData.append("file", fileInput.files[0]);
    } else if (textInput.value) {
      formData.append("text", textInput.value);
    } else {
      messageEl.textContent = "Please upload a file or enter text.";
      messageEl.className = "message error";
      return;
    }
  
    try {
      const response = await fetch(`${API_BASE_URL}/preferences/upload-syllabus`, {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
  
      if (data.success) {
        messageEl.textContent = "Syllabus uploaded successfully!";
        messageEl.className = "message success";
  
        // Fetch and display extracted topics
        const extractedResponse = await fetch(`${API_BASE_URL}/preferences/process-syllabus`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ filepath: data.filepath }),
        });
        const extractedData = await extractedResponse.json();
  
        console.log("Extracted Data:", extractedData); // Debugging
  
        if (extractedData.success) {
          const topics = extractedData.extracted_data.weekly_topics; // Access directly
          console.log("Weekly Topics:", topics); // Debugging
  
          if (topics && topics.length > 0) {
            topicsList.innerHTML = topics
              .map(
                (topic, index) => `
              <div>
                <input type="checkbox" id="topic-${index}" value="${topic}">
                <label for="topic-${index}">${topic}</label>
              </div>
            `
              )
              .join("");
          } else {
            topicsList.innerHTML = "<p>No topics found in the syllabus.</p>";
          }
        } else {
          topicsList.innerHTML = "<p>Failed to extract topics.</p>";
        }
      } else {
        messageEl.textContent = data.error || "Failed to upload syllabus.";
        messageEl.className = "message error";
      }
    } catch (error) {
      console.error("Error uploading syllabus:", error);
      messageEl.textContent = "Failed to upload syllabus.";
      messageEl.className = "message error";
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
    messageEl.className = "message error";
    return;
  }

  const userId = localStorage.getItem("user_id");

  try {
    const response = await fetch(`${API_BASE_URL}/preferences/select-topics`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: userId, selected_topics: selectedTopics }),
    });
    const data = await response.json();
    messageEl.textContent = data.success ? "Topics submitted successfully!" : data.error;
    messageEl.className = data.success ? "message success" : "message error";
  } catch (error) {
    console.error("Error submitting topics:", error);
    messageEl.textContent = "Failed to submit topics.";
    messageEl.className = "message error";
  }
}