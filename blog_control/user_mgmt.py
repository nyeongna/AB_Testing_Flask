from db_model.mysql import conn_mysqldb
from flask_login import UserMixin

class User(UserMixin):
    
    def __init__(self, user_id, user_email, blog_id):
        self.id = user_id
        self.user_email = user_email
        self.blog_id = blog_id
    
    def get_id(self):
        return str(self.id)
    
    @staticmethod
    def get(user_id):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "SELECT * FROM user_info WHERE USER_ID = '" + str(user_id) + "'"
        print(sql)
        db_cursor.execute(sql)
        user = db_cursor.fetchone()
        if not user:
            db_cursor.close()
            return None
        else:
            user = User(user_id=user[0], user_email=user[1], blog_id=user[2])
            return user
    
    @staticmethod
    def find(user_email):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "SELECT * FROM user_info WHERE USER_EMAIL = '" + str(user_email) + "'"
        print(sql)
        db_cursor.execute(sql)
        user = db_cursor.fetchone()
        if not user:
            db_cursor.close()
            return None
        else:
            user = User(user_id=user[0], user_email=user[1], blog_id=user[2])
            return user

    @staticmethod
    def create(user_email, blog_id):
        user = User.find(user_email)
        if not user:
            mysql_db = conn_mysqldb()
            db_cursor = mysql_db.cursor()
            db_cursor.execute("INSERT INTO user_info (USER_EMAIL, BLOG_ID) VALUES (%s, %s)", (str(user_email), str(blog_id)) )
            mysql_db.commit()
            return User.find(user_email)
        else:
            return user
    
    @staticmethod
    def delete(user_id):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = f"DELETE FROM user_info WHERE USER_ID = {int(user_id)}"
        deleted = db_cursor.execute(sql)
        mysql_db.commit()
        return deleted

            