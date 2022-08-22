from flask import flash, jsonify, render_template, redirect, request, url_for
from flask_cors import cross_origin
from flask_login import login_required, login_user, logout_user, current_user

from config import Config


from . import auth
from ..models import User
from app import db, oauth
from ..email import sendVerificationEmail
from .forms import LoginForm, SignUpForm, DeleteAccountForm





@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
        and not current_user.confirmed \
                and request.endpoint \
                and request.blueprint != 'auth' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.home'))
    return render_template('auth/unconfirmed.html')



@auth.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        user=User.query.filter_by(email=email).first()
        
        if user is not None and user.verify_password(password):
            login_user(user)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.home')
            return redirect(next)
        flash('Invalid username or password')
    return render_template ("auth/login.html", form=form)



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out!')
    return redirect(url_for("main.home"))



@auth.route('/signup', methods=["GET", "POST"])
def signup():

    form = SignUpForm()                                                                             

    if form.validate_on_submit():

        email = form.email.data
        username= form.username.data
        password = form.password.data

        #check username exist


        new_user = User(email=email,
                    username=username,
                    password=password)

        db.session.add(new_user)
        db.session.commit()

        token = new_user.generate_confirmation_token()

        
        email_data={
            "to": email,
            "subject": 'Confirm Your Account',
            "template": 'auth/email/confirm',
            "username": username,
            "token":token
        }

        sendVerificationEmail(email_data)

        flash('Thank you for signing up, A confirmation email has been sent to you by email.')

        return redirect(url_for('auth.login'))
    return render_template('auth/signup.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.home'))

    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account. Registration complete!')

    else:
        flash('The confirmation link is invalid or has expired.')

    return redirect(url_for('main.home'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()

    email = current_user.email
    username = current_user.username

    email_data={
            "to":email,
            "subject": 'Confirm Your Account',
            "template": 'auth/email/confirm',
            "username": username,
            "token":token
        }
    sendVerificationEmail(email_data)

    flash('A new confirmation email has been sent to you!.')

    return redirect(url_for('main.home'))


@auth.route('/delete-account/<int:id>', methods=['POST','GET'])
@login_required
def delete_account(id):
    form = DeleteAccountForm()
    if form.validate_on_submit() and form.answer.data==current_user.email:
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        flash('Account deleted')
        return redirect(url_for('main.home'))
    flash("incorrect input")
    return render_template('auth/delete_account.html', form=form)


@auth.route('/reset-password-mail')
def reset_password_mail():
    token = current_user.generate_confirmation_token()

    email = current_user.email
    username = current_user.username

    email_data={
            "to":email,
            "subject": 'Confirm Your Account',
            "template": 'auth/email/confirm',
            "username": username,
            "token":token
        }
    sendVerificationEmail(email_data)

    flash('An email with instructions to reset password has been sent to you!.')


@auth.route('/reset-password', methods=["POST"])
def reset_password():
    
    return redirect(url_for('main.home'))


@auth.route('/facebook')
def facebook():

    #FACEBOOK OAUTH CONFIG
    FACEBOOK_CLIENT_ID = Config.FACEBOOK_APP_ID
    FACEBOOK_CLIENT_SECRET = Config.FACEBOOK_APP_SECRET

    oauth.register(
        name='facebook',
        client_id = FACEBOOK_CLIENT_ID,
        client_secret = FACEBOOK_CLIENT_SECRET,
        access_token_url ='https://graph.facebook/oauth/access_token',
        access_token_params=None,
        authorize_url = 'https://www.facebook.com/dialog/oauth',
        authorize_params=None,
        api_base_url ='https://graph.facebook.com/14.0',
        client_kwargs={'scope':'public_profile,pages_show_list,business_management,user_posts,instagram_basic'}
    )
    redirect_uri = url_for('auth.facebook_auth', _external=True)
    return oauth.facebook.authorize_redirect(redirect_uri)


@auth.route('/facebook/auth/')
def facebook_auth():
    token = oauth.facebook.authorize_access_token()
    resp = oauth.facebook.get(
        'https://graph.facebook.com/14.0/me?fields=id,name,email,picture{url}'
    )
    profile = resp.json()
    #TODO: Save the user to the database and the access_token
    print('Fcebook User', profile)
    flash('Login with Facebook successful')
    return redirect(url_for('main.home'))

    