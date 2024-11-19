from datetime import datetime
from extensions import db
from sqlalchemy.orm import relationship


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)


class KnowledgeArea(db.Model):
    __tablename__ = 'knowledge_areas'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class Specialty(db.Model):
    __tablename__ = 'specialties'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class Specialization(db.Model):
    __tablename__ = 'specializations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class DepartmentHead(db.Model):
    __tablename__ = 'departments_heads'
    id_department_head = db.Column(db.Integer, primary_key=True)
    department_head = db.Column(db.String(200), nullable=False)

    users = relationship("User", back_populates="department_head_rel")


class Department(db.Model):
    __tablename__ = 'departments'
    id_department = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(100), nullable=False)
    id_department_head = db.Column(db.Integer, db.ForeignKey(
        'departments_heads.id_department_head'), nullable=True)


class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    is_curator = db.Column(db.Boolean, default=False)


class EducationProgram(db.Model):
    __tablename__ = 'education_programs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

    users = relationship("User", back_populates="education_program_rel")


class EducationDegree(db.Model):
    __tablename__ = 'education_degrees'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    users = relationship("User", back_populates="education_degree_rel")


class EducationForm(db.Model):
    __tablename__ = 'education_forms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    users = relationship("User", back_populates="education_form_rel")


class BasisOfAdmission(db.Model):
    __tablename__ = 'basis_of_admission'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    users = relationship("User", back_populates="basis_of_admission_rel")


class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    group_cipher = db.Column(db.String(100), unique=True, nullable=False)

    users = db.relationship('User', back_populates='group_rel')


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(255), nullable=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    department = db.Column(db.Integer, db.ForeignKey('departments.id_department'), nullable=True)
    department_head = db.Column(db.Integer, db.ForeignKey('departments_heads.id_department_head'), nullable=True)
    first_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)
    patronymic = db.Column(db.String(100), nullable=True)
    knowledge_area = db.Column(db.Integer, db.ForeignKey('knowledge_areas.id'), nullable=True)
    specialty = db.Column(db.Integer, db.ForeignKey('specialties.id'), nullable=True)
    specialization = db.Column(db.Integer, db.ForeignKey('specializations.id'), nullable=True)
    education_program = db.Column(db.Integer, db.ForeignKey('education_programs.id'), nullable=True)
    education_degree = db.Column(db.Integer, db.ForeignKey('education_degrees.id'), nullable=True)
    education_form = db.Column(db.Integer, db.ForeignKey('education_forms.id'), nullable=True)
    admission_date = db.Column(db.Date, nullable=True)
    basis_of_admission = db.Column(db.Integer, db.ForeignKey('basis_of_admission.id'), nullable=True)
    curator = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=True)
    group_cipher = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    photo = db.Column(db.String(255), nullable=True) 

    role_rel = db.relationship("Role", backref="users")
    department_rel = db.relationship("Department", backref="users")
    department_head_rel = db.relationship(
        "DepartmentHead", back_populates="users")
    knowledge_area_rel = db.relationship("KnowledgeArea", backref="users")
    specialty_rel = db.relationship("Specialty", backref="users")
    specialization_rel = db.relationship("Specialization", backref="users")
    curator_rel = db.relationship("Teacher", backref="users")
    education_program_rel = db.relationship(
        "EducationProgram", back_populates="users")
    education_degree_rel = db.relationship(
        "EducationDegree", back_populates="users")
    education_form_rel = db.relationship(
        "EducationForm", back_populates="users")
    basis_of_admission_rel = db.relationship(
        "BasisOfAdmission", back_populates="users")
    group_rel = db.relationship("Group", back_populates="users")


class Semester(db.Model):
    __tablename__ = 'semesters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    subject_name = db.Column(db.String(255), unique=True, nullable=False)

class StudentProgress(db.Model):
    __tablename__ = 'student_progress'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    semester_id = db.Column(db.Integer, db.ForeignKey('semesters.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    grade = db.Column(db.Integer, nullable=True)
    grade_ects = db.Column(db.String(10), nullable=True)
    grade_date = db.Column(db.Date, nullable=True)
    credits = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=True)
    hours_lectures = db.Column(db.Integer, nullable=True)
    hours_labs = db.Column(db.Integer, nullable=True)
    hours_practice = db.Column(db.Integer, nullable=True)
    hours_seminars = db.Column(db.Integer, nullable=True)
    hours_individual_work = db.Column(db.Integer, nullable=True)
    hours_self_study = db.Column(db.Integer, nullable=True)
    final_control = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    teacher_rel = db.relationship('Teacher', backref='student_progress')
    subject_rel = db.relationship('Subject', backref='student_progress')



def get_all_student_progress(student_id):
    return StudentProgress.query.filter_by(student_id=student_id).all()


def get_student_progress_by_semester(student_id, semester_id):
    return StudentProgress.query.filter_by(student_id=student_id, semester_id=semester_id).all()
