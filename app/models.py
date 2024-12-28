from flask_login import UserMixin
from datetime import datetime
from app import db, login_manager  # login_manager import 추가

# 좋아요 테이블
table_letter_likes = db.Table('letter_likes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('letter_id', db.Integer, db.ForeignKey('letter.id'), primary_key=True)
)

# User 모델
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    
    letters = db.relationship('Letter', backref='author', lazy=True)
    liked_letters = db.relationship('Letter', secondary=table_letter_likes, 
                                    backref=db.backref('likes', lazy='dynamic'))

# 사용자 로더 설정
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Letter 모델
class Letter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    message = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(120), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
