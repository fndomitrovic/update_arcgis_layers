def osm_to_features(output_path, query, file_name):
    
    # Send the query to the Overpass API
    api_response = requests.get('http://overpass-api.de/api/interpreter', params={'data': query})

    # Check if the request was successful
    if api_response.status_code == 200:
        try:
            # Convert JSON recieved from Overpass API into a Python dictionary
            response_json = api_response.json()
 
            # Convert the Overpass API data to ArcGIS-readable GeoJSON format
            def overpass_to_geojson(overpass_data):
                
                # Set up structure of GeoJSON formatted file
                geojson = {
                    'type': 'FeatureCollection',
                    'features': []
                }
                
                # Create dictionary of OSM node IDs & their associated coordinates
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
                        
                # Create dictionary of 'ref' ID numbers & their nodes
                ref_nodes = {}
                for element in overpass_data['elements']:
                    if element['type']=='way' and 'tags' not in element:
                        ref_nodes[element['id']] = element['nodes']
                        
                # Write features into GeoJSON
                for element in overpass_data['elements']:
                    
                    # Create features for ways
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
                                          
                    # Create features for relations
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
                    
                    # Create features for nodes
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
            
            # Run function and write output GeoJSON into a file
            api_data = overpass_to_geojson(response_json)
            feature_path = os.path.join(output_path,f'{file_name}.json')
                
            with open(feature_path,'w') as file:
                json.dump(api_data, file, indent=4)
            print(f'GeoJSON file created: {file_name}.json')
                
            # Create an ArcGIS layer from the GeoJSON file just created
            arcpy.conversion.JSONToFeatures(feature_path, file_name)
            print(f'ArcGIS feature class & layer created: {file_name}')
            
        except json.JSONDecodeError as e:
            print('Error parsing JSON:', e)
    else:
        print(f'Request failed with status code {api_response.status_code}')


def standardize_osm_fields(input_path,fields):
    
    # Open input JSON file as a Python dictionary
    with open(input_path,'r') as file: 
        python_data = json.load(file) 
        
    # For each feature in input JSON data
    for feature in python_data['features']: 
        
        # Retrieve each feature's properties
        if 'properties' in feature:
            properties = feature.get('properties') 
        
        # Only add keys from input list to stan_properties dictionary
        stan_properties = {} 
        for field in fields: 
            if field in properties:
                stan_properties[field] = properties[field] 
            else:
                stan_properties[field] = 'no key'
        
        # Add OSM ID to properties
        stan_properties['osm_id'] = feature['properties']['osm_id']
        
        # Update properties 
        feature['properties'] = stan_properties 
    
    # Convert Python dictionary with updated properties into a JSON file
    file_name = f'{os.path.basename(input_path)[:-5]}_customfields.json'
    feature_path = os.path.join(os.path.dirname(input_path),file_name)
    with open(feature_path, 'w') as file:
        json.dump(python_data,file,indent=4)
    print(f"Custom properties GeoJSON file created: {file_name}")
    
    # Use JSON file just created to create an ArcGIS feature class & layer
    arcpy.conversion.JSONToFeatures(feature_path,file_name[:-5])
    print(f"ArcGIS feature class & layer created: {file_name}")
	


def cb_to_features(output_path):
    # Get data from Citi Bike's station information API endpoint
    api_response = requests.get('https://gbfs.lyft.com/gbfs/2.3/bkn/en/station_information.json')
    
    # Check if request was successful
    if api_response.status_code == 200:
        try: 
            # Convert JSON recieved from Citi Bike API into a Python dictionary
            response_json = api_response.json() 
            
            # Convert data from API into ArcGIS-readable GeoJSON format
            def cb_to_geojson(json_data):
                
                # Set up structure of GeoJSON formatted file
                geojson = {
                    "type": "FeatureCollection",
                    "features": []
                }
                
                # Write each feature into GeoJSON format
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
            
            # Write Python dictionary just created into a JSON file
            api_data = cb_to_geojson(response_json) 
            feature_path = os.path.join(output_path,'citibike_stations.json')
            with open(feature_path,'w') as file:
                json.dump(api_data, file, indent=4)
            print(f'Local JSON file created: citibike_stations.json')
            
        except json.JSONDecodeError as e:
            print("Error parsing JSON:", e)
        
        # Create ArcGIS feature class from GeoJSON file
        arcpy.conversion.JSONToFeatures(feature_path,'citibike_stations')
        print("Layer created: citibike_stations")
    
    else:
        print(f"Request failed with status code {response.status_code}")