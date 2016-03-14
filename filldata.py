import pandas as pd
from app import db, models

from datetime import datetime
import pytz

import config

filename = 'examsessions.csv'
df = pd.read_csv(filename)

User = models.User
CoPoMap = models.CoPoMap

def get_password(pointfaculty):
    if pointfaculty == 'admin':
        return 'ict123qwe_nbaadmin'
    elif pointfaculty == 'guest':
        return 'guest'
    else:
        return 'ictfaculty'

pointfaculty = 'admin'
pf = User.query.filter(User.nickname == pointfaculty).first()
if pf == None:
    pf = User(nickname = pointfaculty, password = get_password(pointfaculty))
else:
    pf.password = get_password(pointfaculty)
db.session.add(pf)

pointfaculty = 'guest'
pf = User.query.filter(User.nickname == pointfaculty).first()
if pf == None:
    pf = User(nickname = pointfaculty, password = get_password(pointfaculty))
else:
    pf.password = get_password(pointfaculty)
db.session.add(pf)



ndf = len(df)
for i in xrange(ndf):
    entry = df.iloc[i].fillna('')
    pointfaculty = entry.pointfaculty
    pf = User.query.filter(User.nickname == pointfaculty).first()
    if pf == None:
        pf = User(nickname = pointfaculty, password = get_password(pointfaculty))
    else:
        pf.password = get_password(pointfaculty)
    db.session.add(pf)
    
    copo = CoPoMap.query.filter(CoPoMap.coursecode == entry.coursecode).filter(CoPoMap.examsession == str(entry.examsession)).first()
    if copo == None:
        copo = CoPoMap()
    
    copo.uniqueID = entry.coursecode+'_'+str(entry.examsession)
    copo.coursecode = entry.coursecode
    copo.coursename = entry.coursename
    copo.classname = entry.classname
    copo.examsession = str(entry.examsession)
    copo.pointfaculty = entry.pointfaculty
    copo.facultyname_1 = entry.facultyname_1
    copo.facultyname_2 = entry.facultyname_2
    copo.facultyname_3 = entry.facultyname_3
    copo.facultyname_4 = entry.facultyname_4
    copo.description = entry.description
    
    copo.whomodified = 'admin'
    now = datetime.now(pytz.timezone("Asia/Calcutta"))
    copo.whenmodified = now.replace(tzinfo=None)
    
    copo.outcomeKlevel_1 = 0
    copo.outcomeKlevel_2 = 0
    copo.outcomeKlevel_3 = 0
    copo.outcomeKlevel_4 = 0
    copo.outcomeKlevel_5 = 0
    copo.outcomeKlevel_6 = 0
    
    copo.copocorr = {}
    for i in xrange(config.ncourseoutcomes):
        copo.copocorr[i] = []
        for j in xrange(config.nprogramoutcomes):
            inp = 'N'
            copo.copocorr[i] += [inp]
    
    copo.coqcorr = {}
    for i in xrange(config.nquestions):
        copo.coqcorr[i] = {}
        for j in xrange(config.ncourseoutcomes):
            copo.coqcorr[i][j] = '0'
        copo.coqcorr[i]["marksassigned"] = '0'
        copo.coqcorr[i]["targetmarks"] = '0'

    copo.bool_done = 0    
    
    db.session.add(copo)
    
    db.session.commit()
    