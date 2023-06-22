class Configurator:

    def __init__(self):
        self.car = None
        self.kgm = 0
        self.mat = {}
        self.nodes = []
        self.edges = []

    def select_model(self, model):
        self.car = json.loads(json.dumps(
            getattr(local, 'models')[model]
        ))

    def select_option(self, option, choice):
        self.car['options'][option] = json.loads(json.dumps(
            getattr(local, option)[choice]
        ))

    def get_coords(self, addr):

        response = gmaps.geocode(addr)

        return response[0]['geometry']['location']['lat'], response[0]['geometry']['location']['lng']  

    def set_coords(self, parent=None):
        
        if parent is None:
            parent = self.car
        
        parent['lat'], parent['lng'] = self.get_coords(parent['addr'])
        
        if 'options' in parent:
            for option, child in parent['options'].items():
                self.set_coords(child)
                
    def sum_mat(self, parent=None):
        
        if parent is None:
            parent = self.car
            self.mat = {}
            
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
            self.nodes = []
        
        self.nodes.append({k: parent[k] for k in set(list(parent.keys())) - set(['options'])})

        if 'options' in parent:
            for option, child in parent['options'].items():
                self.get_nodes(child)
                
    def calc_edges(self, parent=None):
        
        if parent is None:
            parent = self.car
            self.edges = []

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
            
    def get_kgm(self):
        
        for edge in self.edges:
            self.kgm += edge['cumul_weight'] * edge['distance']
            
    def plot(self):
        
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=car.nodes,
            get_position="[lng, lat]",
            get_color=[255, 0, 0],  # Set color to red
            radius_scale=1,
            radius_min_pixels=5,
            radius_max_pixels=10,
            get_radius=10000,  # Set radius to 100 pixels
            pickable=True,
        )

        line_layer = pdk.Layer(
            "LineLayer",
            car.edges,
            get_source_position="start",
            get_target_position="end",
            get_color=[255, 255, 255],
            get_width=3,
            highlight_color=[255, 255, 255],
            picking_radius=10,
            auto_highlight=True,
            pickable=True,
        )

        view = pdk.ViewState(latitude=30, longitude=0, min_zoom=0.7, zoom=1.5, max_zoom=4)

        deck = pdk.Deck(layers=[line_layer, layer], initial_view_state=view)
        
        return deck