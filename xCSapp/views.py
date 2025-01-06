from flask import Blueprint, render_template, request, redirect, url_for, flash
from .db import get_db

bp = Blueprint('views', __name__)

@bp.route('/dp', methods=('GET', 'POST'))
def dp():
    db = get_db()
    if request.method == 'POST':
        school_name = request.form['school_name']
        admission_status = request.form['admission_status']
        admission_date = request.form['admission_date']
        undergraduate_type = request.form['undergraduate_type']
        undergraduate_school = request.form.get('undergraduate_school')
        undergraduate_major = request.form.get('undergraduate_major')
        gpa = request.form['gpa']
        gpa_scale = request.form['gpa_scale']
        average_score = request.form['average_score']
        gre = request.form.get('gre')
        work = request.form['work']
        strong_recommendation = request.form['strong_recommendation']
        has_paper = request.form['has_paper']

        # Data validation
        if not school_name or not gpa:
            flash('School name and GPA are required!')
        else:
            db.execute(
                'INSERT INTO admissions (school_name, admission_status, admission_date, undergraduate_type, '
                'undergraduate_school, undergraduate_major, gpa, gpa_scale, average_score, gre, work, strong_recommendation, has_paper) '
                'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (school_name, admission_status, admission_date, undergraduate_type, undergraduate_school, undergraduate_major, gpa,
                 gpa_scale, average_score, gre, work, strong_recommendation, has_paper)
            )
            db.commit()
            

    admissions = db.execute('SELECT * FROM admissions ORDER BY admission_date DESC').fetchall()
    return render_template('dpnew.html', admissions=admissions)

def get_university_info(university_name):
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT description FROM universities WHERE name = ?", (university_name,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {"description": result[0]}
    return {"description": "没有找到该院校的简介信息"}

@bp.route('/<school>', methods=['GET', 'POST']) 
def show_school_info(school):
    db = get_db()

    # 校验请求是否为POST请求（提交新简介）
    if request.method == 'POST':
        description = request.form['description']
        db.execute('INSERT INTO school_intro (name, description)'
        'VALUES (?,?)', (school, description,))
        db.commit()


    # 获取院校简介信息
    school_info = db.execute('SELECT description_manager FROM school_intro WHERE name = ?', (school,)).fetchone()

    # 获取该院校的录取信息
    admissions = db.execute('SELECT * FROM admissions WHERE school_name = ? ORDER BY admission_date DESC', (school,)).fetchall()
    return render_template('school.html', school_info=school_info, admissions=admissions, school=school)

@bp.route('/cnvisa', methods=('GET', 'POST'))
def cnvisa():
    db = get_db()
    if request.method == 'POST':
        visa_status = request.form['visa_status']
        visa_type = request.form['visa_type']
        interview_date = request.form['interview_date']
        issue_date = request.form['issue_date']
        location = request.form['location']
        major = request.form['major']
        graduate_type = request.form['graduate_type']

        # Data validation
        if not visa_status or not interview_date or not location or not major or not graduate_type or not visa_type:
            flash('信息不完整！')
        else:
            db.execute(
                'INSERT INTO visa (visa_status, interview_date, visa_type, issue_date, location, '
                'major, graduate_type) '
                'VALUES (?, ?, ?, ?, ?, ?, ?)',
                (visa_status, interview_date, visa_type, issue_date, location, major, graduate_type)
            )
            db.commit()
            

    cnvisa = db.execute(
    '''
    SELECT * 
    FROM visa 
    WHERE location IN ('北京', '上海', '广州', '武汉', '沈阳') 
    ORDER BY interview_date DESC
    '''
    ).fetchall()

    return render_template('cnvisa.html', cnvisa=cnvisa)

