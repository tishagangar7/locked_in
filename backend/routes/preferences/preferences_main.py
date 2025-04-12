from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
from flask import Blueprint, request, jsonify
from routes.preferences.get_keys import load_text, load_pdf_text, process_syllabus
from routes.preferences.get_schedule import process_user_schedule
import os


# Create a Flask Blueprint for preferences
preferences_bp = Blueprint('preferences', __name__)

# Upload folder configuration
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the folder exists

# -------------------- CHOOSE MEDIUM --------------------
@preferences_bp.route('/choose-medium', methods=['POST'])
def choose_medium():
    """
    Allows the user to select their preferred medium (remote or in-person).
    """
    data = request.get_json()
    user_id = data.get('user_id')
    medium = data.get('medium')  # "remote" or "in-person"

    if not user_id or not medium:
        return jsonify({"error": "User ID and medium are required"}), 400

    # Update the user's medium preference in the database
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.medium = medium
    db.session.commit()

    return jsonify({"success": True, "message": f"Medium set to {medium} for user {user_id}"}), 200

# -------------------- UPLOAD SYLLABUS --------------------
@preferences_bp.route('/upload-syllabus', methods=['POST'])
def upload_syllabus():
    """
    Handles syllabus uploads (PDF or text) or text input.
    Saves the file in the uploads folder and returns the file path.
    """
    if 'file' in request.files:
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        # Save the uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        return jsonify({"success": True, "filepath": filepath}), 200

    elif 'text' in request.form:
        # Save the text input as a .txt file
        text = request.form['text']
        filename = secure_filename(f"user_input_{len(os.listdir(UPLOAD_FOLDER)) + 1}.txt")
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
        return jsonify({"success": True, "filepath": filepath}), 200

    else:
        return jsonify({"error": "No file or text input provided"}), 400

# -------------------- PROCESS SYLLABUS --------------------
@preferences_bp.route('/process-syllabus', methods=['POST'])
def process_syllabus_route():
    """
    Processes the uploaded syllabus file and extracts topics and keywords.
    """
    data = request.get_json()
    filepath = data.get('filepath')  # Path to the uploaded file

    if not filepath or not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 400

    # Process the syllabus file
    use_structured_prompt = data.get('use_structured_prompt', True)  # Default to structured prompt
    extracted_data = process_syllabus(filepath, use_structured_prompt=use_structured_prompt)

    if extracted_data:
        return jsonify({"success": True, "extracted_data": extracted_data}), 200
    else:
        return jsonify({"success": False, "message": "Failed to process the syllabus"}), 500

# -------------------- SELECT TOPICS --------------------
@preferences_bp.route('/select-topics', methods=['POST'])
def select_topics():
    """
    Allows the user to select topics/keywords from the processed syllabus.
    """
    data = request.get_json()
    user_id = data.get('user_id')
    selected_topics = data.get('selected_topics')  # List of selected topics

    if not user_id or not selected_topics:
        return jsonify({"error": "User ID and selected topics are required"}), 400

    # Save the selected topics to the database (or in-memory storage)
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.selected_topics = ','.join(selected_topics)  # Save as a comma-separated string
    db.session.commit()

    return jsonify({"success": True, "message": "Selected topics saved successfully"}), 200

# -------------------- SET SCHEDULE --------------------
@preferences_bp.route('/process-schedule', methods=['POST'])
def process_schedule_route():
    """
    Processes the user's schedule and validates time slots.
    """
    data = request.get_json()
    processed_schedule = process_user_schedule(data)  # Call the function from preferences.py
    return jsonify(processed_schedule)

# -------------------- GET CLASSES --------------------
@preferences_bp.route('/get-classes', methods=['GET'])
def get_classes():
    """
    Retrieves the list of classes for the user from the database.
    """
    user_id = request.args.get('user_id')  # Get user_id from query parameters
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Retrieve classes associated with the user
    classes = Class.query.filter_by(user_id=user_id).all()
    class_list = [{"id": c.id, "name": c.name} for c in classes]

    return jsonify({"success": True, "classes": class_list}), 200

