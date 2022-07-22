from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User

@app.route('/')
def dashboard():
    session.clear()
    users = User.get_all()
    return render_template('dashboard.html',users=users)

@app.route('/new_user_form/')
def new_user_form():
    # users = User.get_all()
    return render_template('new_user_form.html')

@app.route('/save_user/',methods=['POST'])
def save_user():
    if not User.validate(request.form):
        session['first_name'] = request.form['first_name']
        session['last_name'] = request.form['last_name']
        session['email'] = request.form['email']
        return redirect('/new_user_form/')
    User.save(request.form)
    session.clear()		
    return redirect('/')

# @app.route('/')
# def xxxx():
#     pass

