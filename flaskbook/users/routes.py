from flask import render_template, redirect, url_for, request, flash, Blueprint
from flask_login import current_user, login_required, login_user, logout_user
from flaskbook import db, bcrypt
from flaskbook.modelss import User, Post
from flaskbook.users.forms import RegistrationForm, LoginForm, UpdateProfileForm, RequestResetForm, ResetPasswordForm
from flaskbook.users.utils import save_image, send_reset_email

users = Blueprint('users', __name__)



@users.route("/registration", methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:           #kada smo ulogovani i kada kliknemo na registrate ili login nece nigde otici jer sa ovim govorimo da je trenutno ulogovan, tako isto i za def login
        return redirect(url_for('main.home'))
    formation = RegistrationForm()
    if formation.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(formation.password.data).decode('utf-8')
        user = User(usernamee=formation.username.data, emaill=formation.email.data, passwordd=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! You are now able to Login", 'success')
        return redirect(url_for('users.login'))
    return render_template('registration.html', title='Registration', form=formation)

@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    formation = LoginForm()
    if formation.validate_on_submit():
        user = User.query.filter_by(emaill=formation.email.data).first()
        if user and bcrypt.check_password_hash(user.passwordd, formation.password.data):
            login_user(user, remember=formation.remember.data)
            #next page sluzi kada smo izlogovani na stranici profile, vodi nas direktno na profil stranicu a ne na home kao sto je bilo. U sledeca dve linije koda to i objasnjava kako se to radi
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))  #if next_page znaci da if next_page is not None
        else:
            flash('Login Unsuccessful. Please check your email and password', 'danger')
    return render_template('login.html', title='Login', form=formation)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/profile", methods=['GET', 'POST'])
@login_required                     #ovim kazemo da je potrebno da budes ulogovan kako bi odradio ovu funckiju
def profile():
    formation = UpdateProfileForm()
    #if sluzi da bi updejtovao username i email
    if formation.validate_on_submit():
        #if sluzi da bi postavili sliku
        if formation.image.data:
            image_file = save_image(formation.image.data)
            current_user.picture = image_file
        current_user.usernamee = formation.username.data
        current_user.emaill = formation.email.data
        db.session.commit()
        flash('Your profile has been updated.', 'success')
        return redirect(url_for('users.profile'))
    #elif sluzi da bi samo popunio polja sa trenutnim podatcima
    elif request.method == 'GET':
        formation.username.data = current_user.usernamee
        formation.email.data = current_user.emaill
    picturee = url_for('static', filename='profile_pics/' + current_user.picture)
    return render_template('profile.html', title='Profile', picturee=picturee, form=formation)


@users.route("/user/<string:usernammme>")
def user_posts(usernammme):
    stranica = request.args.get('pageee', 1, type=int)
    userko = User.query.filter_by(usernamee=usernammme).first_or_404()
    posts = Post.query.filter_by(author=userko).order_by(Post.date_posted.desc()).paginate(page=stranica, per_page=2)
    return render_template('user_posts.html', posts=posts, user=userko)



@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    formation = RequestResetForm()
    if formation.validate_on_submit():
        user = User.query.filter_by(emaill=formation.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=formation)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    formation = ResetPasswordForm()
    if formation.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(formation.password.data).decode('utf-8')
        user.passwordd = hashed_password
        db.session.commit()
        flash("Your password has been updated! You are now able to log in", 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=formation)
