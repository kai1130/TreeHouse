import json
import googlemaps

import haversine as hs

from datetime import datetime
from credentials import gmaps_api

gmaps = googlemaps.Client(key=gmaps_api)

class GraphingService:

    def __init__(self,options):
        self.name = "Unnamed Car"
        self.car = None
        self.kgm = 0
        self.mat = {}
        self.nodes = []
        self.edges = []
        self.options = options

    def set_name(self, name):
        self.name = name

    def set_location(self, location=None):
        if location == None:
            location = self.car['addr']

        self.addr = location
        self.user_lat, self.user_lng = self.__get_coords(location)

    def select_model(self, model):
        self.car = self.options['Model'][model]
        

    def select_wheels(self, wheels):
        self.car['options']['wheels'] = self.options['Wheel'][wheels]

        
    def select_seats(self, seats):
        self.car['options']['seats'] = self.options['Seat'][seats]
        

    def select_option(self, option, choice):
        self.car['options'][option.lower()] = self.options[option][choice]
        

    def __get_coords(self, address):

        response = gmaps.geocode(address)
        print('response::  %s' % response)

        return (response[0]['geometry']['location']['lat'], response[0]['geometry']['location']['lng'])

    def set_coords(self, parent=None):
        
        if parent is None:
            parent = self.car
        
        coords = self.__get_coords(parent['addr'])

        print("PARENT:::", parent)

        parent['lat'] = coords[0]
        parent['lng'] = coords[1]
        
        if 'options' in parent:
            for option, child in parent['options'].items():
                if child != -1:
                    self.set_coords(child)
                else:
                    pass
                
    def sum_mat(self, parent=None):
        
        if parent is None:
            parent = self.car
            
        if 'materials' in parent:
            for material, amt in parent['materials'].items():
                print(material, amt)
                if material not in self.mat:
                    self.mat[material] = 0
                self.mat[material] += amt
            
        if 'options' in parent:
            for option, child in parent['options'].items():
                if child != -1:
                    self.sum_mat(child)
                else:
                    pass

    def get_cumul_weight(self, parent=None):
        
        if parent is None:
            parent = self.car
            self.edges = []

        if 'cumul_weight' not in parent:
            parent['cumul_weight'] = parent['weight']

        if 'options' in parent:
            for option, child in parent['options'].items():
                if child != -1:
                    parent['cumul_weight'] += child['weight']
                    self.get_cumul_weight(child)
                else:
                    pass
                
    def get_nodes(self, parent=None):
        
        if parent is None:
            parent = self.car

            self.nodes.append({
                'name': self.name,
                'addr': self.addr,
                'lat': self.user_lat,
                'lng': self.user_lng
            })

        print('Parent: ', parent)
        
        self.nodes.append({k: parent[k] for k in set(list(parent.keys())) - set(['options'])})

        if 'options' in parent:
            for option, child in parent['options'].items():
                if child != -1:
                    self.get_nodes(child)
                else:
                    pass
                
    def calc_edges(self, parent=None):
        
        if parent is None:
            parent = self.car
            
        if 'options' in parent:
            for option, child in parent['options'].items():

                if child == -1:
                    continue
                    
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

    def generatePlot(self):

        if len(self.nodes) == 0 or len(self.edges) == 0:
            return {}

        return {
            "layers" : {
                "scatter_plot": {
                    "type" : "ScatterplotLayer",
                    "data" : self.nodes,
                    "get_position" : "[lng, lat]",
                    "get_color" : [255, 0, 0],
                    "radius_scale" : 1,
                    "radius_min_pixels" : 2,
                    "radius_max_pixels" : 10,
                    "get_radius" : 10000,
                    "pickable" : True
                },
                "line_layer" : {
                    "type" : "LineLayer",
                    "edges" : self.edges,
                    "get_source_position" : "start",
                    "get_target_position" : "end",
                    "get_color" : [255, 255, 255],
                    "picking_radius" : 5,
                    "auto_highlight" : True,
                    "pickable" : True
                }
            },
            "mat" : self.mat,
            "kgm" : self.kgm,
            "name" : self.name,
            "details" : self.car
        }

