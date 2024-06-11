from flask import Flask, render_template, request, url_for, flash, redirect
import pymysql
import logging
from flask import get_flashed_messages
import re


app = Flask(__name__)
app.secret_key = 'many_random_bytes'


def get_db_connection():
    return pymysql.connect(host='localhost', user='root', password='12345', database='crud1')


def is_valid_email(email):
    regex = r'^[a-zA-Z][a-zA-Z0-9._%+-]+@nucleusteq\.(com|in|ac\.in)$'
    if re.fullmatch(regex, email):
        return True
    else:
        return False


@app.route("/")
def data1():
    logging.info("Landing page accessed")
    return render_template("frontpage.html")


@app.route("/userlogin")
def data2():
    logging.info("User login Here")
    return render_template("userlogin.html")


@app.route('/userlogin', methods=['POST'])
def data2_post():
    db = pymysql.connect(host='localhost', user='root', password='12345', database='crud1')
    c = 0
    global username

    a = request.form["email"]
    username = a
    b = request.form["phone"]
    sql = "select * from employee where email=%s and phone=%s"
    cur = db.cursor()
    val=(a,b)
    cur.execute(sql,val)

    print(a, b)

    sql21 = "select * from assign where email=%s"
    cur21 = db.cursor()
    val2=(a)
    cur21.execute(sql21,val2)
    data21 = cur21.fetchall()

    for row in cur.fetchall()   :
        print("valid",row[0],row[1],row[2],row[3])
        logging.info("user dashboard accessed")
        return render_template("userdashboard.html",rows=row,rows2=row,assign=data21)

    else:
        logging.info("Invalid credentials of user-login")
        return "<h1> Invalid Login Credentials <a href='/userlogin'> Try Again</a></h1>"

    print(a, b)


@app.route("/registration")
def data3():
    logging.info("user registration dashboard")
    return render_template("registration.html")


@app.route('/registration', methods=['POST'])
def data3_post():
    db = pymysql.connect(host='localhost', user='root', password='12345', database='crud1')
    a = request.form["id"]
    b = request.form["name"]
    c = request.form["email"]
    d = request.form["phone"]
    e = request.form["designation"]
    
    #if not all([a, b, c, d, e]):
     #   logging.info("One or more fields are empty")
     #   return "<h1> All fields are required <a href='/registration'> Try Again</a></h1>"
    
    #if not is_valid_email(c):
    #    logging.info("Invalid email domain")
    #    return "<h1> Invalid Email Domain <a href='/registration'> Try Again</a></h1>"
    
        
    sql = "select * from employee where email=%s"
    val = (c)
    cur = db.cursor()
    cur.execute(sql, val)

    sql2 = "select * from employee where id=%s"
    val2 = (a)
    cur2 = db.cursor()
    cur2.execute(sql2, val2)
    
    sql3 = "select * from employee where phone=%s"
    val3 = (d)
    cur3 = db.cursor()
    cur3.execute(sql3, val3)


    if cur.fetchall():
        
        logging.info("email is available")
        return "<h1> Email Already Avaliable <a href='/registration'> Try New</a></h1>"
    elif cur2.fetchall():
            logging.info("Id exist")
            return "<h1> Id Already Avaliable <a href='/registration'> Try New</a></h1>"
    elif cur3.fetchall():
            logging.info("contact is available")
            return "<h1> Contact Already Avaliable <a href='/registration'> Try New</a></h1>"
    else:

        sql = "insert into employee values(%s,%s,%s,%s,%s)"
        val = (a, b, c, d, e)
        cur = db.cursor()
        cur.execute(sql, val)
        db.commit()
        print("save")
        logging.info("user is registered")
        return  redirect(url_for('data2'))


@app.route('/index')
def Index():
    db = pymysql.connect(host='localhost', user='root', password='12345', database='crud1')
    sql = "select * from employee"
    cur = db.cursor()
    cur.execute(sql)
    data = cur.fetchall()
    cur.close()
    
    logging.info("admin dashboard-employee management")
    return render_template('index.html', employee=data)



