from flask import jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Entry, app

# CRUD operations for users
# route to create a user
@app.route('/user', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        username = data['username']
        email = data['email']

        if not username or not email:
            return jsonify({"error": "Username and email are required"}), 400

        existing_user = User.query.filter_by(email=email, username=username).all()
        if existing_user:
            return jsonify({"message": "User allready exixts"}), 409
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            return jsonify({"message":"email already exists"}), 409
        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            return jsonify({"message": "Username already exists"}), 409
        
        new_user = User(email=email, username=username)
        db.session.add(new_user)
        db.session.commit()

        user_id = new_user.id
        return jsonify({"message": "User created succesfully with ID " + str(user_id)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# user list and enteries published
@app.route('/user', methods=['GET'])
def get_users_with_entries():
    try:
        users_with_enteries = []
        users = User.query.all()
        for user in users:
            user_entries = [{'title': entry.title, 'date': entry.date.strftime("%Y-%m-%d %H:%M:%S")} for entry in user.entries]
            user_list = {
                'id': user.id,
                'username': user.username,
                'email': user.email,  
            }
            users_with_enteries.append(user_list)
        return jsonify(users_with_enteries), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#details of each and every user with their published entries
@app.route('/user/<int:user_id>/entries', methods=['GET'])
def get_user_entries(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        user_entries = [{'title': entry.title, 'date': entry.date.strftime("%Y-%m-%d %H:%M:%S")} for entry in user.entries] 
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'entries': user_entries
        }
        return jsonify(user_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# operation to update a user
@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        
        if not username or not email:
            return jsonify({"error": "Username and email requires"}), 400

        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        user.username = username
        user.email = email
        db.session.commit()

        return jsonify({"message": "User update successfully"}), 200
    except KeyError as e:
        return jsonify ({"message": f"Missing key in JSON data: {str(e)}"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    

# operation to delete a user
@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        db.session.delete(user)
        db.session.commit()

        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500