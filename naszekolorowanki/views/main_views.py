import base64

from flask import Blueprint, render_template, flash, redirect, url_for, send_from_directory, request
from flask_wtf.file import FileRequired
from sqlalchemy import desc, or_

from naszekolorowanki import login_manager, db
from naszekolorowanki.forms.filter_form import FilterForm
from naszekolorowanki.forms.image_forms import ImageForm
from naszekolorowanki.models.image_models import Image

from naszekolorowanki.utils.utils import upload_path


# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))


bp_main = Blueprint('main', __name__, url_prefix='/')


@bp_main.route('/', methods=['GET'])
def home():
    filter_form = FilterForm(request.args, meta={"csrf": False})
    page = request.args.get('page', 1, type=int)
    images = Image.query.filter(or_(Image.username.contains(f'{filter_form.search.data.strip()}'),
                                    Image.description.contains(f'%{filter_form.search.data.strip()}%')))\
        .filter_by(status=True).order_by(desc(Image.date)).paginate(page=page, per_page=9)

    return render_template('home.html', images=images, form=filter_form)


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

@bp_main.route("/cookies")
def cookies():
    return render_template('cookies.html')