@app.route('/allocateinventory')
def Iallocateinventoryndex():
    db = pymysql.connect(host='localhost', user='root', password='12345', database='crud1')
    sql = "select * from employee"
    cur = db.cursor()
    cur.execute(sql)
    data = cur.fetchall()
    cur.close()
    db = pymysql.connect(host='localhost', user='root', password='12345', database='crud1')
    sql2 = "select * from inventory"
    cur2 = db.cursor()
    cur2.execute(sql2)
    data2 = cur2.fetchall()
    #sql21 = "select * from assign"
    sql21="select employee.id as id ,employee.name as name ,assign.email as email ,assign.type as type from employee,assign where assign.email=employee.email"
    cur21 = db.cursor()
    cur21.execute(sql21)
    data21 = cur21.fetchall()
    cur2.close()
    logging.info("Inventory assign dashboard")
    return render_template('Alloatinventory.html', employee=data,inven=data2,assign=data21)

@app.route('/allocateinventory', methods=['POST'])
def Iallocateinventoryndex2():
    db = pymysql.connect(host='localhost', user='root', password='12345', database='crud1')
    a = request.form["t1"]
    b = request.form["t2"]
    sql = "select * from assign where email=%s and type=%s "
    val = (a, b)
    cur = db.cursor()
    cur.execute(sql, val)
    if cur.fetchall():
        logging.info("Item is already assigned")
        return "<h1>Already Allot <a href='/allocateinventory'>Allot New</a></h1>"
    else:
        sql = "select * from inventory where mname=%s "
        val = (b)
        cur = db.cursor()
        cur.execute(sql, val)
        for row in cur.fetchall():
                    q=int(row[5])
                    sql = "update inventory set quantity=%s  where mname=%s"
                    cur=db.cursor()
                    val=(q-1,b)
                    cur.execute(sql,val)
                    db.commit()
                    print("submit sucessfully ",sql,val)
        sql = "insert into assign values(%s,%s )"
        val = (a, b)
        cur = db.cursor()
        cur.execute(sql, val)
        db.commit()
        print("save")
        
        logging.info("Item assigned")
        return redirect(url_for('Iallocateinventoryndex'))


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == "POST":
        a = request.form["id"]
        c = request.form["email"]
        d = request.form["phone"]
        
        db = pymysql.connect(host='localhost', user='root', password='12345', database='crud1')

        sql2 = "select * from employee where id=%s "
        val2 = (a)
        cur2 = db.cursor()
        cur2.execute(sql2, val2)
        
        sql3 = "select * from employee where email=%s "
        val3 = (c)
        cur3 = db.cursor()
        cur3.execute(sql3, val3)
        
        sql4 = "select * from employee where phone=%s "
        val4 = (d)
        cur4 = db.cursor()
        cur4.execute(sql4, val4)

        if cur2.fetchall():
            logging.info("Id already available")
            return "<h1>Already ID Avaliable <a href='/index'> Try New</a></h1>"
        elif cur3.fetchall():
            logging.info("email already present")
            return "<h1>Already Email Avaliable <a href='/index'> Try New</a></h1>"
        elif cur4.fetchall():
            logging.info("phone is already available")
            return "<h1>Already Phone Avaliable <a href='/index'> Try New</a></h1>"
        else:

            flash('Data Inserted Succesfully')
            db = pymysql.connect(host='localhost', user='root', password='12345', database='crud1')
            a = request.form["id"]
            b = request.form["name"]
            c = request.form["email"]
            d = request.form["phone"]
            e = request.form["designation"]
    

            sql = "insert into employee values(%s,%s,%s,%s,%s)"
            val = (a, b, c, d, e)
            cur = db.cursor()
            cur.execute(sql, val)
            db.commit()
            print("save")
            logging.info("inserted into employee")
            return redirect(url_for('Index'))


@app.route('/returnproduct')
def returnproduct():
    try:

        user = request.args.get('id')
        product = request.args.get('product')


        db = pymysql.connect(host='localhost', user='root', password='12345', database='crud1')

        sql = "select * from inventory where mname=%s "
        val = (product)
        cur = db.cursor()
        cur.execute(sql, val)
        for row in cur.fetchall():
                    q=int(row[5])
                    sql = "update inventory set quantity=%s  where mname=%s"
                    cur=db.cursor()
                    val=(q+1,product)
                    cur.execute(sql,val)
                    db.commit()
                    print("submit sucessfully ",sql,val)

        cur = db.cursor()

        sql = "DELETE FROM assign WHERE email=%s and type=%s"
        val = (user,product)
        cur.execute(sql, val)
        db.commit()

        print("Record Has Been Deleted Successfully")
    except Exception as e:
        print(str(e))
    finally:
        cur.close()
        db.close()

    logging.info("Item is unassigned")
    return redirect(url_for('Iallocateinventoryndex'))



