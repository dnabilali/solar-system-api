from app import db
from flask import Blueprint, jsonify, abort, make_response, request
from .models.planet import Planet


planets_bp = Blueprint("planets", __name__, url_prefix = "/planets")

# ~~~~~~ Handle planet id errors ~~~~~
# FUTURE IDEAS: Create separate helper function module or add as class method
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
    
    # return planet data if id in db
    planet = Planet.query.get(planet_id)

    # handle nonexistant planet id
    if not planet:
        abort(make_response({"message": f"{planet_id} not found"}, 404))

    return planet



@planets_bp.route("",methods= ["GET"])
def display_all_planets():
    response_planets = []
    planets = Planet.query.all()
    for planet in planets:
        response_planets.append({
            "id": planet.id,
            "name": planet.name,
            "description": planet.description,
            "mass": planet.mass
        })
        
    return jsonify(response_planets)


# ~~~~~~ Single planet endpoint ~~~~~~
@planets_bp.route("/<planet_id>",methods=["GET"])
def display_planet(planet_id):
    valid_planet = validate_id(planet_id)
    return {
        "id": valid_planet.id,
        "name": valid_planet.name,
        "description": valid_planet.description,
        "mass": valid_planet.mass,
    }


@planets_bp.route("", methods=["POST"])
def create_planet():
    request_body = request.get_json()

    if "name" not in request_body or "description" not in request_body \
        or "mass" not in request_body:
        abort(make_response({"message" : \
            "Failed to create a planet because the name and/or description \
            and/or mass are missing"}, 400))

    new_planet = Planet(
        name=request_body["name"],
        description=request_body["description"],
        mass=request_body["mass"])

    db.session.add(new_planet)
    db.session.commit()

    return make_response({"message":"planet has been created successfully"}, 201)

@planets_bp.route("/<planet_id>", methods=["PUT"])
def update_planet(planet_id):
    request_body = request.get_json()
    planet = validate_id(planet_id)
    planet.name = request_body["name"] if "name" in request_body else planet.name 
    planet.description = request_body["description"] if "description" in request_body else planet.description
    planet.mass = request_body["mass"] if "mass" in request_body else planet.mass
    db.session.commit()
    return make_response(
        {"message": f"planet #{planet_id} Updated Successfully"}, 200
    )

