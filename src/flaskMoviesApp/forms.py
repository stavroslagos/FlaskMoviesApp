from cProfile import label
from email import message
from flask_wtf.file import FileAllowed, FileField
from wtforms import (StringField, SubmitField, BooleanField, 
                    TextAreaField, IntegerField)
from wtforms.validators import (Optional,DataRequired, Email, 
                                Length, EqualTo, NumberRange, ValidationError)
from FlaskMoviesApp.models import User

from flask_wtf import FlaskForm

from datetime import datetime as dt
from flask_login import current_user


### Συμπληρώστε κάποια από τα imports που έχουν αφαιρεθεί ###
# Added by Stavros Lagos 4.2.2022


current_year = dt.now().year


''' Custom Validation function outside the form class '''
def maxImageSize(max_size=2):
    max_bytes = max_size * 1024 * 1024
    def _check_file_size(form, field):
        if len(field.data.read()) > max_bytes:
            raise ValidationError(f'Το μέγεθος της εικόνας δε μπορεί να υπεβαίνει τα {max_size} MB')

    return _check_file_size


''' Validation function outside the form class '''
def validate_email(form, email):
    user = User.query.filter_by(email=email.data).first()
    if user:
        raise ValidationError(f'Tο email {user.email} υπάρχει ήδη!')



class SignupForm(FlaskForm):
    username = StringField(label="Username",
                           validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."),
                                       Length(min=3, max=15, message="Αυτό το πεδίο πρέπει να είναι από 3 έως 15 χαρακτήρες")])

    email = StringField(label="email",
                           validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."), 
                                       Email(message="Παρακαλώ εισάγετε ένα σωστό email"), validate_email])

    password = StringField(label="password",
                           validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."),
                                       Length(min=3, max=15, message="Ο κωδικός πρέπει να είναι από 3 έως 15 χαρακτήρες")])
    
    password2 = StringField(label="Επιβεβαίωση password",
                           validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."),
                                       Length(min=3, max=15, message="Αυτό το πεδίο πρέπει να είναι από 3 έως 15 χαρακτήρες"),
                                       EqualTo('password', message='Τα δύο password πρέπει να είναι τα ίδια')])
    
    submit = SubmitField('Εγγραφή')


    def validate_username(self, username):
        ## Validator για έλεγχο ύπαρξης του user στη βάση
        # Added by Stavros Lagos 4.2.2022
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(f'To username {user.username} υπάρχει ήδη!')




class AccountUpdateForm(FlaskForm):
    username = StringField(label="Username",
                           validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."),
                                       Length(min=3, max=15, message="Αυτό το πεδίο πρέπει να είναι από 3 έως 15 χαρακτήρες")])

    email = StringField(label="email",
                           validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."), 
                                       Email(message="Παρακαλώ εισάγετε ένα σωστό email")])

    ## Αρχείο Εικόνας, με επιτρεπόμενους τύπους εικόνων τα 'jpg', 'jpeg', 'png', 
    # και μέγιστο μέγεθος αρχείου εικόνας τα 2 MBytes, ΜΗ υποχρεωτικό πεδίο
    # Added by Stavros Lagos 4.2.2022
    profile_image = FileField(label='Εικόνα χρήστη', validators=[Optional(strip_whitespace=True),
                                                    FileAllowed(['jpg','jpeg','png'],'Επιτρέπονται μόνο αρχεία εικόνας τύπου jpg,jpeg,png'),
                                                    maxImageSize(max_size=2)])

   
    submit = SubmitField('Αποστολή')


    def validate_username(self, username):
        ## Validator για έλεγχο ύπαρξης του user στη βάση
        # Added by Stavros Lagos 4.2.2022
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('To username υπάρχει ήδη!')

    def validate_email(self, email):
        ## Validator για έλεγχο ύπαρξης του email στη βάση
        # Added by Stavros Lagos 4.2.2022
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('To email υπάρχει ήδη!')




class LoginForm(FlaskForm):
 
    email = StringField(label="email",
                           validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."), 
                                       Email(message="Παρακαλώ εισάγετε ένα σωστό email")])

    password = StringField(label="password",
                           validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό.")])
    
    remember_me = BooleanField(label="Remember me")

    submit = SubmitField('Είσοδος')




class NewMovieForm(FlaskForm):
    title = StringField(label="Τίτλος ταινίας",
                           validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."),
                                       Length(min=3, max=50, message="Αυτό το πεδίο πρέπει να είναι από 3 έως 15 χαρακτήρες")])

    ## Τίτλος Ταινίας, υποχρεωτικό πεδίο κειμένου από 3 έως 50 χαρακτήρες και το αντίστοιχο label 
    # και μήνυμα στον validator
    # Added by Stavros Lagos 4.2.2022


    plot = TextAreaField(label="Υπόθεση",
                        validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."),
                                       Length(min=5, message="Αυτό το πεδίο πρέπει να είναι μεγαλύτερο από 5 χαρακτήρες")])
    ## Υπόθεση Ταινίας, υποχρεωτικό πεδίο κειμένου, από 5 έως απεριόριστο αριθμό χαρακτήρων 
    # και το αντίστοιχο label και μήνυμα στον validator
    # Added by Stavros Lagos 4.2.2022

    
    image = FileField('Εικόνα Άρθρου', validators=[Optional(strip_whitespace=True),
                                                    FileAllowed([ 'jpg', 'jpeg', 'png' ],
                                                            'Επιτρέπονται μόνο αρχεία εικόνων τύπου jpg, jpeg και png!'),
                                                           maxImageSize(max_size=2)])
    ## Αρχείο Εικόνας, με επιτρεπόμενους τύπους εικόνων τα 'jpg', 'jpeg', 'png', 
    # και μέγιστο μέγεθος αρχείου εικόνας τα 2 MBytes, ΜΗ υποχρεωτικό πεδίο
    # Added by Stavros Lagos 4.2.2022

    release_year = IntegerField('Έτος πρώτης προβολής', validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."),
                                                                    NumberRange(min=1888,max=current_year,
                                                                    message="Το έτος πρώτης προβολής πρέπει να είναι μεταξύ 1888 και {current_year}!")])
    ## IntegerField με το έτος πρώτης προβολής της ταινίας, θα παίρνει τιμές από το 1888 
    # έως το current_year που υπολογίζεται στην αρχή του κώδικα εδώ στο forms.py
    # Added by Stavros Lagos 4.2.2022

    rating = IntegerField('Βαθμολογία Ταινίας', validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."),
                                                                        NumberRange(min=1,max=100,
                                                                    message="Η βαθμολογία πρέπει να είναι μεταξύ 1 και 100!")])
    ## Βαθμολογία Ταινίας (IntegerField), υποχρεωτικό πεδίο, Αριθμητική τιμή από 1 έως 100, 
    # με τη χρήση του validator NumberRange, και με το αντίστοιχο label και μήνυμα στον validator
    # Added by Stavros Lagos 4.2.2022


    submit = SubmitField(label='Αποστολή')
