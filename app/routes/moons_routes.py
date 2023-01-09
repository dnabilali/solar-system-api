from app import db
from flask import Blueprint, jsonify, abort, make_response, request
from ..models.moon import Moon
from app.routes.planets_routes import validate_model
moons_bp = Blueprint("moons", __name__, url_prefix = "/moons")

# ~~~~~~ Planet Routes ~~~~~
@moons_bp.route("", methods=["GET"])
def display_all_moons():
    moons = Moon.query.all()
    # fill http response
    response_moons = []
    for moon in moons:
        response_moons.append(moon.to_dict())  
    return jsonify(response_moons)

@moons_bp.route("/<moon_id>",methods=["GET"])
def display_moon(moon_id):
    moon = validate_model(Moon, moon_id)
    return moon.to_dict()


