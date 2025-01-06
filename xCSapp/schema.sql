CREATE TABLE IF NOT EXISTS school_intro (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    description_manager TEXT
);

CREATE TABLE IF NOT EXISTS admissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    school_name TEXT NOT NULL,
    admission_status TEXT NOT NULL,
    admission_date TEXT NOT NULL,
    undergraduate_type TEXT NOT NULL,
    undergraduate_school TEXT,
    undergraduate_major TEXT, 
    gpa REAL NOT NULL,
    gpa_scale TEXT NOT NULL,
    average_score REAL NOT NULL,
    gre INTEGER,
    work TEXT NOT NULL,
    strong_recommendation TEXT NOT NULL,
    has_paper TEXT NOT NULL
);

DROP TABLE IF EXISTS visa;

CREATE TABLE visa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    visa_status TEXT NOT NULL,
    visa_type TEXT NOT NULL,
    interview_date TEXT NOT NULL,
    issue_date TEXT,
    location TEXT NOT NULL,
    major TEXT NOT NULL, 
    graduate_type  TEXT
);