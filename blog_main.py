from re import L
from flask import Flask, jsonify, request, render_template, make_response, session
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_cors import CORS
import os
from blog_view import blog
from blog_control.user_mgmt import User
from blog_control.session_mgmt import BlogSession

app = Flask(__name__, static_url_path='/static')
CORS(app)
app.secret_key = 'ab_test'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = 'strong'

app.register_blueprint(blog.blog_ab_test, url_prefix='/blog')

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    return make_response(jsonify(success=False), 401)

# log를 따기 위해 session이 들어오면 ip 주소를 추가해준다
@app.before_request
def beforeRequest():
    if 'client_id' not in session:
        session['client_id'] = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

if __name__ == '__main__':
    app.run(host='localhost', port='8080', debug=True)


