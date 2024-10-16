
    # app.py
import json
import time
from flask import Flask, Response, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from sniper_biz import SteemSniperBackend

import os


sniper_bot = SteemSniperBackend()

app = Flask(__name__)
CORS(app)  # Abilita CORS per tutte le route

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///steem_sniper.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True, nullable=False)
        password_hash = db.Column(db.String(128))
        posting_key = db.Column(db.String(128))
        voter = db.Column(db.String(80))
        interval = db.Column(db.Integer)
        authors = db.relationship('Author', backref='user', lazy=True)

        def set_password(self, password):
            self.password_hash = generate_password_hash(password)

        def check_password(self, password):
            return check_password_hash(self.password_hash, password)

class Author(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(80), nullable=False)
        vote_percentage = db.Column(db.Float)
        post_delay_minutes = db.Column(db.Integer)
        daily_vote_limit = db.Column(db.Integer)
        add_comment = db.Column(db.Boolean)
        add_image = db.Column(db.Boolean)
        comment_text = db.Column(db.String(200))
        image_path = db.Column(db.String(200))
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

with app.app_context():
        db.create_all()

@app.route('/register', methods=['POST'])
def register():
        #stampa la request
        print(request.json)
        data = request.json
        if User.query.filter_by(username=data['username']).first():
            return jsonify({"error": "Username already exists"}), 400
        user = User(username=data['username'], voter=data['voter'], interval=data['interval'])
        user.set_password(data['password'])
        user.posting_key = data['posting_key']
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
        print(request.json)
        data = request.json
        user = User.query.filter_by(username=data['username']).first()
        if user and user.check_password(data['password']):
            return jsonify({"message": "Login successful"}), 200
        return jsonify({"error": "Invalid username or password"}), 401

@app.route('/configure_author', methods=['POST'])
def configure_author():
        print(request.json)
        data = request.json
        user = User.query.filter_by(username=data['username']).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        # vediamo cosa c'è in data
        print(data)
        author = Author(
            name=data['author_name'],
            vote_percentage=data['vote_percentage'],
            post_delay_minutes=data['post_delay_minutes'],
            daily_vote_limit=data['daily_vote_limit'],
            add_comment=data['add_comment'],
            add_image=data['add_image'],
            comment_text=data.get('comment_text'),
            image_path=data.get('image_path'),
            user_id=user.id
        )
        db.session.add(author)
        db.session.commit()
        return jsonify({"message": "Author configured successfully"}), 201

@app.route('/get_authors/<username>', methods=['GET'])
def get_authors(username):
        print(username)
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        authors = [
            {
                "name": author.name,
                "vote_percentage": author.vote_percentage,
                "post_delay_minutes": author.post_delay_minutes,
                "daily_vote_limit": author.daily_vote_limit,
                "add_comment": author.add_comment,
                "add_image": author.add_image,
                "comment_text": author.comment_text,
                "image_path": author.image_path
            } for author in user.authors
        ]
        return jsonify(authors), 200

@app.route('/delete_author', methods=['POST'])
def delete_author():
        print(request.json)
        data = request.json
        user = User.query.filter_by(username=data['username']).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        author = Author.query.filter_by(name=data['author_name'], user_id=user.id).first()
        if not author:
            return jsonify({"error": "Author not found"}), 404
        db.session.delete(author)
        db.session.commit()
        return jsonify({"message": "Author deleted successfully"}), 200
    
@app.route('/update_author', methods=['PUT'])
def update_author():
        print(request.json)
        data = request.json
        user = User.query.filter_by(username=data['username']).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        author = Author.query.filter_by(name=data['author_name'], user_id=user.id).first()
        if not author:
            return jsonify({"error": "Author not found"}), 404
        author.vote_percentage = data['vote_percentage']
        author.post_delay_minutes = data['post_delay_minutes']
        author.daily_vote_limit = data['daily_vote_limit']
        author.add_comment = data['add_comment']
        author.add_image = data['add_image']
        author.comment_text = data.get('comment_text')
        author.image_path = data.get('image_path')
        db.session.commit()
        return jsonify({"message": "Author updated successfully"}), 200
