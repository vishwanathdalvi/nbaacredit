from flask.ext.wtf import Form
from wtforms import StringField, SelectField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Length
import config
from app.models import User

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
                    
    

class CoPoForm(Form):
    coursecode  = StringField('coursecode' , validators=[DataRequired()])
    coursename  = StringField('coursename' , validators=[DataRequired()])
    facultyname_1 = StringField('facultyname_1')
    facultyname_2 = StringField('facultyname_2') 
    facultyname_3 = StringField('facultyname_3')
    facultyname_4 = StringField('facultyname_4')
    
    dict_Klevels = config.dict_Klevels
    dict_examsessions = config.dict_examsessions
    
    examsession = SelectField('examsession',
                              choices=[zip(dict_examsessions.keys(),[dict_examsessions[key] for key in dict_examsessions.keys()])],
                              coerce = int)
    courseoutcome_1 = TextAreaField('courseoutcome_1', validators=[Length(max=300)])
    courseoutcome_2 = TextAreaField('courseoutcome_2', validators=[Length(max=300)])
    courseoutcome_3 = TextAreaField('courseoutcome_3', validators=[Length(max=300)])
    courseoutcome_4 = TextAreaField('courseoutcome_4', validators=[Length(max=300)])
    courseoutcome_5 = TextAreaField('courseoutcome_5', validators=[Length(max=300)])
    courseoutcome_6 = TextAreaField('courseoutcome_6', validators=[Length(max=300)])
    
    outcomeKlevel_1 = SelectField('Klevel_1',choices=[zip(dict_Klevels.keys(), [dict_Klevels[key] for key in dict_Klevels.keys()])],coerce = int)
    outcomeKlevel_2 = SelectField('Klevel_2',choices=[zip(dict_Klevels.keys(), [dict_Klevels[key] for key in dict_Klevels.keys()])],coerce = int)
    outcomeKlevel_3 = SelectField('Klevel_3',choices=[zip(dict_Klevels.keys(), [dict_Klevels[key] for key in dict_Klevels.keys()])],coerce = int)
    outcomeKlevel_4 = SelectField('Klevel_4',choices=[zip(dict_Klevels.keys(), [dict_Klevels[key] for key in dict_Klevels.keys()])],coerce = int)
    outcomeKlevel_5 = SelectField('Klevel_5',choices=[zip(dict_Klevels.keys(), [dict_Klevels[key] for key in dict_Klevels.keys()])],coerce = int)
    outcomeKlevel_6 = SelectField('Klevel_6',choices=[zip(dict_Klevels.keys(), [dict_Klevels[key] for key in dict_Klevels.keys()])],coerce = int)
    
    def __init__(self, formID, *args, **kwargs): #FormID is session_coursecode
        Form.__init__(self, formID, *args, **kwargs)
        self.formID = formID
    def validate(self):
        if not Form.validate(self):
            return False
        else:
            return True
        