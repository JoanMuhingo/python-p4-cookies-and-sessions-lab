#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate
from datetime import datetime

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear', methods=['GET'])
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():

    pass

@app.route('/articles/<int:id>', methods=['GET'])
def show_article(id):

    session['page_views'] = session.get('page_views', 0) + 1

    if session['page_views'] <= 3:
        
        article_data = {
            'article_id': id,
            'page_views': session['page_views'],
            'author': 'John Doe',
            'title': 'Sample Article',
            'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
            'preview': 'This is a preview of the article.',
            'minutes_to_read': '8',
            'date' : datetime.utcnow(),
        }
        
        
        return jsonify(article_data)
    else:
        # User has viewed too many pages
        message = {
            'message': 'Maximum pageview limit reached'
        }
        return jsonify(message), 401 # 401 unauthorized

if __name__ == '__main__':
    app.run(port=5555)
