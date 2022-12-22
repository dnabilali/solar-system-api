from app import db

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    mass = db.Column(db.String)

# class Planet:
#     def __init__(self, id, name, description, mass):
#         self.id = id
#         self.name = name
#         self.description = description
#         self.mass = mass

# planets = [Planet(1, "Neptune", "thick, windy", 1.024e26 ),
#            Planet(2, "Mars", "dusty, cold desert",6.39e23),
#            Planet(3, "Earth", "rocky, terrestrial, full of life",5.972e24)
#            ]
