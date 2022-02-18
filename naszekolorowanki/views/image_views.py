import os
import time

from flask import Blueprint, flash, redirect, url_for, render_template, send_from_directory, current_app
from flask_login import login_required
from sqlalchemy import desc

from naszekolorowanki import db, login_manager
from naszekolorowanki.forms.image_forms import ImageForm, EditImageForm
from naszekolorowanki.models.image_models import Image
from naszekolorowanki.models.user_models import User
from naszekolorowanki.utils.save_resize import save_resize_image


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


bp_image = Blueprint('image', __name__, url_prefix='/image')


@bp_image.route('/list_to_accept', methods=['GET'])
@login_required
def list_to_accept():
    images = Image.query.filter_by(status=False).order_by(desc(Image.date)).all()
    return render_template('list.html', images=images, title='Obrazki do zaakceptowania',
                           fn_name="list_to_accept")


@bp_image.route('/list_accepted', methods=['GET'])
@login_required
def list_accepted():
    images = Image.query.filter_by(status=True).order_by(desc(Image.date)).all()
    return render_template('list.html', images=images, title='Zaakceptowane obrazki',
                           fn_name="list_accepted")


@bp_image.route('/add_image', methods=['GET', 'POST'])
def add_image():
    form = ImageForm()

    if form.validate_on_submit():
        filename = save_resize_image(form.image, form.username.data)
        image = Image(username=form.username.data, thumbnail=filename[0], image=filename[1],
                      description=form.description.data)
        db.session.add(image)
        db.session.commit()
        flash(f'Twój obrazek został dodany. '
              f'Po naszej akceptacji zostanie wyświetlony na stronie głównej.', 'secondary')
        return redirect(url_for('main.home'))

    return render_template('add_image.html', form=form)


@bp_image.route('/edit_image/<int:image_id>/<string:fn_name>/<string:title>', methods=['GET', 'POST'])
@login_required
def edit_image(image_id, fn_name, title):

    image = Image.query.get_or_404(image_id)
    form = EditImageForm(obj=image)
    file = os.path.join(current_app.config['IMAGE_RESIZED'], image.image)
    img_size = os.path.getsize(file) / 1024 / 1024
    img_created = time.strftime("%d.%m.%Y godz.%H:%m", time.localtime(os.path.getctime(file)))

    if form.validate_on_submit():
        form.populate_obj(image)
        db.session.commit()
        return redirect(url_for(f'image.{fn_name}'))
    return render_template('edit_image.html', form=form, image=image, fn_name=fn_name,
                           title=title.lower(), img_size=round(img_size, 3), img_created=img_created)


@bp_image.route('/delete_image/<int:image_id>/<string:fn_name>', methods=['GET'])
@login_required
def delete_image(image_id, fn_name):
    image = Image.query.get_or_404(image_id)
    paths = [os.path.join(current_app.config["THUMBNAIL"], image.thumbnail),
             os.path.join(current_app.config["IMAGE_RESIZED"], image.image)]
    for path in paths:
        os.remove(path)
    db.session.delete(image)
    db.session.commit()
    flash('Usunięto obrazek.', 'danger')
    return redirect(url_for(f'image.{fn_name}'))


@bp_image.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(current_app.config["IMAGE_RESIZED"])
    return send_from_directory(directory=uploads, filename=filename)
