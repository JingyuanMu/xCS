DROP TABLE IF EXISTS admissions;

CREATE TABLE IF NOT EXISTS universities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE admissions (
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

