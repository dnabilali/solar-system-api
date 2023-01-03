def test_get_all_planets_with_empty_db_returns_empty_list(client):
    response = client.get("/planets")
    
    assert response.status_code == 200
    assert response.get_json() == []