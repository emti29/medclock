from medclock import db


class Paciente(db.Model):
    __tablename__ = 'pacientes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    usuario = db.Column(db.String(50))
    contraseña = db.Column(db.Text)
    author = db.Column(db.Integer, db.ForeignKey('medicos.id'))
    rut = db.Column(db.String(12), unique=True)


    def __init__(self, nombre, usuario, contraseña, rut, author) -> None:
        self.nombre = nombre
        self.usuario = usuario
        self.contraseña = contraseña
        self.rut = rut
        self.author = author

    def __repr__(self) -> str:
        return f'Paciente: {self.usuario}'