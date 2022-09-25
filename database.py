import mysql.connector
from datetime import datetime
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='admin',
    port='3306',
    database='attendancedb'
)
mycursor = mydb.cursor(buffered=True)
date = datetime.now().date()
def exist_name(name, Time,Event):
    mydb.reconnect()
    mycursor.execute('''SELECT name FROM attendancedb.empattendance  where Time between '00:00:00' and '15:59:59' and Event="Check In" and Date = DATE(NOW()) ''')
    row = mycursor.fetchall()
    for ro in row:
        if (name == ro[0]):
            return True
    return False

def exist_name_out(name, Time,Event):
    mydb.reconnect()
    mycursor.execute('''SELECT name FROM attendancedb.empattendance  where Time between '16:00:00' and '23:59:59' and Event="Check Out" and Date = DATE(NOW())''')
    row = mycursor.fetchall()
    for ro in row:
        if (name == ro[0]):
            return True
    return False


def check_name_state(name, Time, Date,Event):
    crTime = datetime.now().time()
    if (not (exist_name(name, crTime,Event))):
        markAttendance(name, Time, Date,Event)

def check_name_state_out(name, Time, Date,Event):
    crTime = datetime.now().time()
    if (not (exist_name_out(name, crTime,Event))):
        markAttendance(name, Time, Date,Event)

def markAttendance(name, Time, Date,Event):

    mycursor.execute("SELECT employeedata.EmpId FROM employeedata where employeedata.EmpName= %s", (name,))
    EmpId = mycursor.fetchall()
    try:
        EmpId = (EmpId[0][0])
        sql1 = '''insert into attendancedb.empattendance (Name,Date,Time,Event,EmpId) values(%s, %s, %s,%s,%s)'''
        val = (name, Date, Time,Event,EmpId)
        mycursor.execute(sql1, val)
        mydb.commit()
        mydb.close()
    except IndexError:
        pass





