# update_arcgis_layers

The code in this repository was used to create & update three layers (Local bike lanes, Regional bike routes, & Citi Bike stations) on the [PANYNJ Regional Bike Map](https://geoapps.gis.panynj.gov/portal/apps/webappviewer/index.html?id=7f496ee5f7d940e39ed4cd6af2b7435b) available on the PA Planning & Regional Development [Sharepoint](https://panynj.sharepoint.com/sites/PRD/SitePages/Bicycle%20Planning.aspx) page. This repository documents how to update these PANYNJ Regional Bike Map layers with the latest data & the code behind this process.
<br />
<br />

## Contents:
1. [Repository files](#repository-files)
1. [Project background](#project-background)
2. [Data sources](#data-sources)
3. [Using update_web_layers.pyt & updating the PANYNJ Regional Bike Map](Using-update_web_layers.pyt-&-updating-the-PANYNJ-Regional-Bike-Map)
4. [Functions.py documentation](#functions.py-setup)     
     a. [Setup](#setup)     
     b. [Using each functions.py function](#Using-each-functions.py-function)     
     c. [Building an Open Street Map Overpass API query](#Building-an-Open-Street-Map-Overpass-API-query)
5. [Potential errors & limitations](#Potential-errors-&-limitations)
<br />

## Repository files:
[update_web_layers.pyt](update_web_layers.pyt):
- ArcGIS Python toolbox file - Python code used to create & update PANYNJ Regional Bike Map layers adapted into an ArcGIS tool
- .pyt file can be uploaded to a desktop ArcGIS Pro project to create or update the 'Local Bike lanes,' 'Regional bike routes,' & 'Citi Bike stations' layers on the PANYNJ Regional Bike Map
- no code necessary, can all be done through ArcGIS Pro interface  

[functions.py](functions.py):
- commented Python file with code of three functions used inside update_web_layers_.pyt ArcGIS tool which can also be used on their own
  - functions utilizing Open Street Map can query for any Open Street Map data, not only the bike data used in this project
<br />

## Project background:

The Python scripts used in this project aim to solve two issues with creating map layers from downloaded open source data (e.g. downloading a shapefile from NYC Open Data & creating a layer from the shapefile through the ArcGIS interface):
1. Needing to repeatedly download data for the layer to reflect recent changes
2. Infrequent updates to the source data

As a solution used to these problems, this project retrieved bike lane data from Open Street Map and Citi Bike station locations from Citi Bike's Real-Time System Data using the two source's respective APIs. The project uses APIs (Application Programming Interfaces) to access continually updating data through code.
<br />
<br />

## Data sources:

### 1. Open Street Map: Local bike lanes & Regional routes
[Open Street Map](https://www.openstreetmap.org/#map=17/40.71119/-74.01014&layers=CD) (OSM) is a "free, editable map of the entire world that is being built by volunteers." It is a crowdsourced map with features including, but not limited to, infrastructure, natural features, points of interest, & geographic boundaries. Open Street Map was an ideal source for bike lane data because it is continuously being updated by local cyclists. In additon, with OSM's global scale it was possible to create a regional, as opposed to local, bike infrastructure map.  
  
You can browse OSM data on its website, and query & download OSM data through its Overpass API. OSM's Overpass API has a web interface, [Overpass Turbo](https://overpass-turbo.eu/), where you can build and view queries and download data. Alternatively, this project accessed OSM data using Overpass API's endpoint, a URL to access an API through code. With this API endpoint, you can write a query that will retrieve data from Open Street Map into a Python script that will then create an ArcGIS layer from the retrieved data.
<br />

### 2. Citi Bike System Data: Citi Bike docks
[Citi Bike](https://citibikenyc.com/system-data) publishes updating, real-time datasets including station locations and bike availability. This data can also be accessed through an API endpoint URL. However, no query is necessary as there are separate API endpoints specifically for dock locations, bike avilability, etc. 
<br />
<br />   

## Using update_web_layers.pyt & updating the PANYNJ Regional Bike Map

This repository's code was used to create map layers for local bike lanes, regional bike routes and Citi Bike stations that can be updated with the latest data each time the script is run in a desktop ArcGIS Pro application. The layers created from this script were then uploaded to the PA ArcGIS Online Portal and integrated into the PANYNJ Regional Bike Map ArcGIS Web App. However, the layers on this Web App are not automatically updated each time the script in the Desktop ArcGIS Pro is run. The update_web_layers.pyt Python toolbox creates (or updates if running more than once) the 'Local bike lanes,' 'Regional bike routes,' & 'Citi Bike stations' layers seen on the PANYNJ Regional Bike Map in a desktop ArcGIS Pro project. You can then use these layers to update their associated web layer on the PANYNJ Regional Bike Map or use them for another purpose.
<br />

### To use the 'Update Bike Layers' tool & update the PANYNJ Regional Bike Map:
1. Download [update_web_layers.pyt](update_web_layers.pyt)
2. Open a desktop ArcGIS Pro project
3. Open the Catalog Pane (under 'View' tab)
4. Right click on 'Toolboxes' & click 'Add Toolbox'
5. Navigate to & select update_web_layers.pyt and click 'OK'
6. Double click on the 'Update Bike Layers' tool of the 'update_web_layers.pyt' to open the tool
7. Set parameters:
   - Output folder: folder to save JSON files necessary to update web layers to
   - Map: map you want to add the layers to
8. Click 'Run'. The tool will take around 2 minutes to run.
9. Three layers should appear on the map: 'regional_routes,' 'local_bikelanes,' & 'citibike_stations'
     - if only 'citibike_stations' does not appear & there is an 'Update Bike Layers failed' message, see [Potential errors & limitations](#Potential-errors-&-limitations)
<br />

### Next steps to update the PANYNJ Regional Bike Map
10. In the upper right corner, log in to the PA ArcGIS Online Portal
    - needs to be an account with editing privileges for the layers on the PANYNJ Regional Bike Map - likely only on Leo Tsang's account under which the layers were originally uploaded
12. Right click on a layer and click, 'Sharing,' then 'Overwrite Web Layer'
13. Navigate to the matching web layer (see below) & click run
  - Click 'OK' on any prior warning message
  - Desktop ArcGIS layers & matching web layers:
    - Local bike lanes:
      - ArcGIS layer: 'local_bikelanes'
      - PA Portal feature layer: 'Local bike lanes'
    - Regional bike routes:
      - ArcGIS layer: 'regional_routes'
      - PA Portal feature layer: 'Regional bike routes'
    - Citi Bike stations:
      - ArcGIS layer: 'citibike_stations'
      - PA Portal feature layer: 'Citi Bike stations'
<br />

## Functions.py documentation     
The preceding ArcGIS Python toolbox was can be used to create three bike infrastructure layers which can optionally be used to update the PANYNJ Regional Bike Map. The following Python functions, available in [functions.py](functions.py) were used (slightly modified) in [update_web_layers.pyt](update_web_layers.pyt) but can also be run on their own. This section documents each function in [functions.py](functions.py) & how the Open Street Map functions can retrieve all types of OSM data (not only bike data).

## a. Setup
This code was run in an ArcGIS notebook inside of a desktop ArcGIS Pro application. You can create an ArcGIS notebook by clicking on the Insert tab in an ArcGIS Project, then clicking "New Notebook."
To run the following three functions, you will have to first import the following libraries/modules:
```python
import arcpy, os, json, requests
```
<br />

## b. Using each function in [functions.py](functions.py)
<br />

Notes: 
- for all path parameters, recommend using a raw string
e.g. instead of the path
```python
path = 'C:\Users\Flora\folder'
```
Write an 'r' first to make it a raw string - sometimes paths are not recognized if they are not a raw string
```python
path = r'C:\Users\Flora\folder'
```
- Each function will create new JSON files & ArcGIS feature classes/layers or update the file/feature class/layer if it already exists
  - An ArcGIS feature class is the tabular source data of a layer which is the feature class's visualization on a map
<br />

### 1. Create/update an ArcGIS layer of any Open Street Map data
```python
osm_to_features(path, query, file_name)
```

The PANYNJ Regional Bike Map used this function to retrieve bike lanes and regional bike routes, but by changing the query this function can retrieve any data from Open Street Map.

#### Input:
- path = folder path to save Open Street Map JSON data to (string)
- query = Overpass Query Langauge, one of Open Street Map's API's query languages, query - see [Building an Open Street Map Overpass API query](#building-an-open-street-map-overpass-api-query) (string)
- file_name = name for output JSON file and ArcGIS feature class/layer (string)
#### Output:
- JSON file of queried Open Street Map data in GeoJSON format
  - location: input folder path
- ArcGIS feature class & layer of Open Street Map data
  - location: ArcGIS project geodatabase
<br />

### 2. Create/update a new layer of OSM features with custom attributes
```python
standardize_fields(path, output_name, fields)
```
Because of OSM's crowdsourced nature, every feature as a different set of tags (attributes). When creating an ArcGIS layer from OSM data, in order to create a uniform attribute table, ArcGIS gives every feature the same keys (fields) as the first feature in the OSM dataset. If a feature doesn't have a given key, its value is null in the attribute table. Because of this, many tags are lost in the dataset, if the key does not appear in the first feature. This function allows a user to provide a list of keys to be included in the a new layer's attribute table. This step was necessary for this project in order to symbolize bike lanes by their tags. For more information on OSM's tag system, see [Building an Open Street Map Overpass API Query](#Building-an-Open-Street-Map-Overpass-API-query).

#### Input:
- path = path to JSON file created by osm_to_features() function (string)
- output_name = name of output ArcGIS layer (string)
- fields = list of keys to be included as fields in the output layer (list)

#### Output:
- JSON file of OSM data with standardized tags
  - location: input path folder
- ArcGIS feature class & layer of input OSM data with input keys as the fields in the layer attribute table
  - location: ArcGIS project geodatabase
<br />

### 3. Create/update a layer of updating CitiBike station locations
```python
cb_to_features(path)
```
#### Input: 
- path = folder path to save CitiBike JSON data to (string)
#### Output: 
- JSON file of most recent CitiBike stations in GeoJSON format
  - location: input folder path
- ArcGIS feature class & layer of most recent CitiBike docks
  - location: ArcGIS project geodatabase
<br />

## c. Building an Open Street Map Overpass API query
Open Street Map's Overpass API has its own internal query language, Overpass QL, to query and retrieve OSM data. 

Each line of the core of an Overpass QL has three components:
1. data type
2. tag(s)
3. geography

### 1. Data Type
The three data types in Open Street Map are nodes, ways, and relations. Nodes represent points, ways represent lines, and relations represent multiple nodes and/or ways. 
<br />

### 2. Tag(s)
OSM features are identified & described by a tag system. Each tag is a key value pair, such as "bicycle=designated", where the key functions like a column name and the value like a cell value. There are more than 3,000 keys alone used on Open Street Map, and you can find their associated information on OSM's [Taginfo](https://taginfo.openstreetmap.org/) site. 


Some features, such as local bike lanes, can have many identifying tags. For example, below is the query used to retrieve local bike lanes from Trenton, NJ, to Hartford, CT:
```python
bike_lanes = """
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
```
In this query, 26 different tags can retrieve bike lane infrastructure - protected bike lanes, conventional bike lanes, and signed shared bicycle & vehicle lanes.  
  
In contrast, regional cycle routes can be queried with only one line of tags:
```python
regional_routes = """
[out:json];
(
  relation["type"="route"]["network"="rcn"](37.21306, -80.38999, 44.40282, -68.19693);
);
out body;
>;
out skel qt;
"""
```
<br />

### 3. Geography
There are several ways to query for location. For this project, the query used a bounding box with four coordinates of the corners of the bounding box, but it is also possible to query by location name.
<br />
<br />

### Helpful resources for building queries:
1. ChatGPT
   - prompt with "Write an Overpass API query for [features] in [location]'
   - helps with writing the correct syntax, identifying what features are tagged as in OSM, & using operators for complex queries
2. [Overpass Turbo](https://overpass-turbo.eu/)
   - Overpass API web interface
   - build queries & display queried data
   - view JSON data of query before it is manipulated by Python scripts
3. Overpass Turbo Wizard
   - on Overpass Turbo website
   - if you know the tags the features you need, this tool can help you build a query
4. [Taginfo](https://taginfo.openstreetmap.org/)
   - OSM database of the meaning of different keys and key-value pairs
5. Open Street Map Wiki [Overpass QL documentation](https://wiki.openstreetmap.org/wiki/Overpass_API/Overpass_QL)
   - official documentation for OSM Overpass Query Language
<br />

## Potential errors & limitations
The main error when running these tools & functions is the script having trouble connecting with the API.   
1. Trouble connecting with OSM's Overpass API returns the following error message. Typically opening [Overpass Turbo]() on a web browser and running again resolves this issue.
```python
'Request failed with status code 407'
```
  
2. Trouble connecting with Citi Bike's API returns the following error message. For this error I have not yet found a workaround besides trying to run the tool/function at a different time. When running the Update Bike Layers tool, the output 'regional_routes' & 'local_bikelanes' will still be created without error even if the tool returns a 'Update Bike Layers failed' message when the 'citibike_stations' layer cannot be created.
```python
SSLError: HTTPSConnectionPool(host='gbfs.lyft.com', port=443): Max retries exceeded with url: /gbfs/2.3/bkn/en/station_information.json (Caused by SSLError(SSLError("bad handshake: Error([('SSL routines', 'tls_process_server_certificate', 'certificate verify failed')],)",),))
```

