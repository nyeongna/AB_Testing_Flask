import pymongo


mongo_conn = pymongo.MongoClient('mongodb://%s' % ('localhost'))

def conn_mongodb():
    global mongo_conn
    try:
        mongo_conn.admin.command('ismaster')
        blog_ab = mongo_conn.blog_session_db.blog_ab
    except:
        mongo_conn = pymongo.MongoClient('mongodb://%s' % ('localhost'))
        mongo_conn.admin.command('ismaster')
        blog_ab = mongo_conn.blog_session_db.blog_ab

    return blog_ab