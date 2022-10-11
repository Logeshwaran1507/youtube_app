import hashlib
import pymysql

dataBase=pymysql.connect(
    host="mysql",
    user="root",
    passwd="password",
    port=3306,
    database="youtube"
)
cursor=dataBase.cursor()

def create_new_account(username, password):
    password_id=(hashlib.md5(password.encode())).hexdigest()
    cursor.execute('INSERT INTO user(username,password) VALUES (%s, %s)', (username, password_id))
    dataBase.commit()
    msg='Account created Sucessfully'
    return msg

def check_account(username):
    cursor.execute('SELECT * FROM user WHERE username = %s', (username))
    account = cursor.fetchone()
    return account

def account_login(username, password):
    password_id=(hashlib.md5(password.encode())).hexdigest()
    cursor.execute('SELECT * FROM user WHERE username = %s AND password = %s', (username, password_id))
    account = cursor.fetchone()
    return account

def update_default(userid, group_name, keyword):
    cursor.execute('SELECT * FROM default_values WHERE userId = %s', (userid))
    data = cursor.fetchall()
    if data == ():
        cursor.execute('INSERT INTO default_values (userId, group_name, keyword) VALUES (%s, %s, %s)', (userid, group_name, keyword))
        dataBase.commit()
    else:
        cursor.execute('UPDATE default_values SET group_name = %s, keyword = %s WHERE userId=%s', (group_name, keyword, userid))
        dataBase.commit()
    msg="You have successfully updated the default Group and Keyword"
    return msg

def keywords_and_groups(userid):
    cursor.execute('SELECT group_name,keyword FROM groups_keywords WHERE user_id = %s ORDER BY group_name, keyword', (userid))
    data = cursor.fetchall()
    return data
    
def get_default_keywords(userid):
    cursor.execute('SELECT groups_keywords.keyword,groups_keywords.group_name FROM youtube.groups_keywords join default_values on default_values.userId=groups_keywords.user_id and default_values.group_name=groups_keywords.group_name and default_values.keyword=groups_keywords.keyword WHERE userId = %s', (userid))
    default_kw_grp=cursor.fetchone()
    if default_kw_grp==None:
        kw_grps_data = keywords_and_groups(userid)
        if kw_grps_data != ():
            data=kw_grps_data[0]
            update_default(userid, data[0], data[1])
            cursor.execute('SELECT groups_keywords.keyword,groups_keywords.group_name FROM youtube.groups_keywords join default_values on default_values.userId=groups_keywords.user_id and default_values.group_name=groups_keywords.group_name and default_values.keyword=groups_keywords.keyword WHERE userId = %s', (userid))
            default_kw_grp=cursor.fetchone()
    return default_kw_grp

def upload_keywords_and_groups(userid, group_name, keyword):
    cursor.execute('INSERT IGNORE INTO groups_keywords(user_id, group_name, keyword) VALUES(%s, %s, %s)', (userid, group_name, keyword))
    dataBase.commit()
            
def keywords(userid):
    cursor.execute('SELECT keyword FROM groups_keywords WHERE user_id = %s ORDER BY keyword', (userid))
    data = cursor.fetchall()
    return data

def group_names(userid):
    cursor.execute('SELECT DISTINCT group_name FROM groups_keywords WHERE user_id = %s ORDER BY group_name', (userid))
    data = cursor.fetchall()
    return data

def group(userid, keyword):
    cursor.execute('SELECT DISTINCT group_name FROM groups_keywords WHERE user_id = %s AND keyword = %s ORDER BY group_name', (userid, keyword))
    data = cursor.fetchall()
    return data

def delete_keyword(userid, group_name, keyword):
    default_data=get_default_keywords(userid)
    if default_data[0] == keyword:
        cursor.execute('DELETE FROM default_values WHERE userId = %s',(userid))
    cursor.execute('DELETE FROM groups_keywords WHERE user_id = %s AND group_name=%s AND keyword = %s',(userid, group_name, keyword))
    dataBase.commit()

def delete_group(userid, group_name):
    default_data=get_default_keywords(userid)
    if default_data[1] == group_name:
        cursor.execute('DELETE FROM default_values WHERE userId = %s',(userid))
    cursor.execute('DELETE FROM groups_keywords WHERE user_id = %s AND group_name=%s',(userid, group_name))
    dataBase.commit()
    
def upload_save_bookmark(user_id, title, url):
    cursor.execute('INSERT IGNORE INTO bookmark (user_id, title, url) VALUES (%s,%s,%s)',(user_id, title, url))
    dataBase.commit()
    
def saved_bookmarks(user_id):
    cursor.execute('SELECT title,url FROM bookmark WHERE user_id = %s', (user_id))
    bookmarks = cursor.fetchall()
    return bookmarks