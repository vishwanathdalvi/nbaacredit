from wtforms import StringField, SelectField, TextAreaField, PasswordField
from wtforms import FormField, FieldList
from wtforms.validators import DataRequired, Length
from flask.ext.wtf import Form

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
                    
class CoPoCell(Form):
    copocorr = StringField(validators=[Length(max=1)])
class CoPoRow(Form):
    coporow = FieldList(FormField(CoPoCell))

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
        