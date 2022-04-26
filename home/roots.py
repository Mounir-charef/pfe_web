from flask import render_template, redirect, url_for, flash, request
from home import app, fr
from home import forms, db
from home.items import Item
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from home.y import Watermarking, extract
from PIL import Image

@app.route('/',methods=['GET','POST'])
@app.route('/home',methods=['GET','POST'])
@login_required
def hello_world():
    form = forms.Uploadfield()
    if form.validate_on_submit():
        file1 = form.file.data
        filename = secure_filename(file1.filename)
        file1.save(f"{app.config['UPLOAD_FOLDER']}/{filename}")
        Image.open(f"{app.config['UPLOAD_FOLDER']}/{filename}").resize((256,256)).save(f"{app.config['UPLOAD_FOLDER']}/{filename}")
        msg = current_user.name.encode()
        img, PSNR , leng= Watermarking(f"{app.config['UPLOAD_FOLDER']}/{filename}",fr.encrypt(msg).decode())
        leng = str(leng).encode()
        leng = fr.encrypt(leng).decode()

        img.save(f"{app.config['UPLOAD_FOLDER']}/watermarked_{filename}")
        return render_template("upload.html", form=form, filename=filename, PSNR=PSNR, leng=leng)
    return render_template("upload.html", form=form)


@app.route('/extract', methods=['GET', 'POST'])
def reverse():
    form = forms.Extractfield()
    if form.validate_on_submit():
        leng = form.hashkey.data
        leng = leng.encode()
        leng = int(fr.decrypt(leng).decode())

        file1 = form.file.data
        filename = secure_filename(file1.filename)
        file1.save(f"{app.config['UPLOAD_FOLDER']}/{filename}")
        msg = extract(f"{app.config['UPLOAD_FOLDER']}/{filename}",leng).encode()
        msg = fr.decrypt(msg).decode()
        return render_template("extract.html", form=form, msg = msg, filename=filename)
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
                              password_hash = form.pass1.data)
        db.session.add(user_to_create)
        db.session.commit()
        flash(f' Account created with success',category='green')
        login_user(user_to_create)
    if form.errors:
        for key, value in form.errors.items():
            flash(f'Sorry but {value[0]}', category='red')

    users = Item.query.all()
    return render_template('signup.html', form=form,users=users)



@app.route('/logout')
def logout_page():
    logout_user()
    return redirect(url_for('log'))