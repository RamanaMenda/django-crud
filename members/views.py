from configparser import ConfigParser

from django.shortcuts import render
import mysql.connector
from mysql.connector import MySQLConnection
# from mysql.connector import connection

# Create your views here.
def index(request):
    return render(request,'index.html')

def select(request):
    op = request.POST['operation']
    if op == 'CREATE':
        return render(request,'create.html')
    elif op == 'READ':
        db = read_db('config.ini','MYSQL')
        conn = None
        conn = MySQLConnection(**db)
        cursor = conn.cursor()
        query = 'SELECT * FROM student'
        cursor.execute(query)
        rows = cursor.fetchmany(20)
        print(rows)
        return render(request, 'read.html', {'rows':rows})
    elif op == 'UPDATE':
        return render(request,'update.html')
    elif op == 'DELETE':
        return render(request,'delete.html')

def read_db(filename = 'config.ini',section = 'MYSQL'):
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    return db

def create(request):
    if request.method == 'POST':
        db = read_db('config.ini','MYSQL')
        conn = None
        conn = MySQLConnection(**db)
        cursor = conn.cursor()
        print(request.POST)
        name = request.POST["name"]
        roll = request.POST['roll']
        pon = request.POST['pno']
        email = request.POST['email']
        query = "INSERT INTO student(title,roll,phn,email) VALUES(%s,%s,%s,%s)"
        args = (name,roll,pon,email)
        cursor.execute(query,args)
        conn.commit()
        return render(request,'index.html')
    else:
        return render(request,'create.html')
def btn(request):
    return render(request,'index.html')

def delete(request):
    if request.method == 'POST':
        db = read_db('config.ini','MYSQL')
        conn = None
        conn = MySQLConnection(**db)
        cursor = conn.cursor()
        op = request.POST['operation']
        val = request.POST['val']
        if op == 'Name':
            query = "DELETE FROM student WHERE title = %s"
            args = (val,)
        elif op == 'Roll Number':
            query = "DELETE FROM student WHERE roll = %s"
            args = (int(val),)
        elif op == 'Phone Number':
            query = "DELETE FROM student WHERE phn = %s"
            args = (int(val),)
        elif op == 'Email':
            query = "DELETE FROM student WHERE email = %s"
            args = (val,)
        cursor.execute(query,args)
        conn.commit()
        return render(request,'index.html')
    else:
        return render(request,'delete.html')

def update(request):
    if request.method == 'POST':
        db = read_db('config.ini','MYSQL')
        conn = None
        conn = MySQLConnection(**db)
        cursor = conn.cursor()
        op = request.POST['operation']
        val = request.POST['val']
        ob = request.POST['object']
        upd = request.POST['upd']
        if ob == 'Roll Number' or ob == 'Phone Number':
            upd = int(upd)
        if ob == 'Name': ob = "title"
        elif ob == 'Roll Number': ob = "roll"
        elif ob == 'Phone Number': ob = 'phn'
        else: ob = "email"
        if op == 'Name':
            query = 'UPDATE student SET ' + ob + '= %s WHERE title = %s'
            args = (upd,val)
        elif op == 'Roll Number':
            query = 'UPDATE student SET ' + ob + '= %s WHERE roll = %s'
            args = (upd,int(val))
        elif op == 'Phone Number':
            query = 'UPDATE student SET ' + ob + '= %s WHERE phn = %s'
            args = (upd,int(val))
        elif op == 'Email':
            query = 'UPDATE student SET ' + ob + '= %s WHERE email = %s'
            args = (upd,val)
        cursor.execute(query,args)
        conn.commit()
        return render(request,'index.html')
    else:
        return render(request,'update.html')