@bp.route('/cmvisa', methods=('GET', 'POST'))
def cmvisa():
    db = get_db()
    if request.method == 'POST':
        visa_status = request.form['visa_status']
        visa_type = request.form['visa_type']
        interview_date = request.form['interview_date']
        issue_date = request.form['issue_date']
        location = request.form['location']
        major = request.form['major']

        # Data validation
        if not visa_status or not interview_date or not location or not major or not visa_type:
            flash('信息不完整！')
        else:
            db.execute(
                'INSERT INTO visa (visa_status, interview_date, visa_type, issue_date, location, '
                'major) '
                'VALUES (?, ?, ?, ?, ?, ?)',
                (visa_status, interview_date, visa_type, issue_date, location, major)
            )
            db.commit()
            

    cmvisa = db.execute(
    '''
    SELECT * 
    FROM visa 
    WHERE location NOT IN ('北京', '上海', '广州', '武汉', '沈阳') 
    ORDER BY interview_date DESC
    '''
    ).fetchall()

    return render_template('cmvisa.html', cmvisa=cmvisa)

@bp.route('/adminschool', methods=('GET', 'POST'))
def adminschool():

    db = get_db()
    if request.method == 'POST':
        id = request.form.get('id')  # Check if this is an update or new entry

        if id:  # This is an update
            school_name = request.form['school_name']
            admission_status = request.form['admission_status']
            admission_date = request.form['admission_date']
            undergraduate_type = request.form['undergraduate_type']
            undergraduate_school = request.form.get('undergraduate_school')
            undergraduate_major = request.form.get('undergraduate_major')
            gpa = request.form['gpa']
            gpa_scale = request.form['gpa_scale']
            average_score = request.form['average_score']
            gre = request.form.get('gre')
            work = request.form['work']
            strong_recommendation = request.form['strong_recommendation']
            has_paper = request.form['has_paper']

            db.execute(
                'UPDATE admissions SET school_name = ?, admission_status = ?, admission_date = ?, undergraduate_type = ?, '
                'undergraduate_school = ?, undergraduate_major = ?, gpa = ?, gpa_scale = ?, average_score = ?, gre = ?, '
                'work = ?, strong_recommendation = ?, has_paper = ? WHERE id = ?',
                (school_name, admission_status, admission_date, undergraduate_type, undergraduate_school, undergraduate_major, 
                 gpa, gpa_scale, average_score, gre, work, strong_recommendation, has_paper, id)
            )
            db.commit()


    admissions = db.execute('SELECT * FROM admissions ORDER BY admission_date DESC').fetchall()
    return render_template('adminschool.html', admissions=admissions)

@bp.route('/adminvisa', methods=('GET', 'POST'))
def adminvisa():
    db = get_db()
    if request.method == 'POST':
        id = request.form.get('id') 
        if id:
            visa_status = request.form['visa_status']
            visa_type = request.form['visa_type']
            interview_date = request.form['interview_date']
            issue_date = request.form['issue_date']
            location = request.form['location']
            major = request.form['major']
            graduate_type = request.form['graduate_type']

        # Data validation
        if not visa_status or not interview_date or not location or not major or not graduate_type or not visa_type:
            flash('信息不完整！')
        else:
            db.execute(
                'UPDATE visa SET visa_status=?, visa_type=?, interview_date=?, issue_date=?,location=?, major=?,graduate_type=? WHERE id = ?',
                (visa_status, visa_type, interview_date, issue_date, location, major, graduate_type, id)
            )
            db.commit()
            

    cnvisa = db.execute(
    '''
    SELECT * 
    FROM visa 
    ORDER BY interview_date DESC
    '''
    ).fetchall()

    return render_template('adminvisa.html', cnvisa=cnvisa)

@bp.route('/introshow', methods=('GET', 'POST'))
def introshow():
    db = get_db()
    if request.method == 'POST':
        name = request.form['name']
        description_manager =request.form['description_manager']

        db.execute(
                'INSERT INTO school_intro (name,description_manager) '
                'VALUES (?, ?)',
                (name, description_manager)
        )
        db.commit()
            

    school_intros = db.execute('SELECT * FROM school_intro ORDER BY id DESC').fetchall()
    return render_template('introshow.html', school_intros=school_intros)

@bp.route('/introedit', methods=('GET', 'POST'))
def introedit():
    db = get_db()
    if request.method == 'POST':
        id = request.form.get('id') 
        if id:
            description_manager =request.form['description_manager']

            db.execute(
                'UPDATE school_intro SET description_manager=? WHERE id = ?',
                (description_manager, id)
            )
            db.commit()

    school_intros = db.execute('SELECT * FROM school_intro ORDER BY id DESC').fetchall()
    return render_template('introedit.html', school_intros=school_intros)
