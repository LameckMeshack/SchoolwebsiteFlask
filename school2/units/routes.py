from school2.admin.routes import courses, faculties
from flask import redirect, render_template,session, url_for, flash, request
from werkzeug.utils import append_slash_redirect
from wtforms import form
from school2 import db, app
from .models import Addunit, Faculty, Course
from .form import Addunits
from sqlalchemy.exc import IntegrityError
# from sqlalchemy import or_
import os

@app.route('/index', methods=['GET', 'POST'], defaults={"page": 1})
@app.route('/index/<int:page>', methods=['GET', 'POST'])
def index(page):
    page = page
    pages=5
    units = Addunit.query.paginate(page,pages, error_out=False)
    cols =Faculty.query.join( Addunit,(Faculty.id==Addunit.faculty_id)).all()
    courses = Course.query.join(Addunit,(Course.id==Addunit.course_id)).all()   
    return render_template('units/result.html',title='Your Search', units=units, courses=courses,cols=cols)



@app.route('/')
def home():
    units= Addunit.query.filter(Addunit.link != "")    
    cols =Faculty.query.join( Addunit,(Faculty.id==Addunit.faculty_id)).all()
    courses = Course.query.join(Addunit,(Course.id==Addunit.course_id)).all()
    return render_template('units/first.html', units=units, cols=cols, courses=courses)

@app.route('/faculty/<int:id>')
def get_faculty(id):     
   faculty = Addunit.query.filter_by(faculty_id=id)
   courses = Course.query.join(Addunit,(Course.id==Addunit.course_id)).all()
   cols =Faculty.query.join( Addunit,(Faculty.id==Addunit.faculty_id)).all()
   return render_template('units/index.html',faculty=faculty, cols=cols, courses=courses )

@app.route('/courses/<int:id>')
def get_course(id):
    get_coz_unit = Addunit.query.filter_by(course_id=id)
    cols =Faculty.query.join( Addunit,(Faculty.id==Addunit.faculty_id)).all()
    courses = Course.query.join(Addunit,(Course.id==Addunit.course_id)).all()
    return render_template('units/index.html', get_coz_unit=get_coz_unit, courses=courses, cols=cols)


        

@app.route('/addfaculty', methods=['POST', 'GET'])
def addfaculty():
    if 'username' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    if request.method=="POST":
        getfaculty = request.form.get('faculty')
        faculty = Faculty(name=getfaculty)
        db.session.add(faculty)
        flash(f'The faculty {getfaculty} was added to your database', 'success')
        db.session.commit()
        return redirect(url_for('addfaculty'))
    return render_template('units/addfaculty.html', faculties='faculties')


@app.route('/updatefaculty/<int:id>',methods=['GET','POST'])
def updatefaculty(id):
    if 'username' not in session:
        flash('Login first please','danger')
        return redirect(url_for('login'))
    updatefaculty = Faculty.query.get_or_404(id)
    faculty = request.form.get('faculty')
    if request.method =="POST":
        updatefaculty.name = faculty
        flash(f'The faculty {updatefaculty.name} was changed to {faculty}','success')
        db.session.commit()
        return redirect(url_for('faculties'))
    faculty = updatefaculty.name
    return render_template('units/updatefaculty.html', title='Update Faculty',facuties='faculties',updatefaculty=updatefaculty)



@app.route('/deletefaculty/<int:id>', methods=['GET','POST'])
def deletefaculty(id):
    faculty = Faculty.query.get_or_404(id)
    if request.method=="POST":
        db.session.delete(faculty)
        flash(f"The faculty {faculty.name} was deleted from your database","success")
        db.session.commit(faculty)
        return redirect(url_for('admin'))
    flash(f"The faculty {faculty.name} can't be  deleted from your database","warning")
    return redirect(url_for('admin'))


@app.route('/addcourse', methods=['GET', 'POST'])
def addcourse():
    if 'username' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    if request.method=="POST":
        getcourse = request.form.get('course')
        coz = Course(name=getcourse)
        try:
            db.session.add(coz)
            flash(f'The course {getcourse} was added to your database', 'success')
            db.session.commit()
        except IntegrityError:
            db.session.rollback  
        return redirect(url_for('addcourse'))
    return render_template('units/addfaculty.html')


@app.route('/updatecourse/<int:id>',methods=['GET','POST'])
def updatecourse(id):
    if 'username' not in session:
        flash('Login first please','danger')
        return redirect(url_for('login'))
    updatecourse = Course.query.get_or_404(id)
    course = request.form.get('course')  
    if request.method =="POST":
        updatecourse.name = course
        flash(f'The course {updatecourse.name} was changed to {course}','success')
        db.session.commit()
        return redirect(url_for('courses'))
    course = updatecourse.name
    return render_template('units/updatefaculty.html', title='Update course Page',updatecourse=updatecourse)


@app.route('/deletecourse/<int:id>', methods=['GET','POST'])
def deletecourse(id):
    course = Course.query.get_or_404(id)
    if request.method=="POST":
        db.session.delete(course)
        flash(f"The course {course.name} was deleted from your database","success")
        db.session.commit()
        return redirect(url_for('admin'))
    flash(f"The course {course.name} can't be  deleted from your database","warning")
    return redirect(url_for('admin'))



@app.route('/addunit', methods=['POST', 'GET'])
def addunit():
    if 'username' not in session:
        flash('Please login first','danger')
        return redirect(url_for('login'))
    faculties = Faculty.query.all()
    courses = Course.query.all()
    form = Addunits(request.form)
    if request.method == 'POST':
        name = form.name.data
        unitcode = form.unitcode.data
        lecname = form.lecName.data
        faculty = request.form.get('faculty')
        course = request.form.get('course')
        link = form.link.data
        addunit = Addunit(name=name, unitcode=unitcode, lecname=lecname,faculty_id=faculty, course_id=course,link=link)
        db.session.add(addunit)
        db.session.commit()
        flash(f'The unit {name} has been added to the database', 'success')
        return redirect(url_for('admin'))
    return render_template('units/addunit.html', title='Add Unit Page', form=form, faculties=faculties, courses=courses)



@app.route('/updateunit/<int:id>', methods=['GET','POST'])
def updateunit(id):
    form = Addunits(request.form)
    unit = Addunit.query.get_or_404(id)
    faculties = Faculty.query.all()
    courses = Course.query.all()
    faculty = request.form.get('faculty')
    course = request.form.get('course')
    if request.method =="POST":
        unit.name = form.name.data
        unit.unitcode = form.unitcode.data
        unit.lecname = form.lecName.data
        unit.faculty_id = request.form.get('faculty')
        unit.course_id = request.form.get('course')
        unit.link = form.link.data      
        flash('The unit was updated','success')
        db.session.commit()
        return redirect(url_for('admin'))
    form.name.data = unit.name
    form.unitcode.data = unit.unitcode
    form.lecName.data = unit.lecname
    form.link.data = unit.link
    faculty = unit.faculty.name
    course = unit.course.name 
    return render_template('units/updateunit.html', form=form, title='Update unit',getunit=unit, unit=unit, faculties=faculties, courses=courses)


@app.route('/deleteunit/<int:id>', methods=['POST'])
def deleteunit(id):
    unit = Addunit.query.get_or_404(id)
    if request.method =="POST":
        db.session.delete(unit)
        db.session.commit()
        flash(f'The unit {unit.name} was delete from your record','success')
        return redirect(url_for('admin'))
    flash(f'Can not delete the unit','danger')
    return redirect(url_for('admin'))