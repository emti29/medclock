from medclock import db
from datetime import datetime

class Medicamentos(db.Model):
    __tablename__ = 'medicamentos'
    id = db.Column(db.Integer, primary_key=True)
    id_medico = db.Column(db.Integer, db.ForeignKey('medicos.id'), nullable=False)
    nombre_medicamento = db.Column(db.String(50))
    descripcion = db.Column(db.Text)
    rut = db.Column(db.String(12), db.ForeignKey('pacientes.rut'), nullable=False)
    hora = db.Column(db.Time)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, id_medico, nombre_medicamento, descripcion, rut, hora, created):
        self.id_medico = id_medico
        self.nombre_medicamento = nombre_medicamento
        self.descripcion = descripcion
        self.rut = rut
        self.hora = hora
        self.created = created

    def __repr__(self) -> str:
        return f'Medicamento: {self.nombre_medicamento}'