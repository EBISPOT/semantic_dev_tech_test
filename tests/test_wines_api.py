import pytest
import json
from api.winesapi import app

@pytest.fixture
def client():
    return app.test_client()
       

def test_get_all_varietals(client):
    expected = [
        {
          "varietal": "Zinfandel"
        },
        {
          "varietal": "Chardonnay"
        },
        {
          "varietal": "Sangiovesse"
        },
        {
          "varietal": "Malvasia_bianca"
        },
        {
          "varietal": "Canaiolo"
        },
        {
          "varietal": "Nebbiolo"
        }
    ]
    r = client.get('/all_varietals')

    data = r.get_json()
    response = data['data']

    assert r.status_code == 200
    assert len(response) == 6
    assert [i for i in response if i not in expected] == []

def test_get_all_growing_grape_regions(client):
    expected = [
        {
          "grape": "Chardonnay",
          "region": "Chablis",
          "region_of": "Burgundy"
        },
        {
          "grape": "Chardonnay",
          "region": "Chablis",
          "region_of": "France"
        },
        {
          "grape": "Nebbiolo",
          "region": "Piedmont",
          "region_of": "Italy"
        },
        {
          "grape": "Sangiovesse",
          "region": "Chianti",
          "region_of": "Italy"
        },
        {
          "grape": "Malvasia_bianca",
          "region": "Chianti",
          "region_of": "Italy"
        },
        {
          "grape": "Canaiolo",
          "region": "Chianti",
          "region_of": "Italy"
        }
      ]
    r = client.get('/all_grape_regions')
    data = r.get_json()
    response = data['data']

    assert r.status_code == 200
    assert len(response) == 6
    assert [i for i in response if i not in expected] == []

   
def test_get_all_wine_types(client):
    expected = [
        {
          "wine": "Italian_wine"
        },
        {
          "wine": "Barbaresco"
        },
        {
          "wine": "Chianti_wine"
        },
        {
          "wine": "Barolo"
        },
        {
          "wine": "red_wine"
        },
        {
          "wine": "white_wine"
        },
        {
          "wine": "Chablis_wine"
        },
        {
          "wine": "French_wine"
        }
    ]

    r = client.get('/wines/all')
    data = r.get_json()
    response = data['data']

    assert r.status_code == 200
    assert len(response) == 8
    assert [i for i in response if i not in expected] == []

def test_search_red_wines(client):
    expected = [
        {
          "wine": "Chianti_wine"
        },
        {
          "wine": "Barolo"
        },
        {
          "wine": "Barbaresco"
        }
    ]
    r = client.get('/wines?colour=red')
    data = r.get_json()
    response = data['data']
    
    assert r.status_code == 200
    assert len(response) == 3
    assert [i for i in response if i not in expected] == []

def test_search_red_and_italian_wines(client):
    expected = [
        {
          "wine": "Chianti_wine"
        },
        {
          "wine": "Barolo"
        },
        {
          "wine": "Barbaresco"
        }
    ]
    r = client.get('/wines?colour=red&region=Italy')
    data = r.get_json()
    response = data['data']
    
    assert r.status_code == 200
    assert len(response) == 3
    assert [i for i in response if i not in expected] == []

def test_search_white_and_french_wines(client):
    r = client.get('/wines?colour=white&region=France')
    data = r.get_json()
    response = data['data']
    
    assert r.status_code == 200
    assert len(response) == 1
    assert response[0]['wine'] == "Chablis_wine"

def test_search_red_nebbiolo_and_italian_wines(client):
    expected = [
        {
          "wine": "Barolo"
        },
        {
          "wine": "Barbaresco"
        }
    ]
    r = client.get('/wines?colour=red&varietal=Nebbiolo&region=Italy')
    data = r.get_json()
    response = data['data']
    
    assert r.status_code == 200
    assert len(response) == 2
    assert [i for i in response if i not in expected] == []

def test_search_rose_wines(client):
    r = client.get('/wines?colour=rose')
    data = r.get_json()
    
    assert r.status_code == 404
    assert data.get('data') == None



    




