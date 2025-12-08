import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from app import app

def test_app_starts():
    assert app is not None
    assert app.name == 'app'


def test_home_page_loads():
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
        assert b'Pokemon Finder' in response.data or b'Pok' in response.data


def test_pokemon_page_pikachu():
    with app.test_client() as client:
        response = client.get('/pokemon/pikachu')
        assert response.status_code == 200
        assert b'Pikachu' in response.data


def test_pokemon_not_found():
    with app.test_client() as client:
        response = client.get('/pokemon/invalidpokemon676767')
        assert response.status_code == 404


def test_search_api():
    with app.test_client() as client:
        response = client.get('/api/search?q=pika')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)


def test_move_page_loads():
    with app.test_client() as client:
        response = client.get('/move/thunderbolt')
        assert response.status_code == 200
        assert b'Thunderbolt' in response.data or b'thunderbolt' in response.data


def test_ability_page_loads():
    with app.test_client() as client:
        response = client.get('/ability/static')
        assert response.status_code == 200
        assert b'Static' in response.data or b'static' in response.data


def test_health_endpoint():
    with app.test_client() as client:
        response = client.get('/health')
        assert response.status_code == 200

if __name__ == '__main__':
    print("Running smoke tests...")
    test_app_starts()
    print("✅ App starts")
    
    test_home_page_loads()
    print("✅ Home page loads")
    
    test_pokemon_page_pikachu()
    print("✅ Pokemon page loads")
    
    test_pokemon_not_found()
    print("✅ 404 handling works")
    
    test_search_api()
    print("✅ Search API works")
    
    test_move_page_loads()
    print("✅ Move page loads")
    
    test_ability_page_loads()
    print("✅ Ability page loads")
    
    test_health_endpoint()
    print("✅ Health endpoint works")
    
    print("\n✅ All smoke tests passed!")
