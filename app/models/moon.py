from app import db

class Moon(db.Model):
    __tablename__ = 'moons'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    planet = db.relationship("Planet", back_populates="moons")
    planet_id = db.Column(db.Integer, db.ForeignKey("planets.id"))