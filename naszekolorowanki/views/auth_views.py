from os import abort

from flask import Blueprint, request, url_for, render_template, flash
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import redirect

from naszekolorowanki import db
from naszekolorowanki.forms.user_forms import LoginForm, SignUpForm, ChangePasswordForm, DeleteUserForm
from naszekolorowanki.models.user_models import User

bp_auth = Blueprint('auth', __name__, url_prefix='/auth')


@bp_auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            flash(f'You are logged in!', 'success')
            return redirect(request.args.get('next') or url_for('main.home'))
    return render_template('login.html', form=form)


@bp_auth.route('/signup', methods=['GET', 'POST'])
@login_required
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Hello, please log in!', 'info')
        return redirect(url_for('auth.login'))

    return render_template('signup.html', form=form)


@bp_auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You logged out.", 'warning')
    return redirect(url_for('main.home'))


@bp_auth.route('/user/<username>')
@login_required
def user(username):
    user_db = User.query.filter_by(username=username).first_or_404()
    form = DeleteUserForm()
    return render_template('user.html', user=user_db, form=form)


@bp_auth.route('/edit_user/<username>', methods=['GET', 'POST'])
@login_required
def edit_user(username):
    user_db = User.query.filter_by(username=username).first_or_404()

    if current_user != user_db:
        abort(403)

    form = ChangePasswordForm()

    if form.validate_on_submit():
        user_db.password = form.new_password.data
        db.session.commit()
        flash(f'Your password has been changed.', 'info')
        return redirect(url_for('auth.user', username=username))
    flash('Incorrect password.', 'danger')
    return render_template('edit_user.html', form=form, user=user_db)


@bp_auth.route('/delete_user/<username>', methods=['POST'])
@login_required
def delete_user(username):
    user_db = User.query.filter_by(username=username).first_or_404()

    if current_user != user_db:
        abort(403)

    form = DeleteUserForm()

    if form.validate_on_submit():
        db.session.delete(user_db)
        db.session.commit()
        flash(f'You deleted your account.', 'info')
        return redirect(url_for('main.home'))
    flash('Incorrect password.', 'danger')
    return redirect(url_for('auth.user', username=current_user.username))
