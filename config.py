WTF_CSRF_ENABLED = True
SECRET_KEY = 'MyNameIsAnthonyGonsalves'

import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(basedir,'nbacopo.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USERNAME = None
MAIL_PASSWORD = None
ADMINS = ['you@example.com']


ncourseoutcomes = 6
nprogramoutcomes = 14
nquestions = 15

dict_examsessions = {0:'2012-2013 Semester I  (Nov-Dec)',
                     1:'2012-2013 Semester II (Apr-May)',
                     2:'2013-2014 Semester I  (Nov-Dec)',
                     3:'2013-2014 Semester II (Apr-May)',
                     4:'2014-2015 Semester I  (Nov-Dec)',
                     5:'2014-2015 Semester II (Apr-May)',
                     6:'2015-2016 Semester I  (Nov-Dec)'}

dict_Klevels = {0:'K1',
                1:'K2',
                2:'K3',
                3:'K4',
                4:'K5',
                5:'K6'}
                
dict_class = {0: 'FYCE', 
              1: 'SYCE',
              2: 'TYCE',
              3: 'FNCE',
              4: 'MCHE'}

def get_examsession(eid):
    return dict_examsessions[int(eid)]

def get_Klevel(kid):
    return dict_Klevels[int(kid)]

