from flask import Flask,request, session, redirect, url_for, render_template
from flask_paginate import Pagination ,get_page_args
from db_datas import create_new_account, check_account, account_login, get_default_keywords, update_default, upload_keywords_and_groups, keywords, keywords_and_groups, group_names, delete_group,delete_keyword, upload_save_bookmark, saved_bookmarks
import re
from youtube_data import youtube_video_data

app = Flask(__name__)

app.secret_key = 'super-secret-key'

def get_data(lst,offset=0, per_page=10):
    return lst[offset: offset + per_page]
users = list(range(200))
 

@app.route('/login', methods=["GET", "POST"])
def login():
    msg=''
    if request.method == 'POST' and 'username' in request.form:
        username = request.form['username'].lower()
        account=check_account(username)
        if account:
            session['username'] = account[1]
            return redirect(url_for('login2'))
        else:
            msg="Invalid Username"
    return render_template("login.html", msg=msg)

@app.route('/AddSection', methods=["GET", "POST"])
def login2():
    msg=''
    if request.method == 'POST' and 'password' in request.form:
        password = request.form['password']
        username=session['username']
        account=account_login(username, password)
        if account:
            session['loggedin'] = True
            session['userid']=account[0]
            return redirect(url_for('home'))
        else:
            msg="Invalid Password"
    return render_template("login2.html", msg=msg)

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirmpassword']
        account = check_account(username)
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password:
            msg = 'Please fill out the form!'
        elif password != confirm_password:
            msg = "Password doesn't match!"
        else:
            create_new_account(username,password)  
            msg = 'You have successfully registered!'
    return render_template('register.html', msg=msg)


@app.route('/feed_builder', methods=["GET","POST"])
def addGroup():
    if 'loggedin' in session and request.method == 'POST':
        group_name=request.form['groupname']
        kwords = request.form.getlist('kword')
        for kword in kwords:
            if len(kword) != 0 and len(group_name) != 0:
                upload_keywords_and_groups(session['userid'], group_name, kword)
    return render_template('AddGroup.html')

@app.route('/feed_list', methods=["GET","POST"])
def groupList():
    if 'loggedin' in session and request.method == 'POST':
        if request.method == 'POST' and request.form.get('kword')!= None:
            r = request.form['kword']
            r = r.split(',')
            session['group'] = r[0]
            session['keyword']=r[1]
            return redirect(url_for('home'))
        if request.method == 'POST' and request.form.get('deleteKeyword')!=None:
            lst=request.form['deleteKeyword'].split(',')
            group_name=lst[0]
            keyword=lst[1]
            if session.get('keyword')==keyword:
                session.pop('keyword',None)
                session.pop('group',None)
            delete_keyword(session['userid'],group_name,keyword)
        if request.method == 'POST' and request.form.get('deleteGroup')!=None:
            group_name=request.form['deleteGroup']
            if session.get('group') == group_name:
                session.pop('keyword',None)
                session.pop('group',None)
            delete_group(session['userid'],group_name)
        group=group_names(session['userid'])
        g=keywords_and_groups(session['userid'])
        return render_template('listGroup.html' ,groups=group,g=g)
    if 'loggedin' in session:
        user_id=session['userid']
        if keywords_and_groups(user_id)==():
            username=session['username']
            return render_template('index2.html' ,username=username)
        else:
            group=group_names(session['userid'])
            g=keywords_and_groups(session['userid'])
            return render_template('listGroup.html' ,groups=group,g=g)
    else:
        return redirect(url_for('login'))
    
@app.route('/settings', methods=["GET", "POST"])
def setting():
    if 'loggedin' in session and request.method == 'POST':
        req=request.form['defaultUpdate'].split(',')
        group_name=req[0]
        kword=req[1]
        session['keyword']=kword
        session['group']=group_name
        update_default(session['userid'], group_name, kword)
    if 'loggedin' in session:
        user_id=session['userid']
        if keywords_and_groups(user_id)==():
            username=session['username']
            return render_template('index2.html' ,username=username)
        else:
            group=group_names(session['userid'])
            g=keywords_and_groups(session['userid'])
            default_data = get_default_keywords(userid=session['userid'])
            primary_keyword=default_data[0]
            primary_group=default_data[1]
            bk=saved_bookmarks(user_id)
            title = []
            url = []
            for i in bk:
                title.append(i[0])
                url.append(i[1])
            return render_template('setting-2.html' ,groups=group,g=g, primary_keyword=primary_keyword, primary_group=primary_group, title=title, url=url)
        
@app.route('/', methods=["GET","POST"])
def home():
    if 'loggedin' in session:
        user_id=session['userid']
        if keywords_and_groups(user_id)==():
            username=session['username']
            return render_template('index2.html' ,username=username)
        elif session.get('keyword')!=None and request.method == "POST" and request.form.get('q')==None:
            youtube_data=youtube_video_data(session['keyword'])
        elif request.form.get('q')!=None and request.method == "POST":
            session['keyword']=request.form['q']
        elif session.get('keyword')==None and request.form.get('q')==None:
            default_data = get_default_keywords(userid=user_id)
            session['keyword']=default_data[0]
            session['group']=default_data[1]     
        if request.method == "POST" and request.form.get("bk")!=None:
            bk = request.form.get("bk")
            bk = bk.split('#%#')
            t = bk[1]
            url = 'https://www.youtube.com/watch?v='+bk[0]
            upload_save_bookmark(session['userid'], t, url)
        youtube_data = youtube_video_data(session['keyword'])
        videoId = youtube_data[0]
        title = youtube_data[1]
        time = youtube_data[2]
        keyword = keywords(session['userid'])
        page, per_page, offset = get_page_args(page_parameter='page',per_page_parameter='per_page')
        total = len(videoId)
        videoIds = get_data(lst=videoId,offset=offset, per_page=per_page)
        titles = get_data(lst=title,offset=offset, per_page=per_page)
        pagination = Pagination(page=page, per_page=10, total=total,css_framework='bootstrap5')
        return render_template('index.html', videoIds=videoIds, titles=titles, time=time, keywords=keyword, primary_keyword=session['keyword'],page=page,per_page=16,pagination=pagination)
    else:
        return redirect(url_for('login'))
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))
if __name__ == '__main__':
    app.run(host='0.0.0.0')