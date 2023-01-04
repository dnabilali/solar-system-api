def test_get_all_planets_with_empty_db_returns_empty_list(client):
    response = client.get("/planets")
    
    assert response.status_code == 200
    assert response.get_json() == []

def test_get_one_planet(client, two_saved_planets):
    # Act
    response = client.get("/planets/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
            "id" : 1,
            "name": "Earth",
            "description": "rocky, terrestrial, full of life",
            "mass": 5.972e24
    }

def test_create_one_planet(client):
    #Act
    response = client.post("/planets", json = {
         "name": "Neptune", 
         "description": "thick, windy", 
         "mass":1.024e26
    })
    response_body = response.get_json()

    #Assert
    assert response.status_code == 201
    assert response_body == {"message":"planet has been created successfully"}

def test_create_one_planet_missing_mass_return_400(client):
    #Act
    response = client.post("/planets", json = {
         "name": "Neptune", 
         "description": "thick, windy"
    })
    response_body = response.get_json()
    #Assert
    assert response.status_code == 400
    assert response_body == {"message" : \
                "Failed to create a planet because the name and/or description \
                and/or mass are missing"}