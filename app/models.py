from . import db
from datetime import datetime

class Letter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)  # 작성자 이름
    message = db.Column(db.Text, nullable=False)  # 편지 내용
    date = db.Column(db.DateTime, default=datetime.utcnow)  # 작성 날짜
    image = db.Column(db.String(120), nullable=True)  # 이미지 파일 경로
