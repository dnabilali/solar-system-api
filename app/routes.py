from flask import Blueprint, jsonify, abort, make_response
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

# ~~~~~~ Handle planet id errors ~~~~~
def validate_id(planet_id):
    """
    - check for valid id type and if exists
    - return planet object if valid planet id
    """
    try:
        planet_id_int = int(planet_id)
    except:
        # handling invalid planet id type
        abort(make_response({"message": f"{planet_id} is an invalid planet id"}, 400))
    
    # collect the planet data if valid id type
    for planet in planets:
        if planet.id == planet_id_int:
            return planet
    # handle nonexistant planet id
    abort(make_response({"message": f"{planet_id} not found"}, 404))


# ~~~~~~ Single planet endpoint ~~~~~~
@planets_bp.route("/<planet_id>",methods= ["GET"])
def display_planet(planet_id):
    valid_planet = validate_id(planet_id)
    return {
            "id": valid_planet.id,
            "name": valid_planet.name,
            "description": valid_planet.description,
            "mass": valid_planet.mass,
    }
