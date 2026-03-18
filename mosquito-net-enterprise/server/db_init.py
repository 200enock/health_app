import sqlite3
conn = sqlite3.connect("mosquito.db")
c = conn.cursor()
c.executescript("""
CREATE TABLE IF NOT EXISTS users (
 id INTEGER PRIMARY KEY,
 username TEXT UNIQUE,
 password BLOB,
 role TEXT,
 district TEXT
);
CREATE TABLE IF NOT EXISTS sessions (
 token TEXT PRIMARY KEY,
 user_id INTEGER,
 created_at TEXT,
 expires_at TEXT
);
CREATE TABLE IF NOT EXISTS patients (
 id TEXT PRIMARY KEY,
 name TEXT,
 age INTEGER,
 sex TEXT,
 location TEXT,
 district TEXT,
 nin TEXT
);
CREATE TABLE IF NOT EXISTS distributions (
 id TEXT PRIMARY KEY,
 patient_id TEXT,
 date TEXT,
 location TEXT
);
CREATE TABLE IF NOT EXISTS logs (
 id INTEGER PRIMARY KEY,
 action TEXT,
 timestamp TEXT
);
""")
conn.commit()
conn.close()
print("DB initialized")
