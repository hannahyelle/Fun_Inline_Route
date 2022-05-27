# This file will get the map from OSMnx from user input address 
import osmnx as ox
import geopandas as gpd
import networkx as nx
#import myapp/manage.py as 
GOOGLE_API_KEY = "AIzaSyBCM1TPWaZzUXTtAnPbSZZey_C6Tf8Ubyc"


#Load map

#place names use Nominatim AP

def createDiGraph(place):
    #call search function (with user address captured from view)
    #https://osmnx.readthedocs.io/en/stable/osmnx.html#module-osmnx.geometries
    graphData = ox.graph_from_address(place,dist=1000,network_type='bike') #using bike as method as OSM data for bike paths would be similar to that of inline skating

    #add elevation data ontop of edges 
    #https://developers.google.com/maps/documentation/elevation/start#maps_http_elevation_locations-py
    graphData = ox.elevation.add_node_elevations_google(graphData, api_key=GOOGLE_API_KEY)
    graphData = ox.distance.add_edge_lengths(graphData)
    #graphData = ox.geometries_from_address('Boston',tags = {'Highway':['footway','pedestrian']},dist=10000)
    #print(type(graphData))
    #start = ox.get_nearest_nodes(graphData, latlong[0], latlong[1], return_dist=False)
    #print("start node", start)
    #ox.plot_graph(graphData)

    nc = ox.plot.get_node_colors_by_attr(graphData, "elevation", cmap="plasma")
    #fig, ax = ox.plot_graph(graphData, node_color=nc, node_size=5, edge_color="#333333", bgcolor="k")
    return graphData

    #send data to search function with user address as start
    #goal is length of path (half length of path -> turn around?)
        # What about circular paths?
        # Or an unknown start location 

