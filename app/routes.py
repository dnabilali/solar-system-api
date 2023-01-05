from app import db
from flask import Blueprint, jsonify, abort, make_response, request
from .models.planet import Planet

planets_bp = Blueprint("planets", __name__, url_prefix = "/planets")


# ~~~~~~ Validate functions ~~~~~
def validate_planet(cls, planet_id):
    """
    Checks if planet id is valid and returns error messages for invalid inputs
    :params:
    - planet_id (int)
    :returns:
    - planet (object) if valid planet id valid
    """
    try:
        planet_id = int(planet_id)
    except:
        # handling invalid planet id type
        abort(make_response({"message": f"{cls.__name__} {planet_id} is an invalid planet id"}, 400))
    # return planet data if id in db
    planet = cls.query.get(planet_id)
    # handle nonexistant planet id
    if not planet:
        abort(make_response({"message": f"{cls.__name__} {planet_id} not found"}, 404))
    return planet

def validate_post_request(cls, request):
    """
    Checks if post request contains all required planet data
    :returns:
    - request_body (if all requirements present)
    """
    request_body = request.get_json()
    requirements = ["name", "description", "mass"]
    for req in request_body:
        if req not in requirements:
            abort(make_response({
                f"Failed to create {cls.__name__} because {req} is missing"
            }, 400))
    return request_body

def process_kwargs(queries):
    """
    Separate kwargs from HTTP request into separate dicts based on SQLAlchemy query method
    :params:
    - queries (dict)
    :returns:
    - attrs (dict): planet class attributes kwargs for filter_by
        ** name, description, mass
    - orderby (dict): method kwargs for order_by
        ** sort_mass, sort_name
    - sels (dict): selected number of results for limit
    """
    planet_attrs = Planet.get_all_attrs()
    order_methods = ["sort", "desc"]
    attrs = {}
    orderby = {}
    sels = {}
    for kwarg in queries:
        if kwarg in planet_attrs:
            attrs[kwarg] = queries[kwarg]
        elif kwarg in order_methods:
            orderby[kwarg] = queries[kwarg]
        elif kwarg == "limit":
            sels[kwarg] = queries[kwarg]
        else:
            abort(make_response(
                {"message" : f"{kwarg} is an invalid query"}, 400
            ))
    return attrs, orderby, sels

@planets_bp.route("",methods= ["GET"])
def display_all_planets():
    # collect query & parse kwargs
    planet_query = Planet.query
    attrs, orderby, sels = process_kwargs(request.args.to_dict())
    if attrs:
        #  filter by attribute kwargs e.g name=Earth
        planet_query = planet_query.filter_by(**attrs)
    if "sort" in orderby:
        # sort by given attribute e.g.sort=mass
        clause = getattr(Planet, orderby["sort"])
        if "desc" in orderby:
            # sort in descending order e.g.desc=True
            planet_query = planet_query.order_by(clause.desc())
        else:
            # default is asc=True
            planet_query = planet_query.order_by(clause.asc())
    if sels:
        # limit selection of planets to view
        planet_query = planet_query.limit(**sels)
    # perform query
    planets = planet_query.all()
    # fill http response
    response_planets = []
    for planet in planets:
        response_planets.append(planet.to_dict())  
    return jsonify(response_planets)


# ~~~~~~ Single planet endpoint ~~~~~~
@planets_bp.route("/<planet_id>",methods=["GET"])
def display_planet(planet_id):
    valid_planet = validate_planet(Planet, planet_id)
    return valid_planet.to_dict()

@planets_bp.route("", methods=["POST"])
def create_planet():
    request_body = validate_post_request(Planet, request)
    new_planet = Planet.from_dict(request_body)
    db.session.add(new_planet)
    db.session.commit()
    return make_response({"message":"planet has been created successfully"}, 201)

@planets_bp.route("/<planet_id>", methods=["PUT"])
def update_planet(planet_id):
    request_body = request.get_json()
    planet = validate_planet(Planet, planet_id)
    planet.name = request_body["name"] if "name" in request_body else planet.name 
    planet.description = request_body["description"] if "description" in request_body else planet.description
    planet.mass = request_body["mass"] if "mass" in request_body else planet.mass
    db.session.commit()
    return make_response(
        {"message": f"planet #{planet_id} Updated Successfully"}, 200
    )


@planets_bp.route("/<planet_id>", methods=["DELETE"])
def delete_planet(planet_id):
    planet = validate_planet(Planet, planet_id)
    db.session.delete(planet)
    db.session.commit()
    return make_response(
        {"message": f"planet #{planet_id} has been deleted successfully"}, 200
    )
