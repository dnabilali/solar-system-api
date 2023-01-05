from app import db
from flask import Blueprint, jsonify, abort, make_response, request
from ..models.moon import Moon

moons_bp = Blueprint("moons", __name__, url_prefix = "/moons")

# Add nested routes for the endpoint `/planets/<planet_id>/moons` to:
# Create a Moon and link it to an existing Planet record
# Fetch all Moons that a Planet is associated with
