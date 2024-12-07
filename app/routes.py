from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Letter
from . import db
import os
from werkzeug.utils import secure_filename

main = Blueprint('main', __name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/')
def index():
    letters = Letter.query.order_by(Letter.date.desc()).all()  # 최신순
    return render_template('index.html', letters=letters)

@main.route('/write', methods=['GET', 'POST'])
def write_letter():
    if request.method == 'POST':
        name = request.form['name']
        message = request.form['message']
        image_file = request.files['image']

        if name and message:
            filename = None
            if image_file and allowed_file(image_file.filename):
                filename = secure_filename(image_file.filename)
                image_file.save(os.path.join(UPLOAD_FOLDER, filename))
            
            new_letter = Letter(name=name, message=message, image=filename)
            db.session.add(new_letter)
            db.session.commit()
            flash('Your letter has been successfully submitted!')
            return redirect(url_for('main.index'))
        else:
            flash('Name and message are required!')

    return render_template('write_letter.html')
