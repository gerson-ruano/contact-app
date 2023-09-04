from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_fontawesome import FontAwesome

app = Flask(__name__)
fa = FontAwesome(app)

#MYSQL CONECCION
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'flaskcontact'
mysql = MySQL(app)

#CONFIGURACION 
app.secret_key = 'mysecretkey'

#index de aplicacion
@app.route('/')
def inicio():
  cur = mysql.connection.cursor()
  cur.execute(' SELECT * FROM contact')
  data = cur.fetchall()
  return render_template('/index.html', contacts = data)

#Funcion de agregar contacto
@app.route('/add_contact', methods = ['POST'])
def add_contact():
  if request.method == 'POST':
    fullname = request.form['fullname']
    lastname = request.form['lastname']
    phone = request.form['phone']
    email = request.form['email']
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO contact (fullname, lastname, phone, email) VALUES (%s, %s, %s, %s)',
    (fullname, lastname, phone, email)) 
    mysql.connection.commit()
    flash('Contacto agregado satisfactorimente','success')
    return redirect(url_for('inicio'))

#Funcion de editar contacto
@app.route('/edit/<id>')
def get_contact(id):
  cur = mysql.connection.cursor()
  cur.execute('SELECT * FROM contact WHERE id = {0}'.format (id))
  data = cur.fetchall()
  return render_template('edit-contact.html', contact = data[0])
  
#Funcion de Eliminar contactos
@app.route('/delete/<string:id>')
def delete_contact(id):
  cur = mysql.connection.cursor()
  cur.execute('DELETE FROM contact WHERE id = {0}'.format (id))
  mysql.connection.commit()
  flash('Contacto removido satisfactoriamente','warning')
  return redirect(url_for('inicio'))

#Funcion de actualizar contactos
@app.route('/update/<id>', methods = ['POST'])
def update_contact(id):
  if request.method == 'POST':
    fullname = request.form['fullname']
    lastname = request.form['lastname']
    phone = request.form['phone']
    email = request.form['email']

    cur = mysql.connection.cursor()
    cur.execute(""" UPDATE contact SET fullname = %s, lastname = %s, phone = %s, email = %s WHERE id = %s """, (fullname, lastname, phone, email, id))
    mysql.connection.commit()
    flash('Contacto Actualizado Satisfactoriamente','info')
    return redirect(url_for('inicio'))

#Construir el servidor 
if __name__ == '__main__': 
  app.run(port = 3000, debug = True)