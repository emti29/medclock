import functools
from os import error
from flask import(
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from medclock.models.medico import Medico 

from medclock import db

auth = Blueprint('auth', __name__, url_prefix='/auth')

#Registrar un usuario 
@auth.route('/register', methods=('GET','POST'))
def register():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        username = request.form.get('username')
        password = request.form.get('password')

        medico = Medico(nombre, username, generate_password_hash(password))

        error = None
        if not username:
            error = 'Se requiere nombre de usuario'
        elif not password:
            error = 'Se requiere contraseña'
        elif not nombre:
            error = 'Se requiere nombre'
        
        user_name = Medico.query.filter_by(username = username).first()
        if user_name == None:
            db.session.add(medico)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            error = f'El usuario {username} ya esta registrado'
        flash(error)
        
    return render_template('auth/register.html')

#Iniciar Sesión
@auth.route('/login', methods=('GET','POST'))
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        error = None
        
        medico = Medico.query.filter_by(username = username).first()

        if medico == None:
            error = 'Nombre de usuario incorrecto'
        elif not check_password_hash(medico.password, password):
            error = 'Contraseña incorrecta'

        if error is None:
            session.clear()
            session['medico_id'] = medico.id
            return redirect(url_for('blog.index'))
        
        flash(error)
        
    return render_template('auth/login.html')


@auth.before_app_request
def load_logged_in_medico():
    medico_id = session.get('medico_id')

    if medico_id is None:
        g.medico = None
    else:
        g.medico = Medico.query.get_or_404(medico_id)

@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('blog.index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.medico is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view