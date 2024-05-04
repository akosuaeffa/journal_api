from flask import jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Entry
from journal_api import app
from datetime import datetime


# CRUD operations for Entries
# to create an entry
@app.route('/entries', methods=['POST'])
def create_entry():
    try:
        data = request.get_json()
        title = data.get('title')
        content = data.get ('content')
        user_id = data.get ('user_id')

        new_entry = Entry(title=title, content=content, user_id=user_id)
        db.session.add(new_entry)
        db.session.commit()

        return jsonify({"message": "Entry created succesfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# to get entries   
@app.route('/entries', methods=['GET'])
def get_entries():
    try:
        entries_data = db.session.query(Entry, User).join(User).all()
        entries = []
        for entry, user in entries_data:
            entry_data = {
                'title': entry.title,
                'user': user.username,
                'date': entry.date.strftime("%Y-%m-%d %H:%M:%S")
            }
            entries.append(entry_data)
        return jsonify(entries), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# to update an entry
@app.route('/entries/<int:entry_id>', methods=['PUT'])
def update_entry(entry_id):
    try:
        data = request.get_json()
        title = data.get('title')
        content = data.get('content')

        entry = Entry.query.get(entry_id)
        if not entry:
            return jsonify({"error": "Entry not found"}), 404
        
        entry.title = title
        entry.content = content
        db.session.commit()

        return jsonify({"message": "Entry updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500    

@app.route('/entries/<date>', methods=['GET'])
def get_entries_by_date(date):
    try:
        specified_date = datetime.strptime(date, '%Y-%m-%d').date()

        entries = Entry.query.filter(Entry.date == specified_date).all()

        entries_data = [{
            'title': entry.title,
            'user': entry.user.username,
            'date': entry.date.strftime("%Y-%m-%d %H:%M:%S")
            } for entry in entries]
        
        return jsonify(entries_data), 200
    except Exception as e:
        return jsonify ({"error": str(e)}), 500