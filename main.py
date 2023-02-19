from app import app, db, cache
from flask import jsonify, render_template, Response, redirect, url_for
# from flask_login import current_user, login_required, logout_user, login_user

@app.after_request
def after_request(response:Response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

# @login_manager.unauthorized_handler
# def unauthorized():
#     return redirect(url_for('login'))

@app.route('/')
def list_routes():
    return jsonify('Welcome to homepage')

if __name__ == '__main__':
    app.run(port=8080, debug=False, load_dotenv=True)