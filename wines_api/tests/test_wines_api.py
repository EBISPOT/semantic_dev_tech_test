import pytest
import requests

url = 'http://127.0.0.1:5000'

def test_get_all_varieties():
    r = requests.get(url+'/all_varieties')
    data = r.json()
    response = data['data']

    assert r.status_code == 200

    assert response[0]['varietal'] == "Zinfandel"
    assert response[1]['varietal'] == "Chardonnay"
    assert response[2]['varietal'] == "Sangiovesse"
    assert response[3]['varietal'] == "Malvasia_bianca"
    assert response[4]['varietal'] == "Canaiolo"
    assert response[5]['varietal'] == "Nebbiolo"

def test_get_all_growing_grape_regions():
    r = requests.get(url+'/all_grape_regions')
    data = r.json()
    response = data['data']

    assert r.status_code == 200

    assert response[0]['grape'] == "Chardonnay"
    assert response[0]['region'] == "Chablis"
    assert response[0]['region_of'] == "Burgundy"

    assert response[1]['grape'] == "Chardonnay"
    assert response[1]['region'] == "Chablis"
    assert response[1]['region_of'] == "France"

    assert response[2]['grape'] == "Nebbiolo"
    assert response[2]['region'] == "Piedmont"
    assert response[2]['region_of'] == "Italy"

    assert response[3]['grape'] == "Sangiovesse"
    assert response[3]['region'] == "Chianti"
    assert response[3]['region_of'] == "Italy"

    assert response[4]['grape'] == "Malvasia_bianca"
    assert response[4]['region'] == "Chianti"
    assert response[4]['region_of'] == "Italy"

    assert response[5]['grape'] == "Canaiolo"
    assert response[5]['region'] == "Chianti"
    assert response[5]['region_of'] == "Italy"
   
def test_get_all_wine_types():
    r = requests.get(url+'/wines/all')
    data = r.json()
    response = data['data']

    assert r.status_code == 200

    assert response[0]['wine'] == "Italian_wine"
    assert response[1]['wine'] == "Barbaresco"
    assert response[2]['wine'] == "Chianti_wine"
    assert response[3]['wine'] == "Barolo"
    assert response[4]['wine'] == "red_wine"
    assert response[5]['wine'] == "white_wine"
    assert response[6]['wine'] == "Chablis_wine"
    assert response[7]['wine'] == "French_wine"

def test_search_red_wines():
    r = requests.get(url+'/wines?colour=red')
    data = r.json()
    response = data['data']
    
    assert r.status_code == 200

    assert response[0]['wine'] == "Chianti_wine"
    assert response[1]['wine'] == "Barolo"
    assert response[2]['wine'] == "Barbaresco"

def test_search_red_and_italian_wines():
    r = requests.get(url+'/wines?colour=red&region=Italy')
    data = r.json()
    response = data['data']
    
    assert r.status_code == 200

    assert response[0]['wine'] == "Chianti_wine"
    assert response[1]['wine'] == "Barolo"
    assert response[2]['wine'] == "Barbaresco"

def test_search_white_and_french_wines():
    r = requests.get(url+'/wines?colour=white&region=France')
    data = r.json()
    response = data['data']
    
    assert r.status_code == 200

    assert response[0]['wine'] == "Chablis_wine"

def test_search_red_nebbiolo_and_italian_wines():
    r = requests.get(url+'/wines?colour=red&varietal=Nebbiolo&region=Italy')
    data = r.json()
    response = data['data']
    
    assert r.status_code == 200

    assert response[0]['wine'] == "Barolo"

def test_search_rose_wines():
    r = requests.get(url+'/wines?colour=rose')
    data = r.json()
        
    assert r.status_code == 404



    




