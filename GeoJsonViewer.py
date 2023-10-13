import geopandas as gpd
import folium
import json
from io import BytesIO
from flask import Flask
import webbrowser
from threading import Timer



class GeoJsonViewer:
    def __init__(self, geojson_data, initial_location=(48.8588443, 2.2943506), initial_zoom=7):
        self.geojson_data = geojson_data
        self.initial_location = initial_location
        self.initial_zoom = initial_zoom
        self.m = None

    def create_map(self):
        # Convertir la chaîne JSON en bytes
        geojson_bytes = bytes(self.geojson_data, 'utf-8')

        # Charger les données GeoJSON à partir des bytes
        gdf = gpd.read_file(BytesIO(geojson_bytes))

        # Créer une carte Folium
        self.m = folium.Map(location=self.initial_location, zoom_start=self.initial_zoom)

        # Ajouter les données GeoJSON à la carte Folium
        folium.GeoJson(gdf).add_to(self.m)

        first_coord = [self.initial_location[0], self.initial_location[1]]
        folium.Marker(location=first_coord, tooltip='Première coordonnée',icon=folium.Icon(color='green')).add_to(self.m)
    

    def open_browser(self):
      webbrowser.open_new("http://127.0.0.1:5000")

    def run_flask_app(self):
        app = Flask(__name__)

        @app.route('/')
        def show_map():
            self.create_map()  # Exécutez la carte

            # Affichez la carte dans une fenêtre Flask
            return self.m.get_root().render()
        Timer(0, self.open_browser).start()
        app.run(port=5000)


