from flask import render_template, flash, redirect, session, url_for, request, g, abort
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from forms import CoPoForm, LoginForm, CoPoCell, CoPoRow
from models import User, CoPoMap
from datetime import datetime
import pytz
import config

    
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user
    
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        g.user = User.query.filter(User.nickname == form.username.data).first()
        login_user(g.user)
        flash('You are now logged in')
        return redirect(url_for('index'))
    return render_template('login.html', title = 'Login', form = form)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html',
                           title = 'NBA Work Home')

@app.route('/index')
@login_required
def index():
    return redirect(url_for('user',nickname = g.user.nickname))

@app.route('/user/<nickname>')
@login_required
def user(nickname):
    user = User.query.filter(User.nickname == nickname).first()
    if user == None:
        flash('User %s not found.  Please write to your administrator'%nickname)
        return redirect(url_for('home'))
    copos = CoPoMap.query.filter(CoPoMap.pointfaculty == nickname)
    return render_template('user.html', user = user, copos = copos, get_examsession = config.get_examsession)       

def init_form(form, copo):
    for i in xrange(config.ncourseoutcomes):
        row = CoPoRow()
        for j in xrange(config.nprogramoutcomes):
            cell = CoPoCell()
            cell.copocorr = copo.copocorr[i][j]
            row.coporow.append_entry(cell)
        form.copotable.append_entry(row)

def datatoform(form, copo):
    form.outcomeKlevel_1.default = copo.outcomeKlevel_1
    form.outcomeKlevel_2.default = copo.outcomeKlevel_2
    form.outcomeKlevel_3.default = copo.outcomeKlevel_3
    form.outcomeKlevel_4.default = copo.outcomeKlevel_4
    form.outcomeKlevel_5.default = copo.outcomeKlevel_5
    form.outcomeKlevel_6.default = copo.outcomeKlevel_6
    form.process()
    
    form.courseoutcome_1.data = copo.courseoutcome_1
    form.courseoutcome_2.data = copo.courseoutcome_2
    form.courseoutcome_3.data = copo.courseoutcome_3
    form.courseoutcome_4.data = copo.courseoutcome_4
    form.courseoutcome_5.data = copo.courseoutcome_5
    form.courseoutcome_6.data = copo.courseoutcome_6    

def formtodata(form, copo):
    copo.courseoutcome_1 = form.courseoutcome_1.data 
    copo.outcomeKlevel_1 = form.outcomeKlevel_1.data
    copo.courseoutcome_2 = form.courseoutcome_2.data 
    copo.outcomeKlevel_2 = form.outcomeKlevel_2.data
    copo.courseoutcome_3 = form.courseoutcome_3.data 
    copo.outcomeKlevel_3 = form.outcomeKlevel_3.data
    copo.courseoutcome_4 = form.courseoutcome_4.data 
    copo.outcomeKlevel_4 = form.outcomeKlevel_4.data
    copo.courseoutcome_5 = form.courseoutcome_5.data 
    copo.outcomeKlevel_5 = form.outcomeKlevel_5.data
    copo.courseoutcome_6 = form.courseoutcome_6.data 
    copo.outcomeKlevel_6 = form.outcomeKlevel_6.data
    
    i = 0
    for row in form.copotable.entries:
        j = 0
        for cell in row.coporow.entries:
            copo.copocorr[i][j] = cell.copocorr.data
            j += 1
        i += 1

@app.route('/copoform/<uniqueID>', methods = ['GET','POST'])
@login_required
def copoform(uniqueID):
    copo = CoPoMap.query.filter(CoPoMap.uniqueID == uniqueID).first()
    form = CoPoForm()
    courseOutcomeKlevel = [(1, form.courseoutcome_1, form.outcomeKlevel_1),
                           (2, form.courseoutcome_2, form.outcomeKlevel_2),
                           (3, form.courseoutcome_3, form.outcomeKlevel_3),
                           (4, form.courseoutcome_4, form.outcomeKlevel_4),
                           (5, form.courseoutcome_5, form.outcomeKlevel_5),
                           (6, form.courseoutcome_6, form.outcomeKlevel_6)]
    if form.validate_on_submit():
        copo.whomodified = g.user.nickname
        now = datetime.now(pytz.timezone("Asia/Calcutta"))
        copo.whenmodified = now.replace(tzinfo=None) 
        formtodata(form, copo)
        db.session.add(copo)
        db.session.commit()

        flash("Thank you for taking the time to fill up this form.  Your information is saved.")
        return redirect(url_for('user',nickname=g.user.nickname))
    else: 
        datatoform(form, copo)
    return render_template('copoform.html', 
                           user = g.user, 
                           copo = copo, 
                           form = form,
                           courseOutcomeKlevel = courseOutcomeKlevel,
                           get_examsession = config.get_examsession,
                           ncourseoutcomes = config.ncourseoutcomes,
                           nprogramoutcomes = config.nprogramoutcomes)