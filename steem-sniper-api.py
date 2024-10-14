
    # app.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
import os

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
        data = request.json
        user = User.query.filter_by(username=data['username']).first()
        if user and user.check_password(data['password']):
            return jsonify({"message": "Login successful"}), 200
        return jsonify({"error": "Invalid username or password"}), 401

@app.route('/configure_author', methods=['POST'])
def configure_author():
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

if __name__ == '__main__':
        app.run(debug=True)
