from medclock import db


class Medico(db.Model):
    __tablename__ = 'medicos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    username = db.Column(db.String(100))
    password = db.Column(db.Text)


    def __init__(self, nombre, username, password) -> None:
        self.nombre = nombre
        self.username = username
        self.password = password

    def __repr__(self) -> str:
        return f'Medico: {self.username}'
    
