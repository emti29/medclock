import functools
from os import error
from flask import(
    render_template, Blueprint, flash, redirect, request, url_for, session, g)

from werkzeug.security import check_password_hash, generate_password_hash

from medclock.models.pacientes import Paciente 

from medclock import db

pacientes = Blueprint('pacientes', __name__, url_prefix='/pacientes')

#Registrar un paciente
@pacientes.route('/registro', methods=('GET','POST'))
def registro():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        usuario = request.form.get('usuario')
        contraseña = request.form.get('contraseña')
        rut = request.form.get('rut')
        author = request.form.get('author')

        paciente = Paciente(nombre, usuario, generate_password_hash(contraseña), rut, author)

        error = None
        if not usuario:
            error = 'Se requiere nombre de usuario'
        elif not contraseña:
            error = 'Se requiere contraseña'
        elif not nombre:
            error = 'Se requiere nombre'
        elif not rut:
            error = 'Se requiere rut'
        
        paciente_name = Paciente.query.filter_by(usuario = usuario).first()
        if paciente_name == None:
            db.session.add(paciente)
            db.session.commit()
            return redirect(url_for('blog.index'))
        else:
            error = f'El usuario {usuario} ya esta registrado'
        flash(error)
        
    return render_template('pacientes/registro.html')