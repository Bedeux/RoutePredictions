from posixpath import split
import requests
import json
import csv
import geopy.distance
from GeoJsonViewer import GeoJsonViewer


def get_geojson(start_coordonates, end_coordonates):
    waypoints = start_coordonates + "|" + end_coordonates
    querystring = {"stroke": "#ff0000", "stroke-width": 10, "stroke-opacity": 1, "waypoints": waypoints,
                   "mode": "drive", "apiKey": "eb2439e34ab84367ac3f1eb6cad64641"}
    response = requests.request("GET", "https://api.geoapify.com/v1/routing", params=querystring)
    return response.json()

def create_geojson_file_from_routes(routes, file_name="final_path.json"):
    jsonFile = open("./geojson maps/initial_geojsonfile.json", "r")  # Open the JSON file for reading
    initial_data = json.load(jsonFile)  # Read the JSON into the buffer

    initial_data['features'][0]['geometry']['coordinates'] = routes
    jsonFile.close()  # Close the JSON file

    """  
    jsonFile = open(file_name, "w+")
    jsonFile.write(json.dumps(initial_data))
    jsonFile.close()
    """

    viewer = GeoJsonViewer(json.dumps(initial_data),initial_location=initial_coordinates)
    viewer.run_flask_app()


# TODO Optimize function
def get_biggest_french_cities(csv_reader,number_of_cities):
    all_cities = []
    for row in csv_reader:
        all_cities.append(row)
        
    return all_cities[1:number_of_cities+1]

def get_every_n_value(list, n):
    result = []
    for i in range(0, len(list), n):
        result.append(list[i])
    return result

def remove_elements_before_in_list(list,element):
    if element in list:
        index = list.index(element)
        list = list[index+1:]
    return list


def create_unique_route(routes, route):
    for existing_route in routes:
        existing_route = get_every_n_value(existing_route,50)
        index_point = 0
        same_route = True
        while same_route or index_point==len(existing_route)-1:
            same_route = False
            for point in route :
                if geopy.distance.geodesic(point, existing_route[index_point]).km<1:
                    same_route=True
                    route = remove_elements_before_in_list(route,point)
            index_point = index_point+1
    return route


file = open('villes_final.csv')
villes = get_biggest_french_cities(csv.reader(file),5)
start_coordonates = "45.8317361,1.2624837" # "46.3207657,-0.4594615"
initial_coordinates = (45.8317361,1.2624837)
destinations = []
for ville in villes:
    destination = ville[4] + "," + ville[3]
    destinations.append(destination)

itineraires = []
i = 0
for dest in destinations:
    i = i + 1
    print(i)
    loc = dest.split(',')
    loc[0] = format(float(loc[0]), '.14f')
    loc[1] = format(float(loc[1]), '.14f')
    destinat = loc[0] + ',' + loc[1]
    data = get_geojson(start_coordonates, dest)
    itineraire = data['features'][0]['geometry']['coordinates'][0]
    print(len(itineraire))
    # itineraire = create_unique_route(itineraires,itineraire)
    # print(len(itineraire))
    itineraires.append(itineraire)

create_geojson_file_from_routes(itineraires)

        
"""
data = get_geojson(start_coordonates,end_coordonates)
itineraire = data['features'][0]['geometry']['coordinates'][0]
itineraires.append(itineraire)

# TODO Check if start and end is in the path
# Compter le trajet a partir de la fin
for ville in villes:
    data = get_geojson(start_coordonates,ville)
    itineraire = data['features'][0]['geometry']['coordinates'][0]
    itineraires.append(itineraire)
"""


"""
data = get_geojson(start_coordonates,larochelle)
itineraire = data['features'][0]['geometry']['coordinates'][0]

data = get_geojson(start_coordonates,niort)
itineraire2 = data['features'][0]['geometry']['coordinates'][0]
# print(itineraire)

"""



go_by_coordonates = (44.77840710385228, -0.5548664427742672)

# print(geopy.distance.geodesic(coords_1, coords_2).km)

def is_on_the_way(itineraire):
    for location in itineraire:
        real_location = (location[1],location[0])
        if geopy.distance.geodesic(go_by_coordonates, real_location).km < 10:
            return True
    return False