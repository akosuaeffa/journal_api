from flask import jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Entry
from journal_api import app

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
        
        new_user = User(email=email, username=username)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created succesfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# user list and enteries published
@app.route('/user', methods=['GET'])
def get_users_with_entries():
    try:
        users_with_enteries = []
        users = User.query.all()
        for user in users:
            user_list = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'entries': [{'title': entry.title, 'date': entry.date.strftime("%Y-%m-%d %H:%M:%S")} for entry in user.entries]
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
    except Exception as e:
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
        return jsonify({"error": str(e)}), 500