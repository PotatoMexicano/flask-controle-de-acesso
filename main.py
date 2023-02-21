from app import app, db, cache, login_manager
from flask import jsonify, render_template, Response, redirect, url_for
from flask_login import current_user, login_required, logout_user, login_user

@app.after_request
def after_request(response:Response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

@app.route('/')
@login_required
def homepage():
    return jsonify(f'Welcome {current_user.login}.')

if __name__ == '__main__':
    app.run(port=8080, debug=True, load_dotenv=True)