@app.route('/delete')
def delete():
    try:

        user = request.args.get('id')
        db = pymysql.connect(host='localhost', user='root', password='12345', database='crud1')
        cur = db.cursor()

        sql = "DELETE FROM employee WHERE id=%s"
        val = (user)
        cur.execute(sql, val)
        db.commit()

        print("Record Has Been Deleted Successfully")
    except Exception as e:
        print(str(e))
    finally:
        cur.close()
        db.close()
        
    logging.info("employee deleted")  
    return redirect(url_for('Index'))

@app.route('/deleteinvt')
def deleteinvt():
    try:

        user = request.args.get('id')
        db = pymysql.connect(host='localhost', user='root', password='12345', database='crud1')
        cur = db.cursor()

        sql = "DELETE FROM inventory WHERE mid=%s"
        val = (user)
        cur.execute(sql, val)
        db.commit()

        print("Record Has Been Deleted Successfully")
    except Exception as e:
        print(str(e))
    finally:
        cur.close()
        db.close()

    logging.info("deleted from inventory")
    return redirect(url_for('Index1'))


@app.route('/update')
def update():
    print("call for update")
    user = request.args.get('id')
    db = pymysql.connect(host='localhost', user='root', password='12345', database='crud1')
    sql = "select * from employee where id=%s"

    val=(user)
    cur = db.cursor()
    cur.execute(sql,val)
    data = cur.fetchall()
    cur.close()

    logging.info("update dashboard")
    return render_template("indexupdateshow.html", inventory=data)

    print(user)

@app.route('/update', methods=['POST', 'GET'])
def update22():
    print("update is called")
    if request.method == 'POST':
        id_data = request.form['t1']
        print(id_data)
        name = request.form['t2']
        email = request.form['t3']
        phone = request.form['t4']
        des = request.form['t5']
        db = pymysql.connect(host='localhost', user='root', password='12345', database='crud1')
        sql = "UPDATE employee SET name=%s, email=%s, phone=%s,designation=%s WHERE id=%s"
        val = (name, email, phone,des, id_data)
        cur = db.cursor()
        cur.execute(sql, val)
        db.commit()
        print("Data Updated Successfully")
        cur.close()
        db.close()
        logging.info("employee updated")
        return redirect(url_for('Index'))

@app.route("/admin")
def data4():
    db = pymysql.connect(host='localhost', user='root', password='12345', database='crud1')
    sql = "select * from employee"
    cur = db.cursor()
    cur.execute(sql)
    data = cur.fetchall()
    cur.close()
    logging.info("admin login")
    return render_template("admin.html", employee=data)


@app.route('/admin', methods=['POST'])
def data21_post():
    db = pymysql.connect(host='localhost', user='root', password='12345', database='crud1')
    c = 0

    a = request.form["email"]
    b = request.form["password"]

    sql = "select * from admin"
    cur = db.cursor()
    cur.execute(sql)

    for row in cur.fetchall():
        if row[2] == a and row[1] == b:
            c = c + 1
    if c == 0:
        logging.info("Invalid login for admin")
        return "<h1>Invalid Login Credentials <a href='/admin'>Try Again</a></h1>"
    else:
        logging.info("login successfull for admin")
        return redirect(url_for("Index"))


@app.route("/adminsignup")
def data299():
    logging.info("admin register form")
    return render_template("adminsignup.html")


@app.route('/adminsignup', methods=['POST'])
def data333_post():
    db = pymysql.connect(host='localhost', user='root', password='12345', database='crud1')
    a = request.form["username"]
    b = request.form["password"]
    c = request.form["email"]
    d = request.form["contact"]
    sql = "select * from admin where email=%s "
    val = (c)
    cur = db.cursor()
    cur.execute(sql, val)
    sql2 = "select * from admin where contact=%s "
    val2 = (d)
    cur2 = db.cursor()
    cur2.execute(sql2, val2)

    if cur.fetchall():
        logging.info("email is already available-admin")
        return "<h1> Email already exist <a href='/adminsignup'>Try New</a></h1>"
    elif cur2.fetchall():
        logging.info("phone is already available- admin")
        return "<h1> Phone Number already exist <a href='/adminsignup'>Try New</a></h1>"
    else:
        sql = "insert into admin values(%s,%s,%s,%s)"
        val = (a, b, c, d)
        cur = db.cursor()
        cur.execute(sql, val)
        db.commit()
        print("save")
        logging.info("registered-admin")
        return redirect(url_for("data4"))


