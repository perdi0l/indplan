from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import *
from extensions import db
import os

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'uploads')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return redirect(url_for('main.auth'))


@bp.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            password = request.form.get('password')
            if not username or not password:
                flash('Ім`я користувача або пароль не введено.', 'danger')
                return redirect(url_for('main.auth'))

            user = User.query.filter_by(username=username).first()

            if user is None:
                flash('Користувача не знайдено.', 'danger')
                return redirect(url_for('main.auth'))

            if user.password != password:
                flash('Неправильний пароль.', 'danger')
                return redirect(url_for('main.auth'))

            session['user_id'] = user.id
            session['user_role'] = user.role

            if user.role == 1:
                return redirect(url_for('main.admin_panel'))
            elif user.role == 2 or user.role == 1:
                return redirect(url_for('main.student_profile', user_id=user.id))
            # Додати функціонал пізніше
            # elif user.role == 3:  # Викладач
            #     return redirect(url_for('teacher.panel'))
            else:
                flash('Невідома роль користувача.', 'danger')
                return redirect(url_for('main.auth'))
        except Exception as e:
            flash(f'Виникла помилка під час авторизації: {e}', 'danger')
            return redirect(url_for('main.auth'))

    return render_template('auth.html')


@bp.route('/admin')
def admin_panel():
    try:
        user_id = session.get('user_id')
        user_role = session.get('user_role')

        if not user_id or user_role != 1:
            flash("Доступ заборонено: необхідні права адміністратора.", "danger")
            return redirect(url_for('main.auth'))

        users = User.query.all()
        return render_template('admin_panel.html', users=users)
    except Exception as e:
        flash(
            f'Виникла помилка під час завантаження панелі адміністратора: {e}', 'danger')
        return redirect(url_for('main.auth'))


@bp.route('/admin/create_student_progress/<int:student_id>', methods=['GET', 'POST'])
def create_student_progress(student_id):
    selected_semester_id = request.form.get('semester_id') or request.args.get('semester_id')

    if request.method == 'POST' and not selected_semester_id:
        semesters = request.form.getlist('semester_id[]')
        subjects = request.form.getlist('subject_id[]')
        grades = request.form.getlist('grade[]')
        grade_ects = request.form.getlist('grade_ects[]')
        grade_dates = request.form.getlist('grade_date[]')
        credits = request.form.getlist('credits[]')
        teachers = request.form.getlist('teacher_id[]')
        hours_lectures = request.form.getlist('hours_lectures[]')
        hours_labs = request.form.getlist('hours_labs[]')
        hours_practice = request.form.getlist('hours_practice[]')
        hours_seminars = request.form.getlist('hours_seminars[]')
        hours_individual_work = request.form.getlist('hours_individual_work[]')
        hours_self_study = request.form.getlist('hours_self_study[]')
        final_controls = request.form.getlist('final_control[]')

        for i in range(len(grades)):
            new_progress = StudentProgress(
                student_id=student_id,
                semester_id=semesters[i],
                subject_id=subjects[i],
                grade=grades[i],
                grade_ects=grade_ects[i],
                grade_date=grade_dates[i],
                credits=credits[i],
                teacher_id=teachers[i],
                hours_lectures=hours_lectures[i],
                hours_labs=hours_labs[i],
                hours_practice=hours_practice[i],
                hours_seminars=hours_seminars[i],
                hours_individual_work=hours_individual_work[i],
                hours_self_study=hours_self_study[i],
                final_control=final_controls[i]
            )
            db.session.add(new_progress)

        db.session.commit()
        flash('Прогрес збережено!', 'success')
        return redirect(url_for('main.create_student_progress', student_id=student_id))

    semesters = Semester.query.all()
    subjects = Subject.query.all()
    teachers = Teacher.query.all()

    selected_semester_progress = StudentProgress.query.filter_by(
        student_id=student_id, semester_id=selected_semester_id).all() if selected_semester_id else []

    return render_template(
        'create_student_progress.html',
        semesters=semesters,
        subjects=subjects,
        teachers=teachers,
        student_id=student_id,
        selected_semester_id=int(selected_semester_id) if selected_semester_id else None,
        selected_semester_progress=selected_semester_progress
    )



