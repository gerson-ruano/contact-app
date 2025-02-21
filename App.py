from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_fontawesome import FontAwesome
from flask_paginate import Pagination
from bd.config import Config  # Importa la clase Config desde el archivo config.py

app = Flask(__name__)
fa = FontAwesome(app)

# Configura la aplicación con las configuraciones de la clase Config
app.config.from_object(Config)

# MYSQL CONECCION
mysql = MySQL(app)

#index de aplicacion
@app.route('/')
def inicio():
  page = request.args.get('page', type=int, default=1)
  per_page = 10  # Número de elementos por página

  search_query = request.args.get('q', default='')
  cur = mysql.connection.cursor()
  if search_query:
        # Realiza una búsqueda filtrada
      cur.execute('SELECT * FROM contact WHERE fullname LIKE %s OR id LIKE %s', ('%' + search_query + '%', '%' + search_query + '%'))
  else:
      # Sin búsqueda, recupera todos los contactos
      cur.execute('SELECT * FROM contact')
  data = cur.fetchall()  
  pagination = Pagination(page=page, total=len(data), record_name='contacts', per_page=per_page)
  
  #cur = mysql.connection.cursor()
  #cur.execute(' SELECT * FROM contact')
  #data = cur.fetchall()
  #pagination = Pagination(page=page, total=len(data), record_name='contacts', per_page=per_page)
    ## Asegúrate de pasar solo los elementos necesarios según la página actual
  return render_template('/index.html', contacts=data[(page-1)*per_page:page*per_page], pagination=pagination)

#Funcion de agregar contacto
@app.route('/add_contact', methods = ['GET','POST'])
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
    flash('Contacto agregado satisfactorimente')
    return redirect(url_for('inicio'))
  return render_template('add_contact.html')  # Renderiza la plantilla para GET

#Funcion de editar contacto
@app.route('/edit/<id>')
def get_contact(id):
  cur = mysql.connection.cursor()
  cur.execute('SELECT * FROM contact WHERE id = {0}'.format (id))
  data = cur.fetchall()
  return render_template('edit-contact.html', contact = data[0])
  
#Funcion de Eliminar contactos
@app.route('/delete/<string:id>', methods=['POST'])
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contact WHERE id = %s', (id,))
    mysql.connection.commit()
    flash('Contacto removido Satisfactoriamente')
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
    flash('Contacto actualizado Satisfactoriamente')
    return redirect(url_for('inicio'))

#Construir el servidor 
if __name__ == '__main__': 
  app.run(port = 3000, debug = True)