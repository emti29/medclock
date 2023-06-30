from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#Cargar configuraciones

app.config.from_object('config.DevelopmentConfig')
db = SQLAlchemy(app)


#Importar vistas

from medclock.views.auth import auth
app.register_blueprint(auth)

from medclock.views.pacientes import pacientes
app.register_blueprint(pacientes)

from medclock.views.blog import blog
app.register_blueprint(blog)
app.add_url_rule('/', endpoint='index')

with app.app_context():
    db.create_all()