#get_author
@app.route('/get_author/<username>/<author_name>', methods=['GET'])
def get_author(username, author_name):
        print(username)
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        author = Author.query.filter_by(name=author_name, user_id=user.id).first()
        if not author:
            return jsonify({"error": "Author not found"}), 404
        return jsonify({
            "name": author.name,
            "vote_percentage": author.vote_percentage,
            "post_delay_minutes": author.post_delay_minutes,
            "daily_vote_limit": author.daily_vote_limit,
            "add_comment": author.add_comment,
            "add_image": author.add_image,
            "comment_text": author.comment_text,
            "image_path": author.image_path
        }), 200
#bulk_update_authors
@app.route('/bulk_update_authors', methods=['PUT'])
def bulk_update_authors():
    print(request.json)
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
#dell'autore ci arriva solo il nome per es ['gigi','franco','pippo','pluto','paperino','roberto']
    for author_name in data['authors']:
        author = Author.query.filter_by(name=author_name, user_id=user.id).first()
        if not author:
            return jsonify({"error": "Author not found"}), 404
        author.vote_percentage = data['vote_percentage']
        author.post_delay_minutes = data['post_delay_minutes']
        author.daily_vote_limit = data['daily_vote_limit']
        author.add_comment = data.get('add_comment' , False)
        author.add_image = data.get('add_image' , False)
        author.comment_text = data.get('comment_text')
        author.image_path = data.get('image_path')
        db.session.commit()
    return jsonify({"message": "Authors updated successfully"}), 200     
#bulk_delete_authors
@app.route('/bulk_delete_authors', methods=['POST'])
def bulk_delete_authors():
    print(request.json)
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    for author_name in data['authors']:
        author = Author.query.filter_by(name=author_name, user_id=user.id).first()
        if not author:
            return jsonify({"error": "Author not found"}), 404
        db.session.delete(author)
        db.session.commit()
    return jsonify({"message": "Authors deleted successfully"}), 200

@app.route('/get_all', methods=['GET'])
def get_all():
        users = User.query.all()
        response = []
        for user in users:
            authors = [
                {
                    "name": author.name,
                    "vote_percentage": author.vote_percentage,
                    "post_delay_minutes": author.post_delay_minutes,
                    "daily_vote_limit": author.daily_vote_limit,
                    "add_comment": author.add_comment,
                    "add_image": author.add_image,
                    "comment_text": author.comment_text,
                    "image_path": author.image_path
                } for author in user.authors
            ]
            response.append({
                "username": user.username,
                "voter": user.voter,
                "interval": user.interval,
                "authors": authors
            })
        return jsonify(response), 200

@app.route('/start_bot', methods=['POST'])
def start_bot():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    # Configura il bot con i dati dell'utente
    sniper_bot.configure(posting_key=user.posting_key, voter=user.voter, interval=user.interval)

    # Configura gli autori nel bot
    for author in user.authors:
        sniper_bot.configure_author(
            author.name,
            vote_percentage=author.vote_percentage,
            post_delay_minutes=author.post_delay_minutes,
            daily_vote_limit=author.daily_vote_limit,
            add_comment=author.add_comment,
            add_image=author.add_image,
            comment_text=author.comment_text,
            image_path=author.image_path
        )

    # Avvia il bot
    sniper_bot.start()

    return jsonify({"message": "Bot started successfully"}), 200

@app.route('/stop_bot', methods=['POST'])
def stop_bot():
    # Ferma il bot
    sniper_bot.stop()
    return jsonify({"message": "Bot stopped successfully"}), 200

@app.route('/stream_logs')
def stream_logs():
    def generate():
        while True:
            logs = sniper_bot.get_logs()
            if logs:
                yield f"data: {json.dumps(logs)}\n\n"
            time.sleep(1)  # Check for new logs every second

    return Response(generate(), mimetype='text/event-stream')

@app.route('/get_bot_status')
def get_bot_status():
    return jsonify({"running": sniper_bot.running})

if __name__ == '__main__':
        app.run(debug=True)
