from flask import Blueprint, render_template,  send_from_directory, request, current_app
from sqlalchemy import desc, or_

from naszekolorowanki.forms.filter_form import FilterForm
from naszekolorowanki.models.image_models import Image

bp_main = Blueprint('main', __name__, url_prefix='/')


@bp_main.route('/', methods=['GET'])
def home():
    form = FilterForm(request.args, meta={"csrf": False})
    page = request.args.get('page', 1, type=int)
    images = Image.query.filter(or_(Image.username.contains(f'{form.search.data.strip()}'),
                                    Image.description.contains(f'%{form.search.data.strip()}%'))) \
        .filter_by(status=True).order_by(desc(Image.date)).paginate(page=page, per_page=9)
    return render_template('home.html', images=images, form=form)


    # if form.validate_on_submit():
    #     images = Image.query.filter(or_(Image.username.contains(f'{form.search.data.strip()}'),
    #                                     Image.description.contains(f'%{form.search.data.strip()}%'))) \
    #         .filter_by(status=True).order_by(desc(Image.date)).paginate(page=page, per_page=9)
    #     return render_template('home.html', images=images, form=form)

    # images = Image.query.filter_by(status=True).paginate(page=page, per_page=9)
    #
    # return render_template('home.html', form=form, images=images)






@bp_main.route("/uploads/<filename>")
def uploads(filename):
    if filename.rsplit('.', 1)[0][-1] == 'i':
        path = current_app.config["IMAGE_RESIZED"]
    else:
        path = current_app.config["THUMBNAIL"]
    return send_from_directory(path, filename)


@bp_main.route("/cookies")
def cookies():
    return render_template('cookies.html')
