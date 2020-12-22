import os

from flask import Blueprint, flash, redirect, url_for, render_template, send_from_directory
from flask_login import login_required

from naszekolorowanki import db, login_manager
from naszekolorowanki.forms.image_forms import ImageForm, EditImageForm
from naszekolorowanki.models.image_models import Image
from naszekolorowanki.models.user_models import User
from naszekolorowanki.utils.utils import save_image, upload_path


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


bp_image = Blueprint('image', __name__, url_prefix='/image')


@bp_image.route('/list', methods=['GET'])
@login_required
def list():
    images = Image.query.filter_by(status=False).all()
    return render_template('list.html', images=images)


@bp_image.route('/add_image', methods=['GET', 'POST'])
def add_image():
    form = ImageForm()

    if form.validate_on_submit():
        filename = save_image(form.image)
        image = Image(username=form.username.data, image=filename, description=form.description.data)

        db.session.add(image)
        db.session.commit()
        flash(f'Twój obrazek został dodany.'
              f'Po naszej akceptacji zostanie wyświetlony na stronie głównej.', 'info')
        return redirect(url_for('main.home'))

    return render_template('add_image.html', form=form)


@bp_image.route("/uploads/<filename>")
def uploads(filename):
    return send_from_directory(upload_path, filename)


@bp_image.route('/edit_image/<int:image_id>', methods=['GET', 'POST'])
@login_required
def edit_image(image_id):
    image = Image.query.get_or_404(image_id)
    form = EditImageForm(obj=image)
    print(image.image)

    if form.validate_on_submit():
        form.populate_obj(image)
        db.session.commit()
        return redirect(url_for('image.list'))
    return render_template('edit_image.html', form=form, image=image)


@bp_image.route('/delete_image/<int:image_id>', methods=['GET'])
def delete_image(image_id):
    image = Image.query.get_or_404(image_id)
    print(image.image)

    file = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'uploaded_pictures', image.image)
    os.remove(file)
    db.session.delete(image)
    db.session.commit()
    flash('Usunięto obrazek.')
    return redirect(url_for('image.list'))

