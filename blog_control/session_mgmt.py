from db_model.mongodb import conn_mongodb
from datetime import datetime

class BlogSession():
    blog_page = {'A': 'blog_A.html', 'B': 'blog_B.html'}
    session_flag = 0

    @staticmethod
    def save_session_info(session_ip, user_email, webpage_name):
        now = datetime.now()
        now_time = now.strftime('%d-%m-%Y %H:%M:%S')
        mongo_db = conn_mongodb()
        mongo_db.insert_one({
            'session_ip': str(session_ip),
            'user_email': str(user_email),
            'page': str(webpage_name),
            'access_time': now_time})

    @staticmethod
    def get_blog_page(blog_id=None):
        if not blog_id:
            if BlogSession.session_flag == 0:
                BlogSession.session_flag=1
                return BlogSession.blog_page['A']
            else:
                BlogSession.session_flag=0
                return BlogSession.blog_page['B']
        else:
            return BlogSession.blog_page[blog_id]

        