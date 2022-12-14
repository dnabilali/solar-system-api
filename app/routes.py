from flask import Blueprint, jsonify
from .model.planet import planets


planets_bp = Blueprint("planets", __name__, url_prefix = "/planets")

@planets_bp.route("",methods= ["GET"])
def display_planets():
    response_planets = []
    for planet in planets:
        response_planets.append({
            "id": planet.id,
            "name": planet.name,
            "description": planet.description,
            "mass": planet.mass
        })
        
    return jsonify(response_planets)