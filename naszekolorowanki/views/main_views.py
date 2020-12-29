import base64

from flask import Blueprint, render_template, flash, redirect, url_for, send_from_directory
from flask_wtf.file import FileRequired
from sqlalchemy import desc

from naszekolorowanki import login_manager, db
from naszekolorowanki.forms.image_forms import ImageForm
from naszekolorowanki.models.image_models import Image
from naszekolorowanki.models.user_models import User
from naszekolorowanki.utils.utils import upload_path, save_image


# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))


bp_main = Blueprint('main', __name__, url_prefix='/')


@bp_main.route('/', methods=['GET'])
def home():
    images = Image.query.filter_by(status=True).order_by(desc(Image.date)).all()
    return render_template('home.html', images=images)


@bp_main.route('/about_us', methods=['GET'])
def about_us():
    return render_template('about_us.html')

#
# @bp_main.route('/add_image', methods=['GET', 'POST'])
# def add_image():
#     form = ImageForm()
#
#     if form.validate_on_submit():
#         filename = save_image(form.image)
#         image = Image(username=form.username.data, image=filename, description=form.description.data)
#
#         db.session.add(image)
#         db.session.commit()
#         flash(f'Twój obrazek został dodany.'
#               f'Po naszej akceptacji zostanie wyświetlony na stronie głównej.', 'info')
#         return redirect(url_for('main.home'))
#
#     return render_template('add_image.html', form=form)


@bp_main.route("/uploads/<filename>")
def uploads(filename):
    return send_from_directory(upload_path, filename)
