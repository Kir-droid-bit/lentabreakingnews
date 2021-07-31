from datetime import datetime

from flask import render_template, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

from app import app
from database import db, Users, Comment


@app.route('/')
def start():
    return render_template('base.html'), 200


@app.route('/registration/', methods=["GET", "POST"])
def registr():
    if request.method == 'POST':
        if len(request.form['login']) < 6 or len(request.form['login']) > 40:
            flash('Неправильный логин !', category='error')
        elif len(request.form['password']) < 8 or len(request.form['password']) > 40:
            flash('Неправильный пароль!', category='error')
        elif request.form['password'] != request.form['password-repeat']:
            flash('Пароли не совпадают!', category='error')
        else:
            flash('Вы успешно зарегистрированы!', category='success')
            login = request.form['login']
            password = request.form['password']
            time = datetime.now()
            article = Users(login=login, password=generate_password_hash(password), time=time)
            db.session.add(article)
            db.session.commit()
    return render_template("reg.html"), 200


@app.route('/authorization/', methods=["GET", "POST"])
def avto():
    if 'login' in session:
        return "Авторизация не нужна, пользователь авторизован."
    elif request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        get_log = Users.query.filter_by(login=login).first()
        if get_log is None:
            flash('Пользователь не найден!', category='error')
        elif check_password_hash(get_log.password, password) and get_log:
            flash('Пользователь авторизован!', category='success')
            session['login'] = login
        else:
            flash('Неправильный пароль!', category='error')
    return render_template('avto.html', flash=flash), 200


@app.route('/edit-profile/', methods=["GET", "POST"])
def profile():
    if 'login' in session:
        current_login = session['login']
        update = Users.query.filter_by(login=current_login)
        if request.method == 'POST':
            new_login = request.form['login2']
            if len(new_login) < 8:
                flash('Слишком короткий логин!', category='error')
            update = Users.query.filter_by(login=current_login).update({'login': new_login})
            session['login'] = new_login
            db.session.commit()
    else:
        return "Вы не авторизированы!"
    return render_template('example.html', update=update)


@app.route('/logout/')
def logout():
    if 'login' in session:
        session.pop('login', '')
        return "Вы вышли из своей учётной записи!"
    elif 'login' not in session:
        return "Вы не авторизированны!"


@app.route('/news/post/<int:id>', methods=["GET", "POST"])
def twitte(id):
    comment = ""
    req = Comment.query.filter_by(post_id=id).all()
    if request.method == 'POST':
        if 'login' not in session:
            flash('Для начала авторизируйтесь!', category=error)
        elif 'login' in session:
            if len(request.form['comment']) < 8:
                flash('Слишком короткий комментарий!', category=error)
            else:
                comment = request.form['comment']
                session_user = Users.query.filter_by(login=session['login']).first()
                child_table = Comment(comment=comment, login=session['login'], post_id=id, owner=session_user)
                db.session.add(child_table)
                db.session.commit()
    return render_template(f'page{id}.html', flash=flash, session=session, comment=comment, id=id,req=req), 200


@app.errorhandler(404)
def error(error):
    return render_template('error404.html'), 200
