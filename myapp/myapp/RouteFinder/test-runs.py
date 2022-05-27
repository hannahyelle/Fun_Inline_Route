#test runs of map.py and search.py with hard coded search variables 

# from map.py import * as map
# from search.py import * as search

#manually create classes and run them 
import search
import osmnx as ox

def test_boston():
    print("searching for route: dist: 100, place: 'Boston")
    place = 'Boston'
    graph_search = search.searchAgent(100,place)
    print(graph_search.solution)

test_boston()

