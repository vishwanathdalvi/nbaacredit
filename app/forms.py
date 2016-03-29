from wtforms import StringField, SelectField, TextAreaField, PasswordField
from wtforms import FormField, FieldList
from wtforms.validators import DataRequired, Length
from flask.ext.wtf import Form

import config
from app.models import User, CoPoMap

class LoginForm(Form):
    username = StringField('username',validators=[DataRequired()])
    password = PasswordField('password',validators=[DataRequired()])
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
    def validate(self):
        if not Form.validate(self):
            return False
        user = User.query.filter_by(nickname = self.username.data).first()
        if user != None:
            if self.password.data == user.password:
                return True
            else:
                self.password.errors.append("The password is incorrect.  Please enter the correct password.")
                return False
        else:
            self.username.errors.append("Username not found.  Please check with your administrator.")
            return False
                    
 
class CoPoCell(Form):
    copocorr = StringField(validators=[Length(max=10)])

class CoPoRow(Form):
    coporow = FieldList(FormField(CoPoCell))

class CoQCell(Form):
    coqcorr = StringField(validators=[Length(max=10)])

class CoQRow(Form):
    marksassigned = StringField(validators=[Length(max=10)])    
    targetmarks   = StringField(validators=[Length(max=10)])
    coqrow = FieldList(FormField(CoQCell))
    
class CoPoForm(Form):    
    dict_Klevels = config.dict_Klevels
    courseoutcome_1 = TextAreaField('courseoutcome_1', validators=[Length(max=300)])
    courseoutcome_2 = TextAreaField('courseoutcome_2', validators=[Length(max=300)])
    courseoutcome_3 = TextAreaField('courseoutcome_3', validators=[Length(max=300)])
    courseoutcome_4 = TextAreaField('courseoutcome_4', validators=[Length(max=300)])
    courseoutcome_5 = TextAreaField('courseoutcome_5', validators=[Length(max=300)])
    courseoutcome_6 = TextAreaField('courseoutcome_6', validators=[Length(max=300)])
    
    outcomeKlevel_1 = SelectField('Klevel_1', coerce=int, choices=[(key, dict_Klevels[key]) for key in dict_Klevels.keys()])
    outcomeKlevel_2 = SelectField('Klevel_2', coerce=int, choices=[(key, dict_Klevels[key]) for key in dict_Klevels.keys()])
    outcomeKlevel_3 = SelectField('Klevel_3', coerce=int, choices=[(key, dict_Klevels[key]) for key in dict_Klevels.keys()])
    outcomeKlevel_4 = SelectField('Klevel_4', coerce=int, choices=[(key, dict_Klevels[key]) for key in dict_Klevels.keys()])
    outcomeKlevel_5 = SelectField('Klevel_5', coerce=int, choices=[(key, dict_Klevels[key]) for key in dict_Klevels.keys()])
    outcomeKlevel_6 = SelectField('Klevel_6', coerce=int, choices=[(key, dict_Klevels[key]) for key in dict_Klevels.keys()])

    copotable = FieldList(FormField(CoPoRow))
    
    coqtable = FieldList(FormField(CoQRow))
    
    description = TextAreaField('description', validators=[Length(max=300)])

    def __init__(self, *args, **kwargs): #FormID is session_coursecode
        Form.__init__(self, *args, **kwargs)
    def validate(self):
        try:
            if not Form.validate(self):
                return False
            else:
                return True
        except TypeError:
            return True
    def get_courseOutcome(self):
        self.courseOutcomeKlevel = [(1, self.courseoutcome_1, self.outcomeKlevel_1),
                                    (2, self.courseoutcome_2, self.outcomeKlevel_2),
                                    (3, self.courseoutcome_3, self.outcomeKlevel_3),
                                    (4, self.courseoutcome_4, self.outcomeKlevel_4),
                                    (5, self.courseoutcome_5, self.outcomeKlevel_5),
                                    (6, self.courseoutcome_6, self.outcomeKlevel_6)]

    def datatoform(self, copo):
        self.outcomeKlevel_1.default = copo.outcomeKlevel_1
        self.outcomeKlevel_2.default = copo.outcomeKlevel_2
        self.outcomeKlevel_3.default = copo.outcomeKlevel_3
        self.outcomeKlevel_4.default = copo.outcomeKlevel_4
        self.outcomeKlevel_5.default = copo.outcomeKlevel_5
        self.outcomeKlevel_6.default = copo.outcomeKlevel_6
        self.process()
        
        self.courseoutcome_1.data = copo.courseoutcome_1
        self.courseoutcome_2.data = copo.courseoutcome_2
        self.courseoutcome_3.data = copo.courseoutcome_3
        self.courseoutcome_4.data = copo.courseoutcome_4
        self.courseoutcome_5.data = copo.courseoutcome_5
        self.courseoutcome_6.data = copo.courseoutcome_6 
        
        self.description.data = copo.description
        
        #CO-PO Mapping
        for i in xrange(config.ncourseoutcomes):
            row = CoPoRow()
            self.copotable.append_entry(row)
            while len(self.copotable.entries[i].coporow) < config.nprogramoutcomes:
                cell = CoPoCell()
                self.copotable.entries[i].coporow.append_entry(cell)
        
        for i in xrange(config.ncourseoutcomes):
            for j in xrange(config.nprogramoutcomes):
                self.copotable.entries[i].coporow.entries[j].copocorr.data = copo.copocorr[i][j]
        
        #CO-Q mapping
        for i in xrange(config.nquestions):
            row = CoQRow()
            self.coqtable.append_entry(row)
            while len(self.coqtable.entries[i].coqrow) < config.ncourseoutcomes:
                cell = CoQCell()
                self.coqtable.entries[i].coqrow.append_entry(cell)
            
        for i in xrange(config.nquestions):
            for j in xrange(config.ncourseoutcomes):
                self.coqtable.entries[i].coqrow.entries[j].coqcorr.data = copo.coqcorr[i][j]
            self.coqtable.entries[i].marksassigned.data = copo.coqcorr[i]["marksassigned"]
            self.coqtable.entries[i].targetmarks.data = copo.coqcorr[i]["targetmarks"]
            
    def formtodata(self, copo):
        copo.courseoutcome_1 = self.courseoutcome_1.data 
        copo.outcomeKlevel_1 = self.outcomeKlevel_1.data
        copo.courseoutcome_2 = self.courseoutcome_2.data 
        copo.outcomeKlevel_2 = self.outcomeKlevel_2.data
        copo.courseoutcome_3 = self.courseoutcome_3.data 
        copo.outcomeKlevel_3 = self.outcomeKlevel_3.data
        copo.courseoutcome_4 = self.courseoutcome_4.data 
        copo.outcomeKlevel_4 = self.outcomeKlevel_4.data
        copo.courseoutcome_5 = self.courseoutcome_5.data 
        copo.outcomeKlevel_5 = self.outcomeKlevel_5.data
        copo.courseoutcome_6 = self.courseoutcome_6.data 
        copo.outcomeKlevel_6 = self.outcomeKlevel_6.data
        
        copo.description = self.description.data
        
        copo.copocorr = {}
        for i in xrange(config.ncourseoutcomes):
            copo.copocorr[i] = []
            for j in xrange(config.nprogramoutcomes):
                inp = self.copotable.entries[i].coporow.entries[j].copocorr.data
                try:
                    inp = inp.upper()[0]
                except IndexError:
                    inp = 'N'
                inp = inp if inp in ['S','W','M'] else 'N'
                copo.copocorr[i] += [inp]
        
        copo.coqcorr = {}
        for i in xrange(config.nquestions):
            copo.coqcorr[i] = {}
            for j in xrange(config.ncourseoutcomes):
                copo.coqcorr[i][j] = self.coqtable.entries[i].coqrow.entries[j].coqcorr.data
            copo.coqcorr[i]["marksassigned"] = self.coqtable.entries[i].marksassigned.data
            copo.coqcorr[i]["targetmarks"] = self.coqtable.entries[i].targetmarks.data
        
