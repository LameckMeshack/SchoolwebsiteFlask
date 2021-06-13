from flask import render_template, session,flash, request, redirect, url_for
from school2 import app, db, bcrypt
from .forms import RegistrationForm, LoginForm
from .model import User
from school2.units.models import Addunit, Course, Faculty
import os


# @app.route("/admin")
# def admin():
#     units = Addunit.query.all()
#     faculty = Addunit.query.filter_by(faculty_id=id)
#     courses = Course.query.join(Addunit,(Course.id==Addunit.course_id)).all()
#     cols =Faculty.query.join( Addunit,(Faculty.id==Addunit.faculty_id)).all()
#     if 'username' not in session:
#         flash('Please login first','danger')
#         return redirect(url_for('login'))
    
#     return render_template("admin/results.html", title="Admins Page", units=units,faculty=faculty, cols=cols,courses=courses)



@app.route('/admin', methods=['GET', 'POST'], defaults={"page": 1})
@app.route('/admin/<int:page>', methods=['GET', 'POST'])
def admin(page):
    page = page
    pages=5
    units = Addunit.query.paginate(page,pages, error_out=False)
    cols =Faculty.query.join( Addunit,(Faculty.id==Addunit.faculty_id)).all()
    faculty = Addunit.query.filter_by(faculty_id=id)
    courses = Course.query.join(Addunit,(Course.id==Addunit.course_id)).all() 
    if 'username' not in session:
         flash('Please login first','danger')
         return redirect(url_for('login'))  
    # return render_template('units/result.html',title='Your Search', units=units, courses=courses,cols=cols)
    return render_template("admin/results.html", title="Admins Page", units=units,faculty=faculty, cols=cols,courses=courses)


@app.route('/faculties')
def faculties():
    if 'username' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    faculties = Faculty.query.order_by(Faculty.id.desc()).all()
    return render_template('admin/faculty.html', title = 'Faculty Page', faculties=faculties)


@app.route('/courses')
def courses():
    if 'username' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    courses = Course.query.order_by(Course.id.desc()).all()
    return render_template('admin/faculty.html', title='Courses', courses=courses)



@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User( username=form.username.data, regno=form.regno.data,  course=form.course.data, 
                     password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome {form.username.data}. Thanks for registering','success')
        return redirect(url_for('admin'))
    return render_template("admin/register.html", form=form, title="Class Rep Registration")

@app.route('/login', methods=['GET', 'POST'])
def login():
    units = Addunit.query.all()
    faculty = Addunit.query.filter_by(faculty_id=id)
    courses = Course.query.join(Addunit,(Course.id==Addunit.course_id)).all()
    cols =Faculty.query.join( Addunit,(Faculty.id==Addunit.faculty_id)).all()
    
    form = LoginForm(request.form)
    if request.method =="POST" and form.validate():
        user = User.query.filter_by(username = form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['username'] = form.username.data
            flash(f'Welcome {form.username.data} You are logged in now', 'success')
            return redirect(request.args.get('next') or url_for('admin'))
        else:
            flash('Wrong Password please try again', 'danger')
            return redirect(url_for('login'))
    return render_template('admin/login.html', title="Login Page", form=form,  units=units,faculty=faculty, cols=cols,courses=courses)
