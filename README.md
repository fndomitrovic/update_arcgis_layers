# update_arcgis_layers

Contents:
1. About
2. Data sources
3. Setup
4. How to use each function
5. Building an Open Street Map Overpass API query
6. Updating the PANYNJ Regional Bike Map layers

## About:
The code in this repository was used to create an ArcGIS regional bike infrastructure map that could be easily updated with the latest data. This code makes up the updating bike lane and Citi Bike dock layers on the [PANYNJ Regional Bike Map](https://geoapps.gis.panynj.gov/portal/apps/webappviewer/index.html?id=7f496ee5f7d940e39ed4cd6af2b7435b) on the PA Planning & Regional Development Bicycle Planning & Resources Sharepoint page.

The Python scripts used in this project aimed to solve two issues with creating map layers by downloading open source data:
1. Needing to repeatedly download data for the layer to reflect recent changes
2. Infrequent updates to the source data

As a solution used to these problems, this project accessed bike lane data from Open Street Map and Citi Bike dock locations from Citi Bike's System Data using the two source's respective APIs. This project usings APIs - Application Programming Interfaces - to access continually updating data through code.

## Data sources:
### 1. Open Street Map: bike lanes
Open Street Map (OSM), according to the OSM [Wiki](https://wiki.openstreetmap.org/wiki/Main_Page), is a "free, editable map of the entire world that is being built by volunteers." It is a crowdsourced map with unlimited kinds of features. Open Street Map was an ideal source for bike lane data because it is continuously being updated by cyclists. In additon, with OSM's global scale it was possible to create a regional, as opposed to local, bike infrastructure map.  
  
You can browse OSM data on its website, and query and download OSM data through its Overpass API. OSM's Overpass API has a web interface, "Overpass Turbo", where you can build and view queries and download data. Alternatively, this project accessed OSM data using Overpass API's endpoint, a link to access an API through code. With this API endpoint, you can pass a query that will retrieve data from Open Street Map into the Python script, and eventually into an ArcGIS layer.

### 2. Citi Bike System Data: Citi Bike docks
Citi Bike publishes updating, real-time datasets including dock locations and bike availability. This data can also be accessed through an API endpoint. However, no query is necessary as there are separate API endpoints specifically for dock locations, bike avilability, etc. 

## Setup:
This code was run in an ArcGIS notebook inside of a desktop ArcGIS Pro application. You can create an ArcGIS notebook by clicking on the Insert tab in an ArcGIS Project, then clicking "New Notebook."
To run the following two functions, you will have to first import the following libraries/modules:
```python
import arcpy, os, json, requests
```


## How to use each function:

```python
osm_to_features(path, query, file_name)
```
#### Creates a layer of any Open Street Map data. 

This project used the function to retrieve bike lanes and regional bike routes, but by changing the query this function can retrieve any data from Open Street Map.

#### Input:
- path = folder path to save Open Street Map JSON data to (string)
- query = Overpass Query Langauge, one of Open Street Map's API's query languages, query* (string)
- file_name = name for output JSON file and ArcGIS feature class/layer (string)
#### Output:
- JSON file of queried Open Street Map data in GeoJSON format
  - location: input folder path
- ArcGIS feature class & layer of Open Street Map data
  - location: ArcGIS Project geodatabase
 
```python
standardize_fields(path, output_name, fields)
```
#### Creates a new layer of OSM features with custom attributes
Because of OSM's crowdsourced nature, every feature as a different set of tags. When creating an ArcGIS layer from OSM data, in order to create a uniform attribute table, ArcGIS gives every feature the keys as the first feature in the OSM dataset. If a feature doesn't have a given key, its value is null in the attribute table. Because of this, many tags are lost in the dataset, if the key does not appear in the first feature. This function allows a user to provide a list of keys to be included in the a new layer's attribute table. This step was necessary for this project in order to symbolize bike lanes by their tags.

#### Input:
- path = path to JSON file created by osm_to_features() function (string)
- output_name = name of output ArcGIS layer (string)
- fields = list of keys to be included as fields in the output layer (list)

#### Output:
- JSON file of OSM data with standardized tags
  - location: input path folder
- ArcGIS feature class & layer of input OSM data with input keys as the fields in the layer attribute table
  - location: ArcGIS Project geodatabase

```python
cb_to_features(path)
```
#### Creates a layer of updating CitiBike dock locations.
#### Input: 
- path = folder path to save CitiBike JSON data to (string)
#### Output: 
- JSON file of most recent CitiBike docks in GeoJSON format
  - location: input folder path
- ArcGIS feature class & layer of most recent CitiBike docks
  - location: ArcGIS Project geodatabase
 
## Building an Open Street Map Overpass API query
Open Street Map's Overpass API has its own internal query language, Overpass QL, to query and retrieve OSM data. For this project, I used ChatGPT to help build the query with the correct Overpass API syntax.   

From Overpass API's web interface, Overpass Turbo, you can view and edit queries without having to go through the ArcGIS Python script. 

Each line of the core of an Overpass QL has three components:
1. data type
2. tag(s)
3. geography

#### 1. Data Type
The three data types in Open Street Map are nodes, ways, and relations. Nodes represent points, ways represent lines, and relations represent multiple nodes and/or ways. 

#### 2. Tag(s)
OSM features are identified & described by a tag system. Each tag is a key value pair, such as "bicycle=designated", where the key functions like a column name and the value like a cell value. There are more than 3,000 keys alone used on Open Street Map, and you can find their associated information on OSM's Taginfo site.


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
  
In contrast, regional cycle routes can be queried with only one group of tags:
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
ChatGPT can be a useful tool to figure out what different features are tagged as. Every OSM feature will also have a list of its tags when selected on the Open Street Map website.

#### 3. Geography
There are several ways to query for location. For this project, the query used a bounding box with four coordinates of the corners of the bounding box. It's also possible to query by location name.

## Updating the PANYNJ Regional Bike Map layers
The code in this repository was used to create layers for Open Street Map bike lanes and Citi Bike docks that can be updated with the latest data each time the script is run in a desktop ArcGIS Pro application. The layers created from this script were then uploaded to the PA Portal ArcGIS Online and integrated into the PANYNJ Regional Bike Map ArcGIS Web App. However, the layers on this Web App are not automatically updated each time the script in the Desktop ArcGIS Pro is run. 
The following is the workflow to update the layers on the PANYNJ Regional Bike Map Web App:

In a desktop ArcGIS Pro application:
1. Log in to the PANYNJ ArcGIS online portal
   - must log in to an account with editing priveleges for the layer, I used Leo Tsang's account to originally upload and update the layers
2. In an ArcGIS notebook, run all needed scripts (name of script in Github repo) to update the layers
3. To update the bike lanes layer, right click on the 'bikelanes_customfields' layer in the Contents pane, then click 'Overwrite Web Layer'
4. A pop up window of files uploaded on the ArcGIS Online PA Portal will appear - navigate to the 'Bike lanes - Flora' folder and click on the 'Bike lanes' feature layer.
5. Click run
6. To repeat for the Citi Bike docks layer, repeat steps 3-5, but navigate to 'Overwrite Web Layer' from the 'citibike_stations' layer and overwrite the 'CitiBike Docks' ArcGIS Online layer on the PA Portal
