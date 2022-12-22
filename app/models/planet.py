from app import db

class Planet(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    mass = db.Column(db.Float, nullable=False)

# planets = [Planet(1, "Neptune", "thick, windy", 1.024e26 ),
#            Planet(2, "Mars", "dusty, cold desert",6.39e23),
#            Planet(3, "Earth", "rocky, terrestrial, full of life",5.972e24)
#            ]
