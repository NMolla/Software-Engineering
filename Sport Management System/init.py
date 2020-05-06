#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='localhost',
                       port = 3306,
                       user='root',
                       password='',
                       db='SportsManagement',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

#Define a route to hello function
@app.route('/')
def hello():
    return render_template('index.html')

#Define route for login
@app.route('/login')
def login():
    return render_template('login.html')

#Define route for register
@app.route('/register')
def register():
    return render_template('register.html')

#Authenticates the login
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
    #grabs information from the forms
    username = request.form['username']
    password = request.form['password']

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM users WHERE username = %s and password = %s and role = %s'
    cursor.execute(query, (username, password, 'athlete'))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if(data):
        #creates a session for the the user
        #session is a built in
        session['username'] = username
        return render_template('athleteHome.html', username=username)
    else:
        cursor = conn.cursor()
        # executes query
        query = 'SELECT * FROM users WHERE username = %s and password = %s and role = %s'
        cursor.execute(query, (username, password, 'coach'))
        # stores the results in a variable
        data = cursor.fetchone()
        # use fetchall() if you are expecting more than 1 data row
        cursor.close()
        if (data):
            # creates a session for the the user
            # session is a built in
            session['username'] = username
            return render_template('coachHome.html', username=username)
        else:
            cursor = conn.cursor()
            # executes query
            query = 'SELECT * FROM users WHERE username = %s and password = %s and role = %s'
            cursor.execute(query, (username, password, 'admin'))
            # stores the results in a variable
            data = cursor.fetchone()
            # use fetchall() if you are expecting more than 1 data row
            cursor.close()
            if (data):
                # creates a session for the the user
                # session is a built in
                session['username'] = username
                return render_template('adminHome.html', username=username)
            else:
                #returns an error message to the html page
                error = 'Invalid login or username'
                return render_template('login.html', error=error)

#Authenticates the register
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
    #grabs information from the forms
    username = request.form['username']
    password = request.form['password']
    firstName = request.form['firstName']
    lastName = request.form['lastName']
    phoneNumber = request.form['phoneNumber']
    email = request.form['email']
    role = request.form['role']

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM users WHERE username = %s'
    cursor.execute(query, (username))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    error = None
    if(data):
        #If the previous query returns data, then user exists
        error = "This user already exists"
        return render_template('register.html', error = error)
    else:
        ins = 'INSERT INTO users VALUES(%s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(ins, (username, password, firstName, lastName, phoneNumber, email, role))
        conn.commit()
        cursor.close()
        return render_template('index.html')

@app.route('/admin')
def admin(): # irrelevant?
    return render_template('administratorHome.html')

@app.route('/coach')
def coach(): # irrelevant?
    return render_template('coachHome.html')

@app.route('/athlete')
def athlete(): # irrelevant?
    return render_template('athleteHome.html')

@app.route('/manageClasses')
def manageClasses():
    # user = session['username']
    cursor = conn.cursor()
    query1 = 'find registered classes' # configure
    cursor.execute(query1) # add parameters
    data1 = cursor.fetchall() # list of all enrolled classes
    cursor.close()
    return render_template('manageClasses.html', registeredClasses=data1)

@app.route('/manageEquipments')
def manageEquipments():
    # user = session['username']
    cursor = conn.cursor()
    query1 = 'find checked equipments'  # configure
    cursor.execute(query1)  # add parameters
    data1 = cursor.fetchall()  # list of all enrolled classes
    cursor.close()
    return render_template('manageEquipments.html', checkedEquipments=data1)

@app.route('/updateCoachSalary')
def updateCoachSalary():
    return render_template('updateCoachSalary.html')

@app.route('/displayFinancialReport')
def displayFinancialReport():
    return render_template('displayFinancialReport.html')

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')
        
app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug = True)
