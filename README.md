# update_arcgis_layers

## About:
The code in this repository was used to create an ArcGIS regional bike infrastructure map that could be easily updated with the latest data. The Python scripts used in this project aimed to solve two issues with creating map layers by downloading open source data:
1. Needing to repeatedly download data for the layer to reflect recent changes
2. Infrequent updates to the source data

As a solution used to these problems, this project accessed bike lane data from Open Street Map and Citi Bike dock locations from Citi Bike's System Data using the two source's respective APIs. This project usings APIs - Application Programming Interfaces - to access continually updating data through code.

## Data sources:
### 1. Open Street Map: bike lanes
Open Street Map (OSM), according to their wiki, is a "free, editable map of the entire world that is being built by volunteers." It is a crowdsourced map with unlimited kinds of features. Open Street Map was an ideal source for bike lane data because it is continuously being updated by cyclists. In additon, with OSM's global scale it was possible to create a regional, as opposed to local, bike infrastructure map.  
  
You can browse OSM data on its website, and query and download OSM data through its Overpass API. OSM's Overpass API has a web interface, "Overpass Turbo", where you can build and view queries and download data. Alternatively, this project accessed OSM data using Overpass API's endpoint, a link to access an API through code. With this API endpoint, you can pass a query that will retrieve data from Open Street Map into the Python script, and eventually into an ArcGIS layer.

### 2. Citi Bike System Data
Citi Bike publishes updating, real-time datasets including dock locations and bike availability. This data can also be accessed through an API endpoint. However, no query is necessary as there are separate API endpoints specifically for dock locations, bike avilability, etc. 

## Setup:
This code was run in an ArcGIS notebook inside of a desktop ArcGIS Pro application. 

## How to use each function:

```python
cb_to_features(path)
```
#### Creates a layer of updating CitiBike dock locations
#### Input: 
- path = folder path to save CitiBike JSON data to (string)
#### Output: 
- JSON file of most recent CitiBike docks in GeoJSON format
  - location: input folder path
- ArcGIS feature class & layer of most recent CitiBike docks
  - location: ArcGIS Project geodatabase

```python
osm_to_features(path, query, file_name)
```
#### Creates a layer of any Open Street Map data
#### Input:
- path = folder path to save Open Street Map JSON data to (string)
- query = Overpass Query Langauge, one of Open Street Map's API's query languages, query* (string)
- file_name = name for output JSON file and ArcGIS feature class/layer (string)
#### Output:
- JSON file of queried Open Street Map data in GeoJSON format
  - location: input folder path
- ArcGIS feature class & layer of Open Street Map data
  - location: ArcGIS Project geodatabase
