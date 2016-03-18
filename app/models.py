from app import db
import config
import copy

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(80), index=True, unique=True)
    password = db.Column(db.String(120))
    
    @property
    def is_authenticated(self):
        return True
        
    @property
    def is_active(self):
        return True
        
    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        try:
            return unicode(self.id) #python2
        except NameError:
            return str(self.id) #python3
    
    def __repr__(self):
        return '<User %r>'%(self.nickname)

class CoPoMap(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    uniqueID = db.Column(db.String(80), index = True, unique=True)
    coursecode = db.Column(db.String(64), index=True)
    coursename = db.Column(db.String(120), index=True)
    facultyname_1 = db.Column(db.String(64), index=True)
    facultyname_2 = db.Column(db.String(64), index=True)
    facultyname_3 = db.Column(db.String(64), index=True)
    facultyname_4 = db.Column(db.String(64), index=True)
    classname = db.Column(db.String(64), index = True)
    examsession = db.Column(db.String(10), index=True)
    
    pointfaculty = db.Column(db.String(64), index=True)
    
    whenmodified = db.Column(db.DateTime)
    whomodified  = db.Column(db.String(64))
    
    description = db.Column(db.String(300))
        
    courseoutcome_1 = db.Column(db.String(300))
    courseoutcome_2 = db.Column(db.String(300))
    courseoutcome_3 = db.Column(db.String(300))
    courseoutcome_4 = db.Column(db.String(300))
    courseoutcome_5 = db.Column(db.String(300))
    courseoutcome_6 = db.Column(db.String(300))
    
    outcomeKlevel_1 = db.Column(db.String(10))
    outcomeKlevel_2 = db.Column(db.String(10))
    outcomeKlevel_3 = db.Column(db.String(10))
    outcomeKlevel_4 = db.Column(db.String(10))
    outcomeKlevel_5 = db.Column(db.String(10))
    outcomeKlevel_6 = db.Column(db.String(10))
    
    copocorr = db.Column(db.PickleType) #Course Outcome Program Outcome Correlation Matrix
    coqcorr  = db.Column(db.PickleType) #Course Outcome Question Correlation Matrix
    
    bool_done = db.Column(db.Integer)
    bool_uploaded = db.Column(db.Integer)
    
    #marks = db.Column(db.PickleType)
    def __repr__(self):
        return '<Course %s Session %s>'%(self.coursecode, self.examsession) 
    
    def copy_data(self, copo):
        self.courseoutcome_1 = copy.deepcopy(copo.courseoutcome_1) 
        self.courseoutcome_2 = copy.deepcopy(copo.courseoutcome_2)
        self.courseoutcome_3 = copy.deepcopy(copo.courseoutcome_3)        
        self.courseoutcome_4 = copy.deepcopy(copo.courseoutcome_4)
        self.courseoutcome_5 = copy.deepcopy(copo.courseoutcome_5)
        self.courseoutcome_6 = copy.deepcopy(copo.courseoutcome_6)
        
        self.outcomeKlevel_1 = copy.deepcopy(copo.outcomeKlevel_1)
        self.outcomeKlevel_2 = copy.deepcopy(copo.outcomeKlevel_2)
        self.outcomeKlevel_3 = copy.deepcopy(copo.outcomeKlevel_3)
        self.outcomeKlevel_4 = copy.deepcopy(copo.outcomeKlevel_4)
        self.outcomeKlevel_5 = copy.deepcopy(copo.outcomeKlevel_5)
        self.outcomeKlevel_6 = copy.deepcopy(copo.outcomeKlevel_6)
        
        self.copocorr = copy.deepcopy(copo.copocorr)
        
        self.bool_done = 0
        self.bool_uploaded = 0