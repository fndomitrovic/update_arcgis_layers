# -*- coding: utf-8 -*-

import arcpy


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [Tool]


class Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Update Bike Layers"
        self.description = "This tool creates or updates the regional bike routes, local bike lanes, and Citi Bike station layers which are used in the PANYNJ Regional Bike Map."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter(
            displayName = "Output Folder",
            name = "folder_path",
            datatype = "DEFolder",
            parameterType = "Required",
            direction = "Input")

        param1 = arcpy.Parameter(
            displayName = "Map",
            name = "map",
            datatype = "GPMap",
            parameterType = "Required",
            direction = "Input")
            
        params = [param0, param1]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        import os, json, requests, arcpy

        folder_path = parameters[0].valueAsText
        my_map = parameters[1].valueAsText

        def osm_to_features(output_path, query, file_name):
            api_response = requests.get('http://overpass-api.de/api/interpreter', params={'data': query})
            if api_response.status_code == 200:
                try:
                    response_json = api_response.json()
                    def overpass_to_geojson(overpass_data):
                        geojson = {
                            'type': 'FeatureCollection',
                            'features': []
                        }
                        node_coordinates = {}
                        for element in overpass_data['elements']:
                            if element['type'] == 'node' and 'ways' not in element:  
                                node_coordinates[element['id']] = {
                                    'type': 'Feature',
                                    'geometry': {
                                        'type': 'Point',
                                        'coordinates': [element['lon'], element['lat']]
                                    },
                                    'properties': {}
                                }
                        ref_nodes = {}
                        for element in overpass_data['elements']:
                            if element['type']=='way' and 'tags' not in element:
                                ref_nodes[element['id']] = element['nodes']
                        for element in overpass_data['elements']:
                            if element['type'] == 'way' and 'tags' in element:
                                coordinates = [
                                    [node_coordinates[node_id]['geometry']['coordinates'][0],
                                     node_coordinates[node_id]['geometry']['coordinates'][1]]
                                    for node_id in element['nodes']
                                ]
                                properties = element.get('tags')
                                properties['osm_id'] = element.get('id')
                                geojson['features'].append({
                                    'type': 'Feature',
                                    'geometry': {
                                        'type': 'LineString',
                                        'coordinates': coordinates
                                    },
                                    'properties': properties
                                })
                            if element['type'] == 'relation' and 'tags' in element:
                                for member in element['members']:
                                    if member['type'] == 'way':
                                        nodes_list = ref_nodes[member['ref']]
                                        ref_coordinates = [
                                            [node_coordinates[node_id]['geometry']['coordinates'][0],
                                            node_coordinates[node_id]['geometry']['coordinates'][1]]
                                            for node_id in nodes_list
                                        ]
                                        properties = element.get('tags')
                                        properties['osm_id'] = element.get('id')
                                        geojson['features'].append({
                                            'type': 'Feature',
                                            'geometry': {
                                                'type': 'LineString',
                                                'coordinates': ref_coordinates
                                            },
                                            'properties': properties
                                        })
                            if element["type"]=="node" and "tags" in element: 
                                    geojson['features'].append({
                                        "type": "Feature",
                                        "geometry": {
                                            "type": "Point",
                                            "coordinates": [(element.get("lon")),(element.get("lat"))]
                                        },
                                        "properties": element.get("tags")
                                    })
                        return geojson
                    api_data = overpass_to_geojson(response_json)
                    feature_path = os.path.join(output_path,f'{file_name}.json')
                    with open(feature_path,'w') as file:
                        json.dump(api_data, file, indent=4)
                    arcpy.conversion.JSONToFeatures(feature_path, file_name)
                except json.JSONDecodeError as e:
                    print("Error parsing JSON:", e)
            else:
                print(f'Request failed with status code {api_response.status_code}')

        def custom_osm_fields(input_path,fields,file_name):
            with open(input_path,'r') as file: 
                python_data = json.load(file) 
            for feature in python_data['features']: 
                if 'properties' in feature:
                    properties = feature.get('properties') 
                stan_properties = {} 
                for field in fields: 
                    if field in properties:
                        stan_properties[field] = properties[field] 
                    else:
                        stan_properties[field] = 'no key'
                stan_properties['osm_id'] = feature['properties']['osm_id']
                feature['properties'] = stan_properties
            feature_path = os.path.join(os.path.dirname(input_path),f'{file_name}.json')
            with open(feature_path, 'w') as file:
                json.dump(python_data,file,indent=4)
            arcpy.conversion.JSONToFeatures(feature_path, file_name)

        def cb_to_features(output_path):
            api_response = requests.get('https://gbfs.lyft.com/gbfs/2.3/bkn/en/station_information.json')
            if api_response.status_code == 200:
                try: 
                    response_json = api_response.json() 
                    def cb_to_geojson(json_data):    
                        geojson = {
                            "type": "FeatureCollection",
                            "features": []
                        }
                        for feature in json_data['data']['stations']:
                            properties = {}
                            for key in feature:
                                if not isinstance(feature[key],dict):
                                    properties[key] = feature[key]
                            geojson['features'].append({
                                "type": "Feature",
                                "geometry": {
                                    "type": "Point",
                                    "coordinates": [(feature["lon"]), feature["lat"]]
                                },
                                "properties": properties
                            })
                        return geojson
                    api_data = cb_to_geojson(response_json) 
                    feature_path = os.path.join(output_path,'citibike_stations.json')
                    with open(feature_path,'w') as file:
                        json.dump(api_data, file, indent=4)
                except json.JSONDecodeError as e:
                    print("Error parsing JSON:", e)
                arcpy.conversion.JSONToFeatures(feature_path,'citibike_stations')
            else:
                print(f"Request failed with status code {response.status_code}")

        def symbolize(active_map):
            
            # Add & calculate NYCDOT bike lane class fields
            expression = 'calculate_code(!highway!,!cycleway!,!cycleway_left!,!cycleway_right!,!cycleway_both!,!bicycle!,!name!)'
            codeblock = '''
def calculate_code(highway,cycleway,cycleway_left,cycleway_right,cycleway_both,bicycle,name):
    if highway=='cycleway' or cycleway=='track' or cycleway_left=='track' or cycleway_right=='track' or cycleway_both=='track' or cycleway_right=='separate':
        return 'NYC DOT Class I'
    elif cycleway_left=='separate' or cycleway_both=='separate' or cycleway_left=='shared_lanec':
        return 'NYC DOT Class I'
    elif highway=='footway' and bicycle=='yes':
        return 'NYC DOT Class I'
    elif bicycle=='designated':
        if highway=='pedestrian' or highway=='path':
            return 'NYC DOT Class I'
        else:
            return 'NYC DOT Class IV'
    elif cycleway=='lane' or cycleway_left=='lane' or cycleway_right=='lane' or cycleway_both=='lane':
        return 'NYC DOT Class II'
    elif cycleway=='shared_lane' or cycleway_left=='shared_lane' or cycleway_right=='shared_lane' or cycleway_both=='shared_lane':
        return 'NYC DOT Class III'
    elif highway=='path' and bicycle=='yes':
        return 'Trail'
        '''
            arcpy.management.AddField('local_bikelanes','code','TEXT')
            arcpy.management.CalculateField('local_bikelanes','code',expression,'PYTHON3',codeblock)
            
            expression2 = 'calculate_desc(!code!)'
            codeblock2 = '''
def calculate_desc(code):
    if code=='NYC DOT Class I':
        return 'Protected bicycle lane with access point'
    elif code=='NYC DOT Class II':
        return 'Conventional bicycle lane'
    elif code=='NYC DOT Class III' or code=='NYC DOT Class IV':
        return 'Shared bicycle & vehicle lane'
    elif code=='Trail':
        return 'Trail bicycle path'
            '''
            arcpy.management.AddField('local_bikelanes','descriptor','TEXT')
            arcpy.management.CalculateField('local_bikelanes','descriptor',expression2,'PYTHON3',codeblock2)

            # Bike lane symbology
            bikelane_lyr = active_map.listLayers("local_bikelanes")[0]
            bikelane_sym = bikelane_lyr.symbology
            bikelane_sym.updateRenderer('UniqueValueRenderer') 
            bikelane_sym.renderer.fields = ['descriptor']
            
            # Symbolize NYC DOT bike lane classes
            for group in bikelane_sym.renderer.groups: 
                for item in group.items: 
                    if item.values==[['Protected bicycle lane with access point']]:
                        item.symbol.color = {'RGB':[0,147,83,100]} 
                    if item.values==[['Conventional bicycle lane']]:
                        item.symbol.color = {'RGB':[0,185,239,100]} 
                    if item.values==[['Shared bicycle & vehicle lane']]:
                        item.symbol.color = {'RGB':[180,95,165,100]} 
                    if item.values==[['Trail bicycle path']]:
                        item.symbol.applySymbolFromGallery('Dashed 4:4')
                        item.symbol.size = 1
                        item.symbol.color = {'RGB':[0,147,83,100]}
            bikelane_lyr.symbology = bikelane_sym

            # Symbolize Citi Bike stations
            lyr = active_map.listLayers('citibike_stations')[0]
            sym = lyr.symbology
            sym.renderer.symbol.color = {'RGB':[173,216,230,100]}
            sym.renderer.symbol.size = 4
            lyr.symbology = sym

            # Symbolize regional routes
            r_lyr = active_map.listLayers('regional_routes')[0]
            r_sym = r_lyr.symbology
            r_sym.renderer.symbol.applySymbolFromGallery('Dashed 2:2')
            r_sym.renderer.symbol.size = 0.5
            r_sym.renderer.symbol.color = {'RGB':[0,30,0,100]}
            r_lyr.symbology = r_sym

        bikelanes_query = '''
        [out:json];
        (
          way["bicycle"="designated"](40.2115, -75.0517, 41.7968, -72.6750);
          way["cycleway:left"="lane"](40.2115, -75.0517, 41.7968, -72.6750);
          way["cycleway:left"="separate"](40.2115, -75.0517, 41.7968, -72.6750);
          way["cycleway:left"="track"](40.2115, -75.0517, 41.7968, -72.6750);
          way["cycleway:left"="shared_busway"](40.2115, -75.0517, 41.7968, -72.6750);
          way["cycleway:left"="shared_lane"](40.2115, -75.0517, 41.7968, -72.6750);
          way["cycleway:right"="lane"](40.2115, -75.0517, 41.7968, -72.6750);
          way["cycleway:right"="separate"](40.2115, -75.0517, 41.7968, -72.6750);
          way["cycleway:right"="track"](40.2115, -75.0517, 41.7968, -72.6750);
          way["cycleway:right"="shared_busway"](40.2115, -75.0517, 41.7968, -72.6750);
          way["cycleway:right"="shared_lane"](40.2115, -75.0517, 41.7968, -72.6750);
          way["cycleway:both"="lane"](40.2115, -75.0517, 41.7968, -72.6750);
          way["cycleway:both"="separate"](40.2115, -75.0517, 41.7968, -72.6750);
          way["cycleway:both"="track"](40.2115, -75.0517, 41.7968, -72.6750);
          way["cycleway:both"="shared_busway"](40.2115, -75.0517, 41.7968, -72.6750);
          way["cycleway:both"="shared_lane"](40.2115, -75.0517, 41.7968, -72.6750);
          way["cycleway"="lane"](40.2115, -75.0517, 41.7968, -72.6750);
          way["cycleway"="track"](40.2115, -75.0517, 41.7968, -72.6750);
          way["cycleway"="opposite_track"](40.2115, -75.0517, 41.7968, -72.6750);
          way["cycleway"="share_busway"](40.2115, -75.0517, 41.7968, -72.6750);
          way["cycleway"="shared_lane"](40.2115, -75.0517, 41.7968, -72.6750);
          way["highway"="cycleway"](40.2115, -75.0517, 41.7968, -72.6750);
          way["highway"="footway"]["bicycle"="yes"]["footway"!="crossing"]["footway"!="sidewalk"](40.2115, -75.0517, 41.7968, -72.6750);
          way["highway"="path"]["bicycle"="yes"](40.2115, -75.0517, 41.7968, -72.6750);
          way["cycleway:left"="shared_lanec"](40.2115, -75.0517, 41.7968, -72.6750);
          way["cycleway:right"="shared_lanec"](40.2115, -75.0517, 41.7968, -72.6750);
        );
        out body;
        >;
        out skel qt;
        '''

        regional_routes = '''
        [out:json];
        (
          relation["type"="route"]["network"="rcn"](37.21306, -80.38999, 44.40282, -68.19693);
        );
        out body;
        >;
        out skel qt;
        '''

        project = arcpy.mp.ArcGISProject("CURRENT")
        active_map = project.listMaps(my_map)[0]
        
        osm_to_features(folder_path, bikelanes_query, 'bikelanes_defaultfields')
        osm_to_features(folder_path, regional_routes, 'regional_routes')
        active_map.addDataFromPath(arcpy.Describe('regional_routes').catalogPath)
        fields = ['cycleway','cycleway:left','cycleway:right','cycleway:both','highway','name','lanes','bicycle','footway']
        custom_osm_fields(os.path.join(folder_path,'bikelanes_defaultfields.json'),fields,'local_bikelanes')
        active_map.addDataFromPath(arcpy.Describe('local_bikelanes').catalogPath)
        cb_to_features(folder_path)
        active_map.addDataFromPath(arcpy.Describe('citibike_stations').catalogPath)

        symbolize(active_map)
        
        return
