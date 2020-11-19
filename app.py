from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)


# MySQL Connection
app.config['MYSQL_HOST'] = 'LOCALHOST'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'BasicLR23'
app.config['MYSQL_DB'] = 'flask_contact_app'

mydb = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB']
)

# Session
app.secret_key = 'mysecretkey'

# Index
@app.route('/')
def Main():
    cur = mydb.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    
    return render_template('index.html', contacts = data)

# About
@app.route('/about')
def about():
    return render_template('about.html')

# ADD CONTACT
@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']

        cur = mydb.cursor()

        sql = 'INSERT INTO contacts (fullname, phone, email) VALUES (%s, %s, %s)'
        val = (fullname, phone, email)
        cur.execute(sql, val)

        mydb.commit()

        flash('Contact added successfully!')
        return redirect(url_for('Main'))

# EDIT CONTACT
@app.route('/edit_contact/<id>')
def get_contact(id):
    cur = mydb.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = {0}'.format(id))
    data = cur.fetchall()

    return render_template('edit-contact.html', contact = data[0])

# UPDATE CONTACT
@app.route('/update_contact/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']

        cur = mydb.cursor()
        cur.execute("""
        UPDATE contacts
        SET fullname = %s,
            phone = %s,
            email = %s
        WHERE id = %s
        """, (fullname, phone, email, id))

        mydb.commit()

        flash('Contact updated successfully!')
        return redirect(url_for('Main'))

# DELETE CONTACT
@app.route('/delete_contact/<string:id>')
def del_contact(id):
    cur = mydb.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mydb.commit()

    flash('Contact removed successfully!')
    return redirect(url_for('Main'))

if __name__ == '__main__':
    app.run(port=80, debug=True)