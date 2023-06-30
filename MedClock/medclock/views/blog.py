from operator import pos
from flask import(
    render_template, Blueprint, flash, g, redirect, request, url_for
)

from sqlalchemy import exists

from werkzeug.exceptions import abort

from medclock.models.medicamentos import Medicamentos
from medclock.models.medico import Medico
from medclock.models.pacientes import Paciente
from medclock.views.auth import login_required

from medclock import db

blog = Blueprint('blog', __name__)

#Obtner un ususario
def get_medico(id):
    medico = Medico.query.get_or_404(id)
    return medico

@blog.route("/")
def index():
    medicamentos = Medicamentos.query.all()
    medicamentos = list(reversed(medicamentos))
    db.session.commit()
    return render_template('blog/index.html', medicamentos = medicamentos, get_medico=get_medico)

#Registrar un post 
@blog.route('/blog/create', methods=('GET','POST'))
@login_required
def create():
    if request.method == 'POST':
        nombre_medicamento = request.form.get('nombre_medicamento')
        descripcion = request.form.get('descripcion')
        rut = request.form.get('rut')
        hora = request.form.get('hora')
        created = request.form.get('created')


        medicamento = Medicamentos(g.medico.id, nombre_medicamento,descripcion, rut, hora, created)
        error = None
        if not nombre_medicamento:
            error = 'Se requiere un nombre'

        elif not rut:
            error ='Se requiere un rut'
        else:
    # Verificar si el RUT existe en otra tabla
            exists_in_otra_tabla = db.session.query(exists().where(Paciente.rut == rut)).scalar()
            if not exists_in_otra_tabla:
                error = 'El RUT no existe'

        if error is not None:
            flash(error)
        else:
            db.session.add(medicamento)
            db.session.commit()
            return redirect(url_for('blog.index'))
        
        flash(error)


        
        
    return render_template('blog/create.html')

def get_medicamento(id, check_author=True):
    medicamento = Medicamentos.query.get(id)

    if medicamento is None:
        abort(404, f'Id {id} de la publicación no existe.')

    if check_author and medicamento.author != g.medico.id:
        abort(404)
    
    return medicamento

#Update post 
@blog.route('/blog/update/<int:id>', methods=('GET','POST'))
@login_required
def update(id):

    medicamento = get_medicamento(id) 

    if request.method == 'POST':
        medicamento.title = request.form.get('title')
        medicamento.descripcion = request.form.get('descripcion')

        error = None
        if not medicamento.title:
            error = 'Se requiere un título'
        
        if error is not None:
            flash(error)
        else:
            db.session.add(medicamento)
            db.session.commit()
            return redirect(url_for('blog.index'))
        
        flash(error)
        
    return render_template('blog/update.html', medicamento=medicamento)

#Eliminar un post
@blog.route('/blog/delete/<int:id>')
@login_required
def delete(id):
    medicamento = get_medicamento(id)
    db.session.delete(medicamento)
    db.session.commit()

    return redirect(url_for('blog.index'))