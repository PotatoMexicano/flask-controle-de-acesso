from flask import Blueprint, jsonify, render_template, url_for, request, flash, redirect, session
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, login_manager
from app.models.Models import User

auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth', template_folder='templates')

@login_manager.unauthorized_handler
def unauthorized():
    flash("Necessário login", "danger")
    return redirect(url_for('auth.view_login'))

@auth_blueprint.route('/login')
def view_login():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    return render_template('login.html')

@auth_blueprint.route('/logout')
@login_required
def auth_logout():
    logout_user()
    flash("Usuário deslogado !",'warning')
    return redirect(url_for('auth.view_login'))

@auth_blueprint.route('/otpauth', methods=['GET'])
def view_2FA():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    return render_template('2FA.html', data=session.get('TOTP'))

@auth_blueprint.route('/otpauth', methods=['POST'])
def auth_2FA():
    if request.method == 'POST':

        otp = request.form.get('OTP')

        user = User.authUser(username= session.get('username'), password=session.get('password'))

        if user.verify_totp(otp):

            user = User.authUser(session.get('username'), session.get('password'))
            login_user(user)
            user.update_last_login()
            return redirect(url_for('homepage'))

        flash("Ocorreu um erro ao logar","danger")
        return redirect(url_for('auth.auth_2FA'))

@auth_blueprint.route('/2fa')
def register_2FA():
    current_user.create_totp()
    return redirect(url_for('auth.auth_logout'))

@auth_blueprint.route('/login', methods=['POST'])
def auth_login():
    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember')

        if remember == 'on': remember = True
        else: remember = False

        response = User.checkExist(login=username, password=password)

        if response:
            if response.secret_2FA:
                session['TOTP'] = response.view_totp()
                print("2FA is enabled")
                return redirect(url_for('auth.view_2FA'))

            user = User.authUser(username, password)
            login_user(user)
            user.update_last_login()
            return redirect(url_for('homepage'))

        print("2FA disabled")
        return redirect(url_for('auth.view_login'))

    return redirect(url_for('auth.view_login'))