class NewCourseForm(Form):
    coursecode = TextAreaField('coursecode', validators=[Length(max=30)])
    coursename = TextAreaField('coursename', validators=[Length(max=30)])  
    classname  = SelectField('classname', coerce=int, choices=[(key, config.dict_class[key]) for key in config.dict_class.keys()])
    facultyname_1 = TextAreaField('facultyname_1',validators = [Length(max=70)])
    facultyname_2 = TextAreaField('facultyname_2',validators = [Length(max=70)])
    facultyname_3 = TextAreaField('facultyname_3',validators = [Length(max=70)])
    facultyname_4 = TextAreaField('facultyname_4',validators = [Length(max=70)])
    examsession = SelectField('examsession', coerce=int, choices=[(key, config.dict_examsessions[key]) for key in config.dict_examsessions.keys()])
    def __init__(self, *args, **kwargs): #FormID is session_coursecode
        Form.__init__(self, *args, **kwargs)
    def validate(self):
        if not Form.validate(self):
            return False
        else:
            uniqueID = self.coursecode.data+'_'+str(self.examsession.data)
            copos = CoPoMap.query.filter(CoPoMap.uniqueID == uniqueID).first()
            if copos == None:
                return True
            else:
                self.coursecode.errors.append("An entry for this course name for this exam session already exists.")
                return False
    def formtodata(self, copo):
        copo.coursecode = self.coursecode.data
        copo.coursename = self.coursename.data
        copo.classname = config.dict_class[self.classname.data]
        copo.facultyname_1 = self.facultyname_1.data
        copo.facultyname_2 = self.facultyname_2.data
        copo.facultyname_3 = self.facultyname_3.data
        copo.facultyname_4 = self.facultyname_4.data
        copo.examsession = self.examsession.data