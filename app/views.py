from flask import render_template, flash, redirect, session, url_for, request, g, abort
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from forms import CoPoForm, LoginForm, CoPoCell
from models import User, CoPoMap
from datetime import datetime
import pytz
import config

import os
import pandas as pd
from werkzeug import secure_filename
from flask import send_from_directory
from app import UPLOAD_FOLDER, ALLOWED_EXTENSIONS
    

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
    logout_user()
    return render_template('home.html',
                           title = 'NBA Work Home')

@app.route('/programoutcomes')
def programoutcomes():
    return render_template('programoutcomes.html')

@app.route('/guest')
@app.route('/guest/<examsession>/')
@app.route('/guest/<examsession>/<classname>')
def guest(examsession=False, classname=False):
    g.user=User.query.filter(User.nickname == 'guest').first()
    login_user(g.user)
    nexamsessions = len(config.dict_examsessions)
    get_examsession = config.get_examsession
    if examsession:
        if classname:
            copos = CoPoMap.query.filter(CoPoMap.examsession == examsession).filter(CoPoMap.classname == classname)
            welcometext = "You have choses %s class for %s."%(classname, get_examsession(examsession))
            return render_template('guest.html',
                                   user = user,
                                   copos = copos,
                                   welcometext = welcometext,
                                   examsession = True,
                                   classname = True,
                                   get_examsession = get_examsession)            
        else:
            classlist = ['FYCE','SYCE','TYCE','FNCE','MCHE']
            welcometext = "You have chosen %s.  Please select a class."%(get_examsession(examsession))
            return render_template('guest.html', 
                                   iexamsession = examsession,
                                   examsession = True,
                                   classname = False,
                                   welcometext = welcometext,
                                   classlist = classlist)        
    else:
        welcometext = "Please select one of the following exam sessions."
        return render_template('guest.html', 
                               examsession = False,
                               welcometext = welcometext,
                               nexamsessions = nexamsessions, 
                               get_examsession = get_examsession)

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
    if nickname == 'admin':
        copos = CoPoMap.query.filter(True).order_by(CoPoMap.examsession, CoPoMap.classname, CoPoMap.coursecode)
    else:
        copos = CoPoMap.query.filter(CoPoMap.pointfaculty == nickname).order_by(CoPoMap.examsession, CoPoMap.classname, CoPoMap.coursecode)
    return render_template('user.html', user = user, copos = copos, ncopo = copos.count(), get_examsession = config.get_examsession)       
   
@app.route('/copopreview/<uniqueID>',methods=['GET','POST'])
@login_required
def copopreview(uniqueID):
    copo = CoPoMap.query.filter(CoPoMap.uniqueID == uniqueID).first()
    if request.method == 'POST': #
        copo.bool_done = 1
        db.session.add(copo)
        db.session.commit()
        return redirect(url_for('user',nickname=g.user.nickname))
    else:
        form = CoPoForm()
        form.get_courseOutcome()
        form.datatoform(copo)
    return render_template('copopreview.html', 
                           user = g.user, 
                           copo = copo, 
                           form = form,
                           courseOutcomeKlevel = form.courseOutcomeKlevel,
                           get_examsession = config.get_examsession,
                           get_Klevel = config.get_Klevel,
                           ncourseoutcomes = config.ncourseoutcomes,
                           nquestions = config.nquestions,
                           nprogramoutcomes = config.nprogramoutcomes)