@app.route('/index1')
def Index1():
    db = pymysql.connect(host='localhost', user='root', password='12345', database='crud1')
    sql = "select * from inventory"
    cur = db.cursor()
    cur.execute(sql)
    data = cur.fetchall()
    cur.close()

    logging.info("Inventory dashboard")
    return render_template("index1.html", inventory=data)
@app.route('/update2')
def update41():
    print("call")
    user = request.args.get('id')
    db = pymysql.connect(host='localhost', user='root', password='12345', database='crud1')
    sql = "select * from inventory where mid=%s"

    val=(user)
    cur = db.cursor()
    cur.execute(sql,val)
    data = cur.fetchall()
    cur.close()

    logging.info("update inventory item")
    return render_template("inventoryupdateshow.html", inventory=data)

    print(user)

@app.route('/update2', methods=['POST', 'GET'])
def update42():
    print("update is called")
    if request.method == 'POST':
        mid = request.form['t1']
        print(mid)
        mname = request.form['t2']
        mquantity = request.form['t3']
        mmanu = request.form['t4']
        warranty = request.form['t5']
        quantity = request.form['t6']

        db = pymysql.connect(host='localhost', user='root', password='12345', database='crud1')
        sql = "UPDATE inventory SET  mname=%s, mquantity=%s,mmanu=%s,warranty=%s,quantity=%s WHERE mid=%s"
        val = (mname, mquantity, mmanu,warranty,quantity,mid)
        cur = db.cursor()
        cur.execute(sql, val)
        db.commit()
        print("Data Updated Successfully")
        cur.close()
        db.close()
        
        logging.info("Item updated")
        return redirect(url_for('Index1'))



@app.route('/insert1', methods=['POST'])
def insert1():
    if request.method == "POST":
        a = request.form["id"]
        b = request.form["name"]
        d = request.form["bno"]
        
        db = pymysql.connect(host='localhost', user='root', password='12345', database='crud1')

        sql2 = "select * from inventory where mid=%s "
        val2 = (a)
        cur2 = db.cursor()
        cur2.execute(sql2, val2)
        
        sql3 = "select * from inventory where mname=%s "
        val3 = (b)
        cur3 = db.cursor()
        cur3.execute(sql3, val3)
        
        sql4 = "select * from inventory where mmanu=%s "
        val4 = (d)
        cur4 = db.cursor()
        cur4.execute(sql4, val4)

        if cur2.fetchall():
            logging.info("Id already available")
            return "<h1>Already product ID Avaliable <a href='/index1'> Try New</a></h1>"
        elif cur3.fetchall():
            logging.info("product name already present")
            return "<h1>Already Product name Avaliable <a href='/index1'> Try New</a></h1>"
        elif cur4.fetchall():
            logging.info("Bill number is already available")
            return "<h1>Already Bill no. is Avaliable <a href='/index1'> Try New</a></h1>"
        else:

         flash("Data Inserted Succesfully")
         db = pymysql.connect(host='localhost', user='root', password='12345', database='crud1')
         a = request.form["id"]
         b = request.form["name"]
         c = request.form["dop"]
         d = request.form["bno"]
         e = request.form["warranty"]
         f = request.form["quantity"]

         sql = "insert into inventory values(%s,%s,%s,%s,%s,%s)"
         val = (a, b, c, d, e, f)
         cur = db.cursor()
         cur.execute(sql, val)
         db.commit()
         print("save")
         
         logging.info("Item added")
         return redirect(url_for('Index1'))


@app.route('/userdashboard')
def data27_post():
    db = pymysql.connect(host='localhost', user='root', password='12345', database='crud1')
   

    sql = "select * from employee"

    cur = db.cursor()
    cur.execute(sql)
    print(sql)
    
    
    return render_template("userdashboard.html", row=cur.fetchall())

logging.basicConfig(
    filename='app.log', 
    filemode='w',
    level=logging.DEBUG, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False,port=8099)