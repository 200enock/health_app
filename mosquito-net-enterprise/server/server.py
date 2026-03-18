import sqlite3, uuid
from predict import malaria_risk
DB = "mosquito.db"
conn = sqlite3.connect(DB, check_same_thread=False)
cursor = conn.cursor()
def add_patient(name, age, sex, location, district, nin):
    pid = str(uuid.uuid4())
    cursor.execute("INSERT INTO patients (id,name,age,sex,location,district,nin) VALUES (?,?,?,?,?,?,?)",
                   (pid,name,age,sex,location,district,nin))
    conn.commit()
    return pid
def distribute_net(patient_id, location):
    cursor.execute("SELECT * FROM patients WHERE id=?", (patient_id,))
    patient = cursor.fetchone()
    if patient:
        age = patient[2]
        risk = malaria_risk(120,28,70,1000)
        cursor.execute("INSERT INTO distributions (id,patient_id,date,location) VALUES (?,?,date('now'),?)",
                       (str(uuid.uuid4()), patient_id, location))
        conn.commit()
        return {"status":"Distributed","risk":risk}
    return {"error":"Patient not found"}
