def test_get_all_planets_with_empty_db_returns_empty_list(client):
    response = client.get("/planets")
    
    assert response.status_code == 200
    assert response.get_json() == []


def test_get_planet_by_id_with_empty_db_returns_404(client):
    response = client.get("/planets/1")
    
    assert response.status_code == 404
    assert response.get_json() == {"message" : "1 not found"}


def test_update_planet_successfully(client, two_saved_planets):
    test_data = {"name" : "earth", 
            "description" : "terrestrial, full of life",     
            "mass" : 5.97e24}
    response = client.put("planets/1", json=test_data)
    
    assert response.status_code == 200
    assert response.get_json() == {"message": "planet #1 Updated Successfully"}


def test_get_planet_by_invalid_id_returns_400(client, two_saved_planets):
    response = client.get("/planets/earth")
    
    assert response.status_code == 400
    assert response.get_json() == {"message": "earth is an invalid planet id"}