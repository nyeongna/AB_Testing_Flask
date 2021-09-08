from flask import Flask, Blueprint, request, redirect, jsonify, session
from flask.helpers import make_response
from flask.templating import render_template
from blog_control.user_mgmt import User
from blog_control.session_mgmt import BlogSession
from flask_login import login_user, current_user, logout_user

blog_ab_test = Blueprint('blog', __name__)


@blog_ab_test.route('/set_email', methods=['GET', 'POST'])
def set_email():
    if request.method == 'GET':
        return f"<h1> RECEIVED GET: {request.args['user_email']} </h1>"
    elif request.method == 'POST':
        # User.create 호출해서 'user_email'을 갖는 User 객체를 리턴받는다.
          # 'user_email'이 이미 존재한다면 db에서 그대로 읽어올테고, 없다면 mysql에 입력하고 User 객체를 리턴할 것이다.
        print(request.form['user_email'], request.form['blog_id'])
        user = User.create(request.form['user_email'], request.form['blog_id'])
        # flask_login의 login_user 함수를 통해 flask 내부에 위에서 만들어진 User 객체를 등록(로그인)시킨다
        login_user(user)
        return redirect('/blog/main')
    
@blog_ab_test.route('/logout')
def logout():
    # 먼저 mysql db에서 삭제하고자 하는 user_id를 없앤다
    User.delete(current_user.id)
    # logout_user() 호출하면 서버에서 로그아웃 기능을 실행하고 해당 User 객체의 Session(쿠키) 기록을 삭제함
    logout_user()
    return redirect('/blog/main')
    
# login 유저가 들어오면 첫번째 if문
# guest 유저가 들어오면 두번째 else문
@blog_ab_test.route('/main')
def main():
    if current_user.is_authenticated:
        webPage = BlogSession.get_blog_page(current_user.blog_id)
        BlogSession.save_session_info(session['client_id'], current_user.user_email, webPage)
        return render_template(webPage, user_email=current_user.user_email)
    else:
        webPage = BlogSession.get_blog_page()
        BlogSession.save_session_info(session['client_id'], 'guest', webPage)
        return render_template(webPage)
    