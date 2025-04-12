# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

app = Flask(__name__)
CORS(app)

# DB Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create DB
with app.app_context():
    db.create_all()
    
#SIGNUP ROUTE
@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({"success": False, "message": "Email already registered"}), 400

    hashed_pw = generate_password_hash(password)
    new_user = User(email=email, password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"success": True, "user_id": new_user.id})

# LOGIN ROUTE
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        return jsonify({"success": True, "user_id": user.id})
    
    return jsonify({"success": False, "message": "Invalid credentials"}), 401

if __name__ == '__main__':
    app.run(debug=True)


