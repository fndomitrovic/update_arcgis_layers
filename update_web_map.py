def update_web_map(folder_path):
    import os, json, requests, arcpy
    
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
        print("'bikelanes_defaultfields' JSON file & ArcGIS layer updated")

    def custom_osm_fields(input_path,fields):
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
        feature_path = os.path.join(os.path.dirname(input_path),'bikelanes_customfields.json')
        with open(feature_path, 'w') as file:
            json.dump(python_data,file,indent=4)
        arcpy.conversion.JSONToFeatures(feature_path,'bikelanes_customfields')
        print("'bikelanes_customfields' JSON file & ArcGIS layer updated")

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
        print("'citibike_stations' JSON file & ArcGIS layer updated")
        
    bikelanes_query = """
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
    """
    
    osm_to_features(folder_path, bikelanes_query, 'bikelanes_defaultfields')
    fields = ['cycleway','cycleway_left','cycleway_right','cycleway_both','highway','name','lanes','bicycle']
    custom_osm_fields(os.path.join(folder_path,'bikelanes_defaultfields.json'),fields)
    cb_to_features(folder_path)