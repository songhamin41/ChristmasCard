import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'))
    app.config.from_object('config.Config')

    # SQLAlchemy 초기화
    db.init_app(app)

    # Jinja2 캐시 비활성화
    app.jinja_env.cache = {}

    # 블루프린트 등록
    from .routes import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()  # 테이블 생성

    return app
