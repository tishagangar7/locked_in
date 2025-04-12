import os
from flask import request, jsonify
from werkzeug.utils import secure_filename
from models import db, User, UserClass

# Configure upload folder and allowed file types
UPLOAD_FOLDER = 'uploads/'  # Directory to store uploaded images
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def register_profile_routes(app):
    """Register profile-related routes to the Flask app."""

    @app.route('/api/profile', methods=['POST'])
    def update_profile():
        """Update user profile information."""
        data = request.get_json()
        user_id = data.get("user_id")
        user = User.query.get(user_id)

        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404

        user.name = data.get("name")
        user.major = data.get("major")
        user.year = data.get("year")

        # Save CSV to User table
        class_list = data.get("classes", [])
        user.classes = ",".join(class_list)

        # Save to user_classes table too
        UserClass.query.filter_by(user_id=user_id).delete()  # clear old classes
        for c in class_list:
            db.session.add(UserClass(user_id=user_id, class_code=c))

        user.study_style = data.get("study_style")

        db.session.commit()
        return jsonify({"success": True, "message": "Profile updated"})

    @app.route('/api/profile/upload-image/<int:user_id>', methods=['POST'])
    def upload_profile_image(user_id):
        """Upload a profile image for the user."""
        if 'image' not in request.files:
            return jsonify({"success": False, "message": "No image file provided"}), 400

        file = request.files['image']
        if file.filename == '':
            return jsonify({"success": False, "message": "No selected file"}), 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, f"user_{user_id}_{filename}")
            file.save(filepath)

            # Optionally, save the image path to the database
            user = User.query.get(user_id)
            if not user:
                return jsonify({"success": False, "message": "User not found"}), 404
            user.profile_image = filepath  # Assuming `profile_image` is a column in the `User` model
            db.session.commit()

            return jsonify({"success": True, "message": "Image uploaded successfully", "image_url": filepath})

        return jsonify({"success": False, "message": "Invalid file type"}), 400