import os
from flask import render_template, request, redirect, session
from flask import Flask
from flask_mysqldb import MySQL
from datetime import datetime
from flask import send_from_directory


app=Flask(__name__)
app.secret_key="nicolitha28"
mysql=MySQL()


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'sitio'

mysql.init_app(app)

@app.route('/')
def inicio():
    return render_template('sitio/index.html')

@app.route('/img/<imagen>')
def imagenes(imagen):
    print(imagen)
    return send_from_directory(os.path.join('templates/sitio/img'),imagen)

@app.route("/css/<archivocss>")
def css_link(archivocss):
    return send_from_directory(os.path.join('templates/sitio/css'),archivocss)

@app.route('/trabajos')
def trabajos():
    # Obtén un cursor para interactuar con la base de datos
    cursor = mysql.connection.cursor()
    
    # Ejecuta una consulta (por ejemplo, SELECT * FROM trabajos)
    cursor.execute("SELECT * FROM trabajos")
    
    # Obtén los resultados de la consulta (por ejemplo, fetchall() para obtener todos los registros)
    trabajos = cursor.fetchall()
    
    # No olvides cerrar el cursor después de usarlo
    cursor.close()
    return render_template('sitio/trabajos.html', trabajos=trabajos)

@app.route('/nosotros')
def nosotros():
    return render_template('sitio/nosotros.html')

@app.route('/contacto')
def contacto():
    return render_template('sitio/contacto.html')

@app.route('/admin/')
def admin_index():
        if not 'login' in session:
            return redirect("/admin/login")
        return render_template('admin/index.html')

@app.route('/admin/login')
def admin_login():
    return render_template('admin/login.html')

@app.route('/admin/login', methods=['POST'])
def admin_login_post():
    _usuario=request.form['txtUsuario']
    _password=request.form['txtPassword']

    if _usuario=="nicoleandreac" and _password=="19038390":
        session["login"]=True
        session["usuario"]="Administrador"
        return redirect("/admin")
    

    return render_template("admin/login.html", mensaje="Acceso denegado")

@app.route('/admin/cerrar')
def admin_login_cerrar():
    session.clear
    return redirect('/admin/login')

@app.route('/admin/trabajos')
def admin_trabajos():

    if not 'login' in session:
        return redirect("/admin/login")
    

    # Obtén un cursor para interactuar con la base de datos
    cursor = mysql.connection.cursor()
    
    # Ejecuta una consulta (por ejemplo, SELECT * FROM trabajos)
    cursor.execute("SELECT * FROM trabajos")
    
    # Obtén los resultados de la consulta (por ejemplo, fetchall() para obtener todos los registros)
    trabajos = cursor.fetchall()
    
    # No olvides cerrar el cursor después de usarlo
    cursor.close()
    return render_template("admin/trabajos.html", trabajos=trabajos)

@app.route('/admin/nosotros')
def admin_nosotros():
    return render_template("admin/nosotros.html")

@app.route('/admin/contacto')
def admin_contacto():
    return render_template("admin/contacto.html")

@app.route('/admin/trabajos/guardar', methods=['POST'])
def admin_trabajos_guardar():

    if not 'login' in session:
        return redirect("/admin/login")

    _nombre=request.form['txtNombre']
    _url=request.form['txtDes']
    _archivo=request.files['txtImagen']

    tiempo= datetime.now()
    horaActual=tiempo.strftime('%Y%H%M%S')

    if _archivo.filename!="":
        nuevoNombre=horaActual+"_"+_archivo.filename
        _archivo.save("templates/sitio/img/"+nuevoNombre)

    # Utiliza placeholders en la consulta SQL para evitar SQL injection
    sql = "INSERT INTO trabajos (nombre, imagen, descripcion) VALUES (%s, %s, %s)"
    valores = (_nombre, nuevoNombre, _url)  # Cambia 'nombre_archivo.jpg' por el nombre de archivo adecuado

    # Obtén un cursor para interactuar con la base de datos
    cursor = mysql.connection.cursor()
    
    # Ejecuta la consulta con los valores
    cursor.execute(sql, valores)
    
    # Realiza una confirmación para guardar los cambios en la base de datos
    mysql.connection.commit()
    
    # No olvides cerrar el cursor después de usarlo
    cursor.close()

    return redirect('/admin/trabajos')

@app.route('/admin/trabajos/borrar', methods=['POST'])
def admin_trabajos_borrar():

    if not 'login' in session:
        return redirect("/admin/login")

    _id=request.form['txtID']
    print(_id)

    cursor = mysql.connection.cursor()
    
    # Ejecuta una consulta (por ejemplo, SELECT * FROM trabajos)
    cursor.execute("SELECT imagen FROM trabajos WHERE id=%s", (_id,))

    
    # Obtén los resultados de la consulta (por ejemplo, fetchall() para obtener todos los registros)
    trabajo = cursor.fetchall()

    if os.path.exists("templates/sitio/img/"+str(trabajo[0][0])):
        os.unlink("templates/sitio/img/"+str(trabajo[0][0]))
    
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM trabajos WHERE id=%s",(_id,))
    mysql.connection.commit()

    # No olvides cerrar el cursor después de usarlo
    cursor.close()

    return redirect('/admin/trabajos')

if __name__ == '__main__':
    app.run(debug=True)