@app.route('/copoform/<uniqueID>', methods = ['GET','POST'])
@login_required
def copoform(uniqueID):
    copo = CoPoMap.query.filter(CoPoMap.uniqueID == uniqueID).first()
    if request.method == 'POST': #This implies TWO instantiations of CoPoForm as per http://databasefaq.com/index.php/answer/57213/forms-flask-wtforms-fieldlist-how-can-you-populate-a-wtforms-fieldlist-after-the-validate-on-submit-block
        form = CoPoForm()
        form.get_courseOutcome()
        if not form.validate():
            flash(form.errors)
        else:
            copo.bool_done = 0
            copo.whomodified = g.user.nickname
            now = datetime.now(pytz.timezone("Asia/Calcutta"))
            copo.whenmodified = now.replace(tzinfo=None) 
            form.formtodata(copo)
            copo = CoPoMap.query.filter(CoPoMap.uniqueID == uniqueID).first()
            flash("Thank you for taking the time to fill up this form.  Your information is saved.")
            if not validate_and_calculate(copo):
                flash("WARNING! .csv file not uploaded OR Max marks in uploaded file do not tally with max marks in form!  Calculations could be inconsistent. Uploaded file is rejected")
                copo.bool_uploaded = 0
            db.session.add(copo)
            db.session.commit()
                

            return redirect(url_for('copopreview',uniqueID=copo.uniqueID))
    else:
        form = CoPoForm()
        form.get_courseOutcome()
        form.datatoform(copo)
    return render_template('copoform.html',
                           user = g.user, 
                           copo = copo, 
                           form = form,
                           courseOutcomeKlevel = form.courseOutcomeKlevel,
                           get_examsession = config.get_examsession,
                           ncourseoutcomes = config.ncourseoutcomes,
                           nquestions = config.nquestions,
                           nprogramoutcomes = config.nprogramoutcomes)

@app.route('/copy_select/<uniqueID>')
def copy_select(uniqueID):
    user = g.user
    coursecode = uniqueID.split('_')[0]
    copos = CoPoMap.query.filter(CoPoMap.coursecode == coursecode).order_by(CoPoMap.examsession)
    return render_template('copy.html', user = user, uniqueID=uniqueID, copos = copos, ncopo = copos.count(), get_examsession = config.get_examsession)       
    
    
@app.route('/copy_execute/<uniqueID>/<template_uniqueID>')
def copy_execute(uniqueID, template_uniqueID):
    copo = CoPoMap.query.filter(CoPoMap.uniqueID == uniqueID).first()
    template_copo = CoPoMap.query.filter(CoPoMap.uniqueID == template_uniqueID).first()
    
    copo.copy_data(template_copo)
    db.session.add(copo)
    db.session.commit()
    return redirect(url_for('copoform',uniqueID=uniqueID))
    
    
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

listQ = ['Q1','Q2','Q3','Q4','Q5','Q6','Q7','Q8','Q9','Q10','Q11','Q12','Q13','Q14','Q15']
def validate(copo):
    uniqueID = copo.uniqueID
    filename = uniqueID+'.csv'
    filepath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
    if os.path.isfile(filepath):
        df = pd.read_csv(filepath).fillna('0')
        maxx = df.iloc[0]
        bool_marks_tally = True
        for i in xrange(len(listQ)):
            Qi = listQ[i]
            try:
                maxmarks_csv = float(maxx[Qi])
            except ValueError:
                maxmarks_csv = 0.0
            try:
                maxmarks_form = float(copo.coqcorr[i]["marksassigned"])
            except ValueError:
                maxmarks_form = 0.0
            if maxmarks_csv != maxmarks_form:
                bool_marks_tally = False
                break
    else:
        bool_marks_tally = False
    return bool_marks_tally
        
    
def validate_and_calculate(copo):
    try:
        bool_valid = validate(copo)
    except:
        bool_valid = False
    copo.bool_uploaded = 1
    db.session.add(copo)
    db.session.commit()
    return bool_valid
    

@app.route('/upload/<uniqueID>',methods=['GET','POST'])
def upload_file(uniqueID):
    copo = CoPoMap.query.filter(CoPoMap.uniqueID == uniqueID).first()
    form = CoPoForm()
    if request.method == 'POST':
        file = request.files['file']
        file_name = file.filename.split('.')[0]
        if file and allowed_file(file.filename) and file_name == uniqueID:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            return redirect(url_for('copoform',uniqueID=uniqueID))
        else:
            flash("Please upload a file named %s.csv"%(uniqueID))
            return redirect(url_for('upload_file',uniqueID=uniqueID))
    return render_template('upload.html',copo = copo, uniqueID = uniqueID, form=form)
    
@app.route('/showfile/<filename>')
def show_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
    