@bp.route('/admin/add_user', methods=['GET', 'POST'])
def add_user():
    if session.get('user_role') != 1:
        flash("Доступ заборонено", "danger")
        return redirect(url_for('main.auth'))

    try:
        departments = Department.query.all()
        department_heads = DepartmentHead.query.all()
        knowledge_areas = KnowledgeArea.query.all()
        specialties = Specialty.query.all()
        specializations = Specialization.query.all()
        roles = Role.query.all()
        teachers = Teacher.query.all()
        education_programs = EducationProgram.query.all()
        degrees = EducationDegree.query.all()
        forms = EducationForm.query.all()
        admission_bases = BasisOfAdmission.query.all()
        groups = Group.query.all()
    except Exception as e:
        flash(f"Помилка при завантаженні даних для форми: {e}", "danger")
        return redirect(url_for('main.admin_panel'))

    if request.method == 'POST':
        try:
            password = request.form['password']
            group_cipher = request.form['group_cipher'] if request.form['role'] == '2' else None
            admission_date = request.form['admission_date'] if request.form['admission_date'] else None

            photo = None
            if 'photo' in request.files:
                file = request.files['photo']
                if file and allowed_file(file.filename):
                    filename = file.filename
                    file.save(os.path.join(UPLOAD_FOLDER, filename))
                    photo = os.path.join('uploads', filename)

            new_user = User(
                username=request.form['username'],
                password=password,
                role=request.form['role'],
                first_name=request.form['first_name'],
                last_name=request.form['last_name'],
                patronymic=request.form['patronymic'],
                department=request.form['department'],
                department_head=request.form['department_head'],
                knowledge_area=request.form['knowledge_area'],
                specialty=request.form['specialty'],
                specialization=request.form['specialization'],
                education_program=request.form['education_program'],
                education_degree=request.form['education_degree'],
                education_form=request.form['education_form'],
                admission_date=admission_date,
                basis_of_admission=request.form['basis_of_admission'],
                curator=request.form['curator'] if request.form['role'] == '2' else None,
                group_cipher=group_cipher,
                photo=photo
            )

            db.session.add(new_user)
            db.session.commit()
            flash("Користувач успішно доданий", "success")
            return redirect(url_for('main.admin_panel'))
        except Exception as e:
            db.session.rollback()
            flash(f"Помилка при додаванні користувача: {e}", "danger")
            return redirect(url_for('main.add_user'))

    return render_template('add_user.html',
                           departments=departments,
                           department_heads=department_heads,
                           knowledge_areas=knowledge_areas,
                           specialties=specialties,
                           specializations=specializations,
                           roles=roles,
                           teachers=teachers,
                           education_programs=education_programs,
                           degrees=degrees,
                           forms=forms,
                           admission_bases=admission_bases,
                           groups=groups)


@bp.route('/admin/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        departments = Department.query.all()
        department_heads = DepartmentHead.query.all()
        knowledge_areas = KnowledgeArea.query.all()
        specialties = Specialty.query.all()
        specializations = Specialization.query.all()
        roles = Role.query.all()
        teachers = Teacher.query.all()
        education_programs = EducationProgram.query.all()
        degrees = EducationDegree.query.all()
        forms = EducationForm.query.all()
        admission_bases = BasisOfAdmission.query.all()
        groups = Group.query.all()
    except Exception as e:
        flash(
            f"Помилка при завантаженні даних для редагування користувача: {e}", "danger")
        return redirect(url_for('main.admin_panel'))

    if request.method == 'POST':
        try:
            user.username = request.form['username']
            user.role = request.form['role']
            user.first_name = request.form['first_name']
            user.last_name = request.form['last_name']
            user.patronymic = request.form['patronymic']
            user.department = request.form['department']
            user.department_head = request.form['department_head']
            user.knowledge_area = request.form['knowledge_area']
            user.specialty = request.form['specialty']
            user.specialization = request.form['specialization']
            user.education_program = request.form['education_program']
            user.education_degree = request.form['education_degree']
            user.education_form = request.form['education_form']
            user.admission_date = request.form['admission_date'] if request.form['admission_date'] else None
            user.basis_of_admission = request.form['basis_of_admission']
            user.curator = request.form['curator']
            user.group = request.form['group']

            new_password = request.form.get('password')
            if new_password:
                user.password = new_password

            profile_image = request.files.get('profile_image')
            if profile_image and allowed_file(profile_image.filename):
                filename = profile_image.filename
                profile_image.save(os.path.join(UPLOAD_FOLDER, filename))
                user.photo = os.path.join('uploads', filename)

            db.session.commit()
            flash("Користувач успішно оновлений", "success")
            return redirect(url_for('main.admin_panel'))
        except Exception as e:
            db.session.rollback()
            flash(f"Помилка при оновленні даних користувача: {e}", "danger")
            return redirect(url_for('main.edit_user', user_id=user_id))

    return render_template('edit_user.html',
                           user=user,
                           departments=departments,
                           department_heads=department_heads,
                           knowledge_areas=knowledge_areas,
                           specialties=specialties,
                           specializations=specializations,
                           roles=roles,
                           teachers=teachers,
                           education_programs=education_programs,
                           degrees=degrees,
                           forms=forms,
                           admission_bases=admission_bases,
                           groups=groups)


@bp.route('/admin/student_profile/<int:user_id>')
def view_profile(user_id):
    try:
        student = User.query.get_or_404(user_id)
        if student.role != 2:
            flash("Це не студентський профіль.", "danger")
            return redirect(url_for('main.admin_panel'))

        return render_template('student_profile.html', student=student)
    except Exception as e:
        flash(f'Помилка при завантаженні профілю: {e}', 'danger')
        return redirect(url_for('main.admin_panel'))


@bp.route('/admin/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if session.get('user_role') != 1:
        flash("Доступ заборонено", "danger")
        return redirect(url_for('main.auth'))

    try:
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        flash("Користувач успішно видалений", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Помилка при видаленні користувача: {e}", "danger")
    return redirect(url_for('main.admin_panel'))


@bp.route('/student_profile/<int:user_id>', methods=['GET', 'POST'])
def student_profile(user_id):
    try:
        student = User.query.get_or_404(user_id)
        student_progress = get_all_student_progress(user_id)
        semester_ids = {progress.semester_id for progress in student_progress}
        semesters = Semester.query.filter(Semester.id.in_(semester_ids)).all()
        selected_semester_id = request.form.get('semester_id')

        if selected_semester_id:
            student_progress = get_student_progress_by_semester(
                user_id, selected_semester_id)

        if student.photo:
            student.photo = student.photo.replace("\\", "/")

    except Exception as e:
        flash(f"Помилка при завантаженні профілю студента: {e}", "danger")
        return redirect(url_for('main.admin_panel'))

    return render_template('student_profile.html',
                           student=student,
                           semesters=semesters,
                           progress=student_progress)


def init_routes(app):
    app.register_blueprint(bp)
