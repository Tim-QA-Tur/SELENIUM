import requests
import pytest

URL = 'https://api.pokemonbattle.ru/v2'
TOKEN = 'cf05f8742a6e0c238c8704d40014512d'
HEADER = {'Content-Type':'application/json', 'trainer_token' :TOKEN}
TRAINER_ID = '28363'

def test_status_code():
    response = requests.get(url = f'{URL}/pokemons', params = {'trainer_id' :TRAINER_ID})
    assert response.status_code == 200
    

def test_pokemon_name():
    response_get_pok_name = requests.get(url = f'{URL}/pokemons', params = {'trainer_id' :TRAINER_ID})
    assert response_get_pok_name.json()["data"][0]["name"] == 'Chuichui'

def test_trainer_name():
    response_get_name = requests.get(url = f'{URL}/me', headers=HEADER)
    assert response_get_name.json()["data"][0]["trainer_name"] == "Барбос"

@pytest.mark.parametrize('key, value', [('name', 'Chuichui'), ('trainer_id', TRAINER_ID), ('id', '288391')])
def test_parametrize(key, value):
    response_parametrize = requests.get(url = f'{URL}/pokemons', params = {'trainer_id' : TRAINER_ID})
    assert response_parametrize.json()["data"][0][key] == value
