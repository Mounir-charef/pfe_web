from flask import render_template, redirect, url_for, flash, request, Response
from home import app, fr, forms, db, mail
from home.items import Item
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from home.y import watermarking, extract
from home.LSB import LsbWatermark,LsbExtract
from flask_mail import Message
import os
import traceback

@app.route('/',methods=['GET','POST'])
@app.route('/home',methods=['GET','POST'])
@login_required
def hello_world():
    form = forms.Uploadfield()
    if form.validate_on_submit():
        if(form.Method.data == 1):
            file1 = form.file.data
            filename = secure_filename(file1.filename)
            file1.save(f"{app.config['UPLOAD_FOLDER']}/{filename}")
            msg = current_user.name.encode()
            msg = fr.encrypt(msg).decode()
            print(msg)
            try:
                img, PSNR, MSE, leng = watermarking(f"{app.config['UPLOAD_FOLDER']}/{filename}", msg)
            except Exception:
                flash(f' Image can\'t be watermarked please check: Image size: 256x256 and bigger ,  filetype:PNG ',
                      category='red')
                return render_template("upload.html", form=form)
            leng = str(leng).encode()
            leng = fr.encrypt(leng).decode()

            img.save(f"{app.config['UPLOAD_FOLDER']}/watermarked_{filename}",format='PNG')
            return render_template("upload.html", form=form, filename=filename, PSNR=PSNR, MSE=MSE, leng=leng)
        else:
            file1 = form.file.data
            filename = secure_filename(file1.filename)
            file1.save(f"{app.config['UPLOAD_FOLDER']}/{filename}")
            msg = current_user.name.encode()
            msg = fr.encrypt(msg).decode()
            print(msg)
            try:
                img, leng, PSNR, MSE = LsbWatermark(f"{app.config['UPLOAD_FOLDER']}/{filename}", msg)
            except Exception:
                flash(f' Image can\'t be watermarked please check: Image size: 256x256 and bigger ,  filetype:PNG ',
                      category='red')
                return render_template("upload.html", form=form)
            leng = str(leng).encode()
            leng = fr.encrypt(leng).decode()

            img.save(f"{app.config['UPLOAD_FOLDER']}/watermarked_{filename}")
            return render_template("upload.html", form=form, filename=filename, PSNR=PSNR, MSE=MSE, leng=leng)
    return render_template("upload.html", form=form)


@app.route('/extract', methods=['GET', 'POST'])
def reverse():
    form = forms.Extractfield()
    if form.validate_on_submit():
        if(form.Method.data == 1):
            file1 = form.file.data
            filename = secure_filename(file1.filename)
            leng = form.hashkey.data.encode()
            try:
                leng = int(fr.decrypt(leng).decode())
                file1.save(f"{app.config['UPLOAD_FOLDER']}/{filename}")
                msg = extract(f"{app.config['UPLOAD_FOLDER']}/{filename}", leng).encode()
                msg = fr.decrypt(msg).decode()
            except:
                return render_template("extract.html", form=form, filename=filename)
            user = Item.query.filter_by(name=msg).first()
            print(msg, user)
            if user:
                fullname = tuple(msg.split('_'))
                doctor, hospital = fullname
                return render_template("extract.html", form=form, doctor=doctor, hospital=hospital, email=user.email,
                                       filename=filename)
            return render_template("extract.html", form=form, filename=filename)
        else:
            file1 = form.file.data
            filename = secure_filename(file1.filename)
            leng = form.hashkey.data.encode()
            try:
                leng = int(fr.decrypt(leng).decode())
                file1.save(f"{app.config['UPLOAD_FOLDER']}/{filename}")
                msg = LsbExtract(f"{app.config['UPLOAD_FOLDER']}/{filename}", leng).encode()
                msg = fr.decrypt(msg).decode()
            except:
                return render_template("extract.html", form=form, filename=filename)

            user = Item.query.filter_by(name=msg).first()
            print(msg, user)
            if user:
                fullname = tuple(msg.split('_'))
                doctor, hospital = fullname
                return render_template("extract.html", form=form, doctor=doctor, hospital=hospital, email=user.email,
                                       filename=filename)
            return render_template("extract.html", form=form, filename=filename)
    return render_template("extract.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def log():
    if current_user.is_authenticated:
        logout_user()
    form = forms.Loginfield()
    url = request.args.get('next')
    if form.validate_on_submit():
        attempter_user = Item.query.filter_by(name=form.username.data).first()
        if (attempter_user and attempter_user.check_password_correct(form.password.data)):
            login_user(attempter_user)
            if url:
                return redirect(url)
            return redirect(url_for('hello_world'))
        else:
            flash(f' Username or password incorrect',category='red')
            return redirect(request.url)


    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reg():
    form = forms.Registerfield()
    if form.validate_on_submit():
        user_to_create = Item(name=form.user.data,
                              email=form.email.data,
                              password_hash = form.password.data)
        db.session.add(user_to_create)
        db.session.commit()
        try:
            msg = Message('PFE_I_ACAD81', sender=os.environ.get('MAIL_DEFAULT_USER'), recipients=[user_to_create.email])
            msg.body= 'Hello your account is successfully created in USTHB PFE ACAD I81'
            mail.send(msg)
        except Exception:
            print(traceback.format_exc())
            flash("Email failed to send",category='red')
        flash(f' Account created with success',category='green')
        login_user(user_to_create)
        return redirect(url_for('hello_world'))
    if form.errors:
        for key, value in form.errors.items():
            flash(f'Error in {key}:  {value[0]}', category='red')

    users = Item.query.all()
    return render_template('signup.html', form=form,users=users)


@app.route('/logout')
def logout_page():
    logout_user()
    return redirect(url_for('log'))