# -------------------- SAVE SCHEDULE --------------------
@preferences_bp.route('/save-schedule', methods=['POST'])
def save_schedule():
    """
    Saves the user's schedule to the database.
    """
    data = request.get_json()
    user_id = data.get('user_id')
    schedule = data.get('schedule')  # List of schedule slots

    if not user_id or not schedule:
        return jsonify({"error": "User ID and schedule are required"}), 400

    # Save the schedule to the database (example implementation)
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Assuming User has a `schedule` column to store JSON data
    user.schedule = schedule  # Save as JSON
    db.session.commit()

    return jsonify({"success": True, "message": "Schedule saved successfully!"}), 200

# -------------------- GET SCHEDULE --------------------
@preferences_bp.route('/get-schedule', methods=['GET'])
def get_schedule():
    """
    Retrieves the user's saved schedule from the database.
    """
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Assuming User has a `schedule` column
    schedule = user.schedule or []
    return jsonify({"success": True, "schedule": schedule}), 200

# # Create a Flask Blueprint for preferences
# preferences_bp = Blueprint('preferences', __name__)

# # Upload folder configuration
# UPLOAD_FOLDER = './uploads'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the folder exists

# # -------------------- UPLOAD SYLLABUS --------------------
# @preferences_bp.route('/upload-syllabus', methods=['POST'])
# def upload_syllabus():
#     """
#     Handles syllabus uploads (PDF or text) or text input.
#     Saves the file in the uploads folder and returns the file path.
#     """
#     if 'file' in request.files:
#         file = request.files['file']
#         if file.filename == '':
#             return jsonify({"error": "No file selected"}), 400

#         # Save the uploaded file
#         filename = secure_filename(file.filename)
#         filepath = os.path.join(UPLOAD_FOLDER, filename)
#         file.save(filepath)
#         return jsonify({"success": True, "filepath": filepath}), 200

#     elif 'text' in request.form:
#         # Save the text input as a .txt file
#         text = request.form['text']
#         filename = secure_filename(f"user_input_{len(os.listdir(UPLOAD_FOLDER)) + 1}.txt")
#         filepath = os.path.join(UPLOAD_FOLDER, filename)
#         with open(filepath, 'w', encoding='utf-8') as f:
#             f.write(text)
#         return jsonify({"success": True, "filepath": filepath}), 200

#     else:
#         return jsonify({"error": "No file or text input provided"}), 400

# # -------------------- PROCESS SYLLABUS --------------------
# @preferences_bp.route('/process-syllabus', methods=['POST'])
# def process_syllabus_route():
#     """
#     Processes the uploaded syllabus file and extracts topics and keywords.
#     """
#     data = request.get_json()
#     filepath = data.get('filepath')  # Path to the uploaded file

#     if not filepath or not os.path.exists(filepath):
#         return jsonify({"error": "File not found"}), 400

#     # Process the syllabus file
#     use_structured_prompt = data.get('use_structured_prompt', True)  # Default to structured prompt
#     extracted_data = process_syllabus(filepath, use_structured_prompt=use_structured_prompt)

#     if extracted_data:
#         return jsonify({"success": True, "extracted_data": extracted_data}), 200
#     else:
#         return jsonify({"success": False, "message": "Failed to process the syllabus"}), 500

# # -------------------- PROCESS USER SCHEDULE --------------------
# @preferences_bp.route('/process-schedule', methods=['POST'])
# def process_schedule_route():
#     """
#     Processes the user's schedule and validates time slots.
#     """
#     data = request.get_json()
#     processed_schedule = process_user_schedule(data)  # Call the function from preferences.py
#     return jsonify(processed_schedule)

# # -------------------- GET USER SCHEDULE --------------------
# @preferences_bp.route('/get-schedule', methods=['GET'])
# def get_schedule_route():
#     """
#     Retrieves the user's schedule from the database or in-memory storage.
#     """
#     user_id = request.args.get('user_id')  # Get user_id from query parameters
#     if not user_id:
#         return jsonify({"error": "User ID is required"}), 400

#     try:
#         # Call the function from get_schedule.py
#         schedule_data = process_user_schedule({"user_id": user_id})
#         return jsonify({"success": True, "schedule": schedule_data}), 200
#     except Exception as e:
#         return jsonify({"success": False, "message": "Failed to retrieve schedule", "error": str(e)}), 500