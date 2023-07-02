from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SECRET_KEY'] = 'your-secret-key'
db = SQLAlchemy(app)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    college = db.Column(db.String(50))
    roll_no = db.Column(db.String(10))

    def __init__(self, name, college, roll_no):
        self.name = name
        self.college = college
        self.roll_no = roll_no


class StudentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    college = StringField('College', validators=[DataRequired()])
    roll_no = StringField('Roll Number', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    db.create_all()
    form = StudentForm()

    if form.validate_on_submit():
        name = form.name.data
        college = form.college.data
        roll_no = form.roll_no.data
        student = Student(name, college, roll_no)
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('index'))

    students = Student.query.all()
    return render_template('index.html', form=form, students=students)


if __name__ == '__main__':
    app.run(debug=True)
