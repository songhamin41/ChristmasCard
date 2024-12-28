from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import db, Letter
from werkzeug.utils import secure_filename
import os

main = Blueprint('main', __name__)

# 홈 페이지
@main.route('/')
def home():
    letters = Letter.query.all()
    return render_template('index.html', letters=letters)

# 편지 작성
@main.route('/write_letter', methods=['GET', 'POST'])
@login_required
def write_letter():
    if request.method == 'POST':
        name = request.form['name']
        message = request.form['message']
        image = None

        if 'image' in request.files:
            image_file = request.files['image']
            if image_file.filename != '':
                filename = secure_filename(image_file.filename)
                image_path = os.path.join('app/static/uploads', filename)
                image_file.save(image_path)
                image = filename

        new_letter = Letter(name=name, message=message, image=image, user_id=current_user.id)
        db.session.add(new_letter)
        db.session.commit()
        flash("편지가 작성되었습니다!", "success")
        return redirect(url_for('main.home'))

    return render_template('write_letter.html')

# 편지 수정
@main.route('/edit_letter/<int:letter_id>', methods=['GET', 'POST'])
@login_required
def edit_letter(letter_id):
    letter = Letter.query.get_or_404(letter_id)

    if letter.user_id != current_user.id:
        flash("자신의 편지만 수정할 수 있습니다.", "danger")
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        letter.name = request.form['name']
        letter.message = request.form['message']
        db.session.commit()
        flash("편지가 수정되었습니다!", "success")
        return redirect(url_for('main.home'))

    return render_template('edit_letter.html', letter=letter)

# 편지 삭제
@main.route('/delete_letter/<int:letter_id>', methods=['POST'])
@login_required
def delete_letter(letter_id):
    letter = Letter.query.get_or_404(letter_id)

    if letter.user_id != current_user.id:
        flash("자신의 편지만 삭제할 수 있습니다.", "danger")
        return redirect(url_for('main.home'))

    db.session.delete(letter)
    db.session.commit()
    flash("편지가 삭제되었습니다.", "success")
    return redirect(url_for('main.home'))
