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
        password = request.form['password']
        description = request.form['school-description']

        # 验证密码
        if password == '123456': 
            # 将新的院校简介存入数据库
            db.execute('INSERT INTO universities (name, description) VALUES (?, ?)', (school, description))
            db.commit()
            flash('院校简介已成功提交！', 'success')
            
        else:
            flash('密码错误！', 'error')

    # 获取院校简介信息
    school_info = db.execute('SELECT description FROM universities WHERE name = ?', (school,)).fetchone()

    # 获取该院校的录取信息
    admissions = db.execute('SELECT * FROM admissions WHERE school_name = ? ORDER BY admission_date DESC', (school,)).fetchall()
    return render_template('school.html', school_info=school_info, admissions=admissions, school=school)
