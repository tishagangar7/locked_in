// -------------------- Extract User ID --------------------
const urlParams = new URLSearchParams(window.location.search);
const userId = urlParams.get('user_id');
document.getElementById('user_id').value = userId;

// -------------------- Add Class Input --------------------
function addClassInput() {
  const newInputDiv = document.createElement("div");
  newInputDiv.style.display = "flex";
  newInputDiv.style.alignItems = "center";

  const newInput = document.createElement("input");
  newInput.type = "text";
  newInput.placeholder = "Enter class code";
  newInput.className = "class-input";
  newInput.style.marginRight = "10px";

  const removeBtn = document.createElement("button");
  removeBtn.type = "button";
  removeBtn.textContent = "Remove";
  removeBtn.style.color = "red";
  removeBtn.style.marginLeft = "10px";
  removeBtn.addEventListener("click", () => {
    newInputDiv.remove();
  });

  newInputDiv.appendChild(newInput);
  newInputDiv.appendChild(removeBtn);
  document.getElementById("classList").appendChild(newInputDiv);
}

document.getElementById("addClassBtn").addEventListener("click", addClassInput);

// -------------------- Real-Time Validation --------------------
function validateName() {
  const nameField = document.getElementById('name');
  nameField.style.borderColor = nameField.value.trim() ? '' : 'red';
}

function validateYear() {
  const yearField = document.getElementById('year');
  const year = parseInt(yearField.value);
  yearField.style.borderColor = isNaN(year) || year < 1 || year > 5 ? 'red' : '';
}

document.getElementById('name').addEventListener('input', validateName);
document.getElementById('year').addEventListener('input', validateYear);

// -------------------- Handle Profile Submission --------------------
async function submitProfile(e) {
  e.preventDefault();

  const responseMsg = document.getElementById('responseMsg');
  const classInputs = document.querySelectorAll(".class-input");
  const classes = Array.from(classInputs)
    .map(input => input.value.trim())
    .filter(val => val.length > 0);

  // Check for duplicate classes
  const uniqueClasses = new Set(classes);
  if (uniqueClasses.size !== classes.length) {
    responseMsg.textContent = "Duplicate classes are not allowed. Please remove duplicates.";
    responseMsg.style.color = "red";
    return;
  }

  const name = document.getElementById('name').value.trim();
  let major = document.getElementById('major').value.trim();
  const year = document.getElementById('year').value.trim();

  // Check if major is empty
  if (!major) {
    const proceed = window.confirm(
      "Major was empty. Defaulted to 'Undeclared'. Do you want to proceed or go back and change it?"
    );
    if (!proceed) {
      responseMsg.textContent = "⚠️ Please update your major.";
      responseMsg.style.color = "orange";
      return;
    }
    major = "Undeclared";
  }

  responseMsg.textContent = "⏳ Submitting your profile...";
  responseMsg.style.color = "blue";

  const data = {
    user_id: parseInt(document.getElementById('user_id').value),
    name: name,
    major: major,
    year: parseInt(year),
    classes: classes,
    study_style: document.getElementById('study_style').value
  };

  try {
    const res = await fetch('http://127.0.0.1:5000/api/profile', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });

    const result = await res.json();

    if (result.success) {
      responseMsg.textContent = result.message;
      responseMsg.style.color = "green";
    } else {
      responseMsg.textContent = result.message;
      responseMsg.style.color = "red";
    }
  } catch (error) {
    console.error("Error submitting profile:", error);
    responseMsg.textContent = "An error occurred. Please try again.";
    responseMsg.style.color = "red";
  }
}

document.getElementById('profileForm').addEventListener('submit', submitProfile);

// -------------------- Handle Image Upload --------------------
async function uploadImage(e) {
  e.preventDefault();

  const imageInput = document.getElementById('profileImage');
  const imageResponseMsg = document.getElementById('imageResponseMsg');

  if (!imageInput.files[0]) {
    imageResponseMsg.textContent = "Please select an image to upload.";
    imageResponseMsg.style.color = "red";
    return;
  }

  const formData = new FormData();
  formData.append('image', imageInput.files[0]);

  imageResponseMsg.textContent = "⏳ Uploading image...";
  imageResponseMsg.style.color = "blue";

  try {
    const res = await fetch(`http://127.0.0.1:5000/api/profile/upload-image/${userId}`, {
      method: 'POST',
      body: formData
    });

    const result = await res.json();

    if (result.success) {
      imageResponseMsg.textContent = result.message;
      imageResponseMsg.style.color = "green";
    } else {
      imageResponseMsg.textContent = result.message;
      imageResponseMsg.style.color = "red";
    }
  } catch (error) {
    console.error("Error uploading image:", error);
    imageResponseMsg.textContent = "An error occurred. Please try again.";
    imageResponseMsg.style.color = "red";
  }
}

document.getElementById('imageUploadForm').addEventListener('submit', uploadImage);