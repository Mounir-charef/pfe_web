from flask import render_template, redirect, url_for, flash, request, Response
from home import app
from home import forms, db
from home.items import Item
from flask_login import login_user, logout_user, login_required
from werkzeug.utils import secure_filename
from home.y import Watermarking

@app.route('/',methods=['GET','POST'])
@app.route('/home',methods=['GET','POST'])
@login_required
def hello_world():  # put application's code here
    return render_template("index.html")


@app.route('/researchs')
@login_required
def mainpage():
    return render_template("recherches.html")
@app.route('/Types', methods=['GET', 'POST'])
@login_required
def types():
    form = forms.Uploadfield()
    if form.validate_on_submit():
        file1 = form.file.data
        filename = secure_filename(file1.filename)
        file1.save(f"{app.config['UPLOAD_FOLDER']}/{filename}")
        # Image.open(file1).show()
        # mimetype = file1.mimetype
        # image = items.img(img = file1.read(),name = filename,mimetype = mimetype )
        img, PSNR = Watermarking(f"{app.config['UPLOAD_FOLDER']}/{filename}")
        img.save(f"{app.config['UPLOAD_FOLDER']}/{filename}_watermarked.png")
        return render_template("upload.html", form=form, filename=filename,PSNR=PSNR)
    return render_template("upload.html", form=form)

@app.route('/AI')
@login_required
def aipage():
    return render_template("AI.html")

@app.route('/Contact')
def contact_page():
    return redirect(url_for('reg'))

@app.route('/login', methods=['GET', 'POST'])
def log():
    form = forms.Loginfield()
    url = request.args.get('next')
    if form.validate_on_submit():
        attempter_user = Item.query.filter_by(name=form.username.data).first()
        if (attempter_user and attempter_user.check_password_correct(form.password.data)):
            login_user(attempter_user)
            if url:
                return redirect(url)
            return redirect(url_for('log'))
        else:
            return redirect(url_for('hello_world'))


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
    if form.errors:
        for key, value in form.errors.items():
            flash(f'wch al hbiba{value[0]}', category='red')

    users = Item.query.all()
    return render_template('field.html', form=form,users=users)


@app.route('/logout')
def logout_page():
    logout_user()
    return redirect(url_for('log'))