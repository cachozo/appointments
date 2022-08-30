from flask import render_template, redirect, session, request, flash, jsonify #importaciones de módulos de flask
from flask_app import app


from flask_app.models.users import User


from flask_app.models.appointments import Appointment


from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app) 

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

    pwd = bcrypt.generate_password_hash(request.form['password']) 

    formulario = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pwd
    }

    id = User.save(formulario) 

    session['user_id'] = id 

    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    
    user = User.get_by_email(request.form) 

    if not user:
        
        return jsonify(message="E-mail no encontrado")


    if not bcrypt.check_password_hash(user.password, request.form['password']):
        
        return jsonify(message="Password incorrecto")

    session['user_id'] = user.id

    
    return jsonify(message="correcto")

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')

    formulario = {
        "id": session['user_id']
    }

    user = User.get_by_id(formulario) 
    appointments = Appointment.get_all() 
    
    return render_template('dashboard.html', user=user, appointments=appointments)

@app.route('/logout')
def logout():
    session.clear() 
    return redirect('/')