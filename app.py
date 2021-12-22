from email.mime.text import MIMEText

from flask import Flask, render_template, request

from DatabaseConnection import conneciton

from flask_mysqldb import MySQL
from flask_mail import Mail, Message

app = Flask(__name__)
app  = conneciton(app)
mysql = MySQL(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'pawwan431@gmail.com'
app.config['MAIL_PASSWORD'] = 'python@123'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
l=[]
form_data = None

@app.route('/')
def home():
    if request.method == "GET":
        request.method == "GET"
        cur = mysql.connection.cursor()
        curr = mysql.connection.cursor()
        cur.execute("select * from grocerylist;")
        curr.execute("select * from grocerylist;")
        curr.connection.commit()
        cur.connection.commit()
        records = cur.fetchall()
        recordss = curr.fetchall()
        #print(recordss)
    return render_template('index.html',name =records ,names = recordss,car_count = len(l))
    #return render_template('checkout.html')

    return render_template('index.html')

@app.route('/cart',methods=['GET', 'POST'])
def cart(records=None):
    global form_data, l
    if request.method == "GET":
        #form_data = request.form.get('id')
        form_data = request.args.get('type')
        l.append(form_data)
        request.method == "GET"
        cur = mysql.connection.cursor()
        curr = mysql.connection.cursor()
        cur.execute("select * from grocerylist;")
        cur.connection.commit()
        records  =cur.fetchall()
        return render_template('index.html', name=records,car_count = len(l))
    return render_template('index.html',name=records, car_count = len(l))

total_price = None
@app.route('/display', methods=['GET', 'POST'])
def display(records=None):
    global l,total_price
    selected_id = request.args.get('type')
    print(l)
    if selected_id in l:
        l.remove(selected_id)
        print(l)
    if request.method == "GET":
        cur = mysql.connection.cursor()
        #query = "select * from products where productCode IN %s" %str(l)
        id_tuple = tuple(l)

        if len(id_tuple) > 1:
            query = 'SELECT * FROM grocerylist WHERE Item_Code IN {};'.format(id_tuple)
            cur.execute(query)
        else:
            g = id_tuple[0]
            query_string = "SELECT * FROM grocerylist WHERE Item_Code = %s"
            cur.execute(query_string, (g,))

        cur.connection.commit()
        records  =cur.fetchall()
        s = 0
        for i in range(len(records)):
            #print(type(records[i][3]))
            s = s+ float(records[i][3])
        total_price = s
    return render_template('display.html',name =records ,price = s,car_count = len(l))
records_checkout = None
@app.route('/checkout', methods=['GET', 'POST'])
def checkout(records=None):
    global l,records_checkout
    selected_id = request.args.get('type')
    print(l)
    if selected_id in l:
        l.remove(selected_id)
        print(l)
    if request.method == "GET":
        cur = mysql.connection.cursor()
        #query = "select * from products where productCode IN %s" %str(l)
        id_tuple = tuple(l)

        if len(id_tuple) > 1:
            query = 'SELECT * FROM grocerylist WHERE Item_Code IN {};'.format(id_tuple)
            cur.execute(query)
        else:
            g = id_tuple[0]
            query_string = "SELECT * FROM grocerylist WHERE Item_Code = %s"
            cur.execute(query_string, (g,))

        cur.connection.commit()
        records  =cur.fetchall()

        records_checkout = records
        s = 0
        for i in range(len(records)):
            #print(type(records[i][3]))
            s = s+ float(records[i][3])
        #print(s)
    return render_template('checkout.html',name =records ,price = s,car_count = len(l))

invoice_data = []
Tax = 0.075
Grand_total = None
@app.route('/invoice', methods=['GET', 'POST'])
def invoice():
    global invoice_data,Tax,total_price,Grand_total,l

    full_name = request.form.get("firstname")
    Email =request.form.get("email")
    Address =request.form.get("address")
    City =request.form.get("city")
    State =request.form.get("state")
    Zip =request.form.get("zip")

    invoice_data = [full_name,Email,Address,City,State,Zip]

    Tax = total_price*0.075

    Grand_total = Tax+total_price

    msg = Message('Order successfully placed using FUCK.in', sender='pawwan431@gmail.com',
                  recipients=['amshala.srikanth438@gmail.com','ramakanth406@gmail.com'])

    msg.html = render_template( 'invoice.html',invoice_data =  invoice_data,records_checkout = records_checkout,total_price = total_price,Tax = Tax,Grand_total = Grand_total)
    mail.send(msg)

    l.clear()


    return render_template( 'invoice.html',invoice_data =  invoice_data,records_checkout = records_checkout,total_price = total_price,Tax = Tax,Grand_total = Grand_total)

@app.route('/<name>', methods=['GET', 'POST'])
def add(name):
    cur = mysql.connection.cursor()

    query_string = "SELECT * FROM grocerylist WHERE Item_Type = %s"

    cur.execute(query_string, (name,))
    cur.connection.commit()
    records = cur.fetchall()

    return render_template( 'drwopdown.html',name =records )


'''@app.route('/Update', methods=['GET', 'POST'])
def Update(records=None):

    if request.method == "POST":
        global form_data,l
        form_data = request.form['ftname']
        l.append(form_data)
        print(l)
        request.method == "GET"
        cur = mysql.connection.cursor()
        query = "select * from products;"
        cur.execute(query)
        cur.connection.commit()
        return render_template('updating.html')

    return render_template('Update.html')



@app.route('/Delete', methods=['GET', 'POST'])
def Delete(records=None):
    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute("select * from grocerylist")
        cur.connection.commit()
        records  =cur.fetchall()

    return render_template('Delete.html')'''

if __name__ == '__main__':

    app.run()

