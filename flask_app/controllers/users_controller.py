from flask import render_template, redirect, session, request, flash, jsonify #importaciones de módulos de flask
from flask_app import app

#Importando el Modelo de User
from flask_app.models.users import User

#Importamos el modelo de Recetas
from flask_app.models.appointments import Appointment

#Importando BCrypt (encriptar)
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app) #inicializando instancia de Bcrypt

@app.route('/')
def index():
    return render_template('index.html')

#Creando una ruta para /register
@app.route('/register', methods=['POST'])
def register():
    #request.form = {
    #   "first_name": "Elena",
    #   "last_name": "De Troya",
    #   "email": "elena@cd.com",
    #   "password": "123456",
    #}
    if not User.valida_usuario(request.form):
        return redirect('/')

    pwd = bcrypt.generate_password_hash(request.form['password']) #Me encripta el password

    formulario = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pwd
    }

    id = User.save(formulario) #Guardando a mi usuario y recibo el ID del nuevo registro

    session['usuario_id'] = id #Guardando en sesion el identificador

    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    #Verificar que el email EXISTA
    #request.form RECIBIMOS DE HTML
    #request.form = {email: elena@cd.com, password: 123}
    user = User.get_by_email(request.form) #Recibiendo una instancia de usuario o Falso

    if not user:
        #flash('E-mail no encontrado', 'login')
        #return redirect('/')
        return jsonify(message="E-mail no encontrado")


    if not bcrypt.check_password_hash(user.password, request.form['password']):
        #flash('Password incorrecto', 'login')
        #return redirect('/')
        return jsonify(message="Password incorrecto")

    session['user_id'] = user.id

    #return redirect('/dashboard')
    return jsonify(message="correcto")

@app.route('/dashboard')
def dashboard():
    if 'usuario_id' not in session:
        return redirect('/')

    formulario = {
        "id": session['usuario_id']
    }

    user = User.get_by_id(formulario) #Usuario que inicio sesión

    appointments = Appointment.get_all() 
    
    return render_template('dashboard.html', user=user, appointments=appointments)

@app.route('/logout')
def logout():
    session.clear() #Elimine la sesión
    return redirect('/')