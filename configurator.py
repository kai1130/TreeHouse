import json
import googlemaps

import pydeck as pdk
import haversine as hs

from datetime import datetime
from credentials import gmaps_api

gmaps = googlemaps.Client(key=gmaps_api)

class Configurator:

    def __init__(self, options):
        self.car = None
        self.kgm = 0
        self.mat = {}
        self.nodes = []
        self.edges = []
        self.options = options

    def set_name(self, name):
        self.name = name

    def set_location(self, location):
        self.addr = location
        self.user_lat, self.user_lng = self.get_coords(location)

    def select_model(self, model):
        self.car = json.loads(json.dumps(
            self.options['Model'][model]
        ))

    def select_wheels(self, wheels):
        self.car['options']['wheels'] = json.loads(json.dumps(
            self.options['Wheel'][wheels]
        ))
        
    def select_seats(self, seats):
        self.car['options']['seats'] = json.loads(json.dumps(
            self.options['Seat'][seats]
        ))

    def __get_coords(self, address):

        response = gmaps.geocode(address)

        return response[0]['geometry']['location']['lat'], response[0]['geometry']['location']['lng']  

    def set_coords(self, parent=None):
        
        if parent is None:
            parent = self.car
        
        parent['lat'], parent['lng'] = self.__get_coords(parent['addr'])
        
        if 'options' in parent:
            for option, child in parent['options'].items():
                self.set_coords(child)
                
    def sum_mat(self, parent=None):
        
        if parent is None:
            parent = self.car
            
        if 'materials' in parent:
            for material, amt in parent['materials'].items():
                if material not in self.mat:
                    self.mat[material] = 0
                self.mat[material] += amt
            
        if 'options' in parent:
            for option, child in parent['options'].items():
                self.sum_mat(child)

    def get_cumul_weight(self, parent=None):
        
        if parent is None:
            parent = self.car
            self.edges = []

        if 'cumul_weight' not in parent:
            parent['cumul_weight'] = parent['weight']

        if 'options' in parent:
            for option, child in parent['options'].items():
                parent['cumul_weight'] += child['weight']
                self.get_cumul_weight(child)
                
    def get_nodes(self, parent=None):
        
        if parent is None:
            parent = self.car

            self.nodes.append({
                'name': self.name,
                'addr': self.addr,
                'lat': self.user_lat,
                'lng': self.user_lng
            })
        
        self.nodes.append({k: parent[k] for k in set(list(parent.keys())) - set(['options'])})

        if 'options' in parent:
            for option, child in parent['options'].items():
                self.get_nodes(child)
                
    def calc_edges(self, parent=None):
        
        if parent is None:
            parent = self.car
            
        if 'options' in parent:
            for option, child in parent['options'].items():

                parent_coords = [parent['lng'], parent['lat']]
                child_coords = [child['lng'], child['lat']]

                self.edges.append({
                    'start': parent_coords,
                    'end': child_coords,
                    'name': f"{child['name']} -> {parent['name']}",
                    'cumul_weight': child['cumul_weight'],
                    'distance': hs.haversine(
                        parent_coords[::-1],
                        child_coords[::-1])
                })

            self.calc_edges(child)

    def calc_user_edge(self):

        parent = self.car

        user_coords = [self.user_lng, self.user_lat]
        parent_coords = [parent['lng'], parent['lat']]

        self.edges.append({
            'start': user_coords,
            'end': parent_coords,
            'name': f"{parent['name']} -> You :)",
            'cumul_weight': parent['cumul_weight'],
            'distance': hs.haversine(
                        user_coords[::-1],
                        parent_coords[::-1])
        })
            
    def get_kgm(self):
        
        for edge in self.edges:
            self.kgm += edge['cumul_weight'] * edge['distance']

    def plot(self):
        
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=self.nodes,
            get_position="[lng, lat]",
            get_color=[255, 0, 0],  # Set color to red
            radius_scale=1,
            radius_min_pixels=2,
            radius_max_pixels=10,
            get_radius=100000,  # Set radius to 100 pixels
            pickable=True,
        )

        line_layer = pdk.Layer(
            "LineLayer",
            self.edges,
            get_source_position="start",
            get_target_position="end",
            get_color=[255, 255, 255],
            get_width=3,
            highlight_color=[255, 255, 255],
            picking_radius=5,
            auto_highlight=True,
            pickable=True,
        )

        view = pdk.ViewState(latitude=0, longitude=0, min_zoom=0.5, zoom=1, max_zoom=3)

        deck = pdk.Deck(layers=[line_layer, layer], initial_view_state=view)
        
        return deck
