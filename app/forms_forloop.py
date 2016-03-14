from flask.ext.wtf import Form
from wtforms import StringField, SelectField, TextAreaField
from wtforms.validators import DataRequired

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
ncourseoutcomes = 6
nprogramoutcomes = 14
nquestions = 15

class CoPoForm(Form):
    ncourseoutcomes = ncourseoutcomes+0
    nprogramoutcomes = nprogramoutcomes+0
    nquestions = nquestions+0    
    
    coursecode  = StringField('coursecode' , validators=[DataRequired()])
    coursename  = StringField('coursename' , validators=[DataRequired()])
    facultyname_1 = StringField('facultyname_1', validators=[DataRequired()])
    facultyname_2 = StringField('facultyname_2', validators=[DataRequired()]) 
    facultyname_3 = StringField('facultyname_3', validators=[DataRequired()])
    facultyname_4 = StringField('facultyname_4', validators=[DataRequired()]) 
    
    examsession = SelectField('examsession',
                              choices=[zip(dict_examsessions.keys(),[dict_examsessions[key] for key in dict_examsessions.keys()])],
                              coerce = int)
    listcourseoutcomes = []
    listoutcomeKlevel = []
    for i in xrange(ncourseoutcomes):
        courseoutcome = TextAreaField('courseoutcome%d'%(i),validators=[DataRequired()])
        outcomeKlevel = SelectField('klevel%d'%(i),
                                    choices=[zip(dict_Klevels.keys(), [dict_Klevels[key] for key in dict_Klevels.keys()])],
                                    coerce = int)
        listcourseoutcomes.append(courseoutcome)
        listoutcomeKlevel.append(outcomeKlevel)
    
    def __init__(self, formID, *args, **kwargs): #FormID is session_coursecode
        Form.__init__(self, formID, *args, **kwargs)
        self.formID = formID
    def validate(self):
        if not Form.validate(self):
            return False
        else:
            return True
        