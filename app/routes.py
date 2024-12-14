from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.utils import secure_filename
from .models import db, Letter
import os

main = Blueprint('main', __name__)

# 업로드 경로 설정 (절대 경로로 변경)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')  # 절대 경로로 설정

# 업로드 폴더가 없으면 생성
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@main.route('/')
def home():
    # 데이터베이스에서 모든 편지 가져오기
    letters = Letter.query.all()
    return render_template('index.html', letters=letters)

@main.route('/write_letter', methods=['GET', 'POST'])
def write_letter():
    if request.method == 'POST':
        name = request.form['name']
        message = request.form['message']
        image = None

        if 'image' in request.files:
            image_file = request.files['image']
            if image_file.filename != '':
                # 파일 이름 안전화 및 저장
                image = secure_filename(image_file.filename)
                image_path = os.path.join(UPLOAD_FOLDER, image)
                image_file.save(image_path)

        # 데이터베이스에 저장
        new_letter = Letter(name=name, message=message, image=image)
        db.session.add(new_letter)
        db.session.commit()
        flash("Your letter has been sent!", "success")
        return redirect(url_for('main.home'))

    return render_template('write_letter.html')

@main.route('/delete_letter/<int:letter_id>', methods=['POST'])
def delete_letter(letter_id):
    letter = Letter.query.get(letter_id)
    if letter:
        # 파일 삭제 (이미지 파일이 있을 경우)
        if letter.image:
            image_path = os.path.join(UPLOAD_FOLDER, letter.image)
            if os.path.exists(image_path):
                os.remove(image_path)

        # 데이터베이스에서 삭제
        db.session.delete(letter)
        db.session.commit()
        flash("The letter has been deleted successfully!", "success")
    else:
        flash("The letter does not exist.", "danger")
    return redirect(url_for('main.home'))

@main.route('/edit_letter/<int:letter_id>', methods=['GET'])
def edit_letter(letter_id):
    # 편지 수정 페이지
    letter = Letter.query.get_or_404(letter_id)
    return render_template('edit_letter.html', letter=letter)

@main.route('/update_letter/<int:letter_id>', methods=['POST'])
def update_letter(letter_id):
    # 편지 업데이트 처리
    letter = Letter.query.get_or_404(letter_id)
    letter.name = request.form['name']
    letter.message = request.form['message']
    
    if 'image' in request.files and request.files['image'].filename != '':
        image_file = request.files['image']
        image_filename = secure_filename(image_file.filename)
        
        # 업로드 폴더가 없으면 생성
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        # 기존 이미지 파일 삭제
        if letter.image:
            old_image_path = os.path.join(UPLOAD_FOLDER, letter.image)
            if os.path.exists(old_image_path):
                os.remove(old_image_path)

        # 새 파일 저장
        image_path = os.path.join(UPLOAD_FOLDER, image_filename)
        image_file.save(image_path)

        letter.image = image_filename

    db.session.commit()
    flash("The letter has been updated successfully!", "success")
    return redirect(url_for('main.home'))
